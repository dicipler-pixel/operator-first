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

#include <math.h>

#define MAXW 512
typedef struct { uint8_t a[MAXW],b[MAXW]; int la,lb; } St;

static uint64_t rng_s;
static inline uint64_t rnd(void){ rng_s^=rng_s<<13; rng_s^=rng_s>>7; rng_s^=rng_s<<17; return rng_s; }
static inline double rnd01(void){ return (double)(rnd()>>11)/9007199254740992.0; }

/* reduce() comes from the packed core above -- the descent's identical
   copy is dropped rather than shadowed. */
static int invw(const uint8_t*a,int n,uint8_t*o){
    for(int i=0;i<n;i++) o[i]=a[n-1-i]^1; return n;
}
// apply move m; returns 0 if it would overflow the word buffer
static int apply(const St*s,int m,St*r){
    uint8_t t[2*MAXW+4], u[2*MAXW+4];
    *r=*s;
    if(m==0){ uint8_t u[MAXW]; int l=invw(s->a,s->la,u); memcpy(r->a,u,l); r->la=l; return 1; }
    if(m==1){ uint8_t u[MAXW]; int l=invw(s->b,s->lb,u); memcpy(r->b,u,l); r->lb=l; return 1; }
    if(m==2||m==3){
        int lt=s->la; if(lt>MAXW) return 0;
        memcpy(t,s->a,lt);
        if(m==2){ if(lt+s->lb>2*MAXW) return 0; memcpy(t+lt,s->b,s->lb); lt+=s->lb; }
        else    { if(lt+s->lb>2*MAXW) return 0; lt+=invw(s->b,s->lb,t+lt); }
        // BUFFER SAFETY: reduce() can emit up to lt bytes (<= 2*MAXW), so reducing
        // straight into r->a (MAXW bytes) overflows whenever the reduced word is longer
        // than MAXW -- the old length check ran AFTER the write. Reduce into the large
        // temporary, check, then copy. Reported by ChatGPT; it SIGBUSes on fresh targets.
        int l=reduce(t,lt,u); if(l>MAXW) return 0; memcpy(r->a,u,l); r->la=l; return 1;
    }
    if(m==4||m==5){
        int lt=s->lb; if(lt>MAXW) return 0;
        memcpy(t,s->b,lt);
        if(m==4){ if(lt+s->la>2*MAXW) return 0; memcpy(t+lt,s->a,s->la); lt+=s->la; }
        else    { if(lt+s->la>2*MAXW) return 0; lt+=invw(s->a,s->la,t+lt); }
        int l=reduce(t,lt,u); if(l>MAXW) return 0; memcpy(r->b,u,l); r->lb=l; return 1;
    }
    int on0=(m<=9); int g=on0?m-6:m-10; uint8_t gi=g^1;
    const uint8_t*src=on0?s->a:s->b; int ls=on0?s->la:s->lb;
    if(ls+2>2*MAXW) return 0;
    t[0]=(uint8_t)g; memcpy(t+1,src,ls); t[ls+1]=gi;
    uint8_t out[MAXW+4]; int l=reduce(t,ls+2,out); if(l>MAXW) return 0;
    if(on0){ memcpy(r->a,out,l); r->la=l; } else { memcpy(r->b,out,l); r->lb=l; }
    return 1;
}
static inline int tot(const St*s){ return s->la+s->lb; }
static int solved(const St*s){
    // ordered (x,y) ONLY. There is no swap move in 0-13, so (y,x) is NOT the target.
    return (s->la==1&&s->lb==1&&s->a[0]==0&&s->b[0]==2);
}
// cost: total length, with a bonus for having a bare generator in a slot
static int cost(const St*s){
    int c=tot(s);
    if(s->la==1) c-=2;
    if(s->lb==1) c-=2;
    return c;
}

// ---------------------------------------------------------------------------
// DESCENT INTO THE BALL.
//
// Stochastic descent alone has to land EXACTLY on (x,y) -- one state. But T_16
// is 129,247,304 states, every one of them provably AC-trivial. So widen the
// success test: a walk succeeds the moment it touches ANY member of the ball.
// That turns a needle into a haystack of 129 million needles, at the cost of
// one hash lookup per step on states short enough to be in range.
//
// A hit is a path m -> s with s in T_16. The remaining s -> (x,y) is recovered
// separately by the shared ball, which finds it at depth 0. Both halves are
// concatenated and replayed against the ORIGINAL relators before anything is
// called a certificate.
//
// Usage: descent_ball ballcap ballmax seed restarts steps pairs.txt
// ---------------------------------------------------------------------------
static uint8_t *D;                 // BFS depth of each ball state: its EXACT
                                   // distance to (x,y). S is in BFS order and the
                                   // build is level-synchronous, so this costs one
                                   // byte per state and nothing else.
