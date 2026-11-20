# lego-orchestrator

Deterministic orchestration service for Manus LEGO. It owns three things:

1. **Contracts** — typed validation of `config/manus.yaml`, `config/security.yaml`,
   `config/TEAMSCHEMA.yaml`, `config/sources.yaml` and `agents/registry.yaml`, including
   cross-file rules (tool allowlists, approval coverage, gate references).
2. **Governance** — gate evaluation (G0–G6) and requirement traceability from real
   artifacts, never from assertions in prose.
3. **CLI** — the `lego` command surface described in `docs/specifications/requirements.md`.

The catalog indexing engine itself is *not* reimplemented here. `catalog_engine.py`
loads `scripts/lego_catalog.py` as a module so there is exactly one implementation of
record for discovery, scoring and manifest validation (see ADR 0005).

## Usage

```bash
uv sync --project services/orchestrator
uv run --project services/orchestrator lego --help
uv run --project services/orchestrator pytest services/orchestrator/tests
uv run --project services/orchestrator ruff check services/orchestrator
```

## Design constraints

- Standard library first; `pydantic`, `PyYAML` and `jsonschema` are the only runtime
  dependencies.
- Every command is idempotent and read-only unless it explicitly writes a named artifact
  (`selection_plan.json`, `compose_plan.json`, `docs/evidence/*`).
- Fail closed: an unknown tool, an unreachable policy path or an unresolvable gate is an
  error, not a warning.
