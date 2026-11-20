# ADR 0004 — Port the ranking function, then prove parity with a fixture

- **Status:** accepted
- **Date:** 2026-11-20

## Context

The web app sorts search results in the browser, the API ranks on the server, and the
catalog engine ranks in Python. If the three disagree, a user sees a different order in the
SPA than `lego select` would produce, and the "selection" artifact stops being a faithful
record of what the UI showed.

Calling Python from the browser is not an option, and calling the API for every keystroke
would make the SPA dependent on the server for a purely deterministic sort.

## Decision

Reimplement the scoring in TypeScript (`packages/shared/src/ranking.ts`) as a **faithful
port** of `ranked()` in `scripts/lego_catalog.py`, and make the equivalence a test
artefact rather than a claim:

- `tests/fixtures/generate_ranking_cases.py` runs the Python implementation over a fixed
  set of queries and writes `tests/fixtures/ranking-cases.json` (14 cases: exact title
  match, tag match, stopword-only query, ties, provider filtering, empty query).
- The TypeScript suite asserts the port reproduces every case byte-for-byte, including
  tie-break order (id ascending).
- The weights are identical and documented in one place: title 5, tags 4, features 3,
  path 2, framework 1; stopwords `{with, from, this, that, template, example, starter}`.

## Consequences

**Positive.** The browser can rank locally without a round trip, and a divergence is
caught by a test instead of by a user noticing a different order. The fixture doubles as
executable documentation of the scoring rules.

**Negative.** Two implementations must be maintained. The fixture only covers the cases
someone thought to write; a change in Python that no case exercises will not be caught.
Regenerating the fixture is a manual step, and the reviewer must confirm that the *Python*
behaviour is the intended one before regenerating — otherwise the test simply blesses a
regression.

**Rejected alternatives.**

- *Server-side ranking only.* Adds latency and a network dependency to a local sort.
- *A WASM build of the Python function.* Far more machinery than a 60-line scoring
  function justifies, and it would make the web bundle depend on a Python toolchain.
