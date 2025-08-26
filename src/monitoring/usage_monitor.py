"""Cost monitoring for external services."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

import aiofiles  # type: ignore[import-not-found,import-untyped]
import httpx  # type: ignore[import-not-found]

from ..exceptions import MonitoringError


@dataclass
class UsageMonitor:
    """Track API usage costs and alert on budget exceedance."""

    alert_limit: float = field(
        default_factory=lambda: float(os.getenv("COST_ALERT_LIMIT", "150"))
    )
    log_path: str = field(
        default_factory=lambda: os.getenv("MONITOR_LOG_PATH", "usage.csv")
    )
    dashboard_url: Optional[str] = field(
        default_factory=lambda: os.getenv("MONITOR_DASHBOARD_URL")
    )
    totals: Dict[str, float] = field(default_factory=dict)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)

    async def record(self, service: str, cost: float) -> None:
        """Record cost data for a service.

        Args:
            service: Name of the service (e.g., "openrouter").
            cost: Cost incurred in USD.
        """
        if not isinstance(service, str) or not service.strip() or cost < 0:
            raise MonitoringError("invalid monitoring data")
        async with self._lock:
            self.totals[service] = self.totals.get(service, 0.0) + cost
            await self._log(service, cost)
            if self.totals[service] >= self.alert_limit:
                msg = f"{service} cost {self.totals[service]:.2f} exceeds ${self.alert_limit:.2f}"
                raise MonitoringError(msg)

    async def _log(self, service: str, cost: float) -> None:
        """Persist cost data to CSV and optional dashboard."""
        row = f"{datetime.utcnow().isoformat()},{service},{cost:.4f},{self.totals[service]:.4f}\n"
        try:
            async with aiofiles.open(self.log_path, "a") as f:
                await f.write(row)
            if self.dashboard_url:
                async with httpx.AsyncClient(timeout=5) as client:
                    await client.post(
                        self.dashboard_url,
                        json={
                            "service": service,
                            "cost": cost,
                            "total": self.totals[service],
                        },
                    )
        except Exception as exc:  # noqa: BLE001
            raise MonitoringError("failed to log usage") from exc
