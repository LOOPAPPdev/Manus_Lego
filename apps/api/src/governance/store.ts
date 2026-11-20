import { readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { GateReportSchema, TraceabilityReportSchema } from '@lego/schemas';
import type { GateReport, TraceabilityReport } from '@lego/schemas';
import type { Logger } from '@lego/shared';

/**
 * Reads the evidence produced by `lego verify` / `lego report`.
 *
 * Absent evidence is reported as absent. The API never synthesises a passing
 * gate, because a fabricated green gate is worse than a missing one.
 */
export interface GovernanceSnapshot {
  gates: GateReport | null;
  traceability: TraceabilityReport | null;
  loadedAt: string;
  available: boolean;
}

export class GovernanceStore {
  private readonly evidenceDir: string;
  private readonly logger: Logger;
  private cache: { key: string; snapshot: GovernanceSnapshot } | null = null;

  constructor(repoRoot: string, logger: Logger) {
    this.evidenceDir = join(repoRoot, 'docs', 'evidence');
    this.logger = logger;
  }

  private mtime(file: string): number {
    try {
      return statSync(join(this.evidenceDir, file)).mtimeMs;
    } catch {
      return 0;
    }
  }

  snapshot(): GovernanceSnapshot {
    const gatesMtime = this.mtime('gates.json');
    const traceMtime = this.mtime('traceability.json');
    const key = `${gatesMtime}:${traceMtime}`;

    if (this.cache && this.cache.key === key) {
      return this.cache.snapshot;
    }

    const snapshot: GovernanceSnapshot = {
      gates: this.read<GateReport>('gates.json', GateReportSchema),
      traceability: this.read<TraceabilityReport>('traceability.json', TraceabilityReportSchema),
      loadedAt: new Date().toISOString(),
      available: gatesMtime > 0 || traceMtime > 0,
    };

    this.cache = { key, snapshot };
    return snapshot;
  }

  private read<T>(file: string, schema: { safeParse: (value: unknown) => { success: boolean; data?: T } }): T | null {
    try {
      const raw = readFileSync(join(this.evidenceDir, file), 'utf8');
      const parsed = schema.safeParse(JSON.parse(raw));
      if (!parsed.success || !parsed.data) {
        this.logger.warn('evidence.invalid', { file });
        return null;
      }
      return parsed.data;
    } catch {
      return null;
    }
  }
}
