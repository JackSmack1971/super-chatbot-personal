import sys
import types
from pathlib import Path

import pytest
import importlib

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.modules.pop("aiofiles", None)
aiofiles = importlib.import_module("aiofiles")
sys.modules["aiofiles"] = aiofiles


class DummyResponse:
    output = [types.SimpleNamespace(content=[types.SimpleNamespace(text="hi")])]
    usage = {"total_tokens": 100}


class DummyClient:
    def __init__(self, *args, **kwargs) -> None:
        self.responses = types.SimpleNamespace(create=self._create)

    async def _create(self, model: str, input: str) -> DummyResponse:
        return DummyResponse()


class FlakyClient(DummyClient):
    def __init__(self) -> None:
        super().__init__()
        self.calls = 0

    async def _create(self, model: str, input: str) -> DummyResponse:
        self.calls += 1
        if self.calls < 3:
            raise RuntimeError("fail")
        return DummyResponse()


def dummy_async_openai(*args, **kwargs):
    return DummyClient()


sys.modules["openai"] = types.SimpleNamespace(AsyncOpenAI=dummy_async_openai)

from src.monitoring import UsageMonitor  # noqa: E402
from src.openrouter_client import OpenRouterClient  # noqa: E402
from src.exceptions import OpenRouterError  # noqa: E402


@pytest.mark.asyncio
async def test_openrouter_client_records(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "key")
    monkeypatch.setenv("OPENROUTER_PRICE_PER_1K", "0.01")
    monitor = UsageMonitor()
    client = OpenRouterClient(monitor=monitor)
    result = await client.complete("hello")
    assert result == "hi"
    assert monitor.totals["openrouter"] > 0


@pytest.mark.asyncio
async def test_openrouter_client_invalid_prompt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "key")
    client = OpenRouterClient()
    with pytest.raises(OpenRouterError):
        await client.complete("")


@pytest.mark.asyncio
async def test_openrouter_client_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "key")
    flaky = FlakyClient()
    import src.openrouter_client as orc

    monkeypatch.setattr(orc, "AsyncOpenAI", lambda **kwargs: flaky)
    from src.utils import retry as retry_module

    async def fake_sleep(_: float) -> None:
        pass

    monkeypatch.setattr(retry_module.asyncio, "sleep", fake_sleep)
    client = OpenRouterClient()
    result = await client.complete("hello", retries=3)
    assert result == "hi"
    assert flaky.calls == 3
