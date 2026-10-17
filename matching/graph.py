"""Shared graph representation for bipartite problems.

A bipartite graph is (n_left, n_right, adj): adj[u] lists the distinct right
vertices adjacent to left vertex u. Left and right use separate index spaces.
A matching is returned as mate_l, with mate_l[u] the right partner of u or FREE.
"""

from __future__ import annotations

Adj = list[list[int]]
FREE = -1
