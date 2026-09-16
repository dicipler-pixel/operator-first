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
    uint64_t mask; uint32_t nst, head, lvlend, depth;
} Side;

static uint64_t MAXST;

static int side_init(Side*S){
    uint64_t c2=1; while(c2<MAXST*2) c2<<=1;
    S->mask=c2-1; S->nst=0; S->head=0; S->lvlend=0; S->depth=0;
    S->pool=malloc(MAXST*sizeof(St)); S->par=malloc(MAXST*4);
    S->pmv=malloc(MAXST); S->tab=malloc(c2*4);
    if(!S->pool||!S->par||!S->pmv||!S->tab) return 0;
    memset(S->tab,0xFF,c2*4);
    return 1;
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

int main(int argc,char**argv){
    CAP=atoi(argv[1]); MAXST=strtoull(argv[2],0,10);
    if(CAP>MAXW){ printf("CAP_TOO_LARGE %d\n",CAP); return 4; }
    int l0=atoi(argv[3]); uint8_t a[MAXW],b[MAXW];
    for(int i=0;i<l0;i++) a[i]=atoi(argv[4+i]);
    int l1=atoi(argv[4+l0]);
    for(int i=0;i<l1;i++) b[i]=atoi(argv[5+l0+i]);
    int p=5+l0+l1;
    int t0=atoi(argv[p++]); uint8_t ta[MAXW],tb[MAXW];
    for(int i=0;i<t0;i++) ta[i]=atoi(argv[p++]);
    int t1=atoi(argv[p++]);
    for(int i=0;i<t1;i++) tb[i]=atoi(argv[p++]);
    if(l0+l1>CAP){ printf("START_OUTSIDE_CAP %d cap=%d\n",l0+l1,CAP); return 6; }
    if(t0+t1>CAP){ printf("TARGET_OUTSIDE_CAP %d cap=%d\n",t0+t1,CAP); return 6; }

    St s0,sg; memset(&s0,0,sizeof s0); memset(&sg,0,sizeof sg);
    packw(a,l0,&s0.a0,&s0.b0); s0.l0=l0; packw(b,l1,&s0.a1,&s0.b1); s0.l1=l1;
    packw(ta,t0,&sg.a0,&sg.b0); sg.l0=t0; packw(tb,t1,&sg.a1,&sg.b1); sg.l1=t1;
    if(eq(&s0,&sg)){ printf("MEET len=0 states_f=0 states_b=0\nMOVES\n"); return 0; }

    Side F,B;
    if(!side_init(&F)||!side_init(&B)){ printf("ALLOC_FAIL\n"); return 1; }
    int isnew;
    side_intern(&F,&s0,0xFFFFFFFFu,255,&isnew); F.lvlend=F.nst;
    side_intern(&B,&sg,0xFFFFFFFFu,255,&isnew); B.lvlend=B.nst;

    for(;;){
        // expand whichever side has the smaller pending frontier
        uint32_t fpend=F.lvlend-F.head, bpend=B.lvlend-B.head;
        Side*S; Side*O; int fwd;
        // A single empty frontier already decides it: that component is
        // complete and does not contain the other endpoint.
        if(fpend==0){
            printf("CLOSED_F component=%u depth_f=%u states_b=%u depth_b=%u cap=%d\n",
                   F.nst,F.depth,B.nst,B.depth,CAP); return 3; }
        if(bpend==0){
            printf("CLOSED_B component=%u depth_b=%u states_f=%u depth_f=%u cap=%d\n",
                   B.nst,B.depth,F.nst,F.depth,CAP); return 3; }
        if(fpend<=bpend){ S=&F;O=&B;fwd=1; } else { S=&B;O=&F;fwd=0; }

        uint32_t stop=S->lvlend;
        while(S->head<stop){
            uint32_t si=S->head++; St cur=S->pool[si],r;
            for(int m=0;m<14;m++){
                if(!apply(&cur,m,&r)) continue;
                uint32_t id=side_intern(S,&r,si,(uint8_t)m,&isnew);
                if(!isnew) continue;
                uint32_t o=side_find(O,&r);
                if(o!=0xFFFFFFFFu){
                    // MEET. Build start -> meet -> target.
                    static uint8_t mf[100000],mb[100000],out[200000];
                    int nf,nb,n=0;
                    if(fwd){ nf=chain(S,id,mf); nb=chain(O,o,mb); }
                    else   { nf=chain(O,o,mf);  nb=chain(S,id,mb); }
                    for(int k=0;k<nf;k++) out[n++]=mf[k];            // start -> meet
                    for(int k=nb-1;k>=0;k--) out[n++]=INV[mb[k]];    // meet -> target
                    printf("MEET len=%d states_f=%u states_b=%u depth_f=%u depth_b=%u\n",
                           n,F.nst,B.nst,F.depth,B.depth);
                    printf("MOVES");
                    for(int k=0;k<n;k++) printf(" %d",out[k]);
                    printf("\n");
                    return 0;
                }
                if(S->nst>=MAXST-2){
                    printf("BUDGET states_f=%u states_b=%u depth_f=%u depth_b=%u\n",
                           F.nst,B.nst,F.depth,B.depth); return 2; }
            }
        }
        S->depth++; S->lvlend=S->nst;
        fprintf(stderr,"%s depth %u states %u\n",fwd?"F":"B",S->depth,S->nst);
    }
}
