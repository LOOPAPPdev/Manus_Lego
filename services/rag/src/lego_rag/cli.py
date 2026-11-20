"""`lego-rag` command line: ingest, query, evaluate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .answer import build_answer
from .corpus import CorpusError, load_corpus
from .evaluation import evaluate, load_cases
from .models import AccessContext
from .store import RagIndex, StoreError


def _access(clearance: str, tenants: str) -> AccessContext:
    return AccessContext(
        clearance=clearance,  # type: ignore[arg-type]
        tenants=frozenset(part.strip() for part in tenants.split(",") if part.strip()) or frozenset({"public"}),
    )


def cmd_ingest(args: argparse.Namespace) -> int:
    documents = load_corpus(Path(args.corpus), default_classification=args.default_classification)
    index = RagIndex(args.store)
    try:
        stats = index.build(documents, max_tokens=args.max_tokens, overlap=args.overlap)
        manifest = index.document_manifest()
    finally:
        index.close()
    print(
        json.dumps(
            {
                "command": "ingest",
                "corpus": args.corpus,
                "store": args.store,
                "documents": stats["documents"],
                "chunks": stats["chunks"],
                "manifest": manifest,
            },
            indent=2,
        )
    )
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    index = RagIndex(args.store)
    try:
        answer = build_answer(index, args.question, _access(args.clearance, args.tenant), k=args.k)
    finally:
        index.close()
    print(json.dumps({"command": "query", **answer.as_dict()}, indent=2))
    return 0 if not answer.refused else 1


def cmd_eval(args: argparse.Namespace) -> int:
    documents = load_corpus(Path(args.corpus), default_classification=args.default_classification)
    cases = load_cases(Path(args.cases))
    index = RagIndex(":memory:")
    try:
        index.build(documents)
        report = evaluate(index, cases)
    finally:
        index.close()
    print(json.dumps({"command": "eval", **report}, indent=2))
    threshold = args.min_recall
    return 0 if report["metrics"]["recall_at_k"] >= threshold else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lego-rag", description="Permissioned retrieval over Manus LEGO documentation."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Build an index from a document corpus")
    ingest.add_argument("corpus")
    ingest.add_argument("--store", default=".data/rag.sqlite3")
    ingest.add_argument("--default-classification", default="internal", choices=["public", "internal", "restricted"])
    ingest.add_argument("--max-tokens", type=int, default=180)
    ingest.add_argument("--overlap", type=int, default=30)
    ingest.set_defaults(func=cmd_ingest)

    query = sub.add_parser("query", help="Ask a question and receive citations or a refusal")
    query.add_argument("question")
    query.add_argument("--store", default=".data/rag.sqlite3")
    query.add_argument("--clearance", default="public", choices=["public", "internal", "restricted"])
    query.add_argument("--tenant", default="public")
    query.add_argument("--k", type=int, default=4)
    query.set_defaults(func=cmd_query)

    ev = sub.add_parser("eval", help="Evaluate retrieval against a labelled question set")
    ev.add_argument("cases")
    ev.add_argument("--corpus", required=True)
    ev.add_argument("--default-classification", default="internal", choices=["public", "internal", "restricted"])
    ev.add_argument("--min-recall", type=float, default=0.0)
    ev.set_defaults(func=cmd_eval)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (CorpusError, StoreError, FileNotFoundError) as exc:
        print(json.dumps({"error": type(exc).__name__, "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
