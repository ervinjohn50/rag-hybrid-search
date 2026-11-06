"""Split document sections into overlapping chunks for embedding."""

import re
from dataclasses import dataclass

from app.parsing import Section

# Tried in order: paragraphs, then lines, then sentences, then words.
_SEPARATORS = (r"\n\s*\n", r"\n", r"(?<=[.!?])\s+", r"\s+")


@dataclass(frozen=True)
class Chunk:
    text: str
    index: int
    page: int | None = None
    heading: str | None = None


def chunk_sections(sections: list[Section], chunk_size: int, overlap: int) -> list[Chunk]:
    """Chunk each section separately, so a chunk never spans two pages or headings."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    chunks: list[Chunk] = []
    for section in sections:
        for text in _split(section.text, chunk_size, overlap):
            chunks.append(
                Chunk(text=text, index=len(chunks), page=section.page, heading=section.heading)
            )
    return chunks


def _split(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks: list[str] = []
    current = ""
    for piece in _atomize(text.strip(), chunk_size, _SEPARATORS):
        if len((current + piece).rstrip()) <= chunk_size:
            current += piece
            continue
        chunks.append(current.strip())
        tail = _overlap_tail(current.rstrip(), overlap)
        current = tail + piece if len((tail + piece).rstrip()) <= chunk_size else piece
    if current.strip():
        chunks.append(current.strip())
    return chunks


def _atomize(text: str, chunk_size: int, separators: tuple[str, ...]) -> list[str]:
    """Break text at the coarsest boundary that fits, keeping each separator's whitespace.

    Keeping the whitespace means line breaks in tables, lists and code survive when
    the pieces are joined back together.
    """
    if len(text) <= chunk_size:
        return [text] if text.strip() else []
    if not separators:
        # A single unbroken token longer than a chunk, such as a long URL or base64 blob.
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    parts = re.split(f"({separators[0]})", text)
    pieces: list[str] = []
    for i in range(0, len(parts), 2):
        sub_pieces = _atomize(parts[i], chunk_size, separators[1:])
        if sub_pieces and i + 1 < len(parts):
            sub_pieces[-1] += parts[i + 1]
        pieces.extend(sub_pieces)
    return pieces


def _overlap_tail(text: str, overlap: int) -> str:
    """Return up to `overlap` trailing characters, starting on a word boundary."""
    if overlap <= 0 or len(text) <= overlap:
        return ""
    tail = text[-overlap:]
    if not text[-overlap - 1].isspace():
        _, space, tail = tail.partition(" ")
        if not space:
            return ""
    tail = tail.strip()
    return f"{tail} " if tail else ""


def embedding_text(chunk: Chunk, title: str) -> str:
    """Text to embed: the chunk plus its document title and heading for extra context."""
    context = " - ".join(part for part in (title, chunk.heading) if part)
    return f"{context}\n{chunk.text}" if context else chunk.text
