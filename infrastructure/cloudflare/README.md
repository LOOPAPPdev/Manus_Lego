# Cloudflare deployment (optional)

The SPA in `apps/web` is a static bundle: it can be served by the nginx container in
`infrastructure/docker/`, or by Cloudflare Pages. This directory holds the Pages
configuration. **It has not been deployed from this environment** — treat it as reviewed
configuration, not as a working deployment.

## What is configured

| File | Purpose |
|---|---|
| `pages/_headers` | Response headers for every static asset (CSP, HSTS, `nosniff`, frame denial) |
| `pages/_redirects` | SPA history fallback, plus a 404 for unknown API paths |
| `pages/wrangler.toml` | Project name, build command and output directory for `wrangler pages deploy` |

## Build settings

```
Build command:      pnpm install --frozen-lockfile && pnpm exec turbo run build --filter=@lego/web
Output directory:   apps/web/dist
Node version:       22.20.0
```

## Why the API is not deployed here

The API reads `catalog/index.json` and `docs/evidence/*.json` from the filesystem and runs
on Node with `fastify`. Running it on Workers would require an R2 binding and a rewrite of
the store layer; there is no requirement for that, and a half-migrated deployment would be
worse than a documented boundary. The API stays a container; the SPA can be anywhere.

## Consequences to be aware of

- If the SPA is served from Pages and the API from a container, they are cross-origin: the
  API's `cors_origins` allowlist in `config/manus.yaml` must include the Pages domain, and
  the SPA needs `VITE_API_BASE_URL` at build time.
- `_headers` duplicates the CSP that nginx sets. Two sources of truth for a security header
  drift; if you pick Pages, delete the nginx config or keep the two in sync deliberately.
