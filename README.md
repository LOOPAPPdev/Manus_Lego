# Manus LEGO — agentic template catalog and engineering foundation

Use Cloudflare and Vercel templates as reusable **references** without cloning every source
repository. Manus selects a minimal set of inspected components for the current project, and
the governance layer records *why* a template was chosen, at which commit, under which
license. Repo: [`LOOPAPPdev/Manus_Lego`](https://github.com/LOOPAPPdev/Manus_Lego).

> **This repository is not a certification.** It implements controls that map to NIST
> SP 800-218 practices and states, per control, what is implemented, what is partial and
> what is absent. See [`docs/nist-mapping.md`](docs/nist-mapping.md).

## Start in 3 steps

```bash
# A · Generate the source inventory (requires internet access)
export GITHUB_TOKEN=...  # optional GitHub token; never commit it
python3 scripts/lego_catalog.py index --gallery --max-enrich 30 --max-pages 100

# B · Verify and search the manifests
python3 -m unittest discover -s tests -v
python3 scripts/lego_catalog.py validate
python3 scripts/lego_catalog.py search "react authentication database" --limit 10

# C · Create a read-only integration proposal
python3 scripts/lego_catalog.py plan "react authentication database" --limit 5
```

In Claude Code, use `/agenteorchsenior build a BPMS dashboard using Cloudflare` and then
`/lego react database auth`. Claude Code project skills live at
`.claude/skills/agenteorchsenior/SKILL.md` and `.claude/skills/lego/SKILL.md`; these are
**not Python shell commands**. The Python executable is `scripts/lego_catalog.py`.

## Engineering foundation

The catalog engine is wrapped by a monorepo that adds contracts, a governance CLI, a
read-only API, a catalog explorer and a permissioned retrieval service.

```
apps/
  api/            Fastify, read-only HTTP API over the catalog and the evidence artifacts
  web/            React + Vite catalog explorer (search, detail, governance pages)
packages/
  schemas/        zod contracts shared by the API, the web app and the tests
  shared/         paths, config, redacted logger, evidence hashing, ranking port
  ui/             presentational components and formatting helpers
services/
  orchestrator/   `lego` CLI: gates, traceability, composition, security scan
  rag/            `lego-rag`: permissioned retrieval with citations, guardrails and eval
scripts/          lego_catalog.py (stdlib only) and the orchestration wrapper
catalog/          42 template manifests, index, sources, selection and compose plans
config/           project, security, team and source configuration (validated)
agents/           six agent contracts plus the runtime registry
workflows/        executable entry points: discover, retrieve, execute, verify
docs/             specification, decisions, threat model, runbook, evidence
tests/            unit, integration, security and evaluation suites
infrastructure/   containers, compose, Cloudflare Pages config, observability
```

The JavaScript side is a **pnpm workspace driven by Turborepo**; each Python service is an
**independent uv project** with its own lockfile. Rationale:
[ADR 0002](docs/decisions/0002-pnpm-and-turborepo.md),
[ADR 0003](docs/decisions/0003-isolated-python-services.md).

```bash
pnpm install --frozen-lockfile
pnpm exec turbo run lint typecheck build test      # 20 tasks, one command

uv sync --project services/orchestrator
uv sync --project services/rag

docker compose -f infrastructure/docker/compose.yaml up --build
# web → http://localhost:8080   api → http://localhost:8787/health
```

### The `lego` CLI

```bash
uv run --project services/orchestrator lego discover              # allowlisted sources
uv run --project services/orchestrator lego inspect <template-id> # provenance + blockers
uv run --project services/orchestrator lego index --offline       # refresh the index
uv run --project services/orchestrator lego select "workers api"  # ranked proposal
uv run --project services/orchestrator lego compose "workers api" # plan with blockers
uv run --project services/orchestrator lego verify --run-tests    # evaluate G0–G6
uv run --project services/orchestrator lego report                # traceability + manifest
```

`select` and `compose` never authorise a copy. `compose` defaults to **blocked** and lists
what is missing: a pinned commit, a reviewed license, a complete file inventory. No flag
turns a blocked plan into an approved one — approval is a pull request.

### Gates and evidence

| Gate | Question it answers | Artifact it reads |
|---|---|---|
| G0 | Is the specification complete and traceable? | `docs/specifications/` |
| G1 | Is every catalog record's provenance pinned? | `catalog/index.json`, `catalog/sources.json` |
| G2 | Do the contracts, manifests and decisions agree? | `schemas/`, `docs/decisions/` |
| G3 | Any secrets? Any agent with excess permission? | `config/`, tracked files |
| G4 | Do the unit tests pass? | JUnit XML |
| G5 | Do integration and security tests pass, and do the operational docs exist? | JUnit XML, `docs/` |
| G6 | Has a human authorised **this commit**? | `docs/evidence/approvals/` |

Statuses are `pass`, `fail`, `not_evaluated` and `blocked`. **`not_evaluated` is never
treated as a pass**, and G6 stays `blocked` until an approval record names the current
commit — see [the approval format](docs/evidence/approvals/README.md) and
[ADR 0008](docs/decisions/0008-gates-and-evidence.md).

`lego report` links each requirement to the tests that name it. A requirement becomes
`verified` only when a linked test **passed** in the executed suite; otherwise it is
`partial` or `unverified`. Deleting a test degrades the claim instead of hiding it.

```bash
cat docs/evidence/gates.md                # human-readable gate report
cat docs/evidence/traceability.md         # requirement → implementation → test → evidence
cat docs/evidence/evidence-manifest.json  # SHA-256 per artifact, for this commit
```

### Coverage: `enriched` ≠ `verified`

Each manifest carries a `status`: `discovered_unverified` (a URL exists in a public listing;
nothing was inspected), `enriched` (README, file tree and license were read and the commit is
pinned), or `reference_only` (metadata only). The index also reports **partial coverage**: the
Vercel gallery is paginated and the Cloudflare seed list is not exhaustive, so "42 templates"
means "42 templates this engine could observe". A listing says nothing about whether a
template's code is safe to reuse.

### Security posture

Read-only API by construction (no write route exists), security headers, per-client rate
limit, CORS allowlist, zod-validated input. Containers are multi-stage, digest-pinned,
non-root, read-only and capability-dropped. CI actions are pinned to commit SHAs with minimal
permissions; Dependabot covers npm, GitHub Actions and both uv projects; CodeQL and Trivy run
on pull requests and weekly. Threat model with residual risk:
[`docs/security/threat-model.md`](docs/security/threat-model.md).

## One Python command for Manus orchestration

```bash
# One call: run offline tests, refresh public sources, rank and create a LEGO plan
python3 scripts/agenteorchsenior.py pipeline "react authentication database" --max-enrich 30 --max-pages 100

# Work without internet: verify existing references and prepare a proposal
python3 scripts/agenteorchsenior.py check
python3 scripts/agenteorchsenior.py select "react authentication database"
```

The Python command is a **deterministic pipeline**, not an AI agent SDK. Manus must read
`AGENTS.md` and invoke the script using its own permitted execution mechanism; Claude Code
recognizes the two project slash-command skills. A plan **never authorizes** source import, a
production deployment, or credential changes. If remote sources fail, `pipeline` exits
nonzero and does not describe an inventory as complete.

## Current bootstrap inventory

This delivery includes **41 curated Cloudflare template names** from official
`cloudflare/templates/templates.json` and **one Vercel Astro Blog reference**. Most of these
42 records remain *discovery-only*: they have no pinned commit, full source tree or complete
dependency analysis. The `index` command upgrades entries when GitHub API access is
available. Regenerate the initial seed with `python3 scripts/bootstrap_catalog.py`
(overwrites existing catalog data, so use only for a fresh bootstrap).

## Source inventory

- [Cloudflare Workers templates](https://github.com/cloudflare/templates) including official
  `templates.json`, README, `package.json`, Cloudflare product metadata and paths.
- [Vercel examples](https://github.com/vercel/examples) and the public
  [Vercel gallery](https://vercel.com/templates); the gallery includes external GitHub
  repositories not mirrored inside `vercel/examples`.
- Read-only reference links with pinned Git SHA. Scripts and source code are **never executed
  or bulk imported** during indexing.

## Files

| Location | Meaning |
|---|---|
| `catalog/sources.json` | Provider entrypoints and discovery rules |
| `catalog/index.json` | Cross-provider compact search index |
| `catalog/master_index.csv` | Spreadsheet-ready inventory |
| `catalog/templates/<provider>/*.json` | Per-template file tree, README, package scripts, product metadata |
| `catalog/vercel_gallery_links.json` | Public Vercel gallery page-to-GitHub references |
| `schemas/template.schema.json` | Template data contract |
| `scripts/lego_catalog.py` | Pure-Python API indexer + query + plan + validate |
| `scripts/agenteorchsenior.py` | Single-entry Python orchestration wrapper for Manus |
| `config/`, `agents/` | Team schema, security policy, agent contracts and registry |
| `services/orchestrator/` | `lego` CLI: gates, traceability, composition, secret scan |
| `services/rag/` | `lego-rag`: ACL-filtered retrieval, guardrails, evaluation |
| `apps/`, `packages/` | Read-only API, catalog explorer, shared contracts and components |
| `tests/` | Offline unit, integration, security and evaluation suites |
| `.claude/skills/` | `/agenteorchsenior` and `/lego` workflows |
| `.github/workflows/` | CI, security scanning, release, and the manual catalog refresh via PR |

## Execution stages

`spec → discover → pin source SHA → inspect metadata → cross-reference tags → rank →
license/security gate → test → integrate minimal paths → PR → authorized deployment`.

## Documentation

| Document | Contents |
|---|---|
| [`docs/specifications/requirements.md`](docs/specifications/requirements.md) | 17 EARS-style requirements with acceptance criteria |
| [`docs/specifications/traceability.yaml`](docs/specifications/traceability.yaml) | requirement → implementation → evidence |
| [`docs/architecture.mmd`](docs/architecture.mmd) | architecture and trust boundaries |
| [`docs/decisions/`](docs/decisions) | eight ADRs, including the branch reconciliation |
| [`docs/security/threat-model.md`](docs/security/threat-model.md) | assets, trust boundaries, threats, residual risk |
| [`docs/operations/runbook.md`](docs/operations/runbook.md) | commands, signals, deploy, rollback, vulnerability register |
| [`docs/quality/testing-strategy.md`](docs/quality/testing-strategy.md) | test layers and the gaps that are not covered |
| [`docs/nist-mapping.md`](docs/nist-mapping.md) | practice-by-practice coverage, with what is missing |
| [`docs/pipeline.md`](docs/pipeline.md) | the original catalog pipeline notes |

## Branch history

This branch reconciles the two prior feature branches rather than choosing one:
`feat/integrated-master-index` (catalog plus 36 scout reports) and
`feat/manus-lego-catalog` (engine plus manifests). The merge commit keeps both histories
reachable — see [ADR 0001](docs/decisions/0001-reconcile-feature-branches.md).

## Evidence and limitations

A status of `enriched` means the README/config/package files were parsed, **not** that a
runtime deployment was tested. The catalog does not claim complete coverage of Vercel's
dynamically paginated marketplace. If GitHub truncates a repository tree, the output is
explicitly partial. If the internet is unavailable, indexing reports errors instead of
inventing results. CI never deploys applications and requires review to merge a catalog
refresh.

On the engineering foundation specifically:

- No component tests for the web app; it builds and its formatting helpers are tested.
- The retrieval embedder is a deterministic hashing stand-in, and its evaluation numbers
  describe five synthetic documents.
- The release workflow has never run against a registry: SBOM, signing and provenance are
  written configuration, not observed behaviour.
- Container images are not signed, and nothing enforces the hardening at deploy time.
- The rate limiter is per process, and the metric names in the alert rules are not yet
  emitted by the services.
- One human owner, so design and code review are self-review with a written record; the
  control that replaces a second reviewer is the commit-scoped approval record.

See [`docs/pipeline.md`](docs/pipeline.md) for acceptance tests, safeguards and gates.

## Credits and license

This catalog stores links and minimal metadata. External templates retain their own licenses;
review them before reuse. Senior Engineering Partner is a separately supplied third-party
skill and is not redistributed here.
