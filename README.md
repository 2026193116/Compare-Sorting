# Compare-Sorting

2026-2 고급알고리즘 과제 1 — **셸 정렬 · 카운팅 정렬 · 칵테일 셰이커 정렬**을 같은 입력과 같은 실행 환경에서 비교합니다.

## 실행

```sh
docker compose up -d
docker compose exec lab bash
make test
make run
make charts
```

`make run`은 C 구현의 비교 표와 검증 결과를 출력합니다. `make charts`는 고정된 실험 결과를 `report/results.csv`에 저장하고 표준 Python 모듈만으로 SVG 그래프를 다시 만듭니다.

Python 구현은 다음처럼 실행합니다.

```sh
python3 src/main.py
```

## 비교 대상

| 알고리즘 | 과제 구분 | 평균 시간 복잡도 | 추가 공간 | 안정성 |
| --- | --- | --- | --- | --- |
| 셸 정렬 | 배운 정렬 | gap 수열에 따라 보통 `O(n^1.5)` 안팎, 최악은 수열에 의존 | `O(1)` | 불안정 |
| 카운팅 정렬 | 배운 정렬 | `O(n + k)` | `O(n + k)` | 안정 구현 가능 |
| 칵테일 셰이커 정렬 | 배우지 않은 정렬 | `O(n²)`, 최선 `O(n)` | `O(1)` | 안정 |

`k`는 입력의 최댓값과 최솟값 사이의 값 범위입니다. 따라서 카운팅 정렬은 값의 범위가 작고 정수인 입력에서 특히 유리합니다.

## 저장소 구조

```text
src/       sort.h, sort.c, shellSort.c, countingSort.c, cocktailShakerSort.c
           main.c, sort.py, main.py
tests/     test_sort.c, test_sort.py
tools/     plot.py
report/    REPORT.md, algorithm-flow.html, *.svg, results.csv
```

모든 C 빌드는 `Makefile`을 거치며 실행 파일은 `*.out`으로 생성됩니다. 외부 라이브러리는 사용하지 않습니다.

## 보고서와 시각자료

- [정렬 비교 보고서](report/REPORT.md)
- [알고리즘 단계별 인터랙티브 시각화](report/algorithm-flow.html)
- [복잡도 비교 그래프](report/complexity.svg)
- [입력별 예상 동작 그래프](report/input-behavior.svg)

> 보고서의 측정 수치는 실행 환경에 따라 달라질 수 있으므로, 재현 가능한 비교를 위해 비교 횟수·이동 횟수와 함께 해석합니다.
