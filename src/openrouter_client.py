"""OpenRouter API client with cost monitoring."""

from __future__ import annotations

import asyncio
import os
from typing import Optional

from openai import AsyncOpenAI  # type: ignore[import-not-found]

from .exceptions import OpenRouterError
from .monitoring import UsageMonitor


class OpenRouterClient:
    """Async wrapper for OpenRouter API."""

    def __init__(
        self, *, model: Optional[str] = None, monitor: Optional[UsageMonitor] = None
    ) -> None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise OpenRouterError("missing OpenRouter API key")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model or os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
        self.monitor = monitor

    async def complete(self, prompt: str, *, retries: int = 3) -> str:
        """Generate a completion for a prompt."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise OpenRouterError("prompt must be non-empty")
        for attempt in range(retries):
            try:
                response = await asyncio.wait_for(
                    self.client.responses.create(model=self.model, input=prompt),
                    timeout=30,
                )
                text = response.output[0].content[0].text
                usage = getattr(response, "usage", {}) or {}
                tokens = usage.get("total_tokens", 0)
                price = float(os.getenv("OPENROUTER_PRICE_PER_1K", "0"))
                cost = tokens / 1000 * price
                if self.monitor:
                    await self.monitor.record("openrouter", cost)
                return text
            except Exception as exc:  # noqa: BLE001
                if attempt == retries - 1:
                    raise OpenRouterError("OpenRouter request failed") from exc
                await asyncio.sleep(2**attempt)
        raise OpenRouterError("OpenRouter request failed")
