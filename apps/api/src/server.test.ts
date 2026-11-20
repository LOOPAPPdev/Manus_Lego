import { cpSync, mkdtempSync, mkdirSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterAll, describe, expect, it } from 'vitest';
import type { FastifyInstance } from 'fastify';
import { createLogger } from '@lego/shared';
import { buildServer } from './server.js';

const repoRoot = fileURLToPath(new URL('../../../', import.meta.url));
const silent = createLogger({ service: 'test', level: 'error', sink: () => {} });

const app: FastifyInstance = buildServer({ repoRoot, logger: silent, rateLimitPerMinute: 10_000 });
afterAll(async () => {
  await app.close();
});

describe('health and metadata', () => {
  it('reports readiness and catalog availability', async () => {
    const response = await app.inject({ method: 'GET', url: '/health' });
    expect(response.statusCode).toBe(200);
    const body = response.json();
    expect(body.data.status).toBe('ok');
    expect(body.data.catalog_loaded).toBe(true);
    expect(body.meta.request_id).toMatch(/^[0-9a-f-]{36}$/);
  });

  it('exposes the declarative gate definitions and read-only posture', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/meta' });
    expect(response.statusCode).toBe(200);
    const body = response.json();
    expect(body.data.read_only).toBe(true);
    expect(body.data.gates).toHaveLength(7);
    expect(Object.keys(body.data.commands)).toEqual(
      expect.arrayContaining(['discover', 'inspect', 'index', 'select', 'compose', 'verify', 'report']),
    );
  });
});

describe('catalog endpoints', () => {
  it('summarises providers and statuses consistently with the index', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/catalog/summary' });
    expect(response.statusCode).toBe(200);
    const summary = response.json().data;
    const providerTotal = summary.providers.reduce((sum: number, item: { count: number }) => sum + item.count, 0);
    expect(providerTotal).toBe(summary.template_count);
    expect(summary.template_count).toBeGreaterThan(0);
  });

  it('paginates templates and honours the provider filter', async () => {
    const first = await app.inject({ method: 'GET', url: '/api/v1/templates?limit=5&offset=0' });
    expect(first.statusCode).toBe(200);
    const page = first.json().data;
    expect(page.items).toHaveLength(5);
    expect(page.total).toBeGreaterThan(5);

    const cloudflare = await app.inject({ method: 'GET', url: '/api/v1/templates?provider=cloudflare&limit=100' });
    const cloudflarePage = cloudflare.json().data;
    expect(cloudflarePage.items.every((item: { provider: string }) => item.provider === 'cloudflare')).toBe(true);
  });

  it('returns a full manifest with related references for a known template', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/templates/cloudflare:seed:astro-blog-starter-template' });
    expect(response.statusCode).toBe(200);
    const template = response.json().data;
    expect(template.id).toBe('cloudflare:seed:astro-blog-starter-template');
    expect(template.source.repository).toBe('cloudflare/templates');
    expect(template.inventory).toBeDefined();
    expect(Array.isArray(template.related)).toBe(true);
  });

  it('returns a structured 404 for an unknown template', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/templates/cloudflare:seed:does-not-exist' });
    expect(response.statusCode).toBe(404);
    expect(response.json().error.code).toBe('NOT_FOUND');
    expect(response.json().error.request_id).toBeDefined();
  });

  it('rejects invalid pagination input instead of silently clamping', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/templates?limit=0' });
    expect(response.statusCode).toBe(400);
    expect(response.json().error.code).toBe('BAD_REQUEST');
  });

  it('ranks search results with the shared deterministic scorer', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/search?q=react%20authentication%20database&limit=3' });
    expect(response.statusCode).toBe(200);
    const body = response.json().data;
    expect(body.results.length).toBeGreaterThan(0);
    expect(body.results[0].id).toContain('react');
    const scores = body.results.map((item: { score: number }) => item.score);
    expect([...scores].sort((a: number, b: number) => b - a)).toEqual(scores);
  });

  it('requires a query for search', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/search' });
    expect(response.statusCode).toBe(400);
  });
});

