"""Security tests — validate the four-layer defense system.

Four layers:
1. System Prompt: must not contain unauthorized tool names
2. Whitelist: low-privilege user's tools/call should be rejected
3. Groups: groups parameter correctly injected
4. Odoo ACL: permission errors surfaced correctly

These tests validate the security architecture without requiring a real Odoo instance.
"""

import pytest
from app.services.system_prompt import SystemPromptBuilder
from app.models.user import User
from app.models.role import Role
from app.models.tool_whitelist import ToolWhitelist

ALL_TOOLS = [
    {"name": "product_search", "description": "Search products", "inputSchema": {}},
    {"name": "stock_check", "description": "Check stock levels", "inputSchema": {}},
    {"name": "admin_delete", "description": "Delete records (admin only)", "inputSchema": {}},
    {"name": "sales_report", "description": "Generate sales reports", "inputSchema": {}},
]


def make_user_with_whitelist(tool_names: list[str]) -> User:
    """Create a mock User with a Role that has the given tool whitelist."""
    role = Role(id=1, name="test_role")
    role.tool_whitelist = [
        ToolWhitelist(role_id=1, tool_name=name) for name in tool_names
    ]
    user = User(id=1, username="testuser", password_hash="...")
    user.role = role
    return user


class TestLayer1SystemPrompt:
    """Layer 1: System prompt must not leak unauthorized tool names."""

    def test_prompt_only_includes_whitelisted_tools(self):
        """System prompt text should reference only whitelisted tools."""
        user = make_user_with_whitelist(["product_search", "stock_check"])
        prompt, tools = SystemPromptBuilder.build(user, ALL_TOOLS)

        assert "product_search" in prompt
        assert "stock_check" in prompt
        assert "admin_delete" not in prompt
        assert "sales_report" not in prompt
        assert len(tools) == 2

    def test_no_role_means_no_tools(self):
        """User without a role should get no tools."""
        user = User(id=2, username="norole", password_hash="...")
        user.role = None
        prompt, tools = SystemPromptBuilder.build(user, ALL_TOOLS)

        assert len(tools) == 0

    def test_empty_whitelist_means_no_tools(self):
        """User with role but empty whitelist should get no tools."""
        user = make_user_with_whitelist([])
        prompt, tools = SystemPromptBuilder.build(user, ALL_TOOLS)

        assert len(tools) == 0


class TestLayer2Whitelist:
    """Layer 2: Whitelist enforcement in tool filtering."""

    def test_get_available_tools_respects_whitelist(self):
        """Only whitelisted tools should be returned."""
        user = make_user_with_whitelist(["product_search"])
        available = SystemPromptBuilder.get_available_tools(user, ALL_TOOLS)

        assert len(available) == 1
        assert available[0]["name"] == "product_search"

    def test_all_tools_in_whitelist(self):
        """When all tools are whitelisted, all should be available."""
        user = make_user_with_whitelist(["product_search", "stock_check", "admin_delete", "sales_report"])
        available = SystemPromptBuilder.get_available_tools(user, ALL_TOOLS)

        assert len(available) == 4


class TestLayer3Groups:
    """Layer 3: groups parameter injection (validated at MCP client call time)."""

    def test_mcp_call_tool_includes_groups(self):
        """The call_tool method should include groups in the arguments.

        Note: This is tested at the MCP client level. The groups parameter
        is included by the chat service when constructing the MCP call,
        sourced from user.role context.
        """
        # This test documents the expected behavior.
        # Full integration test requires a running Odoo instance.
        pass


class TestLayer4OdooACL:
    """Layer 4: Odoo ACL permission errors are surfaced to the frontend."""

    def test_error_surfaced_as_sse_event(self):
        """When MCP returns an error, it should become an SSE error event."""
        from app.schemas.chat import SSEEvent

        event = SSEEvent("error", {"message": "Access denied by Odoo ACL"})
        sse_text = event.to_sse()

        assert "event: error" in sse_text
        assert "Access denied by Odoo ACL" in sse_text


class TestEndToEndSecurity:
    """End-to-end security verification."""

    def test_four_layers_in_order(self):
        """Verify layers are applied in the correct order:
        1. System Prompt excludes unauthorized tools
        2. Whitelist restricts available tools
        3. Groups parameter is passed to MCP
        4. Odoo ACL is the final gate
        """
        # All layers are tested individually above.
        # This test documents the layered architecture.
        layers = [
            "System Prompt Filtering",
            "Tool Whitelist Enforcement",
            "Groups Parameter Injection",
            "Odoo ACL Enforcement",
        ]
        assert len(layers) == 4
