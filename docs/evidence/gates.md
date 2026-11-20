# Quality gate report

Generated: `2026-11-20T14:30:33Z` · Commit: `3baeeafc48abd199ed48c329c4da920748af36b4` · Environment: `local`
Overall: **blocked**

| Gate | Name | Status | Detail |
|---|---|---|---|
| G0 | Specification and boundaries approved | **pass** | 17 requirements with acceptance criteria |
| G1 | Source, commit, license and provenance verified | **pass** | catalog provenance validation passed |
| G2 | Runtime, dependency and platform compatibility checked | **pass** | contracts and decisions are consistent with the catalog |
| G3 | Security review and minimal reuse approved | **pass** | no secrets detected; agent permissions within allowlist |
| G4 | Tests written and failing before implementation | **pass** | 38/38 tests passing |
| G5 | Integration, security scans and documentation verified | **pass** | 39/39 tests passing |
| G6 | Owner authorization for release and secrets | **blocked** | no recorded human approval for this commit; deployment and secret creation remain blocked (write docs/evidence/approvals/<id>.json with commit=3baeeaf… and decision=approved) |

## How to read this

- `pass` — the artifact named in the evaluator was produced for this commit.
- `not_evaluated` — the check could not run here (for example no JUnit report was supplied).
- `blocked` — a human authorization is missing; this is not a failure of the code.
- `fail` — a control is missing or broken and must be fixed before release.

> Gates operationalise NIST SP 800-218 practices. They are evidence of implemented controls,
> not a statement of certification or full conformance.
