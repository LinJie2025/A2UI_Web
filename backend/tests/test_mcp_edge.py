"""Edge case tests for MCP client and AgentLoop."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.mcp_client import MCPClient
from app.services.agent_loop import AgentLoop
from app.services.llm_client import LLMClient
from app.schemas.chat import SSEEvent


class TestMCPClientEdge:
    """MCP client edge case tests."""

    @pytest.mark.asyncio
    async def test_list_tools_bearer_token(self):
        """Verify Bearer token is included in Authorization header."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": []}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            client = MCPClient(base_url="http://test:8069", token="custom-token-abc")
            await client.list_tools()
            await client.close()

            call_args = mock_post.call_args
            headers = call_args.kwargs.get("headers", {})
            assert headers["Authorization"] == "Bearer custom-token-abc"

    @pytest.mark.asyncio
    async def test_mcp_url_construction(self):
        """Verify MCP URL is {base_url}/mcp."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": []}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            client = MCPClient(base_url="http://odoo:8069/", token="token")
            await client.list_tools()
            await client.close()

            call_args = mock_post.call_args
            assert call_args.args[0] == "http://odoo:8069/mcp"

    @pytest.mark.asyncio
    async def test_mcp_error_response(self):
        """MCP error response raises ValueError."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": {"code": -32601, "message": "Method not found"}}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            client = MCPClient(base_url="http://test:8069", token="token")
            with pytest.raises(ValueError, match="MCP error"):
                await client.list_tools()
            await client.close()

    @pytest.mark.asyncio
    async def test_call_tool_empty_result(self):
        """Call tool with empty result."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": {}}
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            client = MCPClient(base_url="http://test:8069", token="token")
            result = await client.call_tool("empty_tool", {})
            await client.close()

            assert result == {}


class TestAgentLoopEdge:
    """AgentLoop edge case tests."""

    @pytest.mark.asyncio
    async def test_max_loops_reached(self):
        """Agent loop should terminate after MAX_LOOPS with error event."""
        llm_client = MagicMock(spec=LLMClient)
        mcp_client = MagicMock(spec=MCPClient)
        mcp_client.call_tool = AsyncMock(return_value={"result": "ok"})

        async def mock_stream(*args, **kwargs):
            # Always return tool_calls to force re-loop
            yield {
                "choices": [
                    {
                        "delta": {
                            "tool_calls": [
                                {
                                    "index": 0,
                                    "id": "call_loop",
                                    "function": {"name": "loop_tool", "arguments": '{"x":1}'},
                                }
                            ]
                        },
                        "finish_reason": "tool_calls",
                    }
                ]
            }

        llm_client.chat_stream = mock_stream

        loop = AgentLoop(llm_client, mcp_client)
        # Override MAX_LOOPS for testing speed
        import app.services.agent_loop as al
        original_max = al.MAX_LOOPS
        al.MAX_LOOPS = 3

        events = []
        try:
            async for event in loop.run([{"role": "user", "content": "Loop test"}], []):
                events.append(event)
        finally:
            al.MAX_LOOPS = original_max

        # Should have error event about max loops
        error_events = [e for e in events if e.event == "error"]
        assert len(error_events) >= 1
        assert any("maximum" in e.data.get("message", "").lower() for e in error_events)

    @pytest.mark.asyncio
    async def test_tool_json_decode_error(self):
        """Agent loop handles malformed tool arguments gracefully."""
        llm_client = MagicMock(spec=LLMClient)
        mcp_client = MagicMock(spec=MCPClient)
        mcp_client.call_tool = AsyncMock(return_value={"result": "ok"})

        async def mock_stream(*args, **kwargs):
            yield {
                "choices": [
                    {
                        "delta": {
                            "tool_calls": [
                                {
                                    "index": 0,
                                    "id": "call_bad_json",
                                    "function": {
                                        "name": "bad_tool",
                                        "arguments": "not valid json {{{",
                                    },
                                }
                            ]
                        },
                        "finish_reason": "tool_calls",
                    }
                ]
            }
            # Second call: text response
            yield {
                "choices": [
                    {
                        "delta": {"content": "Done."},
                        "finish_reason": "stop",
                    }
                ]
            }

        llm_client.chat_stream = mock_stream

        loop = AgentLoop(llm_client, mcp_client)
        events = []
        async for event in loop.run([{"role": "user", "content": "Test"}], []):
            events.append(event)

        # Should still complete with done event (malformed JSON defaults to {})
        done_events = [e for e in events if e.event == "done"]
        assert len(done_events) == 1

    @pytest.mark.asyncio
    async def test_no_finish_reason_proceeds(self):
        """When no finish_reason is set, loop should break (no tool calls = done)."""
        llm_client = MagicMock(spec=LLMClient)
        mcp_client = MagicMock(spec=MCPClient)

        async def mock_stream(*args, **kwargs):
            yield {
                "choices": [
                    {
                        "delta": {"content": "Simple response without finish_reason"},
                    }
                ]
            }

        llm_client.chat_stream = mock_stream

        loop = AgentLoop(llm_client, mcp_client)
        events = []
        async for event in loop.run([{"role": "user", "content": "Hi"}], []):
            events.append(event)

        done_events = [e for e in events if e.event == "done"]
        assert len(done_events) == 1
