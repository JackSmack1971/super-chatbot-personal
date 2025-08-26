"""Citation span utilities for Dense X Retrieval."""

from __future__ import annotations

from typing import Dict

from .exceptions import CitationError


def generate_citation(context: str, answer: str) -> Dict[str, int]:
    """Return character span for *answer* within *context*.

    Args:
        context: Source text to search.
        answer: Substring expected within ``context``.

    Returns:
        Dictionary with ``start`` and ``end`` indices representing the citation span.

    Raises:
        CitationError: If inputs are invalid or the answer is not found.
    """
    if not isinstance(context, str) or not isinstance(answer, str):
        raise CitationError("context and answer must be strings")
    snippet = answer.strip()
    if not context or not snippet:
        raise CitationError("context and answer must be non-empty")
    start = context.find(snippet)
    if start == -1:
        raise CitationError("answer not found in context")
    end = start + len(snippet)
    return {"start": start, "end": end}
