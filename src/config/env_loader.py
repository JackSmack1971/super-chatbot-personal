"""Utilities for securely loading required environment variables."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Dict, Iterable

from dotenv import load_dotenv  # type: ignore[import-not-found]


class ConfigurationError(Exception):
    """Raised when required environment configuration is missing or invalid."""


async def load_env(required_vars: Iterable[str]) -> Dict[str, str]:
    """Load and validate environment variables asynchronously.

    Args:
        required_vars: Names of required environment variables.

    Returns:
        Mapping of variable names to their resolved values.

    Raises:
        ConfigurationError: If any required variable is missing or invalid.
    """

    vars_list = list(required_vars)
    if not all(isinstance(var, str) and var for var in vars_list):
        raise ConfigurationError(
            "required_vars must contain non-empty strings"  # noqa: E501
        )

    await asyncio.to_thread(load_dotenv, Path(".env"))

    resolved: Dict[str, str] = {}
    for var in vars_list:
        value = os.getenv(var)
        if value is None or not value.strip():
            raise ConfigurationError(f"Missing environment variable: {var}")
        resolved[var] = value

    return resolved
