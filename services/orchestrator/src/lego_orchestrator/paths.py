"""Repository layout resolution.

The CLI must work from any working directory (repo root, a service directory, CI).
Resolution order: ``LEGO_REPO_ROOT`` -> nearest ancestor with ``turbo.json`` ->
nearest ancestor with ``.git``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


class RepositoryNotFound(RuntimeError):
    """Raised when the repository root cannot be located."""


def find_repo_root(start: Path | str | None = None) -> Path:
    override = os.environ.get("LEGO_REPO_ROOT")
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
        raise RepositoryNotFound(f"LEGO_REPO_ROOT does not exist: {candidate}")

    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent

    for marker in ("turbo.json", ".git"):
        cursor = current
        while True:
            if (cursor / marker).exists():
                return cursor
            if cursor.parent == cursor:
                break
            cursor = cursor.parent

    raise RepositoryNotFound(f"Unable to locate the repository root from {current}")


@dataclass(frozen=True, slots=True)
class RepoPaths:
    root: Path

    @property
    def catalog(self) -> Path:
        return self.root / "catalog"

    @property
    def catalog_index(self) -> Path:
        return self.catalog / "index.json"

    @property
    def catalog_templates(self) -> Path:
        return self.catalog / "templates"

    @property
    def catalog_sources(self) -> Path:
        return self.catalog / "sources.json"

    @property
    def template_schema(self) -> Path:
        return self.root / "schemas" / "template.schema.json"

    @property
    def config(self) -> Path:
        return self.root / "config"

    @property
    def manus_config(self) -> Path:
        return self.config / "manus.yaml"

    @property
    def security_policy(self) -> Path:
        return self.config / "security.yaml"

    @property
    def team_schema(self) -> Path:
        return self.config / "TEAMSCHEMA.yaml"

    @property
    def sources_config(self) -> Path:
        return self.config / "sources.yaml"

    @property
    def agents_registry(self) -> Path:
        return self.root / "agents" / "registry.yaml"

    @property
    def requirements(self) -> Path:
        return self.root / "docs" / "specifications" / "requirements.md"

    @property
    def traceability(self) -> Path:
        return self.root / "docs" / "specifications" / "traceability.yaml"

    @property
    def evidence_dir(self) -> Path:
        return self.root / "docs" / "evidence"

    @property
    def gates_report(self) -> Path:
        return self.evidence_dir / "gates.json"

    @property
    def traceability_report(self) -> Path:
        return self.evidence_dir / "traceability.json"

    @property
    def evidence_manifest(self) -> Path:
        return self.evidence_dir / "evidence-manifest.json"

    @property
    def selection_plan(self) -> Path:
        return self.catalog / "selection_plan.json"

    @property
    def compose_plan(self) -> Path:
        return self.catalog / "compose_plan.json"

    @property
    def engine_script(self) -> Path:
        return self.root / "scripts" / "lego_catalog.py"

    @property
    def approvals_dir(self) -> Path:
        return self.evidence_dir / "approvals"


def repo_paths(start: Path | str | None = None) -> RepoPaths:
    return RepoPaths(root=find_repo_root(start))
