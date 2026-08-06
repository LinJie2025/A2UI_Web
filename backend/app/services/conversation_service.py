"""Conversation & Message CRUD service — v2 with unified message model."""

import logging
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation, Message

logger = logging.getLogger(__name__)

# When computing conversation summary, skip these message roles/types
_SKIP_LAST_MSG_TYPES = {"tool"}


class ConversationService:
    """Manage chat conversations and their messages."""

    @staticmethod
    async def list_conversations(db: AsyncSession, user_id: int) -> list[Conversation]:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_conversation(db: AsyncSession, conversation_id: int) -> Conversation | None:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_conversation(db: AsyncSession, user_id: int, title: str | None = None) -> Conversation:
        conv = Conversation(user_id=user_id, title=title)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        return conv

    @staticmethod
    async def update_title(db: AsyncSession, conversation_id: int, title: str | None) -> Conversation | None:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conv = result.scalar_one_or_none()
        if conv is None:
            return None
        conv.title = title
        conv.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(conv)
        return conv

    @staticmethod
    async def delete_conversation(db: AsyncSession, conversation_id: int) -> None:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conv = result.scalar_one_or_none()
        if conv is None:
            raise ValueError(f"Conversation {conversation_id} not found.")
        await db.delete(conv)
        await db.commit()

    @staticmethod
    async def get_messages(db: AsyncSession, conversation_id: int) -> list[Message]:
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def save_message(
        db: AsyncSession,
        conversation_id: int,
        role: str,
        *,
        message_type: str = "chat",
        content: str | None = None,
        tool_calls_json: str | None = None,
        tool_call_id: str | None = None,
        tool_name: str | None = None,
        a2ui_jsonl: str | None = None,
        action_name: str | None = None,
        action_status: str | None = None,
        flush_only: bool = False,
    ) -> Message:
        """Create a message.

        If flush_only=True, only flush (no commit) — for batch inserts
        within a transaction.
        """
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            message_type=message_type,
            content=content,
            tool_calls_json=tool_calls_json,
            tool_call_id=tool_call_id,
            tool_name=tool_name,
            a2ui_jsonl=a2ui_jsonl,
            action_name=action_name,
            action_status=action_status,
        )
        db.add(msg)
        if flush_only:
            await db.flush()
        else:
            await db.commit()
            await db.refresh(msg)
        return msg

    @staticmethod
    async def get_message_count(db: AsyncSession, conversation_id: int) -> int:
        result = await db.execute(
            select(func.count()).where(Message.conversation_id == conversation_id)
        )
        return result.scalar() or 0

    @staticmethod
    async def get_last_user_content(db: AsyncSession, conversation_id: int) -> str | None:
        """Get the most recent non-tool, non-a2ui action message content for summary."""
        result = await db.execute(
            select(Message.content)
            .where(
                Message.conversation_id == conversation_id,
                Message.role != "tool",
            )
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        row = result.scalar_one_or_none()
        return row
