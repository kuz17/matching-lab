"""Tests for matching/cardinality/.

Three independent sources of truth:
  1. networkx.bipartite.hopcroft_karp_matching (reference library)
  2. scipy.sparse.csgraph.maximum_bipartite_matching (second reference)
  3. a König vertex cover certificate (matching/certify/matching.py), needing no library
"""

from __future__ import annotations

import copy
import math

import networkx as nx
import numpy as np
import pytest
from scipy.sparse.csgraph import maximum_bipartite_matching

from matching.cardinality import hopcroft_karp, simple_augmenting, simple_augmenting_recursive
from matching.certify import assert_maximum, matching_size
from matching.instances import deep_chain, gnp, planted_perfect, to_csr, to_networkx

ALGOS = [
    pytest.param(simple_augmenting, id="simple"),
    pytest.param(simple_augmenting_recursive, id="simple_rec"),
    pytest.param(hopcroft_karp, id="hk"),
]
ITERATIVE = [p for p in ALGOS if p.id != "simple_rec"]

N_RANDOM = 240  # seeded random instances per algorithm


def nx_size(n_left, n_right, adj):
    G, top = to_networkx(n_left, n_right, adj)
    return len(nx.bipartite.hopcroft_karp_matching(G, top_nodes=top)) // 2


def scipy_size(n_left, n_right, adj):
    if n_left == 0 or n_right == 0:
        return 0
    mate = maximum_bipartite_matching(to_csr(n_left, n_right, adj), perm_type="column")
    return int(np.count_nonzero(mate >= 0))


def random_instance(seed):
    """Parameters drawn from the seed: mostly small graphs, some medium, rectangular allowed."""
    rng = np.random.default_rng(10_000 + seed)
    hi = 300 if seed % 8 == 0 else 60
    n_left = int(rng.integers(0, hi + 1))
    n_right = int(rng.integers(0, hi + 1))
    p = float(rng.choice([0.0, 0.01, 0.03, 0.05, 0.1, 0.2, 0.5, 0.9]))
    return n_left, n_right, gnp(n_left, n_right, p, seed)


# ---------------------------------------------------------------------------
# Random instances against references and the certificate
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("algo", ALGOS)
@pytest.mark.parametrize("seed", range(N_RANDOM))
def test_random_against_references(algo, seed):
    n_left, n_right, adj = random_instance(seed)
    adj_before = copy.deepcopy(adj)

    mate_l = algo(n_left, n_right, adj)

    assert adj == adj_before, "algorithm mutated its input"
    size = assert_maximum(n_left, n_right, adj, mate_l)
    assert size == nx_size(n_left, n_right, adj)
    assert size == scipy_size(n_left, n_right, adj)


@pytest.mark.parametrize("algo", ALGOS)
@pytest.mark.parametrize("seed", range(40))
def test_planted_perfect(algo, seed):
    n = 1 + seed * 5
    adj = planted_perfect(n, p_extra=0.05, seed=seed)
    mate_l = algo(n, n, adj)
    assert matching_size(n, n, adj, mate_l) == n
    assert all(v != -1 for v in mate_l)


# ---------------------------------------------------------------------------
# Hand-picked edge cases: (n_left, n_right, adj, expected maximum size)
# ---------------------------------------------------------------------------

EDGE_CASES = {
    "empty": (0, 0, [], 0),
    "left_only": (5, 0, [[] for _ in range(5)], 0),
    "right_only": (0, 5, [], 0),
    "no_edges": (4, 4, [[] for _ in range(4)], 0),
    "single_edge": (1, 1, [[0]], 1),
    "isolated_mixed": (5, 5, [[], [2], [], [2, 4], []], 2),
    "complete_5x5": (5, 5, [list(range(5)) for _ in range(5)], 5),
    "complete_3x7": (3, 7, [list(range(7)) for _ in range(3)], 3),
    "complete_7x3": (7, 3, [list(range(3)) for _ in range(7)], 3),
    "star_left": (1, 6, [list(range(6))], 1),
    "star_right": (6, 1, [[0] for _ in range(6)], 1),
    # greedy u -> first neighbour gives 0->0 and blocks 1; max is 2
    "greedy_trap": (2, 2, [[0, 1], [0]], 2),
    # duplicate neighbours violate the contract but must not break anything
    "duplicate_nbrs": (2, 2, [[0, 0, 1], [0, 0]], 2),
    # Hall violation: 3 left vertices share 2 right vertices
    "hall_deficit": (3, 3, [[0, 1], [0, 1], [0, 1, 2]], 3),
    "hall_deficit_strict": (3, 3, [[0, 1], [0, 1], [0, 1]], 2),
    # path of length 5 (L0-R0-L1-R1-L2-R2): perfect matching of size 3
    "path": (3, 3, [[0], [0, 1], [1, 2]], 3),
}


@pytest.mark.parametrize("algo", ALGOS)
@pytest.mark.parametrize("name", list(EDGE_CASES))
def test_edge_cases(algo, name):
    n_left, n_right, adj, expected = EDGE_CASES[name]
    mate_l = algo(n_left, n_right, adj)
    assert assert_maximum(n_left, n_right, adj, mate_l) == expected


@pytest.mark.parametrize("algo", ITERATIVE)
def test_deep_chain_no_recursion_limit(algo):
    """Augmenting path of length ~2n; recursive DFS without care hits RecursionError."""
    n = 5000
    adj = deep_chain(n)
    mate_l = algo(n, n, adj)
    assert matching_size(n, n, adj, mate_l) == n


def test_recursive_fails_on_deep_chain():
    """Documents the limitation: recursion depth grows with path length."""
    with pytest.raises(RecursionError):
        simple_augmenting_recursive(5000, 5000, deep_chain(5000))


# ---------------------------------------------------------------------------
# Hopcroft-Karp specific
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("seed", range(N_RANDOM))
def test_hk_phase_bound(seed):
    r"""Successful phases <= 2*sqrt(s) + 1, where s = maximum matching size.

    After k phases every augmenting path has length >= 2k+1, so the deficit
    s - |M| is at most s/(k+1); each later phase adds >= 1. Take k = ceil(sqrt(s)).
    """
    n_left, n_right, adj = random_instance(seed)
    stats: dict = {}
    mate_l = hopcroft_karp(n_left, n_right, adj, stats=stats)
    s = matching_size(n_left, n_right, adj, mate_l)
    assert "phases" in stats
    assert 0 <= stats["phases"] <= 2 * math.sqrt(s) + 1
    if s > 0:
        assert stats["phases"] >= 1


def test_hk_stats_optional():
    adj = gnp(10, 10, 0.3, seed=0)
    assert hopcroft_karp(10, 10, adj) == hopcroft_karp(10, 10, adj, stats=None)