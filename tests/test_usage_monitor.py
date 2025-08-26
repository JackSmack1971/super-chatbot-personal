import os
import sys
from pathlib import Path

import importlib
import pytest

sys.modules.pop("aiofiles", None)
aiofiles = importlib.import_module("aiofiles")
sys.modules["aiofiles"] = aiofiles

from src.monitoring import UsageMonitor  # noqa: E402
from src.exceptions import MonitoringError  # noqa: E402


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
