# ADR 0001 — Reconcile the two feature branches instead of picking one

- **Status:** accepted
- **Date:** 2026-11-20
- **Deciders:** orchestrator (owner), human owner (approval authority)

## Context

The repository had three relevant refs when this work started:

| Ref | Commit | Content |
|---|---|---|
| `main` | `63f9465` | A README that describes files which do not exist on that branch |
| `feat/manus-lego-catalog` | `b37c522` | The catalog engine, 42 manifests, schemas, tests, pipeline docs, agent skills |
| `feat/integrated-master-index` | `c07bc48` | The same catalog plus `reports/` (36 scout reports and a final report), `scripts/build_master_index.py`, a larger `master_index.csv` |

Both feature branches share the merge-base `63f9465`, but neither is an ancestor of the
other: the catalog files were copied rather than merged, so the two branches carry
duplicate files with identical content. `main` contains none of it.

## Decision

Create `feat/engineering-foundation` from `origin/feat/integrated-master-index` (the
content superset) and merge `origin/feat/manus-lego-catalog` into it with `--no-ff`,
resolving the two conflicting files in favour of the integrated branch:

- `catalog/master_index.csv` — the integrated version has more rows.
- `scripts/agenteorchsenior.py` — the integrated version is the newer revision.

The merge commit (`b85efee`) keeps both histories reachable, so `git log` still shows how
the catalog was built, and a future `git merge-base --is-ancestor` check can prove that no
work was dropped.

## Consequences

**Positive.** No branch is abandoned; the merge is auditable; `main` can fast-forward to a
tree that contains every artifact produced so far.

**Negative.** The repository now has one merge commit whose diff is mostly a no-op
(identical files merged cleanly), which slightly complicates `git log --first-parent`.
The duplicated history between the two feature branches remains — rewriting it would
have been a destructive operation on published refs.

**Rejected alternatives.**

- *Rebase one branch onto the other.* Rewrites published commits and destroys the
  provenance of the scout reports, which reference commit SHAs in their metadata.
- *Squash everything into `main`.* Loses the review trail and makes the catalog's history
  unrecoverable.
- *Reset `main` to the integrated branch.* A force-push to the default branch, which the
  policy forbids without a recorded human approval (see ADR 0008).
