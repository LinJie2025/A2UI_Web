"""A2UI Form Templates — defines which fields to show for each MCP write tool.

Template + ai_tool_get_fields = dynamic, accurate form generation.
Template constrains field selection, get_fields provides real labels/types.

To add a new tool form: add one entry to TOOL_FORMS below.
"""

from typing import TypedDict


class FormField(TypedDict):
    name: str
    """Field technical name (must match Odoo model field name)."""


class FormTemplate(TypedDict, total=False):
    model: str
    """Odoo model technical name (for ai_tool_get_fields query)."""
    title: str
    """Form title displayed at top."""
    fields: list[str]
    """Field names to include in the form (order matters). Max 6."""
    button_text: str
    """Button label (default: '提交')."""
    button_action: str
    """Button action name (default: same as tool name)."""
    hidden_fields: dict[str, str]
    """Fields not shown in the form UI, auto-filled by the backend.
    Format: {field_name: value_expression}
    Supported expressions:
      - $user.username   → current user's username
      - $user.id         → current user's ID
    """


# ── Tool Form Registry ──────────────────────────────────────────────────────
# Key = tool name (must match Odoo MCP tools/list response)
# Value = form template definition

TOOL_FORMS: dict[str, FormTemplate] = {
    "create_contact": {
        "model": "res.partner",
        "title": "创建联系人",
        "fields": ["name", "email", "phone", "x_creator"],
        "button_text": "创建",
        "button_action": "create_contact",
        "hidden_fields": {"x_creator": "$user.username"},
    },
    "stock_transfer_internal": {
        "model": "stock.move",
        "title": "创建内部调拨单",
        "fields": ["product_ref", "quantity", "dest_location", "source_location", "x_creator"],
        "button_text": "创建",
        "button_action": "stock_transfer_internal",
        "hidden_fields": {"x_creator": "$user.username"},
    },
    # Examples — uncomment and fill in as you add Odoo tools:
    # "create_product": {
    #     "model": "product.product",
    #     "title": "创建产品",
    #     "fields": ["name", "default_code", "list_price"],
    #     "button_text": "创建产品",
    #     "button_action": "create_product",
    # },
    # "create_invoice": {
    #     "model": "account.move",
    #     "title": "创建发票",
    #     "fields": ["partner_id", "invoice_date", "amount_total"],
    #     "button_text": "开票",
    #     "button_action": "create_invoice",
    # },
}


def get_template(tool_name: str) -> FormTemplate | None:
    """Return form template for a tool, or None if not configured."""
    return TOOL_FORMS.get(tool_name)


def get_all_template_tool_names() -> list[str]:
    """Return all tool names that have form templates registered."""
    return list(TOOL_FORMS.keys())


def get_visible_fields(template: FormTemplate) -> list[str]:
    """Return fields that should be displayed in the A2UI form,
    excluding hidden_fields keys."""
    fields = template.get("fields", [])
    hidden = set(template.get("hidden_fields", {}).keys())
    return [f for f in fields if f not in hidden]


def resolve_hidden_fields(
    template: FormTemplate,
    form_data: dict[str, str],
    user_username: str,
    user_id: int,
) -> dict[str, str]:
    """Inject hidden field values into form_data using value expressions.

    Returns updated form_data with hidden field values resolved and set.
    """
    import logging
    logger = logging.getLogger(__name__)

    result = dict(form_data)
    hidden = template.get("hidden_fields", {})

    for field_name, expression in hidden.items():
        if expression == "$user.username":
            result[field_name] = user_username
        elif expression == "$user.id":
            result[field_name] = str(user_id)
        else:
            logger.warning(
                "Unknown hidden_field expression %r for field %r — skipped",
                expression,
                field_name,
            )
            continue
        logger.info(
            "Auto-filled hidden field %s=%s (from %s)",
            field_name,
            result[field_name],
            expression,
        )

    return result
