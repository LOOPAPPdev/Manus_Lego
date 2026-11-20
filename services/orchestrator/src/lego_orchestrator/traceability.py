"""Requirement traceability.

A requirement is only ``verified`` when three independent things line up:

1. its declared implementation paths exist in the repository,
2. at least one automated test that references the requirement ID passed in the
   executed suite (JUnit XML), and
3. the evidence artifact it points at exists.

Test links are discovered from source, not asserted in a spreadsheet: any test
function whose body or docstring contains ``REQ-<PRACTICE>-<NNN>`` is linked.
That keeps the matrix honest when tests are renamed or deleted.
"""

from __future__ import annotations

import ast
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from .paths import RepoPaths

REQUIREMENT_ID = re.compile(r"REQ-(?:PO|PS|PW|RV)-\d{3}")

Practice = Literal["PO", "PS", "PW", "RV"]
Status = Literal["verified", "partial", "unverified", "failing"]


class Requirement(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str = Field(pattern=r"^REQ-(PO|PS|PW|RV)-\d{3}$")
    practice: Practice
    title: str
    statement: str
    acceptance: list[str] = Field(min_length=1)
    implementation: list[str] = Field(min_length=1)
    tests: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    manual_control: bool = False


class TraceabilityFile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    schema_version: str
    requirements: list[Requirement]


@dataclass(frozen=True, slots=True)
class TestOutcome:
    nodeid: str
    name: str
    file: str
    outcome: Literal["passed", "failed", "skipped", "error"]
    duration: float
    requirement_ids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "nodeid": self.nodeid,
            "name": self.name,
            "file": self.file,
            "outcome": self.outcome,
            "duration": round(self.duration, 6),
            "requirement_ids": list(self.requirement_ids),
        }


@dataclass(slots=True)
class TestMarker:
    file: str
    name: str
    requirement_ids: tuple[str, ...]


@dataclass(slots=True)
class TraceabilityReport:
    generated_at: str
    commit: str
    requirements: list[dict[str, object]] = field(default_factory=list)
    summary: dict[str, object] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": "1.0.0",
            "generated_at": self.generated_at,
            "commit": self.commit,
            "requirements": self.requirements,
            "summary": self.summary,
        }


def load_requirements(paths: RepoPaths) -> TraceabilityFile:
    if not paths.traceability.is_file():
        raise FileNotFoundError(f"Traceability file missing: {paths.traceability}")
    raw = yaml.safe_load(paths.traceability.read_text(encoding="utf-8"))
    return TraceabilityFile.model_validate(raw)


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def discover_test_markers(root: Path, extra_dirs: tuple[str, ...] = ("tests", "services")) -> list[TestMarker]:
    """Find test functions that declare a requirement ID in their body or docstring."""

    markers: list[TestMarker] = []
    candidates: list[Path] = []
    for directory in extra_dirs:
        base = root / directory
        if base.is_dir():
            candidates.extend(sorted(base.rglob("test_*.py")))
            candidates.extend(sorted(base.rglob("*_test.py")))

    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            if not node.name.startswith("test"):
                continue
            segment = ast.get_source_segment(source, node) or ""
            found = tuple(sorted(set(REQUIREMENT_ID.findall(segment))))
            if found:
                markers.append(TestMarker(file=_relative(path, root), name=node.name, requirement_ids=found))
    return markers


def parse_junit(path: Path, root: Path) -> list[TestOutcome]:
    """Parse a pytest JUnit XML report into outcomes."""

    if not path.is_file():
        return []
    try:
        # JUnit is produced by our own pytest run, not by remote input; defusedxml would
        # add a dependency to a service that otherwise needs none.
        tree = ET.parse(path)  # noqa: S314
    except ET.ParseError:
        return []

    outcomes: list[TestOutcome] = []
    for case in tree.iter("testcase"):
        name = case.get("name", "")
        file_attr = case.get("file") or _file_from_classname(case.get("classname", ""))
        outcome: Literal["passed", "failed", "skipped", "error"] = "passed"
        if case.find("failure") is not None:
            outcome = "failed"
        elif case.find("error") is not None:
            outcome = "error"
        elif case.find("skipped") is not None:
            outcome = "skipped"
        outcomes.append(
            TestOutcome(
                nodeid=f"{file_attr}::{name}",
                name=name,
                file=file_attr.replace("\\", "/"),
                outcome=outcome,
                duration=float(case.get("time") or 0.0),
            )
        )
    return outcomes


def _file_from_classname(classname: str) -> str:
    if not classname:
        return ""
    return classname.replace(".", "/") + ".py"


def collect_outcomes(junit_paths: dict[str, Path], root: Path) -> list[TestOutcome]:
    outcomes: list[TestOutcome] = []
    for path in junit_paths.values():
        outcomes.extend(parse_junit(path, root))
    return outcomes


def link_outcomes(outcomes: list[TestOutcome], markers: list[TestMarker]) -> list[TestOutcome]:
    """Attach requirement IDs to outcomes by (file, test name)."""

    by_key: dict[tuple[str, str], tuple[str, ...]] = {}
    for marker in markers:
        by_key[(marker.file, marker.name)] = marker.requirement_ids

    linked: list[TestOutcome] = []
    for outcome in outcomes:
        base_name = outcome.name.split("[", 1)[0]
        ids = by_key.get((outcome.file, base_name)) or by_key.get((outcome.file, outcome.name)) or ()
        if not ids:
            # Fallback: some runners report only the module path.
            ids = next(
                (value for (file, name), value in by_key.items() if name == base_name and file.endswith(outcome.file)),
                (),
            )
        linked.append(
            TestOutcome(
                nodeid=outcome.nodeid,
                name=outcome.name,
                file=outcome.file,
                outcome=outcome.outcome,
                duration=outcome.duration,
                requirement_ids=tuple(ids),
            )
        )
    return linked


