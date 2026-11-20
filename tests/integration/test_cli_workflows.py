"""End-to-end behaviour of the `lego` CLI on a disposable copy of the repository.

The tests run the CLI in a subprocess with `LEGO_REPO_ROOT` pointed at a temporary
clone of the tracked content, so a failing assertion cannot leave artifacts in the
working tree and `verify` never re-enters this suite.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COPIED = (
    ".gitignore",
    "agents",
    "catalog",
    "config",
    "docs",
    "packages",
    "schemas",
    "scripts",
    "workflows",
)

pytestmark = pytest.mark.integration


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    repository = tmp_path / "repo"
    repository.mkdir()
    for entry in COPIED:
        source = ROOT / entry
        if source.is_dir():
            shutil.copytree(
                source,
                repository / entry,
                ignore=shutil.ignore_patterns("node_modules", ".venv", "dist", "__pycache__"),
            )
        elif source.is_file():
            shutil.copy2(source, repository / entry)
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repository, check=True)
    return repository


def _lego(repository: Path, *args: str) -> subprocess.CompletedProcess[str]:
    script = (
        "import sys;"
        "from lego_orchestrator.cli import main;"
        "sys.exit(main(sys.argv[1:]))"
    )
    env = {**os.environ, "LEGO_REPO_ROOT": str(repository), "PYTHONWARNINGS": "ignore"}
    return subprocess.run(
        [sys.executable, "-c", script, *args],
        cwd=repository,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_config_validate_accepts_the_committed_configuration(sandbox: Path) -> None:
    """REQ-PO-002 — the configuration loads and its cross-file rules hold."""
    completed = _lego(sandbox, "config", "validate")

    assert completed.returncode == 0, completed.stderr or completed.stdout
    payload = json.loads(completed.stdout)
    assert payload["valid"] is True
    assert payload["problems"] == []
    assert len(payload["checked"]) == 5


def test_verify_without_evidence_reports_gaps_not_passes(sandbox: Path) -> None:
    """REQ-PW-005 — gates evaluate produced artifacts; missing evidence is never a pass."""
    completed = _lego(sandbox, "verify")

    assert completed.returncode == 3, completed.stderr or completed.stdout
    payload = json.loads(completed.stdout)
    statuses = {gate["id"]: gate["status"] for gate in payload["gates"]}

    assert statuses["G0"] == "pass"
    assert statuses["G1"] == "pass"
    assert statuses["G2"] == "pass"
    assert statuses["G3"] == "pass"
    assert statuses["G4"] == "not_evaluated"
    assert statuses["G5"] == "not_evaluated"
    assert statuses["G6"] == "blocked"
    assert payload["overall"] == "blocked"

    report = json.loads((sandbox / "docs/evidence/gates.json").read_text(encoding="utf-8"))
    assert report["commit"] == payload["commit"]
    for gate in report["gates"]:
        assert "detail" in gate


def test_select_and_compose_never_authorise_reuse(sandbox: Path) -> None:
    """REQ-PW-002 — composition is a proposal with explicit blockers, never an approval."""
    selected = _lego(sandbox, "select", "workers api template", "--limit", "3")
    assert selected.returncode == 0, selected.stderr
    plan_path = sandbox / "catalog/selection_plan.json"
    assert plan_path.is_file()

    composed = _lego(sandbox, "compose", "workers api template", "--limit", "3")
    assert composed.returncode in {0, 3}, composed.stderr

    plan = json.loads((sandbox / "catalog/compose_plan.json").read_text(encoding="utf-8"))
    assert plan["status"] in {"blocked", "ready_for_review"}
    assert plan["status"] != "approved"
    for candidate in plan["candidates"]:
        assert candidate["reuse_scope"]["copy"] == []
        if candidate["decision"] == "blocked":
            assert candidate["blockers"]


def test_report_marks_requirements_partial_without_junit(sandbox: Path) -> None:
    """REQ-PW-004 — without a test report nothing can be called verified."""
    completed = _lego(sandbox, "report")

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    summary = payload["summary"]

    assert summary["total"] >= 10
    assert summary["verified"] == 0, "no test ran, so nothing may be verified"
    assert summary["partial"] + summary["unverified"] >= 10

    manifest = json.loads((sandbox / "docs/evidence/evidence-manifest.json").read_text(encoding="utf-8"))
    assert manifest["artifact_count"] >= 1, "the manifest must describe the artifacts it hashes"
    assert all(len(artifact["sha256"]) == 64 for artifact in manifest["artifacts"])


def test_unknown_command_is_a_usage_error(sandbox: Path) -> None:
    """REQ-PW-003 — the CLI rejects unknown input instead of guessing."""
    completed = _lego(sandbox, "frobnicate")

    assert completed.returncode == 2
