# Release approvals

Gate **G6** is `blocked` until an approval record in this directory names the commit being
released. This replaces a second human reviewer, which a single-owner repository does not
have — the control is a written, commit-scoped authorisation, not a rubber stamp.

## Format

One JSON file per approval: `<yyyy-mm-dd>-<commit7>.json`.

```json
{
  "id": "2026-11-20-a1b2c3d",
  "commit": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
  "approver": "leonardo.batista",
  "scope": ["release:api", "release:web"],
  "decision": "approved",
  "decided_at": "2026-11-20T14:05:00Z",
  "expires_at": "2026-12-04T00:00:00Z",
  "evidence_reviewed": [
    "docs/evidence/gates.json",
    "docs/evidence/traceability.json",
    "docs/evidence/evidence-manifest.json"
  ],
  "notes": "G0-G5 green at this commit; G6 is this record."
}
```

Rules the gate enforces:

1. `commit` must equal the full SHA of `HEAD` at evaluation time. A short SHA does not match.
2. `decision` must be exactly `approved`. `rejected` and `pending` leave the gate blocked.
3. The record is never edited after the fact. A new commit needs a new record; an expired
   record needs a new record.

## What this does not do

- It does not verify that the approver is a human — it is a file. The control is that the
  *only* way to produce it is a deliberate act by someone with write access, and that it is
  reviewed in the pull request diff.
- It does not expire automatically; `expires_at` is documentation for the operator.

No approval file is committed for this branch: G6 is intentionally `blocked`, because a
release has not been authorised. That is the correct state, and reporting it as a pass would
defeat the gate.
