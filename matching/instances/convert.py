"""Converters from the repo's graph format to reference-library formats."""

from __future__ import annotations

import numpy as np

from matching.graph import Adj
def to_networkx(n_left: int, n_right: int, adj: Adj):
    """networkx Graph with nodes ('L', u) and ('R', v); returns (G, top_nodes)."""
    import networkx as nx

    G = nx.Graph()
    top = [("L", u) for u in range(n_left)]
    G.add_nodes_from(top, bipartite=0)
    G.add_nodes_from((("R", v) for v in range(n_right)), bipartite=1)
    G.add_edges_from((("L", u), ("R", v)) for u in range(n_left) for v in adj[u])
    return G, top


def to_csr(n_left: int, n_right: int, adj: Adj):
    """scipy CSR biadjacency matrix of shape (n_left, n_right)."""
    from scipy.sparse import csr_matrix

    rows = [u for u in range(n_left) for _ in adj[u]]
    cols = [v for u in range(n_left) for v in adj[u]]
    data = np.ones(len(rows), dtype=np.int8)
    return csr_matrix((data, (rows, cols)), shape=(n_left, n_right))
