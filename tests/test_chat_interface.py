import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


class DummyChatInterface:
    def __init__(self, fn):
        self.fn = fn


sys.modules["gradio"] = types.SimpleNamespace(ChatInterface=DummyChatInterface)


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


class FlakyEmbedder:
    def __init__(self) -> None:
        self.calls = 0

    async def embed(self, texts):
        self.calls += 1
        if self.calls < 2:
            raise RuntimeError("boom")
        return [[0.0]]


class FailingEmbedder:
    def __init__(self) -> None:
        self.calls = 0

    async def embed(self, texts):
        self.calls += 1
        raise RuntimeError("boom")


class FlakyIndex:
    def __init__(self) -> None:
        self.calls = 0

    async def query(self, vector, top_k=1):
        self.calls += 1
        if self.calls < 2:
            raise RuntimeError("boom")
        return [{"metadata": {"text": "response"}}]


class FailingIndex:
    def __init__(self) -> None:
        self.calls = 0

    async def query(self, vector, top_k=1):
        self.calls += 1
        raise RuntimeError("boom")


async def _run_handle_message(msg: str) -> str:
    build_interface, handle_message, _ = _import_modules()
    return await handle_message(
        msg,
        embedder=StubEmbedder(),
        index=StubIndex(),
    )


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
    embedder = FailingEmbedder()
    with pytest.raises(ChatError, match="embedding failed"):
        await handle_message("hi", embedder=embedder, index=StubIndex())
    assert embedder.calls == 3


@pytest.mark.asyncio
async def test_handle_message_index_failure() -> None:
    _, handle_message, ChatError = _import_modules()
    index = FailingIndex()
    with pytest.raises(ChatError, match="index query failed"):
        await handle_message("hi", embedder=StubEmbedder(), index=index)
    assert index.calls == 3


@pytest.mark.asyncio
async def test_handle_message_embed_retry_success() -> None:
    _, handle_message, _ = _import_modules()
    embedder = FlakyEmbedder()
    result = await handle_message("hi", embedder=embedder, index=StubIndex())
    assert result == "response"
    assert embedder.calls == 2


@pytest.mark.asyncio
async def test_handle_message_index_retry_success() -> None:
    _, handle_message, _ = _import_modules()
    index = FlakyIndex()
    result = await handle_message("hi", embedder=StubEmbedder(), index=index)
    assert result == "response"
    assert index.calls == 2
