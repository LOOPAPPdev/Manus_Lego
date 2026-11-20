"""Retrieval evaluation: recall@k and MRR on a labelled question set.

Numbers are reported per case so a regression is attributable, not just a lower
aggregate. A case with no expected document is treated as a refusal test.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .models import AccessContext
from .store import RagIndex


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    question: str
    expected_document_ids: tuple[str, ...]
    k: int = 4
    clearance: str = "public"
    tenants: tuple[str, ...] = ("public",)


@dataclass(slots=True)
class CaseResult:
    question: str
    expected: tuple[str, ...]
    retrieved: tuple[str, ...]
    hit: bool
    reciprocal_rank: float
    refused: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "expected": list(self.expected),
            "retrieved": list(self.retrieved),
            "hit": self.hit,
            "reciprocal_rank": round(self.reciprocal_rank, 4),
            "refused": self.refused,
        }


def load_cases(path: Path) -> list[EvaluationCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = []
    for item in payload.get("cases", []):
        cases.append(
            EvaluationCase(
                question=item["question"],
                expected_document_ids=tuple(item.get("expected_document_ids", [])),
                k=int(item.get("k", 4)),
                clearance=item.get("clearance", "public"),
                tenants=tuple(item.get("tenants", ["public"])),
            )
        )
    return cases


def evaluate(index: RagIndex, cases: list[EvaluationCase]) -> dict[str, Any]:
    results: list[CaseResult] = []
    for case in cases:
        access = AccessContext(clearance=case.clearance, tenants=frozenset(case.tenants))  # type: ignore[arg-type]
        hits = index.search(case.question, access, k=case.k)
        retrieved = tuple(dict.fromkeys(hit.chunk.document_id for hit in hits))
        rank = next(
            (
                position + 1
                for position, document_id in enumerate(retrieved)
                if document_id in case.expected_document_ids
            ),
            0,
        )
        results.append(
            CaseResult(
                question=case.question,
                expected=case.expected_document_ids,
                retrieved=retrieved,
                hit=rank > 0,
                reciprocal_rank=1.0 / rank if rank else 0.0,
                refused=not retrieved,
            )
        )

    total = len(results) or 1
    return {
        "cases": [result.as_dict() for result in results],
        "metrics": {
            "cases": len(results),
            "recall_at_k": round(sum(1 for result in results if result.hit) / total, 4),
            "mrr": round(sum(result.reciprocal_rank for result in results) / total, 4),
            "refusal_rate": round(sum(1 for result in results if result.refused) / total, 4),
        },
    }
