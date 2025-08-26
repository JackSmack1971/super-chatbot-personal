import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))  # noqa: E402

import pytest  # noqa: E402
from src.config import ConfigurationError, load_env  # noqa: E402


@pytest.mark.asyncio
async def test_load_env_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("OPENROUTER_API_KEY=ok\nPINECONE_API_KEY=pk\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("PINECONE_API_KEY", raising=False)

    result = await load_env(["OPENROUTER_API_KEY", "PINECONE_API_KEY"])
    assert result == {"OPENROUTER_API_KEY": "ok", "PINECONE_API_KEY": "pk"}


@pytest.mark.asyncio
async def test_load_env_missing_var(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("OPENROUTER_API_KEY=ok\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PINECONE_API_KEY", raising=False)

    with pytest.raises(ConfigurationError):
        await load_env(["OPENROUTER_API_KEY", "PINECONE_API_KEY"])


@pytest.mark.asyncio
async def test_load_env_invalid_input() -> None:
    with pytest.raises(ConfigurationError):
        await load_env([""])
