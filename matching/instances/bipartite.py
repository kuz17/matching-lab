"""Seeded random bipartite instance generators.

Graph representation used throughout the repo
---------------------------------------------
A bipartite graph is a triple ``(n_left, n_right, adj)`` where ``adj`` has
length ``n_left`` and ``adj[u]`` is a sorted list of *distinct* right-vertex
indices in ``range(n_right)``. Left and right vertices live in separate index
spaces, so left vertex 3 and right vertex 3 are different vertices.

Every generator takes an explicit integer ``seed`` and is deterministic.
"""

from __future__ import annotations

import numpy as np

from matching.graph import Adj


def gnp(n_left: int, n_right: int, p: float, seed: int) -> Adj:
    """Random bipartite graph: each of the n_left * n_right edges present independently with prob p.

    Each row is sampled as Binomial(n_right, p) neighbours chosen uniformly
    without replacement, which has exactly the G(n_left, n_right, p) row
    distribution but avoids materialising an n_left x n_right matrix.
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"p must be in [0, 1], got {p}")
    rng = np.random.default_rng(seed)
    adj: Adj = []
    for _ in range(n_left):
        k = int(rng.binomial(n_right, p)) if n_right > 0 else 0
        nbrs = rng.choice(n_right, size=k, replace=False) if k > 0 else []
        adj.append(sorted(int(v) for v in nbrs))
    return adj


def avg_degree(n_left: int, n_right: int, d: float, seed: int) -> Adj:
    """Sparse random graph with expected left degree d (i.e. gnp with p = d / n_right)."""
    p = 0.0 if n_right == 0 else min(1.0, d / n_right)
    return gnp(n_left, n_right, p, seed)


def planted_perfect(n: int, p_extra: float, seed: int) -> Adj:
    """n x n graph guaranteed to have a perfect matching.

    A uniformly random permutation sigma is planted (edges u -- sigma(u)),
    then gnp noise with probability p_extra is added on top. The maximum
    matching size is therefore exactly n, independently of any reference.
    """
    rng = np.random.default_rng(seed)
    sigma = rng.permutation(n)
    noise = gnp(n, n, p_extra, seed + 1_000_003)
    return [sorted(set(noise[u]) | {int(sigma[u])}) for u in range(n)]


def deep_chain(n: int) -> Adj:
    """n x n 'staircase' that forces an augmenting path of length about 2n.

    adj[u] = [u + 1, u] for u < n - 1 and adj[n - 1] = [n - 1]. Neighbours are
    deliberately listed larger-index-first, so an algorithm that scans adj[u]
    in order first matches u -> u + 1 for every u < n - 1 and is then left
    with a single augmenting path that walks the whole chain. The unique
    perfect matching is u -> u. Use this to catch recursion-depth bugs.
    (This one is NOT sorted, on purpose; it is the only generator that breaks
    the sorted-adjacency convention.)
    """
    adj = [[u + 1, u] for u in range(n - 1)]
    if n > 0:
        adj.append([n - 1])
    return adj


