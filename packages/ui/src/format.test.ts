import { describe, expect, it } from 'vitest';
import { coverageNote, formatDate, gateLabel, shortCommit, statusExplanation, statusLabel, toneForStatus } from './format.js';

describe('provenance presentation', () => {
  it('never presents an unverified template as validated', () => {
    expect(statusLabel('discovered_unverified')).toBe('Discovered · unverified');
    expect(statusExplanation('discovered_unverified')).toContain('no pinned commit');
  });

  it('maps statuses to a consistent tone', () => {
    expect(toneForStatus('enriched')).toBe('positive');
    expect(toneForStatus('reference_only')).toBe('warning');
    expect(toneForStatus('fail')).toBe('danger');
    expect(toneForStatus('unknown-value')).toBe('neutral');
  });

  it('renders gate states in readable form', () => {
    expect(gateLabel('not_evaluated')).toBe('Not evaluated');
    expect(gateLabel('blocked')).toBe('Blocked');
  });
});

describe('formatting', () => {
  it('marks missing commits instead of implying a pin', () => {
    expect(shortCommit(null)).toBe('unpinned');
    expect(shortCommit('0123456789abcdef')).toBe('0123456');
  });

  it('handles missing or invalid timestamps', () => {
    expect(formatDate(null)).toBe('not recorded');
    expect(formatDate('not-a-date')).toBe('invalid date');
    expect(formatDate('2026-11-20T10:00:00Z')).toContain('2026');
  });

  it('always states partial coverage explicitly', () => {
    expect(coverageNote('partial_or_unverified')).toContain('partial');
    expect(coverageNote('complete')).toContain('complete');
  });
});
