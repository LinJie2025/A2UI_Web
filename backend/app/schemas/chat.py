"""Chat-related Pydantic schemas — unified API format v2."""

from pydantic import BaseModel, Field


class ChatMessageMeta(BaseModel):
    """Optional metadata for A2UI form submissions."""
    action_name: str | None = None
    form_data: dict = Field(default_factory=dict)


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(default="user", description="user | assistant | system | tool")
    content: str | None = None
    meta: ChatMessageMeta | None = None


class ChatRequest(BaseModel):
    """Unified chat SSE streaming request payload.

    Supports both:
      - Normal chat:  message.content = "hello"
      - A2UI submit:  message.meta.action_name = "create_contact"
    """
    conversation_id: int | None = None
    message: ChatMessage


class SSEEvent:
    """SSE event emitted by the agentic loop."""

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
