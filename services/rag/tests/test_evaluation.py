from __future__ import annotations

from pathlib import Path

from lego_rag.evaluation import evaluate, load_cases
from lego_rag.store import RagIndex

FIXTURES = Path(__file__).parent / "fixtures"


def test_labelled_questions_meet_the_recall_floor(index: RagIndex) -> None:
    cases = load_cases(FIXTURES / "evaluation.json")
    report = evaluate(index, cases)
    metrics = report["metrics"]

    assert metrics["cases"] == len(cases)
    assert metrics["recall_at_k"] >= 0.8, report
    assert metrics["mrr"] >= 0.7, report


def test_public_clearance_never_returns_restricted_documents(index: RagIndex) -> None:
    cases = [case for case in load_cases(FIXTURES / "evaluation.json") if case.clearance == "public"]
    report = evaluate(index, cases)
    for case in report["cases"]:
        assert "incident-runbook" not in case["retrieved"], case


def test_evaluation_is_deterministic(index: RagIndex) -> None:
    cases = load_cases(FIXTURES / "evaluation.json")
    first = evaluate(index, cases)["metrics"]
    second = evaluate(index, cases)["metrics"]
    assert first == second
