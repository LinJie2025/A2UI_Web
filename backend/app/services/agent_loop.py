"""Agentic Loop — the core async generator that drives LLM + tool calling.

The loop streams LLM content deltas to the client, intercepts tool_calls,
executes them via MCP, and feeds results back for further reasoning.

Key constraints:
- MAX_LOOPS = 20 (prevents infinite loops)
- Each iteration has a 30-second timeout (asyncio.wait_for)
"""

import asyncio
import json
import logging
from typing import AsyncIterator
from app.services.llm_client import LLMClient
from app.services.mcp_client import MCPClient
from app.schemas.chat import SSEEvent

logger = logging.getLogger(__name__)

MAX_LOOPS = 20
LOOP_TIMEOUT = 30.0


class AgentLoop:
    """Drives the LLM → tool_call → tool_result → LLM cycle."""

    def __init__(self, llm_client: LLMClient, mcp_client: MCPClient):
        """Initialize the agent loop.

        Args:
            llm_client: LLM client instance.
            mcp_client: MCP client instance for tool execution.
        """
        self._llm = llm_client
        self._mcp = mcp_client

    async def run(
        self,
        messages: list[dict],
        tools: list[dict],
    ) -> AsyncIterator[SSEEvent]:
        """Run the agentic loop, yielding SSE events for the client.

        Args:
            messages: Full message history including system prompt.
            tools: OpenAI-format tool definitions.

        Yields:
            SSEEvent objects: text, tool_call, tool_result, done, error.
        """
        loop_count = 0
        current_messages = list(messages)

        while loop_count < MAX_LOOPS:
            loop_count += 1
            logger.debug(f"AgentLoop iteration {loop_count}/{MAX_LOOPS}")

            try:
                # Stream LLM response with 30s timeout
                stream = self._llm.chat_stream(current_messages, tools if tools else None)

                collected_content = ""
                collected_tool_calls: list[dict] = []
                finish_reason: str | None = None

                async def _consume_stream():
                    nonlocal collected_content, collected_tool_calls, finish_reason
                    async for chunk in stream:
                        choices = chunk.get("choices", [])
                        if not choices:
                            continue
                        delta = choices[0].get("delta", {})
                        finish_reason = choices[0].get("finish_reason") or finish_reason

                        # Text content delta
                        if delta.get("content"):
                            collected_content += delta["content"]
                            yield SSEEvent("text", {"delta": delta["content"]})

                        # Tool calls delta
                        if delta.get("tool_calls"):
                            for tc in delta["tool_calls"]:
                                idx = tc.get("index", 0)
                                while len(collected_tool_calls) <= idx:
                                    collected_tool_calls.append({
                                        "id": "",
                                        "type": "function",
                                        "function": {"name": "", "arguments": ""},
                                    })
                                if tc.get("id"):
                                    collected_tool_calls[idx]["id"] = tc["id"]
                                func = tc.get("function", {})
                                if func.get("name"):
                                    collected_tool_calls[idx]["function"]["name"] = func["name"]
                                if func.get("arguments"):
                                    collected_tool_calls[idx]["function"]["arguments"] += func["arguments"]

                async for sse_event in _consume_stream():
                    yield sse_event

                # If we collected tool calls, execute them
                if collected_tool_calls and finish_reason == "tool_calls":
                    # Add assistant message with tool_calls to history
                    assistant_msg: dict = {
                        "role": "assistant",
                        "content": collected_content or None,
                        "tool_calls": collected_tool_calls,
                    }
                    current_messages.append(assistant_msg)

                    for tc in collected_tool_calls:
                        tool_name = tc["function"]["name"]
                        try:
                            tool_args = json.loads(tc["function"]["arguments"])
                        except json.JSONDecodeError:
                            tool_args = {}

                        yield SSEEvent("tool_call", {
                            "id": tc["id"],
                            "name": tool_name,
                            "arguments": tool_args,
                        })

                        # Execute the tool via MCP
                        try:
                            result = await asyncio.wait_for(
                                self._mcp.call_tool(tool_name, tool_args),
                                timeout=LOOP_TIMEOUT,
                            )
                            yield SSEEvent("tool_result", {
                                "id": tc["id"],
                                "name": tool_name,
                                "result": result,
                            })

                            # Append tool result to messages
                            current_messages.append({
                                "role": "tool",
                                "tool_call_id": tc["id"],
                                "content": json.dumps(result, ensure_ascii=False),
                            })
                        except asyncio.TimeoutError:
                            logger.error(f"Tool {tool_name} timed out after {LOOP_TIMEOUT}s")
                            current_messages.append({
                                "role": "tool",
                                "tool_call_id": tc["id"],
                                "content": json.dumps({"error": f"Tool '{tool_name}' timed out after {LOOP_TIMEOUT}s"}),
                            })
                        except Exception as e:
                            logger.error(f"Tool {tool_name} failed: {e}")
                            current_messages.append({
                                "role": "tool",
                                "tool_call_id": tc["id"],
                                "content": json.dumps({"error": str(e)}),
                            })

                    continue  # Next loop iteration

                # No tool calls — assistant has finished
                break

            except asyncio.TimeoutError:
                logger.error(f"AgentLoop iteration {loop_count} timed out.")
                yield SSEEvent("error", {
                    "code": "TIMEOUT",
                    "message": "AI response timed out. Please try again.",
                    "a2ui_error": True,
                })
                break
            except Exception as e:
                logger.error(f"AgentLoop error: {e}", exc_info=True)
                yield SSEEvent("error", {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Please try again.",
                    "a2ui_error": True,
                })
                break

        if loop_count >= MAX_LOOPS:
            logger.warning("AgentLoop reached MAX_LOOPS limit.")
            yield SSEEvent("error", {"message": "Reached maximum tool call iterations."})

        yield SSEEvent("done", {"status": "completed"})
