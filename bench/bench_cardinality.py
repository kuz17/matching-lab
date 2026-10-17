"""Benchmark max-cardinality matching solvers. Writes one CSV row per run.

Run from the repo root:  python -m bench.bench_cardinality
Only the solver call is timed; instance generation and checking are not.
"""

from __future__ import annotations

from collections.abc import Iterator

OUT_CSV = "bench/out/cardinality.csv"


def grid() -> Iterator[tuple[str, int, float, int]]:
    """Yield (algo_name, n, avg_degree, seed).

    Two sweeps: vary n at fixed average degree, and vary degree at fixed n.
    """
    raise NotImplementedError


def run_one(algo_name: str, n: int, d: float, seed: int) -> dict:
    """Build the instance (untimed), time the solver with time.perf_counter,
    check the result with matching_size (untimed), and return one row:
    algo, n, d, seed, m (edges), size, phases, seconds.
    """
    raise NotImplementedError


def main(out_csv: str = OUT_CSV) -> None:
    """Loop over grid() and write rows to out_csv, with a header comment
    recording Python/numpy versions and the CPU model.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
