#include <stdio.h>
#include <string.h>

#include "sort.h"

static int checks = 0;
static int failures = 0;

static void check_case(
    const char *name,
    SortFunction function,
    const int *source,
    const int *expected,
    size_t n
) {
    int work[64] = {0};

    memcpy(
        work,
        source,
        n * sizeof *work
    );

    SortStats stats = {0, 0};

    function(work, n, &stats);

    ++checks;

    if (memcmp(
            work,
            expected,
            n * sizeof *work
        ) != 0) {

        ++failures;
        printf("FAIL %s\n", name);
    } else {
        printf("ok    %s\n", name);
    }
}

int main(void) {
    const int normal[] = {
        3, 1, 9, -2, 5, 1, 4, 0
    };

    const int normal_expected[] = {
        -2, 0, 1, 1, 3, 4, 5, 9
    };

    const int sorted[] = {
        -3, -1, 0, 2, 4, 5, 9
    };

    const int reverse[] = {
        9, 5, 4, 2, 0, -1, -3
    };

    const int reverse_expected[] = {
        -3, -1, 0, 2, 4, 5, 9
    };

    const int duplicates[] = {
        5, 5, 5, 1, 1, 0, 0, -2
    };

    const int duplicates_expected[] = {
        -2, 0, 0, 1, 1, 5, 5, 5
    };

    const int one[] = {7};
    const int empty[] = {0};

    for (size_t i = 0;
         i < SORT_ALGORITHM_COUNT;
         ++i) {

        const char *name = SORT_ALGORITHMS[i].name;
        SortFunction function = SORT_ALGORITHMS[i].sort;

        check_case(
            name,
            function,
            normal,
            normal_expected,
            8
        );

        check_case(
            "sorted",
            function,
            sorted,
            sorted,
            7
        );

        check_case(
            "reverse",
            function,
            reverse,
            reverse_expected,
            7
        );

        check_case(
            "duplicates",
            function,
            duplicates,
            duplicates_expected,
            8
        );

        check_case(
            "one element",
            function,
            one,
            one,
            1
        );

        check_case(
            "empty",
            function,
            empty,
            empty,
            0
        );
    }

    printf(
        "\n%d checks, %d failures\n",
        checks,
        failures
    );

    return failures != 0;
}
