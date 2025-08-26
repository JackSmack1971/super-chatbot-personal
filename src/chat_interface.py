"""Basic Gradio chat interface leveraging Dense X Retrieval."""

from __future__ import annotations

from typing import List

import gradio as gr  # type: ignore[import-not-found]

from .embedder import BgeEmbedder
from .exceptions import ChatError
from .pinecone_index import PineconeIndex


async def handle_message(
    message: str, *, embedder: BgeEmbedder, index: PineconeIndex
) -> str:
    """Respond to a user query using Dense X Retrieval."""
    if not isinstance(message, str) or not message.strip():
        raise ChatError("message must be a non-empty string")
    vectors = await embedder.embed([message])
    results = await index.query(vectors[0])
    if not results:
        return "No results found."
    return results[0]["metadata"].get("text", "")


def build_interface(embedder: BgeEmbedder, index: PineconeIndex) -> gr.ChatInterface:
    """Construct a Gradio chat interface for Dense X Retrieval."""

    async def responder(message: str, history: List[List[str]]) -> str:
        return await handle_message(message, embedder=embedder, index=index)

    return gr.ChatInterface(responder)
