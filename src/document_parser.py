"""Asynchronous document parsing utilities for Dense X Retrieval."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Awaitable, Callable, Dict

import aiofiles  # type: ignore[import-not-found,import-untyped]
from PyPDF2 import PdfReader  # type: ignore[import-not-found]

from .exceptions import DocumentParsingError


async def _read_text(path: Path) -> str:
    """Read a text or markdown file asynchronously."""
    async with aiofiles.open(path, "r", encoding="utf-8") as handle:
        return await handle.read()


async def _read_pdf(path: Path) -> str:
    """Read a PDF file asynchronously."""

    def _sync_read() -> str:
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return await asyncio.to_thread(_sync_read)


_PARSERS: Dict[str, Callable[[Path], Awaitable[str]]] = {
    ".txt": _read_text,
    ".md": _read_text,
    ".pdf": _read_pdf,
}


async def parse_document(path: Path) -> str:
    """Parse a document into text for Dense X Retrieval."""
    if not isinstance(path, Path):
        raise DocumentParsingError("path must be a pathlib.Path instance")
    if not path.exists() or not path.is_file():
        raise DocumentParsingError("file does not exist")
    parser = _PARSERS.get(path.suffix.lower())
    if parser is None:
        raise DocumentParsingError("unsupported file type")
    try:
        return await parser(path)
    except Exception as exc:  # noqa: BLE001
        raise DocumentParsingError("failed to parse document") from exc
