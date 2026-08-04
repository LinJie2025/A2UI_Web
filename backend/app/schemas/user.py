"""User-related Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Payload for creating a new user."""

    username: str = Field(..., min_length=2, max_length=128)
    password: str = Field(..., min_length=6, max_length=128)
    is_active: bool = True
    is_admin: bool = False
    role_id: int | None = None
    odoo_api_key: str | None = None


class UserUpdate(BaseModel):
    """Payload for updating an existing user."""

    username: str | None = Field(None, min_length=2, max_length=128)
    password: str | None = Field(None, min_length=6, max_length=128)
    is_active: bool | None = None
    is_admin: bool | None = None
    role_id: int | None = None
    odoo_api_key: str | None = None


class UserResponse(BaseModel):
    """User data returned by the API."""

    id: int
    username: str
    is_active: bool
    is_admin: bool
    role_id: int | None = None
    role_name: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
