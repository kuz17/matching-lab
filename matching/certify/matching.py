"""Independent checks for bipartite matchings.

``matching_size`` checks that mate_l is a valid matching.
``konig_cover`` builds a vertex cover from a matching. If the cover has the
same size as the matching and covers every edge, the matching is maximum by
weak duality (|M| <= |C| for any matching M and vertex cover C). This proves
optimality without trusting any reference library.
"""

from __future__ import annotations


def matching_size(n_left: int, n_right: int, adj: list[list[int]], mate_l: list[int]) -> int:
    """Return |M| if mate_l is a valid matching of the graph, else raise AssertionError."""
    assert len(mate_l) == n_left, f"mate_l has length {len(mate_l)}, expected {n_left}"
    nbrs = [set(a) for a in adj]
    used: set[int] = set()
    for u, v in enumerate(mate_l):
        if v == -1:
            continue
        assert isinstance(v, int) and 0 <= v < n_right, f"mate_l[{u}] = {v!r} out of range"
        assert v in nbrs[u], f"({u}, {v}) is not an edge"
        assert v not in used, f"right vertex {v} matched twice"
        used.add(v)
    return len(used)


def konig_cover(
    n_left: int, n_right: int, adj: list[list[int]], mate_l: list[int]
) -> tuple[list[int], list[int]]:
    """König's construction: Z = vertices reachable from free left vertices by alternating paths.

    Returns (cover_left, cover_right) = (L \\ Z, R ∩ Z). If M is maximum this is
    a minimum vertex cover of size |M|. If M is not maximum, some free right
    vertex is reachable, and the returned set is either not a cover or too big.
    """
    mate_r = [-1] * n_right
    for u, v in enumerate(mate_l):
        if v != -1:
            mate_r[v] = u
    in_z_left = [mate_l[u] == -1 for u in range(n_left)]
    in_z_right = [False] * n_right
    stack = [u for u in range(n_left) if in_z_left[u]]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v != mate_l[u] and not in_z_right[v]:  # non-matching edge L -> R
                in_z_right[v] = True
                w = mate_r[v]  # matching edge R -> L
                if w != -1 and not in_z_left[w]:
                    in_z_left[w] = True
                    stack.append(w)
    cover_left = [u for u in range(n_left) if not in_z_left[u]]
    cover_right = [v for v in range(n_right) if in_z_right[v]]
    return cover_left, cover_right


def assert_maximum(n_left: int, n_right: int, adj: list[list[int]], mate_l: list[int]) -> int:
    """Assert mate_l is a valid *maximum* matching via a König certificate; return |M|."""
    size = matching_size(n_left, n_right, adj, mate_l)
    cl, cr = konig_cover(n_left, n_right, adj, mate_l)
    in_cl, in_cr = set(cl), set(cr)
    for u in range(n_left):
        if u in in_cl:
            continue
        for v in adj[u]:
            assert v in in_cr, f"edge ({u}, {v}) uncovered: an augmenting path exists"
    assert len(cl) + len(cr) == size, f"cover size {len(cl) + len(cr)} != |M| = {size}"
    return size
