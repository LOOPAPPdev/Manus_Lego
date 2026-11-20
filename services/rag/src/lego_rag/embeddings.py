"""Embedding backends.

The default backend is a signed hashing embedder: deterministic, offline, no model
download, and good enough to make retrieval *measurable*. It is explicitly a
baseline, not a semantic model — the evaluation harness exists so that swapping it
is a data-driven decision (see README and docs/decisions/0007-rag-design.md).
"""

from __future__ import annotations

import hashlib
import math
from collections import Counter
from typing import Protocol

from .chunking import tokenize


class Embedder(Protocol):
    name: str
    dim: int

    def embed(self, text: str) -> list[float]: ...


class HashingEmbedder:
    """Signed feature hashing with sublinear term frequency and L2 normalisation."""

    name = "hashing-v1"
    dim = 256

    def __init__(self, dim: int = 256) -> None:
        if dim < 32:
            raise ValueError("dim must be at least 32")
        self.dim = dim

    def _bucket(self, token: str) -> tuple[int, float]:
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        index = value % self.dim
        sign = 1.0 if (value >> 63) & 1 else -1.0
        return index, sign

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dim
        counts = Counter(tokenize(text))
        if not counts:
            return vector
        for token, count in counts.items():
            index, sign = self._bucket(token)
            vector[index] += sign * (1.0 + math.log(count))
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return 0.0
    return sum(x * y for x, y in zip(a, b, strict=True))
