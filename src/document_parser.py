"""Asynchronous document parsing utilities for Dense X Retrieval."""

from __future__ import annotations

import asyncio
import os
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


def _resolve_base_dir(base_dir: Path | None) -> Path:
    """Resolve the base directory from an argument or environment variable."""
    env_base = os.getenv("DOCUMENT_BASE_DIR")
    base = Path(env_base) if env_base else base_dir
    return (base or Path(__file__).resolve().parents[1]).resolve()


def _validate_path(path: Path, base_dir: Path) -> Path:
    """Ensure ``path`` is within ``base_dir`` and return its resolved path."""
    resolved_path = path.resolve()
    base = base_dir.resolve()
    if base not in resolved_path.parents and resolved_path != base:
        raise DocumentParsingError("access outside base directory is forbidden")
    return resolved_path


async def parse_document(path: Path, base_dir: Path | None = None) -> str:
    """Parse ``path`` into text ensuring it resides under ``base_dir``.

    Args:
        path: The document to parse.
        base_dir: Optional directory that ``path`` must reside in. Defaults to the
            project root or ``DOCUMENT_BASE_DIR`` environment variable.

    Returns:
        Parsed text content.
    """
    if not isinstance(path, Path):
        raise DocumentParsingError("path must be a pathlib.Path instance")
    base = _resolve_base_dir(base_dir)
    resolved_path = _validate_path(path, base)
    if not resolved_path.exists() or not resolved_path.is_file():
        raise DocumentParsingError("file does not exist")
    parser = _PARSERS.get(resolved_path.suffix.lower())
    if parser is None:
        raise DocumentParsingError("unsupported file type")
    try:
        return await parser(resolved_path)
    except Exception as exc:  # noqa: BLE001
        raise DocumentParsingError("failed to parse document") from exc
