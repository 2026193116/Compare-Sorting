#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "sort.h"

typedef struct {
    const char *name;
    size_t size;
} InputSpec;

static const InputSpec SPECS[] = {
    {"random", 2000},
    {"sorted", 2000},
    {"reverse", 2000},
    {"duplicates", 2000}
};

static int same_array(
    const int lhs[],
    const int rhs[],
    size_t n
) {
    for (size_t i = 0; i < n; ++i) {
        if (lhs[i] != rhs[i]) {
            return 0;
        }
    }
    return 1;
}

static int compare_ints(const void *lhs, const void *rhs) {
    const int a = *(const int *)lhs;
    const int b = *(const int *)rhs;

    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

static void make_input(int values[], size_t n, size_t kind) {
    for (size_t i = 0; i < n; ++i) {
        switch (kind) {
            case 0:
                values[i] = (int)((i * 73U + 19U) % 1000U) - 500;
                break;
            case 1:
                values[i] = (int)i;
                break;
            case 2:
                values[i] = (int)(n - i);
                break;
            default:
                values[i] = (int)((i * 7U + 3U) % 21U) - 10;
                break;
        }
    }
}

static void print_result(const char *algorithm, const char *input,
                         size_t n, const SortStats *stats, double ms,
                         int csv, int valid) {
    if (csv) {
        printf("%s,%s,%zu,%llu,%llu,%.3f,%s\n", algorithm, input, n,
               stats->comparisons, stats->moves, ms, valid ? "true" : "false");
    } else {
        printf("%-20s %-12s %8zu %12llu %12llu %10.3f %s\n",
               algorithm, input, n, stats->comparisons, stats->moves, ms,
               valid ? "yes" : "NO");
    }
}

static int run_case(
    const InputSpec *spec,
    size_t kind,
    int csv
) {
    int *input = malloc(spec->size * sizeof *input);
    int *work = malloc(spec->size * sizeof *work);
    int *expected = malloc(spec->size * sizeof *expected);

    if (!input || !work || !expected) {
        free(input);
        free(work);
        free(expected);
        return 0;
    }

    make_input(input, spec->size, kind);

    memcpy(
        expected,
        input,
        spec->size * sizeof *expected
    );

    /*
     * Build the expected result before timing the
     * individual sorting algorithms.
     */
    qsort(
        expected,
        spec->size,
        sizeof *expected,
        compare_ints
    );

    for (size_t algorithm = 0;
         algorithm < SORT_ALGORITHM_COUNT;
         ++algorithm) {

        memcpy(
            work,
            input,
            spec->size * sizeof *work
        );

        SortStats stats = {0, 0};

        clock_t start = clock();

        SORT_ALGORITHMS[algorithm].sort(
            work,
            spec->size,
            &stats
        );

        clock_t end = clock();

        double ms =
            1000.0 *
            (double)(end - start) /
            (double)CLOCKS_PER_SEC;

        int valid = same_array(
            work,
            expected,
            spec->size
        );

        print_result(
            SORT_ALGORITHMS[algorithm].name,
            spec->name,
            spec->size,
            &stats,
            ms,
            csv,
            valid
        );
    }

    free(input);
    free(work);
    free(expected);

    return 1;
}

int main(int argc, char **argv) {
    int csv = 0;
    int blocks = 0;
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--csv") == 0) csv = 1;
        else if (strcmp(argv[i], "--blocks") == 0) blocks = 1;
        else {
            fprintf(stderr, "usage: %s [--csv] [--blocks]\n", argv[0]);
            return 2;
        }
    }

    if (csv || blocks) {
    printf(
        "algorithm,input,n,comparisons,moves,time_ms,valid\n"
    );
} else {
    printf("=== sorting comparison ===\n");
    printf(
        "%-20s %-12s %8s %12s %12s %10s %s\n",
        "algorithm",
        "input",
        "n",
        "comparisons",
        "moves",
        "time(ms)",
        "valid"
    );
}

    /* Normal input cases. */
    if (!blocks) {
        for (size_t kind = 0;
             kind < sizeof SPECS / sizeof SPECS[0];
             ++kind) {

            if (!run_case(&SPECS[kind], kind, csv)) {
                return 1;
            }
        }
    }

    /* Scale experiment. */
    if (blocks) {
        static const size_t block_sizes[] = {
            128,
            256,
            512,
            1024,
            2048
        };

        for (size_t b = 0;
             b < sizeof block_sizes / sizeof block_sizes[0];
             ++b) {

            InputSpec block = {
                "block",
                block_sizes[b]
            };

            if (!run_case(&block, 0, 1)) {
                return 1;
            }
        }
    }

    return 0;
}
