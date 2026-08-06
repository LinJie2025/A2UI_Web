"""Conversations API — list/get/update/delete (v2 with Pydantic schemas)."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.services.conversation_service import ConversationService
from app.schemas.conversation import (
    ConversationSummary, ConversationDetail, ConversationUpdate, MessageResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["conversations"])


def _msg_to_response(msg) -> dict:
    """Convert ORM Message to dict suitable for Pydantic validation."""
    return {
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "role": msg.role,
        "message_type": msg.message_type or "chat",
        "content": msg.content,
        "tool_calls_json": msg.tool_calls_json,
        "tool_call_id": msg.tool_call_id,
        "tool_name": msg.tool_name,
        "a2ui_jsonl": msg.a2ui_jsonl,
        "action_name": msg.action_name,
        "action_status": msg.action_status,
        "action_result": msg.action_result,
        "created_at": msg.created_at.isoformat() if msg.created_at else "",
    }


def _conv_to_summary(conv, msg_count: int, last_msg: str | None) -> dict:
    """Build conversation summary dict."""
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat() if conv.created_at else "",
        "updated_at": conv.updated_at.isoformat() if conv.updated_at else "",
        "message_count": msg_count,
        "last_message": last_msg,
    }


def _get_last_display_message(messages) -> str | None:
    """Get the last non-tool message content for display (max 100 chars)."""
    for msg in reversed(messages):
        if msg.role != "tool" and msg.content:
            return msg.content[:100]
    return None


@router.get("/conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all conversations for the current user."""
    conversations = await ConversationService.list_conversations(db, current_user.id)
    result: list[dict] = []
    for conv in conversations:
        msgs = conv.messages or []
        count = len(msgs)
        last = _get_last_display_message(msgs)
        item = _conv_to_summary(conv, count, last)
        # Validate through Pydantic
        valid = ConversationSummary.model_validate(item)
        result.append(valid.model_dump())
    return {"code": 0, "data": result, "message": "success"}


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get conversation detail with all messages."""
    conv = await ConversationService.get_conversation(db, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")

    msgs = conv.messages or []
    count = len(msgs)
    last = _get_last_display_message(msgs)
    detail = ConversationDetail.model_validate({
        **_conv_to_summary(conv, count, last),
        "messages": [_msg_to_response(m) for m in msgs],
    })
    return {"code": 0, "data": detail.model_dump(), "message": "success"}


@router.put("/conversations/{conversation_id}")
async def update_conversation(
    conversation_id: int,
    payload: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update conversation metadata (e.g. title)."""
    conv = await ConversationService.get_conversation(db, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied.")

    updated = await ConversationService.update_title(db, conversation_id, payload.title)
    if updated is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return {"code": 0, "data": ConversationSummary.model_validate(
        _conv_to_summary(updated, await ConversationService.get_message_count(db, conversation_id), None)
    ).model_dump(), "message": "Updated."}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation and all its messages."""
    conv = await ConversationService.get_conversation(db, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    if conv.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied.")

    await ConversationService.delete_conversation(db, conversation_id)
    return {"code": 0, "data": None, "message": "Conversation deleted."}
