#!/usr/bin/env python3
"""G0/G1 — discover allowlisted sources and report catalog coverage.

This workflow answers one question: *what may we look at, and how trustworthy is
it?* It performs no writes and, without ``--check``, no network access.

    python3 workflows/discover.py
    python3 workflows/discover.py --check --json

Requires the orchestrator environment:

    uv run --project services/orchestrator python workflows/discover.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "orchestrator" / "src"))

try:
    from lego_orchestrator.cli import EXIT_OK, cmd_discover
    from lego_orchestrator.paths import repo_paths
except ImportError as exc:  # pragma: no cover - environment guidance
    print(
        json.dumps(
            {
                "stage": "discover",
                "state": "blocked",
                "reason": f"missing orchestrator dependencies: {exc}",
                "fix": "uv sync --project services/orchestrator && uv run --project services/orchestrator python workflows/discover.py",
            }
        ),
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="Verify reachability of allowlisted sources (network)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    args = parser.parse_args(argv)

    paths = repo_paths(ROOT)
    if args.json:
        return cmd_discover(paths, argparse.Namespace(check=args.check))
    return cmd_discover(paths, argparse.Namespace(check=args.check)) or EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
