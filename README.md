# Compare-Sorting

2026-2 고급알고리즘 과제 1 — **셸 정렬 · 카운팅 정렬 · 칵테일 셰이커 정렬**을 같은 입력 조건과 실행 환경에서 비교합니다.

## 실행

```sh
docker compose up -d
docker compose exec lab bash

make test
make run
make charts
make sanitize
```

Python 구현은 다음처럼 실행합니다.

```sh
python3 src/main.py
python3 src/main.py --csv
```

`make run`과 `python3 src/main.py`는 정렬 결과를 검증하고, 하나라도 실패하면 비정상 종료 코드(1)를 반환합니다.

## 비교 대상

| 알고리즘 | 과제 구분 | 시간 복잡도 | 추가 공간 | 안정성 |
| --- | --- | --- | --- | --- |
| 셸 정렬 | 배운 정렬 | gap sequence에 의존, 본 구현 최악 `O(n²)` | `O(1)` | 불안정 |
| 카운팅 정렬 | 배운 정렬 | `O(n + k)` | `O(n + k)` | 안정 |
| 칵테일 셰이커 정렬 | 배우지 않은 정렬 | 평균/최악 `O(n²)`, 최선 `O(n)` | `O(1)` | 안정 |

셸 정렬은 `gap = floor(n/4)`에서 시작하여 절반씩 감소시키고 마지막에 `gap = 1`인 삽입 정렬 pass를 수행합니다.

카운팅 정렬의 `k`는 입력의 최댓값과 최솟값 사이에 포함되는 정수 값의 개수이며, 값의 범위가 매우 크면 추가 메모리 사용량도 크게 증가할 수 있습니다.

## 입력 생성

입력 생성은 C와 Python에서 동일한 결정적 수식을 사용합니다.

- `random`: `(i * 73 + 19) % 1000 - 500`으로 생성되는 결정적 의사 무작위 형태
- `sorted`: `[0, 1, 2, ..., n-1]`
- `reverse`: `[n, n-1, ..., 2, 1]`
- `duplicates`: `(i * 7 + 3) % 21 - 10`으로 생성되는 중복이 많은 입력

`random`은 별도의 난수 seed를 사용하는 방식이 아니라 수식에 의해 재현 가능한 입력을 만드는 방식입니다.

## 저장소 구조

```text
src/
  sort.h
  sortctx.h
  sort.c
  shellSort.c
  countingSort.c
  cocktailShakerSort.c
  main.c

  sort.py
  sort_stats.py
  shell_sort.py
  counting_sort.py
  cocktail_shaker_sort.py
  main.py

tests/
  test_sort.c
  test_sort.py

tools/
  plot.py

report/
  REPORT.md
  algorithm-flow.html
  results.csv
  *.svg
```

## 테스트

```sh
make test
```

C와 Python 테스트를 모두 실행합니다.

C 테스트는 빈 배열, 단일 원소, 정렬/역순/중복 입력, 음수, `n=128`, `n=129`, `n=257` 등의 경계 및 대표 사례를 검사하며 `qsort()`를 기준 정답으로 사용합니다.

Python 테스트는 고정된 기본 사례와 seed `2026`의 randomized regression 100개를 검사합니다.

## 그래프 생성

```sh
make charts
```

다음 파일을 생성합니다.

- [복잡도 개념 그래프](report/complexity.svg)
- [입력 형태별 실행 시간](report/input-time.svg)
- [입력 형태별 비교 횟수](report/input-comparisons.svg)
- [입력 형태별 이동 횟수](report/input-moves.svg)
- [입력 크기별 실행 시간](report/scale-time.svg)

`complexity.svg`는 실제 측정값이 아니라 이론적 증가 형태를 개념적으로 나타낸 그래프입니다.

## 메모리 안전성 검사

```sh
make sanitize
```

AddressSanitizer와 UndefinedBehaviorSanitizer를 사용하여 C 실행 파일을 검사합니다.

## 보고서 및 시각자료

- [정렬 비교 보고서](report/REPORT.md)
- [알고리즘 단계별 인터랙티브 시각화](report/algorithm-flow.html)
- [복잡도 개념 그래프](report/complexity.svg)
- [입력 형태별 실행 시간](report/input-time.svg)
- [입력 형태별 비교 횟수](report/input-comparisons.svg)
- [입력 형태별 이동 횟수](report/input-moves.svg)
- [입력 크기별 실행 시간](report/scale-time.svg)

> 측정 시간은 실행 환경과 시스템 부하에 따라 달라질 수 있으므로, 비교 횟수·이동 횟수와 함께 해석합니다.
