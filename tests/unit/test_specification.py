"""Specification, configuration and toolchain contracts.

Every test names the requirement it verifies. `lego report` discovers the marker in
the test body, so renaming or deleting a test changes the requirement status instead
of silently keeping a stale claim.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import jsonschema
import pytest
import yaml

from lego_orchestrator.config import load_configuration
from lego_orchestrator.paths import RepoPaths
from lego_orchestrator.traceability import load_requirements

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def paths() -> RepoPaths:
    return RepoPaths(root=ROOT)


def test_requirements_have_acceptance_criteria(paths: RepoPaths) -> None:
    """REQ-PO-001 — every requirement carries acceptance criteria and appears in the spec."""
    file = load_requirements(paths)
    assert len(file.requirements) >= 10, "the specification must describe the whole foundation"
    assert {requirement.practice for requirement in file.requirements} == {"PO", "PS", "PW", "RV"}

    ids = [requirement.id for requirement in file.requirements]
    assert len(ids) == len(set(ids)), "requirement identifiers must be unique"

    document = (ROOT / "docs/specifications/requirements.md").read_text(encoding="utf-8")
    for requirement in file.requirements:
        assert requirement.acceptance, f"{requirement.id} has no acceptance criteria"
        assert requirement.statement.strip(), f"{requirement.id} has no statement"
        assert requirement.implementation, f"{requirement.id} names no implementation path"
        assert requirement.id in document, f"{requirement.id} is missing from requirements.md"


def test_declared_implementation_paths_exist(paths: RepoPaths) -> None:
    """REQ-PO-001 — the matrix points at real files, not aspirational ones."""
    file = load_requirements(paths)
    missing: list[str] = []
    for requirement in file.requirements:
        for relative in requirement.implementation:
            if not (ROOT / relative).exists():
                missing.append(f"{requirement.id} -> {relative}")
    assert not missing, "traceability references missing paths: " + ", ".join(missing)


def test_agent_permissions_are_bounded(paths: RepoPaths) -> None:
    """REQ-PO-002 — authority comes from the team schema and separation of duties holds."""
    bundle = load_configuration(paths)
    assert bundle.problems == [], f"configuration problems: {bundle.problems}"
    assert bundle.team is not None and bundle.agents is not None

    allowlist = set(bundle.team.tool_policy.catalog)
    for agent in bundle.team.agents:
        unknown = set(agent.tools) - allowlist
        assert not unknown, f"agent {agent.id} uses undeclared tools: {sorted(unknown)}"

    owner = bundle.team.team.owner
    owner_agent = next(agent for agent in bundle.team.agents if agent.id == owner)
    assert "repo_write" not in owner_agent.tools, "the orchestrator must not write code itself"

    auditor = next(agent for agent in bundle.team.agents if agent.id == "quality_auditor")
    assert "repo_write" not in auditor.tools, "the independent reviewer cannot implement what it reviews"

    registry_ids = {agent.id for agent in bundle.agents.agents}
    assert registry_ids == {agent.id for agent in bundle.team.agents}


def test_toolchain_is_reproducible(paths: RepoPaths) -> None:
    """REQ-PO-003 — lockfiles and pinned runtimes make the build reproducible."""
    for relative in ("pnpm-lock.yaml", "services/orchestrator/uv.lock", "services/rag/uv.lock"):
        lock = ROOT / relative
        assert lock.is_file(), f"{relative} must be committed"
        assert lock.stat().st_size > 0, f"{relative} is empty"

    manifest = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"pnpm@\d+\.\d+\.\d+", manifest["packageManager"]), "packageManager must pin an exact pnpm"

    workspace = yaml.safe_load((ROOT / "pnpm-workspace.yaml").read_text(encoding="utf-8"))
    builds = workspace.get("allowBuilds") or {}
    assert builds.get("esbuild") is True, "dependency lifecycle scripts must be allowlisted explicitly"
    assert (ROOT / "turbo.json").is_file()

    config = load_configuration(paths)
    assert config.manus is not None
    version = re.compile(r"(?:>=|\^|~)?\d+\.\d+(?:\.\d+)?")
    assert version.fullmatch(config.manus.runtime.node), config.manus.runtime.node
    assert version.fullmatch(config.manus.runtime.python), config.manus.runtime.python


def test_contracts_match_the_catalog(paths: RepoPaths) -> None:
    """REQ-PW-001 — the published schema accepts every committed manifest."""
    schema = json.loads((ROOT / "schemas/template.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)

    manifests = sorted((ROOT / "catalog/templates").rglob("*.json"))
    assert len(manifests) >= 40, "the catalog must contain the explored templates"

    invalid: dict[str, str] = {}
    for manifest_path in manifests:
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        if errors:
            invalid[manifest_path.name] = errors[0].message
    assert not invalid, f"manifests violating schemas/template.schema.json: {invalid}"

    index = json.loads((ROOT / "catalog/index.json").read_text(encoding="utf-8"))
    assert index["templates"], "the index must expose the templates"
    assert (ROOT / "packages/schemas/src/catalog.ts").is_file(), "TypeScript consumers need the same contract"


def test_typescript_and_python_contracts_agree() -> None:
    """REQ-PW-001 — the TS schema and the JSON Schema describe the same required fields."""
    schema = json.loads((ROOT / "schemas/template.schema.json").read_text(encoding="utf-8"))
    required = set(schema.get("required", []))
    source = (ROOT / "packages/schemas/src/catalog.ts").read_text(encoding="utf-8")
    for field in required:
        assert field in source, f"packages/schemas does not model required field '{field}'"
