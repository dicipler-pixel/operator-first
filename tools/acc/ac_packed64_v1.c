// PACKED-64 corridor enumerator — breaks the memory wall, not the time wall.
//
// The cap-21 run died at 120M states in 6.9 GB. The binding constraint was never CPU
// (23.6M states censused in 121 s) but bytes per state:
//
//     ac_shared_ball_v1:  St 40B + parent 4B + move 1B + table ~8B  =  ~53 B/state
//
// At cap C a state has at most C letters. Two bits per letter plus 5+5 bits for the two
// relator lengths is 2C+10 bits, so for C <= 27 THE ENTIRE STATE FITS IN ONE uint64:
//
//     [ l0 : 5 ][ l1 : 5 ][ letters : 2 bits each, l0 then l1 ]
//
// Storage becomes an ordered array of uint64 (which doubles as the BFS queue) plus an
// open-addressing table of uint32 indices at load factor 0.5:
//
//     8 B (state) + 8 B (table, amortised)  =  16 B/state      ~3.3x more reach
//
// 500M states in 8 GB, against 120M before.
//
// WHAT IS GIVEN UP: parent pointers. This engine answers "is the component closed, and
// does it meet the target set" — it cannot reconstruct a path. That is the right trade
// for a CLOSED verdict, which is a statement about non-existence. On a MEET it prints the
// meeting state so a narrower run with parents can rebuild the path exactly.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXLET 27
static int CAP;

// ---- packing -------------------------------------------------------------
// letters: 0=x 1=x^-1 2=y 3=y^-1, inverse = XOR 1
static inline uint64_t pack(const uint8_t*a,int la,const uint8_t*b,int lb){
    uint64_t v = ((uint64_t)la) | (((uint64_t)lb)<<5);
    int sh=10;
    for(int i=0;i<la;i++){ v |= ((uint64_t)(a[i]&3))<<sh; sh+=2; }
    for(int i=0;i<lb;i++){ v |= ((uint64_t)(b[i]&3))<<sh; sh+=2; }
    return v;
}
static inline void unpack(uint64_t v,uint8_t*a,int*la,uint8_t*b,int*lb){
    *la=(int)(v&31); *lb=(int)((v>>5)&31);
    int sh=10;
    for(int i=0;i<*la;i++){ a[i]=(uint8_t)((v>>sh)&3); sh+=2; }
    for(int i=0;i<*lb;i++){ b[i]=(uint8_t)((v>>sh)&3); sh+=2; }
}
static inline int tot64(uint64_t v){ return (int)(v&31) + (int)((v>>5)&31); }

