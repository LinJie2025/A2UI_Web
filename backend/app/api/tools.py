"""Tools API — GET /api/tools (returns available tools for current user)."""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.services.system_prompt import SystemPromptBuilder
from app.main import global_tools_cache

logger = logging.getLogger(__name__)

router = APIRouter(tags=["tools"])


@router.get("/tools")
async def api_tools(
    current_user: User = Depends(get_current_user),
):
    """Return the list of tools available to the current user.

    Tools are filtered by the user's role tool_whitelist.

    Args:
        current_user: Authenticated user.

    Returns:
        Standard API response with list of available tools.
    """
    available = SystemPromptBuilder.get_available_tools(current_user, global_tools_cache)
    return {
        "code": 0,
        "data": {
            "tools": available,
            "total": len(available),
        },
        "message": "success",
    }
