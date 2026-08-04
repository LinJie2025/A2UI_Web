"""Chat service — orchestrates the full chat flow from request to SSE stream."""

import json
import logging
from datetime import datetime, timezone
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.conversation import Conversation, Message
from app.schemas.chat import SSEEvent
from app.services.llm_client import LLMClient
from app.services.mcp_client import MCPClient
from app.services.system_prompt import SystemPromptBuilder
from app.services.agent_loop import AgentLoop
from app.services.crypto_service import decrypt
from app.config import settings

logger = logging.getLogger(__name__)

MAX_RESULT_SUMMARY_LENGTH = 200


def _extract_summary(content: str) -> str:
    if not content:
        return ""
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            msg = data.get("message") or data.get("result") or data.get("summary")
            if msg and isinstance(msg, str):
                return str(msg)[:MAX_RESULT_SUMMARY_LENGTH]
    except (json.JSONDecodeError, TypeError):
        pass
    return content.strip()[:MAX_RESULT_SUMMARY_LENGTH]


class ChatService:
    def __init__(self):
        self._llm_client = LLMClient()

    def _get_mcp_client(self, user: User) -> MCPClient:
        token = settings.ODOO_MCP_DEFAULT_TOKEN
        if user.odoo_api_key_encrypted:
            token = decrypt(user.odoo_api_key_encrypted)
        return MCPClient(base_url=settings.ODOO_MCP_URL, token=token)

    async def stream_chat(
        self,
        user: User,
        messages: list[dict],
        conversation_id: int | None,
        db: AsyncSession,
        global_tools: list[dict],
        a2ui_action_id: int | None = None,
    ) -> AsyncIterator[SSEEvent]:
        from app.services.conversation_service import ConversationService
        from app.services.a2ui_action_service import A2UIActionService

        conv_service = ConversationService()
        a2ui_svc = A2UIActionService()

        system_prompt, filtered_tools = SystemPromptBuilder.build(user, global_tools)

        if conversation_id:
            conversation = await conv_service.get_conversation(db, conversation_id)
            if conversation is None or conversation.user_id != user.id:
                conversation = await conv_service.create_conversation(db, user.id, title=None)
                conversation_id = conversation.id
        else:
            conversation = await conv_service.create_conversation(db, user.id, title=None)
            conversation_id = conversation.id

        last_user_msg = messages[-1] if messages else None
        if last_user_msg and last_user_msg.get("role") == "user":
            content = last_user_msg.get("content", "")
            if not a2ui_action_id:
                await conv_service.save_message(
                    db, conversation_id=conversation_id, role="user", content=content,
                )
            if conversation.title is None and content:
                title = content[:50] + ("..." if len(content) > 50 else "")
                conversation.title = title
                await db.commit()

        if a2ui_action_id:
            await a2ui_svc.update_status(db, a2ui_action_id, "processing")

        full_messages = [{"role": "system", "content": system_prompt}]
        full_messages.extend(messages)

        mcp_client = self._get_mcp_client(user)
        loop = AgentLoop(self._llm_client, mcp_client)

        collected_content = ""
        collected_tool_calls: list[dict] = []
        a2ui_error_detail: str | None = None

        try:
            async for event in loop.run(full_messages, filtered_tools):
                if event.event == "text":
                    collected_content += event.data.get("delta", "")
                elif event.event == "tool_call":
                    collected_tool_calls.append(event.data)
                elif event.event == "error":
                    a2ui_error_detail = event.data.get("message", "")

                if event.event == "done":
                    event.data["conversation_id"] = conversation_id

                yield event

        finally:
            await mcp_client.close()

        tool_calls_json = json.dumps(collected_tool_calls, ensure_ascii=False) if collected_tool_calls else None
        await conv_service.save_message(
            db, conversation_id=conversation_id, role="assistant",
            content=collected_content or None, tool_calls_json=tool_calls_json,
        )

        if a2ui_action_id:
            if a2ui_error_detail:
                await a2ui_svc.update_status(
                    db, a2ui_action_id, "failed", error_detail=a2ui_error_detail,
                )
            else:
                summary = _extract_summary(collected_content) if collected_content else None
                last_tool_call_id = collected_tool_calls[-1].get("tool_call_id") if collected_tool_calls else None
                await a2ui_svc.update_status(
                    db, a2ui_action_id, "done", result_summary=summary, tool_call_id=last_tool_call_id,
                )

        if a2ui_action_id:
            await a2ui_svc.cleanup_interrupted(db, conversation_id)

        conversation.updated_at = datetime.now(timezone.utc)
        await db.commit()
