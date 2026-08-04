"""Tests for MCP client (JSONRPC 2.0)."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.mcp_client import MCPClient


@pytest.mark.asyncio
async def test_list_tools():
    """Test that list_tools sends correct JSONRPC request and parses response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "result": [
            {"name": "product_search", "description": "Search products", "inputSchema": {}},
            {"name": "stock_check", "description": "Check stock", "inputSchema": {}},
        ],
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        client = MCPClient(base_url="http://test:8069", token="test-token")
        tools = await client.list_tools()
        await client.close()

        assert len(tools) == 2
        assert tools[0]["name"] == "product_search"
        assert tools[1]["name"] == "stock_check"

        # Verify JSONRPC format
        call_args = mock_post.call_args
        payload = call_args.kwargs["json"]
        assert payload["jsonrpc"] == "2.0"
        assert payload["method"] == "tools/list"
        assert payload["id"] == 1


@pytest.mark.asyncio
async def test_call_tool():
    """Test that call_tool sends correct JSONRPC request."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "result": {"products": [{"id": 1, "name": "Widget"}]},
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        client = MCPClient(base_url="http://test:8069", token="test-token")
        result = await client.call_tool("product_search", {"query": "widget"})
        await client.close()

        assert result["products"][0]["name"] == "Widget"

        call_args = mock_post.call_args
        payload = call_args.kwargs["json"]
        assert payload["method"] == "tools/call"
        assert payload["params"]["name"] == "product_search"
        assert payload["params"]["arguments"] == {"query": "widget"}
