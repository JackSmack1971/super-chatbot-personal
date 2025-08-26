import sys
import types
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.append(str(Path(__file__).resolve().parents[1]))


class DummyIndex:
    def __init__(self) -> None:
        self.vectors: Dict[str, Dict[str, Any]] = {}

    def upsert(self, vectors: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        for _id, vec, meta in vectors:
            self.vectors[_id] = {"values": vec, "metadata": meta}

    def query(
        self, vector: List[float], top_k: int, include_metadata: bool
    ) -> Dict[str, Any]:
        matches = [
            {"id": _id, "score": 1.0, "metadata": data["metadata"]}
            for _id, data in list(self.vectors.items())[:top_k]
        ]
        return {"matches": matches}


class FlakyIndex(DummyIndex):
    def __init__(self) -> None:
        super().__init__()
        self.upsert_calls = 0
        self.query_calls = 0

    def upsert(self, vectors: List[Tuple[str, List[float], Dict[str, Any]]]) -> None:
        self.upsert_calls += 1
        if self.upsert_calls < 3:
            raise RuntimeError("fail")
        super().upsert(vectors)

    def query(
        self, vector: List[float], top_k: int, include_metadata: bool
    ) -> Dict[str, Any]:
        self.query_calls += 1
        if self.query_calls < 2:
            raise RuntimeError("fail")
        return super().query(vector, top_k, include_metadata)


class DummyPinecone:
    def __init__(self, api_key: str) -> None:
        self.storage: Dict[str, DummyIndex] = {}

    def list_indexes(self) -> List[Any]:
        return []

    def create_index(self, name: str, dimension: int, metric: str, spec: Any) -> None:
        self.storage[name] = DummyIndex()

    def Index(self, name: str) -> DummyIndex:  # noqa: N802
        return self.storage.setdefault(name, DummyIndex())


class FlakyPinecone(DummyPinecone):
    def create_index(self, name: str, dimension: int, metric: str, spec: Any) -> None:
        self.storage[name] = FlakyIndex()

    def Index(self, name: str) -> FlakyIndex:  # noqa: N802
        return self.storage.setdefault(name, FlakyIndex())


class DummySpec:
    def __init__(self, **kwargs) -> None:
        pass


sys.modules["pinecone"] = types.SimpleNamespace(
    Pinecone=DummyPinecone, ServerlessSpec=DummySpec
)

from src.pinecone_index import PineconeIndex  # noqa: E402
from src.exceptions import IndexingError  # noqa: E402

import pytest  # noqa: E402


@pytest.mark.asyncio
async def test_upsert_and_query(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PINECONE_API_KEY", "k")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "i")
    index = PineconeIndex()
    await index.upsert([("1", [0.0] * 384, {"text": "hello"})])
    results = await index.query([0.0] * 384)
    assert results[0]["metadata"]["text"] == "hello"


@pytest.mark.asyncio
async def test_upsert_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PINECONE_API_KEY", "k")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "i")
    index = PineconeIndex()
    with pytest.raises(IndexingError):
        await index.upsert([])


@pytest.mark.asyncio
async def test_query_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PINECONE_API_KEY", "k")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "i")
    index = PineconeIndex()
    with pytest.raises(IndexingError):
        await index.query([])


@pytest.mark.asyncio
async def test_pinecone_index_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PINECONE_API_KEY", "k")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "i")
    import src.pinecone_index as pi

    flaky_pc = FlakyPinecone(api_key="k")
    monkeypatch.setattr(pi, "Pinecone", lambda api_key: flaky_pc)
    from src.utils import retry as retry_module

    async def fake_sleep(_: float) -> None:
        pass

    monkeypatch.setattr(retry_module.asyncio, "sleep", fake_sleep)
    index = PineconeIndex()
    await index.upsert([("1", [0.0] * 384, {"text": "a"})], retries=3)
    results = await index.query([0.0] * 384, retries=2)
    assert flaky_pc.storage["i"].upsert_calls == 3
    assert flaky_pc.storage["i"].query_calls == 2
    assert results[0]["metadata"]["text"] == "a"
