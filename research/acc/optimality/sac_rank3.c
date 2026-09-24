// Exact Stable AC (sac-r8-v1) meet restricted to rank <= MAXR, mirroring stable_core.py.
// Forward BFS from the start (radius A), backward BFS from the empty presentation (radius B)
// using exact predecessors (the graph is directed at stabilize/destabilize). The minimum
// dS+dT over the intersection is the exact rank<=MAXR distance whenever it is <= A+B.
// usage: sac_rank3 MAXR A B l0 w.. l1 w..      (letters: official ints ±1, ±2)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#ifndef MW
#define MW 200
#endif
#ifndef MR
#define MR 8
#endif
static long OVERFLOW=0;
typedef struct { int k; int l[MR]; int8_t w[MR][MW]; } S;
typedef struct { int cat,i,j,inv,c; } Row; // cat: 0 inv,1 mult,2 conj,3 stab,4 destab
static Row T[257]; static int MAXR;
static void build(void){ int id=0;
  // 0..13 ac-r2-v1
  T[id++]=(Row){0,0,0,0,0}; T[id++]=(Row){0,1,0,0,0};
  T[id++]=(Row){1,0,1,0,0}; T[id++]=(Row){1,0,1,1,0}; T[id++]=(Row){1,1,0,0,0}; T[id++]=(Row){1,1,0,1,0};
  int G[4]={1,-1,2,-2}; for(int i=0;i<2;i++) for(int g=0;g<4;g++) T[id++]=(Row){2,i,0,0,G[g]};
  T[id++]=(Row){3,0,0,0,0};
  for(int i=0;i<8;i++) T[id++]=(Row){4,i,0,0,0};
  for(int i=2;i<8;i++) T[id++]=(Row){0,i,0,0,0};
  for(int i=0;i<8;i++) for(int j=0;j<8;j++){ if(j==i||(i<2&&j<2)) continue; T[id++]=(Row){1,i,j,0,0}; T[id++]=(Row){1,i,j,1,0}; }
  for(int i=0;i<8;i++) for(int g=1;g<=8;g++){ if(i<2&&g<=2) continue; T[id++]=(Row){2,i,0,0,g}; T[id++]=(Row){2,i,0,0,-g}; }
  if(id!=257){ fprintf(stderr,"table %d\n",id); exit(2);} }
static int red(int8_t*o,int n,int8_t c){ if(n>0&&o[n-1]==-c) return n-1; o[n]=c; return n+1; }
// apply move m; return 0 if not applicable (or rank would exceed MAXR)
static int apply(const S*s,int m,S*r){ Row R=T[m]; int k=s->k;
  if(R.cat==3){ if(k>=MAXR) return 0; *r=*s; r->k=k+1; r->l[k]=1; r->w[k][0]=(int8_t)(k+1); return 1; }
  int i=R.i; if(i>=k) return 0;
  if(R.cat==4){ if(s->l[i]!=1||s->w[i][0]<=0) return 0; int g=s->w[i][0];
    for(int j=0;j<k;j++) if(j!=i) for(int t=0;t<s->l[j];t++) if(s->w[j][t]==g||s->w[j][t]==-g) return 0;
    r->k=k-1; int q=0; for(int j=0;j<k;j++){ if(j==i) continue; r->l[q]=s->l[j];
      for(int t=0;t<s->l[j];t++){ int a=s->w[j][t]; r->w[q][t]=(int8_t)(a>g?a-1:(a<-g?a+1:a)); } q++; } return 1; }
  *r=*s;
  if(R.cat==0){ int L=s->l[i]; for(int t=0;t<L;t++) r->w[i][t]=(int8_t)-s->w[i][L-1-t]; return 1; }
  if(R.cat==1){ int j=R.j; if(j>=k) return 0; int n=0; int8_t o[2*MW];
    for(int t=0;t<s->l[i];t++) n=red(o,n,s->w[i][t]);
    if(!R.inv) for(int t=0;t<s->l[j];t++) n=red(o,n,s->w[j][t]); else for(int t=s->l[j]-1;t>=0;t--) n=red(o,n,(int8_t)-s->w[j][t]);
    if(n>MW-2){ OVERFLOW++; return 0; } memcpy(r->w[i],o,n); r->l[i]=n; return 1; }
  int c=R.c; if(abs(c)>k) return 0; int n=0; int8_t o[MW+4]; n=red(o,n,(int8_t)c);
  for(int t=0;t<s->l[i];t++) n=red(o,n,s->w[i][t]); n=red(o,n,(int8_t)-c);
  if(n>MW-2){ OVERFLOW++; return 0; } memcpy(r->w[i],o,n); r->l[i]=n; return 1; }
