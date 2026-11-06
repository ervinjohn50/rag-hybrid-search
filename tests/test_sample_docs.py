"""The sample documents are used by the retrieval eval, so check that they parse as expected."""

from pathlib import Path

import pytest

from app.chunking import chunk_sections
from app.parsing import parse_document

SAMPLE_DOCS = Path(__file__).parent.parent / "sample_docs"


@pytest.mark.parametrize(
    "name", ["gateway-manual.md", "troubleshooting.txt", "warranty-and-returns.pdf"]
)
def test_sample_document_produces_chunks(name):
    sections = parse_document(name, (SAMPLE_DOCS / name).read_bytes())
    chunks = chunk_sections(sections, chunk_size=1200, overlap=150)
    assert chunks
    assert all(len(chunk.text) <= 1200 for chunk in chunks)


def test_sample_pdf_has_three_numbered_pages():
    data = (SAMPLE_DOCS / "warranty-and-returns.pdf").read_bytes()
    sections = parse_document("warranty-and-returns.pdf", data)
    assert [section.page for section in sections] == [1, 2, 3]
    assert "RMA-LF204417" in sections[1].text


def test_sample_manual_keeps_its_headings():
    data = (SAMPLE_DOCS / "gateway-manual.md").read_bytes()
    headings = {section.heading for section in parse_document("gateway-manual.md", data)}
    assert {"Factory reset", "Parental schedules", "Scheduled maintenance"} <= headings
