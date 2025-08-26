import asyncio
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.exceptions import RetryError
from src.utils import retry


@pytest.mark.asyncio
async def test_async_retry_success(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = 0

    async def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("fail")
        return "ok"

    delays: list[float] = []

    async def fake_sleep(delay: float) -> None:
        delays.append(delay)

    monkeypatch.setattr(retry.asyncio, "sleep", fake_sleep)
    result = await retry.async_retry(flaky, max_attempts=3, timeout=0.1)
    assert result == "ok"
    assert delays == [1.0, 2.0]


@pytest.mark.asyncio
async def test_async_retry_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    async def always_fail() -> None:
        raise RuntimeError("fail")

    async def fake_sleep(_: float) -> None:
        pass

    monkeypatch.setattr(retry.asyncio, "sleep", fake_sleep)
    with pytest.raises(RetryError):
        await retry.async_retry(always_fail, max_attempts=2, timeout=0.1)


@pytest.mark.asyncio
async def test_async_retry_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    async def never() -> None:
        await asyncio.Future()

    async def fake_sleep(_: float) -> None:
        pass

    monkeypatch.setattr(retry.asyncio, "sleep", fake_sleep)
    with pytest.raises(RetryError):
        await retry.async_retry(never, max_attempts=2, timeout=0.01)
