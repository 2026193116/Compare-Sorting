#ifndef SORTCTX_H
#define SORTCTX_H

#include <stddef.h>

/* Counters shared by every C sorting implementation. */
typedef struct {
    unsigned long long comparisons;
    unsigned long long moves;
} SortStats;

typedef void (*SortFunction)(int *, size_t, SortStats *);

#endif
