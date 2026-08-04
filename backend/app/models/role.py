"""Role ORM model."""

from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Role(Base):
    """User role with associated tool whitelist entries."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    users: Mapped[list["User"]] = relationship("User", back_populates="role", lazy="selectin")
    tool_whitelist: Mapped[list["ToolWhitelist"]] = relationship(
        "ToolWhitelist", back_populates="role", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}')>"