describe('security posture', () => {
  it('refuses write methods because the API is read-only', async () => {
    const response = await app.inject({ method: 'POST', url: '/api/v1/templates' });
    expect(response.statusCode).toBe(400);
    expect(response.json().error.message).toContain('read-only');
  });

  it('sets hardening headers on every response', async () => {
    const response = await app.inject({ method: 'GET', url: '/health' });
    expect(response.headers['x-content-type-options']).toBe('nosniff');
    expect(response.headers['x-frame-options']).toBe('DENY');
    expect(response.headers['content-security-policy']).toContain("default-src 'none'");
  });

  it('only echoes CORS for configured origins', async () => {
    const allowed = await app.inject({
      method: 'GET',
      url: '/health',
      headers: { origin: 'http://localhost:5173' },
    });
    expect(allowed.headers['access-control-allow-origin']).toBe('http://localhost:5173');

    const denied = await app.inject({
      method: 'GET',
      url: '/health',
      headers: { origin: 'https://attacker.invalid' },
    });
    expect(denied.headers['access-control-allow-origin']).toBeUndefined();
  });

  it('answers preflight without exposing the catalog', async () => {
    const response = await app.inject({
      method: 'OPTIONS',
      url: '/api/v1/templates',
      headers: { origin: 'http://localhost:5173' },
    });
    expect(response.statusCode).toBe(204);
    expect(response.body).toBe('');
  });

  it('enforces the rate limit and advertises retry information', async () => {
    const limited = buildServer({ repoRoot, logger: silent, rateLimitPerMinute: 2 });
    try {
      const first = await limited.inject({ method: 'GET', url: '/health' });
      const second = await limited.inject({ method: 'GET', url: '/health' });
      const third = await limited.inject({ method: 'GET', url: '/health' });
      expect(first.statusCode).toBe(200);
      expect(second.statusCode).toBe(200);
      expect(third.statusCode).toBe(429);
      expect(third.json().error.code).toBe('RATE_LIMITED');
      expect(third.headers['retry-after']).toBeDefined();
    } finally {
      await limited.close();
    }
  });
});

describe('governance endpoints', () => {
  it('reports absent evidence instead of inventing a passing gate', async () => {
    const emptyRepo = mkdtempSync(join(tmpdir(), 'lego-empty-'));
    mkdirSync(join(emptyRepo, 'config'), { recursive: true });
    cpSync(join(repoRoot, 'config'), join(emptyRepo, 'config'), { recursive: true });
    cpSync(join(repoRoot, 'catalog'), join(emptyRepo, 'catalog'), { recursive: true });
    mkdirSync(join(emptyRepo, 'docs', 'evidence'), { recursive: true });

    const isolated = buildServer({ repoRoot: emptyRepo, logger: silent, rateLimitPerMinute: 100 });
    try {
      const response = await isolated.inject({ method: 'GET', url: '/api/v1/gates' });
      expect(response.statusCode).toBe(200);
      expect(response.json().data.available).toBe(false);
      expect(response.json().data.report).toBeNull();
      expect(response.json().data.hint).toContain('lego verify');
    } finally {
      await isolated.close();
    }
  });

  it('serves a valid evidence report when one exists', async () => {
    const fixtureRepo = mkdtempSync(join(tmpdir(), 'lego-evidence-'));
    cpSync(join(repoRoot, 'config'), join(fixtureRepo, 'config'), { recursive: true });
    cpSync(join(repoRoot, 'catalog'), join(fixtureRepo, 'catalog'), { recursive: true });
    mkdirSync(join(fixtureRepo, 'docs', 'evidence'), { recursive: true });
    writeFileSync(
      join(fixtureRepo, 'docs', 'evidence', 'gates.json'),
      JSON.stringify({
        schema_version: '1.0.0',
        generated_at: '2026-11-20T00:00:00Z',
        commit: 'deadbeef',
        environment: 'test',
        overall: 'fail',
        gates: [
          {
            id: 'G4',
            name: 'Tests written and failing before implementation',
            status: 'pass',
            detail: 'unit suite green',
            evidence: ['reports/junit/unit.xml'],
            requirement_ids: ['REQ-PW-004'],
          },
        ],
      }),
    );

    const isolated = buildServer({ repoRoot: fixtureRepo, logger: silent, rateLimitPerMinute: 100 });
    try {
      const response = await isolated.inject({ method: 'GET', url: '/api/v1/gates' });
      expect(response.statusCode).toBe(200);
      expect(response.json().data.available).toBe(true);
      expect(response.json().data.report.overall).toBe('fail');
    } finally {
      await isolated.close();
    }
  });
});
