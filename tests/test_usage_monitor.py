import importlib
import os
import sys
from pathlib import Path
from typing import Any

import httpx
import pytest

sys.modules.pop("aiofiles", None)
aiofiles = importlib.import_module("aiofiles")
sys.modules["aiofiles"] = aiofiles

from src.exceptions import MonitoringError  # noqa: E402
from src.monitoring import UsageMonitor  # noqa: E402


@pytest.mark.asyncio
async def test_monitor_logs_and_alerts(tmp_path: Path) -> None:
    log = tmp_path / "log.csv"
    os.environ["COST_ALERT_LIMIT"] = "1"
    os.environ["MONITOR_LOG_PATH"] = str(log)
    monitor = UsageMonitor()
    await monitor.record("pinecone", 0.6)
    assert log.exists()
    await monitor.record("pinecone", 0.3)
    with pytest.raises(MonitoringError):
        await monitor.record("pinecone", 0.2)
    with open(log) as f:
        assert len(f.readlines()) == 3


@pytest.mark.asyncio
async def test_dashboard_retry_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls = 0

    async def fail_post(self: httpx.AsyncClient, url: str, json: Any) -> None:
        nonlocal calls
        calls += 1
        raise httpx.HTTPError("boom")

    async def no_sleep(_: float) -> None:
        pass

    monkeypatch.setattr(httpx.AsyncClient, "post", fail_post)
    monkeypatch.setattr("asyncio.sleep", no_sleep)
    monkeypatch.setenv("MONITOR_LOG_PATH", str(tmp_path / "log.csv"))
    monkeypatch.setenv("MONITOR_DASHBOARD_URL", "http://dash")
    monkeypatch.setenv("MONITOR_DASHBOARD_RETRIES", "2")
    monkeypatch.setenv("MONITOR_DASHBOARD_TIMEOUT", "0.01")
    monitor = UsageMonitor()
    with pytest.raises(MonitoringError):
        await monitor.record("svc", 0.1)
    assert calls == 2


@pytest.mark.asyncio
async def test_dashboard_retry_success(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls = 0

    async def flaky_post(
        self: httpx.AsyncClient, url: str, json: Any
    ) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls < 2:
            raise httpx.HTTPError("boom")
        return httpx.Response(200)

    async def no_sleep(_: float) -> None:
        pass

    monkeypatch.setattr(httpx.AsyncClient, "post", flaky_post)
    monkeypatch.setattr("asyncio.sleep", no_sleep)
    monkeypatch.setenv("MONITOR_LOG_PATH", str(tmp_path / "log.csv"))
    monkeypatch.setenv("MONITOR_DASHBOARD_URL", "http://dash")
    monkeypatch.setenv("MONITOR_DASHBOARD_RETRIES", "3")
    monkeypatch.setenv("MONITOR_DASHBOARD_TIMEOUT", "0.01")
    monitor = UsageMonitor()
    await monitor.record("svc", 0.1)
    assert calls == 2
