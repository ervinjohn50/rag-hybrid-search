import pytest

from app.parsing import (
    ParseError,
    UnsupportedFileType,
    clean_filename,
    parse_document,
)
from tests.pdf_factory import make_pdf


def test_text_file_is_one_section():
    sections = parse_document("notes.txt", b"  Hello world.\n\nSecond paragraph.  ")
    assert [s.text for s in sections] == ["Hello world.\n\nSecond paragraph."]
    assert sections[0].page is None
    assert sections[0].heading is None


def test_empty_text_file_has_no_sections():
    assert parse_document("empty.txt", b"  \n\n ") == []


def test_byte_order_mark_is_removed():
    assert parse_document("bom.txt", b"\xef\xbb\xbfHello")[0].text == "Hello"


def test_non_utf8_text_is_rejected():
    with pytest.raises(ParseError):
        parse_document("latin.txt", "café".encode("latin-1"))


def test_markdown_splits_on_headings():
    text = b"Intro text.\n\n# Setup\n\nPlug it in.\n\n## Wi-Fi ##\n\nJoin the network.\n"
    sections = parse_document("guide.md", text)
    assert [(s.heading, s.text) for s in sections] == [
        (None, "Intro text."),
        ("Setup", "Plug it in."),
        ("Wi-Fi", "Join the network."),
    ]


def test_markdown_headings_inside_code_fences_are_ignored():
    text = b"# Commands\n\n```bash\n# not a heading\necho hi\n```\n\nAfter the code.\n"
    sections = parse_document("code.md", text)
    assert len(sections) == 1
    assert sections[0].heading == "Commands"
    assert "# not a heading" in sections[0].text
    assert "After the code." in sections[0].text


def test_markdown_heading_with_no_body_is_skipped():
    sections = parse_document("sparse.md", b"# Empty\n\n# Filled\n\nBody.\n")
    assert [(s.heading, s.text) for s in sections] == [("Filled", "Body.")]


def test_pdf_keeps_page_numbers():
    data = make_pdf(["First page text", "Second page text"])
    sections = parse_document("manual.pdf", data)
    assert [s.page for s in sections] == [1, 2]
    assert "First page" in sections[0].text
    assert "Second page" in sections[1].text


def test_pdf_blank_pages_are_skipped_without_renumbering():
    data = make_pdf(["First page text", " ", "Third page text"])
    sections = parse_document("manual.pdf", data)
    assert [s.page for s in sections] == [1, 3]


def test_corrupt_pdf_raises_parse_error():
    with pytest.raises(ParseError):
        parse_document("broken.pdf", b"this is not a pdf")


def test_extension_check_ignores_case():
    assert parse_document("NOTES.TXT", b"Hello")[0].text == "Hello"


@pytest.mark.parametrize("name", ["virus.exe", "archive.zip", "no_extension", "page.html"])
def test_unsupported_types_are_rejected(name):
    with pytest.raises(UnsupportedFileType):
        parse_document(name, b"data")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("report.pdf", "report.pdf"),
        ("../../etc/passwd", "passwd"),
        ("C:\\Users\\someone\\report.pdf", "report.pdf"),
        ("bad\x00name\n.txt", "badname.txt"),
        ("", "untitled"),
        (None, "untitled"),
        ("/", "untitled"),
    ],
)
def test_clean_filename(raw, expected):
    assert clean_filename(raw) == expected


def test_clean_filename_limits_length():
    assert len(clean_filename("a" * 1000 + ".txt")) == 255
