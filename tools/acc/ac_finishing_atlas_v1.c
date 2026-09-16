// FINISHING ATLAS for Andrews-Curtis (ac-r2-v1), 64-letter relators.
//
// Measured in the bidirectional runs: states_b is IDENTICAL across every
// challenge at a given cap -- 2,452,439 at radius 7, 15,614,326 at radius 8,
// cap 23. Of course it is. The ball around the target [[1],[2]] does not
// depend on which challenge is being searched. Yet every bidirectional run
// rebuilt it and spent most of its allocation doing so.
//
// This engine builds the target ball ONCE, then streams every challenge's
// forward search against it. The atlas cost is paid a single time for the
// whole batch, the full forward allocation goes to the corridor, and the
// atlas radius can be pushed far past the 7-8 a shared budget allowed --
// which shortens the forward depth a solve needs by exactly that much.
//
// Only fully expanded atlas levels count: the recorded radius R is the last
// complete level, so "no path of length <= df + R" stays sound.
//
// Usage: cap atlas_budget fwd_budget N  (l0 r0... l1 r1...) x N
// Per challenge: MEET / CLOSED_F / BUDGET, with the bound df + R.
// The four earlier engines are unchanged.
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
    uint64_t mask; uint32_t nst, head, lvlend, depth;
} Side;
static int side_init(Side*S,uint64_t cap_states){
    uint64_t c2=1; while(c2<cap_states*2) c2<<=1;
    S->mask=c2-1; S->nst=0; S->head=0; S->lvlend=0; S->depth=0;
    S->pool=malloc(cap_states*sizeof(St)); S->par=malloc(cap_states*4);
    S->pmv=malloc(cap_states); S->tab=malloc(c2*4);
    if(!S->pool||!S->par||!S->pmv||!S->tab) return 0;
    memset(S->tab,0xFF,c2*4); return 1;
}
static void side_reset(Side*S,uint64_t cap_states){
    uint64_t c2=1; while(c2<cap_states*2) c2<<=1;
    S->nst=0; S->head=0; S->lvlend=0; S->depth=0; memset(S->tab,0xFF,c2*4);
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
static int chain(const Side*S,uint32_t i,uint8_t*out){
    static uint8_t tmp[100000]; int n=0;
    while(S->par[i]!=0xFFFFFFFFu){ tmp[n++]=S->pmv[i]; i=S->par[i]; }
    for(int k=0;k<n;k++) out[k]=tmp[n-1-k];
    return n;
}
static void rdw(char**argv,int*p,uint8_t*w,int*n){
    *n=atoi(argv[(*p)++]); for(int i=0;i<*n;i++) w[i]=atoi(argv[(*p)++]);
}
int main(int argc,char**argv){
    CAP=atoi(argv[1]);
    uint64_t ABUD=strtoull(argv[2],0,10), FBUD=strtoull(argv[3],0,10);
    if(CAP>MAXW){ printf("CAP_TOO_LARGE %d\n",CAP); return 4; }
    int N=atoi(argv[4]); int p=5;

    Side A,F;
    if(!side_init(&A,ABUD)||!side_init(&F,FBUD)){ printf("ALLOC_FAIL\n"); return 1; }

    // ---- phase 1: the atlas, built once ----
    St sg; memset(&sg,0,sizeof sg);
    { uint8_t g0[1]={0},g1[1]={2};   // target (x, y) = [[1],[2]]
      packw(g0,1,&sg.a0,&sg.b0); sg.l0=1; packw(g1,1,&sg.a1,&sg.b1); sg.l1=1; }
    int isnew; side_intern(&A,&sg,0xFFFFFFFFu,255,&isnew); A.lvlend=A.nst;
    uint32_t atlas_R=0;
    while(A.head<A.lvlend){
        uint32_t stop=A.lvlend; int full=1;
        while(A.head<stop){
            uint32_t si=A.head++; St cur=A.pool[si],r;
            for(int m=0;m<14;m++){
                if(!apply(&cur,m,&r)) continue;
                side_intern(&A,&r,si,(uint8_t)m,&isnew);
                if(A.nst>=ABUD-2){ full=0; break; }
            }
            if(!full) break;
        }
        if(!full) break;                 // partial level: do NOT count it
        A.depth++; A.lvlend=A.nst; atlas_R=A.depth;
        fprintf(stderr,"atlas radius %u states %u\n",atlas_R,A.nst);
    }
    printf("ATLAS cap=%d radius=%u states=%u\n",CAP,atlas_R,A.nst); fflush(stdout);

    // ---- phase 2: stream the challenges ----
    for(int c=0;c<N;c++){
        uint8_t a[MAXW],b[MAXW]; int l0,l1;
        rdw(argv,&p,a,&l0); rdw(argv,&p,b,&l1);
        if(l0+l1>CAP){ printf("CH %d OUTSIDE_CAP\n",c); continue; }
        side_reset(&F,FBUD);
        St s0; memset(&s0,0,sizeof s0);
        packw(a,l0,&s0.a0,&s0.b0); s0.l0=l0; packw(b,l1,&s0.a1,&s0.b1); s0.l1=l1;
        side_intern(&F,&s0,0xFFFFFFFFu,255,&isnew); F.lvlend=F.nst;
        uint32_t o=side_find(&A,&s0);
        if(o!=0xFFFFFFFFu){
            static uint8_t mb[100000]; int nb=chain(&A,o,mb);
            printf("CH %d MEET len=%d",c,nb); 
            printf(" MOVES"); for(int k=nb-1;k>=0;k--) printf(" %d",INV[mb[k]]);
            printf("\n"); fflush(stdout); continue;
        }
        int done=0;
        while(!done && F.head<F.lvlend){
            uint32_t stop=F.lvlend;
            while(F.head<stop){
                uint32_t si=F.head++; St cur=F.pool[si],r;
                for(int m=0;m<14;m++){
                    if(!apply(&cur,m,&r)) continue;
                    uint32_t id=side_intern(&F,&r,si,(uint8_t)m,&isnew);
                    if(!isnew) continue;
                    uint32_t j=side_find(&A,&r);
                    if(j!=0xFFFFFFFFu){
                        static uint8_t mf[100000],mb[100000]; int nf=chain(&F,id,mf),nb=chain(&A,j,mb);
                        printf("CH %d MEET len=%d",c,nf+nb);
                        printf(" MOVES");
                        for(int k=0;k<nf;k++) printf(" %d",mf[k]);
                        for(int k=nb-1;k>=0;k--) printf(" %d",INV[mb[k]]);
                        printf("\n"); fflush(stdout); done=1; break;
                    }
                    if(F.nst>=FBUD-2){
                        printf("CH %d BUDGET states=%u depth=%u bound=%u\n",
                               c,F.nst,F.depth,F.depth+atlas_R); fflush(stdout); done=1; break;
                    }
                }
                if(done) break;
            }
            if(done) break;
            F.depth++; F.lvlend=F.nst;
        }
        if(!done) printf("CH %d CLOSED_F component=%u depth=%u\n",c,F.nst,F.depth), fflush(stdout);
    }
    return 0;
}
