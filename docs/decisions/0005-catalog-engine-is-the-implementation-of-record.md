# ADR 0005 — The existing catalog engine stays the implementation of record

- **Status:** accepted
- **Date:** 2026-11-20

## Context

`scripts/lego_catalog.py` is a 36 KB, stdlib-only program that already implements the hard
part of this project: discovering templates from GitHub trees, recording provenance,
validating manifests and producing a deterministic selection plan. It is covered by ten
`unittest` tests and has been used to build the 42 committed manifests.

The new orchestrator needs the same four operations (`index`, `search`, `plan`,
`validate`) plus governance around them (gates, evidence, traceability). Rewriting the
engine inside the orchestrator would be a rewrite of working, tested code — the opposite of
what this task asks for.

## Decision

The engine remains the **single implementation of record**. The orchestrator wraps it:

- `services/orchestrator/src/lego_orchestrator/catalog_engine.py` invokes it as a
  subprocess with a fixed argv (`[sys.executable, script, "--output", root, <command>]`)
  and parses its JSON stdout. No `shell=True`, no interpolation of user input into a shell.
- The engine's own tests keep running unchanged, and the orchestrator's tests exercise the
  adapter through the same public commands a contributor uses.
- Where the orchestrator needs richer semantics (blockers, licensing, inventory), it
  composes on top of the engine's output instead of forking it (`compose.py`).

The adapter also enforces the engine's contract: a missing or non-JSON stdout is an
`EngineError`, never an empty result. That distinction matters — "the engine failed" and
"the catalog is empty" must not look the same to a gate.

## Consequences

**Positive.** No behavioural regression in the discovery logic; one place to fix a
provenance bug; the stdlib-only property means the engine still runs in a bare container.

**Negative.** A subprocess boundary costs ~150 ms per call and makes partial failures
harder to debug (the adapter must surface stderr). Argument order is part of the contract:
`--output` is a global flag and must precede the subcommand — a mistake that this work
found and fixed, and that `tests/unit/test_catalog_and_composition.py` now guards.

**Rejected alternatives.**

- *Import the engine as a module.* Possible, but the engine's `main()` calls `sys.exit`
  and writes to stdout; a subprocess keeps that behaviour honest.
- *Reimplement in the orchestrator and delete the script.* Discards tested behaviour and
  breaks the `.claude/skills` workflows that call the script directly.
