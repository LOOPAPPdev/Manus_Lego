import { useEffect, useState } from 'react';
import { Badge } from '@lego/ui';
import { api, type ProjectMeta } from '../api.js';

export function AboutPage() {
  const [meta, setMeta] = useState<ProjectMeta | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    void api.meta(controller.signal).then((result) => {
      if (result.ok) {
        setMeta(result.envelope.data);
      }
    });
    return () => controller.abort();
  }, []);

  return (
    <div className="page">
      <h1>What this catalog is, and what it is not</h1>

      <div className="columns">
        <section className="panel">
          <h2>Purpose</h2>
          <p>
            Manus LEGO turns a plain-language application goal into a traceable selection of reusable public components. It records
            references — provider, repository, pinned commit, inspected paths — so an engineer can evaluate a template before copying
            anything into a project.
          </p>
          <p>
            It is a reference inventory, not a code mirror. Source files are never vendored, executed or bulk-imported during
            indexing.
          </p>
        </section>

        <section className="panel">
          <h2>Explicit limits</h2>
          <ul>
            <li>
              <strong>Enriched ≠ verified.</strong> An enriched record means metadata was parsed at a commit. It does not mean the
              template builds, deploys or is secure.
            </li>
            <li>
              <strong>Coverage is partial.</strong> The Vercel gallery has no exhaustive public index; Cloudflare templates are
              curated but change upstream.
            </li>
            <li>
              <strong>No automatic reuse.</strong> Selection produces a proposal. Integration requires an adapter plan, license review
              and tests.
            </li>
          </ul>
        </section>
      </div>

      {meta ? (
        <>
          <section className="panel">
            <h2>Project</h2>
            <dl className="definitions">
              <dt>Owner</dt>
              <dd>{meta.project.owner}</dd>
              <dt>Repository</dt>
              <dd className="mono">{meta.project.repository}</dd>
              <dt>Default branch</dt>
              <dd className="mono">{meta.project.default_branch}</dd>
              <dt>API posture</dt>
              <dd>
                <Badge tone={meta.read_only ? 'positive' : 'danger'}>{meta.read_only ? 'read-only' : 'writable'}</Badge>
              </dd>
              <dt>Runtime</dt>
              <dd>
                Node {meta.runtime.node} · Python {meta.runtime.python} · {meta.runtime.package_manager}
              </dd>
            </dl>
          </section>

          <section className="panel">
            <h2>Deterministic commands</h2>
            <table className="table">
              <thead>
                <tr>
                  <th scope="col">Command</th>
                  <th scope="col">Purpose</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(meta.commands).map(([name, command]) => (
                  <tr key={name}>
                    <td className="mono">{command}</td>
                    <td>{DESCRIPTIONS[name] ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          <section className="panel">
            <h2>Gates</h2>
            <table className="table">
              <thead>
                <tr>
                  <th scope="col">Gate</th>
                  <th scope="col">Name</th>
                  <th scope="col">Owner</th>
                  <th scope="col">Blocking</th>
                </tr>
              </thead>
              <tbody>
                {meta.gates.map((gate) => (
                  <tr key={gate.id}>
                    <td className="mono">{gate.id}</td>
                    <td>{gate.name}</td>
                    <td className="mono small">{gate.owner}</td>
                    <td>{gate.blocking ? 'yes' : 'no'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </>
      ) : null}
    </div>
  );
}

const DESCRIPTIONS: Record<string, string> = {
  discover: 'List allowlisted sources and their review state.',
  inspect: 'Inspect one template record and its provenance in detail.',
  index: 'Refresh the public reference index (network, read-only).',
  select: 'Rank candidates for a requirement and write a proposal.',
  compose: 'Turn a proposal into an integration plan with explicit blockers.',
  verify: 'Evaluate quality gates from produced artifacts.',
  report: 'Emit the traceability and evidence reports.',
};