static inline int reduce(const uint8_t*in,int n,uint8_t*out){
    int t=0; for(int i=0;i<n;i++){ uint8_t c=in[i];
        if(t>0&&out[t-1]==(c^1)) t--; else out[t++]=c; } return t;
}
static inline int invword(const uint8_t*a,int n,uint8_t*o){
    for(int i=0;i<n;i++) o[i]=a[n-1-i]^1; return n;
}
// Same move grammar as the official verifier: 0/1 invert, 2-5 multiply, 6-13 conjugate.
// Returns 0 if the child exceeds the cap.
static int apply64(uint64_t s,int m,uint64_t*out){
    uint8_t a[MAXLET+4],b[MAXLET+4],t[2*MAXLET+8],u[2*MAXLET+8];
    int la,lb; unpack(s,a,&la,b,&lb);
    int lt,lu;
    if(m==0){ lu=invword(a,la,u); if(lu+lb>CAP) return 0; *out=pack(u,lu,b,lb); return 1; }
    if(m==1){ lu=invword(b,lb,u); if(la+lu>CAP) return 0; *out=pack(a,la,u,lu); return 1; }
    if(m==2||m==3){
        memcpy(t,a,la); lt=la;
        if(m==2){ memcpy(t+lt,b,lb); lt+=lb; } else { lt+=invword(b,lb,t+lt); }
        lu=reduce(t,lt,u); if(lu+lb>CAP||lu>MAXLET) return 0;
        *out=pack(u,lu,b,lb); return 1;
    }
    if(m==4||m==5){
        memcpy(t,b,lb); lt=lb;
        if(m==4){ memcpy(t+lt,a,la); lt+=la; } else { lt+=invword(a,la,t+lt); }
        lu=reduce(t,lt,u); if(lu+la>CAP||lu>MAXLET) return 0;
        *out=pack(a,la,u,lu); return 1;
    }
    int on0=(m<=9); int k=on0?m-6:m-10; uint8_t g=(uint8_t)k, gi=g^1;
    const uint8_t*src=on0?a:b; int ls=on0?la:lb; int other=on0?lb:la;
    t[0]=g; memcpy(t+1,src,ls); t[ls+1]=gi;
    lu=reduce(t,ls+2,u); if(lu+other>CAP||lu>MAXLET) return 0;
    if(on0) *out=pack(u,lu,b,lb); else *out=pack(a,la,u,lu);
    return 1;
}
static inline uint64_t mix(uint64_t h){
    h^=h>>33; h*=0xFF51AFD7ED558CCDULL; h^=h>>33; h*=0xC4CEB9FE1A85EC53ULL; h^=h>>33;
    return h;
}
static uint64_t *S;          // states, in BFS order; doubles as the queue
static uint32_t *T;          // open-addressing table of indices into S
static uint64_t TMASK;
static uint64_t N=0, NMAX;
static int insert(uint64_t v){          // 1 if newly added
    uint64_t i=mix(v)&TMASK;
    for(;;){
        uint32_t e=T[i];
        if(e==0xFFFFFFFFu){ if(N>=NMAX) return -1; S[N]=v; T[i]=(uint32_t)N; N++; return 1; }
        if(S[e]==v) return 0;
        i=(i+1)&TMASK;
    }
}
static int contains(uint64_t v){
    uint64_t i=mix(v)&TMASK;
    for(;;){ uint32_t e=T[i];
        if(e==0xFFFFFFFFu) return 0;
        if(S[e]==v) return 1;
        i=(i+1)&TMASK; }
}
static int parse(const char*s,uint8_t*w){
    int n=0; for(const char*p=s;*p;p++){
        if(*p=='1'&&n==0&&p[1]==0) break;
        switch(*p){ case 'x': w[n++]=0;break; case 'X': w[n++]=1;break;
                    case 'y': w[n++]=2;break; case 'Y': w[n++]=3;break;
                    default: return -1; } }
    uint8_t o[MAXLET+4]; int r=reduce(w,n,o); memcpy(w,o,r); return r;
}
int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,"usage: packed64 cap maxstates r0 r1\n"); return 2; }
    CAP=atoi(argv[1]);
    if(CAP>MAXLET){ printf("CAP_TOO_LARGE %d (packing holds %d)\n",CAP,MAXLET); return 4; }
    NMAX=strtoull(argv[2],0,10);
    int notriv = getenv("NOTRIV") && atoi(getenv("NOTRIV"));
    uint8_t a[MAXLET+4],b[MAXLET+4];
    int la=parse(argv[3],a), lb=parse(argv[4],b);
    if(la<0||lb<0){ fprintf(stderr,"bad word\n"); return 2; }
    if(la+lb>CAP){ printf("START_ABOVE_CAP %d cap=%d\n",la+lb,CAP); return 6; }

    uint64_t slots=1; while(slots < NMAX*2) slots<<=1;
    TMASK=slots-1;
    S=malloc(NMAX*8); T=malloc(slots*4);
    if(!S||!T){ printf("ALLOC_FAIL need %.1f GB\n",(NMAX*8.0+slots*4.0)/1e9); return 1; }
    memset(T,0xFF,slots*4);
    fprintf(stderr,"budget %llu states, %.2f GB (%.1f B/state)\n",
            (unsigned long long)NMAX,(NMAX*8.0+slots*4.0)/1e9,(NMAX*8.0+slots*4.0)/NMAX);

    insert(pack(a,la,b,lb));
    // target (x,y) = ordered; there is no swap move, so (y,x) is NOT the target
    uint8_t tx[1]={0}, ty[1]={2};
    uint64_t TARGET=pack(tx,1,ty,1);

    uint64_t head=0, lvl_end=1, depth=0;
    while(head<N){
        uint64_t v=S[head++], c;
        for(int m=0;m<14;m++){
            if(!apply64(v,m,&c)) continue;
            // Building the trivial component T_K means enumerating the component OF the
            // target, so the early exit must be suppressed there or the run aborts at
            // depth 0. NOTRIV=1 disables it; the closure report still states whether the
            // target is present, which is the fact that matters.
            if(!notriv && c==TARGET){ printf("MEET_TARGET at state %llu depth~%llu states=%llu\n",
                                  (unsigned long long)head,(unsigned long long)depth,
                                  (unsigned long long)N); return 0; }
            int r=insert(c);
            if(r<0){ printf("BUDGET states=%llu depth=%llu cap=%d\n",
                            (unsigned long long)N,(unsigned long long)depth,CAP); return 3; }
        }
        if(head==lvl_end){ depth++; lvl_end=N;
            if((depth&15)==0) fprintf(stderr,"  depth %llu states %llu\n",
                                      (unsigned long long)depth,(unsigned long long)N); }
    }
    printf("CLOSED component=%llu depth=%llu cap=%d target_in_component=%d\n",
           (unsigned long long)N,(unsigned long long)depth,CAP,contains(TARGET));
    return 0;
}
