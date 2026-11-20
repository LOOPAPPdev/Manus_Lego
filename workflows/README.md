# Workflows

Executable entry points for the deterministic pipeline. Each file is runnable on its
own; none of them requires the Manus UI.

| Workflow | Gate | Purpose | Writes |
|---|---|---|---|
| `discover.py` | G0–G1 | List allowlisted sources, trust and coverage | nothing |
| `retrieve.py` | — | Answer a question from a corpus with citations or refuse | nothing (unless `--store`) |
| `execute.py` | G0–G6 | Run spec → discover → select → compose → verify → report | `catalog/compose_plan.json`, `docs/evidence/*` |
| `verify.py` | G4–G5 | Evaluate gates from JUnit reports | `docs/evidence/gates.{json,md}` |

## Environment

Python workflows need their service environment. Run them through `uv`:

```bash
uv sync --project services/orchestrator
uv run --project services/orchestrator python workflows/execute.py "react authentication database"
uv run --project services/rag python workflows/retrieve.py "which template has D1 sessions" \
  --corpus services/rag/tests/fixtures/corpus
```

A plain `python3 workflows/verify.py` fails fast with an actionable message rather than a
traceback, because the workflow refuses to run with missing dependencies.

## Why separate files

Each workflow maps to a gate, so a failure points at a stage. The logic lives in
`services/orchestrator` and `services/rag`; these files are thin, reviewable entry points
that keep CI and local runs identical.
