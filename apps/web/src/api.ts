/**
 * Thin, typed client for the read-only API.
 *
 * Failure is surfaced as data (`ApiFailure`) rather than thrown, so pages can
 * render an honest error state instead of an empty catalog that looks healthy.
 */

const BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? '/api/v1';

export interface ApiMeta {
  request_id: string;
  generated_at: string;
  source: string;
}

export interface ApiEnvelope<T> {
  data: T;
  meta: ApiMeta;
}

export type ApiResult<T> = { ok: true; envelope: ApiEnvelope<T> } | { ok: false; status: number; message: string };

export interface CatalogEntry {
  id: string;
  provider: string;
  title: string;
  description: string;
  catalog_url: string;
  repository: string;
  path: string;
  commit: string | null;
  source_url: string;
  stack: { languages: string[]; frameworks: string[]; products: string[] };
  features: string[];
  tags: string[];
  platform_metadata: Record<string, unknown>;
  status: string;
  complete: boolean;
  score?: number;
}

export interface CatalogSummary {
  template_count: number;
  coverage: string;
  schema_version: string;
  providers: Array<{ provider: string; count: number; enriched: number; pinned: number }>;
  statuses: Record<string, number>;
  source_status: Array<Record<string, unknown>>;
  last_modified: string | null;
}

export interface TemplateList {
  items: CatalogEntry[];
  total: number;
  limit: number;
  offset: number;
  query: string | null;
}

export interface TemplateDetail {
  id: string;
  provider: string;
  title: string;
  description: string;
  catalog_url: string;
  schema_version: string;
  commit: string | null;
  complete: boolean;
  features: string[];
  tags: string[];
  platform_metadata: Record<string, unknown>;
  status: string;
  source: { repository: string; path: string; commit: string | null; repository_url: string; source_url: string };
  source_url: string;
  stack: {
    languages: string[];
    frameworks: string[];
    products: string[];
    bindings: string[];
    package_manager: string;
    dependencies: Record<string, string>;
    ecosystems: string[];
    runtime_config: string[];
  };
  readme: { path: string | null; url: string | null; excerpt: string | null };
  inventory: {
    complete: boolean;
    file_count: number;
    files: Array<{ path: string; sha: string | null; url: string }>;
    metadata_paths: Record<string, unknown>;
  };
  commands: Record<string, string>;
  license: { status: string; file_path: string | null };
  provenance: { origin: string; source_ref: string | null; inspected_files: string[]; feature_basis: string };
  warnings: string[];
  related: Array<{ id: string; title: string; score: number }>;
}

export interface GateReport {
  generated_at: string;
  commit: string;
  environment: string;
  overall: string;
  gates: Array<{ id: string; name: string; status: string; detail: string; evidence: string[]; requirement_ids: string[] }>;
}

export interface TraceabilityReport {
  generated_at: string;
  commit: string;
  requirements: Array<{
    id: string;
    practice: string;
    title: string;
    status: string;
    implementation_present: boolean;
    tests: Array<{ name: string; outcome: string; requirement_ids: string[] }>;
    evidence: string[];
    notes: string[];
  }>;
  summary: { total: number; verified: number; partial: number; unverified: number; failing: number; by_practice: Record<string, number> };
}

export interface ProjectMeta {
  project: { id: string; name: string; owner: string; repository: string; default_branch: string };
  runtime: { node: string; python: string; package_manager: string };
  read_only: boolean;
  gates: Array<{ id: string; name: string; owner: string; blocking: boolean }>;
  commands: Record<string, string>;
  evidence_available: boolean;
}

async function request<T>(path: string, signal?: AbortSignal): Promise<ApiResult<T>> {
  try {
    const response = await fetch(`${BASE}${path}`, {
      headers: { accept: 'application/json' },
      signal,
    });
    const body = (await response.json().catch(() => null)) as unknown;
    if (!response.ok) {
      const message =
        (body as { error?: { message?: string } } | null)?.error?.message ?? `Request failed with status ${response.status}`;
      return { ok: false, status: response.status, message };
    }
    return { ok: true, envelope: body as ApiEnvelope<T> };
  } catch (error) {
    if ((error as Error).name === 'AbortError') {
      return { ok: false, status: 0, message: 'Request cancelled' };
    }
    return { ok: false, status: 0, message: 'The API is unreachable. Start it with `pnpm --filter @lego/api dev`.' };
  }
}

export const api = {
  summary: (signal?: AbortSignal) => request<CatalogSummary>('/catalog/summary', signal),
  templates: (params: { q?: string; provider?: string; status?: string; limit?: number; offset?: number; sort?: string }, signal?: AbortSignal) => {
    const search = new URLSearchParams();
    if (params.q) search.set('q', params.q);
    if (params.provider && params.provider !== 'all') search.set('provider', params.provider);
    if (params.status && params.status !== 'all') search.set('status', params.status);
    if (params.limit) search.set('limit', String(params.limit));
    if (params.offset) search.set('offset', String(params.offset));
    if (params.sort) search.set('sort', params.sort);
    const query = search.toString();
    return request<TemplateList>(`/templates${query ? `?${query}` : ''}`, signal);
  },
  template: (id: string, signal?: AbortSignal) => request<TemplateDetail>(`/templates/${encodeURIComponent(id)}`, signal),
  gates: (signal?: AbortSignal) =>
    request<{ report: GateReport | null; available: boolean; hint: string | null }>('/gates', signal),
  requirements: (signal?: AbortSignal) =>
    request<{ report: TraceabilityReport | null; available: boolean; hint: string | null }>('/requirements', signal),
  meta: (signal?: AbortSignal) => request<ProjectMeta>('/meta', signal),
};
