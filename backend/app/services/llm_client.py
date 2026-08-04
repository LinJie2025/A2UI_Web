"""LLM client: wraps the OpenAI-compatible SDK for chat streaming."""

import logging
from typing import AsyncIterator
from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Async client for LLM chat completions with streaming support."""

    def __init__(self):
        """Initialize the OpenAI-compatible client."""
        self._client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )
        self._model = settings.LLM_MODEL

    async def chat_stream(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> AsyncIterator[dict]:
        """Stream chat completion chunks from the LLM.

        Args:
            messages: List of message dicts (role, content, tool_calls, etc.).
            tools: Optional list of tool definitions to make available.

        Yields:
            Each chunk dict from the streaming response.
        """
        kwargs: dict = {
            "model": self._model,
            "messages": messages,
            "max_tokens": settings.LLM_MAX_TOKENS,
            "stream": True,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        logger.debug(f"LLM stream: model={self._model}, messages={len(messages)}, tools={len(tools or [])}")

        stream = await self._client.chat.completions.create(**kwargs)

        async for chunk in stream:
            yield chunk.model_dump() if hasattr(chunk, "model_dump") else dict(chunk)
