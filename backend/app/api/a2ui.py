"""A2UI Action API — submit A2UI form actions and query history."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.a2ui_action import A2UIActionSubmitRequest, A2UIActionListResponse
from app.services.a2ui_action_service import A2UIActionService
from app.services.conversation_service import ConversationService
from app.services.chat_service import ChatService
from app.schemas.chat import SSEEvent
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["a2ui"])

a2ui_action_service = A2UIActionService()
conv_service = ConversationService()
chat_service = ChatService()


def _build_user_message(action_name: str, form_data: dict) -> str:
    fields_desc = "\n".join(
        f"  - {key}: {value}" for key, value in form_data.items()
    )
    return (
        f"用户提交了「{action_name}」操作，表单数据如下：\n"
        f"{fields_desc}\n\n"
        f"请根据以上数据执行相应的操作。"
    )


@router.post("/a2ui/submit")
async def a2ui_submit(
    payload: A2UIActionSubmitRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conversation_id = payload.conversation_id
    if conversation_id and conversation_id > 0:
        conversation = await conv_service.get_conversation(db, conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail={
                "code": 404, "data": None, "message": "Conversation not found."
            })
        if conversation.user_id != user.id:
            raise HTTPException(status_code=403, detail={
                "code": 403, "data": None, "message": "Access denied."
            })
    else:
        conversation = await conv_service.create_conversation(db, user.id, title=None)
        conversation_id = conversation.id

    action = await a2ui_action_service.create_action(
        db=db,
        conversation_id=conversation_id,
        action_name=payload.action_name,
        form_data=payload.form_data,
    )

    user_message_text = _build_user_message(payload.action_name, payload.form_data)
    await conv_service.save_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=user_message_text,
    )

    messages = [{"role": "user", "content": user_message_text}]

    from app.main import global_tools_cache

    async def event_generator():
        try:
            async for event in chat_service.stream_chat(
                user=user,
                messages=messages,
                conversation_id=conversation_id,
                db=db,
                global_tools=global_tools_cache,
                a2ui_action_id=action.id,
            ):
                if event.event == "done":
                    event.data["conversation_id"] = conversation_id
                    event.data["a2ui_action_id"] = action.id
                yield event.to_sse()
        except Exception as e:
            error_msg = str(e)
            logger.error(f"A2UI action {action.id} failed: {error_msg}")
            await a2ui_action_service.update_status(
                db=db,
                action_id=action.id,
                status="failed",
                error_detail=error_msg[:500],
            )
            yield SSEEvent("error", {
                "code": "A2UI_ACTION_FAILED",
                "message": error_msg,
            }).to_sse()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/conversations/{conversation_id}/actions")
async def get_conversation_actions(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conversation = await conv_service.get_conversation(db, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail={
            "code": 404, "data": None, "message": "Conversation not found."
        })
    if conversation.user_id != user.id:
        raise HTTPException(status_code=403, detail={
            "code": 403, "data": None, "message": "Access denied."
        })

    actions = await a2ui_action_service.get_actions_by_conversation(db, conversation_id)
    return A2UIActionListResponse(code=0, data=actions, message="success").model_dump()
