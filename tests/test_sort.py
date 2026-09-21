import sys
sys.path.insert(0, "src")
from sort import SORT_ALGORITHMS

cases = [[], [1], [3,1,2,1], list(range(20,0,-1)), [-3,4,-1,0,4]]
failures = 0
for name, fn in SORT_ALGORITHMS:
    for case in cases:
        if fn(case) != sorted(case): print("FAIL", name, case); failures += 1
print(f"{len(SORT_ALGORITHMS)*len(cases)} checks, {failures} failures")
raise SystemExit(failures != 0)
