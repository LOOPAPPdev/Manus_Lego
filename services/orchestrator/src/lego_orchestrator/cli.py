"""`lego` — deterministic command surface for Manus LEGO.

Exit codes are part of the contract:

* ``0`` success / all gates passing
* ``1`` verification failure (a gate failed)
* ``2`` configuration or usage error
* ``3`` blocked: a human authorization or a missing artifact prevents progress
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import catalog_engine, compose, gates, security, traceability
from .config import ConfigBundle, ConfigError, load_configuration
from .evidence import build_manifest, git_commit, utc_now, write_json
from .paths import RepoPaths, RepositoryNotFound, repo_paths

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2
EXIT_BLOCKED = 3


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _emit(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False))


def _load_bundle(paths: RepoPaths) -> ConfigBundle:
    bundle = load_configuration(paths)
    if bundle.problems:
        raise ConfigError(bundle.problems)
    return bundle


def _junit_map(values: list[str]) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ConfigError([f"--junit expects label=path, received '{value}'"])
        label, raw_path = value.split("=", 1)
        mapping[label.strip()] = Path(raw_path).expanduser()
    return mapping


def _run_pytest_suite(root: Path, label: str, targets: list[str], junit: Path) -> dict[str, Any]:
    existing = [target for target in targets if (root / target).exists()]
    if not existing:
        return {"label": label, "state": "skipped", "reason": "no test targets present", "targets": targets}
    junit.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", *existing, f"--junitxml={junit}", "-q"],
        cwd=root,
        check=False,
    )
    return {
        "label": label,
        "state": "passed" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "junit": junit.as_posix(),
        "targets": existing,
    }


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_discover(paths: RepoPaths, args: argparse.Namespace) -> int:
    bundle = _load_bundle(paths)
    index = catalog_engine.load_index(paths)
    counts: dict[str, int] = {}
    for entry in index.get("templates", []):
        counts[entry.get("provider", "unknown")] = counts.get(entry.get("provider", "unknown"), 0) + 1

    sources = [
        {
            "id": source.id,
            "provider": source.provider,
            "repository": source.repository,
            "url": source.url,
            "trust": source.trust,
            "license_posture": source.license_posture,
            "role": source.role,
            "indexed_templates": counts.get(source.provider, 0),
            "reviewed_by": source.reviewed_by,
            "reviewed_at": source.reviewed_at,
        }
        for source in bundle.sources.sources
    ]

    payload: dict[str, Any] = {
        "command": "discover",
        "sources": sources,
        "rejected_sources": [source.model_dump() for source in bundle.sources.rejected_sources],
        "policy": bundle.sources.policy.model_dump(),
        "catalog_coverage": index.get("coverage"),
        "template_count": index.get("template_count", 0),
        "network_checked": False,
        "note": "Discovery is metadata-only. Candidate code is never executed or cloned.",
    }

    if args.check:
        payload["network_checked"] = True
        payload["reachability"] = _check_reachability(sources, bundle)

    _emit(payload)
    return EXIT_OK


def _check_reachability(sources: list[dict[str, Any]], bundle: ConfigBundle) -> list[dict[str, Any]]:
    import urllib.error
    import urllib.request

    allowed = set(bundle.security.network.allowed_hosts)
    results: list[dict[str, Any]] = []
    for source in sources:
        url = str(source["url"])
        host = url.split("//", 1)[-1].split("/", 1)[0]
        if host not in allowed:
            results.append({"id": source["id"], "state": "refused", "reason": f"host not allowlisted: {host}"})
            continue
        try:
            request = urllib.request.Request(  # noqa: S310 - allowlisted https only
                url, method="HEAD", headers={"User-Agent": "Manus-Lego-Discover/1.0"}
            )
            with urllib.request.urlopen(request, timeout=10) as response:  # noqa: S310 - allowlisted https only
                results.append({"id": source["id"], "state": "reachable", "status": response.status})
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            results.append({"id": source["id"], "state": "unreachable", "reason": str(exc)})
    return results


def cmd_inspect(paths: RepoPaths, args: argparse.Namespace) -> int:
    manifests = catalog_engine.load_manifests(paths)
    manifest = manifests.get(args.template_id) or catalog_engine.find_manifest(paths, args.template_id)
    if manifest is None:
        _emit(
            {
                "command": "inspect",
                "id": args.template_id,
                "found": False,
                "hint": "Run `lego select` or `lego index` first.",
            }
        )
        return EXIT_FAIL

    assessment = compose.assess_candidate(
        {"id": manifest.get("id"), "score": None, "commit": manifest.get("source", {}).get("commit")},
        manifest,
    )
    payload = {
        "command": "inspect",
        "found": True,
        "id": manifest.get("id"),
        "title": manifest.get("title"),
        "provider": manifest.get("provider"),
        "status": manifest.get("status"),
        "description": manifest.get("description"),
        "source": manifest.get("source"),
        "inventory": {
            "complete": manifest.get("inventory", {}).get("complete"),
            "file_count": manifest.get("inventory", {}).get("file_count"),
            "metadata_paths": manifest.get("inventory", {}).get("metadata_paths"),
        },
        "stack": manifest.get("stack"),
        "license": manifest.get("license"),
        "provenance": manifest.get("provenance"),
        "warnings": manifest.get("warnings", []),
        "reuse_readiness": {"decision": assessment["decision"], "blockers": assessment["blockers"]},
    }
    if args.files:
        payload["files"] = [item.get("path") for item in manifest.get("inventory", {}).get("files", [])][: args.limit]
    _emit(payload)
    return EXIT_OK


def cmd_index(paths: RepoPaths, args: argparse.Namespace) -> int:
    result = catalog_engine.index(
        paths,
        offline=args.offline,
        refresh=args.refresh,
        gallery=args.gallery,
        max_enrich=args.max_enrich,
        max_pages=args.max_pages,
        max_templates=args.max_templates,
        pause=args.pause,
    )
    _emit({"command": "index", **result})
    return EXIT_OK


def cmd_select(paths: RepoPaths, args: argparse.Namespace) -> int:
    selection = catalog_engine.plan(paths, args.query, provider=args.provider, limit=args.limit)
    manifests = catalog_engine.load_manifests(paths)
    annotated = []
    for candidate in selection.get("candidates", []):
        assessment = compose.assess_candidate(candidate, manifests.get(candidate.get("id", "")))
        annotated.append({**candidate, "blockers": assessment["blockers"], "decision": assessment["decision"]})
    selection["candidates"] = annotated
    write_json(paths.selection_plan, selection)
    _emit(
        {
            "command": "select",
            "plan": paths.selection_plan.relative_to(paths.root).as_posix(),
            "status": selection.get("status"),
            "candidates": [
                {"id": item["id"], "score": item["score"], "decision": item["decision"], "blockers": item["blockers"]}
                for item in annotated
            ],
        }
    )
    return EXIT_OK


def cmd_compose(paths: RepoPaths, args: argparse.Namespace) -> int:
    if args.query:
        selection = catalog_engine.plan(paths, args.query, provider=args.provider, limit=args.limit)
    elif paths.selection_plan.is_file():
        selection = compose.load_plan(paths.selection_plan)
    else:
        raise ConfigError(['no selection plan found; run `lego select "<query>"` or pass a query'])

    plan = compose.build_plan(paths, selection)
    compose.write_plan(paths, plan)
    _emit(
        {
            "command": "compose",
            "plan": paths.compose_plan.relative_to(paths.root).as_posix(),
            "status": plan["status"],
            "summary": plan["summary"],
            "blocked_candidates": [
                {"id": item["id"], "blockers": item["blockers"]}
                for item in plan["candidates"]
                if item["decision"] == "blocked"
            ],
        }
    )
    return EXIT_BLOCKED if plan["status"] == "blocked" else EXIT_OK


def cmd_verify(paths: RepoPaths, args: argparse.Namespace) -> int:
    _load_bundle(paths)
    junit = _junit_map(args.junit)
    runs: list[dict[str, Any]] = []

    if args.run_tests:
        suites = {
            "unit": ["services/orchestrator/tests", "tests/unit"],
            "integration": ["tests/integration"],
            "security": ["tests/security"],
            "evaluations": ["services/rag/tests"],
        }
        reports_dir = paths.root / "reports" / "junit"
        for label, targets in suites.items():
            junit_path = reports_dir / f"{label}.xml"
            run = _run_pytest_suite(paths.root, label, targets, junit_path)
            runs.append(run)
            if run["state"] != "skipped":
                junit[label] = junit_path

    commit = git_commit(paths.root)
    report = gates.evaluate(paths, commit=commit, environment=args.environment, junit_paths=junit)
    written = gates.write_report(paths, report)

    _emit(
        {
            "command": "verify",
            "overall": report.overall,
            "commit": commit,
            "gates": [{"id": gate.id, "status": gate.status, "detail": gate.detail} for gate in report.gates],
            "runs": runs,
            "evidence": written["json"],
        }
    )
    return EXIT_FAIL if report.overall == "fail" else EXIT_BLOCKED if report.overall == "blocked" else EXIT_OK


def cmd_report(paths: RepoPaths, args: argparse.Namespace) -> int:
    junit = _junit_map(args.junit)
    commit = git_commit(paths.root)
    report = traceability.build_report(paths, commit=commit, generated_at=utc_now(), junit_paths=junit)
    written = traceability.write_report(paths, report)
    manifest = build_manifest(paths, commit=commit, producer="lego report")
    manifest_artifact = write_json(paths.evidence_manifest, manifest)

    _emit(
        {
            "command": "report",
            "commit": commit,
            "summary": report.summary,
            "traceability": written,
            "manifest": manifest_artifact.as_dict(),
            "artifacts": manifest["artifact_count"],
        }
    )
    return EXIT_OK


def cmd_config(paths: RepoPaths, args: argparse.Namespace) -> int:
    bundle = load_configuration(paths)
    if args.config_action == "show":
        _emit(
            {
                "command": "config show",
                "valid": bundle.valid,
                "team": bundle.team.team.model_dump() if bundle.team else None,
                "agents": [agent.id for agent in bundle.team.agents] if bundle.team else [],
                "gates": [gate.id for gate in bundle.manus.gates] if bundle.manus else [],
                "problems": bundle.problems,
            }
        )
        return EXIT_OK if bundle.valid else EXIT_USAGE

    _emit(
        {
            "command": "config validate",
            "valid": bundle.valid,
            "problems": bundle.problems,
            "checked": [
                "config/manus.yaml",
                "config/security.yaml",
                "config/TEAMSCHEMA.yaml",
                "config/sources.yaml",
                "agents/registry.yaml",
            ],
        }
    )
    return EXIT_OK if bundle.valid else EXIT_USAGE


def cmd_catalog(paths: RepoPaths, args: argparse.Namespace) -> int:
    if args.catalog_action == "validate":
        verdict = catalog_engine.validate_catalog(paths)
        _emit({"command": "catalog validate", **verdict})
        return EXIT_OK if verdict.get("valid") else EXIT_FAIL
    raise ConfigError([f"unknown catalog action: {args.catalog_action}"])


def cmd_trace(paths: RepoPaths, args: argparse.Namespace) -> int:
    file = traceability.load_requirements(paths)
    markers = traceability.discover_test_markers(paths.root)
    by_requirement: dict[str, list[str]] = {}
    for marker in markers:
        for requirement_id in marker.requirement_ids:
            by_requirement.setdefault(requirement_id, []).append(f"{marker.file}::{marker.name}")

    rows = []
    for requirement in file.requirements:
        rows.append(
            {
                "id": requirement.id,
                "practice": requirement.practice,
                "title": requirement.title,
                "implementation": [item for item in requirement.implementation if (paths.root / item).exists()],
                "missing_implementation": [
                    item for item in requirement.implementation if not (paths.root / item).exists()
                ],
                "tests": sorted(by_requirement.get(requirement.id, [])),
                "evidence": requirement.evidence,
            }
        )
    _emit({"command": "trace", "requirements": rows, "count": len(rows)})
    return EXIT_OK


def cmd_security(paths: RepoPaths, args: argparse.Namespace) -> int:
    bundle = _load_bundle(paths)
    policy = bundle.security
    findings = security.scan_for_secrets(
        paths,
        [(pattern.name, pattern.regex) for pattern in policy.secrets.scan.patterns],
        policy.secrets.scan.allowlist_paths,
    )
    _emit(
        {
            "command": "security scan",
            "findings": [finding.as_dict() for finding in findings],
            "clean": not findings,
            "patterns": [pattern.name for pattern in policy.secrets.scan.patterns],
            "scope": "git ls-files (tracked files only)",
        }
    )
    return EXIT_OK if not findings else EXIT_FAIL


# --------------------------------------------------------------------------- #
# Parser
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lego",
        description="Manus LEGO orchestrator: catalog discovery, composition planning, gates and traceability.",
    )
    parser.add_argument("--root", help="Repository root (defaults to auto-detection)")
    sub = parser.add_subparsers(dest="command", required=True)

    discover = sub.add_parser("discover", help="List allowlisted sources and their review state")
    discover.add_argument("--check", action="store_true", help="Verify source reachability (network)")
    discover.set_defaults(func=cmd_discover)

    inspect = sub.add_parser("inspect", help="Inspect a template record and its reuse readiness")
    inspect.add_argument("template_id")
    inspect.add_argument("--files", action="store_true", help="List inspected file paths")
    inspect.add_argument("--limit", type=int, default=50)
    inspect.set_defaults(func=cmd_inspect)

    index = sub.add_parser("index", help="Refresh the public reference index (network, read-only)")
    index.add_argument("--offline", action="store_true")
    index.add_argument("--refresh", action="store_true")
    index.add_argument("--gallery", action="store_true")
    index.add_argument("--max-enrich", type=int, default=25)
    index.add_argument("--max-pages", type=int, default=100)
    index.add_argument("--max-templates", type=int, default=None)
    index.add_argument("--pause", type=float, default=0.1)
    index.set_defaults(func=cmd_index)

    select = sub.add_parser("select", help="Rank candidates and write a selection proposal")
    select.add_argument("query")
    select.add_argument("--provider", choices=["all", "cloudflare", "vercel"], default="all")
    select.add_argument("--limit", type=int, default=5)
    select.set_defaults(func=cmd_select)

    compose_cmd = sub.add_parser("compose", help="Turn a proposal into an integration plan with explicit blockers")
    compose_cmd.add_argument("query", nargs="?")
    compose_cmd.add_argument("--provider", choices=["all", "cloudflare", "vercel"], default="all")
    compose_cmd.add_argument("--limit", type=int, default=5)
    compose_cmd.set_defaults(func=cmd_compose)

    verify = sub.add_parser("verify", help="Evaluate quality gates from produced artifacts")
    verify.add_argument("--junit", action="append", default=[], metavar="LABEL=PATH")
    verify.add_argument("--run-tests", action="store_true", help="Run the Python suites and capture JUnit XML")
    verify.add_argument("--environment", default="local")
    verify.set_defaults(func=cmd_verify)

    report = sub.add_parser("report", help="Emit the requirement traceability report and evidence manifest")
    report.add_argument("--junit", action="append", default=[], metavar="LABEL=PATH")
    report.set_defaults(func=cmd_report)

    config = sub.add_parser("config", help="Validate or inspect configuration")
    config_sub = config.add_subparsers(dest="config_action", required=True)
    config_sub.add_parser("validate", help="Validate every configuration file and cross-file rule")
    config_sub.add_parser("show", help="Print the effective team, agents and gates")
    config.set_defaults(func=cmd_config)

    catalog = sub.add_parser("catalog", help="Catalog maintenance")
    catalog_sub = catalog.add_subparsers(dest="catalog_action", required=True)
    catalog_sub.add_parser("validate", help="Validate manifest provenance and completeness claims")
    catalog.set_defaults(func=cmd_catalog)

    trace = sub.add_parser("trace", help="Show requirement → implementation → test links")
    trace.set_defaults(func=cmd_trace)

    sec = sub.add_parser("security", help="Security utilities")
    sec_sub = sec.add_subparsers(dest="security_action", required=True)
    sec_sub.add_parser("scan", help="Scan tracked files for credential patterns")
    sec.set_defaults(func=cmd_security)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        paths = repo_paths(args.root)
    except RepositoryNotFound as exc:
        print(json.dumps({"error": "repository_not_found", "detail": str(exc)}), file=sys.stderr)
        return EXIT_USAGE

    try:
        return int(args.func(paths, args))
    except ConfigError as exc:
        print(json.dumps({"error": "configuration_invalid", "problems": exc.problems}, indent=2), file=sys.stderr)
        return EXIT_USAGE
    except catalog_engine.EngineError as exc:
        print(
            json.dumps({"error": "catalog_engine_failed", "detail": str(exc), "stderr": exc.stderr[:2000]}),
            file=sys.stderr,
        )
        return EXIT_FAIL
    except FileNotFoundError as exc:
        print(json.dumps({"error": "missing_artifact", "detail": str(exc)}), file=sys.stderr)
        return EXIT_BLOCKED


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
