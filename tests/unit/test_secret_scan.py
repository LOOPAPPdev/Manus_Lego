"""Credential hygiene.

The scanner is a control, not a guarantee: it covers tracked files with a fixed set of
patterns. These tests assert both directions — the real repository is clean, and the
scanner still detects a planted credential, so a green result means something.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from lego_orchestrator.config import load_configuration
from lego_orchestrator.paths import RepoPaths
from lego_orchestrator.security import scan_for_secrets

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def patterns() -> list[tuple[str, str]]:
    bundle = load_configuration(RepoPaths(root=ROOT))
    assert bundle.security is not None
    scan = bundle.security.secrets.scan
    assert scan.enabled
    return [(pattern.name, pattern.regex) for pattern in scan.patterns]


@pytest.fixture(scope="module")
def allowlist() -> list[str]:
    bundle = load_configuration(RepoPaths(root=ROOT))
    assert bundle.security is not None
    return list(bundle.security.secrets.scan.allowlist_paths)


def test_repository_has_no_credential_patterns(patterns: list[tuple[str, str]], allowlist: list[str]) -> None:
    """REQ-PS-001 — tracked files contain no credential material."""
    findings = scan_for_secrets(RepoPaths(root=ROOT), patterns, allowlist)
    rendered = [f"{finding.path}:{finding.line} ({finding.pattern})" for finding in findings]
    assert not rendered, "credential-like patterns found: " + ", ".join(rendered)


def test_environment_files_are_not_tracked() -> None:
    """REQ-PS-001 — secrets are injected at runtime, never committed."""
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", ".env"],
        cwd=ROOT,
        check=False,
    )
    assert ignored.returncode == 0, ".env must be ignored by Git"

    tracked = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    leaked = [path for path in tracked if path == ".env" or path.endswith("/.env")]
    assert not leaked, f"environment files must not be tracked: {leaked}"
    assert ".env.example" in tracked, "the example file documents the required variables"
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "OPENROUTER_API_KEY=\n" in example, "the example must leave secrets empty"


def test_planted_credential_is_detected(
    tmp_path: Path, patterns: list[tuple[str, str]]
) -> None:
    """REQ-RV-003 — the scanner detects a planted credential, so a clean scan is meaningful."""
    repository = tmp_path / "planted"
    repository.mkdir()
    (repository / "settings.py").write_text(
        'AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"\n'
        'GITHUB_TOKEN = "ghp_012345678901234567890123456789012345"\n',
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(["git", "add", "."], cwd=repository, check=True)

    findings = scan_for_secrets(RepoPaths(root=repository), patterns, [])

    assert findings, "the scanner must detect a planted AWS key and GitHub token"
    detected = {finding.pattern for finding in findings}
    assert len(detected) >= 2, f"expected multiple pattern hits, got {detected}"
    assert all(finding.path.endswith("settings.py") for finding in findings)


def test_allowlist_is_scoped_to_declared_paths() -> None:
    """REQ-PS-001 — allowlisted paths are explicit, never a blanket exclusion."""
    bundle = load_configuration(RepoPaths(root=ROOT))
    assert bundle.security is not None
    allowlist = bundle.security.secrets.scan.allowlist_paths
    blanket = {"*", "**", "**/*", ".*"}
    assert not (set(allowlist) & blanket), "no blanket allowlisting of the whole repository"
    assert all(".." not in entry for entry in allowlist), "allowlist must stay inside the repository"
    assert all(entry.strip() for entry in allowlist)
