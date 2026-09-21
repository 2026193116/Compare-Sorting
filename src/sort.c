#include "sort.h"

/* Shell sort uses gap = floor(n/4), then halves it down to 1. */
const SortAlgorithm SORT_ALGORITHMS[] = {
    {"shellSort", "O(n^1.5) average, O(n^2) worst", "O(1)", 0, shellSort},
    {"countingSort", "O(n + k)", "O(n + k)", 1, countingSort},
    {"cocktailShakerSort", "O(n^2)", "O(1)", 1, cocktailShakerSort}
};

const size_t SORT_ALGORITHM_COUNT =
    sizeof SORT_ALGORITHMS / sizeof SORT_ALGORITHMS[0];
