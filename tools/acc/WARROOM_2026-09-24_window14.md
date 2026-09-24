# WARROOM 2026-09-24 — exact window-14 shortening (Part 2)

Kernel: official `ac-r2-v1`, SAIR commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e` (same validated kernel/fingerprint/table as `acc_opt.c`, included verbatim). Starting paths: the replayed best paths in `ACC_PORTFOLIO_SCREEN/evidence/ALL_293_BEST_IN_THIS_BATCH.txt` (each re-verified with official `core.verify` before the run). Records and k are the values given in the brief.

## Method and proof

For path states s_0..s_n and every pair i<j with j-i <= 14: build B7(s_j) (all states within 7 moves, BFS distance labels, no length cap) and keep B6 of the previous 14 states. min over B6(s_i) ∩ B7(s_j) of dA+dB equals d(s_i,s_j) whenever d(s_i,s_j) <= 13 (a geodesic of length d <= 13 has its vertex at step min(d,6) in both balls, by inverse-closure). So each pair is decided exactly: d(s_i,s_j) < j-i or not. Exact repeated states at any distance are also spliced. Each pass splices the largest saving (segment rebuilt from exact words by a geodesic DFS in B6(s_i) and a distance walk in B7(s_j)), then rescans the whole new path; stops when a full pass finds nothing. The final path is replayed by official `core.verify`. Fingerprint caveat as in the R-band records (~1e-20).

Self-test: the 13-move ac-01586 optimum padded with a random 6-out/6-back detour (25 moves) was reduced to exactly 13 (`runs/2026-09-24/window_selftest.jsonl`).

## Results

| row | record | k | start | end | passes | splices | final path verified | wall |
|---|---|---|---|---|---|---|---|---|
| ac-09058 | 19 | 9 | 20 | 20 | 1 | — | True | 92.3 s |
| ac-02661 | 26 | 8 | 27 | 27 | 1 | — | True | 138.7 s |
| ac-09230 | 26 | 13 | 27 | 27 | 1 | — | True | 148.5 s |
| ac-05818 | 34 | 1 | 37 | 37 | 1 | — | True | 220.6 s |
| ac-09595 | 36 | 2 | 42 | 42 | 1 | — | True | 258.8 s |
| ac-06045 | 37 | 2 | 44 | 44 | 1 | — | True | 283.0 s |
| ac-05558 | 24 | 2 | 32 | 30 | 3 | window [15,29] 14 -> 13 moves; new length 31; window [11,25] 14 -> 13 moves; new length 30 | True | 585.0 s |
| ac-02628 | 26 | 4 | 28 | 27 | 2 | window [11,25] 14 -> 13 moves; new length 27 | True | 327.6 s |
| ac-09757 | 40 | 4 | 40 | 40 | 1 | — | True | 247.5 s |

No result ties a k<=2 row or beats any record, so there are no submission lines. ac-09058 cannot drop below 19 by any method: Part 1 proves no path <= 18 exists.

Final paths:

```
ac-09058: [7, 4, 1, 2, 9, 9, 3, 8, 8, 11, 4, 2, 2, 2, 2, 2, 2, 2, 2, 0]
ac-02661: [1, 11, 5, 11, 5, 12, 12, 12, 0, 12, 4, 9, 3, 9, 9, 9, 9, 4, 2, 2, 2, 0, 3, 3, 3, 3, 3]
ac-09230: [0, 11, 4, 8, 6, 12, 3, 7, 9, 7, 8, 2, 6, 5, 6, 4, 6, 5, 6, 6, 2, 4, 4, 4, 4, 4, 4]
ac-05818: [1, 12, 12, 5, 10, 4, 13, 4, 6, 8, 5, 12, 11, 5, 13, 11, 9, 3, 7, 10, 1, 8, 5, 11, 12, 3, 8, 10, 4, 13, 10, 3, 5, 5, 5, 5, 2]
ac-09595: [1, 6, 10, 0, 5, 10, 12, 12, 5, 13, 13, 2, 11, 4, 12, 12, 2, 6, 8, 12, 12, 5, 12, 11, 4, 3, 7, 8, 8, 4, 7, 8, 3, 7, 8, 2, 5, 5, 5, 1, 4, 2]
ac-06045: [0, 4, 1, 12, 12, 12, 12, 5, 10, 10, 12, 2, 6, 13, 11, 4, 0, 7, 2, 7, 9, 3, 8, 6, 5, 10, 12, 4, 12, 12, 10, 5, 10, 12, 0, 3, 12, 10, 4, 4, 3, 5, 5, 3]
ac-05558: [6, 4, 0, 7, 12, 2, 0, 13, 11, 11, 5, 6, 8, 4, 3, 11, 13, 5, 1, 13, 11, 11, 5, 9, 3, 7, 5, 3, 11, 5]
ac-02628: [1, 12, 4, 1, 8, 5, 6, 9, 4, 12, 1, 4, 6, 6, 3, 7, 9, 6, 8, 4, 11, 3, 3, 0, 4, 4, 4]
ac-09757: [12, 4, 1, 7, 4, 10, 10, 5, 6, 13, 4, 11, 5, 8, 6, 4, 6, 8, 13, 2, 5, 13, 11, 5, 13, 2, 7, 8, 2, 7, 8, 8, 5, 1, 12, 3, 0, 2, 4, 2]
```

## C source (`research/acc/optimality/acc_window.c`)

```c
// ACC exact window shortening, ac-r2-v1 (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e).
// Kernel, fingerprint and table are shared verbatim with acc_opt.c (included).
//
// For path states s_0..s_n: for every pair i<j with j-i <= 14 decide exactly
// whether d(s_i,s_j) <= j-i-1 using B6(s_i) ∩ B7(s_j) (6+7 = 13 >= j-i-1, so
// the minimum of dA+dB over the intersection is the exact distance whenever
// that distance is <= 13). Only B6 of the previous 14 states and one B7 are
// resident. Also splices exact repeated states at any distance.
// Each pass splices the single largest saving; passes repeat until none.
// usage: acc_window WORKDIR l0 w.. l1 w.. n m1..mn
#define ACC_NO_MAIN
#include "acc_opt.c"

