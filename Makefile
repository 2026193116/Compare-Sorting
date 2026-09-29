CC ?= gcc
CFLAGS ?= -std=c17 -Wall -Wextra -O2
DEBUGFLAGS ?= -std=c17 -Wall -Wextra -g -O0

SORT_SRC = src/sort.c src/shellSort.c src/countingSort.c src/cocktailShakerSort.c

.PHONY: all run test test-c test-py charts clean debug

all: test

run: src/main.out
	@./src/main.out

test: test-c test-py

test-c: tests/test_sort.out
	@echo "Running C tests..."
	@./tests/test_sort.out

test-py:
	@echo "Running Python tests..."
	@python3 tests/test_sort.py

charts: src/main.out
	@mkdir -p report
	@./src/main.out --csv --blocks > report/results.csv
	@python3 tools/plot.py

debug: src/main.debug.out

src/main.out: src/main.c $(SORT_SRC) src/sort.h src/sortctx.h
	$(CC) $(CFLAGS) -Isrc -o $@ src/main.c $(SORT_SRC)

tests/test_sort.out: tests/test_sort.c $(SORT_SRC) src/sort.h src/sortctx.h
	$(CC) $(CFLAGS) -Isrc -o $@ tests/test_sort.c $(SORT_SRC)

src/main.debug.out: src/main.c $(SORT_SRC) src/sort.h src/sortctx.h
	$(CC) $(DEBUGFLAGS) -Isrc -o $@ src/main.c $(SORT_SRC)

%.out: %.c
	$(CC) $(CFLAGS) -I$(@D) -o $@ $<

clean:
	rm -f src/*.out tests/*.out report/results.csv
