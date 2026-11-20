"""Requirement ↔ test linkage.

The report only claims `verified` when a test that names the requirement passed. That
makes the linkage itself a control: if a test disappears, the requirement degrades to
`partial` instead of keeping a stale green row.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from lego_orchestrator.paths import RepoPaths
from lego_orchestrator.traceability import (
    discover_test_markers,
    link_outcomes,
    load_requirements,
    parse_junit,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def markers() -> list:
    return discover_test_markers(ROOT)


def test_every_requirement_has_a_linked_test(markers: list) -> None:
    """REQ-PW-004 — each requirement is exercised by at least one automated test."""
    file = load_requirements(RepoPaths(root=ROOT))
    linked = {requirement_id for marker in markers for requirement_id in marker.requirement_ids}
    missing = sorted(requirement.id for requirement in file.requirements if requirement.id not in linked)
    assert not missing, f"requirements without a linked test: {missing}"


def test_markers_ignore_helper_functions(markers: list) -> None:
    """REQ-PW-004 — only test functions create a link, so helpers cannot fake coverage."""
    assert markers, "expected discovered markers"
    assert all(marker.name.startswith("test") for marker in markers)
    assert all(marker.requirement_ids for marker in markers)


def test_marker_discovery_requires_the_identifier_in_the_test_body(tmp_path: Path) -> None:
    """REQ-PW-004 — a mention in a comment outside the test does not count."""
    module = tmp_path / "test_example.py"
    module.write_text(
        '"""Module docstring mentions REQ-PW-004 but is not a test."""\n'
        "\n"
        "def helper():\n"
        "    return 'REQ-PW-004'\n"
        "\n"
        "def test_without_marker():\n"
        "    assert True\n"
        "\n"
        "def test_with_marker():\n"
        '    """REQ-PW-004 — documented here."""\n'
        "    assert True\n",
        encoding="utf-8",
    )

    found = discover_test_markers(tmp_path, extra_dirs=(".",))

    assert [marker.name for marker in found] == ["test_with_marker"]
    assert found[0].requirement_ids == ("REQ-PW-004",)


def test_unlinked_outcomes_stay_unlinked(tmp_path: Path) -> None:
    """REQ-PW-004 — an outcome with no marker never claims a requirement."""
    junit = tmp_path / "junit.xml"
    junit.write_text(
        '<?xml version="1.0"?><testsuites><testsuite name="pytest" tests="1">'
        '<testcase classname="tests.unit.test_example" name="test_anonymous" time="0.01"/>'
        "</testsuite></testsuites>",
        encoding="utf-8",
    )

    outcomes = parse_junit(junit, tmp_path)
    linked = link_outcomes(outcomes, [])

    assert len(linked) == 1
    assert linked[0].outcome == "passed"
    assert linked[0].requirement_ids == ()
