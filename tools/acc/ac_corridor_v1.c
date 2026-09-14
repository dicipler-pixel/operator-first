// Corridor BFS for Andrews-Curtis (move spec ac-r2-v1).
// Letters packed 2 bits each: x=0, x^-1=1, y=2, y^-1=3 (inverse = ^1).
// Search tool only -- every certificate it emits is re-verified by the
// official Python verifier.core before any claim is made.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXW 64
typedef struct { uint64_t w0, w1; uint8_t l0, l1; } St;

static int CAP;                 // max total relator length

static inline uint64_t pack(const uint8_t *a, int n){
    uint64_t v=0; for(int i=0;i<n;i++) v |= ((uint64_t)(a[i]&3))<<(2*i); return v;
}
static inline void unpack(uint64_t v,int n,uint8_t *a){
    for(int i=0;i<n;i++) a[i]=(v>>(2*i))&3;
}
// free reduction by stack cancellation (matches verifier.core.free_reduce)
static inline int reduce(const uint8_t *in,int n,uint8_t *out){
    int t=0;
    for(int i=0;i<n;i++){ uint8_t c=in[i];
        if(t>0 && out[t-1]==(c^1)) t--; else out[t++]=c; }
    return t;
}
static inline int invword(const uint8_t *a,int n,uint8_t *o){
    for(int i=0;i<n;i++) o[i]=a[n-1-i]^1; return n;
}

// apply move m; returns 0 if result exceeds CAP (rejected), else 1
static int apply(const St *s,int m,St *r){
    uint8_t a[MAXW],b[MAXW],t[2*MAXW],u[2*MAXW];
    int la=s->l0, lb=s->l1, lt, lu;
    unpack(s->w0,la,a); unpack(s->w1,lb,b);
    if(m==0){ lu=invword(a,la,u); r->w0=pack(u,lu); r->l0=lu; r->w1=s->w1; r->l1=lb; }
    else if(m==1){ lu=invword(b,lb,u); r->w0=s->w0; r->l0=la; r->w1=pack(u,lu); r->l1=lu; }
    else if(m==2||m==3){
        memcpy(t,a,la); lt=la;
        if(m==2){ memcpy(t+lt,b,lb); lt+=lb; }
        else { lt+=invword(b,lb,t+lt); }
        lu=reduce(t,lt,u); if(lu+lb>CAP||lu>MAXW) return 0;
        r->w0=pack(u,lu); r->l0=lu; r->w1=s->w1; r->l1=lb;
    }
    else if(m==4||m==5){
        memcpy(t,b,lb); lt=lb;
        if(m==4){ memcpy(t+lt,a,la); lt+=la; }
        else { lt+=invword(a,la,t+lt); }
        lu=reduce(t,lt,u); if(lu+la>CAP||lu>MAXW) return 0;
        r->w0=s->w0; r->l0=la; r->w1=pack(u,lu); r->l1=lu;
    }
    else {
        int on0 = (m<=9); int k = on0 ? m-6 : m-10;
        // GENS order (1,-1,2,-2) -> packed (0,1,2,3)
        uint8_t g=(uint8_t)k, gi=g^1;
        const uint8_t *src = on0 ? a : b; int ls = on0 ? la : lb;
        t[0]=g; memcpy(t+1,src,ls); t[ls+1]=gi; lt=ls+2;
        lu=reduce(t,lt,u);
        int other = on0 ? lb : la;
        if(lu+other>CAP||lu>MAXW) return 0;
        if(on0){ r->w0=pack(u,lu); r->l0=lu; r->w1=s->w1; r->l1=lb; }
        else   { r->w0=s->w0; r->l0=la; r->w1=pack(u,lu); r->l1=lu; }
    }
    return 1;
}

static inline uint64_t hsh(const St*s){
    uint64_t h=s->w0*0x9E3779B97F4A7C15ULL ^ (s->w1+0xC2B2AE3D27D4EB4FULL);
    h^=((uint64_t)s->l0<<56)^((uint64_t)s->l1<<48);
    h^=h>>29; h*=0xBF58476D1CE4E5B9ULL; h^=h>>32; return h;
}
static inline int eq(const St*a,const St*b){
    return a->w0==b->w0&&a->w1==b->w1&&a->l0==b->l0&&a->l1==b->l1;
}

static St *pool; static uint32_t *par; static uint8_t *pmv;
static uint32_t *tab; static uint64_t mask; static uint32_t nst;

static uint32_t intern(const St*s,uint32_t parent,uint8_t mv,int *isnew){
    uint64_t i=hsh(s)&mask;
    for(;;){
        uint32_t e=tab[i];
        if(e==0xFFFFFFFFu){ pool[nst]=*s; par[nst]=parent; pmv[nst]=mv;
            tab[i]=nst; *isnew=1; return nst++; }
        if(eq(&pool[e],s)){ *isnew=0; return e; }
        i=(i+1)&mask;
    }
}
int main(int argc,char**argv){
    // argv: cap  maxstates  l0 w0letters... l1 w1letters...   (letters as 0..3)
    CAP=atoi(argv[1]); uint64_t maxst=strtoull(argv[2],0,10);
    if(CAP>32){ printf("CAP_TOO_LARGE %d (words pack 32 letters per uint64)\n",CAP); return 4; }
    int l0=atoi(argv[3]); uint8_t a[MAXW],b[MAXW];
    for(int i=0;i<l0;i++) a[i]=atoi(argv[4+i]);
    int l1=atoi(argv[4+l0]);
    for(int i=0;i<l1;i++) b[i]=atoi(argv[5+l0+i]);
    uint64_t cap2=1; while(cap2 < maxst*2) cap2<<=1; mask=cap2-1;
    pool=malloc(maxst*sizeof(St)); par=malloc(maxst*4); pmv=malloc(maxst);
    tab=malloc(cap2*4);
    if(!pool||!par||!pmv||!tab){ printf("ALLOC_FAIL\n"); return 1; }
    memset(tab,0xFF,cap2*4);
    St s0; s0.w0=pack(a,l0); s0.l0=l0; s0.w1=pack(b,l1); s0.l1=l1;
    St tgt; { uint8_t x[1]={0},y[1]={2}; tgt.w0=pack(x,1); tgt.l0=1; tgt.w1=pack(y,1); tgt.l1=1; }
    int isnew; uint32_t root=intern(&s0,0xFFFFFFFFu,255,&isnew);
    uint32_t head=0, depth=0, lvlend=nst;
    while(head<nst){
        uint32_t s_idx=head++;
        St cur=pool[s_idx]; St r;
        for(int m=0;m<14;m++){
            if(!apply(&cur,m,&r)) continue;
            uint32_t id=intern(&r,s_idx,(uint8_t)m,&isnew);
            if(isnew && eq(&r,&tgt)){
                // emit path
                printf("FOUND ");
                uint32_t c=id; int n=0; static uint8_t mv[100000];
                while(par[c]!=0xFFFFFFFFu){ mv[n++]=pmv[c]; c=par[c]; }
                for(int i=n-1;i>=0;i--) printf("%d ",mv[i]);
                printf("\n"); fflush(stdout); return 0;
            }
            if(nst>=maxst-2){ printf("BUDGET states=%u depth=%u\n",nst,depth); return 2; }
        }
        if(head==lvlend){ depth++; lvlend=nst;
            fprintf(stderr,"depth %u states %u\n",depth,nst); }
    }
    printf("EXHAUSTED states=%u depth=%u cap=%d\n",nst,depth,CAP);
    (void)root; return 3;
}
