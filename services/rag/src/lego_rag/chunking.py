"""Deterministic, heading-aware chunking.

Chunks never cross a heading boundary, which keeps citations meaningful: a
retrieved chunk belongs to exactly one section. Long sections are split on
sentence boundaries with an overlap so a fact spanning a boundary is still
recoverable.
"""

from __future__ import annotations

import hashlib
import re

from .models import Chunk, Document

WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")

# Function words carry no retrieval signal. They are excluded from lexical queries
# and from the "is this hit actually about the question" test, otherwise a query
# such as "revenue for the division" would match any document containing "for".
STOPWORDS = frozenset(
    {
        "a",
        "about",
        "after",
        "all",
        "also",
        "an",
        "and",
        "any",
        "are",
        "as",
        "at",
        "be",
        "because",
        "been",
        "before",
        "being",
        "between",
        "both",
        "but",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "doing",
        "done",
        "during",
        "each",
        "few",
        "for",
        "from",
        "further",
        "had",
        "has",
        "have",
        "having",
        "he",
        "her",
        "here",
        "hers",
        "him",
        "his",
        "how",
        "i",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "itself",
        "just",
        "me",
        "more",
        "most",
        "my",
        "no",
        "nor",
        "not",
        "now",
        "of",
        "off",
        "on",
        "once",
        "only",
        "or",
        "other",
        "our",
        "ours",
        "out",
        "over",
        "own",
        "same",
        "she",
        "should",
        "so",
        "some",
        "such",
        "than",
        "that",
        "the",
        "their",
        "theirs",
        "them",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "to",
        "too",
        "under",
        "until",
        "up",
        "very",
        "was",
        "we",
        "were",
        "what",
        "when",
        "where",
        "which",
        "while",
        "who",
        "whom",
        "why",
        "will",
        "with",
        "would",
        "you",
        "your",
        "yours",
    }
)


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD.finditer(text)]


def content_tokens(text: str) -> list[str]:
    """Tokens that carry retrieval signal (stopwords removed)."""

    return [token for token in tokenize(text) if token not in STOPWORDS]


def _split_long(text: str, max_tokens: int, overlap: int) -> list[str]:
    sentences = [sentence.strip() for sentence in SENTENCE_SPLIT.split(text) if sentence.strip()]
    pieces: list[str] = []
    current: list[str] = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(tokenize(sentence))
        if current and current_tokens + sentence_tokens > max_tokens:
            pieces.append(" ".join(current))
            if overlap > 0:
                tail: list[str] = []
                tail_tokens = 0
                for previous in reversed(current):
                    tail.insert(0, previous)
                    tail_tokens += len(tokenize(previous))
                    if tail_tokens >= overlap:
                        break
                current = tail
                current_tokens = tail_tokens
            else:
                current = []
                current_tokens = 0
        current.append(sentence)
        current_tokens += sentence_tokens

    if current:
        pieces.append(" ".join(current))
    return pieces


def chunk_document(document: Document, *, max_tokens: int = 180, overlap: int = 30) -> list[Chunk]:
    """Split a document into heading-bounded chunks with stable ids."""

    sections: list[tuple[str, list[str]]] = []
    heading = document.title
    buffer: list[str] = []

    for line in document.text.splitlines():
        match = HEADING.match(line.strip())
        if match:
            if any(item.strip() for item in buffer):
                sections.append((heading, buffer))
            heading = match.group(2).strip() or heading
            buffer = []
            continue
        buffer.append(line)
    if any(item.strip() for item in buffer):
        sections.append((heading, buffer))

    if not sections:
        sections = [(document.title, [document.text])]

    chunks: list[Chunk] = []
    ordinal = 0
    for section_heading, lines in sections:
        body = "\n".join(lines).strip()
        if not body:
            continue
        for piece in _split_long(body, max_tokens, overlap):
            digest = hashlib.sha256(f"{document.id}:{ordinal}:{piece[:64]}".encode()).hexdigest()[:16]
            chunks.append(
                Chunk(
                    id=f"{document.id}#{ordinal}-{digest}",
                    document_id=document.id,
                    ordinal=ordinal,
                    heading=section_heading,
                    text=piece,
                    token_count=len(tokenize(piece)),
                )
            )
            ordinal += 1
    return chunks