static uint32_t find_idx(uint64_t v){
    uint64_t i=mix(v)&TMASK;
    for(;;){ uint32_t e=T[i];
        if(e==0xFFFFFFFFu) return 0xFFFFFFFFu;
        if(S[e]==v) return e;
        i=(i+1)&TMASK; }
}
static int in_ball(const St*s){
    if(s->la + s->lb > CAP) return 0;
    if(s->la > MAXLET || s->lb > MAXLET) return 0;
    return contains(pack(s->a, s->la, s->b, s->lb));
}

int main(int argc,char**argv){
    if(argc<7){ fprintf(stderr,"usage: descent_ball ballcap ballmax seed restarts steps pairs.txt\n"); return 2; }
    CAP=atoi(argv[1]);
    if(CAP>MAXLET){ printf("CAP_TOO_LARGE %d\n",CAP); return 4; }
    NMAX=strtoull(argv[2],0,10);
    rng_s=strtoull(argv[3],0,10); if(!rng_s) rng_s=88172645463325252ULL;
    long restarts=atol(argv[4]); long steps=atol(argv[5]);
    int floor2 = getenv("FLOOR2") && atoi(getenv("FLOOR2"));

    uint64_t slots=1; while(slots < NMAX*2) slots<<=1;
    TMASK=slots-1;
    S=malloc(NMAX*8); T=malloc(slots*4);
    if(!S||!T){ printf("ALLOC_FAIL need %.1f GB\n",(NMAX*8.0+slots*4.0)/1e9); return 1; }
    memset(T,0xFF,slots*4);
    fprintf(stderr,"ball budget %llu states, %.2f GB\n",
            (unsigned long long)NMAX,(NMAX*8.0+slots*4.0)/1e9);

    D=malloc(NMAX);
    if(!D){ printf("ALLOC_FAIL depth array\n"); return 1; }
    uint8_t tx[1]={0}, ty[1]={2};
    insert(pack(tx,1,ty,1)); D[0]=0;
    uint64_t head=0, lvl_end=1, depth=0; int closed=1;
    while(head<N){
        uint64_t v=S[head]; uint8_t dv=D[head]; head++;
        uint64_t c;
        for(int m=0;m<14;m++){
            if(!apply64(v,m,&c)) continue;
            int r=insert(c);
            if(r<0){ closed=0; head=N; break; }
            if(r==1) D[N-1] = (dv<255)? dv+1 : 255;
        }
        if(head==lvl_end){ depth++; lvl_end=N;
            if((depth&15)==0) fprintf(stderr,"  ball depth %llu states %llu\n",
                                      (unsigned long long)depth,(unsigned long long)N); }
    }
    if(!closed){ printf("BALL_BUDGET states=%llu cap=%d -- a NOHIT against a PARTIAL ball proves nothing\n",
                        (unsigned long long)N,CAP); }
    else printf("BALL_CLOSED cap=%d states=%llu depth=%llu\n",
                CAP,(unsigned long long)N,(unsigned long long)depth);
    fflush(stdout);

    FILE*f=fopen(argv[6],"r");
    if(!f){ printf("NO_PAIR_FILE\n"); return 5; }
    char id[64]; int l0,l1;
    static uint8_t path[1<<22];
    while(fscanf(f,"%63s %d",id,&l0)==2){
        St s0; memset(&s0,0,sizeof s0);
        s0.la=l0;
        for(int i=0;i<l0;i++){ int v; if(fscanf(f,"%d",&v)!=1){fclose(f);return 5;} s0.a[i]=(uint8_t)v; }
        if(fscanf(f,"%d",&l1)!=1){ fclose(f); return 5; }
        s0.lb=l1;
        for(int i=0;i<l1;i++){ int v; if(fscanf(f,"%d",&v)!=1){fclose(f);return 5;} s0.b[i]=(uint8_t)v; }

        int done=0;
        // A bare NOBALL says nothing about WHY. Track the shortest total length the
        // walk ever reached: if it never gets near CAP the descent is not failing to
        // find the ball, it is failing to get down to where the ball lives.
        int minlen = s0.la + s0.lb;
        for(long r=0; r<restarts && !done; r++){
            St cur=s0; long n=0;
            double temp = 0.6 + 2.4*rnd01();
            for(long t=0; t<steps; t++){
                if(in_ball(&cur)){
                    // PHASE 2: finish inside the ball.
                    // Every state reachable from here without exceeding CAP is still a
                    // ball member, hence still provably trivial, and the ball is connected
                    // at depth 101. So rather than hand the tail to a second engine with
                    // parent pointers (7 GB), just keep walking -- confined to CAP, biased
                    // hard toward shorter states -- until the walk lands exactly on (x,y).
                    // DMOVES then IS the whole path and no tail stage is needed.
                    // The ball BFS already computed every state's EXACT distance to
                    // (x,y). Walking randomly inside the ball took ~100k moves on the
                    // controls, which compression could not rescue. Instead step
                    // strictly downhill on that depth field: each move drops the
                    // distance by one, so the tail is a SHORTEST path and is at most
                    // the ball's depth (101 at cap 16).
                    uint32_t bi = find_idx(pack(cur.a,cur.la,cur.b,cur.lb));
                    while(bi!=0xFFFFFFFFu && D[bi]>0){
                        int moved=0;
                        for(int fm=0; fm<14; fm++){
                            St fx;
                            if(!apply(&cur,fm,&fx)) continue;
                            if(!fx.la || !fx.lb) continue;
                            if(fx.la+fx.lb > CAP) continue;
                            uint32_t fj = find_idx(pack(fx.a,fx.la,fx.b,fx.lb));
                            if(fj==0xFFFFFFFFu) continue;
                            if(D[fj] != D[bi]-1) continue;
                            cur=fx; bi=fj;
                            if(n < (long)sizeof(path)) path[n++]=(uint8_t)fm;
                            moved=1; break;
                        }
                        if(!moved) break;   // cannot happen in a closed ball; bail safely
                    }
                    if(cur.la==1 && cur.lb==1 && cur.a[0]==0 && cur.b[0]==2){
                        printf("%s SOLVED steps=%ld restart=%ld\nDMOVES",id,n,r);
                        for(long k=0;k<n;k++) printf(" %d",path[k]);
                        printf("\n"); fflush(stdout); done=1; break;
                    }
                    // reached the ball but not the target within the finish budget:
                    // still a real hit, the tail just has to come from elsewhere
                    printf("%s BALLHIT steps=%ld restart=%ld\nDMOVES",id,n,r);
                    for(long k=0;k<n;k++) printf(" %d",path[k]);
                    printf("\n"); fflush(stdout); done=1; break;
                }
                int m = rnd()%14;
                St nx;
                if(!apply(&cur,m,&nx)) continue;
                if(!nx.la || !nx.lb) continue;
                int d = (nx.la+nx.lb) - (cur.la+cur.lb);
                // FLOOR2. Judging a move by its IMMEDIATE length change is what
                // stalled this walk at minlen 18-21: on our own 19 certificates
                // 52.6% of the winning moves do not reduce length, so a downhill
                // rule refuses half of them outright. Measured against the moves
                // those certificates DECLINED (310 chosen vs 4,030 declined), the
                // quantity that separates a good uphill move from a bad one is the
                // best length reachable in TWO moves: chosen -1.215 vs declined
                // -0.370, and floor2 <= -3 carries a 4.4x lift over chance.
                // Move-space rotation, by contrast, scored BELOW chance and is not
                // used. Cost is 14 extra applications per candidate.
                if(floor2){
                    int f2 = 1<<20;
                    for(int m2=0;m2<14;m2++){
                        St xx;
                        if(!apply(&nx,m2,&xx)) continue;
                        if(!xx.la || !xx.lb) continue;
                        int t2 = xx.la+xx.lb;
                        if(t2<f2) f2=t2;
                    }
                    if(f2 < (1<<20)){
                        int d2 = f2 - (cur.la+cur.lb);
                        if(d2 < d) d = d2;
                    }
                }
                if(d<=0 || rnd01() < exp(-d/temp)){
                    cur=nx;
                    if(cur.la+cur.lb < minlen) minlen = cur.la+cur.lb;
                    if(n < (long)sizeof(path)) path[n++]=(uint8_t)m;
                }
            }
        }
        if(!done){ printf("%s NOBALL minlen=%d start=%d cap=%d\n",
                          id,minlen,s0.la+s0.lb,CAP); fflush(stdout); }
    }
    fclose(f);
    return 0;
}
