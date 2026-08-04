"""Authentication API endpoints — login / register."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import register, login
from app.middleware.auth_middleware import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])


@router.post("/auth/register")
async def api_register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user account.

    Args:
        payload: Registration data with username and password.
        db: Database session.

    Returns:
        Standard API response with the new user data.
    """
    try:
        user = await register(db, payload.username, payload.password)
        return {
            "code": 0,
            "data": {
                "id": user.id,
                "username": user.username,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            },
            "message": "Registration successful.",
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 409, "data": None, "message": str(e)},
        )


@router.post("/auth/login")
async def api_login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate a user and return a JWT access token.

    Args:
        payload: Login credentials.
        db: Database session.

    Returns:
        Standard API response with JWT token and user info.
    """
    try:
        result = await login(db, payload.username, payload.password)
        return {
            "code": 0,
            "data": result,
            "message": "Login successful.",
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 401, "data": None, "message": str(e)},
        )


@router.get("/auth/me")
async def api_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile.

    Args:
        current_user: Authenticated user from JWT.

    Returns:
        Standard API response with current user data.
    """
    role_name = current_user.role.name if current_user.role else None
    return {
        "code": 0,
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "is_admin": current_user.is_admin,
            "is_active": current_user.is_active,
            "role_id": current_user.role_id,
            "role_name": role_name,
        },
        "message": "success",
    }
