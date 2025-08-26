"""Pinecone indexing utilities for Dense X Retrieval."""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List, Tuple

from pinecone import Pinecone, ServerlessSpec  # type: ignore[import-not-found]

from .exceptions import IndexingError
from .monitoring import UsageMonitor


class PineconeIndex:
    """Async wrapper for a Pinecone index."""

    def __init__(
        self, *, dimension: int = 384, monitor: UsageMonitor | None = None
    ) -> None:
        api_key = os.getenv("PINECONE_API_KEY")
        name = os.getenv("PINECONE_INDEX_NAME")
        if not api_key or not name:
            raise IndexingError("Missing Pinecone configuration")
        try:
            pc = Pinecone(api_key=api_key)
            if name not in [i.name for i in pc.list_indexes()]:
                spec = ServerlessSpec(cloud="aws", region="us-west-2")
                pc.create_index(name, dimension=dimension, metric="cosine", spec=spec)
            self.index = pc.Index(name)
            self.monitor = monitor
            self.upsert_cost = float(os.getenv("PINECONE_UPSERT_COST", "0"))
            self.query_cost = float(os.getenv("PINECONE_QUERY_COST", "0"))
        except Exception as exc:  # noqa: BLE001
            raise IndexingError("failed to initialize Pinecone") from exc

    async def upsert(
        self,
        items: List[Tuple[str, List[float], Dict[str, Any]]],
        *,
        retries: int = 3,
    ) -> None:
        """Upsert vectors into Pinecone with retry logic."""
        if not items:
            raise IndexingError("no items provided")
        for attempt in range(retries):
            try:
                await asyncio.wait_for(
                    asyncio.to_thread(self.index.upsert, vectors=items), timeout=10
                )
                if self.monitor:
                    cost = self.upsert_cost * len(items)
                    await self.monitor.record("pinecone", cost)
                return
            except Exception as exc:  # noqa: BLE001
                if attempt == retries - 1:
                    raise IndexingError("upsert failed") from exc
                await asyncio.sleep(2**attempt)

    async def query(
        self,
        vector: List[float],
        *,
        top_k: int = 1,
        retries: int = 3,
    ) -> List[Dict[str, Any]]:
        """Query Pinecone index for Dense X Retrieval."""
        if not vector:
            raise IndexingError("vector required")
        for attempt in range(retries):
            try:
                result = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.index.query,
                        vector=vector,
                        top_k=top_k,
                        include_metadata=True,
                    ),
                    timeout=10,
                )
                if self.monitor:
                    await self.monitor.record("pinecone", self.query_cost)
                return result.get("matches", [])
            except Exception as exc:  # noqa: BLE001
                if attempt == retries - 1:
                    raise IndexingError("query failed") from exc
                await asyncio.sleep(2**attempt)
        raise IndexingError("query failed")
