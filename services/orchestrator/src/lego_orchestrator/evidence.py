"""Evidence artifacts with reproducible digests.

Every generated report is written atomically and accompanied by a SHA-256 digest,
so a reviewer can prove that the report they read corresponds to the bytes a
given commit produced. The manifest ties reports together for a single run.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .paths import RepoPaths


@dataclass(frozen=True, slots=True)
class Artifact:
    path: str
    sha256: str
    bytes: int

    def as_dict(self) -> dict[str, object]:
        return {"path": self.path, "sha256": self.sha256, "bytes": self.bytes}


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(payload)
        os.replace(temporary, path)
    except BaseException:  # pragma: no cover - defensive cleanup
        Path(temporary).unlink(missing_ok=True)
        raise


def write_bytes(path: Path, payload: bytes) -> Artifact:
    _atomic_write(path, payload)
    return Artifact(path=path.as_posix(), sha256=hashlib.sha256(payload).hexdigest(), bytes=len(payload))


def write_text(path: Path, text: str) -> Artifact:
    return write_bytes(path, text.encode("utf-8"))


def write_json(path: Path, value: Any) -> Artifact:
    payload = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return write_text(path, payload)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit(root: Path) -> str:
    """Return the current commit SHA, or ``uncommitted`` outside a Git repository."""

    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return "uncommitted"
    return completed.stdout.strip() or "uncommitted"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_manifest(paths: RepoPaths, *, commit: str, producer: str) -> dict[str, Any]:
    """Describe every evidence artifact currently on disk."""

    entries: list[dict[str, Any]] = []
    if paths.evidence_dir.is_dir():
        for path in sorted(paths.evidence_dir.rglob("*")):
            if not path.is_file() or path.name == "evidence-manifest.json":
                continue
            entries.append(
                {
                    "path": path.relative_to(paths.root).as_posix(),
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
            )
    return {
        "schema_version": "1.0.0",
        "generated_at": utc_now(),
        "commit": commit,
        "producer": producer,
        "artifact_count": len(entries),
        "artifacts": entries,
    }
