"""Baseline maximum-cardinality matching: one augmenting-path search per left vertex. O(V * E).

Contract: see matching/graph.py. Must not mutate adj.
"""

from __future__ import annotations

from matching.graph import FREE, Adj


def simple_augmenting(n_left: int, n_right: int, adj: Adj) -> list[int]:
    raise NotImplementedError
