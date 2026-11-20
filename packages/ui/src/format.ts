/**
 * Presentation helpers. Kept free of React so they can be unit-tested in a plain
 * Node environment and reused by any renderer.
 */

export type TemplateStatus = 'discovered_unverified' | 'reference_only' | 'enriched';
export type GateStatus = 'pass' | 'fail' | 'blocked' | 'not_evaluated';

const STATUS_LABELS: Record<TemplateStatus, string> = {
  discovered_unverified: 'Discovered · unverified',
  reference_only: 'Reference only',
  enriched: 'Enriched metadata',
};

const STATUS_EXPLANATIONS: Record<TemplateStatus, string> = {
  discovered_unverified: 'Listed by the provider; no pinned commit or file inventory inspected.',
  reference_only: 'Metadata inspected at a pinned commit; runtime behaviour not executed.',
  enriched: 'README and manifest parsed at a pinned commit; still not a runtime guarantee.',
};

const GATE_LABELS: Record<GateStatus, string> = {
  pass: 'Pass',
  fail: 'Fail',
  blocked: 'Blocked',
  not_evaluated: 'Not evaluated',
};

export function statusLabel(status: string): string {
  return STATUS_LABELS[status as TemplateStatus] ?? status;
}

export function statusExplanation(status: string): string {
  return STATUS_EXPLANATIONS[status as TemplateStatus] ?? 'Unknown provenance state.';
}

export function gateLabel(status: string): string {
  return GATE_LABELS[status as GateStatus] ?? status;
}

export function toneForStatus(status: string): 'positive' | 'warning' | 'danger' | 'neutral' {
  if (status === 'enriched' || status === 'pass' || status === 'verified') {
    return 'positive';
  }
  if (status === 'reference_only' || status === 'partial' || status === 'not_evaluated' || status === 'blocked') {
    return 'warning';
  }
  if (status === 'fail' || status === 'failing') {
    return 'danger';
  }
  return 'neutral';
}

export function formatCount(value: number): string {
  return new Intl.NumberFormat('en-GB').format(value);
}

export function formatDate(iso: string | null | undefined): string {
  if (!iso) {
    return 'not recorded';
  }
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return 'invalid date';
  }
  return new Intl.DateTimeFormat('en-GB', { dateStyle: 'medium', timeStyle: 'short' }).format(date);
}

export function shortCommit(commit: string | null | undefined): string {
  if (!commit) {
    return 'unpinned';
  }
  return commit.slice(0, 7);
}

/** Human-readable coverage warning used wherever counts are shown. */
export function coverageNote(coverage: string): string {
  if (coverage.includes('partial') || coverage.includes('unverified')) {
    return 'Coverage is partial. Counts describe what was inspected, not what exists.';
  }
  return 'Coverage reported as complete by the index producer.';
}
