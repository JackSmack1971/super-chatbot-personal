import pytest
import sys
import types
from typing import Any


class _DummyIndex:
    def __init__(self) -> None:
        self.vectors: dict[str, dict[str, Any]] = {}

    def upsert(self, vectors):
        for _id, vec, meta in vectors:
            self.vectors[_id] = {"values": vec, "metadata": meta}

    def query(self, vector, top_k, include_metadata):
        matches = [
            {"id": _id, "score": 1.0, "metadata": data["metadata"]}
            for _id, data in list(self.vectors.items())[:top_k]
        ]
        return {"matches": matches}


class _DummyPinecone:
    def __init__(self, api_key: str) -> None:
        self.storage = {}

    def list_indexes(self):
        return []

    def create_index(self, name, dimension, metric, spec):
        self.storage[name] = _DummyIndex()

    def Index(self, name):  # noqa: N802
        return self.storage.setdefault(name, _DummyIndex())


class _DummySpec:
    def __init__(self, **kwargs) -> None:
        pass


sys.modules["pinecone"] = types.SimpleNamespace(
    Pinecone=_DummyPinecone, ServerlessSpec=_DummySpec
)

from src.chat_interface import _with_retry
from src.exceptions import ChatError


@pytest.mark.asyncio
async def test_with_retry_exponential_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = 0

    async def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("boom")
        return "ok"

    delays: list[float] = []

    async def fake_sleep(delay: float) -> None:
        delays.append(delay)

    import src.chat_interface as ci

    monkeypatch.setattr(ci.asyncio, "sleep", fake_sleep)
    result = await _with_retry(
        flaky,
        retries=3,
        timeout=0.1,
        base_delay=0.5,
        error_cls=ChatError,
    )
    assert result == "ok"
    assert delays == [0.5, 1.0]


@pytest.mark.asyncio
async def test_with_retry_raises_custom_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def always_fail() -> None:
        raise RuntimeError("fail")

    async def fake_sleep(_: float) -> None:
        pass

    import src.chat_interface as ci

    monkeypatch.setattr(ci.asyncio, "sleep", fake_sleep)
    with pytest.raises(ChatError) as excinfo:
        await _with_retry(
            always_fail,
            retries=2,
            timeout=0.1,
            base_delay=0.5,
            error_cls=ChatError,
        )
    assert isinstance(excinfo.value.__cause__, RuntimeError)
