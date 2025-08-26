"""BGE-small-en-v1.5 embedding generator for Dense X Retrieval."""

from __future__ import annotations

import asyncio
from typing import List

from sentence_transformers import SentenceTransformer  # type: ignore[import-not-found]

from .exceptions import EmbeddingError


class BgeEmbedder:
    """Asynchronous wrapper around the BGE embedding model."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    async def _load(self) -> SentenceTransformer:
        if self._model is None:
            try:
                self._model = await asyncio.to_thread(
                    SentenceTransformer, self.model_name
                )
            except Exception as exc:  # noqa: BLE001
                raise EmbeddingError("failed to load embedding model") from exc
        return self._model

    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for Dense X Retrieval."""
        if not texts or not all(isinstance(t, str) and t.strip() for t in texts):
            raise EmbeddingError("texts must be non-empty strings")
        model = await self._load()
        try:
            return await asyncio.to_thread(
                model.encode, texts, normalize_embeddings=True
            )
        except Exception as exc:  # noqa: BLE001
            raise EmbeddingError("embedding generation failed") from exc
