#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "sort.h"

static int isSorted(const int a[], size_t n) { for (size_t i=1;i<n;i++) if(a[i-1]>a[i]) return 0; return 1; }
static void makeInput(int *a, size_t n, int mode) { for(size_t i=0;i<n;i++) { if(mode==0) a[i]=(int)((i*73+19)%1000); else if(mode==1) a[i]=(int)i; else if(mode==2) a[i]=(int)(n-i); else a[i]=(int)((i*17)%16)-8; } }
int main(int argc, char **argv) {
    int csv = argc > 1 && strcmp(argv[1], "--csv") == 0;
    const char *shapes[] = {"random", "sorted", "reverse", "many-duplicates"};
    const size_t n = 2000;
    int *input=malloc(n*sizeof *input), *work=malloc(n*sizeof *work);
    if(!input || !work) return 1;
    if(csv) printf("algorithm,input,n,comparisons,moves,time_ms\n");
    else printf("=== 정렬 비교: 셸 · 카운팅 · 칵테일 셰이커 ===\n[n = %zu]\n%-22s %-16s %12s %12s %10s %s\n",n,"algorithm","input","comparisons","moves","time(ms)","valid");
    for(size_t sh=0;sh<4;sh++) for(size_t ai=0;ai<SORT_ALGORITHM_COUNT;ai++) { SortStats st={0,0}; makeInput(input,n,(int)sh); memcpy(work,input,n*sizeof *work); clock_t begin=clock(); SORT_ALGORITHMS[ai].sort(work,n,&st); double ms=1000.0*(double)(clock()-begin)/CLOCKS_PER_SEC; if(csv) printf("%s,%s,%zu,%llu,%llu,%.3f\n",SORT_ALGORITHMS[ai].name,shapes[sh],n,st.comparisons,st.moves,ms); else printf("%-22s %-16s %12llu %12llu %10.3f %s\n",SORT_ALGORITHMS[ai].name,shapes[sh],st.comparisons,st.moves,ms,isSorted(work,n)?"yes":"NO"); }
    free(input); free(work); return 0;
}
