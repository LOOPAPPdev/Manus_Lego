#!/usr/bin/env python3
"""RAG — retrieve evidence for a question, with citations or an explicit refusal.

The workflow builds an in-memory index over a corpus (never a private one from
Git) and answers within an access context. Retrieved content is treated as
untrusted data; guardrail findings are printed with the answer.

    uv run --project services/rag python workflows/retrieve.py \
        "which template demonstrates D1 sessions" \
        --corpus services/rag/tests/fixtures/corpus --clearance public

Exit codes: 0 answered, 1 refused (no supporting evidence), 2 environment error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "rag" / "src"))

try:
    from lego_rag.answer import build_answer
    from lego_rag.corpus import load_corpus
    from lego_rag.models import AccessContext
    from lego_rag.store import RagIndex
except ImportError as exc:  # pragma: no cover - environment guidance
    print(
        json.dumps(
            {
                "stage": "retrieve",
                "state": "blocked",
                "reason": f"missing RAG dependencies: {exc}",
                "fix": "uv sync --project services/rag",
            }
        ),
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Retrieve evidence with citations.")
    parser.add_argument("question")
    parser.add_argument("--corpus", required=True, help="Directory of documents to index")
    parser.add_argument("--clearance", default="public", choices=["public", "internal", "restricted"])
    parser.add_argument("--tenant", default="public", help="Comma-separated tenant labels")
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--store", default=None, help="Persist the index to this SQLite file instead of memory")
    args = parser.parse_args(argv)

    documents = load_corpus(Path(args.corpus))
    index = RagIndex(args.store)
    try:
        stats = index.build(documents)
        access = AccessContext(
            clearance=args.clearance,  # type: ignore[arg-type]
            tenants=frozenset(part.strip() for part in args.tenant.split(",") if part.strip()),
        )
        answer = build_answer(index, args.question, access, k=args.k)
    finally:
        index.close()

    print(json.dumps({"stage": "retrieve", "index": stats, **answer.as_dict()}, indent=2))
    return 0 if not answer.refused else 1


if __name__ == "__main__":
    raise SystemExit(main())
