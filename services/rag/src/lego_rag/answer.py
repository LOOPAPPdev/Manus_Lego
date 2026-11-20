"""Answer construction: extractive by default, citation-first, refusal-safe.

The default answerer never calls a model. It selects the sentences from the
retrieved chunks that best cover the question terms, and it refuses when the
retrieval evidence is too weak. This makes the pipeline testable and removes the
most common failure mode of RAG demos: a confident answer with no support.
"""

from __future__ import annotations

import re
from collections.abc import Callable

from . import guardrails
from .chunking import content_tokens, tokenize
from .models import AccessContext, Answer, Citation, Hit
from .store import RagIndex

SENTENCE = re.compile(r"(?<=[.!?])\s+")
MAX_EXCERPT = 280


class Retriever:
    """Convenience wrapper binding an index and an access context."""

    def __init__(self, index: RagIndex, access: AccessContext | None = None) -> None:
        self.index = index
        self.access = access or AccessContext()

    def search(self, question: str, *, k: int = 5) -> list[Hit]:
        return self.index.search(question, self.access, k=k)

    def answer(
        self,
        question: str,
        *,
        k: int = 4,
        synthesizer: Callable[[str, list[Hit]], str] | None = None,
    ) -> Answer:
        return build_answer(self.index, question, self.access, k=k, synthesizer=synthesizer)


def _excerpt(text: str) -> str:
    collapsed = " ".join(text.split())
    return collapsed[:MAX_EXCERPT] + ("…" if len(collapsed) > MAX_EXCERPT else "")


def _best_sentences(question: str, hits: list[Hit], limit: int = 2) -> list[str]:
    terms = set(tokenize(question))
    candidates: list[tuple[int, str]] = []
    for hit in hits:
        for sentence in SENTENCE.split(hit.chunk.text):
            cleaned = " ".join(sentence.split())
            if len(cleaned) < 30:
                continue
            overlap = len(terms.intersection(tokenize(cleaned)))
            if overlap:
                candidates.append((overlap, cleaned))
    candidates.sort(key=lambda item: (-item[0], -len(item[1])))
    return [sentence for _, sentence in candidates[:limit]]


def build_answer(
    index: RagIndex,
    question: str,
    access: AccessContext,
    *,
    k: int = 4,
    synthesizer: Callable[[str, list[Hit]], str] | None = None,
) -> Answer:
    hits = index.search(question, access, k=k)
    if not hits:
        return Answer(
            question=question,
            answer=None,
            refused=True,
            reason="no permitted document matched the question",
            hits=[],
        )

    # A hit is only evidence if it overlaps a *content* term of the question.
    # Stopword overlap ("for", "the") is not support.
    question_terms = set(content_tokens(question))
    supported = [
        hit
        for hit in hits
        if question_terms.intersection(hit.matched_terms)
        and (hit.lexical_rank is not None or hit.vector_rank is not None)
    ]
    flags: list[str] = []
    for hit in hits:
        for finding in guardrails.scan(hit.chunk.text):
            flag = f"{finding.rule}@{hit.chunk.id}"
            if flag not in flags:
                flags.append(flag)

    if not supported:
        return Answer(
            question=question,
            answer=None,
            refused=True,
            reason="retrieval produced only weak vector matches without lexical support",
            guardrail_flags=flags,
            hits=hits,
        )

    citations = [
        Citation(
            document_id=hit.chunk.document_id,
            title=hit.document_title,
            source=hit.source,
            chunk_id=hit.chunk.id,
            excerpt=_excerpt(hit.chunk.text),
        )
        for hit in supported[:3]
    ]

    if synthesizer is not None:
        context = "\n\n".join(guardrails.wrap_untrusted(hit.chunk.text, hit.citation) for hit in supported)
        prompt = (
            "Answer the question using only the untrusted documents below. "
            "Cite each claim with [n]. If the documents do not support an answer, reply exactly: INSUFFICIENT_EVIDENCE.\n\n"
            f"Question: {question}\n\n{context}"
        )
        try:
            generated = synthesizer(prompt, supported).strip()
        except Exception as exc:  # a model failure must degrade, not crash
            generated = ""
            flags.append(f"synthesizer_error:{type(exc).__name__}")
        if not generated or "INSUFFICIENT_EVIDENCE" in generated:
            return Answer(
                question=question,
                answer=None,
                refused=True,
                reason="the synthesiser could not support an answer from the retrieved documents",
                citations=citations,
                guardrail_flags=flags,
                hits=hits,
            )
        return Answer(
            question=question,
            answer=generated,
            citations=citations,
            guardrail_flags=flags,
            hits=hits,
        )

    sentences = _best_sentences(question, supported)
    if not sentences:
        return Answer(
            question=question,
            answer=None,
            refused=True,
            reason="retrieved chunks did not contain a sentence covering the question",
            citations=citations,
            guardrail_flags=flags,
            hits=hits,
        )

    lead = supported[0]
    body = " ".join(sentences)
    answer = f"{body} [{lead.document_title} — {lead.citation}]"
    return Answer(
        question=question,
        answer=answer,
        citations=citations,
        guardrail_flags=flags,
        hits=hits,
    )
