# ADR 0003 — Two isolated Python services, not one uv workspace

- **Status:** accepted
- **Date:** 2026-11-20

## Context

Two Python programs are needed: the governance orchestrator (`lego` CLI, gates,
traceability) and the retrieval service (corpus, chunking, guardrails, answers). They have
different dependency profiles and very different threat surfaces. The orchestrator runs in
CI and reads the repository; the retrieval service processes untrusted text and will, in a
real deployment, hold a tenant's documents.

The catalog engine (`scripts/lego_catalog.py`) already exists and is deliberately
stdlib-only, so it runs anywhere with a bare `python3`.

## Decision

Keep **one `pyproject.toml` and one `uv.lock` per service** (`services/orchestrator`,
`services/rag`) rather than a single uv workspace:

- Each service is installed and locked independently: `uv sync --project services/<name>`.
- Neither service depends on the other. Shared behaviour is duplicated *on purpose* where
  it is small (path resolution, evidence hashing) and exposed as a subprocess boundary
  where it is large (the catalog engine).
- The stdlib-only engine stays outside both environments; the orchestrator calls it with
  `sys.executable`, which is also what a contributor's `python3` would do.
- Tests run from the repository root with a `pytest.ini` that adds both `src` directories
  to `pythonpath`, so a single `pytest` invocation exercises both services without
  installing them into one environment.

## Consequences

**Positive.** The retrieval service can be deployed, pinned and scanned without dragging
the CLI's dependencies along, and a supply-chain incident in one service cannot silently
change the other's behaviour. Locks stay small and reviewable.

**Negative.** Two `uv sync` calls, two lockfiles, and a small amount of duplicated utility
code (`paths.py`, evidence hashing). The duplication is intentional: an internal shared
package would reintroduce the coupling this decision avoids, and would need its own
release process.

**Rejected alternatives.**

- *A uv workspace with a shared `lego_common` package.* Cheaper for the two duplicated
  helpers, but couples the deployment and scanning surface of both services.
- *Installing the services into the repository root environment.* Makes "works on my
  machine" depend on whichever service was synced last.
