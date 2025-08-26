"""Basic Gradio chat interface leveraging Dense X Retrieval."""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, List, Type, TypeVar

import gradio as gr  # type: ignore[import-not-found]

from .embedder import BgeEmbedder
from .exceptions import ChatError
from .pinecone_index import PineconeIndex

T = TypeVar("T")


async def _with_retry(
    func: Callable[[], Awaitable[T]],
    *,
    retries: int = 3,
    timeout: float = 10,
    base_delay: float = 0.1,
    error_cls: Type[Exception] = Exception,
) -> T:
    """Execute an async function with retry, timeout, and exponential backoff."""
    for attempt in range(retries):
        try:
            return await asyncio.wait_for(func(), timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            if attempt == retries - 1:
                raise error_cls(str(exc)) from exc
            await asyncio.sleep(base_delay * 2**attempt)


async def handle_message(
    message: str, *, embedder: BgeEmbedder, index: PineconeIndex
) -> str:
    """Respond to a user query using Dense X Retrieval."""
    if not isinstance(message, str) or not message.strip():
        raise ChatError("message must be a non-empty string")
    try:
        vectors = await _with_retry(
            lambda: embedder.embed([message]),
            base_delay=0.1,
            error_cls=ChatError,
        )
    except ChatError as exc:
        raise ChatError("embedding failed") from exc
    try:
        results = await _with_retry(
            lambda: index.query(vectors[0]),
            base_delay=0.1,
            error_cls=ChatError,
        )
    except ChatError as exc:
        raise ChatError("index query failed") from exc
    if not results:
        return "No results found."
    return results[0]["metadata"].get("text", "")


def build_interface(embedder: BgeEmbedder, index: PineconeIndex) -> gr.ChatInterface:
    """Construct a Gradio chat interface for Dense X Retrieval."""

    async def responder(message: str, history: List[List[str]]) -> str:
        return await handle_message(message, embedder=embedder, index=index)

    return gr.ChatInterface(responder)
