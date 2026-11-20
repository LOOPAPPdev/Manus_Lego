# Observability

Three signals, one rule: if an alert fires, the runbook must already say what to do.

## Mapping

| Signal | Emitted by | Sink | Used for |
|---|---|---|---|
| **Logs** | `packages/shared/src/logger.ts` (JSON lines, redacted), Python `logging` | stdout → collector (OTLP) → your log store | Debugging a single request; `request_id` correlates the API envelope with the log line |
| **Metrics** | API counters/histograms (`http_requests_total`, `http_request_duration_seconds_bucket`, `catalog_artifact_mtime_seconds`), gate status gauge, RAG refusal rate and guardrail counter | OTLP → collector → Prometheus endpoint on `:8889` | The alerts in `prometheus/alerts.yml` |
| **Traces** | OTLP spans from the API (Fastify hooks) and the Python services | collector → `debug` exporter by default | Latency attribution; disabled unless `OTEL_EXPORTER_OTLP_ENDPOINT` is set |
| **Alerts** | Prometheus rules | Alertmanager (not configured here) | Paging is manual: this is a single-owner project |

## Honest gaps

1. **The metric names in `alerts.yml` are a contract, not an observation.** The API emits
   structured logs and honours OTLP configuration, but the Prometheus client library is not
   wired into the service in this branch. `http_requests_total` therefore will not exist
   until that instrumentation is added — the alert rules are written so that adding the
   client satisfies them, and this note exists so nobody believes a green dashboard.
2. **No Alertmanager, no paging.** Alerts are evaluated by Prometheus and go nowhere.
3. **No dashboards as code.** Grafana JSON is not committed; building dashboards against
   metric names that do not exist yet would be fiction.
4. **The RAG service is a batch CLI.** Its "metrics" are the numbers printed by
   `lego-rag eval`; the `rag_*` series require a wrapper that exports them.
5. **Log volume is unbounded.** No sampling, no retention policy.

## Running locally

```bash
# Collector (OTLP 4317/4318, Prometheus scrape target 8889, health 13133)
docker run --rm -p 4317:4317 -p 4318:4318 -p 8889:8889 -p 13133:13133 \
  -v "$PWD/infrastructure/monitoring/otel-collector.yaml:/etc/otelcol/config.yaml" \
  otel/opentelemetry-collector-contrib:0.115.1

# Point the services at it
export OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318
export OTEL_SERVICE_NAME=manus-lego-api
```

`infrastructure/monitoring/prometheus/alerts.yml` is validated by `promtool check rules`
in CI when `promtool` is available; the repository does not install it by default, so a
syntax error would be caught at deploy time rather than at review time. That is a known gap,
listed here rather than hidden.
