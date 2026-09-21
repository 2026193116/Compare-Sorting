#include "sort.h"

/* Knuth gap 수열을 큰 간격에서 1까지 줄이며 삽입 정렬을 반복한다. */
void shellSort(int a[], size_t n, SortStats *s) {
    size_t gap = 1;
    while (gap < n / 3) gap = gap * 3 + 1;
    while (gap > 0) {
        for (size_t i = gap; i < n; ++i) {
            int value = a[i];
            size_t j = i;
            while (j >= gap) {
                s->comparisons++;
                if (a[j - gap] <= value) break;
                a[j] = a[j - gap]; s->moves++; j -= gap;
            }
            if (j != i) { a[j] = value; s->moves++; }
        }
        gap = (gap - 1) / 3;
    }
}
