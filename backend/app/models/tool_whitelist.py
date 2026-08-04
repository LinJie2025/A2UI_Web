"""ToolWhitelist ORM model."""

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ToolWhitelist(Base):
    """Maps a role to allowed tool names (composite unique constraint)."""

    __tablename__ = "tool_whitelist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(256), nullable=False)

    # Relationships
    role: Mapped["Role"] = relationship("Role", back_populates="tool_whitelist")

    __table_args__ = (UniqueConstraint("role_id", "tool_name", name="uq_role_tool"),)

    def __repr__(self) -> str:
        return f"<ToolWhitelist(role_id={self.role_id}, tool_name='{self.tool_name}')>"
