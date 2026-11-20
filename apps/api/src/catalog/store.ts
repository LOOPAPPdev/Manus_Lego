import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { CatalogIndexSchema, TemplateManifestSchema } from '@lego/schemas';
import type { CatalogEntry, CatalogIndex, TemplateManifest } from '@lego/schemas';
import { AppError, repoPaths } from '@lego/shared';
import type { Logger } from '@lego/shared';

/**
 * Read-only catalog access.
 *
 * The catalog is data on disk, not a database. Reads are cached and invalidated
 * by mtime, so a catalog refresh (a reviewed PR) becomes visible without a
 * restart. Nothing here writes to the catalog: the API is deliberately
 * incapable of mutating provenance data.
 */
export interface CatalogSnapshot {
  index: CatalogIndex;
  manifests: Map<string, TemplateManifest>;
  loadedAt: string;
  lastModified: string | null;
}

interface CacheState {
  indexMtimeMs: number;
  manifestsMtimeMs: number;
  snapshot: CatalogSnapshot | null;
}

function latestMtime(path: string): number {
  try {
    return statSync(path).mtimeMs;
  } catch {
    return 0;
  }
}

export class CatalogStore {
  private readonly root: string;
  private readonly paths: ReturnType<typeof repoPaths>;
  private readonly logger: Logger;
  private cache: CacheState = { indexMtimeMs: 0, manifestsMtimeMs: 0, snapshot: null };

  constructor(root: string, logger: Logger) {
    this.root = root;
    this.paths = repoPaths(root);
    this.logger = logger;
  }

  private manifestDirectoryMtime(): number {
    try {
      return statSync(this.paths.catalogTemplates).mtimeMs;
    } catch {
      return 0;
    }
  }

  get available(): boolean {
    try {
      return statSync(this.paths.catalogIndex).isFile();
    } catch {
      return false;
    }
  }

  snapshot(): CatalogSnapshot {
    const indexMtime = latestMtime(this.paths.catalogIndex);
    const manifestsMtime = this.manifestDirectoryMtime();

    if (this.cache.snapshot && this.cache.indexMtimeMs === indexMtime && this.cache.manifestsMtimeMs === manifestsMtime) {
      return this.cache.snapshot;
    }

    if (!indexMtime) {
      throw new AppError('CATALOG_UNAVAILABLE', 'catalog/index.json is missing; run `lego index` or check out the catalog.');
    }

    const raw = readFileSync(this.paths.catalogIndex, 'utf8');
    const parsed = CatalogIndexSchema.safeParse(JSON.parse(raw));
    if (!parsed.success) {
      throw new AppError('CATALOG_UNAVAILABLE', 'catalog/index.json does not satisfy the catalog contract.', {
        details: parsed.error.issues.slice(0, 5),
      });
    }

    const manifests = this.loadManifests();
    const snapshot: CatalogSnapshot = {
      index: parsed.data,
      manifests,
      loadedAt: new Date().toISOString(),
      lastModified: indexMtime ? new Date(indexMtime).toISOString() : null,
    };

    this.cache = { indexMtimeMs: indexMtime, manifestsMtimeMs: manifestsMtime, snapshot };
    this.logger.info('catalog.loaded', {
      templates: snapshot.index.templates.length,
      manifests: manifests.size,
      coverage: snapshot.index.coverage,
    });
    return snapshot;
  }

  private loadManifests(): Map<string, TemplateManifest> {
    const manifests = new Map<string, TemplateManifest>();
    let providers: string[];
    try {
      providers = readdirSync(this.paths.catalogTemplates, { withFileTypes: true })
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name);
    } catch {
      return manifests;
    }

    for (const provider of providers) {
      const directory = join(this.paths.catalogTemplates, provider);
      for (const file of readdirSync(directory)) {
        if (!file.endsWith('.json')) {
          continue;
        }
        try {
          const manifest = TemplateManifestSchema.parse(JSON.parse(readFileSync(join(directory, file), 'utf8')));
          manifests.set(manifest.id, manifest);
        } catch (error) {
          // A malformed manifest must not take the whole API down; it is skipped
          // and logged so the catalog validation job can catch it in CI.
          this.logger.warn('catalog.manifest_invalid', { provider, file, error: String(error) });
        }
      }
    }
    return manifests;
  }

  entries(): CatalogEntry[] {
    return this.snapshot().index.templates;
  }

  find(id: string): { entry: CatalogEntry; manifest: TemplateManifest | null } | null {
    const snapshot = this.snapshot();
    const entry = snapshot.index.templates.find((item) => item.id === id);
    if (!entry) {
      return null;
    }
    return { entry, manifest: snapshot.manifests.get(id) ?? null };
  }

  manifest(id: string): TemplateManifest | null {
    return this.snapshot().manifests.get(id) ?? null;
  }

  summary() {
    const snapshot = this.snapshot();
    const byProvider = new Map<string, { provider: 'cloudflare' | 'vercel'; count: number; enriched: number; pinned: number }>();
    const statuses: Record<string, number> = {};

    for (const entry of snapshot.index.templates) {
      const current = byProvider.get(entry.provider) ?? { provider: entry.provider, count: 0, enriched: 0, pinned: 0 };
      current.count += 1;
      if (entry.status === 'enriched') {
        current.enriched += 1;
      }
      if (entry.commit) {
        current.pinned += 1;
      }
      byProvider.set(entry.provider, current);
      statuses[entry.status] = (statuses[entry.status] ?? 0) + 1;
    }

    return {
      template_count: snapshot.index.templates.length,
      coverage: snapshot.index.coverage,
      schema_version: snapshot.index.schema_version,
      providers: [...byProvider.values()].sort((a, b) => a.provider.localeCompare(b.provider)),
      statuses,
      source_status: snapshot.index.source_status.map((item) => ({ ...item })),
      last_modified: snapshot.lastModified,
    };
  }
}
