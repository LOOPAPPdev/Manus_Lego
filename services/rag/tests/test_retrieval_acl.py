from __future__ import annotations

from lego_rag.models import AccessContext
from lego_rag.store import RagIndex, _fts_query


def test_index_reports_documents_and_chunks(index: RagIndex) -> None:
    stats = index.stats()
    assert stats["documents"] == 5
    assert stats["chunks"] >= 5


def test_public_query_cannot_reach_restricted_content(index: RagIndex) -> None:
    hits = index.search("Acme incident escalation pager", AccessContext(clearance="public"), k=10)
    document_ids = {hit.chunk.document_id for hit in hits}
    assert "incident-runbook" not in document_ids


def test_restricted_clearance_with_matching_tenant_can_retrieve(index: RagIndex) -> None:
    access = AccessContext(clearance="restricted", tenants=frozenset({"acme"}))
    hits = index.search("Acme incident escalation pager", access, k=5)
    assert hits, "restricted document should be retrievable for the owning tenant"
    assert hits[0].chunk.document_id == "incident-runbook"


def test_tenant_isolation_between_customers(index: RagIndex) -> None:
    other_tenant = AccessContext(clearance="restricted", tenants=frozenset({"globex"}))
    hits = index.search("Acme incident escalation pager", other_tenant, k=10)
    assert all(hit.chunk.document_id != "incident-runbook" for hit in hits)


def test_hybrid_ranking_puts_the_relevant_document_first(index: RagIndex) -> None:
    hits = index.search("D1 Sessions API read replication", AccessContext(), k=4)
    assert hits
    assert hits[0].chunk.document_id == "d1-sessions"
    assert hits[0].lexical_rank is not None or hits[0].vector_rank is not None


def test_lexical_matches_are_reported_for_explainability(index: RagIndex) -> None:
    hits = index.search("streaming responses workers ai", AccessContext(), k=3)
    assert hits[0].chunk.document_id == "workers-ai-chat"
    assert hits[0].matched_terms


def test_empty_query_returns_nothing(index: RagIndex) -> None:
    assert index.search("", AccessContext()) == []
    assert _fts_query("") == ""


def test_fts_expression_is_quoted_against_syntax_injection() -> None:
    expression = _fts_query('sessions" OR * --')
    # FTS5 operators and punctuation are removed, and every surviving token is
    # quoted, so user input cannot inject MATCH syntax.
    assert expression == '"sessions"'
    assert "*" not in expression and "--" not in expression
    assert _fts_query("d1 sessions") == '"d1" OR "sessions"'


def test_scores_are_ordered_and_bounded(index: RagIndex) -> None:
    hits = index.search("template release approval", AccessContext(clearance="internal"), k=5)
    scores = [hit.score for hit in hits]
    assert scores == sorted(scores, reverse=True)
    assert all(0 < score < 1 for score in scores)
