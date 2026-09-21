import random, time
from sort import SORT_ALGORITHMS

def main():
    random.seed(2026); data = [random.randrange(-50, 51) for _ in range(1000)]
    print("algorithm,time_ms,valid")
    for name, fn in SORT_ALGORITHMS:
        start=time.perf_counter(); result=fn(data); elapsed=(time.perf_counter()-start)*1000
        print(f"{name},{elapsed:.3f},{result == sorted(data)}")
if __name__ == "__main__": main()
