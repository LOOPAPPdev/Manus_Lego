---
title: Release and approval process
classification: internal
tenants: public
tags: release, approval, gates
---
# Release and approval process

A release requires a green gate report and a recorded human approval. The approval
is written to `docs/evidence/approvals` and names the commit it authorizes.

## Sequence

The engineering agent opens a pull request. The quality auditor runs `lego verify`
and attaches the evidence. The owner approves the merge, and only then may a
deployment job run.

## Stop conditions

The pipeline stops when a gate fails, when evidence is missing for the reported
commit, or when a secret is detected in a tracked file. A blocked gate is never
bypassed by re-running the job.
