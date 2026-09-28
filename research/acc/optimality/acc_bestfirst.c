// Cap-free best-first search, ac-r2-v1 (kernel, fingerprint and goal table shared verbatim with acc_opt.c).
// Priority f = 4*L + W4*d (L = total relator length of the state, d = moves from the start, W4 = 4*w), popped
// lowest first, LIFO inside a bucket. No length cap: growth is ranked, not forbidden (the "opposite" of acc_capped).
// Every generated state is looked up in the goal table T (distance <= R to (x,y)); the swapped state gives the
// (y,x) finish for Stable AC (+ [15,15]). A child is dropped when it cannot beat the best path found so far
// (not in T means >= R+1 more moves). States are not stored: nodes keep (parent, move, depth) and a state is
// rebuilt by replaying from the start. First visit wins (greedy; paths are upper bounds, not optimality proofs).
// BF_KEY=p2: rank by P2 (best total length after two multiplications, the beam's P2; conjugation and inversion
// children inherit it) instead of L. The P2 code is extracted verbatim from acc_beam.c at build time:
//   sed -n '/---- P2 begin ----/,/---- P2 end ----/p' acc_beam.c > p2_block.inc
// usage: acc_bestfirst TFILE R W4 BUDGET DMAX LMAX TAG l0 w.. l1 w..
#define ACC_NO_MAIN
#include "acc_opt.c"
#include <math.h>
#include "p2_block.inc"
static const uint8_t PI[14]={0,1,2,3,4,5,8,9,6,7,12,13,10,11};
static void swapst(const St*s,St*r){ r->l[0]=s->l[0]; r->l[1]=s->l[1]; for(int j=0;j<2;j++) for(int i=0;i<s->l[j];i++) r->w[j][i]=s->w[j][i]^2; }
typedef struct { uint32_t par; uint16_t p2; uint8_t mv, d; } Node;
static Node*ND; static uint64_t NN=0, NCAP;
typedef struct { uint32_t*a; uint32_t n, cap; } Bk;
static Bk*BK; static int NB=1<<16;
static void push(int f,uint32_t id){ if(f<0) f=0; if(f>=NB) f=NB-1; Bk*b=&BK[f];
  if(b->n==b->cap){ b->cap=b->cap?b->cap*2:256; b->a=realloc(b->a,4ull*b->cap); if(!b->a) die("bucket alloc"); } b->a[b->n++]=id; }
static St S0, cur, ch, sw;
static void bf_rebuild(uint32_t id,St*out,int*mv,int*dep){ int k=ND[id].d; *dep=k; uint32_t x=id;
  for(int i=k-1;i>=0;i--){ mv[i]=ND[x].mv; x=ND[x].par; } *out=S0; St t; for(int i=0;i<k;i++){ apply(out,mv[i],&t); *out=t; } }
int main(int argc,char**argv){
  if(argc<9) die("usage: acc_bestfirst TFILE R W4 BUDGET DMAX LMAX TAG l0 w.. l1 w..");
  const char*tf=argv[1]; int R=atoi(argv[2]), W4=atoi(argv[3]); uint64_t BUD=strtoull(argv[4],0,10);
  int DMAX=atoi(argv[5]), LMAX=atoi(argv[6]); const char*tag=argv[7]; parse_state(argv,8,&S0);
  struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
  TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); TT.N=stt.st_size/16;
  NCAP=BUD+16; ND=malloc(sizeof(Node)*NCAP); BK=calloc(NB,sizeof(Bk)); if(!ND||!BK) die("alloc");
  tab_init(&SS,1ULL<<24); uint64_t h1,h2; fp(&S0,&h1,&h2); tab_ins(&SS,h1,h2,1,1);
  int best=getenv("BF_BEST")?atoi(getenv("BF_BEST")):(1<<30), bestS=best+2; uint32_t bid=0, sid=0; int bt=0, st=0, haveA=0, haveS=0;
  { int t=tab_find(&TT,h1,h2); if(t>=0&&t<best){ best=t; bid=0; bt=t; haveA=1; } }
  int KP2=getenv("BF_KEY")&&!strcmp(getenv("BF_KEY"),"p2"); uint16_t p0=KP2?p2_of(&S0):0;
  ND[0]=(Node){0,p0,0,0}; NN=1; push(4*(KP2?p0:(S0.l[0]+S0.l[1])),0);
  int mv[256], dep; uint64_t pops=0; int fmin=0; double t0=now();
  while(NN<BUD){
    while(fmin<NB&&BK[fmin].n==0) fmin++; if(fmin>=NB) break;
    uint32_t id=BK[fmin].a[--BK[fmin].n]; pops++;
    int d=ND[id].d; if(d+1>=DMAX||d+1>=best) continue;
    bf_rebuild(id,&cur,mv,&dep);
    for(int m=0;m<14;m++){ apply(&cur,m,&ch); int L=ch.l[0]+ch.l[1]; if(L>LMAX) continue;
      fp(&ch,&h1,&h2); if(tab_ins(&SS,h1,h2,1,1)>=0) continue;
      int dc=d+1, t=tab_find(&TT,h1,h2);
      if(NN>=NCAP) break; uint16_t cp=0; if(KP2) cp=(m>=2&&m<=5)?p2_of(&ch):ND[id].p2;
      ND[NN]=(Node){id,cp,(uint8_t)m,(uint8_t)dc}; uint32_t nid=(uint32_t)NN++;
      if(t>=0&&dc+t<best){ best=dc+t; bid=nid; bt=t; haveA=1;
        fprintf(stderr,"[%s] AC %d (depth %d + %d) after %llu nodes, %.0fs\n",tag,best,dc,t,(unsigned long long)NN,now()-t0); }
      swapst(&ch,&sw); uint64_t g1,g2; fp(&sw,&g1,&g2); int u=tab_find(&TT,g1,g2);
      if(u>=0&&dc+u+2<bestS){ bestS=dc+u+2; sid=nid; st=u; haveS=1; }
      if(t<0&&dc+R+1>=best) continue;          // cannot improve: not in T means >= R+1 more moves
      push(4*(KP2?cp:L)+W4*dc,nid); }
    if((pops&0xFFFFF)==0) fprintf(stderr,"[%s] pops %llu nodes %llu fmin %d best %d\n",tag,(unsigned long long)pops,(unsigned long long)NN,fmin,best<(1<<30)?best:-1);
  }
  printf("[%s] W4=%d nodes=%llu pops=%llu %.0fs\n",tag,W4,(unsigned long long)NN,(unsigned long long)pops,now()-t0);
  for(int which=0;which<2;which++){ if(!(which?haveS:haveA)){ printf("[%s] %s NONE\n",tag,which?"SAC":"AC"); continue; }
    uint32_t id=which?sid:bid; int t=which?st:bt; St c; bf_rebuild(id,&c,mv,&dep);
    int path[1024],Lp=0; for(int k=0;k<dep;k++) path[Lp++]=mv[k];
    if(which){ St tmp; swapst(&c,&tmp); c=tmp; }
    for(int k=t;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&ch); fp(&ch,&h1,&h2); if(tab_find(&TT,h1,h2)==k-1){ path[Lp++]=which?PI[m]:m; c=ch; ok=1; break; } } if(!ok){ printf("REBUILD_FAIL\n"); return 5; } }
    if(which){ path[Lp++]=15; path[Lp++]=15; }
    printf("[%s] %s %d PATH",tag,which?"SAC":"AC",Lp); for(int i=0;i<Lp;i++) printf(" %d",path[i]); printf("\n"); }
  return 0; }
