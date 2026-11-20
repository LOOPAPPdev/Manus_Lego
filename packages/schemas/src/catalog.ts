import { z } from 'zod';

/**
 * Contracts for the committed catalog artifacts in `catalog/`.
 *
 * These mirror `schemas/template.schema.json` (the JSON Schema published for
 * external consumers) and are the single source of truth for the TypeScript
 * surface. The Python orchestrator validates the same documents with
 * `jsonschema`; parity is enforced by `tests/unit/test_catalog_contracts.py`
 * and `packages/schemas/src/catalog.test.ts`.
 */

export const SCHEMA_VERSION = '1.0.0';

export const ProviderSchema = z.enum(['cloudflare', 'vercel']);
export type Provider = z.infer<typeof ProviderSchema>;

export const TemplateStatusSchema = z.enum(['discovered_unverified', 'reference_only', 'enriched']);
export type TemplateStatus = z.infer<typeof TemplateStatusSchema>;

export const LicenseStatusSchema = z.enum(['needs_review', 'permissive', 'copyleft', 'proprietary', 'unknown']);

export const TemplateSourceSchema = z.object({
  repository: z.string().regex(/^[^/]+\/[^/]+$/, 'repository must be owner/name'),
  path: z.string(),
  commit: z.string().nullable(),
  repository_url: z.string(),
  source_url: z.string(),
});
export type TemplateSource = z.infer<typeof TemplateSourceSchema>;

export const TemplateFileSchema = z.object({
  path: z.string(),
  sha: z.string().nullable(),
  size: z.number().int().nullable().optional(),
  url: z.string(),
});

export const TemplateInventorySchema = z.object({
  complete: z.boolean(),
  file_count: z.number().int().nonnegative(),
  files: z.array(TemplateFileSchema),
  metadata_paths: z.record(z.string(), z.unknown()),
});

export const TemplateStackSchema = z.object({
  languages: z.array(z.string()),
  frameworks: z.array(z.string()),
  dependencies: z.record(z.string(), z.string()),
  package_manager: z.string(),
  products: z.array(z.string()),
  bindings: z.array(z.string()),
  ecosystems: z.array(z.string()),
  runtime_config: z.array(z.string()),
});

export const TemplateReadmeSchema = z.object({
  path: z.string().nullable(),
  url: z.string().nullable(),
  excerpt: z.string().nullable(),
});

export const TemplateLicenseSchema = z.object({
  status: LicenseStatusSchema,
  file_path: z.string().nullable(),
});

export const TemplateProvenanceSchema = z.object({
  origin: z.string(),
  source_ref: z.string().nullable(),
  inspected_files: z.array(z.string()),
  feature_basis: z.string(),
});

export const TemplateManifestSchema = z.object({
  schema_version: z.string(),
  id: z.string().min(3),
  provider: ProviderSchema,
  title: z.string(),
  description: z.string(),
  catalog_url: z.string(),
  source: TemplateSourceSchema,
  readme: TemplateReadmeSchema,
  inventory: TemplateInventorySchema,
  stack: TemplateStackSchema,
  commands: z.record(z.string(), z.string()),
  features: z.array(z.string()),
  tags: z.array(z.string()),
  platform_metadata: z.record(z.string(), z.unknown()),
  license: TemplateLicenseSchema,
  provenance: TemplateProvenanceSchema,
  status: TemplateStatusSchema,
  warnings: z.array(z.string()),
});
export type TemplateManifest = z.infer<typeof TemplateManifestSchema>;

/** Compact record used by `catalog/index.json` for search and listings. */
export const CatalogEntrySchema = z.object({
  id: z.string().min(3),
  provider: ProviderSchema,
  title: z.string(),
  description: z.string(),
  catalog_url: z.string(),
  repository: z.string(),
  path: z.string(),
  commit: z.string().nullable(),
  source_url: z.string(),
  stack: z.object({
    languages: z.array(z.string()),
    frameworks: z.array(z.string()),
    products: z.array(z.string()),
  }),
  features: z.array(z.string()),
  tags: z.array(z.string()),
  platform_metadata: z.record(z.string(), z.unknown()),
  status: TemplateStatusSchema,
  complete: z.boolean(),
});
export type CatalogEntry = z.infer<typeof CatalogEntrySchema>;

export const SourceStatusSchema = z
  .object({
    provider: z.string(),
    repo: z.string().optional(),
    source: z.string().optional(),
    state: z.string(),
    commit: z.string().nullable().optional(),
    found: z.number().int().optional(),
    count: z.number().int().optional(),
    reason: z.string().optional(),
  })
  .catchall(z.unknown());

export const CatalogIndexSchema = z.object({
  schema_version: z.string(),
  scope: z.string(),
  coverage: z.string(),
  source_status: z.array(SourceStatusSchema),
  template_count: z.number().int().nonnegative(),
  templates: z.array(CatalogEntrySchema),
});
export type CatalogIndex = z.infer<typeof CatalogIndexSchema>;

export const SourceDefinitionSchema = z
  .object({
    provider: z.string(),
    repo: z.string().regex(/^[^/]+\/[^/]+$/, 'repo must be owner/name'),
    /** `catalog/sources.json` uses `root`; `config/sources.yaml` uses `url`. */
    root: z.string().optional(),
    url: z.string().optional(),
    curated_manifest: z.string().optional(),
    metadata: z.string().optional(),
    role: z.string().optional(),
    license_review: z.string().optional(),
  })
  .catchall(z.unknown());
export type SourceDefinition = z.infer<typeof SourceDefinitionSchema>;

export const CatalogSourcesSchema = z
  .object({
    schema_version: z.string().optional(),
    github_sources: z.array(SourceDefinitionSchema),
    vercel_categories: z.array(z.string()).optional(),
    vercel_sitemaps: z.array(z.string()).optional(),
    policy: z.record(z.string(), z.unknown()).optional(),
  })
  .catchall(z.unknown());
export type CatalogSources = z.infer<typeof CatalogSourcesSchema>;

export const SelectionCandidateSchema = z.object({
  id: z.string(),
  score: z.number(),
  source_url: z.string(),
  commit: z.string().nullable(),
  reason: z.string(),
  validation: z.object({
    license: z.string(),
    security: z.string(),
    dependency_compatibility: z.string(),
    integration_tests: z.string(),
  }),
});

export const SelectionPlanSchema = z.object({
  schema_version: z.string(),
  status: z.literal('proposal_only'),
  request: z.string(),
  strategy: z.string(),
  candidates: z.array(SelectionCandidateSchema),
  gates: z.array(z.string()),
});
export type SelectionPlan = z.infer<typeof SelectionPlanSchema>;
