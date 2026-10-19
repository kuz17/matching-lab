"""
Hopcroft-Karp maximum-cardinality matching. O(E * sqrt(V)).

Each phase: a BFS layers the graph from all free left vertices and finds the
shortest augmenting-path length; then one DFS per free left vertex finds a
maximal set of vertex-disjoint shortest augmenting paths and flips them.

Contract: see matching/graph.py. Must not mutate adj.
"""

from __future__ import annotations

from collections import deque

from matching.graph import FREE, Adj


def hopcroft_karp(n_left: int, n_right: int, adj: Adj, stats: dict | None = None) -> list[int]:
    """
    Maximum-cardinality bipartite matching by Hopcroft-Karp; returns mate_l.
    stats gives number of phases
    """
    INF = n_left + n_right + 1
    mate_l = [FREE] * n_left
    mate_r = [FREE] * n_right
    dist = [INF] * n_left
    limit = INF

    def bfs() -> bool:
        nonlocal limit
        q = deque()
        for u in range(n_left):
            if mate_l[u] == FREE:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF

        limit = INF
        while q:
            x = q.popleft()
            if dist[x] >= limit:     # don't expand past the shortest layer
                continue
            for v in adj[x]:
                if mate_r[v] == FREE:            # free right vertex: shortest layer found
                    limit = dist[x]
                else:                            # follow the matching edge back to the left
                    w = mate_r[v]
                    if dist[w] == INF:
                        dist[w] = dist[x] + 1
                        q.append(w)

        return limit != INF

    def dfs_from(root: int) -> bool:
        """
        Iterative DFS along layers (same frame structure as augmenting.augment_from).

        Uses v if it is free and x is in the last layer, or if v's mate is exactly
        one layer deeper.
        """
        stack = [[root, 0]]
        via = []
        while stack:
            x, i = stack[-1]
            if i == len(adj[x]):     # dead end
                dist[x] = INF        # keeps each phase O(E): x is never entered again
                stack.pop()
                if via:
                    via.pop()
                continue

            v = adj[x][i]
            stack[-1][1] += 1

            if mate_r[v] == FREE:
                if dist[x] == limit:             # shortest augmenting path found: flip it
                    for k in range(len(via)):
                        mate_l[stack[k][0]] = via[k]
                        mate_r[via[k]] = stack[k][0]
                    mate_l[x] = v
                    mate_r[v] = x
                    return True
            elif dist[mate_r[v]] == dist[x] + 1:  # go one layer deeper
                via.append(v)
                stack.append([mate_r[v], 0])

        return False

    phases = 0
    while bfs():
        augmented = False
        for u in range(n_left):
            if mate_l[u] == FREE and dfs_from(u):
                augmented = True        # for a correct phase: bfs() found a shortest augmenting path and some DFS realises it
        if augmented:
            phases += 1
    if stats is not None:
        stats["phases"] = phases
    return mate_l