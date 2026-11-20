---
title: D1 Sessions API template
classification: public
tenants: public
tags: d1, sessions, database, workers
---
# D1 Sessions API template

The `d1-starter-sessions-api-template` demonstrates the D1 Sessions API for read
replication in a Cloudflare Worker. It creates a database binding named `DB` and
uses a session object to route queries.

## When to use it

Choose this template when a Worker needs sequential consistency for a single user
session without a central database connection pool. It is a poor fit for
analytical queries or cross-tenant reporting.

## Reuse notes

The template is discovered from `cloudflare/templates` and is not pinned in the
bootstrap catalog. Copying its migration files requires a license review first.
