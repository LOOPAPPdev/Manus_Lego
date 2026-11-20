import { randomUUID } from 'node:crypto';
import Fastify from 'fastify';
import type { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import { z } from 'zod';
import {
  TemplateListQuerySchema,
  CatalogSummarySchema,
  HealthSchema,
  TemplateDetailSchema,
  TemplateListSchema,
} from '@lego/schemas';
import { AppError, createLogger, loadManusConfig, rankTemplates, repoPaths } from '@lego/shared';
import type { Logger, ManusConfig } from '@lego/shared';
import { CatalogStore } from './catalog/store.js';
import { GovernanceStore } from './governance/store.js';
import { FixedWindowLimiter } from './lib/rate-limit.js';

export const SERVICE_NAME = 'lego-api';
export const SERVICE_VERSION = '0.1.0';

export interface ServerOptions {
  repoRoot?: string;
  config?: ManusConfig;
  logger?: Logger;
  /** Overrides `config.api.rate_limit_per_minute`; used by tests. */
  rateLimitPerMinute?: number;
}

interface BuildContext {
  config: ManusConfig;
  logger: Logger;
  catalog: CatalogStore;
  governance: GovernanceStore;
  limiter: FixedWindowLimiter;
  startedAt: number;
}

function envelope(data: unknown, requestId: string, source: string) {
  return {
    data,
    meta: { request_id: requestId, generated_at: new Date().toISOString(), source },
  };
}

function clientKey(request: FastifyRequest): string {
  return request.ip || 'unknown';
}

export function buildServer(options: ServerOptions = {}): FastifyInstance {
  const loaded = options.config ? { config: options.config } : loadManusConfig(options.repoRoot);
  const config = loaded.config;
  const logger =
    options.logger ??
    createLogger({
      service: SERVICE_NAME,
      level: (process.env.LEGO_LOG_LEVEL as 'debug' | 'info' | 'warn' | 'error' | undefined) ?? 'info',
    });
  const paths = repoPaths(options.repoRoot);

  const context: BuildContext = {
    config,
    logger,
    catalog: new CatalogStore(paths.root, logger),
    governance: new GovernanceStore(paths.root, logger),
    limiter: new FixedWindowLimiter(options.rateLimitPerMinute ?? config.api.rate_limit_per_minute),
    startedAt: Date.now(),
  };

  const app = Fastify({
    logger: false,
    genReqId: () => randomUUID(),
    bodyLimit: 64 * 1024,
    trustProxy: true,
  });

  // ---- Security headers and method allowlist (read-only by construction) ----
  app.addHook('onRequest', async (request: FastifyRequest, reply: FastifyReply) => {
    reply.header('X-Content-Type-Options', 'nosniff');
    reply.header('X-Frame-Options', 'DENY');
    reply.header('Referrer-Policy', 'no-referrer');
    reply.header('Cross-Origin-Resource-Policy', 'same-site');
    reply.header('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'");
    reply.header('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');

    if (request.method !== 'GET' && request.method !== 'HEAD' && request.method !== 'OPTIONS') {
      throw new AppError('BAD_REQUEST', `Method ${request.method} is not allowed; this API is read-only.`, {
        details: { allowed: ['GET', 'HEAD', 'OPTIONS'] },
      });
    }

    const origin = request.headers.origin;
    if (origin && config.api.cors_origins.includes(origin)) {
      reply.header('Access-Control-Allow-Origin', origin);
      reply.header('Vary', 'Origin');
      reply.header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
      reply.header('Access-Control-Allow-Headers', 'Content-Type');
      reply.header('Access-Control-Max-Age', '600');
    }

    if (request.method === 'OPTIONS') {
      await reply.code(204).send();
      return;
    }

    const decision = context.limiter.check(clientKey(request));
    reply.header('X-RateLimit-Limit', String(options.rateLimitPerMinute ?? config.api.rate_limit_per_minute));
    reply.header('X-RateLimit-Remaining', String(decision.remaining));
    reply.header('X-RateLimit-Reset', String(decision.resetSeconds));
    if (!decision.allowed) {
      reply.header('Retry-After', String(decision.resetSeconds));
      throw new AppError('RATE_LIMITED', 'Request rate exceeded for this client.', {
        details: { retry_after_seconds: decision.resetSeconds },
      });
    }

    context.logger.info('http.request', {
      request_id: request.id,
      method: request.method,
      url: request.url,
    });
  });

  // ---- Error handling: never leak internals, always return the envelope ----
  app.setErrorHandler((error: unknown, request, reply) => {
    if (error instanceof AppError) {
      context.logger.warn('http.error', { request_id: request.id, code: error.code, status: error.status });
      void reply.code(error.status).send({ error: { ...error.toJSON(), request_id: request.id } });
      return;
    }
    if (error instanceof z.ZodError) {
      void reply.code(400).send({
        error: {
          code: 'BAD_REQUEST',
          message: 'Request validation failed.',
          details: error.issues.map((issue) => ({ path: issue.path.join('.'), message: issue.message })),
          request_id: request.id,
        },
      });
      return;
    }
    const statusCode = (error as { statusCode?: number }).statusCode ?? 500;
    if (statusCode < 500) {
      void reply.code(statusCode).send({
        error: { code: 'BAD_REQUEST', message: (error as Error).message, request_id: request.id },
      });
      return;
    }
    context.logger.error('http.unhandled', { request_id: request.id, error: String(error) });
    void reply.code(500).send({
      error: { code: 'INTERNAL', message: 'Unexpected server error.', request_id: request.id },
    });
  });

  app.setNotFoundHandler((request, reply) => {
    void reply.code(404).send({
      error: {
        code: 'NOT_FOUND',
        message: `No route for ${request.method} ${request.url}`,
        request_id: request.id,
      },
    });
  });

  // ---- Routes ----
  app.get('/health', async (request) => {
    return envelope(
      HealthSchema.parse({
        status: 'ok',
        service: SERVICE_NAME,
        version: SERVICE_VERSION,
        commit: process.env.GITHUB_SHA ?? process.env.GIT_COMMIT ?? 'unknown',
        catalog_loaded: context.catalog.available,
        uptime_seconds: (Date.now() - context.startedAt) / 1000,
      }),
      request.id,
      'runtime',
    );
  });

  app.get('/api/v1/catalog/summary', async (request) => {
    const summary = CatalogSummarySchema.parse(context.catalog.summary());
    return envelope(summary, request.id, 'catalog/index.json');
  });

  app.get('/api/v1/templates', async (request) => {
    const query = TemplateListQuerySchema.parse(request.query ?? {});
    const snapshot = context.catalog.snapshot();

    let items = snapshot.index.templates;
    if (query.provider !== 'all') {
      items = items.filter((entry) => entry.provider === query.provider);
    }
    if (query.status !== 'all') {
      items = items.filter((entry) => entry.status === query.status);
    }

    let scored: Array<(typeof items)[number] & { score?: number }>;
    if (query.q) {
      const ranked = rankTemplates({ templates: items }, query.q, { provider: 'all', limit: items.length });
      scored = ranked;
    } else {
      scored = [...items];
    }

    if (query.sort === 'title') {
      scored = [...scored].sort((a, b) => a.title.localeCompare(b.title));
    } else if (query.sort === 'provider') {
      scored = [...scored].sort((a, b) => a.provider.localeCompare(b.provider) || a.title.localeCompare(b.title));
    }

    const page = scored.slice(query.offset, query.offset + query.limit);
    const payload = TemplateListSchema.parse({
      items: page,
      total: scored.length,
      limit: query.limit,
      offset: query.offset,
      query: query.q ?? null,
    });
    return envelope(payload, request.id, 'catalog/index.json');
  });

  app.get('/api/v1/templates/:id', async (request) => {
    const { id } = z.object({ id: z.string().min(3).max(200) }).parse(request.params);
    const found = context.catalog.find(id);
    if (!found) {
      throw new AppError('NOT_FOUND', `Template ${id} is not in the catalog.`);
    }

    const manifest = found.manifest;
    const base = manifest ?? {
      schema_version: snapshotVersion(context.catalog),
      ...found.entry,
      readme: { path: null, url: null, excerpt: null },
      inventory: { complete: found.entry.complete, file_count: 0, files: [], metadata_paths: {} },
      stack: {
        languages: found.entry.stack.languages,
        frameworks: found.entry.stack.frameworks,
        dependencies: {},
        package_manager: 'unknown',
        products: found.entry.stack.products,
        bindings: [],
        ecosystems: [],
        runtime_config: [],
      },
      commands: {},
      license: { status: 'needs_review', file_path: null },
      provenance: {
        origin: 'catalog_index',
        source_ref: null,
        inspected_files: [],
        feature_basis: 'index_summary_only',
      },
      warnings: ['Full manifest not available; only the compact index entry is published.'],
    };

    const related = rankTemplates(
      { templates: context.catalog.entries().filter((entry) => entry.id !== id) },
      `${found.entry.title} ${found.entry.tags.join(' ')}`,
      { provider: found.entry.provider, limit: 4 },
    ).map((entry) => ({ id: entry.id, title: entry.title, score: entry.score }));

    const payload = TemplateDetailSchema.parse({
      ...base,
      commit: found.entry.commit,
      complete: found.entry.complete,
      related,
    });
    return envelope(payload, request.id, 'catalog/templates');
  });

  app.get('/api/v1/search', async (request) => {
    const query = z
      .object({
        q: z.string().trim().min(1).max(200),
        provider: z.enum(['all', 'cloudflare', 'vercel']).default('all'),
        limit: z.coerce.number().int().min(1).max(50).default(10),
      })
      .parse(request.query ?? {});

    const results = rankTemplates({ templates: context.catalog.entries() }, query.q, {
      provider: query.provider,
      limit: query.limit,
    });
    return envelope(
      { query: query.q, provider: query.provider, count: results.length, results },
      request.id,
      'catalog/index.json',
    );
  });

  app.get('/api/v1/gates', async (request) => {
    const snapshot = context.governance.snapshot();
    return envelope(
      {
        report: snapshot.gates,
        available: snapshot.gates !== null,
        hint: snapshot.gates ? null : 'Run `lego verify` to produce docs/evidence/gates.json.',
      },
      request.id,
      'docs/evidence/gates.json',
    );
  });

  app.get('/api/v1/requirements', async (request) => {
    const snapshot = context.governance.snapshot();
    return envelope(
      {
        report: snapshot.traceability,
        available: snapshot.traceability !== null,
        hint: snapshot.traceability
          ? null
          : 'Run `lego report` to produce docs/evidence/traceability.json.',
      },
      request.id,
      'docs/evidence/traceability.json',
    );
  });

  app.get('/api/v1/meta', async (request) => {
    return envelope(
      {
        project: config.project,
        runtime: config.runtime,
        read_only: config.api.read_only,
        gates: config.gates,
        commands: config.commands,
        evidence_available: context.governance.snapshot().available,
      },
      request.id,
      'config/manus.yaml',
    );
  });

  return app;
}

function snapshotVersion(store: CatalogStore): string {
  return store.snapshot().index.schema_version;
}
