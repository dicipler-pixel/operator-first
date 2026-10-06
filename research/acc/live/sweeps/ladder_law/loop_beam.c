// loop_beam: layered beam over a restricted AC move set (ac-r2-v1 kernel of acc_opt.c) from START to the exact GOAL state.
// Keeps the W states of each depth with the best progress score of the multiplied relator (slot):
//   score = #letters of generator group XG  -  2 * #letters of the other group
// (a BS rewrite adds one XG letter; a cancellation removes two of the other; a junk multiplication scores -1).
// Global first-visit dedupe by the 128-bit fingerprint. Stops at the first depth that reaches GOAL. Not a certificate.
// usage: loop_beam W CAP MAXD SLOT XG MASK  l0 w.. l1 w..  l0 w.. l1 w..     (letters 0=x 1=X 2=y 3=Y; MASK bit m = move m)
// prints  LOOP d PATH m1 m2 ...   or   NONE depth
#define ACC_NO_MAIN
#include "../../../optimality/acc_opt.c"
typedef struct { int sc; int sc2; int par; uint8_t mv; uint64_t h1, h2; } Cand;
static int ccmp(const void*a,const void*b){ const Cand*x=a,*y=b; if(x->sc!=y->sc) return y->sc-x->sc; if(x->sc2!=y->sc2) return y->sc2-x->sc2;
    return (x->h1<y->h1)?-1:(x->h1>y->h1); }
typedef struct { int n; uint32_t*off; uint16_t*l0,*l1; uint8_t*ar; size_t cap; } Layer;
static void lay_init(Layer*L,int W,size_t bytes){ L->off=malloc(4*(size_t)W); L->l0=malloc(2*(size_t)W); L->l1=malloc(2*(size_t)W);
    L->ar=malloc(bytes); L->cap=bytes; L->n=0; if(!L->off||!L->ar) die("alloc"); }
static size_t lay_used;
static void lay_put(Layer*L,const St*s){ size_t need=s->l[0]+s->l[1]; if(lay_used+need>L->cap) die("arena");
    L->off[L->n]=(uint32_t)lay_used; L->l0[L->n]=s->l[0]; L->l1[L->n]=s->l[1];
    memcpy(L->ar+lay_used,s->w[0],s->l[0]); memcpy(L->ar+lay_used+s->l[0],s->w[1],s->l[1]); lay_used+=need; L->n++; }
static void lay_get(const Layer*L,int i,St*s){ s->l[0]=L->l0[i]; s->l[1]=L->l1[i];
    memcpy(s->w[0],L->ar+L->off[i],s->l[0]); memcpy(s->w[1],L->ar+L->off[i]+s->l[0],s->l[1]); }
static St A,Bs,G; static int TIE,TGT;
int main(int argc,char**argv){
    int W=atoi(argv[1]), CAP=atoi(argv[2]), MAXD=atoi(argv[3]), SLOT=atoi(argv[4]), XG=atoi(argv[5]);
    TIE=getenv("TIE")?atoi(getenv("TIE")):0; TGT=getenv("TGT")?atoi(getenv("TGT")):0;
    unsigned MASK=(unsigned)strtoul(argv[6],0,0); int ai=7; St S0; ai=parse_state(argv,ai,&S0); ai=parse_state(argv,ai,&G);
    uint64_t g1,g2; fp(&G,&g1,&g2);
    Tab seen; tab_init(&seen,1ULL<<24); uint64_t h1,h2; fp(&S0,&h1,&h2); tab_ins(&seen,h1,h2,0,1);
    size_t bytes=(size_t)W*(size_t)(CAP+2);
    Layer cur, nxt; lay_init(&cur,W,bytes); lay_init(&nxt,W,bytes); lay_used=0; lay_put(&cur,&S0);
    int32_t**PAR=calloc(MAXD+2,sizeof(int32_t*)); uint8_t**MV=calloc(MAXD+2,sizeof(uint8_t*));
    Cand*C=malloc(sizeof(Cand)*(size_t)W*14);
    for(int d=1; d<=MAXD; d++){
        int nc=0;
        for(int i=0;i<cur.n;i++){ lay_get(&cur,i,&A);
            for(int m=0;m<14;m++){ if(!((MASK>>m)&1)) continue; apply(&A,m,&Bs);
                if(Bs.l[0]+Bs.l[1]>CAP) continue; fp(&Bs,&h1,&h2);
                if(h1==g1&&h2==g2){ // goal: rebuild
                    int path[1<<14]; int L=d; path[d-1]=m; int p=i;
                    for(int k=d-1;k>=1;k--){ path[k-1]=MV[k][p]; p=PAR[k][p]; }
                    printf("LOOP %d PATH",L); for(int k=0;k<L;k++) printf(" %d",path[k]); printf("\n"); return 0; }
                if(tab_ins(&seen,h1,h2,d&15,1)>=0) continue;
                const uint8_t*w=Bs.w[SLOT]; int L=Bs.l[SLOT], nx=0; for(int t=0;t<L;t++) nx+=((w[t]>>1)==XG);
                int runs=0; for(int t=0;t<L;t++) runs+=(t==0||w[t]!=w[t-1]); int L1=Bs.l[1-SLOT]; int nxe=(TGT>0&&nx>TGT)?2*TGT-nx:nx; C[nc].sc=nxe-2*(L-nx); C[nc].sc2=(TIE==1)?-runs:(TIE==2)?-L1:(TIE==3)?-(runs*8+L1):0; C[nc].par=i; C[nc].mv=(uint8_t)m; C[nc].h1=h1; C[nc].h2=h2; nc++; } }
        if(!nc){ printf("NONE %d\n",d); return 0; }
        qsort(C,nc,sizeof(Cand),ccmp); int k=nc<W?nc:W;
        PAR[d]=malloc(4*(size_t)k); MV[d]=malloc((size_t)k);
        lay_used=0; nxt.n=0;
        for(int i=0;i<k;i++){ lay_get(&cur,C[i].par,&A); apply(&A,C[i].mv,&Bs); lay_put(&nxt,&Bs); PAR[d][i]=C[i].par; MV[d][i]=C[i].mv; }
        Layer t=cur; cur=nxt; nxt=t;
        if(d%50==0){ fprintf(stderr,"d=%d kept %d best %d seen %llu\n",d,k,C[0].sc,(unsigned long long)seen.n); }
    }
    printf("NONE %d\n",MAXD); return 0; }
