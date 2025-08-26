import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

sys.modules["dotenv"] = types.SimpleNamespace(load_dotenv=lambda _: None)

import pytest  # noqa: E402
from src.config import ConfigurationError, load_env  # noqa: E402


@pytest.mark.asyncio
async def test_load_env_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "ok")
    monkeypatch.setenv("PINECONE_API_KEY", "pk")
    result = await load_env(["OPENROUTER_API_KEY", "PINECONE_API_KEY"])
    assert result == {"OPENROUTER_API_KEY": "ok", "PINECONE_API_KEY": "pk"}


@pytest.mark.asyncio
async def test_load_env_missing_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PINECONE_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "ok")
    with pytest.raises(ConfigurationError):
        await load_env(["OPENROUTER_API_KEY", "PINECONE_API_KEY"])


@pytest.mark.asyncio
async def test_load_env_invalid_input() -> None:
    with pytest.raises(ConfigurationError):
        await load_env([""])
