"""Adapter around the existing catalog engine (`scripts/lego_catalog.py`).

The engine is the implementation of record for discovery, scoring, manifest
validation and plan generation. This module deliberately does **not** reimplement
any of it (ADR 0005): it invokes the engine as a subprocess so its exit codes,
stdout contract and fail-closed behaviour are preserved exactly, and loads it as
a module only where a library call is genuinely needed (tests, parity checks).
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any

from .paths import RepoPaths


class EngineError(RuntimeError):
    """The catalog engine failed or returned unparseable output."""

    def __init__(self, message: str, *, returncode: int | None = None, stderr: str = "") -> None:
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(message)


@lru_cache(maxsize=1)
def load_engine_module(script: Path) -> ModuleType:
    """Import the engine script as a module (read-only use)."""

    spec = importlib.util.spec_from_file_location("lego_catalog_engine", script)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise EngineError(f"Cannot load catalog engine from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_engine(paths: RepoPaths, args: list[str], *, timeout: int = 900) -> subprocess.CompletedProcess[str]:
    """Run the engine with the current interpreter and return the completed process."""

    if not paths.engine_script.is_file():
        raise EngineError(f"Catalog engine missing: {paths.engine_script}")

    completed = subprocess.run(
        [sys.executable, str(paths.engine_script), *args],
        cwd=paths.root,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return completed


def _parse_json_output(completed: subprocess.CompletedProcess[str], action: str) -> Any:
    stdout = completed.stdout.strip()
    if not stdout:
        raise EngineError(
            f"Engine '{action}' produced no output", returncode=completed.returncode, stderr=completed.stderr
        )
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise EngineError(
            f"Engine '{action}' returned non-JSON output",
            returncode=completed.returncode,
            stderr=completed.stderr or stdout[:500],
        ) from exc


def validate_catalog(paths: RepoPaths) -> dict[str, Any]:
    """Run the engine's provenance validation and return its JSON verdict."""

    completed = run_engine(paths, ["--output", str(paths.root), "validate"])
    payload = _parse_json_output(completed, "validate")
    if completed.returncode not in (0, 1):
        raise EngineError(
            "Engine validate failed unexpectedly", returncode=completed.returncode, stderr=completed.stderr
        )
    return payload


def search(paths: RepoPaths, query: str, *, provider: str = "all", limit: int = 10) -> dict[str, Any]:
    completed = run_engine(
        paths,
        ["--output", str(paths.root), "search", query, "--provider", provider, "--limit", str(limit)],
    )
    if completed.returncode != 0:
        raise EngineError("Engine search failed", returncode=completed.returncode, stderr=completed.stderr)
    return _parse_json_output(completed, "search")


def plan(paths: RepoPaths, query: str, *, provider: str = "all", limit: int = 5) -> dict[str, Any]:
    completed = run_engine(
        paths,
        ["--output", str(paths.root), "plan", query, "--provider", provider, "--limit", str(limit)],
    )
    if completed.returncode != 0:
        raise EngineError("Engine plan failed", returncode=completed.returncode, stderr=completed.stderr)
    plan_path = paths.selection_plan
    if not plan_path.is_file():
        raise EngineError(f"Engine did not write the selection plan at {plan_path}")
    return json.loads(plan_path.read_text(encoding="utf-8"))


def index(
    paths: RepoPaths,
    *,
    offline: bool = False,
    refresh: bool = False,
    gallery: bool = False,
    max_enrich: int = 25,
    max_pages: int = 100,
    max_templates: int | None = None,
    pause: float = 0.1,
) -> dict[str, Any]:
    args = ["--output", str(paths.root), "index", "--max-enrich", str(max_enrich), "--max-pages", str(max_pages)]
    if offline:
        args.append("--offline")
    if refresh:
        args.append("--refresh")
    if gallery:
        args.append("--gallery")
    if max_templates is not None:
        args += ["--max-templates", str(max_templates)]
    args += ["--pause", str(pause)]
    completed = run_engine(paths, args, timeout=1800)
    if completed.returncode != 0:
        raise EngineError("Engine index failed", returncode=completed.returncode, stderr=completed.stderr)
    return _parse_json_output(completed, "index")


def load_index(paths: RepoPaths) -> dict[str, Any]:
    if not paths.catalog_index.is_file():
        raise EngineError(f"Catalog index missing: {paths.catalog_index}")
    return json.loads(paths.catalog_index.read_text(encoding="utf-8"))


def manifest_paths(paths: RepoPaths) -> list[Path]:
    if not paths.catalog_templates.is_dir():
        return []
    return sorted(paths.catalog_templates.glob("*/*.json"))


def load_manifests(paths: RepoPaths) -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    for path in manifest_paths(paths):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        identifier = document.get("id")
        if isinstance(identifier, str):
            manifests[identifier] = document
    return manifests


def find_manifest(paths: RepoPaths, template_id: str) -> dict[str, Any] | None:
    for path in manifest_paths(paths):
        if path.stem == template_id.rsplit(":", 1)[-1]:
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if document.get("id") == template_id:
                return document
    return None
