"""Domain models for retrieval, citations and answers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Classification = Literal["public", "internal", "restricted"]

CLEARANCE_ORDER: dict[str, int] = {"public": 0, "internal": 1, "restricted": 2}


@dataclass(frozen=True, slots=True)
class AccessContext:
    """Who is asking.

    ``clearance`` is the highest classification the caller may read. ``tenants``
    is the set of tenant labels the caller belongs to; a document with no tenant
    label is available to every tenant.
    """

    clearance: Classification = "public"
    tenants: frozenset[str] = frozenset({"public"})
    subject: str = "anonymous"

    def permits(self, classification: str, tenants: tuple[str, ...]) -> bool:
        if CLEARANCE_ORDER.get(classification, 99) > CLEARANCE_ORDER[self.clearance]:
            return False
        if not tenants:
            return True
        return bool(self.tenants.intersection(tenants))


@dataclass(frozen=True, slots=True)
class Document:
    id: str
    title: str
    source: str
    text: str
    classification: Classification = "internal"
    tenants: tuple[str, ...] = ()
    sha256: str = ""
    tags: tuple[str, ...] = ()

    @property
    def acl_label(self) -> str:
        return f"{self.classification}:{','.join(self.tenants) or '*'}"


@dataclass(frozen=True, slots=True)
class Chunk:
    id: str
    document_id: str
    ordinal: int
    heading: str
    text: str
    token_count: int


@dataclass(frozen=True, slots=True)
class Hit:
    chunk: Chunk
    document_title: str
    source: str
    classification: str
    score: float
    lexical_rank: int | None
    vector_rank: int | None
    matched_terms: tuple[str, ...] = ()

    @property
    def citation(self) -> str:
        return f"{self.source}#{self.chunk.ordinal}"


@dataclass(frozen=True, slots=True)
class Citation:
    document_id: str
    title: str
    source: str
    chunk_id: str
    excerpt: str


@dataclass(slots=True)
class Answer:
    question: str
    answer: str | None
    citations: list[Citation] = field(default_factory=list)
    refused: bool = False
    reason: str | None = None
    guardrail_flags: list[str] = field(default_factory=list)
    hits: list[Hit] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "question": self.question,
            "answer": self.answer,
            "refused": self.refused,
            "reason": self.reason,
            "citations": [
                {
                    "document_id": citation.document_id,
                    "title": citation.title,
                    "source": citation.source,
                    "chunk_id": citation.chunk_id,
                    "excerpt": citation.excerpt,
                }
                for citation in self.citations
            ],
            "guardrail_flags": self.guardrail_flags,
            "hits": [
                {
                    "chunk_id": hit.chunk.id,
                    "document_id": hit.chunk.document_id,
                    "title": hit.document_title,
                    "score": round(hit.score, 6),
                    "classification": hit.classification,
                    "lexical_rank": hit.lexical_rank,
                    "vector_rank": hit.vector_rank,
                }
                for hit in self.hits
            ],
        }
