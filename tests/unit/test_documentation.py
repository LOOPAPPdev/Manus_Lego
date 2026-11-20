"""Documentation that the gates depend on.

G5 fails when the architecture diagram, the threat model or the runbook is missing.
This module asserts the documents also contain the sections an operator needs, so a
placeholder file cannot satisfy the gate.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    path = ROOT / relative
    assert path.is_file(), f"{relative} is required by gate G5"
    return path.read_text(encoding="utf-8")


def test_runbook_documents_vulnerability_register() -> None:
    """REQ-RV-002 — vulnerabilities are triaged with severities, owners and SLAs."""
    runbook = _read("docs/operations/runbook.md")

    for severity in ("Critical", "High", "Medium", "Low"):
        assert severity in runbook, f"the register must define {severity} severity"
    assert re.search(r"\bSLA\b", runbook), "remediation SLAs must be stated"
    assert "severity" in runbook.lower()
    assert "rollback" in runbook.lower(), "the runbook must describe how to roll back"
    assert "on-call" in runbook.lower() or "owner" in runbook.lower()


def test_threat_model_names_trust_boundaries_and_mitigations() -> None:
    """REQ-RV-003 — the threat model covers the AI-specific risks this repo actually has."""
    threat_model = _read("docs/security/threat-model.md")

    for topic in ("prompt injection", "untrusted", "secret", "supply chain"):
        assert topic in threat_model.lower(), f"threat model must discuss {topic}"
    assert "trust boundar" in threat_model.lower()
    assert "residual" in threat_model.lower(), "residual risk must be explicit"


def test_architecture_diagram_is_renderable() -> None:
    """REQ-PO-004 — the architecture is described in a diagram source, not prose only."""
    diagram = _read("docs/architecture.mmd")
    assert diagram.startswith(("flowchart", "graph", "---")), "expected a Mermaid diagram source"
    assert "api" in diagram.lower()
    assert "orchestrator" in diagram.lower()


def test_readme_states_limits_and_non_claims() -> None:
    """REQ-PW-005 — the project never presents implemented controls as certification."""
    readme = _read("README.md")
    lowered = readme.lower()

    assert "not a certification" in lowered or "not certified" in lowered
    assert "verified" in lowered
    assert "enriched" in lowered, "the catalog coverage labels must be explained"
    for command in ("lego verify", "lego report", "turbo"):
        assert command in readme, f"README must document `{command}`"


@pytest.mark.parametrize("relative", ["docs/nist-mapping.md", "docs/quality/testing-strategy.md"])
def test_supporting_documents_exist(relative: str) -> None:
    """REQ-PO-001 — the specification set is complete and navigable."""
    assert (ROOT / relative).is_file(), f"{relative} is part of the specification set"
