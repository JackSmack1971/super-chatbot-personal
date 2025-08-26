import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.citation import generate_citation  # noqa: E402
from src.exceptions import CitationError  # noqa: E402


def test_generate_citation_success() -> None:
    context = "This is pair 5 for testing citations."
    span = generate_citation(context, "pair 5")
    assert span == {"start": 8, "end": 14}


def test_generate_citation_not_found() -> None:
    with pytest.raises(CitationError):
        generate_citation("no match here", "absent")
