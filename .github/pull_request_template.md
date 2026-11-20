## What changed

<!-- One paragraph. Link the requirement ids this change implements. -->

Requirements: `REQ-…`

## Why

<!-- The problem, not the patch. If it is a bug, say how it was found. -->

## Evidence

Paste the relevant lines from `docs/evidence/gates.json` (or the job summary) — not a
screenshot of a green check.

| Gate | Status | Detail |
|---|---|---|
| G0 |  |  |
| G1 |  |  |
| G2 |  |  |
| G3 |  |  |
| G4 |  |  |
| G5 |  |  |
| G6 |  |  |

```
$ uv run --project services/orchestrator lego verify --run-tests
$ pnpm exec turbo run lint typecheck build test
```

## Checklist

- [ ] Every new behaviour has a test that names the requirement it verifies
- [ ] `lego report` shows no requirement that regressed from `verified` to `partial`
- [ ] No credential, token or tenant document is included in the diff
- [ ] New external dependencies are justified in an ADR or in the PR body
- [ ] Documentation updated (`docs/`, `README.md`) where behaviour is user-visible
- [ ] If this touches `catalog/`, the provenance (commit, path, license) is recorded

## Honest limits

<!-- What this change does NOT cover. "Nothing" is rarely true. -->

## Risk and rollback

<!-- Blast radius, and how to undo it. -->
