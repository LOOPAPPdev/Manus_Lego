import type { CatalogEntry, CatalogIndex } from '@lego/schemas';

/**
 * Deterministic lexical ranking.
 *
 * This is a faithful port of `ranked()` / `name_words()` in
 * `scripts/lego_catalog.py`. The catalog engine stays the single
 * implementation of record; this port exists so the read-only API can answer
 * search queries without shelling out to Python. Parity is asserted against a
 * shared fixture generated from the Python implementation
 * (`tests/fixtures/ranking-cases.json`), so drift fails CI.
 *
 * Weights: title 5, tags 4, features 3, path 2, framework 1.
 */
export const RANKING_WEIGHTS = { title: 5, tags: 4, features: 3, path: 2, framework: 1 } as const;

const STOPWORDS = new Set(['with', 'from', 'this', 'that', 'template', 'example', 'starter']);

export function nameWords(input: string): Set<string> {
  const matches = input.toLowerCase().match(/[a-z][a-z0-9-]{1,}/g) ?? [];
  const words = new Set<string>();
  for (const word of matches) {
    if (!STOPWORDS.has(word)) {
      words.add(word);
    }
  }
  return words;
}

function intersectionSize(a: Set<string>, b: Set<string>): number {
  let count = 0;
  for (const item of a) {
    if (b.has(item)) {
      count += 1;
    }
  }
  return count;
}

export interface RankedEntry extends CatalogEntry {
  score: number;
}

export function scoreEntry(entry: CatalogEntry, wanted: Set<string>): number {
  return (
    RANKING_WEIGHTS.title * intersectionSize(wanted, nameWords(entry.title)) +
    RANKING_WEIGHTS.tags * intersectionSize(wanted, nameWords(entry.tags.join(' '))) +
    RANKING_WEIGHTS.features * intersectionSize(wanted, nameWords(entry.features.join(' '))) +
    RANKING_WEIGHTS.path * intersectionSize(wanted, nameWords(entry.path)) +
    RANKING_WEIGHTS.framework * intersectionSize(wanted, nameWords(entry.stack.frameworks.join(' ')))
  );
}

export function rankTemplates(
  index: Pick<CatalogIndex, 'templates'>,
  query: string,
  options: { provider?: 'all' | 'cloudflare' | 'vercel'; limit?: number } = {},
): RankedEntry[] {
  const provider = options.provider ?? 'all';
  const limit = options.limit ?? 10;
  const wanted = nameWords(query);
  const hits: RankedEntry[] = [];

  for (const entry of index.templates) {
    if (provider !== 'all' && entry.provider !== provider) {
      continue;
    }
    const score = scoreEntry(entry, wanted);
    if (score > 0) {
      hits.push({ ...entry, score });
    }
  }

  return hits.sort((a, b) => (b.score - a.score) || a.id.localeCompare(b.id)).slice(0, limit);
}
