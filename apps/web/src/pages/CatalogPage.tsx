import { useEffect, useMemo, useRef, useState } from 'react';
import { CoverageBanner, EmptyState, Stat, StatusBadge, TemplateCard } from '@lego/ui';
import { api, type CatalogEntry, type CatalogSummary } from '../api.js';
import { ErrorNotice, Loading } from '../components/Feedback.js';

const PAGE_SIZE = 12;

export function CatalogPage() {
  const [summary, setSummary] = useState<CatalogSummary | null>(null);
  const [items, setItems] = useState<CatalogEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [query, setQuery] = useState('');
  const [debounced, setDebounced] = useState('');
  const [provider, setProvider] = useState('all');
  const [status, setStatus] = useState('all');
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebounced(query.trim()), 250);
    return () => window.clearTimeout(timer);
  }, [query]);

  useEffect(() => {
    setOffset(0);
  }, [debounced, provider, status]);

  useEffect(() => {
    const controller = new AbortController();
    void api.summary(controller.signal).then((result) => {
      if (result.ok) {
        setSummary(result.envelope.data);
      } else if (result.status !== 0) {
        setError(result.message);
      } else {
        setError(result.message);
      }
    });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    setLoading(true);

    void api
      .templates({ q: debounced, provider, status, limit: PAGE_SIZE, offset, sort: debounced ? 'relevance' : 'title' }, controller.signal)
      .then((result) => {
        if (controller.signal.aborted) return;
        if (result.ok) {
          setItems(result.envelope.data.items);
          setTotal(result.envelope.data.total);
          setError(null);
        } else {
          setError(result.message);
        }
        setLoading(false);
      });

    return () => controller.abort();
  }, [debounced, provider, status, offset]);

  const statusOptions = useMemo(() => ['all', ...Object.keys(summary?.statuses ?? {})], [summary]);

  return (
    <div className="page">
      <section className="hero">
        <div>
          <h1>Reference catalog for Cloudflare and Vercel templates</h1>
          <p className="lede">
            Select the smallest reusable set of components, pinned to a commit, before writing application code. Every record states
            what was inspected — and what was not.
          </p>
        </div>
        {summary ? (
          <div className="stats">
            <Stat label="Templates" value={summary.template_count} hint="indexed records" />
            <Stat label="Providers" value={summary.providers.length} hint="source monorepos" />
            <Stat
              label="Pinned commits"
              value={summary.providers.reduce((sum, item) => sum + item.pinned, 0)}
              hint="reuse requires a pin"
            />
          </div>
        ) : null}
      </section>

      {summary ? <CoverageBanner coverage={summary.coverage} lastModified={summary.last_modified} /> : null}

      <section className="controls" aria-label="Catalog filters">
        <label className="field field--grow">
          <span className="field__label">Search</span>
          <input
            className="input"
            type="search"
            value={query}
            placeholder="react authentication database"
            onChange={(event) => setQuery(event.target.value)}
            aria-describedby="search-hint"
          />
          <span id="search-hint" className="field__hint">
            Deterministic lexical scoring: title 5 · tags 4 · features 3 · path 2 · framework 1
          </span>
        </label>
        <label className="field">
          <span className="field__label">Provider</span>
          <select className="input" value={provider} onChange={(event) => setProvider(event.target.value)}>
            <option value="all">All providers</option>
            <option value="cloudflare">Cloudflare</option>
            <option value="vercel">Vercel</option>
          </select>
        </label>
        <label className="field">
          <span className="field__label">Provenance</span>
          <select className="input" value={status} onChange={(event) => setStatus(event.target.value)}>
            {statusOptions.map((option) => (
              <option key={option} value={option}>
                {option === 'all' ? 'Any status' : option.replace(/_/g, ' ')}
              </option>
            ))}
          </select>
        </label>
      </section>

      {error ? <ErrorNotice message={error} /> : null}

      <section aria-live="polite" aria-busy={loading}>
        <div className="results-header">
          <h2>
            {debounced ? `Results for “${debounced}”` : 'All indexed templates'}
            <span className="muted"> · {total} records</span>
          </h2>
          {total > PAGE_SIZE ? (
            <div className="pager">
              <button className="button" onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))} disabled={offset === 0}>
                Previous
              </button>
              <span className="muted small">
                {offset + 1}–{Math.min(offset + PAGE_SIZE, total)}
              </span>
              <button
                className="button"
                onClick={() => setOffset(offset + PAGE_SIZE)}
                disabled={offset + PAGE_SIZE >= total}
              >
                Next
              </button>
            </div>
          ) : null}
        </div>

        {loading && items.length === 0 ? <Loading label="Loading catalog" /> : null}

        {!loading && items.length === 0 && !error ? (
          <EmptyState title="No template matches those filters">
            The index is partial by design. Try a broader query, or run <code>lego index</code> to refresh from public sources.
          </EmptyState>
        ) : null}

        <div className="grid">
          {items.map((item) => (
            <TemplateCard
              key={item.id}
              template={item}
              onSelect={(id) => {
                window.location.hash = `#/template/${encodeURIComponent(id)}`;
              }}
            />
          ))}
        </div>
      </section>

      {summary ? (
        <section className="panel">
          <h2>Source status</h2>
          <p className="muted small">
            Reported by the indexer. A source in an error state means coverage is <strong>not</strong> complete for that provider.
          </p>
          <table className="table">
            <thead>
              <tr>
                <th scope="col">Provider</th>
                <th scope="col">Repository / source</th>
                <th scope="col">State</th>
                <th scope="col">Commit</th>
              </tr>
            </thead>
            <tbody>
              {summary.source_status.map((source, index) => (
                <tr key={`${String(source.provider)}-${index}`}>
                  <td>{String(source.provider)}</td>
                  <td className="mono small">{String(source.repo ?? source.source ?? '—')}</td>
                  <td>
                    <StatusBadge status={String(source.state)} />
                  </td>
                  <td className="mono small">{source.commit ? String(source.commit).slice(0, 7) : 'unpinned'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ) : null}
    </div>
  );
}
