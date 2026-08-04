"""MCP JSONRPC 2.0 client for communicating with Odoo /mcp endpoint."""

import logging
import httpx
from app.schemas.chat import ToolDef

logger = logging.getLogger(__name__)


class MCPClient:
    """Async HTTP client for Odoo MCP JSONRPC 2.0 protocol.

    Communicates via POST to {base_url}/mcp with Bearer token authentication.
    """

    def __init__(self, base_url: str, token: str):
        """Initialize MCP client.

        Args:
            base_url: Base URL of the Odoo instance (e.g. http://localhost:8069).
            token: Bearer token for MCP authentication.
        """
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(30.0))

    async def _request(self, method: str, params: dict, request_id: int = 1) -> dict:
        """Send a JSONRPC 2.0 request to the MCP endpoint.

        Args:
            method: The JSONRPC method name (e.g. 'tools/list', 'tools/call').
            params: The params dict for the method.
            request_id: JSONRPC request ID.

        Returns:
            The 'result' field from the JSONRPC response.

        Raises:
            httpx.HTTPError: On HTTP or transport errors.
            ValueError: If the JSONRPC response contains an error.
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

        url = f"{self._base_url}/mcp"
        logger.debug(f"MCP request: {method} → {url}")

        resp = await self._client.post(url, json=payload, headers=headers)
        resp.raise_for_status()

        data = resp.json()
        if "error" in data:
            raise ValueError(f"MCP error: {data['error']}")
        return data.get("result", {})

    async def list_tools(self) -> list[dict]:
        """Fetch the list of available tools from the MCP server.

        Returns:
            List of tool definition dicts with 'name', 'description', 'inputSchema'.
        """
        result = await self._request("tools/list", {}, request_id=1)
        tools = result if isinstance(result, list) else result.get("tools", [])
        return tools

    async def call_tool(self, name: str, arguments: dict) -> dict:
        """Call a specific tool on the MCP server.

        Args:
            name: The tool name to invoke.
            arguments: The arguments to pass to the tool.

        Returns:
            The tool execution result dict.
        """
        params = {"name": name, "arguments": arguments}
        result = await self._request("tools/call", params, request_id=2)
        return result

    async def close(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()
