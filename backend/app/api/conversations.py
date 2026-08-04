"""Conversations API — list/get/delete conversations and messages."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.services.conversation_service import ConversationService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["conversations"])


def _conv_to_response(conv, msg_count: int = 0) -> dict:
    last_msg = None
    if conv.messages:
        last_message = conv.messages[-1]
        last_msg = (last_message.content or "")[:100] if last_message.content else None
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat() if conv.created_at else "",
        "updated_at": conv.updated_at.isoformat() if conv.updated_at else "",
        "message_count": msg_count or len(conv.messages),
        "last_message": last_msg,
    }


def _msg_to_response(msg) -> dict:
    return {
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "role": msg.role,
        "content": msg.content,
        "tool_calls_json": msg.tool_calls_json,
        "tool_call_id": msg.tool_call_id,
        "created_at": msg.created_at.isoformat() if msg.created_at else "",
    }


@router.get("/conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conversations = await ConversationService.list_conversations(db, current_user.id)
    result = []
    for conv in conversations:
        count = len(conv.messages)
        result.append(_conv_to_response(conv, count))
    return {"code": 0, "data": result, "message": "success"}


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conv = await ConversationService.get_conversation(db, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": "Conversation not found."})
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail={"code": 403, "data": None, "message": "Access denied."})

    messages = await ConversationService.get_messages(db, conversation_id)
    return {
        "code": 0,
        "data": {
            **_conv_to_response(conv, len(messages)),
            "messages": [_msg_to_response(m) for m in messages],
        },
        "message": "success",
    }


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conv = await ConversationService.get_conversation(db, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": "Conversation not found."})
    if conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail={"code": 403, "data": None, "message": "Access denied."})

    messages = await ConversationService.get_messages(db, conversation_id)
    return {"code": 0, "data": [_msg_to_response(m) for m in messages], "message": "success"}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conv = await ConversationService.get_conversation(db, conversation_id)
    if conv is None:
        raise HTTPException(status_code=404, detail={"code": 404, "data": None, "message": "Conversation not found."})
    if conv.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail={"code": 403, "data": None, "message": "Access denied."})

    await ConversationService.delete_conversation(db, conversation_id)
    return {"code": 0, "data": None, "message": "Conversation deleted."}
