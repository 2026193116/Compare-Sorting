# Compare-Sorting 과제 제출 저장소

2026-2 고급알고리즘 과제 1 — **셸 정렬 · 카운팅 정렬 · 칵테일 셰이커 정렬** 구현 및 비교 분석

## 저장소 개요

이 저장소는 세 가지 정렬 알고리즘(셸 정렬, 카운팅 정렬, 칵테일 셰이커 정렬)을 C언어와 Python으로 구현하고, 동일한 입력 조건과 측정 기준으로 성능을 비교 분석하는 과제입니다.

## 구현 대상 알고리즘

### 1. 셸 정렬 (Shell Sort)
- **초기 gap**: floor(n/4)
- **감소 방식**: gap /= 2
- **시간 복잡도**: O(n^1.5) 평균
- **추가 공간**: O(1)
- **안정성**: 불안정

### 2. 카운팅 정렬 (Counting Sort)
- **특징**: 음수 입력 지원, min 기반 오프셋 사용
- **시간 복잡도**: O(n+k)
- **추가 공간**: O(n+k)
- **안정성**: 안정

### 3. 칵테일 셰이커 정렬 (Cocktail Shaker Sort)
- **특징**: 양방향 pass 구조, 조기 종료 최적화
- **시간 복잡도**: O(n²) 평균, O(n) 최선
- **추가 공간**: O(1)
- **안정성**: 안정

## 파일 구조

### C 구현
- `src/shellSort.c`: 셸 정렬 C 코드
- `src/countingSort.c`: 카운팅 정렬 C 코드
- `src/cocktailShakerSort.c`: 칵테일 셰이커 정렬 C 코드
- `src/sort.h`: 정렬 함수 선언, SortStats 구조체
- `src/sort.c`: 알고리즘 레지스트리
- `src/main.c`: 입력 생성, 측정, 검증

### Python 구현
- `src/shell_sort.py`: 셸 정렬 Python 코드
- `src/counting_sort.py`: 카운팅 정렬 Python 코드
- `src/cocktail_shaker_sort.py`: 칵테일 셰이커 정렬 Python 코드
- `src/sort.py`: 알고리즘 레지스트리
- `src/main.py`: 입력 생성, 측정, 검증

### 테스트
- `tests/test_sort.c`: C 단위 테스트
- `tests/test_sort.py`: Python 단위 테스트

### 보고서 및 자료
- `report/REPORT.md`: 정렬 알고리즘 분석 보고서
- `report/algorithm-flow.html`: 알고리즘 단계별 인터랙티브 시각화
- `report/results.csv`: 실험 결과 데이터
- `tools/plot.py`: CSV를 SVG 그래프로 변환

## 실행 방법

### 환경 설정
```sh
docker compose up -d
docker compose exec lab bash
```

### 테스트 실행
```sh
make test   # C와 Python 테스트 모두 실행
```

### C 구현 실행
```sh
make run    # 정렬 결과 비교표 출력
```

### Python 구현 실행
```sh
python3 src/main.py          # 표준 출력
python3 src/main.py --csv    # CSV 형식 출력
```

### 그래프 생성
```sh
make charts  # 실험 실행 후 report/results.csv 생성 및 SVG 그래프 생성
```

## 실험 조건

### 입력 패턴 (n=2000)
- **random**: 무작위 배열 (seed 기반)
- **sorted**: 이미 정렬된 배열 (0 to 1999)
- **reverse**: 역순 배열 (1999 to 0)
- **duplicates**: 중복 값이 많은 배열

### 측정 항목
- **비교 횟수**: 두 원소 비교 연산 횟수
- **이동 횟수**: 원소 배치/교환 횟수 (정의는 알고리즘별로 상이)
- **실행 시간**: 밀리초 단위 측정
- **검증**: 정렬 결과 정확성 확인

## 구현 특징

### C와 Python의 동일성
- 동일한 입력 생성 방식
- 동일한 알고리즘 로직
- 통일된 비교/이동 횟수 정의
- 동일한 검증 기준

### 이동 횟수의 정의

**셸 정렬**
- 원소가 한 칸 이동할 때마다 1회 증가

**카운팅 정렬**
- 최종 배열로 복사할 때만 n회 증가 (n = 배열 크기)

**칵테일 셰이커 정렬**
- 한 번의 교환을 3회 이동으로 카운팅 (임시 변수 포함)

## 빌드 설정

- **컴파일러**: GCC (C17 표준)
- **컴파일 플래그**: `-Wall -Wextra -O2`
- **외부 의존성**: 없음 (표준 라이브러리만 사용)
- **경고**: 모두 제거됨

## 보고서

[정렬 비교 보고서](report/REPORT.md)에서 다음을 다룹니다:
- 각 알고리즘의 원리와 시간복잡도
- C 및 Python 구현 코드 설명
- 실험 설계 및 실행 방법
- 결과 분석 및 해석
- 알고리즘 선택 기준
