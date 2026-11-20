#!/usr/bin/env python3
"""G0–G6 — the executable orchestration workflow.

Runs the deterministic stages in order and stops at the first gate that cannot
pass. It never merges, deploys or creates secrets: the final stage reports what a
human must authorize.

    uv run --project services/orchestrator python workflows/execute.py \
        "react authentication database" --limit 3

Stages: spec → discover → select → compose → verify → report.

Exit codes: 0 all evaluated gates pass, 1 a gate failed, 2 configuration error,
3 blocked (missing evidence or human authorization).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "orchestrator" / "src"))

try:
    from lego_orchestrator import catalog_engine, compose, gates, traceability
    from lego_orchestrator.cli import EXIT_BLOCKED, EXIT_FAIL, EXIT_OK, EXIT_USAGE, _load_bundle
    from lego_orchestrator.config import ConfigError
    from lego_orchestrator.evidence import git_commit, utc_now
    from lego_orchestrator.paths import repo_paths
except ImportError as exc:  # pragma: no cover - environment guidance
    print(
        json.dumps(
            {
                "stage": "execute",
                "state": "blocked",
                "reason": f"missing orchestrator dependencies: {exc}",
                "fix": "uv sync --project services/orchestrator",
            }
        ),
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


def stage(name: str, state: str, **fields: object) -> None:
    print(json.dumps({"stage": name, "state": state, **fields}, ensure_ascii=False), flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Manus LEGO orchestration workflow.")
    parser.add_argument("request", help="Plain-language requirement to satisfy")
    parser.add_argument("--provider", choices=["all", "cloudflare", "vercel"], default="all")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--junit", action="append", default=[], metavar="LABEL=PATH")
    parser.add_argument("--environment", default="local")
    parser.add_argument("--skip-network", action="store_true", help="Do not refresh the catalog (default)")
    args = parser.parse_args(argv)

    paths = repo_paths(ROOT)

    try:
        bundle = _load_bundle(paths)
    except ConfigError as exc:
        stage("spec", "failed", problems=exc.problems)
        return EXIT_USAGE
    stage("spec", "passed", owner=bundle.manus.project.owner, gates=len(bundle.manus.gates))

    index = catalog_engine.load_index(paths)
    stage(
        "discover",
        "passed",
        templates=index.get("template_count", 0),
        coverage=index.get("coverage"),
        sources=[source.id for source in bundle.sources.sources],
    )

    selection = catalog_engine.plan(paths, args.request, provider=args.provider, limit=args.limit)
    manifests = catalog_engine.load_manifests(paths)
    assessed = [
        compose.assess_candidate(candidate, manifests.get(candidate.get("id", "")))
        for candidate in selection.get("candidates", [])
    ]
    stage(
        "select",
        "passed" if assessed else "blocked",
        request=args.request,
        candidates=[{"id": item["id"], "decision": item["decision"], "blockers": len(item["blockers"])} for item in assessed],
    )

    plan = compose.build_plan(paths, selection)
    compose.write_plan(paths, plan)
    stage("compose", plan["status"], summary=plan["summary"], plan="catalog/compose_plan.json")

    junit = {}
    for value in args.junit:
        label, _, raw = value.partition("=")
        if raw:
            junit[label] = Path(raw)
    commit = git_commit(paths.root)
    report = gates.evaluate(paths, commit=commit, environment=args.environment, junit_paths=junit)
    gates.write_report(paths, report)
    stage(
        "verify",
        report.overall,
        gates=[{"id": gate.id, "status": gate.status} for gate in report.gates],
        evidence="docs/evidence/gates.json",
    )

    trace = traceability.build_report(paths, commit=commit, generated_at=utc_now(), junit_paths=junit)
    traceability.write_report(paths, trace)
    stage("report", "passed", summary=trace.summary, evidence="docs/evidence/traceability.json")

    if report.overall == "fail":
        return EXIT_FAIL
    if report.overall in {"blocked", "not_evaluated"}:
        stage("release", "blocked", reason="human authorization or missing evidence prevents release")
        return EXIT_BLOCKED
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
