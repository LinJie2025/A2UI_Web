"""Chat API — POST /api/chat (SSE streaming endpoint)."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.chat import ChatRequest, SSEEvent
from app.services.chat_service import ChatService
from app.errors import AppError
from app.main import global_tools_cache

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])

chat_service = ChatService()


@router.post("/chat")
async def api_chat(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Stream a chat response via Server-Sent Events.

    Accepts a list of messages (and optional conversation_id), returns
    an SSE stream with events: text, tool_call, tool_result, done, error.

    Args:
        payload: Chat request with messages and optional conversation_id.
        db: Database session.
        current_user: Authenticated user.

    Returns:
        StreamingResponse with media_type text/event-stream.
    """
    # Convert messages to dicts
    messages = []
    for msg in payload.messages:
        msg_dict = {"role": msg.role, "content": msg.content}
        if msg.tool_calls:
            msg_dict["tool_calls"] = msg.tool_calls
        if msg.tool_call_id:
            msg_dict["tool_call_id"] = msg.tool_call_id
        if msg.name:
            msg_dict["name"] = msg.name
        messages.append(msg_dict)

    # Reload global tools if empty
    tools = global_tools_cache
    if not tools:
        logger.warning("Global tools cache empty — chat may have limited tool access.")

    async def event_generator():
        """Generate SSE text stream from chat service."""
        try:
            async for event in chat_service.stream_chat(
                user=current_user,
                messages=messages,
                conversation_id=payload.conversation_id,
                db=db,
                global_tools=tools,
            ):
                yield event.to_sse()
        except AppError as e:
            logger.warning(f"Chat error: {e.code} — {e.message}")
            yield SSEEvent("error", {
                "code": e.code,
                "message": e.message,
                "a2ui_error": True,  # signal frontend to render as A2UI error component
            }).to_sse()
        except Exception as e:
            logger.error(f"Chat stream error: {e}", exc_info=True)
            yield SSEEvent("error", {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again.",
                "a2ui_error": True,
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
