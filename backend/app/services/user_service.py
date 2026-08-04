"""User CRUD service — admin operations on user accounts."""

import logging
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.role import Role
from app.services.crypto_service import encrypt
from app.services.auth_service import hash_password

logger = logging.getLogger(__name__)


class UserService:
    """Administrative user management."""

    @staticmethod
    async def list_users(db: AsyncSession) -> list[User]:
        """List all users with their roles loaded.

        Args:
            db: Database session.

        Returns:
            List of User instances.
        """
        result = await db.execute(
            select(User).order_by(User.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int) -> User | None:
        """Get a single user by ID.

        Args:
            db: Database session.
            user_id: User primary key.

        Returns:
            User instance or None.
        """
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, data: dict) -> User:
        """Create a new user (admin operation).

        Args:
            db: Database session.
            data: User creation fields.

        Returns:
            The created User.

        Raises:
            ValueError: If username already exists.
        """
        existing = await db.execute(select(User).where(User.username == data["username"]))
        if existing.scalar_one_or_none():
            raise ValueError(f"Username '{data['username']}' already taken.")

        user = User(
            username=data["username"],
            password_hash=hash_password(data.get("password", "changeme")),
            is_active=data.get("is_active", True),
            is_admin=data.get("is_admin", False),
            role_id=data.get("role_id"),
        )

        if data.get("odoo_api_key"):
            user.odoo_api_key_encrypted = encrypt(data["odoo_api_key"])

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, data: dict) -> User:
        """Update an existing user.

        Args:
            db: Database session.
            user_id: User primary key.
            data: Fields to update.

        Returns:
            The updated User.

        Raises:
            ValueError: If user not found or username conflict.
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise ValueError(f"User {user_id} not found.")

        if "username" in data and data["username"] != user.username:
            existing = await db.execute(
                select(User).where(User.username == data["username"])
            )
            if existing.scalar_one_or_none():
                raise ValueError(f"Username '{data['username']}' already taken.")
            user.username = data["username"]

        if "password" in data and data["password"]:
            user.password_hash = hash_password(data["password"])

        if "is_active" in data:
            user.is_active = data["is_active"]

        if "is_admin" in data:
            user.is_admin = data["is_admin"]

        if "role_id" in data:
            user.role_id = data["role_id"]

        if "odoo_api_key" in data:
            user.odoo_api_key_encrypted = encrypt(data["odoo_api_key"]) if data["odoo_api_key"] else None

        user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def toggle_active(db: AsyncSession, user_id: int) -> User:
        """Toggle the is_active flag for a user.

        Args:
            db: Database session.
            user_id: User primary key.

        Returns:
            The updated User.
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise ValueError(f"User {user_id} not found.")
        user.is_active = not user.is_active
        user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)
        return user
