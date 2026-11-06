import pytest

from app.chunking import Chunk, chunk_sections, embedding_text
from app.parsing import Section

SIZE = 200
OVERLAP = 40


def sentences(count: int) -> str:
    return " ".join(f"Sentence number {i} talks about something." for i in range(count))


def test_short_section_stays_whole():
    chunks = chunk_sections([Section(text="Just one line.")], SIZE, OVERLAP)
    assert [c.text for c in chunks] == ["Just one line."]


def test_long_text_respects_chunk_size():
    chunks = chunk_sections([Section(text=sentences(100))], SIZE, OVERLAP)
    assert len(chunks) > 1
    assert all(len(c.text) <= SIZE for c in chunks)


def test_no_words_are_lost():
    text = sentences(100)
    chunks = chunk_sections([Section(text=text)], SIZE, OVERLAP)
    combined = " ".join(c.text for c in chunks)
    for i in range(100):
        assert f"Sentence number {i} talks" in combined


def test_neighbouring_chunks_overlap():
    chunks = chunk_sections([Section(text=sentences(100))], SIZE, OVERLAP)
    for first, second in zip(chunks, chunks[1:], strict=False):
        opening_words = " ".join(second.text.split()[:3])
        assert opening_words in first.text


def test_zero_overlap_produces_no_repeats():
    chunks = chunk_sections([Section(text=sentences(100))], SIZE, 0)
    combined = " ".join(c.text for c in chunks)
    assert combined.count("Sentence number 50 talks") == 1


def test_splits_prefer_paragraph_boundaries():
    first = "A" * 120 + "."
    second = "B" * 120 + "."
    chunks = chunk_sections([Section(text=f"{first}\n\n{second}")], SIZE, 0)
    assert [c.text for c in chunks] == [first, second]


def test_line_breaks_survive_in_long_sections():
    table = "\n".join(f"| row {i} | value {i} |" for i in range(60))
    chunks = chunk_sections([Section(text=table)], SIZE, OVERLAP)
    assert len(chunks) > 1
    assert all("\n" in c.text for c in chunks)
    assert "| row 0 | value 0 |\n| row 1 | value 1 |" in chunks[0].text


def test_unbroken_token_is_split_to_fit():
    chunks = chunk_sections([Section(text="x" * 1000)], SIZE, OVERLAP)
    assert all(len(c.text) <= SIZE for c in chunks)
    assert sum(c.text.count("x") for c in chunks) >= 1000


def test_location_is_kept_and_sections_are_not_merged():
    sections = [
        Section(text="Page one text.", page=1),
        Section(text="Page two text.", page=2),
        Section(text="Under a heading.", heading="Setup"),
    ]
    chunks = chunk_sections(sections, SIZE, OVERLAP)
    assert [(c.text, c.page, c.heading) for c in chunks] == [
        ("Page one text.", 1, None),
        ("Page two text.", 2, None),
        ("Under a heading.", None, "Setup"),
    ]


def test_indexes_run_across_sections():
    sections = [Section(text=sentences(30), page=1), Section(text=sentences(30), page=2)]
    chunks = chunk_sections(sections, SIZE, OVERLAP)
    assert [c.index for c in chunks] == list(range(len(chunks)))


def test_blank_section_produces_nothing():
    assert chunk_sections([Section(text="   \n\n  ")], SIZE, OVERLAP) == []


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        chunk_sections([Section(text="text")], 100, 100)


def test_embedding_text_adds_title_and_heading():
    chunk = Chunk(text="Body text.", index=0, heading="Setup")
    assert embedding_text(chunk, "manual.md") == "manual.md - Setup\nBody text."


def test_embedding_text_without_heading():
    chunk = Chunk(text="Body text.", index=0)
    assert embedding_text(chunk, "notes.txt") == "notes.txt\nBody text."
