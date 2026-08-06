"""Conversation and Message ORM models.

v2 Message model — single table for all message types:
  - chat (role: user/assistant/tool) — normal conversation
  - a2ui_action (role: user) — A2UI form submission
"""

from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Conversation(Base):
    """A chat conversation owned by a user."""

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", lazy="selectin",
        cascade="all, delete-orphan", order_by="Message.created_at",
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title='{self.title}')>"


class Message(Base):
    """A single message within a conversation.

    Supports both normal chat messages and A2UI form submissions
    in a single table, differentiated by message_type.
    """

    __tablename__ = "messages"
    __table_args__ = (
        Index("idx_messages_conv_created", "conversation_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("conversations.id"), nullable=False, index=True
    )

    # ── Core identity ──────────────────────────────────────────────
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    # "user" | "assistant" | "tool"
    message_type: Mapped[str] = mapped_column(String(32), nullable=False, default="chat")
    # "chat" | "a2ui_action"

    # ── Chat fields ─────────────────────────────────────────────────
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool_calls_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool_call_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tool_name: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # ── A2UI fields ─────────────────────────────────────────────────
    a2ui_jsonl: Mapped[str | None] = mapped_column(Text, nullable=True)
    action_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    action_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # "submitted" | "processing" | "done" | "failed"
    action_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    # LLM response text for form submissions (e.g. "已创建联系人 张三")

    # ── Timestamps ──────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role='{self.role}', type='{self.message_type}')>"
