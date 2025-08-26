import sys
from pathlib import Path
import types
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[1]))


class DummyChatInterface:
    def __init__(self, fn):
        self.fn = fn


sys.modules["gradio"] = types.SimpleNamespace(ChatInterface=DummyChatInterface)


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


def _import_modules():
    from src.chat_interface import build_interface, handle_message
    from src.exceptions import ChatError

    return build_interface, handle_message, ChatError


class StubEmbedder:
    async def embed(self, texts):
        return [[0.0]]


class StubIndex:
    async def query(self, vector, top_k=1):
        return [{"metadata": {"text": "response"}}]


class FailingEmbedder:
    async def embed(self, texts):
        raise RuntimeError("boom")


class FailingIndex:
    async def query(self, vector, top_k=1):
        raise RuntimeError("boom")


async def _run_handle_message(msg: str) -> str:
    build_interface, handle_message, _ = _import_modules()
    return await handle_message(msg, embedder=StubEmbedder(), index=StubIndex())


def test_build_interface_type() -> None:
    build_interface, _, _ = _import_modules()
    iface = build_interface(StubEmbedder(), StubIndex())
    assert isinstance(iface, DummyChatInterface)


import pytest  # noqa: E402


@pytest.mark.asyncio
async def test_handle_message_success() -> None:
    result = await _run_handle_message("hi")
    assert result == "response"


@pytest.mark.asyncio
async def test_handle_message_invalid() -> None:
    _, handle_message, ChatError = _import_modules()
    with pytest.raises(ChatError):
        await handle_message("", embedder=StubEmbedder(), index=StubIndex())


@pytest.mark.asyncio
async def test_handle_message_embed_failure() -> None:
    _, handle_message, ChatError = _import_modules()
    with pytest.raises(ChatError, match="embedding failed"):
        await handle_message("hi", embedder=FailingEmbedder(), index=StubIndex())


@pytest.mark.asyncio
async def test_handle_message_index_failure() -> None:
    _, handle_message, ChatError = _import_modules()
    with pytest.raises(ChatError, match="index query failed"):
        await handle_message("hi", embedder=StubEmbedder(), index=FailingIndex())
