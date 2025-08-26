"""Run code quality checks including coverage tests."""

from __future__ import annotations

import asyncio
import sys
from typing import Sequence


class QualityCheckError(Exception):
    """Raised when a quality check command fails."""


async def run_command(cmd: Sequence[str]) -> None:
    """Run a single command asynchronously."""
    process = await asyncio.create_subprocess_exec(*cmd)
    await process.communicate()
    if process.returncode != 0:
        raise QualityCheckError(
            f"Command {' '.join(cmd)} failed with exit code {process.returncode}"
        )


async def run_checks(commands: Sequence[Sequence[str]] | None = None) -> None:
    """Run standard quality checks or provided commands."""
    cmds = commands or [
        ["black", "src", "tests", "scripts"],
        [
            "flake8",
            "--max-line-length=100",
            "--extend-ignore=E203,E402",
            "src",
            "tests",
        ],
        ["pytest"],
    ]
    for cmd in cmds:
        try:
            await run_command(cmd)
        except QualityCheckError as exc:
            print(exc)
            raise


def main() -> None:
    """Entry point for running quality checks."""
    try:
        asyncio.run(run_checks())
    except QualityCheckError:
        sys.exit(1)


if __name__ == "__main__":
    main()
