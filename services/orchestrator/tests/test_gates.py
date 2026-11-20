"""Gate evaluation.

The point of these tests is the negative space: a gate that could not run must not look
like a gate that passed, and a blocked gate must not fail the build.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from lego_orchestrator import gates
from lego_orchestrator.paths import RepoPaths

ROOT = Path(__file__).resolve().parents[3]

PASSING_JUNIT = """<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1" failures="0" errors="0">
    <testcase classname="tests.unit.test_example" name="test_ok" time="0.01"/>
  </testsuite>
</testsuites>
"""

FAILING_JUNIT = """<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" tests="1" failures="1" errors="0">
    <testcase classname="tests.unit.test_example" name="test_broken" time="0.01">
      <failure message="assert False">assert False</failure>
    </testcase>
  </testsuite>
</testsuites>
"""


@pytest.fixture(scope="module")
def paths() -> RepoPaths:
    return RepoPaths(root=ROOT)


def test_missing_junit_is_not_evaluated(paths: RepoPaths) -> None:
    """REQ-PW-005 — no report means the gate did not run, which is not a pass."""
    report = gates.evaluate(paths, commit="0" * 40, junit_paths={})
    by_id = {gate.id: gate for gate in report.gates}

    assert by_id["G4"].status == "not_evaluated"
    assert by_id["G5"].status == "not_evaluated"
    assert "JUnit" in by_id["G4"].detail
    assert report.overall != "pass", "an unevaluated gate must not yield an overall pass"


def test_blocked_gate_is_reported_as_blocked(paths: RepoPaths) -> None:
    """REQ-PO-005 — without an approval for this commit, G6 is blocked, not failed."""
    report = gates.evaluate(paths, commit="deadbeef" * 5, junit_paths={})
    g6 = next(gate for gate in report.gates if gate.id == "G6")

    assert g6.status == "blocked"
    assert "approval" in g6.detail
    assert report.overall in {"blocked", "fail"}


def test_failing_junit_fails_the_gate(paths: RepoPaths, tmp_path: Path) -> None:
    """REQ-PW-005 — a failing test is a failing gate."""
    junit = tmp_path / "unit.xml"
    junit.write_text(FAILING_JUNIT, encoding="utf-8")

    report = gates.evaluate(paths, commit="a" * 40, junit_paths={"unit": junit})
    g4 = next(gate for gate in report.gates if gate.id == "G4")

    assert g4.status == "fail"
    assert "1 failing" in g4.detail
    assert report.overall == "fail"


def test_passing_junit_passes_the_gate(paths: RepoPaths, tmp_path: Path) -> None:
    """REQ-PW-004 — the happy path: a report with no failures passes."""
    junit = tmp_path / "unit.xml"
    junit.write_text(PASSING_JUNIT, encoding="utf-8")

    report = gates.evaluate(paths, commit="b" * 40, junit_paths={"unit": junit})
    g4 = next(gate for gate in report.gates if gate.id == "G4")

    assert g4.status == "pass"
    assert "1/1" in g4.detail


def test_every_gate_declares_requirements_and_a_detail(paths: RepoPaths) -> None:
    """REQ-PO-001 — a gate with no requirement and no explanation is unauditable."""
    report = gates.evaluate(paths, commit="c" * 40, junit_paths={})

    assert [gate.id for gate in report.gates] == list(gates.GATE_ORDER)
    for gate in report.gates:
        assert gate.requirement_ids, f"{gate.id} maps to no requirement"
        assert gate.detail, f"{gate.id} has no detail"
        assert gate.status in {"pass", "fail", "blocked", "not_evaluated"}
