// Beam search + exact finish. Forward beam from the start keeps the W states of smallest total
// relator length per depth (ties broken by fingerprint), deduplicated across all depths. Every
// generated state is looked up in T_9 (distance to (x,y)) and, via the generator swap, in T_9
// again (distance to (y,x)). A hit at depth d with ball distance t gives an AC path d+t (to (x,y))
// or a Stable AC path d+t+2 (via (y,x)). Kernel/fingerprint/table shared with acc_opt.c.
// usage: acc_beam TFILE W DMAX l0 w.. l1 w..
#define ACC_NO_MAIN
#include "acc_opt.c"
#include <math.h>
typedef struct { uint64_t off; uint32_t par; uint8_t mv; uint32_t len; } Node;
static uint8_t*AR; static uint64_t ARn,ARcap;
static uint64_t store(const St*s){ uint64_t need=4+s->l[0]+s->l[1]; if(ARn+need>ARcap){ ARcap=ARcap?ARcap*2:(1ULL<<26); while(ARn+need>ARcap) ARcap*=2; AR=realloc(AR,ARcap); if(!AR) die("arena"); }
  uint8_t*p=AR+ARn; p[0]=s->l[0]&255; p[1]=s->l[0]>>8; p[2]=s->l[1]&255; p[3]=s->l[1]>>8; memcpy(p+4,s->w[0],s->l[0]); memcpy(p+4+s->l[0],s->w[1],s->l[1]); uint64_t o=ARn; ARn+=need; return o; }
static void load(uint64_t o,St*s){ uint8_t*p=AR+o; s->l[0]=p[0]|(p[1]<<8); s->l[1]=p[2]|(p[3]<<8); memcpy(s->w[0],p+4,s->l[0]); memcpy(s->w[1],p+4+s->l[0],s->l[1]); }
static void swapst(const St*s,St*r){ r->l[0]=s->l[0]; r->l[1]=s->l[1]; for(int j=0;j<2;j++) for(int i=0;i<s->l[j];i++) r->w[j][i]=s->w[j][i]^2; } // x<->y: 0<->2, 1<->3
static const uint8_t PI[14]={0,1,2,3,4,5,8,9,6,7,12,13,10,11};
typedef struct { uint64_t key; uint32_t idx; } Cand;
// BEAM_H=1: ACSolverX tuned priority (Avi161/ACSolverX HEURISTICS.md), scaled x16:
// L + 2.53*K + 6.418*MK + 8.458*S + 3.292*|#x-#y|/L. K = sum over relators of cyclic generator-block
// count (0 for a pure power), MK = max of the two, S = mean block length of the thinner generator.
static double BAL=0;
static uint32_t hprio(const St*s){ int L=s->l[0]+s->l[1]; if(!L) return 0; int K=0,MK=0,cnt[2]={0,0},blk[2]={0,0};
  for(int r=0;r<2;r++){ int n=s->l[r]; if(!n) continue; int k=0;
    for(int i=0;i<n;i++){ int g=s->w[r][i]>>1, gp=s->w[r][(i+n-1)%n]>>1; cnt[g]++; if(g!=gp){ k++; blk[g]++; } }
    if(k==0) blk[s->w[r][0]>>1]++; int kr=k/2; K+=kr; if(kr>MK) MK=kr; }
  int th=cnt[0]<=cnt[1]?0:1; double S=blk[th]?(double)cnt[th]/blk[th]:0; double im=fabs((double)(cnt[0]-cnt[1]))/L;
  double P=L+2.53*K+6.418*MK+8.458*S+3.292*im+BAL*fabs((double)(s->l[0]-s->l[1])); return (uint32_t)(P*16.0); }
