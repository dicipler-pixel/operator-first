// Supermove (substitution) beam search in conjugacy-class space, after ACSolverX (MIT, Math & AI Lab at Caltech, 6a12515).
// State: two cyclically reduced words, each canonical up to rotation and inversion; the pair is unordered.
// Move: replace x by cred(rot(x) * rot(y^s)) with a cancellation at the junction (x,y ordered either way, s = +-1).
// Beam: keep the W children with the smallest total length (fingerprint tie-break, optional noise), dedupe globally.
// Output: the class road (one line per state, letters as ints) to the first total-length-2 state.
// usage: smbeam W DMAX LCAP SEED l0 w.. l1 w..   (letters 1,-1,2,-2)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MW 96
typedef struct { int8_t a[MW], b[MW]; uint8_t la, lb; } St;
typedef struct { St s; int32_t par; uint32_t key; } Node;
static int cred(int8_t*w,int n){ int8_t t[4*MW]; int m=0; for(int i=0;i<n;i++){ if(m&&t[m-1]==-w[i]) m--; else t[m++]=w[i]; }
  int lo=0,hi=m; while(hi-lo>1&&t[lo]==-t[hi-1]){ lo++; hi--; } int L=hi-lo; if(L>MW) return -1; memcpy(w,t+lo,L); return L; }
static void canon(int8_t*w,int n){ if(n==0) return; int8_t best[MW],cand[MW],iv[MW]; memcpy(best,w,n);
  for(int i=0;i<n;i++) iv[i]=-w[n-1-i];
  for(int pass=0;pass<2;pass++){ int8_t*src=pass?iv:w; for(int r=0;r<n;r++){ for(int i=0;i<n;i++) cand[i]=src[(i+r)%n];
    if(memcmp(cand,best,n)<0) memcpy(best,cand,n); } } memcpy(w,best,n); }
static int cmpw(const int8_t*a,int la,const int8_t*b,int lb){ if(la!=lb) return la<lb?-1:1; return memcmp(a,b,la); }
static void norm(St*s){ canon(s->a,s->la); canon(s->b,s->lb); if(cmpw(s->a,s->la,s->b,s->lb)>0){ St t=*s; memcpy(s->a,t.b,t.lb); s->la=t.lb; memcpy(s->b,t.a,t.la); s->lb=t.la; } }
static uint64_t hs(const St*s){ uint64_t h=1469598103934665603ULL; h^=s->la; h*=1099511628211ULL; for(int i=0;i<s->la;i++){ h^=(uint8_t)s->a[i]; h*=1099511628211ULL; }
  h^=0xFF; h*=1099511628211ULL; for(int i=0;i<s->lb;i++){ h^=(uint8_t)s->b[i]; h*=1099511628211ULL; } h^=h>>29; return h?h:1; }
static uint64_t*HT; static uint64_t HN;
static int seen(uint64_t h){ uint64_t i=h&(HN-1); while(HT[i]){ if(HT[i]==h) return 1; i=(i+1)&(HN-1); } HT[i]=h; return 0; }
static Node*POOL; static size_t PN=0,PC=0;
static int32_t addnode(const St*s,int32_t par,uint32_t key){ if(PN==PC){ PC=PC?PC*2:1<<20; POOL=realloc(POOL,PC*sizeof(Node)); if(!POOL){fprintf(stderr,"oom\n");exit(2);} }
  POOL[PN].s=*s; POOL[PN].par=par; POOL[PN].key=key; return (int32_t)PN++; }
static int cmpk(const void*x,const void*y){ uint32_t a=POOL[*(const int32_t*)x].key,b=POOL[*(const int32_t*)y].key; return a<b?-1:a>b; }
static void emit(int32_t id){ int32_t st[4096]; int n=0; while(id>=0&&n<4096){ st[n++]=id; id=POOL[id].par; }
  printf("ROAD %d\n",n); for(int i=n-1;i>=0;i--){ St*s=&POOL[st[i]].s; for(int j=0;j<s->la;j++) printf("%d ",s->a[j]); printf("|"); for(int j=0;j<s->lb;j++) printf(" %d",s->b[j]); printf("\n"); } fflush(stdout); }
