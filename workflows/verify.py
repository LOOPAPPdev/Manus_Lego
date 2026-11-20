#!/usr/bin/env python3
"""G4/G5 — evaluate quality gates from produced artifacts.

By default the workflow consumes existing JUnit reports. Pass ``--run-tests`` to
execute the Python suites first and capture fresh XML.

    uv run --project services/orchestrator python workflows/verify.py \
        --junit unit=reports/junit/unit.xml \
        --junit integration=reports/junit/integration.xml \
        --junit security=reports/junit/security.xml

Exit codes: 0 pass, 1 fail, 3 blocked / not evaluated.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "orchestrator" / "src"))

try:
    from lego_orchestrator.cli import cmd_verify
    from lego_orchestrator.paths import repo_paths
except ImportError as exc:  # pragma: no cover - environment guidance
    print(f"missing orchestrator dependencies: {exc}\nfix: uv sync --project services/orchestrator", file=sys.stderr)
    raise SystemExit(2) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Manus LEGO quality gates.")
    parser.add_argument("--junit", action="append", default=[], metavar="LABEL=PATH")
    parser.add_argument("--run-tests", action="store_true")
    parser.add_argument("--environment", default="local")
    args = parser.parse_args(argv)

    namespace = argparse.Namespace(junit=args.junit, run_tests=args.run_tests, environment=args.environment)
    return cmd_verify(repo_paths(ROOT), namespace)


if __name__ == "__main__":
    raise SystemExit(main())
