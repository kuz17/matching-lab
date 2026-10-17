# matching-lab

Classical bipartite matching algorithms in Python, validated against reference
libraries (networkx, scipy) and with independent optimality certificates.

**Status:** work in progress. Nothing below is claimed unless it has been run.

| Module | Status |
|---|---|
| `matching/cardinality/augmenting.py` — augmenting paths, iterative + recursive | done, tests pass |
| `matching/cardinality/hopcroft_karp.py` — Hopcroft–Karp | in progress |
| `matching/assignment/lp.py` — assignment LP (Pyomo + HiGHS) | not started |
| `apps/path_cover.py` — min trucks via min path cover | not started |
| `matching/assignment/hungarian.py` — Hungarian, O(n^3) | not started |
| `matching/flow/min_cost_flow.py` — min-cost flow (SSP) | not started |

## Running

```bash
pip install -r requirements.txt        # or requirements.lock for the exact versions used
pytest -q
```

## Validation

Every maximum-cardinality solver is checked three independent ways:

1. **networkx** `hopcroft_karp_matching` (reference library),
2. **scipy** `maximum_bipartite_matching` (second reference),
3. a **König vertex-cover certificate** (`matching/certify/matching.py`): from the
   returned matching $M$ it builds a vertex cover $C$ and checks $|C| = |M|$ and that
   $C$ covers every edge. Since $|M| \le |C|$ for any matching and any cover, this
   proves $M$ is maximum without trusting any library.

Instances: 240 seeded random graphs per solver (sizes 0–300, rectangular allowed,
densities 0–0.9), 40 graphs with a planted perfect matching, 16 hand-picked edge
cases (empty, isolated vertices, Hall deficit, greedy trap, …), and a 5000-vertex
chain whose only augmenting path has about 10,000 edges.

**Run so far** (2026-10-17, Python 3.14, versions in `requirements.lock`):

`pytest -q -k "simple or recursive"`: **594 passed**.

| Test | `simple` (iterative) | `simple_rec` (recursive) |
|---|---|---|
| Random graphs vs networkx, scipy and the König certificate | 240 | 240 |
| Planted perfect matching (answer known to be $n$) | 40 | 40 |
| Hand-picked edge cases | 16 | 16 |
| Deep chain (5000 vertices): must succeed | 1 | – |
| Deep chain: must raise `RecursionError` | – | 1 |
| **Total** | **297** | **297** |

## Results

Benchmarks have not been run yet. Tables will be added from `bench/` runs, with
the machine, Python version and number of seeds recorded next to each table.

## Limits

- Pure Python. No compiled code (numba/C), so absolute runtimes are slow.
- `simple_augmenting` is $O(VE)$; it is a baseline, not meant for large graphs.
- `simple_augmenting_recursive` raises `RecursionError` when an augmenting path
  exceeds Python's recursion limit (about 1000). A test asserts this on the deep
  chain. It is kept only for comparison; `simple_augmenting` is the iterative default.

## How this was built

The repository skeleton was generated with Claude (Anthropic): the layout, the
instance generators (`matching/instances/`), the graph contract
(`matching/graph.py`), the König certificate (`matching/certify/`), the test suite
(`tests/`) and the benchmark stubs (`bench/`). The algorithm implementations
(`matching/cardinality/`) are written by me, with code review from Claude.