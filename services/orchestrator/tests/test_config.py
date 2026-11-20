"""Configuration loading and cross-file validation.

The configuration is a control surface, not documentation: an unknown key, an agent with a
tool it should not hold, or a policy path that does not exist must be an error.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from lego_orchestrator.config import load_configuration
from lego_orchestrator.paths import RepoPaths

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture()
def scratch(tmp_path: Path) -> Path:
    """A copy of the configuration tree that a test may break on purpose."""
    repository = tmp_path / "repo"
    for entry in ("config", "agents", "workflows"):
        shutil.copytree(ROOT / entry, repository / entry)
    return repository


def test_committed_configuration_is_valid() -> None:
    """REQ-PO-002 — the configuration in the repository passes every cross-file rule."""
    bundle = load_configuration(RepoPaths(root=ROOT))

    assert bundle.problems == []
    assert bundle.valid is True
    assert bundle.team is not None
    assert len(bundle.team.agents) == 6


def test_unknown_key_is_rejected(scratch: Path) -> None:
    """REQ-PW-003 — an unknown key is a validation error, not a silently ignored field."""
    path = scratch / "config/manus.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["api"]["rate_limit_per_minute_typo"] = 5
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    bundle = load_configuration(RepoPaths(root=scratch))

    assert bundle.valid is False
    assert any("rate_limit_per_minute_typo" in problem for problem in bundle.problems)


def test_orchestrator_cannot_hold_repo_write(scratch: Path) -> None:
    """REQ-PO-002 — separation of duties is enforced by validation, not by convention."""
    path = scratch / "config/TEAMSCHEMA.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    for agent in document["agents"]:
        if agent["id"] == document["team"]["owner"]:
            agent["tools"] = [*agent["tools"], "repo_write"]
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    bundle = load_configuration(RepoPaths(root=scratch))

    assert bundle.valid is False
    assert any("repo_write" in problem for problem in bundle.problems)


def test_undeclared_tool_is_rejected(scratch: Path) -> None:
    """REQ-PO-002 — an agent may only use tools from the declared catalogue."""
    path = scratch / "config/TEAMSCHEMA.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["agents"][1]["tools"] = [*document["agents"][1]["tools"], "root_shell"]
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    bundle = load_configuration(RepoPaths(root=scratch))

    assert bundle.valid is False
    assert any("root_shell" in problem for problem in bundle.problems)


def test_missing_policy_file_is_rejected(scratch: Path) -> None:
    """REQ-PW-003 — a declared policy path that does not exist is a broken configuration."""
    (scratch / "agents/orchestrator/AGENT.md").unlink()

    bundle = load_configuration(RepoPaths(root=scratch))

    assert bundle.valid is False
    assert any("prompt file missing" in problem for problem in bundle.problems)


def test_agent_registry_matches_the_team_schema() -> None:
    """REQ-PO-002 — the runtime registry and the team schema cannot drift apart."""
    bundle = load_configuration(RepoPaths(root=ROOT))

    assert bundle.team is not None and bundle.agents is not None
    assert {agent.id for agent in bundle.agents.agents} == {agent.id for agent in bundle.team.agents}
    assert bundle.agents.orchestrator, "the registry must name the orchestrator entry point"
    for agent in bundle.agents.agents:
        assert agent.prompt, f"registry entry {agent.id} has no prompt"
