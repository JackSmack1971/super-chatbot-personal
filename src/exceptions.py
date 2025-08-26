"""Custom exceptions for Dense X Retrieval pipeline."""

from __future__ import annotations


class DocumentParsingError(Exception):
    """Raised when a document cannot be parsed for Dense X Retrieval."""


class EmbeddingError(Exception):
    """Raised when embedding generation fails in Dense X Retrieval."""


class IndexingError(Exception):
    """Raised when Pinecone index operations fail in Dense X Retrieval."""


class ChatError(Exception):
    """Raised for chat interface issues in Dense X Retrieval."""


class MonitoringError(Exception):
    """Raised when cost monitoring fails or budget exceeded."""


class OpenRouterError(Exception):
    """Raised when OpenRouter API calls fail."""
