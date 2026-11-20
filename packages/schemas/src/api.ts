import { z } from 'zod';
import { CatalogEntrySchema, ProviderSchema, TemplateManifestSchema, TemplateStatusSchema } from './catalog.js';
import { GateReportSchema, TraceabilityReportSchema } from './governance.js';

export const ApiMetaSchema = z.object({
  request_id: z.string(),
  generated_at: z.string(),
  source: z.string(),
});

export type ApiMeta = z.infer<typeof ApiMetaSchema>;

export const ApiErrorSchema = z.object({
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.unknown().optional(),
    request_id: z.string(),
  }),
});
export type ApiError = z.infer<typeof ApiErrorSchema>;

export function apiEnvelope<T extends z.ZodTypeAny>(data: T) {
  return z.object({ data, meta: ApiMetaSchema });
}

export const HealthSchema = z.object({
  status: z.literal('ok'),
  service: z.string(),
  version: z.string(),
  commit: z.string(),
  catalog_loaded: z.boolean(),
  uptime_seconds: z.number().nonnegative(),
});
export type Health = z.infer<typeof HealthSchema>;

export const CatalogSummarySchema = z.object({
  template_count: z.number().int().nonnegative(),
  coverage: z.string(),
  schema_version: z.string(),
  providers: z.array(
    z.object({
      provider: ProviderSchema,
      count: z.number().int().nonnegative(),
      enriched: z.number().int().nonnegative(),
      pinned: z.number().int().nonnegative(),
    }),
  ),
  statuses: z.record(z.string(), z.number().int()),
  source_status: z.array(z.record(z.string(), z.unknown())),
  last_modified: z.string().nullable(),
});
export type CatalogSummary = z.infer<typeof CatalogSummarySchema>;

export const TemplateListQuerySchema = z.object({
  q: z.string().trim().max(200).optional(),
  provider: z.union([ProviderSchema, z.literal('all')]).default('all'),
  status: z.union([TemplateStatusSchema, z.literal('all')]).default('all'),
  limit: z.coerce.number().int().min(1).max(100).default(25),
  offset: z.coerce.number().int().min(0).default(0),
  sort: z.enum(['relevance', 'title', 'provider']).default('relevance'),
});
export type TemplateListQuery = z.infer<typeof TemplateListQuerySchema>;

export const TemplateListSchema = z.object({
  items: z.array(
    CatalogEntrySchema.extend({
      score: z.number().optional(),
    }),
  ),
  total: z.number().int().nonnegative(),
  limit: z.number().int(),
  offset: z.number().int(),
  query: z.string().nullable(),
});
export type TemplateList = z.infer<typeof TemplateListSchema>;

export const TemplateDetailSchema = TemplateManifestSchema.extend({
  /** Denormalised from `source.commit` so clients do not have to reach into the source block. */
  commit: z.string().nullable(),
  /** Denormalised from `inventory.complete`. */
  complete: z.boolean(),
  related: z.array(z.object({ id: z.string(), title: z.string(), score: z.number() })),
});
export type TemplateDetail = z.infer<typeof TemplateDetailSchema>;

export const GovernanceResponseSchema = z.object({
  gates: GateReportSchema.nullable(),
  traceability: TraceabilityReportSchema.nullable(),
  available: z.boolean(),
  hint: z.string(),
});
export type GovernanceResponse = z.infer<typeof GovernanceResponseSchema>;
