"""Extract text from uploaded files.

Files are handled as bytes in memory. The uploaded filename only selects a parser
and is shown as a label; it is never used as a filesystem path.
"""

import io
import re
from dataclasses import dataclass
from pathlib import PurePosixPath

from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".md", ".markdown", ".txt"}

_MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


class UnsupportedFileType(ValueError):
    """The file extension is not one we can parse."""


class ParseError(ValueError):
    """The file looks like a supported type but its contents could not be read."""


@dataclass(frozen=True)
class Section:
    """A run of text with the location it came from."""

    text: str
    page: int | None = None
    heading: str | None = None


def clean_filename(filename: str | None) -> str:
    """Reduce a client-supplied filename to a safe display name."""
    name = PurePosixPath((filename or "").replace("\\", "/")).name
    name = "".join(ch for ch in name if ch.isprintable()).strip()
    return name[:255] or "untitled"


def parse_document(filename: str, data: bytes) -> list[Section]:
    """Return the non-empty sections of a document, in reading order."""
    extension = PurePosixPath(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileType(f"Unsupported file type: {extension or 'no extension'}")
    if extension == ".pdf":
        return _parse_pdf(data)
    text = _decode(data)
    if extension in {".md", ".markdown"}:
        return _parse_markdown(text)
    return [Section(text=text.strip())] if text.strip() else []


def _decode(data: bytes) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ParseError("Text files must be UTF-8 encoded") from exc


def _parse_pdf(data: bytes) -> list[Section]:
    try:
        reader = PdfReader(io.BytesIO(data))
        encrypted = reader.is_encrypted
        pages = [] if encrypted else [page.extract_text() or "" for page in reader.pages]
    except Exception as exc:
        # Uploads are untrusted, and malformed PDFs raise many exception types inside pypdf.
        raise ParseError("Could not read this PDF") from exc
    if encrypted:
        raise ParseError("Encrypted PDFs are not supported")
    return [
        Section(text=text.strip(), page=number)
        for number, text in enumerate(pages, start=1)
        if text.strip()
    ]


def _parse_markdown(text: str) -> list[Section]:
    """Split Markdown at headings, ignoring heading-like lines inside code fences."""
    sections: list[Section] = []
    heading: str | None = None
    lines: list[str] = []
    in_fence = False

    def flush() -> None:
        body = "\n".join(lines).strip()
        if body:
            sections.append(Section(text=body, heading=heading))
        lines.clear()

    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        match = None if in_fence else _MARKDOWN_HEADING.match(line)
        if match:
            flush()
            heading = match.group(2)
        else:
            lines.append(line)
    flush()
    return sections
