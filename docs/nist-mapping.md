# NIST mapping — what is implemented, what is not

**This document is not a certification, an assessment or a claim of conformance.** It maps
the controls in this repository to practices from the documents the specification named, so
a reader can check each one against the evidence that exists. Nothing here has been reviewed
by an assessor.

Reference documents: NIST SP 800-218 (SSDF 1.1), SP 800-160v1r1, SP 800-204D, SP 800-218A,
the AI Risk Management Framework (AI 100-1), and SP 800-190.

## 1. SSDF practice coverage

| SSDF practice | Implemented control | Evidence in this repository | Coverage |
|---|---|---|---|
| PO.1 — Define security requirements | 17 EARS-style requirements with acceptance criteria, mapped to implementation and tests | `docs/specifications/requirements.md`, `traceability.yaml`, gate G0 | **Full** for this codebase |
| PO.2 — Implement roles and responsibilities | Six agent contracts, a registry, a tool allowlist, separation of duties (the orchestrator cannot write code; the auditor cannot implement) | `config/TEAMSCHEMA.yaml`, `agents/registry.yaml`, `agents/*/AGENT.md`, G3 | **Full** |
| PO.3 — Implement supporting toolchains | pnpm + Turborepo, uv per service, committed lockfiles, pinned runtimes | `package.json`, `pnpm-lock.yaml`, `services/*/uv.lock`, `turbo.json` | **Full** |
| PO.4 — Define and use criteria for software security checks | Seven gates, each reading a named artifact, with four-valued status | `services/orchestrator/src/lego_orchestrator/gates.py`, `docs/evidence/gates.json` | **Full** |
| PO.5 — Implement and maintain secure environments | Multi-stage, digest-pinned, non-root images; read-only rootfs; dropped capabilities | `infrastructure/docker/*`, `tests/security/test_containers.py` | **Partial** — no signed images, no admission policy |
| PS.1 — Protect all forms of code from unauthorised access | Secret scan, `.env` ignored, secrets from environment, log redaction | `config/security.yaml`, `security.py`, `packages/shared/src/logger.ts`, G3 | **Partial** — Git history is not scanned |
| PS.2 — Provide a mechanism for verifying software release integrity | SHA-256 digest per artifact, commit recorded, actions pinned by SHA, SBOM + provenance in the release workflow | `docs/evidence/evidence-manifest.json`, `tests/security/test_workflows.py`, `release.yml` | **Partial** — the release workflow exists but has never run against a registry |
| PS.3 — Archive and protect each release | Evidence artifacts are committed under `docs/evidence/` | `docs/evidence/` | **Partial** — no long-term archive, no retention policy |
| PW.1 — Design software to meet security requirements | Threat model, ADRs, contracts-first schemas | `docs/security/threat-model.md`, `docs/decisions/`, `packages/schemas` | **Full** |
| PW.2 — Review the software design | ADRs record alternatives and consequences; the auditor role is separate from implementation | `docs/decisions/0001`–`0008`, `agents/quality-auditor/AGENT.md` | **Partial** — one human, so design review is self-review with a written record |
| PW.4 — Reuse existing, well-secured software | Catalog with provenance, license posture and inventory; composition defaults to `blocked` | `catalog/`, `compose.py`, G1, `tests/unit/test_catalog_and_composition.py` | **Full** for the *process*; no template's code has been audited |
| PW.5 — Create source code following secure coding practices | Read-only API, fail-closed config, input validation, no `shell=True`, no path traversal from user input | `apps/api/src/server.ts`, `config.py`, `catalog_engine.py` | **Partial** — no formal secure-coding checklist per change |
| PW.6 — Configure compilation, build and CI securely | Minimal workflow permissions, no `pull_request_target`, SHA-pinned actions, frozen lockfiles | `.github/workflows/*`, `tests/security/test_workflows.py` | **Full** |
| PW.7 — Review and/or analyse code | CodeQL, dependency review, ruff (with `S` rules), eslint + typescript-eslint | `security.yml`, `services/*/pyproject.toml`, `eslint.config.js` | **Partial** — no human code review by a second engineer |
| PW.8 — Test executable code | 100+ automated tests across TS and Python, plus retrieval evaluation | `tests/`, `apps/*/`, `packages/*/`, `services/*/tests` | **Partial** — no fuzzing, no coverage gate |
| PW.9 — Configure software to have secure settings by default | Read-only API, security headers, rate limit, non-root containers | `apps/api/src/server.ts`, `infrastructure/docker/compose.yaml` | **Full** |
| RV.1 — Identify and confirm vulnerabilities on an ongoing basis | CodeQL, Dependabot (npm, actions, uv), Trivy, scheduled scans | `.github/workflows/security.yml`, `.github/dependabot.yml` | **Partial** — no VEX, no runtime SBOM |
| RV.2 — Assess, prioritise and remediate vulnerabilities | Register with severities, SLAs and named decision maker | `docs/operations/runbook.md` §6 | **Full** as a process; two entries recorded |
| RV.3 — Analyse vulnerabilities to identify root causes | Each fix lands with a test that would have caught it | `tests/`, register entries VULN-0001/0002 | **Partial** — no formal RCA template |

## 2. SP 800-204D (software supply chain)

Implemented: locked dependencies, pinned CI actions, SBOM generation and provenance
attestation in `release.yml`, an artifact manifest with digests, and a dependency-review
gate. **Not implemented:** image signing (cosign), an admission controller that rejects
unsigned images, and reproducible builds. The workflow is written to do the first two; it
has not been executed against a registry, so it is untested configuration.

## 3. SP 800-190 (container security)

Implemented and tested: digest-pinned bases, multi-stage builds, non-root users, health
checks, read-only root filesystems, `no-new-privileges`, `cap_drop: ALL`, no Docker socket,
no host networking. **Not implemented:** image scanning of *built* images in this sandbox,
runtime threat detection (Falco or similar), and secrets injection at runtime (the compose
file uses environment variables, which are visible to `docker inspect`).

## 4. AI RMF (AI 100-1) and SP 800-218A

The retrieval service is the only AI component. Mapped functions:

| Function | Control |
|---|---|
| Govern | The AI data policy in `config/security.yaml` (no PII in logs, embeddings treated as sensitive, no private corpora in Git) |
| Map | The corpus is synthetic and labelled; the threat model lists prompt injection as T1 |
| Measure | `lego-rag eval` reports recall@k, MRR and refusal rate per question; the guardrail suite asserts detection and refusal |
| Manage | Guardrail flags are surfaced with every answer; a flagged document is reported, not silently dropped |

**Not done:** no red-teaming beyond nine regex rules, no model card, no bias evaluation (the
system does not generate free-form text by default), and no independent assessment. The
evaluation numbers describe five synthetic documents, not a tenant corpus.

## 5. SP 800-160v1r1

Used as a design lens rather than a checklist: assets and trust boundaries are enumerated in
the threat model, security requirements are traced to implementation, and residual risk is
stated per threat. No formal system security plan exists.

## 6. What would be needed for a real conformance claim

1. An independent assessor and a defined assessment scope.
2. Coverage for the items marked *Partial* above, with evidence, not intentions.
3. A human second reviewer, or an explicit compensating control accepted by the owner.
4. Executed release and container-signing pipelines, with the resulting attestations
   archived.
5. Retention and archive policy for evidence artifacts.

Until then, the honest statement is: **the controls listed as *Full* are implemented and
tested in this repository; the rest are partial or absent.**
