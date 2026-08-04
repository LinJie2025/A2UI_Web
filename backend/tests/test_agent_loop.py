"""Tests for Agentic Loop."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.agent_loop import AgentLoop
from app.services.llm_client import LLMClient
from app.services.mcp_client import MCPClient
from app.schemas.chat import SSEEvent


@pytest.mark.asyncio
async def test_agent_loop_simple_text_response():
    """Test agent loop with a simple text response (no tool calls)."""
    llm_client = MagicMock(spec=LLMClient)
    mcp_client = MagicMock(spec=MCPClient)

    async def mock_stream(*args, **kwargs):
        yield {
            "choices": [
                {
                    "delta": {"content": "Hello, how can I help?"},
                    "finish_reason": "stop",
                }
            ]
        }

    llm_client.chat_stream = mock_stream

    loop = AgentLoop(llm_client, mcp_client)
    events = []
    async for event in loop.run([{"role": "user", "content": "Hi"}], []):
        events.append(event)

    assert len(events) >= 2  # text + done
    text_events = [e for e in events if e.event == "text"]
    assert len(text_events) >= 1
    assert "Hello" in text_events[0].data.get("delta", "")

    done_events = [e for e in events if e.event == "done"]
    assert len(done_events) == 1


@pytest.mark.asyncio
async def test_agent_loop_tool_call():
    """Test agent loop with a tool call → tool result cycle."""
    llm_client = MagicMock(spec=LLMClient)
    mcp_client = MagicMock(spec=MCPClient)
    mcp_client.call_tool = AsyncMock(return_value={"result": "success"})

    call_count = [0]

    async def mock_stream(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            # First iteration: tool call
            yield {
                "choices": [
                    {
                        "delta": {
                            "tool_calls": [
                                {
                                    "index": 0,
                                    "id": "call_001",
                                    "function": {"name": "test_tool", "arguments": '{"param":"value"}'},
                                }
                            ]
                        },
                        "finish_reason": "tool_calls",
                    }
                ]
            }
        else:
            # Second iteration: final response
            yield {
                "choices": [
                    {
                        "delta": {"content": "The result is success."},
                        "finish_reason": "stop",
                    }
                ]
            }

    llm_client.chat_stream = mock_stream

    loop = AgentLoop(llm_client, mcp_client)
    events = []
    async for event in loop.run([{"role": "user", "content": "Test"}], []):
        events.append(event)

    # Verify tool_call and tool_result events emitted
    tool_call_events = [e for e in events if e.event == "tool_call"]
    assert len(tool_call_events) == 1
    assert tool_call_events[0].data["name"] == "test_tool"

    tool_result_events = [e for e in events if e.event == "tool_result"]
    assert len(tool_result_events) == 1

    done_events = [e for e in events if e.event == "done"]
    assert len(done_events) == 1
