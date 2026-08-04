"""Authentication service: registration, login, JWT management."""

import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)

# bcrypt with 12 rounds
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt.

    Args:
        password: Plaintext password.

    Returns:
        Bcrypt hash string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash.

    Args:
        plain_password: The plaintext password to check.
        hashed_password: The stored bcrypt hash.

    Returns:
        True if the password matches.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Create a JWT access token for the given user.

    Args:
        user_id: The user's primary key.

    Returns:
        Encoded JWT string.
    """
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """Decode a JWT access token and return the user ID.

    Args:
        token: The JWT string.

    Returns:
        User ID if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub", ""))
        return user_id
    except (JWTError, ValueError) as e:
        logger.warning(f"JWT decode failed: {e}")
        return None


async def register(db: AsyncSession, username: str, password: str) -> User:
    """Register a new user.

    Args:
        db: Database session.
        username: Desired username.
        password: Plaintext password.

    Returns:
        The newly created User.

    Raises:
        ValueError: If the username is already taken.
    """
    existing = await db.execute(select(User).where(User.username == username))
    if existing.scalar_one_or_none() is not None:
        raise ValueError(f"Username '{username}' is already taken.")

    user = User(
        username=username,
        password_hash=hash_password(password),
        is_active=True,
        is_admin=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login(db: AsyncSession, username: str, password: str) -> dict:
    """Authenticate a user and return a JWT token.

    Args:
        db: Database session.
        username: The username.
        password: The plaintext password.

    Returns:
        Dict with access_token and user info.

    Raises:
        ValueError: If credentials are invalid or user is inactive.
    """
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise ValueError("Invalid username or password.")
    if not user.is_active:
        raise ValueError("This account has been deactivated.")
    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid username or password.")

    access_token = create_access_token(user.id)
    role_name = user.role.name if user.role else None

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "role_id": user.role_id,
            "role_name": role_name,
        },
    }


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Fetch a user by primary key.

    Args:
        db: Database session.
        user_id: The user's ID.

    Returns:
        User instance or None.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
