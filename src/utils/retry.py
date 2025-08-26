"""Generic async retry utilities with exponential backoff."""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar, Type

from ..exceptions import RetryError

T = TypeVar("T")


async def async_retry(
    func: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    timeout: float = 30.0,
    error_cls: Type[Exception] = RetryError,
) -> T:
    """Retry an async callable with exponential backoff and timeout.

    Args:
        func: Async callable with no arguments.
        max_attempts: Maximum number of attempts before failing.
        base_delay: Initial backoff delay in seconds.
        timeout: Per-attempt timeout in seconds.
        error_cls: Exception type raised after final failure.

    Returns:
        Result of the callable if successful.

    Raises:
        error_cls: If all attempts fail or timeout occurs.
    """
    if max_attempts < 1 or base_delay <= 0 or timeout <= 0:
        raise error_cls("invalid retry parameters")
    for attempt in range(max_attempts):
        try:
            return await asyncio.wait_for(func(), timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            if attempt == max_attempts - 1:
                raise error_cls("operation failed after retries") from exc
            await asyncio.sleep(base_delay * 2**attempt)
    raise error_cls("operation failed after retries")
