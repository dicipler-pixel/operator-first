// Corridor BFS for Andrews-Curtis (ac-r2-v1), 64-letter relators, with MANY
// TARGETS supplied on the command line.
//
// ac_corridor64_v1.c hardcodes the trivial presentation (x,y) as the target,
// so a BFS from a start can only ever answer "is the trivial presentation in
// this component". That makes the component structure of the capped graph
// invisible to the instrument -- the gap named by the Atlas card
// CASCADE-FOUR-RECORDS ("a separately named topological invariant").
//
// Testing n presentations pairwise for shared component membership costs
// O(n^2) enumerations with a single-target engine. This variant takes a LIST
// of targets and reports which ones the start's component contains, so one
// enumeration settles every membership at once -- and with union-find over the
// results, a whole profile needs one enumeration per COMPONENT rather than per
// pair. ac_corridor64_target_v1.c and _v1.c are both unchanged.
//
// Usage: cap budget l0 r0... l1 r1... N  (t0 tg0... t1 tg1...) x N
//
// Prints one HIT line per target found, then the usual verdict. Unlike the
// single-target engine it does NOT stop early on a hit: it keeps going so that
// every membership is decided by the one pass.
//
// Search tool only: every certificate is re-verified by the official Python
// verifier, never by a re-implementation.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXW 64
typedef struct { uint64_t a0,b0,a1,b1; uint8_t l0,l1; } St;
static int CAP;
static inline void packw(const uint8_t*w,int n,uint64_t*lo,uint64_t*hi){
    uint64_t L=0,H=0;
    for(int i=0;i<n;i++){ uint64_t v=w[i]&3; if(i<32) L|=v<<(2*i); else H|=v<<(2*(i-32)); }
    *lo=L; *hi=H;
}
static inline void unpackw(uint64_t lo,uint64_t hi,int n,uint8_t*w){
    for(int i=0;i<n;i++) w[i]= (i<32)? ((lo>>(2*i))&3) : ((hi>>(2*(i-32)))&3);
}
static inline int reduce(const uint8_t*in,int n,uint8_t*out){
    int t=0; for(int i=0;i<n;i++){ uint8_t c=in[i];
        if(t>0&&out[t-1]==(c^1)) t--; else out[t++]=c; } return t;
}
static inline int invword(const uint8_t*a,int n,uint8_t*o){
    for(int i=0;i<n;i++) o[i]=a[n-1-i]^1; return n;
}
static int apply(const St*s,int m,St*r){
    uint8_t a[MAXW],b[MAXW],t[2*MAXW+4],u[2*MAXW+4];
    int la=s->l0, lb=s->l1, lt,lu;
    unpackw(s->a0,s->b0,la,a); unpackw(s->a1,s->b1,lb,b);
    *r=*s;
    if(m==0){ lu=invword(a,la,u); packw(u,lu,&r->a0,&r->b0); r->l0=lu; }
    else if(m==1){ lu=invword(b,lb,u); packw(u,lu,&r->a1,&r->b1); r->l1=lu; }
    else if(m==2||m==3){
        memcpy(t,a,la); lt=la;
        if(m==2){ memcpy(t+lt,b,lb); lt+=lb; } else { lt+=invword(b,lb,t+lt); }
        lu=reduce(t,lt,u); if(lu+lb>CAP||lu>MAXW) return 0;
        packw(u,lu,&r->a0,&r->b0); r->l0=lu;
    } else if(m==4||m==5){
        memcpy(t,b,lb); lt=lb;
        if(m==4){ memcpy(t+lt,a,la); lt+=la; } else { lt+=invword(a,la,t+lt); }
        lu=reduce(t,lt,u); if(lu+la>CAP||lu>MAXW) return 0;
        packw(u,lu,&r->a1,&r->b1); r->l1=lu;
    } else {
        int on0=(m<=9); int k=on0?m-6:m-10; uint8_t g=(uint8_t)k, gi=g^1;
        const uint8_t*src=on0?a:b; int ls=on0?la:lb;
        t[0]=g; memcpy(t+1,src,ls); t[ls+1]=gi; lt=ls+2;
        lu=reduce(t,lt,u); int other=on0?lb:la;
        if(lu+other>CAP||lu>MAXW) return 0;
        if(on0){ packw(u,lu,&r->a0,&r->b0); r->l0=lu; }
        else   { packw(u,lu,&r->a1,&r->b1); r->l1=lu; }
    }
    return 1;
}
static inline uint64_t hsh(const St*s){
    uint64_t h=s->a0*0x9E3779B97F4A7C15ULL;
    h^=(s->b0+0xC2B2AE3D27D4EB4FULL); h*=0x165667B19E3779F9ULL;
    h^=(s->a1+0x27D4EB2F165667C5ULL); h*=0x9E3779B97F4A7C15ULL;
    h^=(s->b1+0x94D049BB133111EBULL);
    h^=((uint64_t)s->l0<<56)^((uint64_t)s->l1<<48);
    h^=h>>29; h*=0xBF58476D1CE4E5B9ULL; h^=h>>32; return h;
}
static inline int eq(const St*x,const St*y){
    return x->a0==y->a0&&x->b0==y->b0&&x->a1==y->a1&&x->b1==y->b1&&x->l0==y->l0&&x->l1==y->l1;
}
static St*pool; static uint32_t*par; static uint8_t*pmv; static uint32_t*tab;
static uint64_t mask; static uint32_t nst;
static uint32_t intern(const St*s,uint32_t p,uint8_t mv,int*isnew){
    uint64_t i=hsh(s)&mask;
    for(;;){ uint32_t e=tab[i];
        if(e==0xFFFFFFFFu){ pool[nst]=*s; par[nst]=p; pmv[nst]=mv; tab[i]=nst; *isnew=1; return nst++; }
        if(eq(&pool[e],s)){ *isnew=0; return e; }
        i=(i+1)&mask; }
}
int main(int argc,char**argv){
    CAP=atoi(argv[1]); uint64_t maxst=strtoull(argv[2],0,10);
    if(CAP>MAXW){ printf("CAP_TOO_LARGE %d\n",CAP); return 4; }
    int l0=atoi(argv[3]); uint8_t a[MAXW],b[MAXW];
    for(int i=0;i<l0;i++) a[i]=atoi(argv[4+i]);
    int l1=atoi(argv[4+l0]);
    for(int i=0;i<l1;i++) b[i]=atoi(argv[5+l0+i]);
    uint64_t c2=1; while(c2<maxst*2) c2<<=1; mask=c2-1;
    pool=malloc(maxst*sizeof(St)); par=malloc(maxst*4); pmv=malloc(maxst); tab=malloc(c2*4);
    if(!pool||!par||!pmv||!tab){ printf("ALLOC_FAIL\n"); return 1; }
    memset(tab,0xFF,c2*4);
    St s0; memset(&s0,0,sizeof s0);
    packw(a,l0,&s0.a0,&s0.b0); s0.l0=l0; packw(b,l1,&s0.a1,&s0.b1); s0.l1=l1;
    // a LIST of targets follows the start presentation
    int base=5+l0+l1;
    if(argc<base+1){ printf("NO_TARGET_ARGS\n"); return 5; }
    int NT=atoi(argv[base]); int p=base+1;
    if(NT<1||NT>4096){ printf("BAD_TARGET_COUNT %d\n",NT); return 7; }
    St*tg=malloc((size_t)NT*sizeof(St)); uint8_t*hit=calloc(NT,1);
    if(!tg||!hit){ printf("ALLOC_FAIL\n"); return 1; }
    for(int k=0;k<NT;k++){
        uint8_t ta[MAXW],tb[MAXW];
        int t0=atoi(argv[p++]); for(int i=0;i<t0;i++) ta[i]=atoi(argv[p++]);
        int t1=atoi(argv[p++]); for(int i=0;i<t1;i++) tb[i]=atoi(argv[p++]);
        if(t0+t1>CAP){ printf("TARGET_OUTSIDE_CAP idx=%d t=%d cap=%d\n",k,t0+t1,CAP); return 6; }
        memset(&tg[k],0,sizeof(St));
        packw(ta,t0,&tg[k].a0,&tg[k].b0); tg[k].l0=t0;
        packw(tb,t1,&tg[k].a1,&tg[k].b1); tg[k].l1=t1;
        if(eq(&s0,&tg[k])){ hit[k]=1; printf("HIT %d 0\n",k); }
    }
    int nhit=0; for(int k=0;k<NT;k++) nhit+=hit[k];
    int isnew; intern(&s0,0xFFFFFFFFu,255,&isnew);
    uint32_t head=0,depth=0,lvlend=nst;
    while(head<nst){
        uint32_t si=head++; St cur=pool[si],r;
        for(int m=0;m<14;m++){
            if(!apply(&cur,m,&r)) continue;
            uint32_t id=intern(&r,si,(uint8_t)m,&isnew);
            if(isnew && nhit<NT){
                // check the new state against every target still unhit
                for(int k=0;k<NT;k++) if(!hit[k] && eq(&r,&tg[k])){
                    hit[k]=1; nhit++;
                    uint32_t c=id; int n=0; static uint8_t mv[200000];
                    while(par[c]!=0xFFFFFFFFu){ mv[n++]=pmv[c]; c=par[c]; }
                    printf("HIT %d %d\n",k,n); fflush(stdout);
                }
            }
            if(nst>=maxst-2){
                printf("BUDGET states=%u depth=%u hits=%d/%d\n",nst,depth,nhit,NT);
                return 2; }
        }
        if(head==lvlend){ depth++; lvlend=nst; fprintf(stderr,"depth %u states %u\n",depth,nst); }
    }
    // Exhausted: the start's component is fully enumerated and the target,
    // which was range-checked to be inside the cap, is not in it. The two
    // presentations therefore lie in DIFFERENT COMPONENTS of the capped graph.
    printf("EXHAUSTED states=%u depth=%u cap=%d hits=%d/%d\n",nst,depth,CAP,nhit,NT);
    return 3;
}
