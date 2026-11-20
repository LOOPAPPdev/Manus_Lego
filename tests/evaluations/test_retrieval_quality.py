"""Retrieval quality and answer safety over the synthetic corpus.

Quality is measured, not asserted: recall@k and MRR come from the labelled question
set, and the thresholds below are the regression budget for this corpus. They say
nothing about a real tenant's documents.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from lego_rag.answer import build_answer
from lego_rag.corpus import load_corpus
from lego_rag.evaluation import evaluate, load_cases
from lego_rag.models import AccessContext
from lego_rag.store import RagIndex

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "services/rag/tests/fixtures"

pytestmark = pytest.mark.evaluation


@pytest.fixture(scope="module")
def index():
    documents = load_corpus(FIXTURES / "corpus")
    assert len(documents) >= 4
    with RagIndex() as store:
        store.build(documents)
        yield store


def test_retrieval_meets_the_quality_budget(index: RagIndex) -> None:
    """REQ-PW-004 — retrieval is measured against labelled questions on every run."""
    cases = load_cases(FIXTURES / "evaluation.json")
    assert len(cases) >= 4

    metrics = evaluate(index, cases)["metrics"]

    assert metrics["recall_at_k"] >= 0.9, metrics
    assert metrics["mrr"] >= 0.8, metrics
    assert metrics["refusal_rate"] <= 0.25, metrics


def test_restricted_documents_require_clearance_and_tenant(index: RagIndex) -> None:
    """REQ-PW-003 — ACLs are applied before scoring, so restricted text never surfaces."""
    question = "Acme incident escalation pager acknowledgement time"

    public_hits = index.search(question, AccessContext(clearance="public", tenants=frozenset({"public"})), k=5)
    assert not [hit for hit in public_hits if hit.chunk.document_id == "incident-runbook"]

    cleared = index.search(question, AccessContext(clearance="restricted", tenants=frozenset({"acme"})), k=5)
    assert [hit for hit in cleared if hit.chunk.document_id == "incident-runbook"]


def test_unknown_classification_fails_closed(tmp_path: Path) -> None:
    """REQ-PW-003 — a document with an unrecognised classification is treated as restricted."""
    (tmp_path / "odd.md").write_text(
        "---\ntitle: Odd document\nclassification: secret-squirrel\ntenants: acme\n---\n"
        "# Odd\nRestricted content that must not leak.\n",
        encoding="utf-8",
    )

    documents = load_corpus(tmp_path)

    assert len(documents) == 1
    assert documents[0].classification == "restricted"


def test_poisoned_document_is_flagged_and_not_obeyed(index: RagIndex) -> None:
    """REQ-RV-003 — an instruction inside a document is surfaced as a finding, not followed."""
    answer = build_answer(
        index,
        "What must a catalog contribution include?",
        AccessContext(clearance="public", tenants=frozenset({"public"})),
    )

    assert answer.guardrail_flags, "the injected instructions must be reported"
    assert any("override" in flag or "exfiltration" in flag for flag in answer.guardrail_flags), answer.guardrail_flags
    rendered = (answer.answer or "").lower()
    assert "system prompt" not in rendered


def test_unanswerable_question_refuses_instead_of_guessing(index: RagIndex) -> None:
    """REQ-PW-003 — with no supporting evidence the service refuses and says why."""
    answer = build_answer(
        index,
        "quantum chromodynamics lattice spacing",
        AccessContext(clearance="public", tenants=frozenset({"public"})),
    )

    assert answer.refused is True
    assert answer.answer is None
    assert answer.reason
