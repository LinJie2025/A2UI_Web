"""A2UI Action-related Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, Field


class A2UIActionSubmitRequest(BaseModel):
    """Request body for POST /api/a2ui/submit."""

    conversation_id: int = Field(default=0, ge=0, description="Conversation ID (0 = create new conversation)")
    action_name: str = Field(..., min_length=1, max_length=128, description="Button action name, e.g. 'create_order'")
    form_data: dict[str, object] = Field(
        default_factory=dict, description="User-submitted form field values"
    )


class A2UIActionResponse(BaseModel):
    """A single A2UI action record returned in list/detail views."""

    id: int
    conversation_id: int
    action_name: str
    form_data: dict[str, object] | None = None
    status: str
    result_summary: str | None = None
    error_detail: str | None = None
    tool_call_id: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class A2UIActionListResponse(BaseModel):
    """Wrapper for the actions list response."""

    code: int = 0
    data: list[A2UIActionResponse] = []
    message: str = "success"
