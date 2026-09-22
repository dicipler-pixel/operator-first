// BIDIRECTIONAL corridor BFS for Andrews-Curtis (ac-r2-v1) -- v2.
//
// v1 reported EXHAUSTED only when BOTH frontiers emptied. That hid the
// strongest verdict the search can produce. If ONE side's frontier empties
// with no meet, that side's component is fully enumerated and the other
// endpoint is not in it -- the two lie in DIFFERENT COMPONENTS of the capped
// graph, which is a disconnection theorem regardless of what the other side
// is still doing. v1 mislabelled those runs BUDGET whenever the opposite
// side went on to fill its allocation, e.g. ac-02422 at cap 16, whose forward
// component closes at 476 states while the backward ball runs to 20M.
//
// The meet test is symmetric in time: every newly interned state is checked
// against the other side's table, on whichever side is expanding, so a state
// found early by one side is still detected when the other reaches it later.
// A closed side therefore stays sound as the open side grows.
//
// Verdicts: MEET (path found), CLOSED_F / CLOSED_B (disconnection, with the
// closed component's size), BUDGET (undecided -- but see
// ACC_PATH_LENGTH_BOUNDS_v1.md: df+db is still a proved lower bound).
//
// Usage: cap budget_per_side l0 r0... l1 r1... t0 tg0... t1 tg1...
// v1 and the three one-sided engines are unchanged.
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

static const uint8_t INV[14]={0,1,3,2,5,4,7,6,9,8,11,10,13,12};

typedef struct {
    St*pool; uint32_t*par; uint8_t*pmv; uint32_t*tab;
    uint64_t mask; uint32_t nst, head, lvlend, depth; uint64_t cap_states;
} Side;

static uint64_t MAXST;
static uint64_t MAXST_B, MAXST_F;

static int side_init_n(Side*S,uint64_t cap_states){
    MAXST=cap_states;
    uint64_t c2=1; while(c2<MAXST*2) c2<<=1;
    S->mask=c2-1; S->nst=0; S->head=0; S->lvlend=0; S->depth=0;
    S->pool=malloc(MAXST*sizeof(St)); S->par=malloc(MAXST*4);
    S->pmv=malloc(MAXST); S->tab=malloc(c2*4);
    if(!S->pool||!S->par||!S->pmv||!S->tab) return 0;
    memset(S->tab,0xFF,c2*4);
    S->cap_states=cap_states;
    return 1;
}
static void side_reset(Side*S){
    uint64_t c2=1; while(c2<S->cap_states*2) c2<<=1;
    S->nst=0; S->head=0; S->lvlend=0; S->depth=0;
    memset(S->tab,0xFF,c2*4);
}
static uint32_t side_intern(Side*S,const St*s,uint32_t p,uint8_t mv,int*isnew){
    uint64_t i=hsh(s)&S->mask;
    for(;;){ uint32_t e=S->tab[i];
        if(e==0xFFFFFFFFu){ S->pool[S->nst]=*s; S->par[S->nst]=p; S->pmv[S->nst]=mv;
                            S->tab[i]=S->nst; *isnew=1; return S->nst++; }
        if(eq(&S->pool[e],s)){ *isnew=0; return e; }
        i=(i+1)&S->mask; }
}
static uint32_t side_find(const Side*S,const St*s){
    uint64_t i=hsh(s)&S->mask;
    for(;;){ uint32_t e=S->tab[i];
        if(e==0xFFFFFFFFu) return 0xFFFFFFFFu;
        if(eq(&S->pool[e],s)) return e;
        i=(i+1)&S->mask; }
}
// moves from the side's root down to index i, in application order
static int chain(const Side*S,uint32_t i,uint8_t*out){
    uint8_t tmp[100000]; int n=0;
    while(S->par[i]!=0xFFFFFFFFu){ tmp[n++]=S->pmv[i]; i=S->par[i]; }
    for(int k=0;k<n;k++) out[k]=tmp[n-1-k];
    return n;
}

// ---------------------------------------------------------------------------
// Escape-radius sweep.
//
// Only exit states with exactly ONE edge back into K_W can ever be ADVANCE:
// if there are two or more, forbidding one still leaves another and the state
// returns at depth 1. So for each such exit, forbid that one edge as the first
// move and BFS under cap W+1 to find the minimum number of moves back into
// K_W. The histogram of that distance gives the ADVANCE count at EVERY radius
// at once: ADVANCE(R) = #{ exits with min_return_dist > R }.
//
// Sampled by stride to keep the sweep cheap; the population is reported so the
// fractions can be scaled.
//
// Usage: acc_radius W kbudget ebudget sample maxdepth localcap l0 a.. l1 b..
// ---------------------------------------------------------------------------
static Side K, E, L;
static int in_K(const St*s){ return side_find(&K,s)!=0xFFFFFFFFu; }

