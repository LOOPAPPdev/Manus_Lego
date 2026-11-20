"""CI/CD supply-chain and permission controls.

These tests read the workflow files as text on purpose: GitHub's YAML dialect makes
`on:` a boolean key under YAML 1.1, and a regex over `uses:` lines is a more honest
check of "every action is pinned" than a partially parsed document.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = ROOT / ".github/workflows"

#: Write scopes each workflow is allowed to request. Anything else fails the suite.
ALLOWED_WRITE_SCOPES: dict[str, set[str]] = {
    "release.yml": {"contents", "id-token", "attestations", "packages"},
    "security.yml": {"security-events"},
    "catalog-refresh.yml": {"contents", "pull-requests"},
}


def _workflows() -> list[Path]:
    files = sorted(WORKFLOW_DIR.glob("*.yml")) + sorted(WORKFLOW_DIR.glob("*.yaml"))
    return files


@pytest.fixture(scope="module")
def workflows() -> list[Path]:
    files = _workflows()
    assert files, "the repository must ship CI workflows"
    return files


def test_actions_are_pinned_to_commit_shas(workflows: list[Path]) -> None:
    """REQ-PS-003 — a mutable tag can be repointed; a commit SHA cannot."""
    offenders: list[str] = []
    references = 0
    for workflow in workflows:
        text = workflow.read_text(encoding="utf-8")
        for match in re.finditer(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)", text, re.MULTILINE):
            reference = match.group(1)
            references += 1
            if reference.startswith("./"):
                continue
            if reference.startswith("docker://"):
                if "@sha256:" not in reference:
                    offenders.append(f"{workflow.name}: {reference}")
                continue
            _, _, version = reference.partition("@")
            if not re.fullmatch(r"[0-9a-f]{40}", version):
                offenders.append(f"{workflow.name}: {reference}")

    assert references >= 8, "expected the CI to use the standard actions"
    assert not offenders, "unpinned actions: " + ", ".join(offenders)


def test_workflows_declare_minimal_permissions(workflows: list[Path]) -> None:
    """REQ-PW-006 — the default token is read-only and each job widens it explicitly."""
    problems: list[str] = []
    for workflow in workflows:
        text = workflow.read_text(encoding="utf-8")
        if not re.search(r"^permissions:", text, re.MULTILINE):
            problems.append(f"{workflow.name}: no top-level permissions block")
            continue
        if "write-all" in text:
            problems.append(f"{workflow.name}: uses write-all")
        allowed = ALLOWED_WRITE_SCOPES.get(workflow.name, set())
        for scope in re.findall(r"^\s*([a-z-]+):\s*write\s*$", text, re.MULTILINE):
            if scope not in allowed:
                problems.append(f"{workflow.name}: unexpected write scope '{scope}'")
    assert not problems, "; ".join(problems)


def test_no_pull_request_target(workflows: list[Path]) -> None:
    """REQ-PW-006 — pull_request_target exposes secrets to fork code."""
    offenders = [workflow.name for workflow in workflows if "pull_request_target" in workflow.read_text(encoding="utf-8")]
    assert not offenders, f"pull_request_target is forbidden: {offenders}"


def test_dependabot_covers_every_ecosystem() -> None:
    """REQ-RV-001 — npm, GitHub Actions and both Python services are updated automatically."""
    path = ROOT / ".github/dependabot.yml"
    assert path.is_file(), "Dependabot configuration is required"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    ecosystems = {entry["package-ecosystem"] for entry in document["updates"]}
    assert {"npm", "github-actions", "uv"} <= ecosystems, ecosystems

    directories = {
        (entry.get("directory") or "").lstrip("/")
        for entry in document["updates"]
        if entry["package-ecosystem"] == "uv"
    }
    assert {"services/orchestrator", "services/rag"} <= directories, directories
    assert all(entry.get("schedule", {}).get("interval") in {"daily", "weekly", "monthly"} for entry in document["updates"])


def test_security_workflow_runs_codeql_and_scans_containers() -> None:
    """REQ-RV-001 — static analysis and image scanning run on a schedule and on PRs."""
    path = WORKFLOW_DIR / "security.yml"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")

    assert "github/codeql-action/init@" in text
    assert "github/codeql-action/analyze@" in text
    assert "security-events: write" in text
    assert "schedule:" in text, "a weekly scan catches drift that a PR-only scan misses"
    assert "pull_request:" in text
    assert "trivy" in text.lower() or "upload-sarif" in text
    assert "actions/dependency-review-action@" in text, "dependency review must gate pull requests"


def test_release_requires_a_protected_environment() -> None:
    """REQ-PO-005 — publishing is gated by a human approval on an environment."""
    text = (WORKFLOW_DIR / "release.yml").read_text(encoding="utf-8")

    assert "environment:" in text, "the release job must target a protected environment"
    assert "production" in text
    assert "workflow_dispatch" in text
    assert "attestations: write" in text or "id-token: write" in text, "provenance needs an OIDC token"
    assert "sbom" in text.lower(), "the release must publish an SBOM"


def test_catalog_refresh_opens_a_pull_request() -> None:
    """REQ-PS-002 — refreshing the index is a reviewed pull request, never a push to main."""
    text = (WORKFLOW_DIR / "catalog-refresh.yml").read_text(encoding="utf-8")

    assert "workflow_dispatch" in text, "the refresh is human-triggered by design"
    assert "contents: write" in text
    assert "git push origin \"$branch\"" in text or "git push" in text
    assert "gh pr create" in text, "the refreshed index must arrive as a reviewable PR"
    assert "secrets.GITHUB_TOKEN" in text or "secrets.CATALOG_TOKEN" in text
    assert "git push origin main" not in text, "never push the index directly to the default branch"
