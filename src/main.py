"""Run every Python sorting implementation in src."""

import argparse
import random
import time

from sort import SORT_ALGORITHMS


def make_input(size, kind):
    if kind == "sorted":
        return list(range(size))
    if kind == "reverse":
        return list(range(size, 0, -1))
    if kind == "duplicates":
        return [(index * 7 + 3) % 21 - 10 for index in range(size)]
    random.seed(2026 + size)
    return [random.randrange(-500, 500) for _ in range(size)]


def run_case(name, values, csv):
    expected = sorted(values)
    for algorithm_name, algorithm in SORT_ALGORITHMS:
        start = time.perf_counter()
        result = algorithm(values)
        elapsed = (time.perf_counter() - start) * 1000
        valid = result == expected
        if csv:
            print(f"{algorithm_name},{name},{len(values)},,,{elapsed:.3f},{str(valid).lower()}")
        else:
            print(f"{algorithm_name:20} {name:12} {len(values):8} {elapsed:10.3f} {'yes' if valid else 'NO'}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--blocks", action="store_true")
    args = parser.parse_args()

    csv = args.csv or args.blocks
    if csv:
        print("algorithm,input,n,comparisons,moves,time_ms,valid")
    else:
        print("=== sorting comparison ===")
        print(f"{'algorithm':20} {'input':12} {'n':8} {'time(ms)':10} valid")

    if args.blocks:
        for size in (128, 256, 512, 1024, 2048):
            run_case("block", make_input(size, "random"), True)
    else:
        for name in ("random", "sorted", "reverse", "duplicates"):
            run_case(name, make_input(2000, name), csv)


if __name__ == "__main__":
    main()
