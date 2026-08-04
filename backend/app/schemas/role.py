"""Role-related Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    """Payload for creating a new role."""

    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = None
    tool_names: list[str] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    """Payload for updating an existing role."""

    name: str | None = Field(None, min_length=1, max_length=128)
    description: str | None = None
    tool_names: list[str] | None = None


class RoleResponse(BaseModel):
    """Role data returned by the API."""

    id: int
    name: str
    description: str | None = None
    created_at: datetime
    tool_names: list[str] = Field(default_factory=list)

    model_config = {"from_attributes": True}
