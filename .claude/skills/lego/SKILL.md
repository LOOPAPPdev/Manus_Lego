---
name: lego
description: Find and combine verified template building blocks by catalog ID, Git path and pinned commit. Prepare a minimal reuse plan without bulk import or uncontrolled code execution.
argument-hint: "<required features, framework and runtime>"
---
# /lego — Reference-first component composer

Input: `$ARGUMENTS` or the current project requirements. Use only read-only operations until integration gates pass.

## Read → Match → Verify → Plan
1. Read `catalog/index.json` and `docs/pipeline.md`.
2. Run `python3 scripts/lego_catalog.py search "<keywords>" --limit 10`.
3. Run `python3 scripts/lego_catalog.py plan "<keywords>" --limit 5`. This writes `catalog/selection_plan.json`, **not project source code**.
4. Filter by required runtime, language, frameworks, platform bindings, license, auth, storage, dependencies and source stability. Report mismatches.
5. Cross-reference exact repository/path/commit with metadata. If a catalog record is `discovered_unverified` or `reference_only`, inspect source before recommending integration.
6. Select either one full starter or the smallest importable subset. Record the per-file origin and license, and verify its runtime dependencies.
7. Define integration contracts, tests and fallback. Human approval is required for production deployment, secrets, purchase, or destructive changes.

## Contract
Output a JSON plan shaped as `catalog/selection_plan.json`. Describe `required_capabilities`, `matched_catalog_ids`, `source_pins`, `files_to_reuse`, `dependencies`, `conflicts`, `license_result`, `tests`, `risks`, `uncovered_requirements` and `ready_to_integrate`.

Never clone all source repositories merely to inventory metadata. Never blindly concatenate incompatible stacks or assume a deployment is no-code. Follow `AGENTS.md` and the senior orchestrator before modifying code.