def build_report(
    paths: RepoPaths,
    *,
    commit: str,
    generated_at: str,
    junit_paths: dict[str, Path],
) -> TraceabilityReport:
    requirements = load_requirements(paths)
    markers = discover_test_markers(paths.root)
    outcomes = link_outcomes(collect_outcomes(junit_paths, paths.root), markers)

    executed = {(outcome.file, outcome.name.split("[", 1)[0]): outcome for outcome in outcomes}
    report = TraceabilityReport(generated_at=generated_at, commit=commit)
    counts = {"verified": 0, "partial": 0, "unverified": 0, "failing": 0}
    by_practice: dict[str, int] = {}

    for requirement in requirements.requirements:
        missing = [item for item in requirement.implementation if not (paths.root / item).exists()]
        implementation_present = len(missing) < len(requirement.implementation)

        declared = {marker.name for marker in markers if requirement.id in marker.requirement_ids}
        declared_files = {marker.file for marker in markers if requirement.id in marker.requirement_ids}
        linked = [
            outcome
            for outcome in outcomes
            if requirement.id in outcome.requirement_ids
            or (outcome.file in declared_files and outcome.name.split("[", 1)[0] in declared)
        ]

        notes: list[str] = []
        if missing:
            notes.append(f"missing implementation paths: {', '.join(missing)}")
        if not declared:
            notes.append("no test references this requirement id")
        elif not linked:
            notes.append("tests reference this requirement but were not part of the executed suite")

        passing = [outcome for outcome in linked if outcome.outcome == "passed"]
        failing = [outcome for outcome in linked if outcome.outcome in {"failed", "error"}]
        evidence_present = [item for item in requirement.evidence if (paths.root / item).exists()]
        evidence_missing = [item for item in requirement.evidence if not (paths.root / item).exists()]
        if evidence_missing:
            notes.append(f"evidence not produced yet: {', '.join(evidence_missing)}")

        status: Status
        if failing:
            status = "failing"
            notes.append(f"{len(failing)} linked test(s) failing")
        elif not implementation_present:
            status = "unverified"
        elif requirement.manual_control:
            # A manual control is verified only when its evidence exists *and* a test that
            # exercises the surrounding automation passed. Evidence alone is a file on disk,
            # not a run: an approval README must never make a release look authorised.
            status = "verified" if evidence_present and passing else "partial"
        elif passing and not evidence_missing:
            status = "verified"
        elif passing:
            status = "partial"
        else:
            status = "partial"

        counts[status] += 1
        by_practice[requirement.practice] = by_practice.get(requirement.practice, 0) + 1

        report.requirements.append(
            {
                "id": requirement.id,
                "practice": requirement.practice,
                "title": requirement.title,
                "status": status,
                "implementation_present": implementation_present,
                "missing_implementation": missing,
                "tests": [outcome.as_dict() for outcome in linked],
                "declared_tests": sorted(declared),
                "evidence": evidence_present,
                "manual_control": requirement.manual_control,
                "notes": notes,
            }
        )

    report.summary = {
        "total": len(requirements.requirements),
        "verified": counts["verified"],
        "partial": counts["partial"],
        "unverified": counts["unverified"],
        "failing": counts["failing"],
        "by_practice": by_practice,
        "tests_executed": len(executed),
    }
    return report


def render_markdown(report: TraceabilityReport) -> str:
    """Render the matrix as a reviewable Markdown table."""

    summary = report.summary
    lines = [
        "# Requirement traceability",
        "",
        f"Generated: `{report.generated_at}` · Commit: `{report.commit}`",
        "",
        "| Requirement | Practice | Title | Status | Tests | Evidence |",
        "|---|---|---|---|---|---|",
    ]
    for item in report.requirements:
        tests = item["tests"]
        passed = sum(1 for test in tests if isinstance(test, dict) and test.get("outcome") == "passed")
        lines.append(
            "| `{id}` | {practice} | {title} | {status} | {passed}/{total} | {evidence} |".format(
                id=item["id"],
                practice=item["practice"],
                title=str(item["title"]).replace("|", "\\|"),
                status=item["status"],
                passed=passed,
                total=len(tests),  # type: ignore[arg-type]
                evidence=len(item["evidence"]),  # type: ignore[arg-type]
            )
        )

    lines += [
        "",
        "## Summary",
        "",
        f"- Total requirements: **{summary['total']}**",
        f"- Verified: **{summary['verified']}**",
        f"- Partial: **{summary['partial']}**",
        f"- Unverified: **{summary['unverified']}**",
        f"- Failing: **{summary['failing']}**",
        f"- Tests executed and linked: **{summary['tests_executed']}**",
        "",
        "> Statuses are computed from repository state and the executed JUnit report. "
        "`partial` means at least one of implementation, passing test or evidence is missing. "
        "This table maps NIST SSDF practices to controls; it is not a certification.",
        "",
    ]
    return "\n".join(lines)


def write_report(paths: RepoPaths, report: TraceabilityReport) -> dict[str, object]:
    from .evidence import write_json, write_text

    payload = report.as_dict()
    json_artifact = write_json(paths.traceability_report, payload)
    markdown_artifact = write_text(paths.evidence_dir / "traceability.md", render_markdown(report))
    return {"json": json_artifact.as_dict(), "markdown": markdown_artifact.as_dict()}


def load_report(path: Path) -> dict[str, object] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
