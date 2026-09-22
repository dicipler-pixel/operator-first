// Direct meet from the wall, ac-r2-v1 (SAIR a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e).
//
// Compact packed-64 state. For cap <= 31 every relator word has <= 31 letters,
// so at 2 bits per letter each word fits one uint64 and the high halves of the
// original 4-word layout are provably always zero. 24 bytes per state instead
// of 40. Asserted at run time.
//
// Phases: build T_16 ball from (x,y); close K_W; take ALL exits at length W+1;
// multi-source BFS from those exits under the meet cap, testing ball
// membership on every newly interned state.
//
// K_W is pre-seeded into the search table as already-visited. That is sound and
// loses nothing: if K_W contained any T_16 state t, then (x,y) would be
// reachable from the start within cap max(W,16) = W, contradicting the measured
// "target absent" verdict at cap W. So K_W is disjoint from T_16 and re-walking
// it could not produce a hit.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXW 32
typedef struct { uint64_t a0,a1; uint8_t l0,l1; } St;
static int CAP;
static inline void packw(const uint8_t*w,int n,uint64_t*lo){
    uint64_t L=0; for(int i=0;i<n;i++) L|=((uint64_t)(w[i]&3))<<(2*i); *lo=L;
}
static inline void unpackw(uint64_t lo,int n,uint8_t*w){
    for(int i=0;i<n;i++) w[i]=(lo>>(2*i))&3;
}
static inline int reduce(const uint8_t*in,int n,uint8_t*out){
    int t=0; for(int i=0;i<n;i++){ uint8_t c=in[i];
        if(t>0&&out[t-1]==(c^1)) t--; else out[t++]=c; } return t;
}
static inline int invword(const uint8_t*a,int n,uint8_t*o){
    for(int i=0;i<n;i++) o[i]=a[n-1-i]^1; return n;
}
static int apply(const St*s,int m,St*r){
    uint8_t a[MAXW+2],b[MAXW+2],t[2*MAXW+8],u[2*MAXW+8];
    int la=s->l0, lb=s->l1, lt,lu;
    unpackw(s->a0,la,a); unpackw(s->a1,lb,b);
    *r=*s;
    if(m==0){ lu=invword(a,la,u); packw(u,lu,&r->a0); r->l0=lu; }
    else if(m==1){ lu=invword(b,lb,u); packw(u,lu,&r->a1); r->l1=lu; }
    else if(m==2||m==3){
        memcpy(t,a,la); lt=la;
        if(m==2){ memcpy(t+lt,b,lb); lt+=lb; } else { lt+=invword(b,lb,t+lt); }
        lu=reduce(t,lt,u); if(lu+lb>CAP||lu>31) return 0;
        packw(u,lu,&r->a0); r->l0=lu;
    } else if(m==4||m==5){
        memcpy(t,b,lb); lt=lb;
        if(m==4){ memcpy(t+lt,a,la); lt+=la; } else { lt+=invword(a,la,t+lt); }
        lu=reduce(t,lt,u); if(lu+la>CAP||lu>31) return 0;
        packw(u,lu,&r->a1); r->l1=lu;
    } else {
        int on0=(m<=9); int k=on0?m-6:m-10; uint8_t g=(uint8_t)k, gi=g^1;
        const uint8_t*src=on0?a:b; int ls=on0?la:lb;
        t[0]=g; memcpy(t+1,src,ls); t[ls+1]=gi; lt=ls+2;
        lu=reduce(t,lt,u); int other=on0?lb:la;
        if(lu+other>CAP||lu>31) return 0;
        if(on0){ packw(u,lu,&r->a0); r->l0=lu; } else { packw(u,lu,&r->a1); r->l1=lu; }
    }
    return 1;
}
static inline uint64_t hsh(const St*s){
    uint64_t h=0x9E3779B97F4A7C15ULL;
    h^=(s->a0+0x165667B19E3779F9ULL); h*=0xC2B2AE3D27D4EB4FULL;
    h^=(s->a1+0x27D4EB2F165667C5ULL); h*=0x9E3779B97F4A7C15ULL;
    h^=((uint64_t)s->l0<<56)^((uint64_t)s->l1<<48);
    h^=h>>29; h*=0xBF58476D1CE4E5B9ULL; h^=h>>32; return h;
}
static inline int eq(const St*x,const St*y){
    return x->a0==y->a0&&x->a1==y->a1&&x->l0==y->l0&&x->l1==y->l1;
}
static const uint8_t INV[14]={0,1,3,2,5,4,7,6,9,8,11,10,13,12};
typedef struct { St*pool; uint32_t*par; uint8_t*pmv; uint32_t*tab;
    uint64_t mask; uint32_t nst,head,lvlend,depth; } Side;
