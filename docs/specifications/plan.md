# Implementation plan

The strategy for this change was **dependency-first, then spec → plan → TDD → verify**, with
the orchestrator as owner. This document records the order and the reason for it, so a
reviewer can see why each artifact exists rather than reading the diff as a flat list.

## 0. Inspect before writing

| Question | Answer found |
|---|---|
| What is on `main`? | A README describing files that live on other branches |
| Which branches carry the real work? | `feat/manus-lego-catalog`, `feat/integrated-master-index` |
| Are they related? | Shared merge-base, no ancestor relationship, duplicated files |
| What already works? | The stdlib catalog engine, 42 manifests, 10 `unittest` tests, a PR-based refresh workflow |
| What must not be rewritten? | `scripts/lego_catalog.py`, the manifests, the `.claude/skills` contracts |

Outcome: [ADR 0001](../decisions/0001-reconcile-feature-branches.md) — merge, don't choose.

## 1. Dependency first

Nothing can be verified before the toolchain is pinned:

1. pnpm workspace + Turborepo task graph, Node and Python versions recorded in
   `config/manus.yaml` and enforced by `packageManager` / `.python-version`.
2. One `uv` project per Python service, each with a committed lockfile.
3. `pytest.ini` at the root so a single invocation can exercise both services without
   installing them into one environment.

Verification: `pnpm install --frozen-lockfile`, `uv sync --frozen` twice, and the pre-existing
engine tests still green (10/10) before any new code.

## 2. Specification

Written before the implementation it describes, because the gates read it:

- 17 requirements in EARS form, each with acceptance criteria, grouped by SSDF practice.
- `traceability.yaml` maps each requirement to implementation paths and evidence paths.
- Tests carry `REQ-…` markers; the report links them by scanning test bodies, so a deleted
  test degrades a requirement to `partial` instead of leaving a stale claim.

## 3. Contracts, then code

`packages/schemas` (zod) and `schemas/template.schema.json` were written first, then:

| Layer | Depends on | Verified by |
|---|---|---|
| `packages/shared` (ranking port, config, logger, evidence) | schemas | 14-case parity fixture generated from the Python engine |
| `apps/api` | schemas, shared | `app.inject` unit tests + HTTP integration tests against the built artifact |
| `apps/web` | schemas, shared, ui | build + typecheck (no component tests — stated gap) |
| `services/orchestrator` | config files, engine | unit tests for gates/config, integration tests for the CLI |
| `services/rag` | its own corpus | 29 tests, including ACL and injection cases |

## 4. TDD loop, with real defects found

The tests were written to fail, and several did — against the implementation, not the test:

1. **Engine adapter argument order.** `--output` is a global flag; passing it after the
   subcommand made every engine call exit 2 with empty stdout. Fixed in the adapter and
   guarded by `test_catalog_validation_reports_valid`.
2. **Stopword-only evidence.** The answerer counted "the/of/and" overlap as support for an
   answer. Fixed by requiring a content-term overlap, with a `STOPWORDS` set.
3. **Empty query returning noise.** An empty query scored every document by hash collision;
   fixed with an early return and a vector-similarity floor.
4. **Noisy credential pattern.** `cloudflare_token` matched any 40-character string followed
   by a dot, flagging vendored test fixtures. Tightened to require the variable name; recorded
   as VULN-0001 in the runbook.
5. **Manual controls marked verified by a file.** An approval README alone made a release
   requirement `verified`. Changed so a manual control also needs a passing test; recorded in
   the report notes rather than hidden.

## 5. Verification

```bash
pnpm exec turbo run lint typecheck build test          # 20 tasks
uv run --project services/orchestrator ruff check …
uv run --project services/rag ruff check …
python3 -m unittest discover -s tests -p "test_lego_catalog.py"   # engine, unchanged
uv run --project services/orchestrator lego verify --run-tests    # G0–G6
uv run --project services/orchestrator lego report                # traceability + manifest
```

Expected and observed: **G0–G5 pass, G6 blocked** (no human approval exists for this commit),
overall `blocked`, exit code 3. A blocked gate is a process state, not a defect; reporting it
as a pass would defeat the control.

## 6. Not done in this change

Production deployment, image signing verification, a shared rate-limit store, component tests
for the SPA, and a second human reviewer. Each is listed in
[`../quality/testing-strategy.md`](../quality/testing-strategy.md),
[`../nist-mapping.md`](../nist-mapping.md) or the README's limitations section.
