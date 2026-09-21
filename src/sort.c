#include "sort.h"

/* Add a new implementation here; main.c does not name algorithms directly. */
const SortAlgorithm SORT_ALGORITHMS[] = {
    {"shellSort", "gap-dependent", "O(1)", 0, shellSort},
    {"countingSort", "O(n + k)", "O(n + k)", 1, countingSort},
    {"cocktailShakerSort", "O(n^2)", "O(1)", 1, cocktailShakerSort}
};

const size_t SORT_ALGORITHM_COUNT =
    sizeof SORT_ALGORITHMS / sizeof SORT_ALGORITHMS[0];
