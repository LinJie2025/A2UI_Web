"""Chat service — unified streaming chat with A2UI support (v2).

Supports both normal chat and A2UI form submissions through a single flow.
Uses delayed batch save for transactional integrity.
"""

import json
import logging
from datetime import datetime, timezone
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.chat import SSEEvent
from app.services.llm_client import LLMClient
from app.form_templates import get_template, resolve_hidden_fields
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
        message_content: str | None,
        conversation_id: int | None,
        db: AsyncSession,
        global_tools: list[dict],
        *,
        action_name: str | None = None,
        form_data: dict | None = None,
    ) -> AsyncIterator[SSEEvent]:
        """Unified streaming chat — handles both normal chat and A2UI form submissions.

        Each message is stateless: only the system prompt + current message
        are sent to the LLM. No conversation history is loaded.

        Args:
            user: Authenticated user.
            message_content: User message text (None for A2UI form-only submits).
            conversation_id: Existing conversation ID (None = create new).
            db: Async database session.
            global_tools: Cached MCP tool list.
            action_name: A2UI form action name (e.g. "create_contact").
            form_data: A2UI form data.
        """
        from app.services.conversation_service import ConversationService

        conv_service = ConversationService()

        # ── Build system prompt & filter tools ──────────────────────────
        system_prompt, filtered_tools = SystemPromptBuilder.build(user, global_tools)

        # ── Get or create conversation ──────────────────────────────────
        if conversation_id:
            conversation = await conv_service.get_conversation(db, conversation_id)
            if conversation is None or conversation.user_id != user.id:
                conversation = await conv_service.create_conversation(db, user.id)
                conversation_id = conversation.id
        else:
            conversation = await conv_service.create_conversation(db, user.id)
            conversation_id = conversation.id

        # ── Inject hidden field values ────────────────────────────────────
        if action_name and form_data:
            tmpl = get_template(action_name)
            if tmpl:
                form_data = resolve_hidden_fields(
                    tmpl, form_data, user.username, user.id
                )
            else:
                logger.warning(
                    "No template found for action_name=%s — hidden fields not injected",
                    action_name,
                )

        # ── Build user message content ──────────────────────────────────
        if action_name and form_data:
            # A2UI form submission → construct natural language message
            display_text = f"用户提交了表单 [{action_name}]，数据：{json.dumps(form_data, ensure_ascii=False)}"
        else:
            display_text = message_content or ""

        # ── Save user message ───────────────────────────────────────────
        if action_name:
            user_msg = await conv_service.save_message(
                db, conversation_id=conversation_id, role="user",
                message_type="a2ui_action",
                content=display_text,
                action_name=action_name,
                action_status="submitted",
            )
        else:
            user_msg = await conv_service.save_message(
                db, conversation_id=conversation_id, role="user",
                content=display_text,
            )

        # Notify frontend that user message is saved
        yield SSEEvent("user_message_saved", {
            "conversation_id": conversation_id,
            "message_id": user_msg.id,
        })

        # ── Set conversation title from first message ───────────────────
        if conversation.title is None and display_text:
            conversation.title = display_text[:50] + ("..." if len(display_text) > 50 else "")
            await db.commit()

        # ── Build LLM messages (stateless: only system + current message) ─
        full_messages: list[dict] = [{"type": "system", "role": "system", "content": system_prompt}]
        full_messages.append({"type": "user", "role": "user", "content": display_text})

        # ── Run agent loop ──────────────────────────────────────────────
        # Diagnostic: log message structure before sending to LLM
        for i, m in enumerate(full_messages):
            missing = [k for k in ("type", "role") if k not in m]
            if missing:
                logger.warning(
                    "⚠ messages[%d] MISSING fields: %s | keys present: %s",
                    i, missing, list(m.keys()),
                )
        logger.debug(
            "Sending %d messages to LLM: %s",
            len(full_messages),
            [{"i": i, "type": m.get("type"), "role": m.get("role"),
              "has_content": "content" in m, "has_tool_calls": "tool_calls" in m}
             for i, m in enumerate(full_messages)],
        )

        mcp_client = self._get_mcp_client(user)
        loop = AgentLoop(self._llm_client, mcp_client)

        collected_content = ""
        collected_tool_calls: list[dict] = []
        a2ui_error_detail: str | None = None
        pending_messages: list[dict] = []  # Buffer for delayed batch save

        try:
            async for event in loop.run(full_messages, filtered_tools):
                if event.event == "text":
                    collected_content += event.data.get("delta", "")
                elif event.event == "tool_call":
                    collected_tool_calls.append(event.data)
                elif event.event == "tool_result":
                    # Buffer tool messages for batch save
                    pending_messages.append({
                        "role": "tool",
                        "message_type": "chat",
                        "tool_call_id": event.data.get("id", ""),
                        "tool_name": event.data.get("name", ""),
                        "content": json.dumps(event.data.get("result", {}), ensure_ascii=False),
                    })
                elif event.event == "error":
                    a2ui_error_detail = event.data.get("message", "")

                if event.event == "done":
                    event.data["conversation_id"] = conversation_id

                yield event

        finally:
            await mcp_client.close()

        # ── Batch save pending messages + assistant reply ───────────────
        try:
            # Separate A2UI JSONL from text content
            a2ui_jsonl, text_content = self._split_a2ui_content(collected_content)

            for pm in pending_messages:
                await conv_service.save_message(
                    db, conversation_id=conversation_id,
                    role=pm["role"],
                    message_type=pm.get("message_type", "chat"),
                    content=pm.get("content"),
                    tool_call_id=pm.get("tool_call_id"),
                    tool_name=pm.get("tool_name"),
                    flush_only=True,
                )

            tool_calls_json = json.dumps(collected_tool_calls, ensure_ascii=False) if collected_tool_calls else None

            if action_name:
                # A2UI form submission: everything goes onto the a2ui_action
                # user message — both the text result and any A2UI JSONL result.
                user_msg.action_status = "failed" if a2ui_error_detail else "done"

                # Store result A2UI JSONL directly on the a2ui_action message
                # so the frontend can render it inside the original form bubble.
                user_msg.a2ui_jsonl = a2ui_jsonl

                # Clean action_result: if a result A2UI card exists, use a brief
                # status message instead of the LLM's chain-of-thought text.
                if a2ui_jsonl:
                    user_msg.action_result = "操作失败" if a2ui_error_detail else "操作完成"
                elif text_content:
                    summary = _extract_summary(text_content)
                    user_msg.action_result = summary if summary else "操作完成"
                else:
                    user_msg.action_result = "操作完成" if not a2ui_error_detail else "操作失败"
            else:
                # Normal chat: save assistant message with text + optional A2UI content
                await conv_service.save_message(
                    db, conversation_id=conversation_id, role="assistant",
                    content=text_content or None,
                    tool_calls_json=tool_calls_json,
                    a2ui_jsonl=a2ui_jsonl,
                    flush_only=True,
                )

            # Single commit for all pending messages
            await db.commit()

        except Exception as e:
            logger.error(f"Failed to save messages: {e}", exc_info=True)

        # ── Touch conversation timestamp ────────────────────────────────
        conversation.updated_at = datetime.now(timezone.utc)
        await db.commit()

    # ── Helper methods ──────────────────────────────────────────────────

    @staticmethod
    def _split_a2ui_content(text: str) -> tuple[str | None, str | None]:
        """Split collected LLM output into A2UI JSONL and plain text.

        Returns (a2ui_jsonl, text_content).
        """
        if not text:
            return None, None

        a2ui_lines: list[str] = []
        text_lines: list[str] = []

        for line in text.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                data = json.loads(stripped)
                if isinstance(data, dict) and any(
                    key in data for key in ("createSurface", "updateComponents", "updateDataModel", "deleteSurface")
                ):
                    a2ui_lines.append(stripped)
                    continue
            except (json.JSONDecodeError, TypeError):
                pass
            text_lines.append(stripped)

        return ("\n".join(a2ui_lines) if a2ui_lines else None,
                "\n".join(text_lines) if text_lines else None)


