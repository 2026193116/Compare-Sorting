#ifndef SORT_H
#define SORT_H

#include <stddef.h>
#include "sortctx.h"

typedef struct {
    const char *name;
    const char *timeComplexity;
    const char *spaceComplexity;
    int stable;
    SortFunction sort;
} SortAlgorithm;

void shellSort(int a[], size_t n, SortStats *stats);
void countingSort(int a[], size_t n, SortStats *stats);
void cocktailShakerSort(int a[], size_t n, SortStats *stats);

extern const SortAlgorithm SORT_ALGORITHMS[];
extern const size_t SORT_ALGORITHM_COUNT;

#endif
