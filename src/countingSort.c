#include "sort.h"
#include <stdlib.h>

/* 음수도 처리하기 위해 min을 0번 인덱스로 옮긴다. */
void countingSort(int a[], size_t n, SortStats *s) {
    if (n < 2) return;
    int min = a[0], max = a[0];
    for (size_t i = 1; i < n; ++i) { if (a[i] < min) min = a[i]; if (a[i] > max) max = a[i]; }
    size_t range = (size_t)((long long)max - min + 1);
    size_t *count = calloc(range, sizeof *count);
    int *output = malloc(n * sizeof *output);
    if (!count || !output) { free(count); free(output); return; }
    for (size_t i = 0; i < n; ++i) count[(size_t)((long long)a[i] - min)]++;
    for (size_t i = 1; i < range; ++i) count[i] += count[i - 1];
    for (size_t i = n; i-- > 0;) output[--count[(size_t)((long long)a[i] - min)]] = a[i];
    for (size_t i = 0; i < n; ++i) { a[i] = output[i]; s->moves++; }
    free(count); free(output);
}
