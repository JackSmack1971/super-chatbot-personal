"""Custom exceptions for Dense X Retrieval pipeline."""

from __future__ import annotations

# Use Gradio's base error type when available; provide a fallback otherwise.
try:  # pragma: no cover - import guard
    from gradio.exceptions import GradioError
except Exception:  # pragma: no cover - gradio missing or outdated

    class GradioError(Exception):
        """Fallback base error when GradioError cannot be imported."""

        pass


class DocumentParsingError(GradioError):
    """Raised when a document cannot be parsed for Dense X Retrieval."""


class EmbeddingError(GradioError):
    """Raised when embedding generation fails in Dense X Retrieval."""


class IndexingError(GradioError):
    """Raised when Pinecone index operations fail in Dense X Retrieval."""


class ChatError(GradioError):
    """Raised for chat interface issues in Dense X Retrieval."""


class MonitoringError(GradioError):
    """Raised when cost monitoring fails or budget exceeded."""


class OpenRouterError(GradioError):
    """Raised when OpenRouter API calls fail."""


class CitationError(GradioError):
    """Raised when citation generation fails."""


class RetryError(GradioError):
    """Raised when an operation exceeds retry attempts."""


class InitializationError(GradioError):
    """Raised when application startup fails."""
