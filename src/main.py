"""Run every Python sorting implementation in src."""

import argparse
import time

from sort import SORT_ALGORITHMS
from sort_stats import SortStats


def make_input(size, kind):
    """Create the same deterministic inputs as the C implementation."""
    if kind == "random":
        return [
            (index * 73 + 19) % 1000 - 500
            for index in range(size)
        ]

    if kind == "sorted":
        return list(range(size))

    if kind == "reverse":
        return list(range(size, 0, -1))

    if kind == "duplicates":
        return [
            (index * 7 + 3) % 21 - 10
            for index in range(size)
        ]

    raise ValueError(f"Unknown input kind: {kind}")


def run_case(name, values, csv):
    """Run every algorithm once and return whether all results were valid."""
    expected = sorted(values)
    all_valid = True

    for algorithm_name, algorithm in SORT_ALGORITHMS:
        # Match the C implementation: input copying happens
        # before timing starts.
        work = list(values)
        stats = SortStats()

        start = time.perf_counter()
        result = algorithm(
            work,
            stats=stats,
            copy_input=False,
        )
        elapsed = (time.perf_counter() - start) * 1000

        valid = result == expected

        if not valid:
            all_valid = False

        if csv:
            print(
                f"{algorithm_name},{name},{len(values)},"
                f"{stats.comparisons},{stats.moves},"
                f"{elapsed:.3f},{str(valid).lower()}"
            )
        else:
            print(
                f"{algorithm_name:20} "
                f"{name:12} "
                f"{len(values):8} "
                f"{stats.comparisons:12} "
                f"{stats.moves:12} "
                f"{elapsed:10.3f} "
                f"{'yes' if valid else 'NO'}"
            )

    return all_valid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--blocks", action="store_true")
    args = parser.parse_args()

    csv = args.csv or args.blocks
    all_valid = True

    if csv:
        print(
            "algorithm,input,n,comparisons,moves,time_ms,valid"
        )
    else:
        print("=== sorting comparison ===")
        print(
            f"{'algorithm':20} "
            f"{'input':12} "
            f"{'n':>8} "
            f"{'comparisons':12} "
            f"{'moves':12} "
            f"{'time(ms)':10} "
            f"valid"
        )

    if args.blocks:
        for size in (128, 256, 512, 1024, 2048):
            if not run_case(
                "block",
                make_input(size, "random"),
                True,
            ):
                all_valid = False
    else:
        for name in (
            "random",
            "sorted",
            "reverse",
            "duplicates",
        ):
            if not run_case(
                name,
                make_input(2000, name),
                csv,
            ):
                all_valid = False

    raise SystemExit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
