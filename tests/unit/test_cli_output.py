"""`lego verify` must keep its JSON report on stdout even when it runs the suites.

REQ-PW-005 — the gate report is a machine-readable artifact. If the suites' own
output were inherited, a caller doing `lego verify --run-tests > report.json`
would get a file that no parser accepts, and the gate result would silently
become unreadable exactly when it matters.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from lego_orchestrator import cli


class _Completed:
    """Stand-in for `subprocess.CompletedProcess` with captured suite output."""

    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_run_pytest_suite_sends_suite_output_to_stderr(
    tmp_path: Path, monkeypatch: Any, capsys: Any
) -> None:
    """The suite's chatter is forwarded to stderr; stdout stays empty."""
    targets = tmp_path / "tests" / "unit"
    targets.mkdir(parents=True)

    def fake_run(*args: Any, **kwargs: Any) -> _Completed:
        assert kwargs["capture_output"] is True, "the suite output must be captured, not inherited"
        assert kwargs["text"] is True
        return _Completed(0, "36 passed in 1.19s\n", "warning: something\n")

    monkeypatch.setattr(subprocess, "run", fake_run)
    junit = tmp_path / "reports" / "junit" / "unit.xml"

    result = cli._run_pytest_suite(tmp_path, "unit", ["tests/unit"], junit)

    captured = capsys.readouterr()
    assert captured.out == "", "stdout is reserved for the JSON report"
    assert "36 passed" in captured.err
    assert "warning: something" in captured.err
    assert result["state"] == "passed"
    assert result["returncode"] == 0
    assert result["junit"] == junit.as_posix()


def test_run_pytest_suite_marks_failures_and_skips_absent_targets(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """A failing suite is reported as failed, and a missing target is skipped, not passed."""
    (tmp_path / "tests" / "unit").mkdir(parents=True)
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Completed(1, "1 failed\n", ""))

    failed = cli._run_pytest_suite(tmp_path, "unit", ["tests/unit"], tmp_path / "unit.xml")
    skipped = cli._run_pytest_suite(tmp_path, "integration", ["tests/integration"], tmp_path / "i.xml")

    assert failed["state"] == "failed"
    assert failed["returncode"] == 1
    assert skipped["state"] == "skipped"
    assert skipped["reason"] == "no test targets present"