// BEAM_SHADOW=w with BEAM_SHADOW_FILE=probes.bin: add w x (sum over SL(2,p) probes of the exact shadow distance
// of (phi(r0), phi(r1)) to (phi(x), phi(y))) to the priority. Shadows ignore word length, so they keep
// pointing at the target during a hump (corr +0.24 with moves left on hump states, where length is -0.24).
typedef struct { uint32_t n; uint16_t one,img[4]; uint16_t*mul; uint8_t*dist; } Probe;
static Probe*PRB; static int NPRB; static double SHW;
static void load_probes(const char*fn){ FILE*f=fopen(fn,"rb"); if(!f) die("probe file"); char m[4]; uint32_t k;
  if(fread(m,1,4,f)!=4||memcmp(m,"SHDW",4)||fread(&k,4,1,f)!=1) die("probe header"); PRB=calloc(k,sizeof(Probe)); NPRB=(int)k;
  for(uint32_t i=0;i<k;i++){ Probe*P=&PRB[i]; if(fread(&P->n,4,1,f)!=1||fread(&P->one,2,1,f)!=1||fread(P->img,2,4,f)!=4) die("probe");
    uint64_t nn=(uint64_t)P->n*P->n; P->mul=malloc(nn*2); P->dist=malloc(nn);
    if(fread(P->mul,2,nn,f)!=nn||fread(P->dist,1,nn,f)!=nn) die("probe tables"); } fclose(f); }
static uint32_t shadow(const St*s){ uint32_t tot=0; for(int i=0;i<NPRB;i++){ const Probe*P=&PRB[i]; uint32_t g[2];
    for(int r=0;r<2;r++){ uint32_t x=P->one; for(int j=0;j<s->l[r];j++) x=P->mul[(uint64_t)x*P->n+P->img[s->w[r][j]]]; g[r]=x; }
    tot+=P->dist[(uint64_t)g[0]*P->n+g[1]]; } return tot; }