static int inv_of(int m){ Row R=T[m]; if(R.cat==0) return m; if(R.cat==1) return R.inv?m-1:m+1; if(R.cat==2) return (R.c>0)?m+1:m-1; return -1; }
static int seq(const S*a,const S*b){ if(a->k!=b->k) return 0; for(int j=0;j<a->k;j++){ if(a->l[j]!=b->l[j]||memcmp(a->w[j],b->w[j],a->l[j])) return 0; } return 1; }
// predecessors: all (p,m) with apply(p,m)==t
typedef void (*pcb)(const S*,int,void*);
static void preds(const S*t,pcb f,void*u){ S p,chk; int k=t->k;
  for(int m=0;m<257;m++){ Row R=T[m];
    if(R.cat<=2){ int mi=inv_of(m); if(apply(t,mi,&p)&&apply(&p,m,&chk)&&seq(&chk,t)) f(&p,m,u); }
    else if(R.cat==3){ if(k>=1&&t->l[k-1]==1&&t->w[k-1][0]==k){ int ok=1; for(int j=0;j<k-1;j++) for(int x=0;x<t->l[j];x++) if(abs(t->w[j][x])==k) ok=0;
        if(ok){ p=*t; p.k=k-1; f(&p,m,u); } } }
    else { int i=R.i; if(i>k||k+1>MAXR) continue;
      for(int g=1;g<=k+1;g++){ p.k=k+1; int q=0;
        for(int j=0;j<k+1;j++){ if(j==i){ p.l[j]=1; p.w[j][0]=(int8_t)g; continue; }
          p.l[j]=t->l[q]; for(int x=0;x<t->l[q];x++){ int a=t->w[q][x]; p.w[j][x]=(int8_t)(a>=g?a+1:(a<=-g?a-1:a)); } q++; }
        if(apply(&p,m,&chk)&&seq(&chk,t)) f(&p,m,u); } } } }
// fingerprint table
static inline uint64_t mix(uint64_t x){ x^=x>>30; x*=0xbf58476d1ce4e5b9ULL; x^=x>>27; x*=0x94d049bb133111ebULL; x^=x>>31; return x; }
static void fp(const S*s,uint64_t*a,uint64_t*b){ uint64_t h1=0x9E37+s->k, h2=0x7F4A7C15ULL*(s->k+3);
  for(int j=0;j<s->k;j++){ h1=mix(h1^(0x100u+s->l[j])); h2=mix(h2+0x51ULL*(s->l[j]+7));
    for(int x=0;x<s->l[j];x++){ h1=mix(h1^(uint64_t)(uint8_t)s->w[j][x]); h2=mix(h2*0x100000001B3ULL+(uint8_t)s->w[j][x]+x); } }
  *a=h1|1; *b=h2&~0xFULL; }
typedef struct { uint64_t*t; uint64_t N,n; } Tb;
static void tinit(Tb*T,uint64_t N){ T->N=N; T->n=0; T->t=calloc(2*N,8); if(!T->t){ fprintf(stderr,"oom\n"); exit(3);} }
static int tfind(const Tb*T,uint64_t a,uint64_t b){ uint64_t i=(uint64_t)(((unsigned __int128)a*T->N)>>64);
  for(;;){ if(!T->t[2*i]) return -1; if(T->t[2*i]==a&&(T->t[2*i+1]&~0xFULL)==b) return (int)(T->t[2*i+1]&0xF); if(++i==T->N) i=0; } }
static int tins(Tb*T,uint64_t a,uint64_t b,int d){ if(T->n*10>=T->N*8){ fprintf(stderr,"table full\n"); exit(4);} uint64_t i=(uint64_t)(((unsigned __int128)a*T->N)>>64);
  for(;;){ if(!T->t[2*i]){ T->t[2*i]=a; T->t[2*i+1]=b|(uint64_t)d; T->n++; return 1; } if(T->t[2*i]==a&&(T->t[2*i+1]&~0xFULL)==b) return 0; if(++i==T->N) i=0; } }
// layered state storage: variable-length byte arena (no per-state word cap)
typedef struct { uint8_t*b; uint64_t n,cap,cnt; } Vec;
static void push(Vec*V,const S*s){ uint64_t need=2; for(int j=0;j<s->k;j++) need+=2+s->l[j];
  if(V->n+need>V->cap){ V->cap=V->cap?V->cap*2:(1<<20); while(V->n+need>V->cap) V->cap*=2; V->b=realloc(V->b,V->cap); if(!V->b){fprintf(stderr,"oom\n");exit(3);} }
  uint8_t*p=V->b+V->n; *p++=(uint8_t)s->k; for(int j=0;j<s->k;j++){ *p++=(uint8_t)(s->l[j]&255); *p++=(uint8_t)(s->l[j]>>8); memcpy(p,s->w[j],s->l[j]); p+=s->l[j]; }
  V->n=p-V->b; V->cnt++; }
