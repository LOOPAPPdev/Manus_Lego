import type { ReactNode } from 'react';
import { coverageNote, formatCount, formatDate, gateLabel, shortCommit, statusExplanation, statusLabel, toneForStatus } from './format.js';

export interface BadgeProps {
  children: ReactNode;
  tone?: 'positive' | 'warning' | 'danger' | 'neutral' | 'accent';
  title?: string;
}

export function Badge({ children, tone = 'neutral', title }: BadgeProps) {
  return (
    <span className={`badge badge--${tone}`} title={title}>
      {children}
    </span>
  );
}

export interface StatusBadgeProps {
  status: string;
  withExplanation?: boolean;
}

export function StatusBadge({ status, withExplanation = false }: StatusBadgeProps) {
  return (
    <Badge tone={toneForStatus(status)} title={withExplanation ? statusExplanation(status) : undefined}>
      {statusLabel(status)}
    </Badge>
  );
}

export function ProviderBadge({ provider }: { provider: string }) {
  return <Badge tone="accent">{provider}</Badge>;
}

export interface TemplateCardData {
  id: string;
  title: string;
  description: string;
  provider: string;
  status: string;
  tags: string[];
  features: string[];
  stack: { languages: string[]; frameworks: string[]; products: string[] };
  commit: string | null;
  source_url: string;
  score?: number;
}

export interface TemplateCardProps {
  template: TemplateCardData;
  onSelect?: (id: string) => void;
}

export function TemplateCard({ template, onSelect }: TemplateCardProps) {
  const interactive = typeof onSelect === 'function';
  return (
    <article
      className={`card${interactive ? ' card--interactive' : ''}`}
      onClick={interactive ? () => onSelect(template.id) : undefined}
      onKeyDown={
        interactive
          ? (event) => {
              if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                onSelect(template.id);
              }
            }
          : undefined
      }
      role={interactive ? 'button' : undefined}
      tabIndex={interactive ? 0 : undefined}
    >
      <header className="card__header">
        <h3 className="card__title">{template.title}</h3>
        {typeof template.score === 'number' ? <span className="card__score">score {template.score}</span> : null}
      </header>
      <div className="card__badges">
        <ProviderBadge provider={template.provider} />
        <StatusBadge status={template.status} />
        <Badge tone={template.commit ? 'positive' : 'warning'} title="A pinned commit is required before reuse">
          {shortCommit(template.commit)}
        </Badge>
      </div>
      <p className="card__description">{template.description}</p>
      {template.stack.frameworks.length > 0 || template.stack.languages.length > 0 ? (
        <p className="card__meta">
          <strong>Stack</strong>{' '}
          {[...new Set([...template.stack.frameworks, ...template.stack.languages])].join(', ')}
        </p>
      ) : null}
      {template.tags.length > 0 ? (
        <p className="card__tags">
          {template.tags.slice(0, 8).map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </p>
      ) : null}
      <footer className="card__footer">
        <a
          className="link"
          href={template.source_url}
          target="_blank"
          rel="noreferrer noopener"
          onClick={(event) => event.stopPropagation()}
        >
          View pinned source
        </a>
      </footer>
    </article>
  );
}

export interface GateLike {
  id: string;
  name: string;
  status: string;
  detail: string;
  evidence: string[];
}

export function GateTable({ gates }: { gates: GateLike[] }) {
  if (gates.length === 0) {
    return <p className="muted">No gate report has been generated for this commit.</p>;
  }
  return (
    <table className="table">
      <thead>
        <tr>
          <th scope="col">Gate</th>
          <th scope="col">Name</th>
          <th scope="col">Status</th>
          <th scope="col">Evidence</th>
        </tr>
      </thead>
      <tbody>
        {gates.map((gate) => (
          <tr key={gate.id}>
            <td className="mono">{gate.id}</td>
            <td>
              {gate.name}
              <div className="muted small">{gate.detail}</div>
            </td>
            <td>
              <Badge tone={toneForStatus(gate.status)}>{gateLabel(gate.status)}</Badge>
            </td>
            <td className="mono small">{gate.evidence.length > 0 ? gate.evidence.join(', ') : '—'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export interface RequirementLike {
  id: string;
  title: string;
  practice: string;
  status: string;
  tests: Array<{ name: string; outcome: string }>;
  evidence: string[];
}

export function RequirementTable({ requirements }: { requirements: RequirementLike[] }) {
  if (requirements.length === 0) {
    return <p className="muted">No traceability report has been generated for this commit.</p>;
  }
  return (
    <table className="table">
      <thead>
        <tr>
          <th scope="col">Requirement</th>
          <th scope="col">SSDF</th>
          <th scope="col">Status</th>
          <th scope="col">Tests</th>
        </tr>
      </thead>
      <tbody>
        {requirements.map((requirement) => {
          const passed = requirement.tests.filter((test) => test.outcome === 'passed').length;
          return (
            <tr key={requirement.id}>
              <td>
                <span className="mono">{requirement.id}</span>
                <div className="small">{requirement.title}</div>
              </td>
              <td className="mono">{requirement.practice}</td>
              <td>
                <Badge tone={toneForStatus(requirement.status)}>{requirement.status}</Badge>
              </td>
              <td className="small">
                {requirement.tests.length > 0 ? `${passed}/${requirement.tests.length} passing` : 'no test linked'}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export interface StatProps {
  label: string;
  value: number | string;
  hint?: string;
}

export function Stat({ label, value, hint }: StatProps) {
  return (
    <div className="stat">
      <span className="stat__label">{label}</span>
      <span className="stat__value">{typeof value === 'number' ? formatCount(value) : value}</span>
      {hint ? <span className="stat__hint">{hint}</span> : null}
    </div>
  );
}

export function CoverageBanner({ coverage, lastModified }: { coverage: string; lastModified?: string | null }) {
  return (
    <div className="banner" role="note">
      <strong>Coverage disclaimer.</strong> {coverageNote(coverage)} Last index change: {formatDate(lastModified)}.
    </div>
  );
}

export function EmptyState({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="empty">
      <h3>{title}</h3>
      {children ? <p className="muted">{children}</p> : null}
    </div>
  );
}
