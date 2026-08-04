"""Admin API — Role CRUD endpoints (admin-only)."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_admin_user
from app.services.role_service import RoleService
from app.schemas.role import RoleCreate, RoleUpdate

logger = logging.getLogger(__name__)

router = APIRouter(tags=["admin-roles"])


def _role_to_response(role) -> dict:
    """Convert a Role ORM instance to a response dict."""
    tool_names = [tw.tool_name for tw in (role.tool_whitelist or [])]
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "created_at": role.created_at.isoformat() if role.created_at else "",
        "tool_names": tool_names,
    }


@router.get("/admin/roles")
async def list_roles(
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all roles."""
    roles = await RoleService.list_roles(db)
    return {
        "code": 0,
        "data": [_role_to_response(r) for r in roles],
        "message": "success",
    }


@router.get("/admin/roles/{role_id}")
async def get_role(
    role_id: int,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single role."""
    role = await RoleService.get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": "Role not found."})
    return {
        "code": 0,
        "data": _role_to_response(role),
        "message": "success",
    }


@router.post("/admin/roles")
async def create_role(
    payload: RoleCreate,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new role."""
    try:
        role = await RoleService.create_role(db, payload.model_dump())
        return {
            "code": 0,
            "data": _role_to_response(role),
            "message": "Role created.",
        }
    except ValueError as e:
        raise HTTPException(status_code=409, detail={"code": 409, "data": None, "message": str(e)})


@router.put("/admin/roles/{role_id}")
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing role."""
    try:
        update_data = payload.model_dump(exclude_unset=True)
        role = await RoleService.update_role(db, role_id, update_data)
        return {
            "code": 0,
            "data": _role_to_response(role),
            "message": "Role updated.",
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": str(e)})


@router.delete("/admin/roles/{role_id}")
async def delete_role(
    role_id: int,
    _admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a role."""
    try:
        await RoleService.delete_role(db, role_id)
        return {
            "code": 0,
            "data": None,
            "message": "Role deleted.",
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": str(e)})
