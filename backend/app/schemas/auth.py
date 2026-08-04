"""Authentication-related Pydantic schemas."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Login request payload."""

    username: str = Field(..., min_length=2, max_length=128)
    password: str = Field(..., min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    """Registration request payload."""

    username: str = Field(..., min_length=2, max_length=128)
    password: str = Field(..., min_length=6, max_length=128)


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    user: "UserInfo"


class UserInfo(BaseModel):
    """Minimal user info returned with token."""

    id: int
    username: str
    is_admin: bool
    is_active: bool
    role_id: int | None = None
    role_name: str | None = None

    model_config = {"from_attributes": True}
