// COMPOUND EYE HARNESS — census inside the C enumerator loop.
//
// HARNESS v2's design note: "embed the cheap HARNESS census directly inside that C
// proposal loop. Then the 14 labelled responses cost almost nothing extra, because the
// enumerator is already generating those 14 children."
//
// That is exactly what this does. The BFS already calls apply() fourteen times per state
// to expand it. The labelled response is harvested from those same proposals — no second
// pass, no recomputation. The marginal cost of the census is a few integer ops per child.
//
// Retention rule, from the design doc: a compressed signature is NEVER exact state
// equality. Every record carries the exact freely-reduced ordered pair as text so the
// Python reference harness can re-derive anything and check it. The channel codes route
// attention; they never prune and never certify.
//
// Emits JSONL, one line per state, with the fields the Python harness computes:
//   state, total_length, lengths, imbalance, M (exponent ledger), detM,
//   outcome_by_move   (14 chars, D/S/U by length delta)          -- interior census
//   boundary_outcome_by_move (14 chars, R when the child re-enters the component)
//   delta_total_by_move (14 ints)
//
// Usage: census cap r0 r1 mode          mode = component | boundary
//        words use x X y Y  (capital = inverse)
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
// Identical move grammar to the official verifier and to the Python harness:
// 0/1 invert, 2-5 multiply, 6-9 conjugate r0, 10-13 conjugate r1.
// NOTE: no cap filtering here. The census must see every proposal, including the ones
// that leave the component; the caller decides what the cap means.
static int apply_nocap(const St*s,int m,St*r){
    uint8_t a[MAXW],b[MAXW],t[2*MAXW+4],u[2*MAXW+4];
    int la=s->l0, lb=s->l1, lt,lu;
    unpackw(s->a0,s->b0,la,a); unpackw(s->a1,s->b1,lb,b);
    *r=*s;
    if(m==0){ lu=invword(a,la,u); packw(u,lu,&r->a0,&r->b0); r->l0=lu; }
    else if(m==1){ lu=invword(b,lb,u); packw(u,lu,&r->a1,&r->b1); r->l1=lu; }
    else if(m==2||m==3){
        memcpy(t,a,la); lt=la;
        if(m==2){ memcpy(t+lt,b,lb); lt+=lb; } else { lt+=invword(b,lb,t+lt); }
        lu=reduce(t,lt,u); if(lu>MAXW) return 0;
        packw(u,lu,&r->a0,&r->b0); r->l0=lu;
    } else if(m==4||m==5){
        memcpy(t,b,lb); lt=lb;
        if(m==4){ memcpy(t+lt,a,la); lt+=la; } else { lt+=invword(a,la,t+lt); }
        lu=reduce(t,lt,u); if(lu>MAXW) return 0;
        packw(u,lu,&r->a1,&r->b1); r->l1=lu;
    } else {
        int on0=(m<=9); int k=on0?m-6:m-10; uint8_t g=(uint8_t)k, gi=g^1;
        const uint8_t*src=on0?a:b; int ls=on0?la:lb;
        t[0]=g; memcpy(t+1,src,ls); t[ls+1]=gi;
        lu=reduce(t,ls+2,u); if(lu>MAXW) return 0;
        if(on0){ packw(u,lu,&r->a0,&r->b0); r->l0=lu; }
        else   { packw(u,lu,&r->a1,&r->b1); r->l1=lu; }
    }
    return 1;
}
static inline int tot(const St*s){ return s->l0+s->l1; }
static inline int eq(const St*x,const St*y){
    return x->a0==y->a0&&x->b0==y->b0&&x->a1==y->a1&&x->b1==y->b1&&x->l0==y->l0&&x->l1==y->l1;
}
static uint64_t hsh(const St*s){
    uint64_t h=0x9E3779B97F4A7C15ULL;
    h^=(s->a0+0x9E3779B97F4A7C15ULL); h*=0xFF51AFD7ED558CCDULL;
    h^=(s->b0+0xC2B2AE3D27D4EB4FULL); h*=0x165667B19E3779F9ULL;
    h^=(s->a1+0x27D4EB2F165667C5ULL); h*=0x9E3779B97F4A7C15ULL;
    h^=(s->b1+0x94D049BB133111EBULL);
    h^=((uint64_t)s->l0<<56)^((uint64_t)s->l1<<48);
    h^=h>>29; h*=0xBF58476D1CE4E5B9ULL; h^=h>>32; return h;
}
static St *pool; static uint32_t *tab; static uint64_t mask; static uint32_t nst;
static uint32_t intern(const St*s,int*isnew){
    uint64_t i=hsh(s)&mask;
    for(;;){ uint32_t e=tab[i];
        if(e==0xFFFFFFFFu){ pool[nst]=*s; tab[i]=nst; *isnew=1; return nst++; }
        if(eq(&pool[e],s)){ *isnew=0; return e; }
        i=(i+1)&mask; }
}
static uint32_t find(const St*s){
    uint64_t i=hsh(s)&mask;
    for(;;){ uint32_t e=tab[i];
        if(e==0xFFFFFFFFu) return 0xFFFFFFFFu;
        if(eq(&pool[e],s)) return e;
        i=(i+1)&mask; }
}
static int cmp_u64(const void*A,const void*B){
    uint64_t a=*(const uint64_t*)A, b=*(const uint64_t*)B;
    return (a>b)-(a<b);
}
static const char LET[4]={'x','X','y','Y'};
static void wtext(uint64_t lo,uint64_t hi,int n,char*out){
    uint8_t w[MAXW]; unpackw(lo,hi,n,w);
    for(int i=0;i<n;i++) out[i]=LET[w[i]];
    out[n]= n?0:0; if(!n){ out[0]='1'; out[1]=0; }
}
// exponent ledger: (sum of x-exponents, sum of y-exponents) per relator
static void expsum(uint64_t lo,uint64_t hi,int n,int*ex,int*ey){
    uint8_t w[MAXW]; unpackw(lo,hi,n,w); *ex=0;*ey=0;
    for(int i=0;i<n;i++){ if(w[i]<2) *ex += (w[i]==0)?1:-1; else *ey += (w[i]==2)?1:-1; }
}
static int parse(const char*s,uint8_t*w){
    int n=0; for(const char*p=s;*p;p++){
        if(*p=='1'&&n==0&&p[1]==0) break;
        switch(*p){ case 'x': w[n++]=0;break; case 'X': w[n++]=1;break;
                    case 'y': w[n++]=2;break; case 'Y': w[n++]=3;break;
                    default: return -1; } }
    uint8_t o[MAXW]; int r=reduce(w,n,o); memcpy(w,o,r); return r;
}
int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,"usage: census cap r0 r1 component|boundary|collide\n"); return 2; }
    CAP=atoi(argv[1]);
    uint8_t a[MAXW],b[MAXW];
    int la=parse(argv[2],a), lb=parse(argv[3],b);
    if(la<0||lb<0){ fprintf(stderr,"bad word\n"); return 2; }
    int want_boundary = strcmp(argv[4],"boundary")==0;
    int want_collide  = strcmp(argv[4],"collide")==0;

    uint64_t cap2=1; while(cap2< (1ULL<<26)) cap2<<=1;
    pool=malloc((size_t)(1<<25)*sizeof(St)); tab=malloc(cap2*4);
    if(!pool||!tab){ fprintf(stderr,"alloc\n"); return 1; }
    memset(tab,0xFF,cap2*4); mask=cap2-1; nst=0;

    St s0; memset(&s0,0,sizeof s0);
    packw(a,la,&s0.a0,&s0.b0); s0.l0=la;
    packw(b,lb,&s0.a1,&s0.b1); s0.l1=lb;
    int isnew; intern(&s0,&isnew);
    // BFS the capped component. Each expansion generates all 14 children anyway.
    for(uint32_t head=0; head<nst; head++){
        St cur=pool[head],r;
        for(int m=0;m<14;m++){
            if(!apply_nocap(&cur,m,&r)) continue;
            if(tot(&r)<=CAP) intern(&r,&isnew);
        }
    }
    uint32_t ncomp=nst;
    fprintf(stderr,"component=%u cap=%d\n",ncomp,CAP);

    // COLLISION PASS. The architecture escalates to Magnus/Fox only on cells where a
    // cheaper recorded view merges states. So the number that sizes the deep-eye budget is
    // not the component size, it is how many states sit in cells of size > 1 at each ladder
    // level. Counted here in C by hashing each level's signature and sorting; emitting
    // 23.6M JSONL records and grouping them elsewhere is not a viable route.
    if(want_collide){
        uint64_t *sig=malloc((size_t)ncomp*8);
        if(!sig){ fprintf(stderr,"alloc sig\n"); return 1; }
        const char *LVL[4]={"scalar_total_length","boundary_histogram(RDSU)",
                            "labelled_14_channel","exponent_ledger"};
        printf("{\"schema\":\"harness-collision-pass-v1\",\"component\":%u,\"cap\":%d,\"levels\":[\n",ncomp,CAP);
        for(int lvl=0; lvl<4; lvl++){
            for(uint32_t i=0;i<ncomp;i++){
                St s=pool[i],r;
                uint64_t h=1469598103934665603ULL;
                if(lvl==0){ h=(uint64_t)tot(&s); }
                else if(lvl==1){
                    int D=0,S=0,U=0;
                    for(int m=0;m<14;m++){ if(!apply_nocap(&s,m,&r)) continue;
                        int d=tot(&r)-tot(&s); if(d<0)D++; else if(d==0)S++; else U++; }
                    h=((uint64_t)D<<40)^((uint64_t)S<<20)^(uint64_t)U;
                } else if(lvl==2){
                    for(int m=0;m<14;m++){ if(!apply_nocap(&s,m,&r)) continue;
                        int d=tot(&r)-tot(&s);
                        uint64_t c = d<0?1: d==0?2:3;
                        h^=c; h*=1099511628211ULL; }
                } else {
                    int e0x,e0y,e1x,e1y;
                    expsum(s.a0,s.b0,s.l0,&e0x,&e0y); expsum(s.a1,s.b1,s.l1,&e1x,&e1y);
                    h^=(uint64_t)(e0x+1000); h*=1099511628211ULL;
                    h^=(uint64_t)(e0y+1000); h*=1099511628211ULL;
                    h^=(uint64_t)(e1x+1000); h*=1099511628211ULL;
                    h^=(uint64_t)(e1y+1000); h*=1099511628211ULL;
                }
                sig[i]=h;
            }
            // sort to count classes and cell sizes. qsort, not a shell sort: the gap
            // sequence n/2,n/4,... is O(n^2) in the worst case and this array is 23.6M.
            qsort(sig,ncomp,sizeof(uint64_t),cmp_u64);
            uint64_t classes=0, in_cells=0, biggest=0;
            for(uint64_t i=0;i<ncomp;){
                uint64_t j=i; while(j<ncomp && sig[j]==sig[i]) j++;
                uint64_t n=j-i; classes++;
                if(n>1) in_cells+=n;
                if(n>biggest) biggest=n;
                i=j;
            }
            printf("  {\"level\":\"%s\",\"classes\":%llu,\"states_in_collision_cells\":%llu,"
                   "\"pct_needing_escalation\":%.2f,\"largest_cell\":%llu}%s\n",
                   LVL[lvl],(unsigned long long)classes,(unsigned long long)in_cells,
                   100.0*in_cells/ncomp,(unsigned long long)biggest, lvl<3?",":"");
            fflush(stdout);
        }
        printf("]}\n");
        free(sig);
        return 0;
    }

    // Census. For interior states the code is D/S/U by length delta. For boundary
    // children it is R when the child's move re-enters the component -- the same rule
    // the Python harness applies in boundary_record().
    char t0[MAXW+2],t1[MAXW+2];
    if(!want_boundary){
        for(uint32_t i=0;i<ncomp;i++){
            St s=pool[i],r; char code[15]; int d[14];
            for(int m=0;m<14;m++){
                if(!apply_nocap(&s,m,&r)){ code[m]='?'; d[m]=0; continue; }
                d[m]=tot(&r)-tot(&s);
                code[m]= d[m]<0?'D': d[m]==0?'S':'U';
            }
            code[14]=0;
            wtext(s.a0,s.b0,s.l0,t0); wtext(s.a1,s.b1,s.l1,t1);
            int e0x,e0y,e1x,e1y;
            expsum(s.a0,s.b0,s.l0,&e0x,&e0y); expsum(s.a1,s.b1,s.l1,&e1x,&e1y);
            printf("{\"state\":[\"%s\",\"%s\"],\"total_length\":%d,\"lengths\":[%d,%d],"
                   "\"imbalance\":%d,\"M\":[[%d,%d],[%d,%d]],\"detM\":%d,"
                   "\"outcome_by_move\":\"%s\",\"delta_total_by_move\":[",
                   t0,t1,tot(&s),s.l0,s.l1,abs(s.l0-s.l1),e0x,e0y,e1x,e1y,
                   e0x*e1y-e0y*e1x,code);
            for(int m=0;m<14;m++) printf("%s%d",m?",":"",d[m]);
            printf("]}\n");
        }
    } else {
        // distinct boundary children, then their labelled channel against the component
        uint32_t base=nst;
        for(uint32_t i=0;i<ncomp;i++){
            St s=pool[i],r;
            for(int m=0;m<14;m++){
                if(!apply_nocap(&s,m,&r)) continue;
                if(tot(&r)<=CAP) continue;
                intern(&r,&isnew);
            }
        }
        fprintf(stderr,"boundary_children=%u\n",nst-base);
        for(uint32_t i=base;i<nst;i++){
            St s=pool[i],r; char code[15]; int d[14];
            for(int m=0;m<14;m++){
                if(!apply_nocap(&s,m,&r)){ code[m]='?'; d[m]=0; continue; }
                d[m]=tot(&r)-tot(&s);
                uint32_t f=find(&r);
                if(f!=0xFFFFFFFFu && f<ncomp) code[m]='R';
                else code[m]= d[m]<0?'D': d[m]==0?'S':'U';
            }
            code[14]=0;
            wtext(s.a0,s.b0,s.l0,t0); wtext(s.a1,s.b1,s.l1,t1);
            int e0x,e0y,e1x,e1y;
            expsum(s.a0,s.b0,s.l0,&e0x,&e0y); expsum(s.a1,s.b1,s.l1,&e1x,&e1y);
            printf("{\"state\":[\"%s\",\"%s\"],\"total_length\":%d,\"lengths\":[%d,%d],"
                   "\"imbalance\":%d,\"M\":[[%d,%d],[%d,%d]],\"detM\":%d,"
                   "\"boundary_outcome_by_move\":\"%s\",\"delta_total_by_move\":[",
                   t0,t1,tot(&s),s.l0,s.l1,abs(s.l0-s.l1),e0x,e0y,e1x,e1y,
                   e0x*e1y-e0y*e1x,code);
            for(int m=0;m<14;m++) printf("%s%d",m?",":"",d[m]);
            printf("]}\n");
        }
    }
    return 0;
}
