# ADR 0008 — Gates evaluate artifacts, and `blocked` is not `pass`

- **Status:** accepted
- **Date:** 2026-11-20

## Context

A gate that a human marks "done" is a claim. A gate that reads an artifact is evidence.
The difference matters most in the failure case: the dangerous outcome is not a red gate, it
is a green gate that was never actually evaluated.

## Decision

Seven gates (`G0`–`G6`) are evaluated by `lego verify` from files that exist in the
repository:

| Gate | Reads | Fails when |
|---|---|---|
| G0 | `docs/specifications/requirements.md`, `traceability.yaml`, configuration bundle | a requirement lacks acceptance criteria, a practice is unmapped, config is invalid |
| G1 | `catalog/index.json`, `catalog/sources.json` (through the engine) | provenance validation fails, or an enriched record has no pinned commit |
| G2 | `schemas/template.schema.json`, every manifest, `docs/decisions/*.md`, `packages/schemas/src` | a manifest violates the schema, fewer than three ADRs, no shared contracts |
| G3 | `config/security.yaml`, `config/TEAMSCHEMA.yaml`, tracked files | a credential pattern matches, an agent uses an undeclared tool, the orchestrator holds `repo_write` |
| G4 | JUnit XML for the `unit` label | a test fails, or no report was supplied |
| G5 | JUnit XML for `integration` + `security`, plus the architecture diagram, threat model and runbook | a test fails, a document is missing |
| G6 | `docs/evidence/approvals/*.json` | no approval matches the current commit |

Statuses are deliberately four-valued:

- `pass` — the artifact was produced for this commit.
- `fail` — a control is missing or broken.
- `not_evaluated` — the check could not run (no JUnit report, no network). **Never treated
  as a pass.**
- `blocked` — a human authorisation is missing. Not a code defect; the process is waiting.

`overall` is `fail` if any gate failed, else `blocked` if any gate is blocked, else `pass`
only when every gate passed. The CLI maps this to exit codes `0` / `1` / `3`, so a pipeline
can distinguish "broken" from "waiting for a human".

G6 is blocked by design in this repository: there is one human owner, so the approval must
be recorded as a file that names the commit, rather than requiring a second reviewer who
does not exist. `docs/evidence/approvals/README.md` documents the schema.

## Consequences

**Positive.** The gate report is reproducible from the commit alone; a reviewer can re-run
`lego verify` and get the same answer. Missing evidence degrades to `not_evaluated` instead
of a false green. The traceability report uses the same JUnit input, so a requirement cannot
be "verified" by a test that did not run.

**Negative.** Gates are only as good as their checks — G1 trusts the engine's validation,
and G3's secret scan is pattern-based, so a novel credential format will pass. Those limits
are listed in `docs/nist-mapping.md` rather than implied away. Writing evidence files is a
manual step today; CI runs `lego verify` and uploads the report, but does not commit it.

**Rejected alternatives.**

- *A single boolean "CI green".* Collapses "not run" into "passed".
- *Requiring two human approvals.* Impossible for a single-owner repository; it would make
  the gate permanently red and teach everyone to ignore it.
