"""A2UI Action ORM model — tracks form submissions per conversation."""

from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class A2UIAction(Base):
    __tablename__ = "a2ui_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    action_name: Mapped[str] = mapped_column(String(128), nullable=False)
    form_data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    # submitted → processing → done / failed / interrupted
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="submitted")
    result_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool_call_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False
    )

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="a2ui_actions")
