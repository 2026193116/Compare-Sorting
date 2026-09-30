import random
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

from sort import SORT_ALGORITHMS
from sort_stats import SortStats


CASES = [
    [],
    [1],
    [1, 1, 1, 1],
    [3, 1, 2, 1],
    list(range(20, -1, -1)),
    [-3, 4, -1, 0, 4],
    [-500, 499, 0, -500, 499],
    [5, -1, 5, 2, 0, -1, 2, 5],
    list(range(128)),
    list(range(128, 0, -1)),
    [7] * 129,
]


def check_case(name, function, case):
    checks = 0
    failures = 0

    original = list(case)
    stats = SortStats()

    result = function(
        case,
        stats=stats,
    )

    expected = sorted(case)

    checks += 1

    if result != expected:
        print(
            "FAIL",
            name,
            "input=",
            case,
            "result=",
            result,
            "expected=",
            expected,
        )
        failures += 1

    checks += 1

    if case != original:
        print(
            "FAIL",
            name,
            "modified input in-place:",
            case,
        )
        failures += 1

    if name == "countingSort":
        checks += 1

        expected_moves = len(case) if len(case) >= 2 else 0

        if (
            stats.comparisons != 0
            or stats.moves != expected_moves
        ):
            print(
                "FAIL",
                name,
                "unexpected stats:",
                stats,
                "n=",
                len(case),
            )
            failures += 1

    return checks, failures


def main():
    checks = 0
    failures = 0

    for name, function in SORT_ALGORITHMS:
        for case in CASES:
            c, f = check_case(name, function, case)
            checks += c
            failures += f

    rng = random.Random(2026)

    for _ in range(100):
        case = [
            rng.randint(-100, 100)
            for _ in range(rng.randint(0, 200))
        ]

        for name, function in SORT_ALGORITHMS:
            c, f = check_case(name, function, case)
            checks += c
            failures += f

    print(
        f"{checks} checks, {failures} failures"
    )

    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
