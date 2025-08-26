import sys
import types
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).resolve().parents[1]))


class DummyModel:
    def encode(
        self, texts: List[str], normalize_embeddings: bool = True
    ) -> List[List[float]]:
        return [[0.0] * 384 for _ in texts]


sys.modules["sentence_transformers"] = types.SimpleNamespace(
    SentenceTransformer=lambda name: DummyModel()
)

from src.embedder import BgeEmbedder  # noqa: E402
from src.exceptions import EmbeddingError  # noqa: E402

import pytest  # noqa: E402


@pytest.mark.asyncio
async def test_embedder_success() -> None:
    embedder = BgeEmbedder()
    result = await embedder.embed(["hello"])
    assert len(result[0]) == 384


@pytest.mark.asyncio
async def test_embedder_invalid_input() -> None:
    embedder = BgeEmbedder()
    with pytest.raises(EmbeddingError):
        await embedder.embed([""])
