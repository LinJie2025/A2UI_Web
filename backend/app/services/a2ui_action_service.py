"""A2UI Action CRUD service."""

import json
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.a2ui_action import A2UIAction

logger = logging.getLogger(__name__)

PROCESSING_TIMEOUT_MINUTES = 5


class A2UIActionService:
    """Manage A2UI form submission actions."""

    @staticmethod
    async def create_action(
        db: AsyncSession,
        conversation_id: int,
        action_name: str,
        form_data: dict | None = None,
    ) -> A2UIAction:
        form_json = json.dumps(form_data, ensure_ascii=False) if form_data else None
        action = A2UIAction(
            conversation_id=conversation_id,
            action_name=action_name,
            form_data=form_json,
            status="submitted",
        )
        db.add(action)
        await db.commit()
        await db.refresh(action)
        logger.info(f"Created A2UI action {action.id}: {action_name}")
        return action

    @staticmethod
    async def update_status(
        db: AsyncSession,
        action_id: int,
        status: str,
        result_summary: str | None = None,
        error_detail: str | None = None,
        tool_call_id: str | None = None,
    ) -> None:
        values: dict = {
            "status": status,
            "updated_at": datetime.now(timezone.utc),
        }
        if result_summary is not None:
            values["result_summary"] = result_summary
        if error_detail is not None:
            values["error_detail"] = error_detail
        if tool_call_id is not None:
            values["tool_call_id"] = tool_call_id
        await db.execute(
            update(A2UIAction).where(A2UIAction.id == action_id).values(**values)
        )
        await db.commit()
        logger.info(f"A2UI action {action_id} -> {status}")

    @staticmethod
    async def get_actions_by_conversation(db: AsyncSession, conversation_id: int) -> list[dict]:
        result = await db.execute(
            select(A2UIAction)
            .where(A2UIAction.conversation_id == conversation_id)
            .order_by(A2UIAction.created_at.desc())
        )
        actions = result.scalars().all()
        return [_action_to_dict(a) for a in actions]

    @staticmethod
    async def cleanup_interrupted(db: AsyncSession, conversation_id: int) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=PROCESSING_TIMEOUT_MINUTES)
        result = await db.execute(
            update(A2UIAction)
            .where(
                A2UIAction.conversation_id == conversation_id,
                A2UIAction.status == "processing",
                A2UIAction.updated_at < cutoff,
            )
            .values(status="interrupted", updated_at=datetime.now(timezone.utc))
        )
        await db.commit()
        count = result.rowcount
        if count:
            logger.info(f"Cleaned up {count} interrupted A2UI actions in conversation {conversation_id}")
        return count


def _action_to_dict(action: A2UIAction) -> dict:
    form_data = None
    if action.form_data:
        try:
            form_data = json.loads(action.form_data)
        except json.JSONDecodeError:
            form_data = {"_raw": action.form_data}
    return {
        "id": action.id,
        "conversation_id": action.conversation_id,
        "action_name": action.action_name,
        "form_data": form_data,
        "status": action.status,
        "result_summary": action.result_summary,
        "error_detail": action.error_detail,
        "tool_call_id": action.tool_call_id,
        "created_at": action.created_at.isoformat() if action.created_at else "",
        "updated_at": action.updated_at.isoformat() if action.updated_at else "",
    }
