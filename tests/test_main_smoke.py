import importlib
import sys
import types
from pathlib import Path

import pytest
from src.exceptions import InitializationError

sys.path.append(str(Path(__file__).resolve().parents[1]))


@pytest.mark.asyncio
async def test_startup_smoke(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PINECONE_API_KEY", "key")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "index")
    monkeypatch.setitem(
        sys.modules,
        "dotenv",
        types.SimpleNamespace(load_dotenv=lambda _: None),
    )
    monkeypatch.setitem(
        sys.modules,
        "pinecone",
        types.SimpleNamespace(Pinecone=object, ServerlessSpec=object),
    )
    main = importlib.reload(importlib.import_module("src.main"))

    dummy_interface = object()
    monkeypatch.setattr(main, "BgeEmbedder", lambda: object())
    monkeypatch.setattr(main, "PineconeIndex", lambda: object())
    monkeypatch.setattr(main, "build_interface", lambda e, i: dummy_interface)

    interface = await main.startup()
    assert interface is dummy_interface


@pytest.mark.asyncio
async def test_startup_missing_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(
        sys.modules,
        "dotenv",
        types.SimpleNamespace(load_dotenv=lambda _: None),
    )
    monkeypatch.setitem(
        sys.modules,
        "pinecone",
        types.SimpleNamespace(Pinecone=object, ServerlessSpec=object),
    )
    main = importlib.reload(importlib.import_module("src.main"))

    monkeypatch.delenv("PINECONE_API_KEY", raising=False)
    monkeypatch.delenv("PINECONE_INDEX_NAME", raising=False)
    with pytest.raises(InitializationError):
        await main.startup()
