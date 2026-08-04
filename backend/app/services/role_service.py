"""Role CRUD service — manage roles and their tool whitelists."""

import logging
from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from app.models.tool_whitelist import ToolWhitelist

logger = logging.getLogger(__name__)


class RoleService:
    """Administrative role and tool whitelist management."""

    @staticmethod
    async def list_roles(db: AsyncSession) -> list[Role]:
        """List all roles with tool whitelists loaded.

        Args:
            db: Database session.

        Returns:
            List of Role instances.
        """
        result = await db.execute(
            select(Role).order_by(Role.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_role(db: AsyncSession, role_id: int) -> Role | None:
        """Get a single role by ID.

        Args:
            db: Database session.
            role_id: Role primary key.

        Returns:
            Role instance or None.
        """
        result = await db.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_role(db: AsyncSession, data: dict) -> Role:
        """Create a new role with optional tool whitelist.

        Args:
            db: Database session.
            data: Dict with 'name', 'description', 'tool_names'.

        Returns:
            The created Role.

        Raises:
            ValueError: If role name already exists.
        """
        existing = await db.execute(select(Role).where(Role.name == data["name"]))
        if existing.scalar_one_or_none():
            raise ValueError(f"Role '{data['name']}' already exists.")

        role = Role(
            name=data["name"],
            description=data.get("description"),
        )
        db.add(role)
        await db.flush()

        # Create tool whitelist entries
        for tool_name in data.get("tool_names", []):
            tw = ToolWhitelist(role_id=role.id, tool_name=tool_name)
            db.add(tw)

        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def update_role(db: AsyncSession, role_id: int, data: dict) -> Role:
        """Update an existing role and optionally its tool whitelist.

        Args:
            db: Database session.
            role_id: Role primary key.
            data: Fields to update.

        Returns:
            The updated Role.
        """
        result = await db.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()
        if role is None:
            raise ValueError(f"Role {role_id} not found.")

        if "name" in data and data["name"]:
            role.name = data["name"]
        if "description" in data:
            role.description = data["description"]

        await db.flush()

        # Replace tool whitelist if provided
        if "tool_names" in data and data["tool_names"] is not None:
            await db.execute(
                delete(ToolWhitelist).where(ToolWhitelist.role_id == role_id)
            )
            for tool_name in data["tool_names"]:
                tw = ToolWhitelist(role_id=role_id, tool_name=tool_name)
                db.add(tw)

        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def delete_role(db: AsyncSession, role_id: int) -> None:
        """Delete a role (cascades to tool whitelist).

        Args:
            db: Database session.
            role_id: Role primary key.

        Raises:
            ValueError: If role not found.
        """
        result = await db.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()
        if role is None:
            raise ValueError(f"Role {role_id} not found.")
        await db.delete(role)
        await db.commit()

    @staticmethod
    async def get_tool_whitelist(db: AsyncSession, role_id: int) -> list[str]:
        """Get the list of tool names for a role.

        Args:
            db: Database session.
            role_id: Role primary key.

        Returns:
            List of tool name strings.
        """
        result = await db.execute(
            select(ToolWhitelist).where(ToolWhitelist.role_id == role_id)
        )
        return [tw.tool_name for tw in result.scalars().all()]

    @staticmethod
    async def set_tool_whitelist(
        db: AsyncSession, role_id: int, tool_names: list[str]
    ) -> None:
        """Replace the tool whitelist for a role.

        Args:
            db: Database session.
            role_id: Role ID.
            tool_names: New list of tool names.
        """
        await db.execute(
            delete(ToolWhitelist).where(ToolWhitelist.role_id == role_id)
        )
        for tool_name in tool_names:
            tw = ToolWhitelist(role_id=role_id, tool_name=tool_name)
            db.add(tw)
        await db.commit()
