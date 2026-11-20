# Manus LEGO — Engineering Requirements

**Status:** baseline for the engineering foundation. **Owner:** orchestrator.
**Traceability:** every requirement below has an entry in [`traceability.yaml`](traceability.yaml)
and is verified by `lego report`.

## Scope and method

These requirements describe the *engineering foundation* of Manus LEGO: the monorepo, the
contracts, the orchestration CLI, the retrieval service, the security controls and the evidence
that proves them. They are written in EARS form (`WHEN … THE SYSTEM SHALL …`) so each one has a
testable acceptance criterion.

The requirements are grouped by the four NIST SP 800-218 (SSDF) practices. The mapping is a
*design decision about which control implements which practice*; it is not a conformance claim.
See [`../nist-mapping.md`](../nist-mapping.md) for the evidence-per-practice view and its limits.

**Out of scope for this baseline:** production deployment of the web application, commercial
license review of third-party templates, and any claim that an external template is secure.

---

## PO — Prepare the organization

### REQ-PO-001 — Requirements carry acceptance criteria

**WHEN** a requirement is added to the specification, **THE SYSTEM SHALL** record an identifier,
a statement, and at least one acceptance criterion, and the identifier **SHALL** appear in
`docs/specifications/traceability.yaml`.

*Acceptance:* `lego config validate` and the G0 gate pass; every requirement in the matrix has a
non-empty `acceptance` list; a requirement without acceptance criteria fails G0.

### REQ-PO-002 — Authority, roles and separation of duties are declared

**WHEN** an agent acts on the repository, **THE SYSTEM SHALL** resolve its permissions from
`config/TEAMSCHEMA.yaml`, and the orchestrator **SHALL NOT** hold repository write access.

*Acceptance:* the agent registry matches the team schema by identifier and tool set; an agent
using a tool outside `tool_policy.catalog` fails validation; the independent auditor cannot hold
`repo_write`.

### REQ-PO-003 — Toolchains are reproducible

**WHEN** a build or test runs in CI, **THE SYSTEM SHALL** install from committed lockfiles
(`pnpm-lock.yaml`, `services/*/uv.lock`) with a pinned Node and Python runtime.

*Acceptance:* `pnpm install --frozen-lockfile` and `uv sync --frozen` succeed; the lockfiles are
tracked by Git; dependency lifecycle scripts are allowlisted explicitly.

### REQ-PO-004 — Build and release environments are defined as code

**WHEN** a service is deployed, **THE SYSTEM SHALL** use a container definition committed to
`infrastructure/`, built in multiple stages, running as a non-root user with pinned base images.

*Acceptance:* every Dockerfile has a digest-pinned or version-pinned base image, a non-root
`USER`, and a health check; the compose file declares read-only root filesystems.

### REQ-PO-005 — Release requires recorded human authorization

**WHEN** a change is proposed for production, **THE SYSTEM SHALL** require an approval record that
names the commit, the approver and the scope.

*Acceptance:* G6 is `blocked` until `docs/evidence/approvals/<id>.json` contains
`decision: approved` and the current commit SHA. A blocked gate never reports as a pass.

---

## PS — Protect the software

### REQ-PS-001 — Credentials never enter the repository

**WHEN** code, tests, fixtures or documentation are committed, **THE SYSTEM SHALL** contain no
credential material, and secrets **SHALL** be read from the environment or the platform secret
store at runtime.

*Acceptance:* the secret scan over tracked files reports zero findings; a planted credential
pattern is detected by the scanner's own test.

### REQ-PS-002 — Every external artifact is referenced with provenance

**WHEN** the catalog records an external template, **THE SYSTEM SHALL** record provider,
repository, commit (or an explicit `null` with a status that forbids reuse), path and license
posture.

*Acceptance:* catalog validation reports no record that claims completeness without a pinned
commit; every manifest satisfies `schemas/template.schema.json`; a record with an unpinned commit
cannot be composed for reuse.

### REQ-PS-003 — Release artifacts are integrity-checked

**WHEN** evidence or a release artifact is produced, **THE SYSTEM SHALL** publish a SHA-256 digest
and the commit it describes, and CI actions **SHALL** be pinned to immutable commit SHAs.

