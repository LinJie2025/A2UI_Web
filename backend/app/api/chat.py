"""Chat API — POST /api/chat (SSE streaming, unified v2).

Handles both normal chat and A2UI form submissions through a single endpoint.
"""

import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.middleware.auth_middleware import get_current_user
from app.schemas.chat import ChatRequest, SSEEvent
from app.services.chat_service import ChatService
from app.services import mcp_client
from app.config import settings
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
    """Unified streaming chat endpoint.

    Request format:
        {
          "conversation_id": 123 | null,
          "message": {
            "role": "user",
            "content": "Hey, find contacts",
            "meta": {                          // optional, for A2UI form submission
              "action_name": "create_contact",
              "form_data": {"name": "Zhang"}
            }
          }
        }

    Returns SSE stream with events:
        user_message_saved, text, tool_call, tool_result, done, error.
    """
    msg = payload.message
    meta = msg.meta
    action_name = meta.action_name if meta else None
    form_data = meta.form_data if meta else None

    # Try to reload tools if cache is empty (e.g. Odoo MCP wasn't reachable at startup)
    tools = global_tools_cache
    if not tools:
        logger.warning("Global tools cache empty, attempting reload from MCP...")
        try:
            client = mcp_client.MCPClient(
                base_url=settings.ODOO_MCP_URL,
                token=settings.ODOO_MCP_DEFAULT_TOKEN,
            )
            result = await client.list_tools()
            global_tools_cache.clear()
            global_tools_cache.extend(result)
            tools = global_tools_cache
            logger.info(f"Reloaded {len(tools)} tools from MCP per-request.")
        except Exception as e:
            logger.warning(f"Failed to reload tools from MCP: {e}")

    async def event_generator():
        try:
            async for event in chat_service.stream_chat(
                user=current_user,
                message_content=msg.content,
                conversation_id=payload.conversation_id,
                db=db,
                global_tools=tools,
                action_name=action_name,
                form_data=form_data,
            ):
                yield event.to_sse()
        except AppError as e:
            logger.warning(f"Chat error: {e.code} — {e.message}")
            yield SSEEvent("error", {
                "code": e.code,
                "message": e.message,
                "a2ui_error": True,
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
