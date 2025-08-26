import sys
import types
from pathlib import Path
from typing import Any, Dict, List, Tuple

import importlib
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.modules.pop("aiofiles", None)
aiofiles = importlib.import_module("aiofiles")
sys.modules["aiofiles"] = aiofiles


class DummyIndex:
    def upsert(self, vectors: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        return None

    def query(
        self, vector: List[float], top_k: int, include_metadata: bool
    ) -> Dict[str, Any]:
        return {"matches": []}


class DummyPinecone:
    def __init__(self, api_key: str) -> None:
        self.storage: Dict[str, DummyIndex] = {}

    def list_indexes(self) -> List[Any]:
        return []

    def create_index(self, name: str, dimension: int, metric: str, spec: Any) -> None:
        self.storage[name] = DummyIndex()

    def Index(self, name: str) -> DummyIndex:  # noqa: N802
        return self.storage.setdefault(name, DummyIndex())


class DummySpec:
    def __init__(self, **kwargs) -> None:
        pass


sys.modules["pinecone"] = types.SimpleNamespace(
    Pinecone=DummyPinecone, ServerlessSpec=DummySpec
)

from src.monitoring import UsageMonitor  # noqa: E402
from src.pinecone_index import PineconeIndex  # noqa: E402


@pytest.mark.asyncio
async def test_pinecone_monitor(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PINECONE_API_KEY", "k")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "i")
    monkeypatch.setenv("PINECONE_UPSERT_COST", "0.1")
    monitor = UsageMonitor()
    index = PineconeIndex(monitor=monitor)
    await index.upsert([("1", [0.0] * 384, {"t": "x"})])
    assert monitor.totals["pinecone"] == 0.1