static uint64_t get(const Vec*V,uint64_t off,S*s){ const uint8_t*p=V->b+off; s->k=*p++; for(int j=0;j<s->k;j++){ s->l[j]=p[0]|(p[1]<<8); p+=2; memcpy(s->w[j],p,s->l[j]); p+=s->l[j]; } return p-V->b; }
static Tb FT,BT; static Vec FL[16],BL[16]; static int curd;
static int BMAX; static void addB(const S*p,int m,void*u){ (void)m;(void)u; uint64_t a,b; fp(p,&a,&b); if(tins(&BT,a,b,curd)&&curd<BMAX) push(&BL[curd],p); }
static int stepwalk_found; static S walkS; static int walkm;
static void findpredF(const S*p,int m,void*u){ int want=*(int*)u; uint64_t a,b; if(stepwalk_found) return; fp(p,&a,&b); if(tfind(&FT,a,b)==want){ stepwalk_found=1; walkS=*p; walkm=m; } }
int main(int argc,char**argv){ build();
  if(!strcmp(argv[1],"apply")){ MAXR=8; int m; S t,r; while(scanf("%d %d",&m,&t.k)==2){ for(int j=0;j<t.k;j++){ if(scanf("%d",&t.l[j])!=1) return 1; for(int x=0;x<t.l[j];x++){ int v; if(scanf("%d",&v)!=1) return 1; t.w[j][x]=(int8_t)v; } }
      if(!apply(&t,m,&r)){ printf("NA\n"); continue; } printf("%d",r.k); for(int j=0;j<r.k;j++){ printf(" %d",r.l[j]); for(int x=0;x<r.l[j];x++) printf(" %d",r.w[j][x]); } printf("\n"); } return 0; }
  MAXR=atoi(argv[1]); int A=atoi(argv[2]),B=atoi(argv[3]); BMAX=B;
  uint64_t NS=getenv("NSLOTS")?strtoull(getenv("NSLOTS"),0,10):(1ULL<<26); tinit(&BT,NS); uint64_t a,b; S r;
  S e; e.k=0; fp(&e,&a,&b); tins(&BT,a,b,0); push(&BL[0],&e);
  for(curd=1;curd<=B;curd++){ { static S cur; for(uint64_t off=0;off<BL[curd-1].n;) { off=get(&BL[curd-1],off,&cur); preds(&cur,addB,NULL); } }
    fprintf(stderr,"B layer %d: total %llu\n",curd,(unsigned long long)BT.n); }
  char tag[64];
  while(scanf("%63s",tag)==1){ S s0; s0.k=2; for(int j=0;j<2;j++){ if(scanf("%d",&s0.l[j])!=1) return 1; for(int x=0;x<s0.l[j];x++){ int v; if(scanf("%d",&v)!=1) return 1; s0.w[j][x]=(int8_t)v; } }
    OVERFLOW=0; tinit(&FT,NS); for(int d=0;d<16;d++){ FL[d].n=0; FL[d].cnt=0; }
    fp(&s0,&a,&b); tins(&FT,a,b,0); push(&FL[0],&s0); int best=99; S bestS; int bdS=0,bdT=0; uint64_t streamed=0;
    { int dt=tfind(&BT,a,b); if(dt>=0){ best=dt; bestS=s0; bdS=0; bdT=dt; } }
    static S cur; for(int d=1;d<=A;d++){ for(uint64_t off=0;off<FL[d-1].n;){ off=get(&FL[d-1],off,&cur); for(int m=0;m<257;m++){ if(!apply(&cur,m,&r)) continue; fp(&r,&a,&b);
          if(d<A){ if(tins(&FT,a,b,d)){ push(&FL[d],&r); int dt=tfind(&BT,a,b); if(dt>=0&&d+dt<best){ best=d+dt; bestS=r; bdS=d; bdT=dt; } } }
          else { if(tfind(&FT,a,b)>=0) continue; streamed++; int dt=tfind(&BT,a,b); if(dt>=0&&d+dt<best){ best=d+dt; bestS=r; bdS=d; bdT=dt; } } } } }
    printf("%s F_stored=%llu streamed=%llu",tag,(unsigned long long)FT.n,(unsigned long long)streamed);
    if(OVERFLOW) printf(" WARNING_CAP_HIT=%ld(not_exact)",OVERFLOW);
    if(best==99){ printf(" NO_MEET rank<=%d dist>%d\n",MAXR,A+B); fflush(stdout); free(FT.t); continue; }
    int path[64],L=0,rev[32],mr=2; S c=bestS; int bad=0;
    for(int k=bdS;k>0;k--){ int want=k-1; stepwalk_found=0; preds(&c,findpredF,&want); if(!stepwalk_found){ bad=1; break; } rev[k-1]=walkm; c=walkS; if(c.k>mr) mr=c.k; }
    for(int k=0;k<bdS&&!bad;k++) path[L++]=rev[k];
    c=bestS; if(bestS.k>mr) mr=bestS.k;
    for(int k=bdT;k>0&&!bad;k--){ int ok=0; for(int m=0;m<257&&!ok;m++){ if(!apply(&c,m,&r)) continue; fp(&r,&a,&b); int dd=tfind(&BT,a,b);
          if(dd==k-1){ path[L++]=m; c=r; ok=1; if(c.k>mr) mr=c.k; } } if(!ok) bad=1; }
    if(bad) printf(" MEET dist=%d REBUILD_FAIL\n",best);
    else { printf(" MEET rank<=%d dist=%d maxrank_on_path=%d path",MAXR,best,mr); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); }
    fflush(stdout); free(FT.t); }
  return 0; }
