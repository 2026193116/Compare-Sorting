#include <stdio.h>
#include <string.h>
#include "sort.h"
static int checks, failures;
static void check(const char *name, SortFunction fn, const int *want, const int *src, size_t n) { int a[16]={0}; memcpy(a,src,n*sizeof *a); SortStats s={0,0}; fn(a,n,&s); checks++; if(memcmp(a,want,n*sizeof *a)!=0) { failures++; printf("FAIL %s\n",name); } else printf("ok    %s\n",name); }
int main(void) { const int want[]={-2,0,1,1,3,4,5,9}; const int src[]={3,1,9,-2,5,1,4,0}; for(size_t i=0;i<SORT_ALGORITHM_COUNT;i++) { check(SORT_ALGORITHMS[i].name,SORT_ALGORITHMS[i].sort,want,src,8); int one[]={7}; check("one element",SORT_ALGORITHMS[i].sort,one,one,1); int empty[]={0}; check("empty",SORT_ALGORITHMS[i].sort,empty,empty,0); } printf("\n%d checks, %d failures\n",checks,failures); return failures!=0; }