static int side_init(Side*S,uint64_t n){
    uint64_t c2=1; while(c2<n*2) c2<<=1;
    S->mask=c2-1; S->nst=S->head=S->lvlend=S->depth=0;
    S->pool=malloc(n*sizeof(St)); S->par=malloc(n*4); S->pmv=malloc(n); S->tab=malloc(c2*4);
    if(!S->pool||!S->par||!S->pmv||!S->tab) return 0;
    memset(S->tab,0xFF,c2*4); return 1;
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
        if(eq(&S->pool[e],s)) return e; i=(i+1)&S->mask; }
}
static int chain(const Side*S,uint32_t i,uint8_t*out){
    static uint8_t tmp[1<<20]; int n=0;
    while(S->par[i]!=0xFFFFFFFFu){ tmp[n++]=S->pmv[i]; i=S->par[i]; }
    for(int k=0;k<n;k++) out[k]=tmp[n-1-k]; return n;
}
static Side B,S;
int main(int argc,char**argv){
    if(argc<9){ printf("usage: ballcap ballbudget W meetcap depth sbudget l0 a.. l1 b..\n"); return 2; }
    int ballcap=atoi(argv[1]); uint64_t bb=strtoull(argv[2],0,10);
    int W=atoi(argv[3]); int meetcap=atoi(argv[4]); int maxd=atoi(argv[5]);
    uint64_t sb=strtoull(argv[6],0,10);
    int ai=7;
    int l0=atoi(argv[ai++]); uint8_t a[MAXW]; for(int i=0;i<l0;i++) a[i]=(uint8_t)atoi(argv[ai++]);
    int l1=atoi(argv[ai++]); uint8_t b[MAXW]; for(int i=0;i<l1;i++) b[i]=(uint8_t)atoi(argv[ai++]);
    if(meetcap>31){ printf("MEETCAP_GT_31 %d (compact state invalid)\n",meetcap); return 4; }
    if(!side_init(&B,bb)||!side_init(&S,sb)){ printf("ALLOC_FAIL\n"); return 1; }

    // ---- T_16 ball ----
    CAP=ballcap;
    St sg; memset(&sg,0,sizeof sg);
    { uint8_t ta[1]={0},tb[1]={2}; packw(ta,1,&sg.a0); sg.l0=1; packw(tb,1,&sg.a1); sg.l1=1; }
    int isnew; side_intern(&B,&sg,0xFFFFFFFFu,255,&isnew); B.lvlend=B.nst;
    while(B.lvlend>B.head && B.nst+64<bb){
        uint32_t stop=B.lvlend;
        while(B.head<stop && B.nst+64<bb){
            uint32_t si=B.head++; St cur=B.pool[si],r;
            for(int m=0;m<14;m++){ if(!apply(&cur,m,&r)) continue;
                side_intern(&B,&r,si,(uint8_t)m,&isnew); }
        }
        B.depth++; B.lvlend=B.nst;
    }
    printf("BALL cap=%d states=%u depth=%u\n",ballcap,B.nst,B.depth); fflush(stdout);

    // ---- close K_W ----
    CAP=W;
    St s0; memset(&s0,0,sizeof s0);
    packw(a,l0,&s0.a0); s0.l0=l0; packw(b,l1,&s0.a1); s0.l1=l1;
    side_intern(&S,&s0,0xFFFFFFFFu,255,&isnew); S.lvlend=S.nst;
    while(S.lvlend>S.head && S.nst+64<sb){
        uint32_t stop=S.lvlend;
        while(S.head<stop && S.nst+64<sb){
            uint32_t si=S.head++; St cur=S.pool[si],r;
            for(int m=0;m<14;m++){ if(!apply(&cur,m,&r)) continue;
                side_intern(&S,&r,si,(uint8_t)m,&isnew); }
        }
        S.depth++; S.lvlend=S.nst;
    }
    uint32_t nK=S.nst;
    printf("K_W W=%d states=%u %s\n",W,nK,(S.lvlend<=S.head)?"CLOSED":"BUDGET"); fflush(stdout);

    // ---- X: ALL exit states at length W+1 ----
    CAP=W+1;
    for(uint32_t i=0;i<nK && S.nst+64<sb;i++){
        St cur=S.pool[i],r;
        for(int m=0;m<14;m++){ if(!apply(&cur,m,&r)) continue;
            side_intern(&S,&r,i,(uint8_t)m,&isnew); }
    }
    uint32_t nX=S.nst-nK;
    printf("X exits=%u\n",nX); fflush(stdout);

    // ---- multi-source BFS under meetcap ----
    CAP=meetcap;
    S.head=nK; S.lvlend=S.nst; S.depth=0;
    int minlen=99; uint32_t hit=0xFFFFFFFFu, bidx=0;
    for(uint32_t i=nK;i<S.nst;i++){ int L=S.pool[i].l0+S.pool[i].l1; if(L<minlen) minlen=L; }
    while(hit==0xFFFFFFFFu && S.lvlend>S.head && S.nst+64<sb && S.depth<maxd){
        uint32_t stop=S.lvlend;
        while(S.head<stop && S.nst+64<sb){
            uint32_t si=S.head++; St cur=S.pool[si],r;
            for(int m=0;m<14;m++){
                if(!apply(&cur,m,&r)) continue;
                uint32_t id=side_intern(&S,&r,si,(uint8_t)m,&isnew);
                if(!isnew) continue;
                int L=r.l0+r.l1; if(L<minlen) minlen=L;
                uint32_t o=side_find(&B,&r);
                if(o!=0xFFFFFFFFu){ hit=id; bidx=o; break; }
            }
            if(hit!=0xFFFFFFFFu) break;
        }
        if(hit!=0xFFFFFFFFu) break;
        S.depth++; S.lvlend=S.nst;
        fprintf(stderr,"  depth %u states %u minlen %d\n",S.depth,S.nst,minlen);
    }
    printf("VISITED total=%u beyond_K=%u depth=%u minlen=%d\n",
           S.nst,S.nst-nK,S.depth,minlen);
    if(hit!=0xFFFFFFFFu){
        static uint8_t mf[1<<20],mb[1<<20],out[1<<21];
        int nf=chain(&S,hit,mf), nbk=chain(&B,bidx,mb), n=0;
        for(int k=0;k<nf;k++) out[n++]=mf[k];
        for(int k=nbk-1;k>=0;k--) out[n++]=INV[mb[k]];
        printf("MEET len=%d\nMOVES",n);
        for(int k=0;k<n;k++) printf(" %d",out[k]);
        printf("\n");
    } else {
        printf("%s\n",(S.nst+64>=sb)?"NO_MEET_BUDGET":(S.depth>=maxd?"NO_MEET_DEPTH":"NO_MEET_EXHAUSTED"));
    }
    return 0;
}
