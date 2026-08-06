"""Conversation-related Pydantic schemas — v2 with unified Message type."""

from datetime import datetime
from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """A single message in a conversation."""
    id: int
    conversation_id: int
    role: str
    message_type: str = "chat"
    content: str | None = None
    tool_calls_json: str | None = None
    tool_call_id: str | None = None
    tool_name: str | None = None
    a2ui_jsonl: str | None = None
    action_name: str | None = None
    action_status: str | None = None
    action_result: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationSummary(BaseModel):
    """Conversation summary returned in list view."""
    id: int
    user_id: int
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    last_message: str | None = None

    model_config = {"from_attributes": True}


class ConversationDetail(BaseModel):
    """Conversation detail with full message list."""
    id: int
    user_id: int
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    last_message: str | None = None
    messages: list[MessageResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class ConversationUpdate(BaseModel):
    """Request body for updating conversation metadata."""
    title: str | None = Field(None, min_length=1, max_length=256)
