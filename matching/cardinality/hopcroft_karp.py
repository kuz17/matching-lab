"""Hopcroft-Karp maximum-cardinality matching. O(E * sqrt(V)).

Contract: see matching/graph.py. Must not mutate adj.
"""

from __future__ import annotations

from matching.graph import FREE, Adj


def hopcroft_karp(n_left: int, n_right: int, adj: Adj, stats: dict | None = None) -> list[int]:
    """If stats is a dict, set stats["phases"] = number of phases that augmented at least once."""
    raise NotImplementedError
