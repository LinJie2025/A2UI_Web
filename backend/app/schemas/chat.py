"""Chat-related Pydantic schemas."""

from pydantic import BaseModel, Field


class ChatMessageItem(BaseModel):
    """A single message in the chat request."""

    role: str = Field(..., description="One of: user, assistant, system, tool")
    content: str | None = None
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None
    name: str | None = None


class ChatRequest(BaseModel):
    """Chat SSE streaming request payload."""

    messages: list[ChatMessageItem] = Field(..., min_length=1)
    conversation_id: int | None = None


class SSEEvent:
    """Base SSE event emitted by the agentic loop."""

    def __init__(self, event: str, data: dict):
        self.event = event
        self.data = data

    def to_sse(self) -> str:
        """Format as SSE string."""
        import json

        return f"event: {self.event}\ndata: {json.dumps(self.data, ensure_ascii=False)}\n\n"


class ToolDef(BaseModel):
    """MCP tool definition."""

    name: str
    description: str = ""
    inputSchema: dict = Field(default_factory=dict)
