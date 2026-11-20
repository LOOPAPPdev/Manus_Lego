"""Turn a selection proposal into an explicit integration plan.

The composer never decides that code is safe to copy. It enumerates the blockers
that a human and the engineering agent must clear, and it defaults to
``blocked`` whenever provenance, license or inventory evidence is missing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import catalog_engine
from .evidence import utc_now, write_json
from .paths import RepoPaths

SCHEMA_VERSION = "1.0.0"


def assess_candidate(candidate: dict[str, Any], manifest: dict[str, Any] | None) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []

    if manifest is None:
        blockers.append("manifest missing: run `lego index` to inspect this template before reuse")
        manifest = {}

    source = manifest.get("source", {})
    commit = source.get("commit") or candidate.get("commit")
    if not commit:
        blockers.append("no pinned commit: provenance is not reproducible")
    if not manifest:
        blockers.append("no inspected file inventory: the reuse surface is unknown")
    else:
        inventory = manifest.get("inventory", {})
        if not inventory.get("complete"):
            blockers.append("file inventory incomplete: uninspected paths may exist")
        if not inventory.get("files"):
            warnings.append("no files recorded; the template may be a metadata-only record")

    license_info = manifest.get("license", {})
    license_status = license_info.get("status", "unknown")
    if license_status in {"needs_review", "unknown", None}:
        blockers.append(f"license status '{license_status}': review required before copying code")

    if manifest.get("status") == "discovered_unverified":
        blockers.append("discovery-only record: no README or manifest inspection")

    for warning in manifest.get("warnings", []):
        warnings.append(str(warning))

    adapter_plan = [
        "Record the target runtime (Workers, Pages, Node, container) and confirm it matches the template's stack.",
        "Select the smallest set of files: configuration, one vertical slice, and the tests that cover it.",
        "Write an adapter at the boundary instead of importing template internals.",
        "Add a license and attribution note to docs/decisions before any file is copied.",
        "Reproduce the template's declared commands locally before adapting them.",
    ]

    required_tests = [
        "Contract test: the adapter returns the documented shape for a valid input.",
        "Failure test: the adapter rejects an invalid input without leaking internals.",
        "Provenance test: the reused file path and commit are recorded in the decision record.",
    ]

    return {
        "id": candidate.get("id"),
        "score": candidate.get("score"),
        "decision": "blocked" if blockers else "ready_for_review",
        "blockers": blockers,
        "warnings": warnings,
        "provenance": {
            "repository": source.get("repository") or candidate.get("source_url"),
            "path": source.get("path"),
            "commit": commit,
            "source_url": source.get("source_url") or candidate.get("source_url"),
            "license_status": license_status,
        },
        "reuse_scope": {
            "copy": [],
            "reference_only": True,
            "note": "Copying is a reviewed decision; this plan intentionally lists no files.",
        },
        "adapter_plan": adapter_plan,
        "required_tests": required_tests,
    }


def build_plan(paths: RepoPaths, selection: dict[str, Any]) -> dict[str, Any]:
    manifests = catalog_engine.load_manifests(paths)
    candidates = selection.get("candidates", [])
    assessments = [assess_candidate(candidate, manifests.get(candidate.get("id", ""))) for candidate in candidates]
    blocked = [item for item in assessments if item["decision"] == "blocked"]

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "request": selection.get("request"),
        "source_plan": paths.selection_plan.relative_to(paths.root).as_posix(),
        "status": "blocked" if blocked or not assessments else "ready_for_review",
        "summary": {
            "candidates": len(assessments),
            "blocked": len(blocked),
            "ready_for_review": len(assessments) - len(blocked),
        },
        "candidates": assessments,
        "next_actions": [
            "Resolve every blocker listed per candidate; do not copy code while any remain.",
            "Write an ADR that records the selected files, the commit and the license.",
            "Implement the adapter test-first; the plan lists the minimum tests.",
            "Re-run `lego verify` and attach the evidence to the pull request.",
        ],
    }


def write_plan(paths: RepoPaths, plan: dict[str, Any]) -> dict[str, Any]:
    artifact = write_json(paths.compose_plan, plan)
    return {"plan": plan, "artifact": artifact.as_dict()}


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
