// ACC exact window shortening, ac-r2-v1 (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e).
// Kernel, fingerprint and table are shared verbatim with acc_opt.c (included).
//
// Low-memory variant of acc_window.c. For path states s_0..s_n and each
// pair i<j with j-i <= 11, decide exactly
// whether d(s_i,s_j) <= j-i-1 using B5A(s_i) ∩ B5B(s_j) (5+5 = 10 >= j-i-1, so
// the minimum of dA+dB over the intersection is the exact distance whenever
// that distance is <= 10). Only B5A of the previous 11 states and one B5B are
// resident. Also splices exact repeated states at any distance.
// Each pass splices the single largest saving; passes repeat until none.
// usage: acc_window11 WORKDIR l0 w.. l1 w.. n m1..mn
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
// B5A extraction
static void extract(const Tab*B5B,Tab*B5A){ uint64_t c=0; for(uint64_t i=0;i<B5B->N;i++) if(B5B->t[2*i]&&(B5B->t[2*i+1]&0xF)<=5) c++;
    tab_init(B5A,c*10/7+16); for(uint64_t i=0;i<B5B->N;i++) if(B5B->t[2*i]&&(B5B->t[2*i+1]&0xF)<=5)
        tab_ins_raw(B5A,B5B->t[2*i],B5B->t[2*i+1]&~0xFULL,(int)(B5B->t[2*i+1]&0xF)); }
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
        for(int i=0;i<=n;i++) for(int j=n;j>i+11;j--) if(st_eq(&P[i],&P[j])&&j-i>bsave){ bsave=j-i; bi=i; bj=j; bd=0; break; }
        Tab B5A[12]; memset(B5A,0,sizeof B5A);
        for(int j=0;j<=n;j++){ Tab B5B; tab_init(&B5B,1u<<19); bfs(&B5B,&P[j],5,dir,"W",1,0,NULL); rmf(dir,"W",4);
            if(B5B.n>maxball) maxball=B5B.n;
            for(int i=(j>11?j-11:0);i<j;i++){ int gap=j-i; Tab*A=&B5A[i%12]; int bestp=99,pp=0; uint64_t g1=0,g2=0;
                for(uint64_t x=0;x<A->N;x++){ uint64_t h1=A->t[2*x]; if(!h1) continue; int da=(int)(A->t[2*x+1]&0xF);
                    if(da>=gap) continue; uint64_t h2=A->t[2*x+1]&~0xFULL; int db=tab_find(&B5B,h1,h2);
                    if(db>=0&&da+db<bestp){ bestp=da+db; pp=da; g1=h1; g2=h2; } }
                if(bestp<gap){ printf("  pass %d: d(s_%d,s_%d)=%d < %d\n",pass,i,j,bestp,gap); fflush(stdout);
                    if(gap-bestp>bsave){ St M; if(!dfs(A,&P[i],0,pp,g1,g2,seg,&M)) die("dfs rebuild failed");
                        int L=pp; St c=M,nx2; for(int k=bestp-pp;k>0;k--){ int ok=0; uint64_t h1,h2;
                            for(int m=0;m<14;m++){ apply(&c,m,&nx2); fp(&nx2,&h1,&h2); if(tab_find(&B5B,h1,h2)==k-1){ seg[L++]=m; c=nx2; ok=1; break; } }
                            if(!ok) die("walk to s_j failed"); }
                        if(!st_eq(&c,&P[j])) die("segment does not reach s_j");
                        bsave=gap-bestp; bi=i; bj=j; bd=bestp; memcpy(bseg,seg,sizeof(int)*bestp); } } }
            tab_free(&B5A[j%12]); extract(&B5B,&B5A[j%12]); tab_free(&B5B);
        }
        for(int k=0;k<12;k++) tab_free(&B5A[k]);
        printf("PASS %d done: max |B5B|=%llu, %.1fs\n",pass,(unsigned long long)maxball,now()-tp);
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
