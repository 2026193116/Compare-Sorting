# 정렬 비교 보고서 (셸 · 카운팅 · 칵테일 셰이커)

## 1. 과제 개요

이번 과제에서는 세 정렬 알고리즘을 동일한 입력 생성기와 실행 인터페이스로 구현하고, 결과 배열뿐 아니라 비교 횟수·이동 횟수·실행 시간을 함께 측정하였다.

- 비교 대상: 셸 정렬, 카운팅 정렬, 칵테일 셰이커 정렬
- 셸 정렬의 gap 정책: `gap = floor(n/4)`에서 시작한 뒤 매 pass마다 `gap = floor(gap/2)`로 줄이고 `gap = 1` pass를 수행

## 2. 구현 구조와 실험 인터페이스

C에서는 `SortFunction` 함수 포인터와 `SortStats`를 사용하여 모든 알고리즘을 같은 방식으로 호출한다. `sort.c`의 레지스트리는 이름, 복잡도, 안정성, 함수 포인터를 한 목록으로 관리한다.

| 파일 | 역할 |
| --- | --- |
| `src/sortctx.h` | `SortStats`와 `SortFunction` 정의 |
| `src/sort.h` | 정렬 함수와 `SortAlgorithm` 선언 |
| `src/sort.c` | 알고리즘 메타데이터 레지스트리 |
| `src/shellSort.c` | `n/4` 시작 gap을 사용하는 셸 정렬 구현 |
| `src/countingSort.c` | 카운팅 정렬 구현 |
| `src/cocktailShakerSort.c` | 칵테일 셰이커 정렬 구현 |
| `src/main.c` | 입력 생성, 복사, 시간 측정, 결과 검증, CSV 출력 |
| `tests/test_sort.c` | 모든 구현의 경계 조건 검사 |
| `tools/plot.py` | CSV 기반 SVG 그래프 생성 |

## 3. C와 Python 구현

세 알고리즘 모두 오름차순 정렬을 수행한다. C 구현은 작업 배열을 제자리에서 수정하며 통계를 `SortStats`에 기록한다. Python 구현은 입력을 복사한 뒤 정렬된 리스트를 반환한다. 두 언어의 실행 시간은 런타임과 메모리 모델이 다르므로 직접 비교하지 않는다.

셸 정렬은 `floor(n/4), floor(n/8), ..., 1`의 gap 수열을 사용한다. 각 gap에서 gap만큼 떨어진 원소들에 삽입 정렬을 적용한 뒤 다음 gap으로 넘어간다.

## 4. 알고리즘별 원리와 복잡도

### 4.1 셸 정렬

셸 정렬은 배열 전체에 삽입 정렬을 한 번만 적용하지 않고, 일정한 간격의 부분 배열을 먼저 정렬한다. 이 구현에서는 초기 gap을 `floor(n/4)`로 정하고, 매 단계 gap을 절반으로 줄인다. 마지막 `gap = 1` 단계가 일반적인 삽입 정렬에 해당한다.

- **장점:** 추가 배열 없이 동작하며, 큰 gap에서 멀리 떨어진 역순을 먼저 줄여 단순 삽입 정렬보다 빠르다.
- **한계:** 안정적이지 않으며 입력 분포와 gap 수열에 따라 실제 성능이 달라진다.
- **복잡도:** 추가 공간 `O(1)`, 최선 `O(n log n)`, 평균 `O(n^1.5)`, 최악 `O(n^2)`로 정리한다. 이는 `gap = floor(n/4)`에서 시작해 절반씩 줄이는 수열을 기준으로 한 보고서상의 분석이다.

### 4.2 카운팅 정렬

최솟값과 최댓값을 구하고 `k = max - min + 1` 크기의 빈도 배열을 만든다. 시간 복잡도는 `O(n + k)`, 추가 공간은 `O(n + k)`이다.

### 4.3 칵테일 셰이커 정렬

왼쪽에서 오른쪽, 오른쪽에서 왼쪽으로 인접 원소를 비교하는 pass를 반복한다. 최선 `O(n)`, 평균·최악 `O(n²)`, 추가 공간 `O(1)`이다.

## 5. 실험 방법과 시각화

`main.c`는 `random`, `sorted`, `reverse`, `duplicates` 입력을 각각 `n = 2000`으로 만들고, 각 알고리즘의 비교 횟수·이동 횟수·실행 시간을 기록한다. `make charts`는 CSV를 갱신하고 `tools/plot.py`를 실행해 `report/` 아래 SVG를 생성한다.

### 이론적 복잡도

![복잡도 개념 그래프](complexity.svg)

### 입력 형태에 따른 실행 시간

![입력 형태별 실행 시간](input-time.svg)

### 입력 형태에 따른 비교 횟수

![입력 형태별 비교 횟수](input-comparisons.svg)

### 입력 형태에 따른 이동 횟수

![입력 형태별 이동 횟수](input-moves.svg)

### 입력 크기 증가에 따른 시간 변화

![입력 크기별 실행 시간](scale-time.svg)

측정 시간은 실행 환경에 따라 달라지므로 특정 숫자보다 곡선의 방향과 알고리즘별 상대 차이를 해석한다.

## 6. 결과 해석

| 알고리즘 | 최선 | 평균 | 최악 | 추가 공간 | 안정성 |
| --- | --- | --- | --- | --- | --- |
| 셸 정렬 | `O(n log n)` | `O(n^1.5)` | `O(n²)` | `O(1)` | 아니오 |
| 카운팅 정렬 | `O(n+k)` | `O(n+k)` | `O(n+k)` | `O(n+k)` | 예(현재 구현 방식) |
| 칵테일 셰이커 | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | 예 |

초기 gap을 `n/4`로 두면 큰 순서 오류를 먼저 줄일 수 있고, gap이 1에 가까워질수록 삽입 정렬처럼 세밀하게 정리한다. 입력 크기가 커질수록 칵테일 셰이커 정렬의 이차적 증가가 가장 뚜렷하며, 셸 정렬은 같은 조건에서 더 완만하게 증가할 것으로 예상된다.

## 7. 결론

셸 정렬은 gap 수열을 명시하지 않으면 복잡도를 하나의 수식으로 고정하기 어렵다. 본 구현과 분석에서는 `floor(n/4)`를 시작 gap으로 사용하고 절반씩 줄이는 정책을 명시하여, 보고서의 최선·평균·최악 복잡도를 코드와 일치시켰다.

## 참고 자료

1. [Wikipedia — Sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm)
2. [Wikipedia — Shellsort](https://en.wikipedia.org/wiki/Shellsort)
3. [Wikipedia — Counting sort](https://en.wikipedia.org/wiki/Counting_sort)
4. [Wikipedia — Cocktail shaker sort](https://en.wikipedia.org/wiki/Cocktail_shaker_sort)
5. [강의 실습 template](https://github.com/lec-algorithm/hw1-sample-2026)
