#include "sort.h"

/* 양방향으로 한 번씩 훑어 큰 값과 작은 값을 동시에 확정한다. */
void cocktailShakerSort(int a[], size_t n, SortStats *s) {
    if (n < 2) return;
    size_t left = 0, right = n - 1;
    int swapped = 1;
    while (swapped) {
        swapped = 0;
        for (size_t i = left; i < right; ++i) { s->comparisons++; if (a[i] > a[i + 1]) { int t=a[i]; a[i]=a[i+1]; a[i+1]=t; s->moves+=3; swapped=1; } }
        if (!swapped) break;
        --right; swapped = 0;
        for (size_t i = right; i > left; --i) { s->comparisons++; if (a[i-1] > a[i]) { int t=a[i-1]; a[i-1]=a[i]; a[i]=t; s->moves+=3; swapped=1; } }
        ++left;
    }
}
