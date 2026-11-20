# Manus LEGO — Agentic Template Reference Catalog

**Purpose:** use Cloudflare and Vercel templates as reusable *references* without cloning all source repositories. Manus selects a minimal set of tested components for the current project. Repo: [`LOOPAPPdev/Manus_Lego`](https://github.com/LOOPAPPdev/Manus_Lego).

## Start in 3 steps

```bash
# A · Generate source inventory (requires internet access)
export GITHUB_TOKEN=...  # optional GitHub token; never commit it
python3 scripts/lego_catalog.py index --gallery --max-enrich 30 --max-pages 100

# B · Verify and search the manifests
python3 -m unittest discover -s tests -v
python3 scripts/lego_catalog.py validate
python3 scripts/lego_catalog.py search "react authentication database" --limit 10

# C · Create a read-only integration proposal
python3 scripts/lego_catalog.py plan "react authentication database" --limit 5
```

In Claude Code, use `/agenteorchsenior build a BPMS dashboard using Cloudflare` and then `/lego react database auth`. Claude Code project skills live at `.claude/skills/agenteorchsenior/SKILL.md` and `.claude/skills/lego/SKILL.md`; these are **not Python shell commands**. The Python executable is `scripts/lego_catalog.py`.


## One Python command for Manus orchestration

```bash
# One call: run offline tests, refresh public sources, rank and create a LEGO plan
python3 scripts/agenteorchsenior.py pipeline "react authentication database" --max-enrich 30 --max-pages 100

# Work without internet: verify existing references and prepare a proposal
python3 scripts/agenteorchsenior.py check
python3 scripts/agenteorchsenior.py select "react authentication database"
```

The Python command is a **deterministic pipeline**, not an AI agent SDK. Manus must read `AGENTS.md` and invoke the script using its own permitted execution mechanism; Claude Code recognizes the two project slash-command skills. A plan **never authorizes** source import, a production deployment, or credential changes. If remote sources fail, `pipeline` exits nonzero and does not describe an inventory as complete.

## Current bootstrap inventory
This delivery includes **41 curated Cloudflare template names** from official `cloudflare/templates/templates.json` and **one Vercel Astro Blog reference**. These 42 records are *discovery-only* and have no pinned commit, full source tree or complete dependency analysis yet. The `index` command upgrades entries when GitHub API access is available. Regenerate the initial seed with `python3 scripts/bootstrap_catalog.py` (overwrites existing catalog data, so use only for a fresh bootstrap).

## Source inventory
- [Cloudflare Workers templates](https://github.com/cloudflare/templates) including official `templates.json`, README, `package.json`, Cloudflare product metadata and paths.
- [Vercel examples](https://github.com/vercel/examples) and public [Vercel gallery](https://vercel.com/templates); the gallery includes external GitHub repositories not mirrored inside `vercel/examples`.
- Read-only reference links with pinned Git SHA. Scripts and source code are **never executed or bulk imported** during indexing.

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
| `tests/` | Offline unit and end-to-end fixture tests |
| `.claude/skills/` | `/agenteorchsenior` and `/lego` workflows |
| `.github/workflows/catalog-refresh.yml` | Manual GitHub Actions refresh via PR |

## Execution stages
`spec → discover → pin source SHA → inspect metadata → cross-reference tags → rank → license/security gate → test → integrate minimal paths → PR → authorized deployment`.

## Evidence and limitations
A status of `enriched` means the README/config/package files were parsed, **not** that a runtime deployment was tested. The catalog does not claim complete coverage of Vercel's dynamically paginated marketplace. If GitHub truncates a repository tree, the output is explicitly partial. If internet is unavailable, indexing reports errors instead of inventing results. CI never deploys applications and requires review to merge a catalog refresh.

See [`docs/pipeline.md`](docs/pipeline.md) for acceptance tests, safeguards and gates.

## Credits and license
This catalog stores links and minimal metadata. External templates retain their own licenses; review them before reuse. Senior Engineering Partner is a separately supplied third-party skill and is not redistributed here.
