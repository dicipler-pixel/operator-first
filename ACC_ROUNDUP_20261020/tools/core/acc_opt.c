// ACC exact-optimality meet engine, ac-r2-v1
// (SAIR Andrews-Curtis commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e,
//  competition/tools/verifier/core.py, 14 moves). NO LENGTH CAP.
//
// Letters: 0=x 1=x^-1 2=y 3=y^-1 (inverse = c^1). Official ints: 1,-1,2,-2.
// States are stored as a 128-bit fingerprint (two independent 64-bit hashes
// of the exact ordered word pair) in an open-addressing table; the low 4
// bits of the second hash hold the BFS distance (so 123 fingerprint bits).
// Positive results are replayed exactly by the official verifier.
//
// Modes:
//   apply                       stdin "m l0 l1 w..." -> stdout "l0 l1 w..."
//   tball R NSLOTS OUT WORKDIR  build T_R around (x,y), write table to OUT
//   meet TFILE B A NSLOTS_S WORKDIR TAG l0 w.. l1 w..
//        load T_B (B = radius), BFS the start to S_(A-1) (stored), stream
//        layer A (stored too when STORE_LAST=1 in env), report the minimum
//        dS+dT over S_A ∩ T_B, and rebuild + print the path when it exists.
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define MAXW 8192
typedef struct { int l[2]; uint8_t w[2][MAXW]; } St;
static const uint8_t INV[14]={0,1,3,2,5,4,7,6,9,8,11,10,13,12};

static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec; }
static void die(const char*m){ fprintf(stderr,"FATAL %s\n",m); printf("FATAL %s\n",m); exit(3); }

// ---- kernel: mirrors core.apply_move exactly ----
static int push_red(uint8_t*o,int n,uint8_t c){ if(n>0&&o[n-1]==(c^1)) return n-1; o[n]=c; return n+1; }
static void apply(const St*s,int m,St*r){
    int j,k,n=0; const uint8_t*a;
    if(m==0||m==1){ j=m; r->l[1-j]=s->l[1-j]; memcpy(r->w[1-j],s->w[1-j],s->l[1-j]);
        int L=s->l[j]; for(int i=0;i<L;i++) r->w[j][i]=s->w[j][L-1-i]^1; r->l[j]=L; return; }
    if(m<=5){ j=(m<=3)?0:1; k=1-j; int inv=(m==3||m==5);
        r->l[k]=s->l[k]; memcpy(r->w[k],s->w[k],s->l[k]);
        uint8_t*o=r->w[j]; a=s->w[j]; for(int i=0;i<s->l[j];i++) n=push_red(o,n,a[i]);
        const uint8_t*b=s->w[k]; int lb=s->l[k];
        if(!inv) for(int i=0;i<lb;i++) n=push_red(o,n,b[i]);
        else for(int i=lb-1;i>=0;i--) n=push_red(o,n,b[i]^1);
        if(n>MAXW-4) die("MAXW"); r->l[j]=n; return; }
    j=(m<=9)?0:1; k=1-j; uint8_t g=(uint8_t)((m-6)&3); // GENS=(1,-1,2,-2) -> 0,1,2,3
    r->l[k]=s->l[k]; memcpy(r->w[k],s->w[k],s->l[k]);
    uint8_t*o=r->w[j]; a=s->w[j]; n=push_red(o,0,g);
    for(int i=0;i<s->l[j];i++) n=push_red(o,n,a[i]);
    n=push_red(o,n,g^1); if(n>MAXW-4) die("MAXW"); r->l[j]=n;
}
static int st_eq(const St*a,const St*b){ return a->l[0]==b->l[0]&&a->l[1]==b->l[1]&&
    !memcmp(a->w[0],b->w[0],a->l[0])&&!memcmp(a->w[1],b->w[1],a->l[1]); }

