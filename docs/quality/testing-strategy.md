# Testing strategy

## Principle

A test exists to make a claim falsifiable. Every requirement in
`docs/specifications/requirements.md` names at least one test that would fail if the control
disappeared; `lego report` links them by scanning test bodies for `REQ-…` markers. A
requirement whose test was deleted becomes `partial`, not silently green.

## Layers

| Layer | Location | Runtime | What it proves |
|---|---|---|---|
| Unit (Python) | `services/*/tests`, `tests/unit` | pytest | Configuration rules, gate evaluation, composition blockers, traceability linkage, secret scanning, catalog provenance |
| Unit (TypeScript) | `apps/*/src`, `packages/*/src` | vitest | Zod contracts against the real catalog, ranking parity with Python, API route behaviour via `app.inject`, UI formatting |
| Integration | `tests/integration` | pytest + subprocess | The built API over HTTP, and the `lego` CLI against a disposable copy of the repository |
| Security | `tests/security` | pytest | Workflow pinning, permissions, Dependabot coverage, container hardening |
| Evaluation | `tests/evaluations`, `services/rag/tests` | pytest | Retrieval quality (recall@k, MRR), ACL enforcement, injection flagging, refusal |

`lego verify --run-tests` runs the four pytest labels (`unit`, `integration`, `security`,
`evaluations`) into JUnit XML under `reports/junit/`, then evaluates the gates against those
files. The same XML feeds `lego report`, so gate G4/G5 and the traceability matrix cannot
disagree about what ran.

## Conventions

- Test names state the behaviour, not the method: `test_write_methods_are_refused`.
- The docstring starts with the requirement id and one sentence of intent.
- A test may assert on the *absence* of a capability (no `pull_request_target`, no
  `repo_write` for the orchestrator). Negative tests are first-class here.
- Fixtures that describe behaviour shared across languages live in `tests/fixtures/` and are
  generated from the Python implementation, never hand-written.
- `pytest.ini` sets `--strict-markers`; an unknown marker is an error, not a warning.

## What is not covered (honest gaps)

1. **The web app has no component tests.** `packages/ui` has formatting unit tests, and the
   SPA builds, but no test renders a page and asserts on the DOM. A regression in
   `CatalogPage` would ship. Adding React Testing Library is the obvious next step.
2. **No coverage threshold.** Coverage is not measured, so an untested branch is invisible
   rather than reported as a number.
3. **No fuzzing or property-based tests.** The zod and pydantic schemas are exercised with
   real data, not adversarial input.
4. **The retrieval evaluation is tiny.** Four questions over five documents. It catches a
   broken retriever, not a subtle ranking regression.
5. **No load tests.** The rate limiter and the mtime cache are tested for behaviour, not for
   throughput.
6. **No browser end-to-end tests.** The API integration suite uses HTTP directly.
7. **Container tests are static.** They read the Dockerfiles and compose file; no image is
   built or run in this environment.

Each gap is listed rather than hidden, because a testing strategy that claims full coverage
is the first thing a reviewer stops believing.

## Running

```bash
# Everything the gates read
uv run --project services/orchestrator lego verify --run-tests

# Just the Python suites
uv run --project services/orchestrator pytest tests services/orchestrator/tests -q
uv run --project services/rag pytest services/rag/tests -q

# TypeScript
pnpm exec turbo run test
```

A test that needs a built artifact (the API, `node`) skips with a message instead of
failing, and the skip is visible in the JUnit report.
