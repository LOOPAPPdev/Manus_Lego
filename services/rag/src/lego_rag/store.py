"""SQLite-backed hybrid index: BM25 (FTS5) + hashed vectors, fused with RRF.

Access control is applied while selecting candidate rows, before any scoring, so a
restricted chunk cannot influence the ranking of a public query. Tenant filtering is
applied in Python because the tenant list is a small, variable-length set; the
clearance filter is applied in SQL.
"""

from __future__ import annotations

import json
import sqlite3
import struct
from collections.abc import Iterable, Sequence
from pathlib import Path

from .chunking import chunk_document, content_tokens, tokenize
from .embeddings import Embedder, HashingEmbedder, cosine
from .models import CLEARANCE_ORDER, AccessContext, Chunk, Document, Hit

RRF_K = 60
SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  source TEXT NOT NULL,
  classification TEXT NOT NULL,
  tenants TEXT NOT NULL,
  tags TEXT NOT NULL,
  sha256 TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS chunks (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  ordinal INTEGER NOT NULL,
  heading TEXT NOT NULL,
  text TEXT NOT NULL,
  token_count INTEGER NOT NULL,
  vector BLOB NOT NULL
);
CREATE INDEX IF NOT EXISTS chunks_document ON chunks(document_id);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  chunk_id UNINDEXED,
  text,
  tokenize='porter unicode61'
);
"""


class StoreError(RuntimeError):
    """Raised when the index cannot be built or queried."""


def _pack(vector: Sequence[float]) -> bytes:
    return struct.pack(f"<{len(vector)}f", *vector)


def _unpack(payload: bytes) -> list[float]:
    count = len(payload) // 4
    return list(struct.unpack(f"<{count}f", payload))


def _fts_query(text: str) -> str:
    tokens = [token.replace('"', "") for token in content_tokens(text)]
    if not tokens:
        return ""
    # Quoting each token prevents FTS5 syntax injection from user input.
    return " OR ".join(f'"{token}"' for token in tokens[:32])


class RagIndex:
    def __init__(self, location: str | Path | None = None, *, embedder: Embedder | None = None) -> None:
        self.location = ":memory:" if location is None else str(location)
        if location is not None and str(location) != ":memory:":
            Path(location).parent.mkdir(parents=True, exist_ok=True)
        self.embedder = embedder or HashingEmbedder()
        self.connection = sqlite3.connect(self.location)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        try:
            self.connection.executescript(SCHEMA)
        except sqlite3.OperationalError as exc:  # pragma: no cover - build-dependent
            raise StoreError(f"SQLite FTS5 is unavailable in this build: {exc}") from exc
        self.connection.commit()

    # -- build -------------------------------------------------------------
    def clear(self) -> None:
        self.connection.executescript("DELETE FROM chunks_fts; DELETE FROM chunks; DELETE FROM documents;")
        self.connection.commit()

    def build(self, documents: Iterable[Document], *, max_tokens: int = 180, overlap: int = 30) -> dict[str, int]:
        self.clear()
        document_count = 0
        chunk_count = 0
        for document in documents:
            self.connection.execute(
                "INSERT OR REPLACE INTO documents (id, title, source, classification, tenants, tags, sha256)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    document.id,
                    document.title,
                    document.source,
                    document.classification,
                    ",".join(document.tenants),
                    ",".join(document.tags),
                    document.sha256,
                ),
            )
            document_count += 1
            for chunk in chunk_document(document, max_tokens=max_tokens, overlap=overlap):
                vector = self.embedder.embed(f"{chunk.heading}\n{chunk.text}")
                self.connection.execute(
                    "INSERT OR REPLACE INTO chunks (id, document_id, ordinal, heading, text, token_count, vector)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        chunk.id,
                        chunk.document_id,
                        chunk.ordinal,
                        chunk.heading,
                        chunk.text,
                        chunk.token_count,
                        _pack(vector),
                    ),
                )
                self.connection.execute(
                    "INSERT INTO chunks_fts (chunk_id, text) VALUES (?, ?)",
                    (chunk.id, f"{chunk.heading} {chunk.text}"),
                )
                chunk_count += 1
        self.connection.commit()
        return {"documents": document_count, "chunks": chunk_count}

    # -- query -------------------------------------------------------------
    def _clearance_levels(self, access: AccessContext) -> list[str]:
        ceiling = CLEARANCE_ORDER[access.clearance]
        return [label for label, level in CLEARANCE_ORDER.items() if level <= ceiling]

    def _candidate_rows(self, access: AccessContext) -> list[sqlite3.Row]:
        levels = self._clearance_levels(access)
        placeholders = ",".join("?" for _ in levels)
        # Only the placeholder count is interpolated; every value is bound by SQLite.
        query = (
            # The only interpolation is the placeholder count; values are bound below.
            "SELECT c.id, c.document_id, c.ordinal, c.heading, c.text, c.token_count, c.vector, "  # noqa: S608
            "d.title, d.source, d.classification, d.tenants "
            "FROM chunks c JOIN documents d ON d.id = c.document_id "
            f"WHERE d.classification IN ({placeholders})"
        )
        rows = self.connection.execute(query, levels).fetchall()
        return [
            row for row in rows if access.permits(row["classification"], tuple(filter(None, row["tenants"].split(","))))
        ]

    def _lexical_ranks(self, query: str, permitted: set[str], limit: int) -> dict[str, int]:
        expression = _fts_query(query)
        if not expression:
            return {}
        try:
            rows = self.connection.execute(
                "SELECT chunk_id FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts) LIMIT ?",
                (expression, limit * 4),
            ).fetchall()
        except sqlite3.OperationalError:
            return {}
        ranks: dict[str, int] = {}
        for row in rows:
            chunk_id = row["chunk_id"]
            if chunk_id in permitted and chunk_id not in ranks:
                ranks[chunk_id] = len(ranks) + 1
        return ranks

    def search(
        self,
        query: str,
        access: AccessContext | None = None,
        *,
        k: int = 5,
        min_score: float = 0.0,
        min_vector_similarity: float = 0.08,
    ) -> list[Hit]:
        access = access or AccessContext()
        rows = self._candidate_rows(access)
        if not rows or not content_tokens(query):
            # A stopword-only query has no retrieval signal; returning the whole
            # corpus ranked by hash collisions would be worse than returning nothing.
            return []

        by_id = {row["id"]: row for row in rows}
        query_vector = self.embedder.embed(query)

        scored: list[tuple[str, float]] = []
        for row in rows:
            similarity = cosine(query_vector, _unpack(row["vector"]))
            if similarity >= min_vector_similarity:
                scored.append((row["id"], similarity))
        scored.sort(key=lambda item: (-item[1], item[0]))
        vector_ranks = {chunk_id: index + 1 for index, (chunk_id, _) in enumerate(scored[: max(k * 4, 20)])}

        lexical_ranks = self._lexical_ranks(query, set(by_id), k)

        fused: list[tuple[str, float]] = []
        for chunk_id in set(lexical_ranks) | set(vector_ranks):
            score = 0.0
            if chunk_id in lexical_ranks:
                score += 1.0 / (RRF_K + lexical_ranks[chunk_id])
            if chunk_id in vector_ranks:
                score += 1.0 / (RRF_K + vector_ranks[chunk_id])
            fused.append((chunk_id, score))
        fused.sort(key=lambda item: (-item[1], item[0]))

        query_terms = set(content_tokens(query))
        hits: list[Hit] = []
        for chunk_id, score in fused:
            if score <= min_score:
                continue
            row = by_id[chunk_id]
            chunk = Chunk(
                id=row["id"],
                document_id=row["document_id"],
                ordinal=row["ordinal"],
                heading=row["heading"],
                text=row["text"],
                token_count=row["token_count"],
            )
            hits.append(
                Hit(
                    chunk=chunk,
                    document_title=row["title"],
                    source=row["source"],
                    classification=row["classification"],
                    score=score,
                    lexical_rank=lexical_ranks.get(chunk_id),
                    vector_rank=vector_ranks.get(chunk_id),
                    matched_terms=tuple(sorted(query_terms.intersection(tokenize(chunk.text)))),
                )
            )
            if len(hits) >= k:
                break
        return hits

    def stats(self) -> dict[str, int]:
        documents = self.connection.execute("SELECT COUNT(*) AS n FROM documents").fetchone()["n"]
        chunks = self.connection.execute("SELECT COUNT(*) AS n FROM chunks").fetchone()["n"]
        return {"documents": documents, "chunks": chunks}

    def document_manifest(self) -> list[dict[str, object]]:
        rows = self.connection.execute(
            "SELECT id, title, source, classification, tenants, sha256 FROM documents ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> RagIndex:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def index_metadata(path: Path) -> dict[str, object] | None:
    """Read the sidecar metadata of a persisted index, when present."""

    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
