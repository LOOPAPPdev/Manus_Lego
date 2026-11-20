import { useEffect, useState } from 'react';
import { Badge, StatusBadge, statusExplanation } from '@lego/ui';
import { api, type TemplateDetail } from '../api.js';
import { ErrorNotice, Hint, Loading } from '../components/Feedback.js';

export function TemplatePage({ id }: { id: string }) {
  const [template, setTemplate] = useState<TemplateDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    void api.template(id, controller.signal).then((result) => {
      if (controller.signal.aborted) return;
      if (result.ok) {
        setTemplate(result.envelope.data);
        setError(null);
      } else {
        setError(result.message);
      }
      setLoading(false);
    });
    return () => controller.abort();
  }, [id]);

  if (loading) {
    return <Loading label="Loading template" />;
  }

  if (error || !template) {
    return (
      <div className="page">
        <a className="link" href="#/">
          ← Back to catalog
        </a>
        <ErrorNotice message={error ?? 'Template not found.'} />
      </div>
    );
  }

  const reuseBlockers = [
    template.commit ? null : 'No pinned commit: provenance cannot be reproduced.',
    template.license.status === 'needs_review' ? 'License not reviewed: copying code is not permitted.' : null,
    template.inventory.complete ? null : 'File inventory incomplete: the template may contain paths not inspected.',
    template.status === 'discovered_unverified' ? 'Discovery-only record: no manifest or README inspection.' : null,
  ].filter((item): item is string => item !== null);

  return (
    <div className="page">
      <a className="link" href="#/">
        ← Back to catalog
      </a>

      <header className="detail-header">
        <div>
          <h1>{template.title}</h1>
          <p className="lede">{template.description}</p>
          <div className="badges">
            <Badge tone="accent">{template.provider}</Badge>
            <StatusBadge status={template.status} />
            <Badge tone={template.commit ? 'positive' : 'warning'}>
              {template.commit ? template.commit.slice(0, 7) : 'unpinned'}
            </Badge>
            <Badge tone={template.inventory.complete ? 'positive' : 'warning'}>
              {template.inventory.complete ? 'inventory complete' : 'inventory partial'}
            </Badge>
          </div>
        </div>
        <div className="detail-actions">
          <a className="button" href={template.source_url} target="_blank" rel="noreferrer noopener">
            Open source
          </a>
          <a className="button button--ghost" href={template.catalog_url} target="_blank" rel="noreferrer noopener">
            Provider page
          </a>
        </div>
      </header>

      <p className="muted small">{statusExplanation(template.status)}</p>

      {reuseBlockers.length > 0 ? (
        <div className="notice notice--warning">
          <strong>Not ready to integrate.</strong>
          <ul>
            {reuseBlockers.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ) : (
        <Hint>Gates G1–G3 have evidence for this record. Integration still requires a written adapter plan and tests.</Hint>
      )}

      <div className="columns">
        <section className="panel">
          <h2>Provenance</h2>
          <dl className="definitions">
            <dt>Repository</dt>
            <dd className="mono">{template.source.repository}</dd>
            <dt>Path</dt>
            <dd className="mono">{template.source.path}</dd>
            <dt>Commit</dt>
            <dd className="mono">{template.commit ?? 'not pinned'}</dd>
            <dt>Origin</dt>
            <dd>{template.provenance.origin}</dd>
            <dt>Feature basis</dt>
            <dd>{template.provenance.feature_basis}</dd>
            <dt>License</dt>
            <dd>
              {template.license.status}
              {template.license.file_path ? ` · ${template.license.file_path}` : ''}
            </dd>
          </dl>
        </section>

        <section className="panel">
          <h2>Stack</h2>
          <dl className="definitions">
            <dt>Languages</dt>
            <dd>{template.stack.languages.join(', ') || '—'}</dd>
            <dt>Frameworks</dt>
            <dd>{template.stack.frameworks.join(', ') || '—'}</dd>
            <dt>Products</dt>
            <dd>{template.stack.products.join(', ') || '—'}</dd>
            <dt>Bindings</dt>
            <dd>{template.stack.bindings.join(', ') || '—'}</dd>
            <dt>Package manager</dt>
            <dd>{template.stack.package_manager}</dd>
          </dl>
        </section>
      </div>

      {Object.keys(template.commands).length > 0 ? (
        <section className="panel">
          <h2>Declared commands</h2>
          <p className="muted small">Copied from the template manifest. Not executed by this system.</p>
          <table className="table">
            <thead>
              <tr>
                <th scope="col">Script</th>
                <th scope="col">Command</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(template.commands).map(([name, command]) => (
                <tr key={name}>
                  <td className="mono">{name}</td>
                  <td className="mono small">{command}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ) : null}

      <section className="panel">
        <h2>
          Inspected files <span className="muted">· {template.inventory.file_count}</span>
        </h2>
        {template.inventory.files.length > 0 ? (
          <ul className="filelist">
            {template.inventory.files.slice(0, 200).map((file) => (
              <li key={file.path} className="mono small">
                {file.path}
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted">
            No file inventory was recorded. This record came from provider metadata only, so no path-level reuse decision can be made
            yet.
          </p>
        )}
      </section>

      {template.warnings.length > 0 ? (
        <section className="panel panel--warning">
          <h2>Warnings</h2>
          <ul>
            {template.warnings.map((warning) => (
              <li key={warning}>{warning}</li>
            ))}
          </ul>
        </section>
      ) : null}

      {template.related.length > 0 ? (
        <section className="panel">
          <h2>Related references</h2>
          <ul className="related">
            {template.related.map((item) => (
              <li key={item.id}>
                <a className="link" href={`#/template/${encodeURIComponent(item.id)}`}>
                  {item.title}
                </a>
                <span className="muted small"> · score {item.score}</span>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </div>
  );
}
