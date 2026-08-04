"""Conversation & Message CRUD service."""

import logging
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation, Message

logger = logging.getLogger(__name__)


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
        content: str | None = None,
        tool_calls_json: str | None = None,
        tool_call_id: str | None = None,
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls_json=tool_calls_json,
            tool_call_id=tool_call_id,
        )
        db.add(msg)
        await db.commit()
        await db.refresh(msg)
        return msg

    @staticmethod
    async def get_message_count(db: AsyncSession, conversation_id: int) -> int:
        result = await db.execute(
            select(func.count()).where(Message.conversation_id == conversation_id)
        )
        return result.scalar() or 0
