// Corridor BFS for Andrews-Curtis (ac-r2-v1), 64-letter relators.
// Two uint64 per relator, 2 bits per letter. Search tool only: every
// certificate is re-verified by the official Python verifier.
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
static St*pool; static uint32_t*par; static uint8_t*pmv; static uint32_t*tab;
static St*ball; static uint32_t*btab; static uint64_t bmask; static uint32_t bn;
static uint64_t mask; static uint32_t nst;
static uint32_t intern(const St*s,uint32_t p,uint8_t mv,int*isnew){
    uint64_t i=hsh(s)&mask;
    for(;;){ uint32_t e=tab[i];
        if(e==0xFFFFFFFFu){ pool[nst]=*s; par[nst]=p; pmv[nst]=mv; tab[i]=nst; *isnew=1; return nst++; }
        if(eq(&pool[e],s)){ *isnew=0; return e; }
        i=(i+1)&mask; }
}
static int in_ball(const St*s){
    if(!bn) return 0;
    uint64_t i=hsh(s)&bmask;
    for(;;){ uint32_t e=btab[i];
        if(e==0xFFFFFFFFu) return 0;
        if(eq(&ball[e],s)) return 1;
        i=(i+1)&bmask; }
}
static void load_ball(const char*path){
    FILE*f=fopen(path,"rb"); if(!f){ bn=0; return; }
    uint64_t n; if(fread(&n,8,1,f)!=1){ fclose(f); bn=0; return; }
    ball=malloc(n*sizeof(St)); uint64_t c=1; while(c<n*2) c<<=1; bmask=c-1;
    btab=malloc(c*4); memset(btab,0xFF,c*4);
    for(uint64_t k=0;k<n;k++){
        uint64_t a0,b0,a1,b1; uint8_t l0,l1;
        if(fread(&a0,8,1,f)!=1) break; if(fread(&b0,8,1,f)!=1) break;
        if(fread(&a1,8,1,f)!=1) break; if(fread(&b1,8,1,f)!=1) break;
        if(fread(&l0,1,1,f)!=1) break; if(fread(&l1,1,1,f)!=1) break;
        St t; memset(&t,0,sizeof t); t.a0=a0;t.b0=b0;t.a1=a1;t.b1=b1;t.l0=l0;t.l1=l1;
        ball[bn]=t; uint64_t i=hsh(&t)&bmask;
        while(btab[i]!=0xFFFFFFFFu) i=(i+1)&bmask;
        btab[i]=bn++;
    }
    fclose(f);
    fprintf(stderr,"ball loaded: %u states\n",bn);
}
int main(int argc,char**argv){
    CAP=atoi(argv[1]); uint64_t maxst=strtoull(argv[2],0,10);
    if(CAP>MAXW){ printf("CAP_TOO_LARGE %d\n",CAP); return 4; }
    int l0=atoi(argv[3]); uint8_t a[MAXW],b[MAXW];
    for(int i=0;i<l0;i++) a[i]=atoi(argv[4+i]);
    int l1=atoi(argv[4+l0]);
    for(int i=0;i<l1;i++) b[i]=atoi(argv[5+l0+i]);
    uint64_t c2=1; while(c2<maxst*2) c2<<=1; mask=c2-1;
    pool=malloc(maxst*sizeof(St)); par=malloc(maxst*4); pmv=malloc(maxst); tab=malloc(c2*4);
    if(!pool||!par||!pmv||!tab){ printf("ALLOC_FAIL\n"); return 1; }
    memset(tab,0xFF,c2*4);
    { const char*bp=getenv("AC_BALL"); if(bp) load_ball(bp); }
    St s0; memset(&s0,0,sizeof s0);
    packw(a,l0,&s0.a0,&s0.b0); s0.l0=l0; packw(b,l1,&s0.a1,&s0.b1); s0.l1=l1;
    St tgt; memset(&tgt,0,sizeof tgt);
    { uint8_t x[1]={0},y[1]={2}; packw(x,1,&tgt.a0,&tgt.b0); tgt.l0=1; packw(y,1,&tgt.a1,&tgt.b1); tgt.l1=1; }
    int isnew; intern(&s0,0xFFFFFFFFu,255,&isnew);
    uint32_t head=0,depth=0,lvlend=nst;
    while(head<nst){
        uint32_t si=head++; St cur=pool[si],r;
        for(int m=0;m<14;m++){
            if(!apply(&cur,m,&r)) continue;
            uint32_t id=intern(&r,si,(uint8_t)m,&isnew);
            if(isnew&&(eq(&r,&tgt)||in_ball(&r))){
                printf("%s ", eq(&r,&tgt)?"FOUND":"BALLHIT"); uint32_t c=id; int n=0; static uint8_t mv[200000];
                while(par[c]!=0xFFFFFFFFu){ mv[n++]=pmv[c]; c=par[c]; }
                for(int i=n-1;i>=0;i--) printf("%d ",mv[i]);
                printf("\n"); fflush(stdout); return 0;
            }
            if(nst>=maxst-2){ printf("BUDGET states=%u depth=%u\n",nst,depth); return 2; }
        }
        if(head==lvlend){ depth++; lvlend=nst; fprintf(stderr,"depth %u states %u\n",depth,nst); }
    }
    printf("EXHAUSTED states=%u depth=%u cap=%d\n",nst,depth,CAP);
    return 3;
}
