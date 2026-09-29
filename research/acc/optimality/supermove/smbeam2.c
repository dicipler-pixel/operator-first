// Cost-aware supermove beam (after ACSolverX s_move, MIT, Math & AI Lab at Caltech, 6a12515).
// State: the ACTUAL relators r0, r1 (cyclically reduced, specific rotation) plus g = official ac-r2-v1 moves spent so far.
// Supermove on relator x (r0 or r1) with the other relator y, sign s: rotate x by i (min(i,nx-i) conjugations), rotate y
// by j (min(j,ny-j) conjugations), multiply x <- x*y^s (one move 2-5, junction must cancel), cyclically reduce x (one
// conjugation per cancelled end pair). Dedupe by conjugacy class (rotation+inversion, unordered pair), keeping lower g.
// Beam key = (total length)*LS + g*LG (+ seeded noise). After the first goal (total length 2), EXTRA more depths are
// searched for a cheaper goal. Output: BEST g, then the actual road (r0 | r1 per line).
// usage: smbeam2 W DMAX LCAP SEED LS LG EXTRA l0 w.. l1 w..   (letters 1,-1,2,-2)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MW 96
typedef struct { int8_t w[2][MW]; uint8_t l[2]; } St;
typedef struct { St s; int32_t par; uint16_t g; uint64_t key; } Node;
static int cred(int8_t*w,int n,int*lo_out){ int8_t t[4*MW]; int m=0; for(int i=0;i<n;i++){ if(m&&t[m-1]==-w[i]) m--; else t[m++]=w[i]; }
  int lo=0,hi=m; while(hi-lo>1&&t[lo]==-t[hi-1]){ lo++; hi--; } int L=hi-lo; if(L>MW) return -1; memcpy(w,t+lo,L); *lo_out=lo; return L; }
static void canon(const int8_t*w,int n,int8_t*best){ if(n==0) return; int8_t cand[MW],iv[MW]; memcpy(best,w,n);
  for(int i=0;i<n;i++) iv[i]=-w[n-1-i];
  for(int pass=0;pass<2;pass++){ const int8_t*src=pass?iv:w; for(int r=0;r<n;r++){ for(int i=0;i<n;i++) cand[i]=src[(i+r)%n];
    if(memcmp(cand,best,n)<0) memcpy(best,cand,n); } } }
static int cmpw(const int8_t*a,int la,const int8_t*b,int lb){ if(la!=lb) return la<lb?-1:1; return memcmp(a,b,la); }
static uint64_t hcls(const St*s){ int8_t c0[MW],c1[MW]; canon(s->w[0],s->l[0],c0); canon(s->w[1],s->l[1],c1);
  const int8_t*A=c0,*B=c1; int la=s->l[0],lb=s->l[1]; if(cmpw(A,la,B,lb)>0){ const int8_t*t=A;A=B;B=t; int u=la;la=lb;lb=u; }
  uint64_t h=1469598103934665603ULL; h^=la; h*=1099511628211ULL; for(int i=0;i<la;i++){ h^=(uint8_t)A[i]; h*=1099511628211ULL; }
  h^=0xFF; h*=1099511628211ULL; for(int i=0;i<lb;i++){ h^=(uint8_t)B[i]; h*=1099511628211ULL; } h^=h>>29; return h?h:1; }
static uint64_t*HK; static uint16_t*HG; static uint64_t HN;
// returns 1 if (h,g) should be skipped (class seen with g' <= g); else records g
static int seen(uint64_t h,uint16_t g){ uint64_t i=h&(HN-1); while(HK[i]){ if(HK[i]==h){ if(HG[i]<=g) return 1; HG[i]=g; return 0; } i=(i+1)&(HN-1); } HK[i]=h; HG[i]=g; return 0; }
static Node*POOL; static size_t PN=0,PC=0;
static int32_t addnode(const St*s,int32_t par,uint16_t g,uint64_t key){ if(PN==PC){ PC=PC?PC*2:1<<20; POOL=realloc(POOL,PC*sizeof(Node)); if(!POOL){fprintf(stderr,"oom\n");exit(2);} }
  POOL[PN].s=*s; POOL[PN].par=par; POOL[PN].g=g; POOL[PN].key=key; return (int32_t)PN++; }
static int cmpk(const void*x,const void*y){ uint64_t a=POOL[*(const int32_t*)x].key,b=POOL[*(const int32_t*)y].key; return a<b?-1:a>b; }
static void emit(int32_t id){ int32_t st[4096]; int n=0; while(id>=0&&n<4096){ st[n++]=id; id=POOL[id].par; }
  printf("ROAD %d\n",n); for(int i=n-1;i>=0;i--){ St*s=&POOL[st[i]].s; for(int j=0;j<s->l[0];j++) printf("%d ",s->w[0][j]); printf("|"); for(int j=0;j<s->l[1];j++) printf(" %d",s->w[1][j]); printf("\n"); } fflush(stdout); }