// ---- 128-bit fingerprint: two independent 64-bit hashes of the exact pair ----
static inline uint64_t fmix_a(uint64_t x){ x^=x>>30; x*=0xbf58476d1ce4e5b9ULL; x^=x>>27; x*=0x94d049bb133111ebULL; x^=x>>31; return x; }
static inline uint64_t fmix_b(uint64_t x){ x^=x>>33; x*=0xff51afd7ed558ccdULL; x^=x>>33; x*=0xc4ceb9fe1a85ec53ULL; x^=x>>33; return x; }
static inline uint64_t rotl(uint64_t x,int r){ return (x<<r)|(x>>(64-r)); }
static void fp(const St*s,uint64_t*h1o,uint64_t*h2o){
    uint64_t h1=0x243F6A8885A308D3ULL^((uint64_t)s->l[0]*0x9E3779B97F4A7C15ULL)^((uint64_t)s->l[1]<<40);
    uint64_t h2=0x13198A2E03707344ULL+((uint64_t)s->l[1]*0xC2B2AE3D27D4EB4FULL)+((uint64_t)s->l[0]<<44);
    uint64_t idx=0;
    for(int j=0;j<2;j++){ const uint8_t*w=s->w[j]; int L=s->l[j];
        for(int i=0;i<L;i+=32){ uint64_t c=0; int e=(L-i<32)?L-i:32;
            for(int t=0;t<e;t++) c|=(uint64_t)w[i+t]<<(2*t);
            idx++;
            h1=fmix_a(h1^c^(idx*0xD6E8FEB86659FD93ULL));
            h2=rotl(h2^fmix_b(c*0x9FB21C651E98DF25ULL+idx),29)*0x87C37B91114253D5ULL+0x52DCE729ULL; } }
    h1=fmix_a(h1^0xA0761D6478BD642FULL); h2=fmix_b(h2^idx);
    *h1o=h1|1ULL; *h2o=h2&~0xFULL;
}

