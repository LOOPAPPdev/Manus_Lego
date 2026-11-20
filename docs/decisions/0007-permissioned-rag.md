# ADR 0007 — Permissioned retrieval with extractive answers

- **Status:** accepted
- **Date:** 2026-11-20

## Context

The specification asks for a RAG service with prompt-injection defences, citations and an
evaluation harness. The repository has no tenant data and no model budget, and the
sandbox has no embedding API. Whatever is built must be honest about what it proves: a
demo over synthetic documents, not a claim that retrieval is safe for a real tenant.

## Decision

Build a small, dependency-light service whose security properties are testable:

1. **ACL before scoring.** Documents carry `classification` (`public`/`internal`/
   `restricted`) and `tenants`. The store filters candidate rows by the caller's clearance
   and tenant set *before* ranking, so a restricted chunk is never scored, never returned
   and cannot leak through a score side-channel. An unrecognised classification fails
   closed to `restricted`.
2. **Hybrid retrieval.** SQLite FTS5 for lexical matching plus a deterministic signed
   hashing embedder (256 dims) for fuzzy matching, fused with reciprocal rank fusion
   (`k=60`). The embedder is a stand-in for a real model, and the code says so.
3. **Evidence or refusal.** An answer is only produced when a retrieved chunk overlaps a
   *content* term of the question (stopwords do not count). Otherwise the service refuses
   with a reason instead of returning the least-bad neighbour.
4. **Retrieved text is data.** Every chunk is wrapped in `<untrusted source="…">` with the
   closing tag neutralised, and scanned against nine instruction-pattern rules. Findings
   are surfaced in `guardrail_flags` with the chunk id; the content is never silently
   dropped, so a reviewer can see that a source tried to steer the model.
5. **Measured quality.** `tests/fixtures/evaluation.json` labels four questions over five
   documents (including a restricted tenant document and a poisoned document).
   `lego-rag eval` and the pytest suite report recall@k, MRR and refusal rate. The numbers
   describe *this corpus only*.

## Consequences

**Positive.** Every claim has a test: ACL filtering, fail-closed classification,
injection detection, refusal, and retrieval quality. No network dependency, no key, no
cost. The store is a single SQLite file that can be deleted and rebuilt.

**Negative.** The hashing embedder is not semantic: it matches character n-grams, so a
paraphrase with no shared vocabulary will miss. Recall on a real corpus would be worse, and
the evaluation numbers must not be quoted as a product metric. Swapping in a real embedder
changes the vector dimension and requires a reindex — the store records the embedder name
in its metadata for exactly this reason.

**Rejected alternatives.**

- *Call an external embedding API.* No key in this environment, and it would make tests
  non-deterministic and network-dependent.
- *A generative answerer by default.* Without a verifiable model, a generated sentence is
  an ungrounded claim. The service therefore defaults to extraction from cited chunks and
  accepts a synthesizer only as an explicit injection point, with `INSUFFICIENT_EVIDENCE`
  handled as a refusal.
- *Dropping flagged documents.* Hides an attack instead of recording it.