static int fin_cost(const St*s){ // (a,b) single letters -> (x,y): inversions if in order, else a swap (estimate 6)
  int a=s->w[0][0],b=s->w[1][0]; if(abs(a)==1&&abs(b)==2) return (a<0)+(b<0); return 6+(a<0)+(b<0); }
int main(int argc,char**argv){
  if(argc<9){ fprintf(stderr,"usage\n"); return 1; }
  int W=atoi(argv[1]),DMAX=atoi(argv[2]),LCAP=atoi(argv[3]); unsigned seed=(unsigned)atoi(argv[4]); int LS=atoi(argv[5]),LG=atoi(argv[6]),EXTRA=atoi(argv[7]); int ai=8;
  St s0; for(int r=0;r<2;r++){ s0.l[r]=atoi(argv[ai++]); for(int i=0;i<s0.l[r];i++) s0.w[r][i]=atoi(argv[ai++]); }
  uint16_t g0=0; for(int r=0;r<2;r++){ int lo; int L=cred(s0.w[r],s0.l[r],&lo); s0.l[r]=L; g0+=lo; }
  HN=1ULL<<25; HK=calloc(HN,8); HG=calloc(HN,2); seen(hcls(&s0),g0);
  int32_t*beam=malloc(sizeof(int32_t)); int bn=1; beam[0]=addnode(&s0,-1,g0,0);
  int32_t*cand=NULL; size_t cc=0,cn=0; int32_t best=-1; int bestc=1<<30, goal_d=-1;
  for(int d=1;d<=DMAX;d++){ cn=0;
    for(int bi=0;bi<bn;bi++){ St cur=POOL[beam[bi]].s; uint16_t g=POOL[beam[bi]].g;
      for(int xi=0;xi<2;xi++){ const int8_t*x=cur.w[xi]; int nx=cur.l[xi]; const int8_t*y=cur.w[1-xi]; int ny=cur.l[1-xi];
        if(nx==0||ny==0) continue;
        for(int sg=0;sg<2;sg++){ int8_t ys[MW]; for(int i=0;i<ny;i++) ys[i]=sg? -y[ny-1-i] : y[i];
          for(int i=0;i<nx;i++){ int8_t last=x[(i+nx-1)%nx]; int cx=i<nx-i?i:nx-i;
            for(int j=0;j<ny;j++){ if(ys[j]!=-last) continue; int cy=j<ny-j?j:ny-j;
              int8_t w[4*MW]; int n=0; for(int t=0;t<nx;t++) w[n++]=x[(i+t)%nx]; for(int t=0;t<ny;t++) w[n++]=ys[(j+t)%ny];
              int lo; int L=cred(w,n,&lo); if(L<=0||L+ny>LCAP) continue;
              St c; memcpy(c.w[xi],w,L); c.l[xi]=L;
              int r= sg? (ny-j)%ny : j; for(int t=0;t<ny;t++) c.w[1-xi][t]=y[(r+t)%ny]; c.l[1-xi]=ny;
              int gc=g+cx+cy+1+lo; if(gc>65000) continue;
              uint64_t h=hcls(&c); if(seen(h,(uint16_t)gc)) continue;
              uint64_t noise=seed? ((h^((uint64_t)seed*0x9E3779B97F4A7C15ULL))>>61):0;
              uint64_t key=(((uint64_t)(c.l[0]+c.l[1])*LS+(uint64_t)gc*LG+noise*LS)<<20)|(h&0xFFFFF);
              int32_t id=addnode(&c,beam[bi],(uint16_t)gc,key);
              if(c.l[0]+c.l[1]==2){ int tc=gc+fin_cost(&c); if(tc<bestc){ bestc=tc; best=id; if(goal_d<0) goal_d=d; } continue; }
              if(cn==cc){ cc=cc?cc*2:1<<20; cand=realloc(cand,cc*sizeof(int32_t)); } cand[cn++]=id; } } } } }
    if(best>=0&&d>=goal_d+EXTRA) break;
    if(cn==0) break;
    qsort(cand,cn,sizeof(int32_t),cmpk); bn=cn<(size_t)W?(int)cn:W; beam=realloc(beam,sizeof(int32_t)*bn); memcpy(beam,cand,sizeof(int32_t)*bn);
    if(PN>(size_t)40000000) break; }
  if(best<0){ printf("NONE\n"); return 0; }
  printf("FOUND depth %d cost %d\n",goal_d,bestc); emit(best); return 0; }
