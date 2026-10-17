"""Turn raw benchmark CSVs into the markdown tables used in README.md.

Run from the repo root:  python -m bench.report bench/out/cardinality.csv
"""

from __future__ import annotations

import sys


def to_markdown(csv_path: str) -> str:
    """Group rows by (algo, n, d); report median seconds, median phases and number of seeds."""
    raise NotImplementedError


if __name__ == "__main__":
    print(to_markdown(sys.argv[1]))
