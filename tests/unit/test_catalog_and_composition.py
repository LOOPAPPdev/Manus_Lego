"""Catalog provenance and reuse composition.

The catalog is the product's source of truth about external templates. These tests
assert that it never claims more than it verified, and that reuse defaults to
`blocked` until provenance, license and inventory evidence exist.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from lego_orchestrator import catalog_engine, compose
from lego_orchestrator.paths import RepoPaths

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def paths() -> RepoPaths:
    return RepoPaths(root=ROOT)


def test_catalog_validation_reports_valid(paths: RepoPaths) -> None:
    """REQ-PS-002 — the committed catalog passes its own provenance rules."""
    verdict = catalog_engine.validate_catalog(paths)
    assert verdict.get("valid") is True, verdict.get("issues")
    assert verdict.get("templates", 0) >= 40


def test_records_never_claim_completeness_without_a_commit(paths: RepoPaths) -> None:
    """REQ-PS-002 — an enriched record must pin the commit it describes."""
    index = catalog_engine.load_index(paths)
    templates = index["templates"]
    assert templates

    unpinned = [
        entry["id"]
        for entry in templates
        if entry.get("status") in {"enriched", "reference_only"} and not entry.get("commit")
    ]
    assert not unpinned, f"records claim enrichment without a pinned commit: {unpinned}"

    for entry in templates:
        assert entry.get("provider") in {"cloudflare", "vercel"}
        assert entry.get("repository"), f"{entry['id']} has no repository"
        assert entry.get("source_url"), f"{entry['id']} has no source URL"
        if entry.get("status") == "enriched":
            assert entry.get("path"), f"{entry['id']} claims enrichment without an inspected path"


def test_unknown_template_is_blocked_not_guessed(paths: RepoPaths) -> None:
    """REQ-PW-002 — a candidate without a manifest cannot be composed."""
    plan = compose.build_plan(paths, {"request": "unknown", "candidates": [{"id": "does-not-exist"}]})

    assert plan["status"] == "blocked"
    candidate = plan["candidates"][0]
    assert candidate["decision"] == "blocked"
    assert any("manifest missing" in blocker for blocker in candidate["blockers"])
    assert candidate["reuse_scope"]["copy"] == [], "a plan must not list files before review"
    assert candidate["reuse_scope"]["reference_only"] is True


def test_composition_requires_reviewed_license_and_inventory(paths: RepoPaths) -> None:
    """REQ-PW-002 — missing license review or incomplete inventory blocks reuse."""
    manifest = {
        "status": "enriched",
        "source": {"repository": "cloudflare/templates", "path": "x", "commit": "a" * 40},
        "inventory": {"complete": False, "files": []},
        "license": {"status": "needs_review"},
    }
    assessment = compose.assess_candidate({"id": "x", "score": 1.0}, manifest)

    assert assessment["decision"] == "blocked"
    joined = " ".join(assessment["blockers"])
    assert "inventory incomplete" in joined
    assert "needs_review" in joined


def test_complete_evidence_yields_ready_for_review(paths: RepoPaths) -> None:
    """REQ-PW-002 — the only non-blocked state is `ready_for_review`, never `approved`."""
    manifest = {
        "status": "enriched",
        "source": {"repository": "cloudflare/templates", "path": "x", "commit": "b" * 40},
        "inventory": {"complete": True, "files": ["wrangler.toml"]},
        "license": {"status": "permissive"},
    }
    assessment = compose.assess_candidate({"id": "x", "score": 1.0}, manifest)

    assert assessment["decision"] == "ready_for_review"
    assert assessment["blockers"] == []
    assert assessment["reuse_scope"]["copy"] == []
