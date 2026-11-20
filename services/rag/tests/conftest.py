from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from lego_rag.corpus import load_corpus
from lego_rag.models import Document
from lego_rag.store import RagIndex

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def corpus() -> list[Document]:
    return load_corpus(FIXTURES / "corpus")


@pytest.fixture
def index(corpus: list[Document]) -> Iterator[RagIndex]:
    instance = RagIndex(":memory:")
    instance.build(corpus)
    try:
        yield instance
    finally:
        instance.close()
