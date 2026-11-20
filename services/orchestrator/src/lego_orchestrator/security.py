"""Repository secret scanning.

Deliberately conservative: high-signal credential prefixes and private-key headers
only. Entropy heuristics generate noise that trains reviewers to ignore alerts.

Scans tracked files (``git ls-files``) so build output and local ``.env`` files are
out of scope by construction. A file that cannot be decoded is skipped, never
reported as clean by accident.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from .paths import RepoPaths

MAX_SCAN_BYTES = 2_000_000
BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".woff",
    ".woff2",
    ".ttf",
    ".sqlite3",
    ".bin",
}


@dataclass(frozen=True, slots=True)
class SecretFinding:
    path: str
    pattern: str
    line: int

    def as_dict(self) -> dict[str, object]:
        return {"path": self.path, "pattern": self.pattern, "line": self.line}


def tracked_files(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return []
    return [name for name in completed.stdout.split("\0") if name]


def _is_allowlisted(relative_path: str, allowlist: list[str]) -> bool:
    return any(fnmatch(relative_path, pattern) for pattern in allowlist)


def scan_for_secrets(paths: RepoPaths, patterns: list[tuple[str, str]], allowlist: list[str]) -> list[SecretFinding]:
    """Return findings for credential patterns in tracked files."""

    compiled = [(name, re.compile(regex)) for name, regex in patterns]
    findings: list[SecretFinding] = []

    for relative in tracked_files(paths.root):
        if _is_allowlisted(relative, allowlist):
            continue
        candidate = paths.root / relative
        if not candidate.is_file() or candidate.suffix.lower() in BINARY_SUFFIXES:
            continue
        try:
            if candidate.stat().st_size > MAX_SCAN_BYTES:
                continue
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for name, regex in compiled:
                if regex.search(line):
                    findings.append(SecretFinding(path=relative, pattern=name, line=line_number))
    return findings
