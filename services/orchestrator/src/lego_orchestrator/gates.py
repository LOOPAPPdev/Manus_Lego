"""Quality gate evaluation (G0-G6).

A gate is ``pass`` only when the evaluator can name the artifact that proves it.
Anything that cannot be checked in this environment is ``not_evaluated``; a gate
that is missing a human authorization is ``blocked``, which is a distinct and
honest state from a failure.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import jsonschema

from . import catalog_engine, security, traceability
from .config import ConfigBundle, ConfigError, load_configuration
from .evidence import utc_now, write_json, write_text
from .paths import RepoPaths

GateStatus = Literal["pass", "fail", "blocked", "not_evaluated"]
GATE_ORDER = ("G0", "G1", "G2", "G3", "G4", "G5", "G6")

REQUIREMENT_IDS_BY_GATE: dict[str, tuple[str, ...]] = {
    "G0": ("REQ-PO-001", "REQ-PO-002", "REQ-PO-003"),
    "G1": ("REQ-PS-002", "REQ-PW-002"),
    "G2": ("REQ-PW-001", "REQ-PO-004"),
    "G3": ("REQ-PS-001", "REQ-PW-003", "REQ-RV-003"),
    "G4": ("REQ-PW-004",),
    "G5": ("REQ-PW-005", "REQ-PW-006", "REQ-RV-001"),
    "G6": ("REQ-PS-003", "REQ-PO-005"),
}


@dataclass(slots=True)
class GateResult:
    id: str
    name: str
    status: GateStatus
    detail: str
    evidence: list[str] = field(default_factory=list)
    requirement_ids: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "evidence": self.evidence,
            "requirement_ids": self.requirement_ids,
        }


@dataclass(slots=True)
class GateReport:
    generated_at: str
    commit: str
    environment: str
    gates: list[GateResult]

    @property
    def overall(self) -> GateStatus:
        statuses = {gate.status for gate in self.gates}
        if "fail" in statuses:
            return "fail"
        if "blocked" in statuses:
            return "blocked"
        if "not_evaluated" in statuses:
            return "not_evaluated"
        return "pass"

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "generated_at": self.generated_at,
            "commit": self.commit,
            "environment": self.environment,
            "overall": self.overall,
            "gates": [gate.as_dict() for gate in self.gates],
        }


def _summarise_junit(path: Path) -> tuple[int, int, int, bool]:
    """Return (total, passed, failed, present)."""

    outcomes = traceability.parse_junit(path, path.parent)
    if not outcomes:
        return 0, 0, 0, path.is_file()
    passed = sum(1 for outcome in outcomes if outcome.outcome == "passed")
    failed = sum(1 for outcome in outcomes if outcome.outcome in {"failed", "error"})
    return len(outcomes), passed, failed, True


def _gate_g0(paths: RepoPaths, bundle: ConfigBundle) -> GateResult:
    evidence: list[str] = []
    problems: list[str] = []

    if not paths.requirements.is_file():
        problems.append("docs/specifications/requirements.md is missing")
    else:
        evidence.append("docs/specifications/requirements.md")

    try:
        file = traceability.load_requirements(paths)
        evidence.append("docs/specifications/traceability.yaml")
        practices = {requirement.practice for requirement in file.requirements}
        missing_practices = {"PO", "PS", "PW", "RV"} - practices
        if missing_practices:
            problems.append(f"no requirement mapped to practices: {sorted(missing_practices)}")
        without_acceptance = [r.id for r in file.requirements if not r.acceptance]
        if without_acceptance:
            problems.append(f"requirements without acceptance criteria: {without_acceptance}")
        if len(file.requirements) < 10:
            problems.append(f"only {len(file.requirements)} requirements declared; the specification is incomplete")
    except (FileNotFoundError, ValueError) as exc:
        problems.append(str(exc))

    if bundle.problems:
        problems.append(f"{len(bundle.problems)} configuration problem(s)")

    return GateResult(
        id="G0",
        name="Specification and boundaries approved",
        status="fail" if problems else "pass",
        detail="; ".join(problems)
        if problems
        else f"{len(traceability.load_requirements(paths).requirements)} requirements with acceptance criteria",
        evidence=evidence,
        requirement_ids=list(REQUIREMENT_IDS_BY_GATE["G0"]),
    )


def _gate_g1(paths: RepoPaths) -> GateResult:
    evidence: list[str] = []
    problems: list[str] = []

    try:
        verdict = catalog_engine.validate_catalog(paths)
        evidence.append("catalog/index.json")
        if not verdict.get("valid"):
            issues = verdict.get("issues", [])
            problems.append(f"catalog validation failed with {len(issues)} issue(s): {issues[:3]}")
        index = catalog_engine.load_index(paths)
        templates = index.get("templates", [])
        if not templates:
            problems.append("catalog index contains no templates")
        unpinned_claims = [
            item["id"]
            for item in templates
            if item.get("status") in {"enriched", "reference_only"} and not item.get("commit")
        ]
        if unpinned_claims:
            problems.append(f"{len(unpinned_claims)} enriched record(s) without a pinned commit")
        if not paths.catalog_sources.is_file():
            problems.append("catalog/sources.json is missing")
        else:
            evidence.append("catalog/sources.json")
    except (catalog_engine.EngineError, json.JSONDecodeError) as exc:
        problems.append(str(exc))

    return GateResult(
        id="G1",
        name="Source, commit, license and provenance verified",
        status="fail" if problems else "pass",
        detail="; ".join(problems) if problems else "catalog provenance validation passed",
        evidence=evidence,
        requirement_ids=list(REQUIREMENT_IDS_BY_GATE["G1"]),
    )


def _gate_g2(paths: RepoPaths) -> GateResult:
    evidence: list[str] = []
    problems: list[str] = []

    schema_path = paths.template_schema
    if not schema_path.is_file():
        problems.append("schemas/template.schema.json is missing")
    else:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        manifests = catalog_engine.manifest_paths(paths)
        if not manifests:
            problems.append("no template manifests found")
        invalid: list[str] = []
        for manifest_path in manifests:
            try:
                document = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                invalid.append(f"{manifest_path.name}: invalid JSON")
                continue
            errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
            if errors:
                invalid.append(f"{manifest_path.name}: {errors[0].message}")
        if invalid:
            problems.append(f"{len(invalid)} manifest(s) violate the published schema: {invalid[:3]}")
        else:
            evidence.append("schemas/template.schema.json")

    decisions = sorted((paths.root / "docs" / "decisions").glob("*.md"))
    if len(decisions) < 3:
        problems.append("fewer than three architecture decision records")
    else:
        evidence.append("docs/decisions")

    if not (paths.root / "packages" / "schemas" / "src").is_dir():
        problems.append("shared TypeScript contracts (packages/schemas) are missing")

    return GateResult(
        id="G2",
        name="Runtime, dependency and platform compatibility checked",
        status="fail" if problems else "pass",
        detail="; ".join(problems) if problems else "contracts and decisions are consistent with the catalog",
        evidence=evidence,
        requirement_ids=list(REQUIREMENT_IDS_BY_GATE["G2"]),
    )


def _gate_g3(paths: RepoPaths, bundle: ConfigBundle) -> GateResult:
    evidence: list[str] = []
    problems: list[str] = []

    try:
        policy = bundle.security
        evidence.append("config/security.yaml")
        findings = security.scan_for_secrets(
            paths,
            [(pattern.name, pattern.regex) for pattern in policy.secrets.scan.patterns],
            policy.secrets.scan.allowlist_paths,
        )
        if findings:
            problems.append(
                "secret-like patterns found: "
                + ", ".join(f"{finding.path}:{finding.line} ({finding.pattern})" for finding in findings[:5])
            )
        else:
            evidence.append("security-scan:clean")
    except ConfigError as exc:
        problems.extend(exc.problems)

    agent_problems = [problem for problem in bundle.problems if "TEAMSCHEMA" in problem or "registry" in problem]
    if agent_problems:
        problems.append(f"{len(agent_problems)} agent permission problem(s)")
    else:
        evidence.append("config/TEAMSCHEMA.yaml")

    return GateResult(
        id="G3",
        name="Security review and minimal reuse approved",
        status="fail" if problems else "pass",
        detail="; ".join(problems) if problems else "no secrets detected; agent permissions within allowlist",
        evidence=evidence,
        requirement_ids=list(REQUIREMENT_IDS_BY_GATE["G3"]),
    )


def _gate_tests(
    gate_id: str, name: str, labels: tuple[str, ...], junit_paths: dict[str, Path], requirement_ids: tuple[str, ...]
) -> GateResult:
    missing = [label for label in labels if label not in junit_paths]
    if missing:
        return GateResult(
            id=gate_id,
            name=name,
            status="not_evaluated",
            detail=f"no JUnit report for: {', '.join(missing)}. Run the suite or pass --junit label=path.",
            evidence=[],
            requirement_ids=list(requirement_ids),
        )

    total = passed = failed = 0
    evidence: list[str] = []
    for label in labels:
        path = junit_paths[label]
        suite_total, suite_passed, suite_failed, present = _summarise_junit(path)
        if not present:
            return GateResult(
                id=gate_id,
                name=name,
                status="not_evaluated",
                detail=f"JUnit report missing for {label}: {path}",
                evidence=[],
                requirement_ids=list(requirement_ids),
            )
        total += suite_total
        passed += suite_passed
        failed += suite_failed
        evidence.append(path.as_posix())

    if total == 0:
        return GateResult(
            id=gate_id,
            name=name,
            status="fail",
            detail="JUnit reports contain no test cases",
            evidence=evidence,
            requirement_ids=list(requirement_ids),
        )

    return GateResult(
        id=gate_id,
        name=name,
        status="fail" if failed else "pass",
        detail=f"{passed}/{total} tests passing" + (f", {failed} failing" if failed else ""),
        evidence=evidence,
        requirement_ids=list(requirement_ids),
    )


def _gate_g5_docs(paths: RepoPaths) -> list[str]:
    problems: list[str] = []
    for relative in ("docs/architecture.mmd", "docs/security/threat-model.md", "docs/operations/runbook.md"):
        if not (paths.root / relative).is_file():
            problems.append(f"missing {relative}")
    return problems


def _gate_g6(paths: RepoPaths, commit: str) -> GateResult:
    approvals = sorted(paths.approvals_dir.glob("*.json")) if paths.approvals_dir.is_dir() else []
    for approval_path in approvals:
        try:
            record = json.loads(approval_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if record.get("commit") == commit and record.get("decision") == "approved":
            return GateResult(
                id="G6",
                name="Owner authorization for release and secrets",
                status="pass",
                detail=f"release approved by {record.get('approver', 'unknown')}",
                evidence=[approval_path.relative_to(paths.root).as_posix()],
                requirement_ids=list(REQUIREMENT_IDS_BY_GATE["G6"]),
            )

    return GateResult(
        id="G6",
        name="Owner authorization for release and secrets",
        status="blocked",
        detail=(
            "no recorded human approval for this commit; deployment and secret creation remain blocked "
            f"(write docs/evidence/approvals/<id>.json with commit={commit[:7]}… and decision=approved)"
        ),
        evidence=[],
        requirement_ids=list(REQUIREMENT_IDS_BY_GATE["G6"]),
    )


def evaluate(
    paths: RepoPaths,
    *,
    commit: str,
    environment: str = "local",
    junit_paths: dict[str, Path] | None = None,
) -> GateReport:
    """Evaluate every gate against the current repository state."""

    junit = junit_paths or {}
    bundle = load_configuration(paths)
    names = {gate.id: gate.name for gate in bundle.manus.gates} if bundle.manus else {}

    gates = [
        _gate_g0(paths, bundle),
        _gate_g1(paths),
        _gate_g2(paths),
        _gate_g3(paths, bundle),
        _gate_tests(
            "G4",
            names.get("G4", "Tests written and failing before implementation"),
            ("unit",),
            junit,
            REQUIREMENT_IDS_BY_GATE["G4"],
        ),
        _gate_tests(
            "G5",
            names.get("G5", "Integration, security scans and documentation verified"),
            ("integration", "security"),
            junit,
            REQUIREMENT_IDS_BY_GATE["G5"],
        ),
        _gate_g6(paths, commit),
    ]

    # G5 additionally requires the operational documents.
    g5 = gates[5]
    if g5.status == "pass":
        doc_problems = _gate_g5_docs(paths)
        if doc_problems:
            g5.status = "fail"
            g5.detail = f"{g5.detail}; " + "; ".join(doc_problems)
        else:
            g5.evidence.extend(["docs/architecture.mmd", "docs/security/threat-model.md", "docs/operations/runbook.md"])

    for gate in gates:
        if gate.id in names:
            gate.name = names[gate.id]

    return GateReport(generated_at=utc_now(), commit=commit, environment=environment, gates=gates)


def render_markdown(report: GateReport) -> str:
    lines = [
        "# Quality gate report",
        "",
        f"Generated: `{report.generated_at}` · Commit: `{report.commit}` · Environment: `{report.environment}`",
        f"Overall: **{report.overall}**",
        "",
        "| Gate | Name | Status | Detail |",
        "|---|---|---|---|",
    ]
    for gate in report.gates:
        lines.append(f"| {gate.id} | {gate.name} | **{gate.status}** | {gate.detail.replace('|', '/')} |")
    lines += [
        "",
        "## How to read this",
        "",
        "- `pass` — the artifact named in the evaluator was produced for this commit.",
        "- `not_evaluated` — the check could not run here (for example no JUnit report was supplied).",
        "- `blocked` — a human authorization is missing; this is not a failure of the code.",
        "- `fail` — a control is missing or broken and must be fixed before release.",
        "",
        "> Gates operationalise NIST SP 800-218 practices. They are evidence of implemented controls,",
        "> not a statement of certification or full conformance.",
        "",
    ]
    return "\n".join(lines)


def write_report(paths: RepoPaths, report: GateReport) -> dict[str, Any]:
    json_artifact = write_json(paths.gates_report, report.as_dict())
    markdown_artifact = write_text(paths.evidence_dir / "gates.md", render_markdown(report))
    return {"report": report.as_dict(), "json": json_artifact.as_dict(), "markdown": markdown_artifact.as_dict()}