static St *P; static int n;
static int moves[4096];
static void states_from_moves(const St*s0){ P[0]=*s0; for(int k=0;k<n;k++) apply(&P[k],moves[k],&P[k+1]); }

// DFS from s along geodesic children of ball A until reaching fingerprint (g1,g2) at depth p
static int dfs(const Tab*A,const St*s,int depth,int p,uint64_t g1,uint64_t g2,int*seg,St*out){
    uint64_t h1,h2; if(depth==p){ fp(s,&h1,&h2); if(h1==g1&&h2==g2){ *out=*s; return 1; } return 0; }
    St*c=malloc(sizeof(St));
    for(int m=0;m<14;m++){ apply(s,m,c); fp(c,&h1,&h2); if(tab_find(A,h1,h2)!=depth+1) continue;
        seg[depth]=m; if(dfs(A,c,depth+1,p,g1,g2,seg,out)){ free(c); return 1; } }
    free(c); return 0;
}
// B6 extraction
static void extract(const Tab*B7,Tab*B6){ uint64_t c=0; for(uint64_t i=0;i<B7->N;i++) if(B7->t[2*i]&&(B7->t[2*i+1]&0xF)<=6) c++;
    tab_init(B6,c*10/7+16); for(uint64_t i=0;i<B7->N;i++) if(B7->t[2*i]&&(B7->t[2*i+1]&0xF)<=6)
        tab_ins_raw(B6,B7->t[2*i],B7->t[2*i+1]&~0xFULL,(int)(B7->t[2*i+1]&0xF)); }
static void tab_free(Tab*T){ if(T->t){ munmap(T->t,(size_t)16*T->N); T->t=NULL; } }

