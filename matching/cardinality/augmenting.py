"""
Baseline maximum-cardinality matching: one augmenting-path search per left vertex. O(V * E).

Contains Iterative(default) and Recusrive DFS 

Contract: see matching/graph.py. Must not mutate adj.
"""

from __future__ import annotations

from matching.graph import FREE, Adj


def simple_augmenting(n_left: int, n_right: int, adj: Adj) -> list[int]:
    """Iterative DFS: no recursion limit"""
    mate_l = [FREE] * n_left
    mate_r = [FREE] * n_right
    seen = [-1] * n_right

    def augment_from(root: int) -> bool:
        stack = [[root, 0]]        # frames [x, i]: i = next neighbour index of x to try
        via = []                   # via[k] = right vertex between stack[k] and stack[k+1]
        while stack:
            x, i = stack[-1]
            if i == len(adj[x]):
                stack.pop()
                if via:
                    via.pop()
                continue

            v = adj[x][i]
            stack[-1][1] += 1      # advance this frame's position
            if seen[v] == root:
                continue
            seen[v] = root

            if mate_r[v] == FREE:
                for k in range(len(via)):
                    mate_l[stack[k][0]] = via[k]
                    mate_r[via[k]] = stack[k][0]

                mate_l[x] = v
                mate_r[v] = x

                return True
            else:
                via.append(v)
                stack.append([mate_r[v], 0])
            
        return False

    for u in range(n_left):
        augment_from(u)
    return mate_l


def simple_augmenting_recursive(n_left: int, n_right: int, adj: Adj) -> list[int]:
    """Recursive DFS: recursion limit"""
    mate_l = [FREE] * n_left
    mate_r = [FREE] * n_right
    seen = [-1] * n_right

    def try_augment(x: int, root: int) -> bool:
        for v in adj[x]:
            if seen[v] != root:
                seen[v] = root
                if mate_r[v] == FREE or try_augment(mate_r[v],root):
                    mate_l[x] = v
                    mate_r[v] = x
                    return True

        return False


    for u in range(n_left): #we search for an augment path starting from u
        try_augment(u,u)
        
    return mate_l




        