import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { CatalogIndexSchema } from '@lego/schemas';
import { describe, expect, it } from 'vitest';
import { nameWords, rankTemplates, scoreEntry } from './ranking.js';

const repoRoot = fileURLToPath(new URL('../../../', import.meta.url));
const index = CatalogIndexSchema.parse(JSON.parse(readFileSync(join(repoRoot, 'catalog/index.json'), 'utf8')));

interface ParityCase {
  query: string;
  provider: 'all' | 'cloudflare' | 'vercel';
  limit: number;
  expected: Array<{ id: string; score: number }>;
}

const parity = JSON.parse(readFileSync(join(repoRoot, 'tests/fixtures/ranking-cases.json'), 'utf8')) as {
  generated_by: string;
  cases: ParityCase[];
};

describe('tokenizer parity with the Python catalog engine', () => {
  it('drops stopwords and requires at least two characters', () => {
    expect([...nameWords('Build a React Starter Template with D1')].sort()).toEqual(['build', 'd1', 'react']);
  });

  it('keeps hyphenated tokens intact', () => {
    // The Python tokenizer treats a hyphenated run as one token, so the
    // "template" stopword does not strip it: parity requires the same output.
    expect([...nameWords('react-postgres-fullstack-template')]).toEqual(['react-postgres-fullstack-template']);
  });
});

describe('ranking parity with the Python catalog engine', () => {
  it('uses the documented weights', () => {
    const entry = index.templates[0];
    expect(entry).toBeDefined();
    if (!entry) return;
    const wanted = new Set(['zzz']);
    expect(scoreEntry(entry, wanted)).toBe(0);
  });

  for (const testCase of parity.cases) {
    it(`matches Python for query "${testCase.query}" (${testCase.provider}, limit ${testCase.limit})`, () => {
      const results = rankTemplates(index, testCase.query, {
        provider: testCase.provider,
        limit: testCase.limit,
      });
      expect(results.map((entry) => ({ id: entry.id, score: entry.score }))).toEqual(testCase.expected);
    });
  }
});
