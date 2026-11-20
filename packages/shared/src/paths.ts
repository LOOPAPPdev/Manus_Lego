import { existsSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';

/**
 * Resolve the repository root without assuming the current working directory.
 *
 * Order: explicit argument -> `LEGO_REPO_ROOT` -> nearest ancestor containing
 * `turbo.json` (the monorepo marker) -> nearest ancestor containing `.git`.
 */
export function findRepoRoot(startPath: string = process.cwd()): string {
  const explicit = process.env.LEGO_REPO_ROOT;
  if (explicit && existsSync(explicit)) {
    return resolve(explicit);
  }

  let current = resolve(startPath);
  if (!existsSync(current) || !statSync(current).isDirectory()) {
    current = dirname(current);
  }

  for (const marker of ['turbo.json', join('.git')]) {
    let cursor = current;
    for (;;) {
      if (existsSync(join(cursor, marker))) {
        return cursor;
      }
      const parent = dirname(cursor);
      if (parent === cursor) {
        break;
      }
      cursor = parent;
    }
  }

  throw new Error(`Unable to locate the repository root from ${startPath}`);
}

export interface RepoPaths {
  root: string;
  catalog: string;
  catalogIndex: string;
  catalogTemplates: string;
  catalogSources: string;
  config: string;
  manusConfig: string;
  securityPolicy: string;
  teamSchema: string;
  agentsRegistry: string;
  requirements: string;
  traceability: string;
  evidenceDir: string;
  gatesReport: string;
  traceabilityReport: string;
}

export function repoPaths(root: string = findRepoRoot()): RepoPaths {
  return {
    root,
    catalog: join(root, 'catalog'),
    catalogIndex: join(root, 'catalog', 'index.json'),
    catalogTemplates: join(root, 'catalog', 'templates'),
    catalogSources: join(root, 'catalog', 'sources.json'),
    config: join(root, 'config'),
    manusConfig: join(root, 'config', 'manus.yaml'),
    securityPolicy: join(root, 'config', 'security.yaml'),
    teamSchema: join(root, 'config', 'TEAMSCHEMA.yaml'),
    agentsRegistry: join(root, 'agents', 'registry.yaml'),
    requirements: join(root, 'docs', 'specifications', 'requirements.md'),
    traceability: join(root, 'docs', 'specifications', 'traceability.yaml'),
    evidenceDir: join(root, 'docs', 'evidence'),
    gatesReport: join(root, 'docs', 'evidence', 'gates.json'),
    traceabilityReport: join(root, 'docs', 'evidence', 'traceability.json'),
  };
}