*Acceptance:* `docs/evidence/evidence-manifest.json` lists a digest per artifact; every `uses:`
reference in `.github/workflows` is a 40-character SHA; an unpinned action fails the security
suite.

---

## PW — Produce well-secured software

### REQ-PW-001 — Contracts are defined before implementation

**WHEN** a runtime boundary is introduced, **THE SYSTEM SHALL** publish a schema for it, and both
the TypeScript and Python sides **SHALL** validate against that contract.

*Acceptance:* `packages/schemas` and `schemas/template.schema.json` parse the committed catalog;
the Python gate G2 validates every manifest against the published JSON Schema.

### REQ-PW-002 — Reuse requires a pinned, reviewed component

**WHEN** a template is proposed for reuse, **THE SYSTEM SHALL** produce a composition plan that
lists every blocker (missing commit, unreviewed license, incomplete inventory) and **SHALL**
default to `blocked`.

*Acceptance:* `lego compose` returns exit code 3 and `status: blocked` while any candidate lacks a
pinned commit or a reviewed license; the plan lists no files to copy.

### REQ-PW-003 — Configuration and input fail closed

**WHEN** configuration is missing a required field or input violates a schema, **THE SYSTEM
SHALL** reject the operation instead of applying a default.

*Acceptance:* unknown configuration keys raise a validation error; the API returns `400` for an
out-of-range pagination parameter; an unknown classification is downgraded to `restricted`.

### REQ-PW-004 — Behaviour changes are covered by automated tests

**WHEN** a behaviour is implemented, **THE SYSTEM SHALL** include at least one automated test that
references the requirement identifier and passes in the executed suite.

*Acceptance:* `lego report` marks a requirement `partial` when no linked test ran, and `verified`
only when a linked test passed.

### REQ-PW-005 — Independent verification precedes merge

**WHEN** a pull request is opened, **THE SYSTEM SHALL** evaluate gates from produced artifacts and
**SHALL NOT** allow the implementing agent to approve its own work.

*Acceptance:* the gate report records per-gate status with an evidence path; a missing JUnit report
yields `not_evaluated`, never `pass`; the auditor role cannot hold `repo_write`.

### REQ-PW-006 — Secure defaults in services and containers

**WHEN** the API or a container starts, **THE SYSTEM SHALL** run with least privilege: read-only
routes, security headers, a request rate limit, non-root user and no privilege escalation.

*Acceptance:* the API rejects write methods; hardening headers are present on every response; the
rate limiter returns `429` with `Retry-After`; the container definitions set `no-new-privileges`
and a read-only root filesystem.

---

## RV — Respond to vulnerabilities

### REQ-RV-001 — Continuous dependency and static analysis

**WHEN** a dependency or source file changes, **THE SYSTEM SHALL** run dependency review, static
analysis and container scanning, and **SHALL** keep the results as workflow artifacts.

*Acceptance:* `security.yml` runs on pull requests and on a schedule; results are uploaded as
artifacts; Dependabot covers npm, uv, pip and GitHub Actions.

### REQ-RV-002 — Vulnerability intake and remediation are recorded

**WHEN** a vulnerability is reported, **THE SYSTEM SHALL** record severity, affected component,
decision and remediation commit in the operations runbook's register.

*Acceptance:* the runbook contains a triage table and remediation SLAs; the process names the
person accountable for the decision.

### REQ-RV-003 — Secret exposure is detected and handled

**WHEN** a credential pattern appears in a tracked file or in retrieved content, **THE SYSTEM
SHALL** report it, refuse to continue the affected operation, and record the finding.

*Acceptance:* the scanner detects planted patterns; a retrieved document containing instruction
overrides is flagged in the answer's `guardrail_flags` without being obeyed.

---

## Non-functional requirements

| Area | Requirement | Acceptance |
|---|---|---|
| Determinism | The same commit produces the same gate and traceability results | Two consecutive `lego report` runs produce identical digests for the same JUnit input |
| Performance | Catalog listing responds within 200 ms for 1 000 records in-memory | API test asserts a page query under the budget |
| Portability | Python services run on CPython 3.12 with SQLite FTS5 | CI matrix runs 3.12; a build without FTS5 fails with an actionable error |
| Honesty | Reports never upgrade an unverified state | `enriched` is never rendered as "verified"; absent evidence renders as `not_evaluated` |
