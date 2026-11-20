"""Corpus loading with front-matter metadata.

Documents are plain text or Markdown files with an optional YAML-ish header:

```
---
title: D1 sessions API
classification: internal
tenants: acme, public
tags: d1, sessions
---
Body text…
```

The parser is intentionally small (no YAML dependency) and fails closed: an
unknown classification is treated as ``restricted`` rather than downgraded.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .models import Classification, Document

ALLOWED_CLASSIFICATIONS: tuple[Classification, ...] = ("public", "internal", "restricted")
SUPPORTED_SUFFIXES = {".md", ".txt", ".markdown"}


class CorpusError(RuntimeError):
    """Raised when a document cannot be parsed safely."""


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    metadata: dict[str, str]
    body: str


def parse_front_matter(text: str) -> ParsedDocument:
    if not text.startswith("---"):
        return ParsedDocument(metadata={}, body=text)

    lines = text.splitlines()
    metadata: dict[str, str] = {}
    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        stripped = line.strip()
        if stripped == "---":
            end_index = index
            break
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise CorpusError(f"Invalid front-matter line {index + 1}: expected 'key: value'")
        key, value = stripped.split(":", 1)
        metadata[key.strip().lower()] = value.strip()

    if end_index is None:
        raise CorpusError("Front matter opened with '---' but never closed")
    body = "\n".join(lines[end_index + 1 :]).lstrip("\n")
    return ParsedDocument(metadata=metadata, body=body)


def _split_list(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(",") if part.strip())


def load_document(path: Path, *, default_classification: Classification = "internal") -> Document:
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise CorpusError(f"Cannot read {path}: {exc}") from exc

    parsed = parse_front_matter(raw)
    declared = parsed.metadata.get("classification", default_classification).lower()
    if declared not in ALLOWED_CLASSIFICATIONS:
        # Fail closed: an unknown label must never widen access.
        declared = "restricted"

    title = parsed.metadata.get("title") or path.stem.replace("-", " ").replace("_", " ").title()
    tenants = _split_list(parsed.metadata.get("tenants", ""))
    tags = _split_list(parsed.metadata.get("tags", ""))

    return Document(
        id=parsed.metadata.get("id") or path.stem,
        title=title,
        source=path.as_posix(),
        text=parsed.body,
        classification=declared,  # type: ignore[arg-type]
        tenants=tenants,
        sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        tags=tags,
    )


def load_corpus(directory: Path, *, default_classification: Classification = "internal") -> list[Document]:
    if not directory.is_dir():
        raise CorpusError(f"Corpus directory not found: {directory}")
    documents: list[Document] = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            documents.append(load_document(path, default_classification=default_classification))
    if not documents:
        raise CorpusError(f"No supported documents in {directory}")
    return documents
