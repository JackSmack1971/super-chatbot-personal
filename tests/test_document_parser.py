import sys
import types
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


class AsyncFile:
    def __init__(
        self, path: Path, mode: str = "r", encoding: str | None = None
    ) -> None:
        self._f = open(path, mode, encoding=encoding)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._f.close()

    async def read(self) -> str:
        return self._f.read()


aiofiles_stub = types.SimpleNamespace(
    open=lambda path, mode="r", encoding="utf-8": AsyncFile(path, mode, encoding)
)
sys.modules["aiofiles"] = aiofiles_stub


class DummyPage:
    def extract_text(self) -> str:
        return ""


class DummyReader:
    def __init__(self, path):
        self.pages = [DummyPage()]


sys.modules["PyPDF2"] = types.SimpleNamespace(PdfReader=DummyReader)

from src.document_parser import parse_document  # noqa: E402
from src.exceptions import DocumentParsingError  # noqa: E402

import pytest  # noqa: E402


@pytest.mark.asyncio
async def test_parse_text_files(tmp_path: Path) -> None:
    txt = tmp_path / "sample.txt"
    md = tmp_path / "sample.md"
    txt.write_text("hello")
    md.write_text("world")
    assert await parse_document(txt, base_dir=tmp_path) == "hello"
    assert await parse_document(md, base_dir=tmp_path) == "world"


@pytest.mark.asyncio
async def test_parse_pdf_file(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"")
    text = await parse_document(pdf_path, base_dir=tmp_path)
    assert isinstance(text, str)


@pytest.mark.asyncio
async def test_parse_document_invalid(tmp_path: Path) -> None:
    invalid = tmp_path / "nope.docx"
    invalid.write_text("oops")
    with pytest.raises(DocumentParsingError):
        await parse_document(invalid, base_dir=tmp_path)


@pytest.mark.asyncio
async def test_rejects_path_traversal(tmp_path: Path) -> None:
    base = tmp_path / "base"
    base.mkdir()
    outside = tmp_path / "secret.txt"
    outside.write_text("secret")
    traversal = base / ".." / outside.name
    with pytest.raises(DocumentParsingError):
        await parse_document(traversal, base_dir=base)
