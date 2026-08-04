"""Conversation-related Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel


class MessageResponse(BaseModel):
    """A single message in a conversation."""

    id: int
    conversation_id: int
    role: str
    content: str | None = None
    tool_calls_json: str | None = None
    tool_call_id: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationResponse(BaseModel):
    """Conversation summary returned in list view."""

    id: int
    user_id: int
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    last_message: str | None = None

    model_config = {"from_attributes": True}


class ConversationDetailResponse(BaseModel):
    """Conversation with full messages."""

    id: int
    user_id: int
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse] = []

    model_config = {"from_attributes": True}
