# Operations runbook

**Service owner:** orchestrator (single accountable owner).
**Human approval authority:** repository owner (see `docs/evidence/approvals/`).
**On-call:** this is a single-owner project; the owner is the on-call engineer. Escalation
is "open an issue and mention the owner" — there is no pager, and this document does not
pretend otherwise.

## 1. Everyday commands

| Task | Command |
|---|---|
| Install JS dependencies | `pnpm install --frozen-lockfile` |
| Install a Python service | `uv sync --project services/orchestrator` (or `services/rag`) |
| Install optional Lang integrations | `uv sync --project services/orchestrator --group lang` (LangGraph, LangChain, LangSmith, MCP, Deep Agents) |
| Full local verification | `pnpm exec turbo run lint typecheck build test` |
| Gate evaluation | `uv run --project services/orchestrator lego verify --run-tests` |
| Traceability + evidence manifest | `uv run --project services/orchestrator lego report` |
| Catalog validity | `uv run --project services/orchestrator lego catalog validate` |
| Secret scan | `uv run --project services/orchestrator lego security scan` |
| Retrieval evaluation | `uv run --project services/rag lego-rag eval services/rag/tests/fixtures/evaluation.json` |
| Local stack | `docker compose -f infrastructure/docker/compose.yaml up --build` |

## 2. Health and signals

The API exposes `GET /health` (liveness + catalog state) and `GET /api/v1/meta`
(commit, artifact mtimes). Both return the standard envelope, so a probe should check
`data.status == "ok"` rather than an HTTP 200 alone.

Signals worth alerting on, and why:

| Signal | Threshold | Why it matters |
|---|---|---|
| `http_requests_total{status=5xx}` | > 1% for 5 min | The API only reads files; a 5xx means a broken artifact or a bug |
| `http_request_duration_seconds{p95}` | > 0.5 s | Catalog loads are in-memory and mtime-cached |
| `api_rate_limited_total` | spike | Either abuse or a client that ignores `Retry-After` |
| `catalog_artifact_age_seconds` | > 7 days | A stale catalog means `catalog-refresh.yml` is failing silently |
| `gate_status{gate="G0..G6"}` | any `fail` | A control regressed |
| `rag_refusal_rate` | > 0.5 | Retrieval broke, or the corpus changed under the questions |
| `rag_guardrail_findings_total` | any increase | Someone is publishing instruction-shaped content |

The metric names above are the contract that `infrastructure/monitoring/` configures; the
services emit logs and (where configured) OTLP traces. See
`infrastructure/monitoring/README.md` for the mapping and for what is *not* instrumented.

## 3. Deploy

1. Merge to `main` only with a green `ci.yml` and `security.yml` run.
2. `release.yml` builds images tagged with the commit SHA, generates an SBOM, attests
   provenance and waits on the protected `production` environment.
3. Record the approval: write `docs/evidence/approvals/<yyyy-mm-dd>-<sha7>.json` with
   `commit`, `approver`, `scope`, `decision: approved`, `expires_at`. G6 turns green only
   for that commit.
4. Deploy the tagged digest, not `latest`.
5. Verify `GET /health` returns `data.catalog_loaded == true` and that `/api/v1/meta`
   reports the expected commit.

## 4. Rollback

Images are immutable and tagged by commit, so rollback is a redeploy of the previous tag:

```bash
docker pull ghcr.io/loopappdev/manus-lego-api:<previous-sha>
docker compose -f infrastructure/docker/compose.yaml up -d --no-deps api
```

Verify health, then record the rollback in the incident register below. Do not revert the
approval file: it authorises a commit, and the history of what was approved must survive.

## 5. Incident response

1. **Contain.** For a credential leak: revoke the credential first, then rotate. For a bad
   release: roll back before investigating.
2. **Assess.** Which artifacts are affected? Check `docs/evidence/evidence-manifest.json`
   for the digests of what shipped.
3. **Record.** Add a row to the register below within one working day.
4. **Fix.** Land the fix with a test that would have caught it. If no test can catch it,
   say so in the register instead of implying coverage.
5. **Close.** Record the commit that fixed it and the date.

## 6. Vulnerability register

Severity follows CVSS v3.1 bands. SLAs are calendar days from triage to a fix in `main`.

| Severity | SLA | Decision maker | Notes |
|---|---|---|---|
| Critical | 2 days | repository owner | Stop feature work; rotate any exposed credential immediately |
| High | 7 days | repository owner | Mitigate or document a compensating control |
| Medium | 30 days | orchestrator | Bundle with the next change |
| Low | 90 days | orchestrator | Track, fix opportunistically |

| ID | Date | Severity | Component | Summary | Decision | Fix commit | Closed |
|---|---|---|---|---|---|---|---|
| VULN-0001 | 2026-11-20 | Low | `config/security.yaml` | The `cloudflare_token` pattern matched any 40-character string followed by a dot, producing false positives in vendored files | Tightened to require the variable name as an anchor | (this change) | 2026-11-20 |
| VULN-0002 | 2026-11-20 | Medium | `services/orchestrator/catalog_engine.py` | `--output` was passed after the engine subcommand, so every engine call exited 2 with empty stdout | Moved the global flag before the subcommand; guarded by a unit test | (this change) | 2026-11-20 |
| VULN-0003 | 2026-11-20 | High | `.github/workflows/release.yml` | A step name containing `(G6 included: ...)` was unquoted, so the file was not valid YAML and GitHub would have rejected the entire release workflow — every release control in it would silently not exist | Quoted the step name; added a test that parses every workflow as YAML | (this change) | 2026-11-20 |
| VULN-0004 | 2026-11-20 | Medium | `services/orchestrator/cli.py` | `lego verify --run-tests` inherited the child pytest stdout, so the JSON gate report was not parseable exactly in the mode that produces it | Captured the child output and forwarded it to stderr; regression test pins stdout purity | (this change) | 2026-11-20 |
| VULN-0005 | 2026-11-20 | Medium | `config/security.yaml`, `tests/unit/test_secret_scan.py` | The secret scan allowlisted `**/*.md`, hiding any credential pasted into documentation; the scan's own fixture also contained a literal credential-shaped string that flagged the repository once the test file was tracked | Allowlist scoped to `tests/security/**`; fixture assembled at runtime | (this change) | 2026-11-20 |

The entries above are real defects found while building and testing this work: one by the
test suite, one by the CLI refusing to be parsed, one by a lint pass and one by committing
the tests. They are recorded rather than quietly fixed, because a register that is always
empty is not evidence of anything.

## 7. Known limitations

- The rate limiter is in-process; it does not coordinate across replicas.
- Dependency review cannot run on this repository: the dependency graph and GitHub Advanced
  Security are not available, so the compare API returns 403. The job probes first and reports
  the control as absent rather than failing red forever. Enabling it is a repository setting,
  not a code change.
- The retrieval embedder is a deterministic hashing stand-in, not a semantic model.
- Container images are not signed, and no admission controller enforces the hardening.
- Evidence files are produced locally and uploaded by CI; they are not committed on every
  run, so a stale `docs/evidence/gates.json` can lag behind `main`.
| Install optional Lang integrations | `uv sync --project services/orchestrator --group lang` (LangGraph, LangChain, LangSmith, MCP and Deep Agents) |