int main(int argc,char**argv){
    const char*dir=argv[1]; St s0; int ai=parse_state(argv,2,&s0); n=atoi(argv[ai++]);
    for(int k=0;k<n;k++) moves[k]=atoi(argv[ai++]);
    P=malloc(sizeof(St)*(4096+1)); states_from_moves(&s0);
    if(!(P[n].l[0]==1&&P[n].l[1]==1&&P[n].w[0][0]==0&&P[n].w[1][0]==2)) die("path does not reach (x,y)");
    printf("START length %d\n",n); fflush(stdout); double T0=now(); int pass=0;
    for(;;){ pass++; double tp=now();
        int bi=-1,bj=-1,bd=0,bsave=0,seg[32],bseg[32]; uint64_t maxball=0;
        // repeated states at any distance
        for(int i=0;i<=n;i++) for(int j=n;j>i+14;j--) if(st_eq(&P[i],&P[j])&&j-i>bsave){ bsave=j-i; bi=i; bj=j; bd=0; break; }
        Tab B6[15]; memset(B6,0,sizeof B6);
        for(int j=0;j<=n;j++){ Tab B7; tab_init(&B7,1u<<22); bfs(&B7,&P[j],7,dir,"W",1,0,NULL); rmf(dir,"W",6);
            if(B7.n>maxball) maxball=B7.n;
            for(int i=(j>14?j-14:0);i<j;i++){ int gap=j-i; Tab*A=&B6[i%15]; int bestp=99,pp=0; uint64_t g1=0,g2=0;
                for(uint64_t x=0;x<A->N;x++){ uint64_t h1=A->t[2*x]; if(!h1) continue; int da=(int)(A->t[2*x+1]&0xF);
                    if(da>=gap) continue; uint64_t h2=A->t[2*x+1]&~0xFULL; int db=tab_find(&B7,h1,h2);
                    if(db>=0&&da+db<bestp){ bestp=da+db; pp=da; g1=h1; g2=h2; } }
                if(bestp<gap){ printf("  pass %d: d(s_%d,s_%d)=%d < %d\n",pass,i,j,bestp,gap); fflush(stdout);
                    if(gap-bestp>bsave){ St M; if(!dfs(A,&P[i],0,pp,g1,g2,seg,&M)) die("dfs rebuild failed");
                        int L=pp; St c=M,nx2; for(int k=bestp-pp;k>0;k--){ int ok=0; uint64_t h1,h2;
                            for(int m=0;m<14;m++){ apply(&c,m,&nx2); fp(&nx2,&h1,&h2); if(tab_find(&B7,h1,h2)==k-1){ seg[L++]=m; c=nx2; ok=1; break; } }
                            if(!ok) die("walk to s_j failed"); }
                        if(!st_eq(&c,&P[j])) die("segment does not reach s_j");
                        bsave=gap-bestp; bi=i; bj=j; bd=bestp; memcpy(bseg,seg,sizeof(int)*bestp); } } }
            tab_free(&B6[j%15]); extract(&B7,&B6[j%15]); tab_free(&B7);
        }
        for(int k=0;k<15;k++) tab_free(&B6[k]);
        printf("PASS %d done: max |B7|=%llu, %.1fs\n",pass,(unsigned long long)maxball,now()-tp);
        if(bsave==0) break;
        int nm[4096],L=0; for(int k=0;k<bi;k++) nm[L++]=moves[k]; for(int k=0;k<bd;k++) nm[L++]=bseg[k]; for(int k=bj;k<n;k++) nm[L++]=moves[k];
        memcpy(moves,nm,sizeof(int)*L); n=L; states_from_moves(&s0);
        if(!(P[n].l[0]==1&&P[n].l[1]==1&&P[n].w[0][0]==0&&P[n].w[1][0]==2)) die("spliced path does not reach (x,y)");
        printf("SPLICE window [%d,%d] %d -> %d moves; new length %d\n",bi,bj,bj-bi,bd,n);
        printf("PATH"); for(int k=0;k<n;k++) printf(" %d",moves[k]); printf("\n"); fflush(stdout);
    }
    printf("FINAL length %d wall %.1fs\nFINALPATH",n,now()-T0); for(int k=0;k<n;k++) printf(" %d",moves[k]); printf("\n");
    return 0;
}
```
