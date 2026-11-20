#!/usr/bin/env python3
"""Generate the cross-language ranking parity fixture.

The Python catalog engine (`scripts/lego_catalog.py`) is the implementation of
record for lexical ranking. The TypeScript port in
`packages/shared/src/ranking.ts` must produce identical output; this fixture is
the contract between them.

Regenerate after any intentional change to the ranking weights or tokenizer:

    python3 tests/fixtures/generate_ranking_cases.py

A change to the fixture is a change to observable behaviour and must be
reviewed as such (see docs/decisions/0004-shared-ranking-port.md).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import lego_catalog  # noqa: E402

QUERIES = [
    ("react authentication database", "all", 10),
    ("cloudflare d1", "all", 10),
    ("astro blog", "all", 5),
    ("next js starter", "all", 10),
    ("workers ai chat", "all", 10),
    ("vectorize embedding", "all", 10),
    ("postgres fullstack", "all", 10),
    ("svelte", "all", 5),
    ("email routing", "all", 5),
    ("kubernetes operator golang", "all", 10),
    ("react", "cloudflare", 5),
    ("astro", "vercel", 5),
    ("", "all", 3),
    ("x402 proxy", "all", 3),
]


def main() -> int:
    index = json.loads((ROOT / "catalog" / "index.json").read_text(encoding="utf-8"))
    cases = []
    for query, provider, limit in QUERIES:
        hits = lego_catalog.ranked(index, query, provider, limit)
        cases.append(
            {
                "query": query,
                "provider": provider,
                "limit": limit,
                "expected": [{"id": hit["id"], "score": hit["score"]} for hit in hits],
            }
        )
    payload = {
        "generated_by": "tests/fixtures/generate_ranking_cases.py",
        "engine": "scripts/lego_catalog.py::ranked",
        "catalog_template_count": index.get("template_count", 0),
        "cases": cases,
    }
    out = Path(__file__).with_name("ranking-cases.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(cases)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
