# ADR 0006 — The API is read-only by construction

- **Status:** accepted
- **Date:** 2026-11-20

## Context

The web app needs the catalog, the gate report and the requirement matrix. All three are
files in the repository that a human or an agent produces through Git. Nothing in the
product needs to write them over HTTP.

An API that *can* write is an API that must authenticate, authorise, audit and rate-limit
writes. Each of those is a place to get it wrong, and none of them buys a capability the
project needs.

## Decision

The Fastify service exposes only `GET`/`HEAD`/`OPTIONS`. Anything else is rejected in an
`onRequest` hook before routing:

- The method allowlist is enforced centrally, so a route added later cannot accidentally
  become writable.
- Responses are validated with the shared zod schemas (`packages/schemas`) and returned in
  one envelope: `{ data, meta: { request_id, generated_at, source } }`. Errors use
  `{ error: { code, message, details, request_id } }` and never include a stack trace.
- The data comes from `docs/evidence/*.json` and `catalog/index.json` through
  mtime-invalidated caches. If an artifact is missing, the endpoint says so
  (`available: false` with a hint) instead of inventing a status.
- Hardening is on by default: CSP `default-src 'none'`, `X-Frame-Options: DENY`,
  `nosniff`, `no-referrer`, a per-client fixed-window rate limit with `Retry-After`, a
  64 KB body limit, and a CORS allowlist that echoes only configured origins.
- The trust boundary is the process: no database, no session, no cookies, no user input
  reaching a filesystem path. `:id` is validated and matched against the loaded index.

## Consequences

**Positive.** There is no authentication surface to get wrong, no write audit trail to
maintain, and the API can be cached aggressively. A compromised API process can read the
repository's public artifacts and nothing else.

**Negative.** Updating the catalog requires a Git commit and a redeploy rather than an API
call — acceptable, because that is exactly the governance model this project is built
around. The rate limiter is in-process, so it resets on restart and does not coordinate
across replicas; that is documented as a known limit rather than hidden.

**Rejected alternatives.**

- *A write API with a token.* Adds a credential to protect, an audit log to keep, and a
  way to bypass the gates that are the point of the system.
- *GraphQL.* More expressive than needed for six read endpoints, and it moves validation
  into resolvers where the shared schema contract is harder to enforce.
