import { mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { loadManusConfig, ManusConfigSchema } from './config.js';
import { redact } from './logger.js';
import { findRepoRoot, repoPaths } from './paths.js';
import { sha256, stableStringify, writeJsonArtifact } from './evidence.js';

describe('repository paths', () => {
  it('locates the monorepo root from a nested directory', () => {
    const root = findRepoRoot();
    expect(repoPaths(root).catalogIndex.endsWith('catalog/index.json')).toBe(true);
  });
});

describe('configuration', () => {
  it('loads and validates config/manus.yaml', () => {
    const { config } = loadManusConfig();
    expect(config.project.owner).toBe('orchestrator');
    expect(config.api.read_only).toBe(true);
    expect(config.gates.map((gate) => gate.id)).toEqual(['G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6']);
  });

  it('rejects a configuration without gates', () => {
    const result = ManusConfigSchema.safeParse({ schema_version: '1.0' });
    expect(result.success).toBe(false);
  });
});

describe('logger redaction', () => {
  it('removes credential-shaped fields at any depth', () => {
    const redacted = redact({
      GITHUB_TOKEN: 'ghp_example',
      nested: { authorization: 'Bearer abc', safe: 'value' },
    }) as Record<string, unknown>;
    expect(redacted.GITHUB_TOKEN).toBe('[redacted]');
    expect((redacted.nested as Record<string, unknown>).authorization).toBe('[redacted]');
    expect((redacted.nested as Record<string, unknown>).safe).toBe('value');
  });
});

describe('evidence artifacts', () => {
  it('writes stable JSON with a digest that matches the bytes on disk', () => {
    const dir = mkdtempSync(join(tmpdir(), 'lego-evidence-'));
    const path = join(dir, 'nested', 'report.json');
    const artifact = writeJsonArtifact(path, { b: 2, a: 1 });
    expect(readFileSync(path, 'utf8')).toBe(`${stableStringify({ a: 1, b: 2 })}\n`);
    expect(artifact.sha256).toBe(sha256(readFileSync(path)));
    expect(artifact.bytes).toBeGreaterThan(0);
  });
});
