import { readFileSync } from 'node:fs';
import { parse as parseYaml } from 'yaml';
import { z } from 'zod';
import { repoPaths } from './paths.js';

/**
 * Typed view of `config/manus.yaml`.
 *
 * The Python orchestrator owns the authoritative validation (pydantic models in
 * `services/orchestrator/src/lego_orchestrator/config.py`). This schema is the
 * consumer-side contract: if the file drifts, the API fails fast at boot instead
 * of serving partially configured behaviour.
 */
export const ManusConfigSchema = z.object({
  schema_version: z.string(),
  project: z.object({
    id: z.string(),
    name: z.string(),
    owner: z.string(),
    repository: z.string(),
    default_branch: z.string(),
  }),
  runtime: z.object({
    node: z.string(),
    python: z.string(),
    package_manager: z.string(),
  }),
  catalog: z.object({
    root: z.string(),
    index: z.string(),
    manifests: z.string(),
    coverage_label: z.string(),
  }),
  api: z.object({
    port: z.number().int().positive(),
    cors_origins: z.array(z.string()),
    read_only: z.boolean(),
    rate_limit_per_minute: z.number().int().positive(),
  }),
  web: z.object({
    port: z.number().int().positive(),
  }),
  paths: z.object({
    requirements: z.string(),
    traceability: z.string(),
    evidence_dir: z.string(),
    agents: z.string(),
    team_schema: z.string(),
    security_policy: z.string(),
  }),
  commands: z.record(z.string(), z.string()),
  gates: z.array(
    z.object({
      id: z.string(),
      name: z.string(),
      owner: z.string(),
      blocking: z.boolean(),
    }),
  ),
});
export type ManusConfig = z.infer<typeof ManusConfigSchema>;

export interface LoadedConfig {
  config: ManusConfig;
  path: string;
}

export function loadManusConfig(root?: string): LoadedConfig {
  const paths = repoPaths(root);
  const raw = readFileSync(paths.manusConfig, 'utf8');
  const parsed = ManusConfigSchema.safeParse(parseYaml(raw));
  if (!parsed.success) {
    throw new Error(`Invalid config/manus.yaml: ${z.prettifyError(parsed.error)}`);
  }
  return { config: parsed.data, path: paths.manusConfig };
}
