"""Admin API — User CRUD endpoints (admin-only)."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_admin_user
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["admin-users"])


def _user_to_response(user: User) -> dict:
    """Convert a User ORM instance to a response dict."""
    return {
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "role_id": user.role_id,
        "role_name": user.role.name if user.role else None,
        "created_at": user.created_at.isoformat() if user.created_at else "",
        "updated_at": user.updated_at.isoformat() if user.updated_at else "",
    }


@router.get("/admin/users")
async def list_users(
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all users (admin only)."""
    users = await UserService.list_users(db)
    return {
        "code": 0,
        "data": [_user_to_response(u) for u in users],
        "message": "success",
    }


@router.get("/admin/users/{user_id}")
async def get_user(
    user_id: int,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single user by ID."""
    user = await UserService.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": "User not found."})
    return {
        "code": 0,
        "data": _user_to_response(user),
        "message": "success",
    }


@router.post("/admin/users")
async def create_user(
    payload: UserCreate,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new user."""
    try:
        user = await UserService.create_user(db, payload.model_dump())
        return {
            "code": 0,
            "data": _user_to_response(user),
            "message": "User created.",
        }
    except ValueError as e:
        raise HTTPException(status_code=409, detail={"code": 409, "data": None, "message": str(e)})


@router.put("/admin/users/{user_id}")
async def update_user(
    user_id: int,
    payload: UserUpdate,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing user."""
    try:
        update_data = payload.model_dump(exclude_unset=True)
        user = await UserService.update_user(db, user_id, update_data)
        return {
            "code": 0,
            "data": _user_to_response(user),
            "message": "User updated.",
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": str(e)})


@router.post("/admin/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Toggle user active status."""
    try:
        user = await UserService.toggle_active(db, user_id)
        return {
            "code": 0,
            "data": _user_to_response(user),
            "message": f"User {'activated' if user.is_active else 'deactivated'}.",
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": str(e)})
