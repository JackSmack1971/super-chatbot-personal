"""Application startup for the Gradio chat interface."""

from __future__ import annotations

import asyncio
from typing import Sequence

import gradio as gr  # type: ignore[import-not-found]

from .chat_interface import build_interface
from .config import ConfigurationError, load_env
from .embedder import BgeEmbedder
from .exceptions import InitializationError
from .pinecone_index import PineconeIndex

REQUIRED_ENV_VARS: Sequence[str] = ("PINECONE_API_KEY", "PINECONE_INDEX_NAME")


async def startup() -> gr.ChatInterface:
    """Initialize components and build the Gradio interface.

    Returns:
        Configured Gradio ChatInterface.

    Raises:
        InitializationError: If environment loading or component setup fails.
    """
    try:
        await load_env(REQUIRED_ENV_VARS)
    except ConfigurationError as exc:
        raise InitializationError("environment loading failed") from exc

    try:
        embedder = await asyncio.to_thread(BgeEmbedder)
    except Exception as exc:  # noqa: BLE001
        raise InitializationError("embedder initialization failed") from exc

    try:
        index = await asyncio.to_thread(PineconeIndex)
    except Exception as exc:  # noqa: BLE001
        raise InitializationError("index initialization failed") from exc

    return build_interface(embedder, index)


def main() -> None:
    """Launch the Gradio chat interface."""
    try:
        interface = asyncio.run(startup())
        interface.launch()
    except Exception as exc:  # noqa: BLE001
        raise InitializationError("application startup failed") from exc


if __name__ == "__main__":
    main()