int main(int argc,char**argv){
  if(argc<6){ fprintf(stderr,"usage\n"); return 1; }
  int W=atoi(argv[1]),DMAX=atoi(argv[2]),LCAP=atoi(argv[3]); unsigned seed=(unsigned)atoi(argv[4]); int ai=5;
  St s0; s0.la=atoi(argv[ai++]); for(int i=0;i<s0.la;i++) s0.a[i]=atoi(argv[ai++]); s0.lb=atoi(argv[ai++]); for(int i=0;i<s0.lb;i++) s0.b[i]=atoi(argv[ai++]);
  s0.la=cred(s0.a,s0.la); s0.lb=cred(s0.b,s0.lb); norm(&s0);
  HN=1ULL<<26; HT=calloc(HN,8); seen(hs(&s0));
  int32_t*beam=malloc(sizeof(int32_t)*1); int bn=1; beam[0]=addnode(&s0,-1,0);
  int32_t*cand=NULL; size_t cc=0,cn=0;
  for(int d=1;d<=DMAX;d++){ cn=0;
    for(int bi=0;bi<bn;bi++){ St cur=POOL[beam[bi]].s;
      for(int ord=0;ord<2;ord++){ const int8_t*x=ord?cur.b:cur.a; int nx=ord?cur.lb:cur.la; const int8_t*y=ord?cur.a:cur.b; int ny=ord?cur.la:cur.lb;
        if(nx==0||ny==0) continue;
        for(int sg=0;sg<2;sg++){ int8_t ys[MW]; for(int i=0;i<ny;i++) ys[i]=sg? -y[ny-1-i] : y[i];
          for(int i=0;i<nx;i++){ int8_t last=x[(i+nx-1)%nx];
            for(int j=0;j<ny;j++){ if(ys[j]!=-last) continue;
              int8_t w[4*MW]; int n=0; for(int t=0;t<nx;t++) w[n++]=x[(i+t)%nx]; for(int t=0;t<ny;t++) w[n++]=ys[(j+t)%ny];
              int L=cred(w,n); if(L<=0||L+ny>LCAP) continue;
              St c; memcpy(c.a,w,L); c.la=L; memcpy(c.b,y,ny); c.lb=ny; norm(&c);
              uint64_t h=hs(&c); if(seen(h)) continue;
              uint32_t noise=seed? (uint32_t)((h^((uint64_t)seed*0x9E3779B97F4A7C15ULL))>>61):0;
              uint32_t key=((uint32_t)(c.la+c.lb+noise)<<20)|(uint32_t)(h&0xFFFFF);
              int32_t id=addnode(&c,beam[bi],key);
              if(c.la+c.lb==2){ printf("FOUND depth %d nodes %zu\n",d,PN); emit(id); return 0; }
              if(cn==cc){ cc=cc?cc*2:1<<20; cand=realloc(cand,cc*sizeof(int32_t)); } cand[cn++]=id; } } } } }
    if(cn==0){ printf("DEAD depth %d\n",d); return 0; }
    qsort(cand,cn,sizeof(int32_t),cmpk); bn=cn<(size_t)W?(int)cn:W; beam=realloc(beam,sizeof(int32_t)*bn); memcpy(beam,cand,sizeof(int32_t)*bn);
    if(d%5==0) fprintf(stderr,"d=%d cand=%zu best=%d pool=%zu\n",d,cn,POOL[beam[0]].s.la+POOL[beam[0]].s.lb,PN);
    if(PN>(size_t)60000000){ printf("POOLCAP depth %d\n",d); return 0; } }
  printf("NONE\n"); return 0; }
