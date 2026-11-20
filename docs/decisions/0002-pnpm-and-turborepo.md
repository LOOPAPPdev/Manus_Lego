# ADR 0002 — pnpm workspaces with a Turborepo task graph

- **Status:** accepted
- **Date:** 2026-11-20

## Context

The specification asks for a Turborepo monorepo for the JavaScript/TypeScript side. The
JavaScript surface here is small (a React SPA, a Fastify API and three libraries), but the
*contract* surface is not: the same catalog must be readable from TypeScript, from Python
and from a browser. A single npm project would make `packages/schemas` impossible to
consume without publishing, and npm's flat `node_modules` would let a package import a
dependency it never declared.

## Decision

Use **pnpm workspaces** (`apps/*`, `packages/*`) driven by **Turborepo 2**.

- `pnpm-workspace.yaml` declares the globs and an explicit `allowBuilds` allowlist
  (`esbuild: true`). pnpm 11 blocks dependency lifecycle scripts by default; an allowlist
  keeps the supply-chain surface visible instead of disabling the protection.
- `turbo.json` defines `build → typecheck/lint/test` with `outputs` and `inputs` so a
  cache hit is a real cache hit, not a stale artefact.
- Packages are referenced with the workspace protocol (`"@lego/schemas": "workspace:*"`),
  so a change to the contract invalidates every consumer's cache entry.
- TypeScript uses `module: NodeNext` with explicit `.js` specifiers in relative imports.
  The same source therefore runs unmodified under Node (the API) and under Vite (the web
  app), and `tsc --noEmit` catches a missing extension at build time rather than at
  runtime.

## Consequences

**Positive.** One command (`pnpm exec turbo run lint typecheck build test`) is the entire
local verification loop, and it is the same command CI runs. Workspace protocol imports
make the dependency graph explicit. The lockfile is a single source of truth for the JS
side.

**Negative.** pnpm's strict `node_modules` breaks packages that assume hoisting; the fix
is to declare the dependency, which is the behaviour we want. Turborepo's cache is
local-only here (no remote cache), so CI pays the full build cost on a cold cache.

**Rejected alternatives.**

- *npm workspaces.* Hoisting hides undeclared dependencies, and `npm ci` is slower here.
- *Nx.* More capable, but its plugin model is heavier than this repository needs.
- *A single package with path aliases.* Loses per-package `package.json` boundaries, which
  is exactly what makes `packages/schemas` reusable by the Python side through generated
  JSON Schema.
