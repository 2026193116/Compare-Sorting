#include "sort.h"

/*
 * Shell sort with a quarter-size initial gap.
 * The gap sequence is floor(n / 4), floor(n / 8), ... , 1.
 */
void shellSort(int a[], size_t n, SortStats *s) {
    size_t gap = n / 4;
    if (gap == 0) gap = 1;

    while (gap > 0) {
        for (size_t i = gap; i < n; ++i) {
            int value = a[i];
            size_t j = i;
            while (j >= gap) {
                s->comparisons++;
                if (a[j - gap] <= value) break;
                a[j] = a[j - gap];
                s->moves++;
                j -= gap;
            }
            if (j != i) {
                a[j] = value;
                s->moves++;
            }
        }
        gap /= 2;
    }
}
