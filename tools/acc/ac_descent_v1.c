// DEEP STOCHASTIC DESCENT for Andrews-Curtis -- a different algorithm, not another BFS.
//
// Every engine in this repo so far enumerates a length-capped ball breadth-first. That is
// structurally incapable of reaching a 200-move solution: the frontier explodes long before
// the depth does. But the records we are trying to beat on solved k=1 rows are 60-595 moves
// long, so the path we need IS deep.
//
// This goes deep and narrow instead. From the start presentation it walks the move graph,
// choosing moves that reduce total relator length, accepting an increase with a temperature-
// controlled probability so it can climb out of local minima. No cap on depth, no state
// table, O(1) memory. Many independent restarts. It is incomplete -- it can miss a path that
// exists -- but unlike BFS it can FIND a long one.
//
// Records every improving trajectory in full so a hit is replayable move for move.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#define MAXW 512
typedef struct { uint8_t a[MAXW],b[MAXW]; int la,lb; } St;

static uint64_t rng_s;
static inline uint64_t rnd(void){ rng_s^=rng_s<<13; rng_s^=rng_s>>7; rng_s^=rng_s<<17; return rng_s; }
static inline double rnd01(void){ return (double)(rnd()>>11)/9007199254740992.0; }

static int reduce(const uint8_t*in,int n,uint8_t*out){
    int t=0;
    for(int i=0;i<n;i++){ uint8_t c=in[i];
        if(t>0&&out[t-1]==(c^1)) t--; else out[t++]=c; }
    return t;
}
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
int main(int argc,char**argv){
    // usage: seed restarts steps target_len la a... lb b...
    if(argc<6){ printf("usage: seed restarts steps beat_len la a.. lb b..\n"); return 2; }
    rng_s=strtoull(argv[1],0,10); if(!rng_s) rng_s=88172645463325252ULL;
    long restarts=atol(argv[2]); long steps=atol(argv[3]); int beat=atoi(argv[4]);
    St s0; memset(&s0,0,sizeof s0);
    int p=5; s0.la=atoi(argv[p++]);
    for(int i=0;i<s0.la;i++) s0.a[i]=(uint8_t)atoi(argv[p++]);
    s0.lb=atoi(argv[p++]);
    for(int i=0;i<s0.lb;i++) s0.b[i]=(uint8_t)atoi(argv[p++]);

    static uint8_t path[4000000]; int best_len=1<<30;
    for(long r=0;r<restarts;r++){
        St cur=s0; int n=0;
        double T=2.0+3.0*rnd01();
        for(long st=0;st<steps;st++){
            if(solved(&cur)){
                if(n<best_len){
                    best_len=n;
                    printf("HIT len=%d beat=%d restart=%ld\nMOVES",n,beat,r);
                    for(int k=0;k<n;k++) printf(" %d",path[k]);
                    printf("\n"); fflush(stdout);
                    if(n<beat) return 0;   // already better than the record: stop
                }
                break;
            }
            // pick a move: prefer cost-reducing, accept increases by temperature
            int order[14]; for(int i=0;i<14;i++) order[i]=i;
            for(int i=13;i>0;i--){ int j=rnd()%(i+1); int t=order[i];order[i]=order[j];order[j]=t; }
            int c0=cost(&cur); int taken=-1; St nx;
            for(int i=0;i<14;i++){
                St cand; if(!apply(&cur,order[i],&cand)) continue;
                int d=cost(&cand)-c0;
                if(d<0 || rnd01()<exp(-(double)d/T)){ nx=cand; taken=order[i]; break; }
            }
            if(taken<0) break;
            cur=nx; if(n<4000000) path[n++]=(uint8_t)taken;
            T*=0.9999; if(T<0.35) T=0.35;
        }
    }
    if(best_len==(1<<30)) printf("NOHIT\n");
    return 1;
}
