"""Tests for the instance generators and the certificate (testing the test harness)."""

from __future__ import annotations

import pytest

from matching.certify import assert_maximum, konig_cover
from matching.instances import avg_degree, deep_chain, gnp, planted_perfect, to_csr, to_networkx


@pytest.mark.parametrize("seed", range(20))
def test_gnp_format_and_determinism(seed):
    a = gnp(30, 17, 0.2, seed)
    b = gnp(30, 17, 0.2, seed)
    assert a == b
    assert len(a) == 30
    for row in a:
        assert row == sorted(set(row))
        assert all(0 <= v < 17 for v in row)


def test_gnp_extremes():
    assert gnp(5, 5, 0.0, 0) == [[] for _ in range(5)]
    assert gnp(5, 5, 1.0, 0) == [list(range(5)) for _ in range(5)]
    assert gnp(0, 5, 0.5, 0) == []
    assert gnp(3, 0, 0.5, 0) == [[], [], []]
    with pytest.raises(ValueError):
        gnp(2, 2, 1.5, 0)


def test_gnp_density_roughly_right():
    adj = gnp(400, 400, 0.05, seed=1)
    m = sum(len(r) for r in adj)
    assert abs(m - 0.05 * 400 * 400) < 5 * (0.05 * 0.95 * 400 * 400) ** 0.5  # within 5 sd


def test_avg_degree():
    adj = avg_degree(2000, 2000, 3.0, seed=2)
    mean = sum(len(r) for r in adj) / 2000
    assert 2.7 < mean < 3.3


@pytest.mark.parametrize("seed", range(10))
def test_planted_has_permutation(seed):
    n = 25
    adj = planted_perfect(n, 0.1, seed)
    G, top = to_networkx(n, n, adj)
    import networkx as nx

    assert len(nx.bipartite.hopcroft_karp_matching(G, top_nodes=top)) // 2 == n


def test_deep_chain_shape():
    adj = deep_chain(4)
    assert adj == [[1, 0], [2, 1], [3, 2], [3]]
    assert deep_chain(0) == []
    assert deep_chain(1) == [[0]]


def test_converters_shapes():
    adj = [[0, 2], [], [1]]
    G, top = to_networkx(3, 4, adj)
    assert G.number_of_nodes() == 7 and G.number_of_edges() == 3
    A = to_csr(3, 4, adj)
    assert A.shape == (3, 4) and A.nnz == 3


def test_certificate_accepts_maximum_and_rejects_non_maximum():
    adj = [[0, 1], [0]]  # max matching {0-1, 1-0}
    assert assert_maximum(2, 2, adj, [1, 0]) == 2
    with pytest.raises(AssertionError):
        assert_maximum(2, 2, adj, [0, -1])  # maximal but not maximum
    with pytest.raises(AssertionError):
        assert_maximum(2, 2, adj, [0, 0])  # not a matching
    with pytest.raises(AssertionError):
        assert_maximum(2, 2, adj, [1, 1])  # (1,1) not an edge


def test_konig_cover_on_path():
    adj = [[0], [0, 1], [1, 2]]
    cl, cr = konig_cover(3, 3, adj, [0, 1, 2])
    assert len(cl) + len(cr) == 3
