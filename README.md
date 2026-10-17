# matching-lab

Classical bipartite matching algorithms in Python, validated against reference
libraries (networkx, scipy) and with independent optimality certificates.

**Status:** work in progress. Nothing below is claimed until it has been run.

| Module | Status |
|---|---|
| `matching/cardinality/` — simple augmenting paths, Hopcroft–Karp | in progress |
| `matching/assignment/lp.py` — assignment LP (Pyomo + HiGHS) | not started |
| `apps/path_cover.py` — min trucks via min path cover | not started |
| `matching/assignment/hungarian.py` — Hungarian, O(n^3) | not started |
| `matching/flow/min_cost_flow.py` — min-cost flow (SSP) | not started |

## Running

```bash
pip install -r requirements.txt
pytest -q
```

## Results

(Tables are added only from actual runs, with the machine and versions recorded.)

## Limits

(To be filled in honestly as modules land.)