int main(int argc,char**argv){
    if(argc<9){ printf("usage: W kb eb sample maxdepth localcap l0 a.. l1 b..\n"); return 2; }
    int W=atoi(argv[1]);
    uint64_t kb=strtoull(argv[2],0,10), eb=strtoull(argv[3],0,10);
    uint32_t sample=(uint32_t)strtoul(argv[4],0,10);
    int maxd=atoi(argv[5]);
    uint64_t lc=strtoull(argv[6],0,10);
    int ai=7;
    int l0=atoi(argv[ai++]); uint8_t a[MAXW]; for(int i=0;i<l0;i++) a[i]=(uint8_t)atoi(argv[ai++]);
    int l1=atoi(argv[ai++]); uint8_t b[MAXW]; for(int i=0;i<l1;i++) b[i]=(uint8_t)atoi(argv[ai++]);
    if(!side_init_n(&K,kb)||!side_init_n(&E,eb)||!side_init_n(&L,lc)){ printf("ALLOC_FAIL\n"); return 1; }

    CAP=W;
    St s0; memset(&s0,0,sizeof s0);
    packw(a,l0,&s0.a0,&s0.b0); s0.l0=l0;
    packw(b,l1,&s0.a1,&s0.b1); s0.l1=l1;
    int isnew;
    side_intern(&K,&s0,0xFFFFFFFFu,255,&isnew); K.lvlend=K.nst;
    while(K.lvlend>K.head && K.nst+64<kb){
        uint32_t stop=K.lvlend;
        while(K.head<stop && K.nst+64<kb){
            uint32_t si=K.head++; St cur=K.pool[si],r;
            for(int m=0;m<14;m++){ if(!apply(&cur,m,&r)) continue;
                side_intern(&K,&r,si,(uint8_t)m,&isnew); }
        }
        K.depth++; K.lvlend=K.nst;
    }
    if(K.lvlend>K.head){ printf("K_NOT_CLOSED\n"); return 3; }
    printf("K_W W=%d CLOSED states=%u\n",W,K.nst); fflush(stdout);

    CAP=W+1;
    for(uint32_t i=0;i<K.nst;i++){
        St cur=K.pool[i],r;
        for(int m=0;m<14;m++){ if(!apply(&cur,m,&r)) continue;
            if(in_K(&r)) continue; side_intern(&E,&r,i,(uint8_t)m,&isnew); }
    }
    printf("EXITS distinct=%u\n",E.nst); fflush(stdout);

    // population of b==1 exits
    uint32_t nb1=0;
    for(uint32_t i=0;i<E.nst;i++){
        St s=E.pool[i],x; int nb=0;
        for(int m=0;m<14;m++){ if(!apply(&s,m,&x)) continue; if(in_K(&x)) nb++; }
        if(nb==1) nb1++;
    }
    printf("EXITS_b_eq1=%u (only these can ever be ADVANCE)\n",nb1); fflush(stdout);
    { uint64_t byclass[3]={0,0,0};
      for(uint32_t i=0;i<E.nst;i++){ uint8_t mv=E.pmv[i];
        if(mv<=1) byclass[0]++; else if(mv<=5) byclass[1]++; else byclass[2]++; }
      printf("ENTERING_MOVE inv(0-1)=%llu mul(2-5)=%llu conj(6-13)=%llu\n",
        (unsigned long long)byclass[0],(unsigned long long)byclass[1],
        (unsigned long long)byclass[2]); fflush(stdout); }

    uint32_t stride = nb1>sample ? nb1/sample : 1;
    uint64_t hist[32]; memset(hist,0,sizeof hist);
    uint64_t unresolved=0, taken=0, seen=0;

    for(uint32_t i=0;i<E.nst && taken<sample;i++){
        St s=E.pool[i],x; int nb=0, only=-1;
        for(int m=0;m<14;m++){ if(!apply(&s,m,&x)) continue; if(in_K(&x)){nb++; only=m;} }
        if(nb!=1) continue;
        if(seen++ % stride) continue;
        taken++;

        side_reset(&L);
        side_intern(&L,&s,0xFFFFFFFFu,255,&isnew); L.lvlend=L.nst;
        int d=0, found=0;
        while(!found && L.lvlend>L.head && L.nst+64<lc && d<maxd){
            uint32_t stop=L.lvlend;
            while(L.head<stop && L.nst+64<lc){
                uint32_t si=L.head++; St cur=L.pool[si],r;
                for(int m=0;m<14;m++){
                    if(si==0 && m==only) continue;      // forbid the one edge back
                    if(!apply(&cur,m,&r)) continue;
                    if(in_K(&r)){ found=d+1; break; }
                    side_intern(&L,&r,si,(uint8_t)m,&isnew);
                }
                if(found) break;
            }
            if(found) break;
            d++; L.lvlend=L.nst;
        }
        if(found && found<32) hist[found]++; else unresolved++;
    }
    printf("SAMPLED %llu of %u  (stride %u)\n",(unsigned long long)taken,nb1,stride);
    printf("min_return_dist histogram:\n");
    for(int k=1;k<32;k++) if(hist[k]) printf("  d=%d : %llu\n",k,(unsigned long long)hist[k]);
    if(unresolved) printf("  unresolved (>=maxdepth or local cap) : %llu\n",(unsigned long long)unresolved);
    uint64_t cum=0;
    printf("ADVANCE(R) = sampled exits with min_return_dist > R:\n");
    for(int R=1;R<=maxd;R++){
        cum=0; for(int k=1;k<=R;k++) cum+=hist[k];
        printf("  R=%d : %llu of %llu\n",R,(unsigned long long)(taken-cum),(unsigned long long)taken);
    }
    return 0;
}
