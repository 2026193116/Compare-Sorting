from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

from sort import SORT_ALGORITHMS


CASES = [
    [],
    [1],
    [1, 1, 1, 1],
    [3, 1, 2, 1],
    list(range(20, -1, -1)),
    [-3, 4, -1, 0, 4],
    [-500, 499, 0, -500, 499],
    [5, -1, 5, 2, 0, -1, 2, 5],
]


def main():
    checks = 0
    failures = 0

    for name, function in SORT_ALGORITHMS:
        for case in CASES:
            original = list(case)
            result = function(case)
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

            if case != original:
                print(
                    "FAIL",
                    name,
                    "modified input in-place:",
                    case,
                )
                failures += 1

    print(
        f"{checks} checks, {failures} failures"
    )

    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