static int cmpc(const void*a,const void*b){ uint64_t x=((Cand*)a)->key,y=((Cand*)b)->key; return x<y?-1:x>y; }
int main(int argc,char**argv){
  const char*tf=argv[1]; uint64_t W=strtoull(argv[2],0,10); int DMAX=atoi(argv[3]); St s0; parse_state(argv,4,&s0);
  struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
  TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); if(TT.t==MAP_FAILED) die("mmap"); TT.N=stt.st_size/16;
  Tab V; tab_init(&V,1ULL<<24);
  Node*nodes=malloc(sizeof(Node)*(W*(uint64_t)(DMAX+1)+1)); uint64_t nn=0;
  uint64_t h1,h2; fp(&s0,&h1,&h2); tab_ins(&V,h1,h2,0,1); nodes[nn++]=(Node){store(&s0),0xFFFFFFFFu,255,(uint32_t)(s0.l[0]+s0.l[1])};
  uint64_t lo=0,hi=1; int bestAC=1<<30,bestSAC=1<<30; uint32_t acNode=0,sacNode=0; int acT=0,sacT=0; St acSt,sacSt;
  Cand*C=malloc(sizeof(Cand)*W*14); St*tmpS=malloc(sizeof(St)*1); (void)tmpS;
  static St cur,nx,sw; St*kids=NULL; uint64_t kcap=0;
  // scratch arena for one depth's children; permanent arena (AR) holds kept states only
  uint8_t*SA=NULL; uint64_t SAn=0,SAcap=0; Tab L; tab_init(&L,1ULL<<23);
  // BEAM_LOOK=1: two-level key (height = best total length reachable in one more move, tiebreak = own length)
  int LOOK=getenv("BEAM_LOOK")?atoi(getenv("BEAM_LOOK")):0;
  int HP=getenv("BEAM_H")?atoi(getenv("BEAM_H")):0; BAL=getenv("BEAM_BAL")?atof(getenv("BEAM_BAL")):0;
  SHW=getenv("BEAM_SHADOW")?atof(getenv("BEAM_SHADOW")):0.0; if(SHW>0){ if(!getenv("BEAM_SHADOW_FILE")) die("BEAM_SHADOW_FILE"); load_probes(getenv("BEAM_SHADOW_FILE")); }
  int NOISE=getenv("BEAM_NOISE")?atoi(getenv("BEAM_NOISE")):0; if(HP) NOISE*=16; /* priority is scaled x16 */ uint64_t SEED=getenv("BEAM_SEED")?strtoull(getenv("BEAM_SEED"),0,10)*0xD1B54A32D192ED03ULL:0;
  for(int d=1;d<=DMAX;d++){
    if(d>=bestAC && d+2>=bestSAC) break;
    Node*tmpN=malloc(sizeof(Node)*(hi-lo)*14+1); uint64_t nt=0; SAn=0; memset(L.t,0,16*L.N); L.n=0;
    for(uint64_t i=lo;i<hi;i++){ load(nodes[i].off,&cur);
      for(int m=0;m<14;m++){ apply(&cur,m,&nx); fp(&nx,&h1,&h2);
        if(tab_find(&V,h1,h2)>=0) continue; if(tab_ins(&L,h1,h2,1,1)>=0) continue;
        int t=tab_find(&TT,h1,h2); if(t>=0&&d+t<bestAC){ bestAC=d+t; acNode=(uint32_t)i; acT=t; acSt=nx; }
        swapst(&nx,&sw); uint64_t g1,g2; fp(&sw,&g1,&g2); int u=tab_find(&TT,g1,g2);
        if(u>=0&&d+u+2<bestSAC){ bestSAC=d+u+2; sacNode=(uint32_t)i; sacT=u; sacSt=nx; }
        uint32_t len=nx.l[0]+nx.l[1]; uint64_t need=4+len;
        if(SAn+need>SAcap){ SAcap=SAcap?SAcap*2:(1ULL<<26); while(SAn+need>SAcap) SAcap*=2; SA=realloc(SA,SAcap); if(!SA) die("scratch"); }
        uint8_t*q=SA+SAn; q[0]=nx.l[0]&255; q[1]=nx.l[0]>>8; q[2]=nx.l[1]&255; q[3]=nx.l[1]>>8; memcpy(q+4,nx.w[0],nx.l[0]); memcpy(q+4+nx.l[0],nx.w[1],nx.l[1]);
        tmpN[nt]=(Node){SAn,(uint32_t)i,(uint8_t)m,len}; SAn+=need;
        // BEAM_NOISE=n, BEAM_SEED=s: add a seeded pseudo-random 0..n to the length key (route diversity)
        uint32_t klen=HP?hprio(&nx):len; if(SHW>0) klen+=(uint32_t)(SHW*(HP?16.0:1.0)*shadow(&nx)+0.5); if(NOISE){ uint64_t z=(h1^SEED)*0x9E3779B97F4A7C15ULL; z^=z>>29; klen+=(uint32_t)(z%(uint64_t)(NOISE+1)); }
        uint64_t key=((uint64_t)klen<<40)|((h1^SEED)>>24);
        if(LOOK){ uint32_t best=len; St y; for(int m2=0;m2<14;m2++){ apply(&nx,m2,&y); uint32_t l2=y.l[0]+y.l[1]; if(l2<best) best=l2; }
          key=((uint64_t)best<<52)|((uint64_t)(len&4095)<<40)|(h1>>24); }
        C[nt]=(Cand){key,(uint32_t)nt}; nt++; } }
    uint64_t keep=nt<W?nt:W; if(nt>W){ qsort(C,nt,sizeof(Cand),cmpc);
      // diversity ("zag"): keep the best DIV fraction by length, fill the rest evenly from the longer remainder
      double DIV=getenv("BEAM_DIV")?atof(getenv("BEAM_DIV")):1.0; uint64_t k1=(uint64_t)(W*DIV); if(k1>W) k1=W;
      if(k1<W){ uint64_t rest=nt-k1, need=W-k1; for(uint64_t q=0;q<need;q++){ uint64_t src=k1+(uint64_t)((double)q*rest/need); C[k1+q]=C[src]; } }
      // novelty quota: at most NOV states per shape bucket (lengths + exponent sums), rest filled in length order
      int NOV=getenv("BEAM_NOV")?atoi(getenv("BEAM_NOV")):0;
      if(NOV>0){ static uint16_t cnt[1<<20]; memset(cnt,0,sizeof cnt); Cand*K=malloc(sizeof(Cand)*W); uint8_t*used=calloc(nt,1); uint64_t kk=0;
        for(uint64_t q=0;q<nt&&kk<W;q++){ Node x=tmpN[C[q].idx]; uint8_t*z=SA+x.off; int l0=z[0]|(z[1]<<8), l1=z[2]|(z[3]<<8); int e[4]={0,0,0,0};
          for(int t=0;t<l0;t++){ uint8_t c=z[4+t]; e[(c>>1)]+=(c&1)?-1:1; } for(int t=0;t<l1;t++){ uint8_t c=z[4+l0+t]; e[2+(c>>1)]+=(c&1)?-1:1; }
          uint64_t b=((uint64_t)l0*1315423911ULL)^((uint64_t)l1*2654435761ULL)^((uint64_t)(e[0]+64)<<8)^((uint64_t)(e[1]+64)<<16)^((uint64_t)(e[2]+64)<<24)^((uint64_t)(e[3]+64)<<32);
          b=(b*0x9E3779B97F4A7C15ULL)>>44; if(cnt[b]<NOV){ cnt[b]++; K[kk++]=C[q]; used[q]=1; } }
        for(uint64_t q=0;q<nt&&kk<W;q++) if(!used[q]) K[kk++]=C[q];
        memcpy(C,K,sizeof(Cand)*kk); free(K); free(used); } }
    lo=nn; for(uint64_t k=0;k<keep;k++){ Node x=tmpN[C[k].idx]; uint8_t*q=SA+x.off; St t2; t2.l[0]=q[0]|(q[1]<<8); t2.l[1]=q[2]|(q[3]<<8);
        memcpy(t2.w[0],q+4,t2.l[0]); memcpy(t2.w[1],q+4+t2.l[0],t2.l[1]); x.off=store(&t2); fp(&t2,&h1,&h2); tab_ins(&V,h1,h2,(d>15?15:d),1); nodes[nn++]=x; }
    hi=nn; free(tmpN);
    uint32_t mn=~0u,mx=0; for(uint64_t i=lo;i<hi;i++){ if(nodes[i].len<mn) mn=nodes[i].len; if(nodes[i].len>mx) mx=nodes[i].len; }
    if(d%10==0||bestAC<(1<<30)) fprintf(stderr,"d=%d gen=%llu kept=%llu len[%u..%u] bestAC=%d bestSAC=%d arena=%lluMB\n",d,(unsigned long long)nt,(unsigned long long)keep,mn,mx,bestAC<(1<<30)?bestAC:-1,bestSAC<(1<<30)?bestSAC:-1,(unsigned long long)(ARn>>20));
    if(hi==lo) break; }
  // rebuild: prefix via parent chain, then exact finish through T_9
  for(int which=0;which<2;which++){ int best=which?bestSAC:bestAC; if(best>=(1<<30)){ printf("%s NONE\n",which?"SAC":"AC"); continue; }
    uint32_t pn=which?sacNode:acNode; St fin=which?sacSt:acSt; int t=which?sacT:acT;
    int pre[4096],np=0; // moves from start to parent node, then the move to fin
    // find the move from parent to fin
    load(nodes[pn].off,&cur); int mfin=-1; for(int m=0;m<14;m++){ apply(&cur,m,&nx); if(st_eq(&nx,&fin)){ mfin=m; break; } }
    uint32_t q=pn; while(nodes[q].par!=0xFFFFFFFFu){ pre[np++]=nodes[q].mv; q=nodes[q].par; }
    int path[8192],L=0; for(int i=np-1;i>=0;i--) path[L++]=pre[i]; path[L++]=mfin;
    St c=fin; if(which) swapst(&fin,&c);
    for(int k=t;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&nx); fp(&nx,&h1,&h2); if(tab_find(&TT,h1,h2)==k-1){ path[L++]=which?PI[m]:m; c=nx; ok=1; break; } } if(!ok){ printf("REBUILD_FAIL\n"); break; } }
    if(which){ path[L++]=15; path[L++]=15; }
    printf("%s %d PATH",which?"SAC":"AC",L); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); }
  return 0; }
