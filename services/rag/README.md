# lego-rag

Permissioned retrieval-augmented generation for Manus LEGO.

## Why this exists

The catalog tells you which components exist. Answering *"which template fits this
requirement, and on what evidence?"* needs retrieval over documentation — with three
properties that a naive vector store does not give you:

1. **Permissioned retrieval.** Classification and tenant filters are applied *before*
   scoring, so a restricted chunk cannot influence a public answer.
2. **Citations or refusal.** Every claim carries the chunk that supports it. If nothing
   clears the relevance floor, the service returns no answer and says why.
3. **Poisoned-document resistance.** Retrieved text is untrusted input: it is wrapped,
   scanned for instruction-like patterns and never executed.

## Design

| Concern | Choice | Reason |
|---|---|---|
| Storage | SQLite + FTS5 | Zero infrastructure, transactional, portable in CI |
| Lexical search | BM25 (`bm25()` in FTS5) | Strong baseline, no model download |
| Vector search | Deterministic hashing embedder, 256 dims | Reproducible offline; swappable behind a protocol |
| Fusion | Reciprocal rank fusion (k=60) | Robust to score-scale differences between retrievers |
| Generation | Extractive by default; optional LLM | Deterministic tests; LLM is opt-in and citation-checked |

## Commands

```bash
uv sync --project services/rag
uv run --project services/rag lego-rag ingest tests/fixtures/corpus --store .data/rag.sqlite3
uv run --project services/rag lego-rag query "which template has D1 sessions" --clearance internal --tenant public
uv run --project services/rag lego-rag eval tests/fixtures/evaluation.json --corpus tests/fixtures/corpus
```

## Limits

The hashing embedder captures lexical overlap, not semantics. It is a deliberate
baseline: it makes evaluation cheap and honest. Replacing it with a hosted embedding
model is a configuration change plus a new evaluation run — not a redesign.
