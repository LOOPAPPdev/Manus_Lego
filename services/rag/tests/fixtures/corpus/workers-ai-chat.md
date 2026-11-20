---
title: Workers AI chat application
classification: public
tenants: public
tags: workers-ai, chat, llm, streaming
---
# Workers AI chat application

The `llm-chat-app-template` streams responses from Workers AI to a small frontend.
It keeps no conversation history on the server and relies on the browser to hold
the transcript.

## Trade-offs

Streaming gives fast perceived latency but complicates retries: a failed stream
must be restarted from the beginning. There is no server-side moderation step in
the template, so an application that accepts untrusted input must add one.

## Deployment

The template deploys with `wrangler deploy` and requires an AI binding. Model
selection is configured in the Worker, not in the frontend.