// ---- table (any slot count; home slot = mulhi(h1, nslots)) ----
typedef struct { uint64_t*t; uint64_t N,n; } Tab;
static void tab_init(Tab*T,uint64_t N){ T->N=N; T->n=0;
    size_t sz=(size_t)16*N; T->t=mmap(0,sz,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    if(T->t==MAP_FAILED) die("mmap table");
    madvise(T->t,sz,MADV_HUGEPAGE); }
static inline uint64_t slot0(const Tab*T,uint64_t h1){ return (uint64_t)(((unsigned __int128)h1*T->N)>>64); }
static int tab_find(const Tab*T,uint64_t h1,uint64_t h2){
    uint64_t i=slot0(T,h1);
    for(;;){ uint64_t a=T->t[2*i]; if(!a) return -1;
        if(a==h1&&(T->t[2*i+1]&~0xFULL)==h2) return (int)(T->t[2*i+1]&0xF);
        if(++i==T->N) i=0; } }
static int tab_ins_raw(Tab*T,uint64_t h1,uint64_t h2,int d){ // returns existing dist, or -1 if inserted
    uint64_t i=slot0(T,h1);
    for(;;){ uint64_t a=T->t[2*i];
        if(!a){ T->t[2*i]=h1; T->t[2*i+1]=h2|(uint64_t)d; T->n++; return -1; }
        if(a==h1&&(T->t[2*i+1]&~0xFULL)==h2) return (int)(T->t[2*i+1]&0xF);
        if(++i==T->N) i=0; } }
static void tab_grow(Tab*T){ Tab G; tab_init(&G,T->N*2);
    for(uint64_t i=0;i<T->N;i++) if(T->t[2*i]) tab_ins_raw(&G,T->t[2*i],T->t[2*i+1]&~0xFULL,(int)(T->t[2*i+1]&0xF));
    munmap(T->t,(size_t)16*T->N); *T=G;
    fprintf(stderr,"  grew table to %llu slots\n",(unsigned long long)T->N); }
// grow=1: double at load 0.80; grow=0: fixed size, refuse above load 0.90
static int tab_ins(Tab*T,uint64_t h1,uint64_t h2,int d,int grow){
    if(grow){ if(T->n*5>=T->N*4) tab_grow(T); }
    else if(T->n*10>=T->N*9) die("fixed table above load 0.90");
    return tab_ins_raw(T,h1,h2,d); }

// ---- layer files ----
static void wr_state(FILE*f,const St*s){ uint16_t h[2]={(uint16_t)s->l[0],(uint16_t)s->l[1]};
    fwrite(h,2,2,f); fwrite(s->w[0],1,s->l[0],f); fwrite(s->w[1],1,s->l[1],f); }
static int rd_state(FILE*f,St*s){ uint16_t h[2]; if(fread(h,2,2,f)!=2) return 0;
    s->l[0]=h[0]; s->l[1]=h[1];
    if(fread(s->w[0],1,h[0],f)!=h[0]||fread(s->w[1],1,h[1],f)!=h[1]) die("short read"); return 1; }
static FILE*openf(const char*dir,const char*tag,int d,const char*mode){ char p[4096];
    snprintf(p,sizeof p,"%s/%s_layer%02d.bin",dir,tag,d); FILE*f=fopen(p,mode); if(!f) die(p);
    setvbuf(f,NULL,_IOFBF,1<<24); return f; }
static void rmf(const char*dir,const char*tag,int d){ char p[4096]; snprintf(p,sizeof p,"%s/%s_layer%02d.bin",dir,tag,d); unlink(p); }

static St cur,nx,tmp;

// ---- BFS: layers 0..D stored in table T; layer files kept for D-1 (and D if keepD) ----
// cb called on each new state (layer d) — used by meet to look up T.
typedef void (*newcb)(const St*,int);
static uint64_t layer_cnt[64];
static void bfs(Tab*T,const St*s0,int D,const char*dir,const char*tag,int grow,int write_last,newcb cb){
    uint64_t h1,h2; fp(s0,&h1,&h2); tab_ins(T,h1,h2,0,grow); layer_cnt[0]=1; if(cb) cb(s0,0);
    FILE*o=openf(dir,tag,0,"wb"); wr_state(o,s0); fclose(o);
    for(int d=1;d<=D;d++){ double t0=now();
        FILE*in=openf(dir,tag,d-1,"rb"); FILE*out=(d<D||write_last)?openf(dir,tag,d,"wb"):NULL;
        uint64_t c=0;
        while(rd_state(in,&cur)) for(int m=0;m<14;m++){ apply(&cur,m,&nx); fp(&nx,&h1,&h2);
            if(tab_ins(T,h1,h2,d,grow)<0){ c++; if(out) wr_state(out,&nx); if(cb) cb(&nx,d); } }
        fclose(in); if(out) fclose(out); if(d>=2) rmf(dir,tag,d-2);
        layer_cnt[d]=c; fprintf(stderr,"  %s layer %d: +%llu  total %llu  (%.1fs)\n",tag,d,(unsigned long long)c,(unsigned long long)T->n,now()-t0);
    }
}

// ---- meet ----
static Tab TT,SS; static int gB,gA; static int best=99; static St bestSt; static int bestdS,bestdT;
static uint64_t meets=0;
static void on_new(const St*s,int d){ uint64_t h1,h2; fp(s,&h1,&h2); int dt=tab_find(&TT,h1,h2);
    if(dt>=0){ meets++; if(d+dt<best){ best=d+dt; bestSt=*s; bestdS=d; bestdT=dt; } } }

static int rebuild(const St*start,int*path){
    static St c,n; uint64_t h1,h2; int L=0, rev[64];
    c=bestSt; for(int k=bestdS;k>0;k--){ int ok=0;
        for(int m=0;m<14;m++){ apply(&c,m,&n); fp(&n,&h1,&h2); if(tab_find(&SS,h1,h2)==k-1){ rev[bestdS-k]=INV[m]; c=n; ok=1; break; } }
        if(!ok) return -1; }
    if(!st_eq(&c,start)) return -2;
    for(int i=bestdS-1;i>=0;i--) path[L++]=rev[i];
    c=bestSt; for(int k=bestdT;k>0;k--){ int ok=0;
        for(int m=0;m<14;m++){ apply(&c,m,&n); fp(&n,&h1,&h2); if(tab_find(&TT,h1,h2)==k-1){ path[L++]=m; c=n; ok=1; break; } }
        if(!ok) return -3; }
    if(!(c.l[0]==1&&c.l[1]==1&&c.w[0][0]==0&&c.w[1][0]==2)) return -4;
    return L;
}

static int parse_state(char**argv,int ai,St*s){
    for(int j=0;j<2;j++){ s->l[j]=atoi(argv[ai++]); for(int i=0;i<s->l[j];i++) s->w[j][i]=(uint8_t)atoi(argv[ai++]); }
    return ai; }

#ifndef ACC_NO_MAIN
int main(int argc,char**argv){
    if(argc<2) die("usage");
    if(!strcmp(argv[1],"apply")){ int m; St s,r;
        while(scanf("%d %d %d",&m,&s.l[0],&s.l[1])==3){
            for(int j=0;j<2;j++) for(int i=0;i<s.l[j];i++){ int x; if(scanf("%d",&x)!=1) die("in"); s.w[j][i]=(uint8_t)x; }
            apply(&s,m,&r); printf("%d %d",r.l[0],r.l[1]);
            for(int j=0;j<2;j++) for(int i=0;i<r.l[j];i++) printf(" %d",r.w[j][i]); printf("\n"); }
        return 0; }
    if(!strcmp(argv[1],"tball")){ int R=atoi(argv[2]); uint64_t NS=strtoull(argv[3],0,10); const char*out=argv[4],*dir=argv[5];
        double t0=now(); Tab T; tab_init(&T,NS); St g; g.l[0]=1;g.l[1]=1;g.w[0][0]=0;g.w[1][0]=2;
        bfs(&T,&g,R,dir,"T",0,0,NULL); rmf(dir,"T",R-1);
        uint64_t cum=0; for(int d=0;d<=R;d++){ cum+=layer_cnt[d]; printf("T r%d layer %llu cumulative %llu\n",d,(unsigned long long)layer_cnt[d],(unsigned long long)cum); }
        FILE*f=fopen(out,"wb"); if(!f) die("out"); if(fwrite(T.t,16,T.N,f)!=T.N) die("write T"); fclose(f);
        printf("TBALL R=%d states=%llu slots=%llu wall=%.1fs\n",R,(unsigned long long)T.n,(unsigned long long)T.N,now()-t0); return 0; }
    if(!strcmp(argv[1],"meet")){ const char*tf=argv[2]; gB=atoi(argv[3]); gA=atoi(argv[4]); uint64_t NS=strtoull(argv[5],0,10);
        const char*dir=argv[6],*tag=argv[7]; St s0; parse_state(argv,8,&s0);
        int store_last=getenv("STORE_LAST")?atoi(getenv("STORE_LAST")):1;
        double t0=now();
        struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
        uint64_t slots=stt.st_size/16;
        TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); if(TT.t==MAP_FAILED) die("mmap T");
        TT.N=slots; TT.n=0;
        fprintf(stderr,"[%s] T loaded %llu slots (%.1fs)\n",tag,(unsigned long long)slots,now()-t0);
        tab_init(&SS,NS); best=99; meets=0;
        int D=store_last?gA:gA-1;
        bfs(&SS,&s0,D,dir,tag,1,!store_last,on_new);
        uint64_t streamed=0;
        if(!store_last){ // stream layer A from layer A-1, not stored
            FILE*in=openf(dir,tag,gA-1,"rb"); uint64_t h1,h2;
            while(rd_state(in,&cur)) for(int m=0;m<14;m++){ apply(&cur,m,&nx); fp(&nx,&h1,&h2);
                if(tab_find(&SS,h1,h2)>=0) continue; streamed++;
                int dt=tab_find(&TT,h1,h2); if(dt>=0){ meets++; if(gA+dt<best){ best=gA+dt; bestSt=nx; bestdS=gA; bestdT=dt; } } }
            fclose(in); }
        rmf(dir,tag,gA-1); rmf(dir,tag,gA);
        uint64_t cum=0; for(int d=0;d<=D;d++){ cum+=layer_cnt[d]; printf("[%s] S layer %d: %llu  cumulative %llu\n",tag,d,(unsigned long long)layer_cnt[d],(unsigned long long)cum); }
        if(!store_last) printf("[%s] S layer %d streamed (edges into new states, not deduplicated): %llu\n",tag,gA,(unsigned long long)streamed);
        printf("[%s] SA_STORED=%llu A=%d B=%d LMAX=%d MEETS=%llu\n",tag,(unsigned long long)cum,gA,gB,gA+gB,(unsigned long long)meets);
        if(best<99){ int path[128]; int L=rebuild(&s0,path);
            printf("[%s] RESULT MEET exact_distance=%d dS=%d dT=%d rebuild=%d\n",tag,best,bestdS,bestdT,L);
            if(L>0){ printf("[%s] PATH",tag); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); } }
        else printf("[%s] RESULT NO_MEET no path of length <= %d\n",tag,gA+gB);
        printf("[%s] WALL %.1fs\n",tag,now()-t0); return 0; }
    die("mode");
}
#endif
