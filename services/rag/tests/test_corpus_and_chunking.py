from __future__ import annotations

from pathlib import Path

import pytest

from lego_rag.chunking import chunk_document, tokenize
from lego_rag.corpus import CorpusError, load_document, parse_front_matter
from lego_rag.models import Document


def test_front_matter_is_parsed_without_yaml() -> None:
    parsed = parse_front_matter("---\ntitle: Example\nclassification: public\n---\nBody text\n")
    assert parsed.metadata == {"title": "Example", "classification": "public"}
    assert parsed.body.strip() == "Body text"


def test_unclosed_front_matter_fails_closed() -> None:
    with pytest.raises(CorpusError):
        parse_front_matter("---\ntitle: Example\nno closing marker\n")


def test_unknown_classification_is_downgraded_to_restricted(tmp_path: Path) -> None:
    path = tmp_path / "doc.md"
    path.write_text("---\ntitle: Suspicious\nclassification: super-secret\n---\nbody\n", encoding="utf-8")
    document = load_document(path)
    # Never widen access because of a typo in metadata.
    assert document.classification == "restricted"


def test_missing_corpus_directory_raises(tmp_path: Path) -> None:
    from lego_rag.corpus import load_corpus

    with pytest.raises(CorpusError):
        load_corpus(tmp_path / "absent")


def test_chunks_respect_heading_boundaries() -> None:
    document = Document(
        id="doc",
        title="Doc",
        source="doc.md",
        text="# Alpha\nFirst section body with several words.\n# Beta\nSecond section body with other words.\n",
        classification="public",
    )
    chunks = chunk_document(document)
    assert len(chunks) == 2
    assert chunks[0].heading == "Alpha"
    assert chunks[1].heading == "Beta"
    assert all(chunk.document_id == "doc" for chunk in chunks)
    assert "Second section" in chunks[1].text


def test_chunk_ids_are_stable_across_runs() -> None:
    document = Document(id="doc", title="Doc", source="doc.md", text="Stable content here.", classification="public")
    first = [chunk.id for chunk in chunk_document(document)]
    second = [chunk.id for chunk in chunk_document(document)]
    assert first == second


def test_long_sections_split_with_overlap() -> None:
    sentence = "This sentence contains a number of tokens used for the split test. "
    document = Document(
        id="long",
        title="Long",
        source="long.md",
        text="# Section\n" + sentence * 40,
        classification="public",
    )
    chunks = chunk_document(document, max_tokens=40, overlap=10)
    assert len(chunks) > 1
    assert all(chunk.token_count <= 60 for chunk in chunks)
    assert len({chunk.id for chunk in chunks}) == len(chunks)


def test_tokenizer_lowercases_and_keeps_hyphenated_terms() -> None:
    assert tokenize("D1-starter Sessions API") == ["d1-starter", "sessions", "api"]
