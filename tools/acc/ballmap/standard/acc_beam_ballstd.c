// Beam search + exact finish. Forward beam from the start keeps the W states of smallest total
// relator length per depth (ties broken by fingerprint), deduplicated across all depths. Every
// generated state is looked up in T_9 (distance to (x,y)) and, via the generator swap, in T_9
// again (distance to (y,x)). A hit at depth d with ball distance t gives an AC path d+t (to (x,y))
// or a Stable AC path d+t+2 (via (y,x)). Kernel/fingerprint/table shared with acc_opt.c.
// usage: acc_beam TFILE W DMAX l0 w.. l1 w..
// Options (env): BEAM_H, BEAM_BAL, BEAM_DIV, BEAM_NOV, BEAM_NOISE, BEAM_SEED, BEAM_LOOK, BEAM_SHADOW(+_FILE),
// BEAM_MACROS(+BEAM_MACW), BEAM_P2 (+BEAM_P2CUT), BEAM_QUOTA (+BEAM_ELITE), BEAM_WH, BEAM_DUAL, BEAM_TRACE_FILE, BEAM_C16;
// see the comments at each.
// All off by default.
// build: gcc -O3 -march=native -o acc_beam acc_beam.c -lm
#define ACC_NO_MAIN
#include "acc_opt.c"
#include <math.h>
#include <gmp.h>
#include "c16_table.inc"
// BEAM_C16=file (ceiling finish table from acc_c16.c; rival idea nahom §2.1): every new child whose total length is <= the
// table's ceiling is also looked up there. Its distance c (BFS inside the ceiling, an upper bound on the true distance)
// gives an AC candidate td+c, and the swapped child (x<->y) gives a SAC candidate td+c+2, exactly as T does. T is looked
// up first and wins ties (strict <). A C16 finish's tail is rebuilt by greedy descent in the table (first move to an
// in-ceiling neighbour at distance c-1). Unset: the table is not loaded and nothing changes.
static C16 CT; static int C16on=0,acC16=0,sacC16=0; static uint64_t c16look,c16ac,c16sac;
typedef struct { uint64_t off; uint32_t par; uint8_t mv; uint32_t len; uint16_t td; uint16_t p2; } Node;  // td = true path length; p2 = P2 (BEAM_P2 only; same 24-byte size)
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
// BEAM_MACROS=file ("count: m1 m2 ..." per line), BEAM_MACW=w: Schur elimination of the hump (atlas UPG-FEEDBACK).
// Each mined up-and-back-down excursion is one extra child per state, so the high interior states never have to
// survive the beam. Children carry their true path length td; the key adds w x (td - layer) so extra moves cost.
static int NMAC; static uint8_t MAC[240][8]; static int MACL[240]; static double MACW=1.0;
static void load_macros(const char*fn){ FILE*f=fopen(fn,"rb"); if(!f) die("macro file"); char line[512];
  while(NMAC<240&&fgets(line,sizeof line,f)){ char*p=strchr(line,':'); if(!p) continue; p++; int k=0,v,off;
    while(k<8&&sscanf(p,"%d%n",&v,&off)==1){ if(v<0||v>13) die("macro move"); MAC[NMAC][k++]=(uint8_t)v; p+=off; }
    if(k>=2){ MACL[NMAC]=k; NMAC++; } } fclose(f); }
static int apply_macro(const St*s,int mi,St*r){ static St a,b; St*x=&a,*y=&b; *x=*s;
  for(int j=0;j<MACL[mi];j++){ if(x->l[0]+x->l[1]>2000) return 0; apply(x,MAC[mi][j],y); St*t=x; x=y; y=t; } *r=*x; return 1; }
// ---- P2 begin ----
// BEAM_P2=1: rank children by P2 (level-1 cut BEAM_P2CUT, default 8; 0 = no cut), then P1m, then the existing key
// (hprio when BEAM_H=1, else length, with the SHADOW/MACROS/NOISE terms). BEAM_P2=2: P2, then the existing key.
// BEAM_P2=3 (score zoo, research/acc/live/SCORE_ZOO.md): P2, then comm_len, then P1m, then the existing key, where
// comm_len = cyclically reduced length of r0 r1 r0^-1 r1^-1 on the stored words (O(L), computed for every child: it is
// the word-level tie-break that separates the conjugation children P2 ties).
// Definitions and tie-breaks are those of p2_hump_test.py (this is a port of the scratch p2bench.c, which matched the
// Python on 200/200 states). Words over aAbB (a=x A=x^-1 b=y B=y^-1, inverse = case flip), handled by cyclic cores:
//   P2  = best total cyclically reduced length after exactly two multiplications r_i <- rot(r_i)*rot(r_j)^{+-1},
//         level 1 cut to the c best classes (by cyclic total, then canonical key) before level 2 ("P2c" in the test).
//   P1m = stored r_i times a rotation of core(r_j)^{+-1}: free length + |core r_j| (min over i != j and the sign).
// P2 is a function of the unordered pair of cyclic classes up to rotation and inversion (the cut and the level-1 set
// only see all-rotation products, and a product rot(A^-1)rot(C) is conjugate-inverse to one rot(A)rot(C^-1) of no
// larger free length). Conjugation (6-13) and inversion (0-1) children therefore inherit the parent's P2 (compile
// with -DP2_CHECK_INHERIT to recompute and count mismatches); multiplication (2-5) and macro children compute it,
// with a class-keyed cache. P1m is not conjugation invariant and is computed for every child. A core longer than
// P2W, or a level-1 overflow, gives the saturated value P2SAT (ranked last).
#define P2W 256                       /* max core length of a relator for P2 */
#define P2L (2*P2W+4)                 /* max length of a level-1 product */
#define P2MAXS (1<<16)                /* level-1 classes (hash table has 2x slots) */
#define P2POOL (1<<23)
#define P2SAT 511
static inline char p2_invc(char c){ return c^0x20; }
static int p2_cycred(const char*w,int n,char*out){ int i=0,j=n; while(j-i>1&&w[i]==p2_invc(w[j-1])){ i++; j--; }
  memcpy(out,w+i,j-i); out[j-i]=0; return j-i; }
static void p2_inv(const char*w,int n,char*out){ for(int i=0;i<n;i++) out[i]=p2_invc(w[n-1-i]); out[n]=0; }
static int p2_minrot2(const char*d,int n){ int best=0; for(int i=1;i<n;i++){ if(memcmp(d+i,d+best,n)<0) best=i; } return best; }
static void p2_canon(const char*w,int n,char*out){          /* canonical cyclic word up to rotation and inversion */
  if(n==0){ out[0]=0; return; } char d[2*P2L+2],iw[P2L+1],di[2*P2L+2];
  memcpy(d,w,n); memcpy(d+n,w,n); p2_inv(w,n,iw); memcpy(di,iw,n); memcpy(di+n,iw,n);
  int a=p2_minrot2(d,n),b=p2_minrot2(di,n); if(memcmp(d+a,di+b,n)<=0) memcpy(out,d+a,n); else memcpy(out,di+b,n); out[n]=0; }
static int p2_lcs(const char*A,int n,const char*B,int m){    /* longest common cyclic subword, <= min(n,m) */
  if(!n||!m) return 0; char A2[2*P2L+2],B2[2*P2L+2]; memcpy(A2,A,n); memcpy(A2+n,A,n); memcpy(B2,B,m); memcpy(B2+m,B,m);
  int cap=n<m?n:m,best=0;
  for(int i=0;i<n;i++) for(int j=0;j<m;j++){ int k=0; while(k<cap&&A2[i+k]==B2[j+k]) k++; if(k>best){ best=k; if(best==cap) return cap; } }
  return best; }
static void p2_p1cores(const char*A,int n,const char*B,int m,int*cyc,int*fr){
  char iB[P2L+1]; p2_inv(B,m,iB); int kp=p2_lcs(A,n,iB,m),km=p2_lcs(A,n,B,m);
  int K=kp>km?kp:km,s=n<m?n:m,f=n+m-2*K+s,c=f;
  if(K==s){ const char*Lw=n>=m?A:B,*Sw=n>=m?B:A; int nl=n>=m?n:m,ns=n>=m?m:n;
    char L2[2*P2L+2],T[P2L+1],T2[2*P2L+2],rem[P2L+1],core[P2L+1]; memcpy(L2,Lw,nl); memcpy(L2+nl,Lw,nl);
    for(int sg=0;sg<2;sg++){ if((sg==0?kp:km)!=s) continue; if(sg==0) p2_inv(Sw,ns,T); else { memcpy(T,Sw,ns); T[ns]=0; }
      memcpy(T2,T,ns); memcpy(T2+ns,T,ns);
      for(int t=0;t<nl;t++){ int hit=0; for(int r=0;r<ns&&!hit;r++) if(!memcmp(L2+t,T2+r,ns)) hit=1; if(!hit) continue;
        memcpy(rem,L2+t+ns,nl-ns); int rl=p2_cycred(rem,nl-ns,core); if(rl+ns<c) c=rl+ns; } } }
  *cyc=c; *fr=f; }
static int p2_p1m(const char*r0,int n0,const char*r1,int n1){
  static char core[MAXW+1],ic[MAXW+1]; int best=1<<30;
  for(int side=0;side<2;side++){ const char*R=side?r1:r0,*O=side?r0:r1; int n=side?n1:n0,no=side?n0:n1;
    int m=p2_cycred(O,no,core); p2_inv(core,m,ic); int lim=n<m?n:m;
    for(int v=0;v<2;v++){ const char*Cw=v?ic:core;
      for(int q=0;q<m;q++){ int k=0; while(k<lim&&R[n-1-k]==p2_invc(Cw[(q+k)%m])) k++; int t=n+m-2*k+m; if(t<best) best=t; } } }
  return best; }
typedef struct { int ft,ci,p,q,k; } P2Pair;
typedef struct { int ct,ft,core_off,core_len,key1,key2,oth,p1c,p1f; } P2St;
static P2Pair*p2pairs; static P2St*p2sts; static P2St**p2lst; static char*p2pool; static int*p2order; static int p2top,p2nst,p2ovf;
static int p2htab[2*P2MAXS]; static unsigned p2hgen[2*P2MAXS],p2gen;
static const char*p2cC[4],*p2cmod[4]; static int p2cn[4],p2cm[4];
static char p2modD[4][2*P2W+2],p2CD[4][2*P2W+2],p2iCD[4][2*P2W+2],p2canA[P2W+1],p2canB[P2W+1];
static const char*p2kstr(int off){ return off<0?(off==-1?p2canA:p2canB):p2pool+off; }
static int p2keycmp(const P2St*a,const P2St*b){ int c=strcmp(p2kstr(a->key1),p2kstr(b->key1)); return c?c:strcmp(p2kstr(a->key2),p2kstr(b->key2)); }
static int p2_byct(const void*x,const void*y){ const P2St*a=*(P2St*const*)x,*b=*(P2St*const*)y; return a->ct!=b->ct?a->ct-b->ct:p2keycmp(a,b); }
static uint32_t p2_hsh(const char*a,const char*b){ uint32_t h=2166136261u; for(;*a;a++) h=(h^(unsigned char)*a)*16777619u;
  h=(h^'|')*16777619u; for(;*b;b++) h=(h^(unsigned char)*b)*16777619u; return h; }
static void p2_add(const P2Pair*pr){
  if(p2ovf) return; int n=p2cn[pr->ci],m=p2cm[pr->ci],k=pr->k,L=0; char w[P2L+1],core[P2L+1],cn[P2L+1];
  memcpy(w,p2modD[pr->ci]+pr->p,n-k); L=n-k; memcpy(w+L,p2CD[pr->ci]+pr->q+k,m-k); L+=m-k;
  int cl=p2_cycred(w,L,core); p2_canon(core,cl,cn);
  int othkey=pr->ci<2?-2:-1; const char*co=p2kstr(othkey); int cnf=strcmp(cn,co)<=0;
  uint32_t h=cnf?p2_hsh(cn,co):p2_hsh(co,cn); int ct=cl+m;
  for(uint32_t s=h&(2*P2MAXS-1);;s=(s+1)&(2*P2MAXS-1)){ int id=p2hgen[s]==p2gen?p2htab[s]:-1;
    if(id<0){ if(p2nst>=P2MAXS||p2top+2*(cl+1)>P2POOL){ p2ovf=1; return; } p2hgen[s]=p2gen; P2St*e=&p2sts[p2nst];
      e->ct=ct; e->ft=pr->ft; e->p1c=-1; e->core_off=p2top; memcpy(p2pool+p2top,core,cl+1); e->core_len=cl; p2top+=cl+1;
      int cnoff=p2top; memcpy(p2pool+p2top,cn,cl+1); p2top+=cl+1;
      e->key1=cnf?cnoff:othkey; e->key2=cnf?othkey:cnoff; e->oth=pr->ci<2?1:0; p2htab[s]=p2nst++; return; }
    P2St*e=&p2sts[id]; const char*k1=p2kstr(e->key1),*k2=p2kstr(e->key2);
    if(!strcmp(k1,cnf?cn:co)&&!strcmp(k2,cnf?co:cn)){ if(ct<e->ct) e->ct=ct; if(pr->ft<e->ft) e->ft=pr->ft; return; } } }
static int p2_eval(const char*A,int n,const char*B,int m,int cut){   /* P2c of cores A (n), B (m); -1 on overflow */
  if(!p2pairs){ p2pairs=malloc(sizeof(P2Pair)*4*P2W*P2W); p2order=malloc(sizeof(int)*4*P2W*P2W); p2sts=malloc(sizeof(P2St)*P2MAXS);
    p2lst=malloc(sizeof(P2St*)*P2MAXS); p2pool=malloc(P2POOL); if(!p2pairs||!p2order||!p2sts||!p2lst||!p2pool) die("p2 alloc"); }
  char iA[P2W+1],iB[P2W+1]; p2_inv(A,n,iA); p2_inv(B,m,iB); p2_canon(A,n,p2canA); p2_canon(B,m,p2canB);
  p2cmod[0]=A; p2cC[0]=B;  p2cn[0]=n; p2cm[0]=m;   p2cmod[1]=A; p2cC[1]=iB; p2cn[1]=n; p2cm[1]=m;
  p2cmod[2]=B; p2cC[2]=A;  p2cn[2]=m; p2cm[2]=n;   p2cmod[3]=B; p2cC[3]=iA; p2cn[3]=m; p2cm[3]=n;
  int np=0,maxft=0;
  for(int ci=0;ci<4;ci++){ int nn=p2cn[ci],mm=p2cm[ci],lim=nn<mm?nn:mm; char*md=p2modD[ci],*cd=p2CD[ci],*icd=p2iCD[ci];
    memcpy(md,p2cmod[ci],nn); memcpy(md+nn,p2cmod[ci],nn); memcpy(cd,p2cC[ci],mm); memcpy(cd+mm,p2cC[ci],mm);
    for(int i=0;i<2*mm;i++) icd[i]=p2_invc(cd[i]);
    for(int p=0;p<nn;p++){ const char*a=md+p-1+nn;             /* a[-k] = mod[(p-1-k) mod n] */
      for(int q=0;q<mm;q++){ const char*c=icd+q; int k=0; while(k<lim&&a[-k]==c[k]) k++;
        P2Pair*pr=&p2pairs[np++]; pr->ft=nn+mm-2*k+mm; pr->ci=ci; pr->p=p; pr->q=q; pr->k=k; if(pr->ft>maxft) maxft=pr->ft; } } }
  p2gen++; p2nst=0; p2top=0; p2ovf=0;
  for(int i=0;i<np;i++){ int lim=p2cn[p2pairs[i].ci]<p2cm[p2pairs[i].ci]?p2cn[p2pairs[i].ci]:p2cm[p2pairs[i].ci]; if(p2pairs[i].k==lim) p2_add(&p2pairs[i]); }
  static int cnt[4*P2W+4],start[4*P2W+4];                      /* counting sort of the other pairs by ft */
  memset(cnt,0,sizeof(int)*(maxft+2)); for(int i=0;i<np;i++) cnt[p2pairs[i].ft]++;
  start[0]=0; for(int f=1;f<=maxft+1;f++) start[f]=start[f-1]+cnt[f-1];
  for(int i=0;i<np;i++) p2order[start[p2pairs[i].ft]++]=i;
  for(int f=maxft+1;f>0;f--) start[f]=start[f-1]; start[0]=0;
  for(int f=0;f<=maxft;f++){ if(!cnt[f]) continue;
    for(int j=start[f];j<start[f]+cnt[f];j++){ P2Pair*pr=&p2pairs[p2order[j]]; int lim=p2cn[pr->ci]<p2cm[pr->ci]?p2cn[pr->ci]:p2cm[pr->ci]; if(pr->k!=lim) p2_add(pr); }
    if(cut>0&&p2nst>=cut){ int nc=0,nf=0; for(int i=0;i<p2nst;i++){ nc+=p2sts[i].ct<=f; nf+=p2sts[i].ft<=f; } if(nc>=cut&&nf>=cut) break; } }
  if(p2ovf||!p2nst) return -1;
  for(int i=0;i<p2nst;i++) p2lst[i]=&p2sts[i];
  int lim=(cut>0&&cut<p2nst)?cut:p2nst,best=1<<30; qsort(p2lst,p2nst,sizeof(P2St*),p2_byct);
  for(int i=0;i<lim;i++){ P2St*e=p2lst[i]; if(e->p1c<0){ const char*o=e->oth?B:A; int on=e->oth?m:n; p2_p1cores(p2pool+e->core_off,e->core_len,o,on,&e->p1c,&e->p1f); }
    if(e->p1c<best) best=e->p1c; }
  return best; }
// beam wrappers: letter codes 0..3 -> a A b B; class-keyed direct-mapped cache
static int P2M=0,P2CUT=8; static uint64_t P2calls,P2hits,P2satn,P2inh; static double P2time;
typedef struct { uint64_t a,b; uint32_t v; } P2Cache; static P2Cache*P2C;
#define P2CB 18
static void p2_enc(const uint8_t*w,int n,char*o){ static const char E[4]={'a','A','b','B'}; for(int i=0;i<n;i++) o[i]=E[w[i]]; o[n]=0; }
static uint16_t p2_of(const St*s){ static char r0[MAXW+1],r1[MAXW+1],A[MAXW+1],B[MAXW+1];
  double t0=now(); P2calls++; p2_enc(s->w[0],s->l[0],r0); p2_enc(s->w[1],s->l[1],r1);
  int na=p2_cycred(r0,s->l[0],A),nb=p2_cycred(r1,s->l[1],B);
  if(na>P2W||nb>P2W||!na||!nb){ P2satn++; P2time+=now()-t0; return P2SAT; }
  char ca[P2W+1],cb[P2W+1]; p2_canon(A,na,ca); p2_canon(B,nb,cb); const char*x=strcmp(ca,cb)<=0?ca:cb,*y=x==ca?cb:ca;
  uint64_t ha=0xcbf29ce484222325ULL,hb=0x84222325cbf29ce4ULL^(uint64_t)P2CUT;
  for(const char*p=x;;p++){ unsigned char c=*p?(unsigned char)*p:'|'; ha=(ha^c)*0x100000001b3ULL; hb=fmix_b(hb+c*0x9E3779B97F4A7C15ULL); if(!*p) break; }
  for(const char*p=y;*p;p++){ ha=(ha^(unsigned char)*p)*0x100000001b3ULL; hb=fmix_b(hb+(unsigned char)*p*0x9E3779B97F4A7C15ULL); }
  ha|=1; if(!P2C){ P2C=calloc((size_t)1<<P2CB,sizeof(P2Cache)); if(!P2C) die("p2 cache"); }
  P2Cache*e=&P2C[fmix_a(ha^hb)>>(64-P2CB)]; if(e->a==ha&&e->b==hb){ P2hits++; P2time+=now()-t0; return (uint16_t)e->v; }
  int v=p2_eval(A,na,B,nb,P2CUT); if(v<0||v>P2SAT){ v=P2SAT; P2satn++; }
  e->a=ha; e->b=hb; e->v=(uint32_t)v; P2time+=now()-t0; return (uint16_t)v; }
static uint32_t p1m_of(const St*s){ static char r0[MAXW+1],r1[MAXW+1]; p2_enc(s->w[0],s->l[0],r0); p2_enc(s->w[1],s->l[1],r1);
  int v=p2_p1m(r0,s->l[0],r1,s->l[1]); return v>1023?1023:(uint32_t)v; }
static uint32_t comm_len(const St*s){ static uint8_t o[4*MAXW+8]; int n=0;   /* |cycred(r0 r1 r0^-1 r1^-1)|, saturated at 1023 */
  for(int i=0;i<s->l[0];i++) n=push_red(o,n,s->w[0][i]); for(int i=0;i<s->l[1];i++) n=push_red(o,n,s->w[1][i]);
  for(int i=s->l[0]-1;i>=0;i--) n=push_red(o,n,s->w[0][i]^1); for(int i=s->l[1]-1;i>=0;i--) n=push_red(o,n,s->w[1][i]^1);
  int i=0,j=n; while(j-i>1&&o[i]==(o[j-1]^1)){ i++; j--; } return (uint32_t)(j-i>1023?1023:j-i); }
// ---- P2 end ----
// ---- atlas begin ----
// BEAM_QUOTA=q (atlas B16/B17, "overflow builds its own wall"): at most q survivors per class, class = the unordered
// pair of cyclic conjugacy classes of (r0, r1), each taken up to inversion (hash of the cyclically reduced word's least
// rotation, the smaller of the word's and its inverse's). Candidates are admitted in key order; BEAM_DIV then keeps
// its best fraction and samples its tail from the admitted list only. If fewer than W are admitted, the remaining
// slots are filled from the over-quota candidates in key order. Not combinable with BEAM_NOV.
// BEAM_ELITE=e (with BEAM_QUOTA; "protect what can be protected, release the rest"): the best e candidates by the full
// key are admitted regardless of class and do not use up their class's quota; the quota applies to the rest only.
// BEAM_WH=1 (atlas B83, "measure in a matched frame"): secondary key = Whitehead-minimal cyclic total length, found by
// greedy steepest descent over the 8 automorphisms x->x y^e, x->y^e x, y->y x^e, y->x^e y (e = +-1) applied to both
// cyclic words until none lowers the total. It sits right after P2 when BEAM_P2 is set (in P1m's slot for mode 2,
// before P1m for mode 1), else right after the existing key; only fingerprint tie-break bits come after it.
// Class and WH are functions of the class, so conjugation (6-13) and inversion (0-1) children inherit them;
// multiplication (2-5) and macro children compute them, WH through a class-keyed cache.
// BEAM_TRACE_FILE=f (atlas B20 / Plate XI, "lost among ties, ranked wrong, or short of width?"): lines "i h1 h2"
// (index on a known path, hex fingerprints of that state as fp() gives them). Each depth prints to stderr, for every
// traced state that becomes a candidate: its rank in the sorted candidate list, the tie block [lo,hi) of its key
// without the fingerprint bits, the cut keys at k1 = W*DIV and W, and whether it survived. Observation only.
static int QUOTA=0,WHM=0; static uint64_t ELITE=0; static double DUALF=0;
// BEAM_CLIMB=c ("opposite approach", 2026-09-28): for depths 1..c the plain length key is inverted (longer first), so the
// beam deliberately climbs before it descends; hump rows' record paths must first grow the relators. Main and second-eye
// keys both use the inverted key during the climb. Unset: no change.
static int CLIMB=0;
// BEAM_DUAL=f (0<f<1; "two eyes", from the beam-loss diagnostic: P2 drops roads at single-step P2 rises that the plain
// H key keeps): the first f*W survivors are chosen by the main key exactly as without BEAM_DUAL (QUOTA/ELITE/DIV/NOV
// as set, with f*W in place of W); the other (1-f)*W are the best by the plain key (klen: hprio when BEAM_H=1, else
// length, plus SHADOW/MACROS/NOISE terms; fingerprint tie-break) among the candidates the first eye left, with the
// same BEAM_DIV split (best DIV fraction, the rest sampled evenly from that eye's tail). Candidates are unique by
// fingerprint within a depth, so the eyes never share a state.
static uint64_t WHcalls,WHhits,WHsat; static double WHtime;
static int at_least_rot(const uint8_t*s,int n){ int i=0,j=1,k=0;   /* s holds the word twice */
  while(i<n&&j<n&&k<n){ uint8_t a=s[i+k],b=s[j+k]; if(a==b){ k++; continue; } if(a>b) i+=k+1; else j+=k+1; if(i==j) j++; k=0; }
  return i<j?i:j; }
static uint64_t at_rel_class(const uint8_t*w,int n){ int i=0,j=n; while(j-i>1&&w[i]==(w[j-1]^1)){ i++; j--; } int m=j-i;
  if(!m) return 0x5BD1E9955BD1E995ULL; static uint8_t d[2*MAXW],di[2*MAXW];
  memcpy(d,w+i,m); memcpy(d+m,w+i,m); for(int t=0;t<m;t++) di[t]=w[j-1-t]^1; memcpy(di+m,di,m);
  int a=at_least_rot(d,m),b=at_least_rot(di,m); const uint8_t*p=memcmp(d+a,di+b,m)<=0?d+a:di+b;
  uint64_t h=0x9E3779B97F4A7C15ULL^((uint64_t)m*0xC2B2AE3D27D4EB4FULL),c=0; int t=0;
  for(int q=0;q<m;q++){ c|=(uint64_t)p[q]<<(2*t); if(++t==32){ h=fmix_a(h^c); c=0; t=0; } }
  return fmix_a(h^c^((uint64_t)t<<58)); }
static uint64_t at_class(const St*s){ uint64_t a=at_rel_class(s->w[0],s->l[0]),b=at_rel_class(s->w[1],s->l[1]);
  if(a>b){ uint64_t t=a; a=b; b=t; } return fmix_b(a*0x9FB21C651E98DF25ULL^rotl(b,23))|1ULL; }
static int wh_img(const uint8_t*w,int n,int a,uint8_t*o){     /* a: bit2 gen (x/y), bit1 side (g->g t / g->t g), bit0 e */
  uint8_t g=(a>>2)?2:0,t=(uint8_t)(((a>>2)?0:2)|(a&1)); int side=(a>>1)&1,L=0;
  for(int i=0;i<n;i++){ uint8_t c=w[i];
    if(c==g){ if(!side){ L=push_red(o,L,g); L=push_red(o,L,t); } else { L=push_red(o,L,t); L=push_red(o,L,g); } }
    else if(c==(g^1)){ if(!side){ L=push_red(o,L,t^1); L=push_red(o,L,g^1); } else { L=push_red(o,L,g^1); L=push_red(o,L,t^1); } }
    else L=push_red(o,L,c); }
  int i=0,j=L; while(j-i>1&&o[i]==(o[j-1]^1)){ i++; j--; } if(i) memmove(o,o+i,j-i); return j-i; }
#define WHCAP 4000                    /* cyclic total above this: WH saturates at 1023 */
static uint16_t wh_min(const St*s){ static uint8_t buf[6][2*WHCAP+8]; uint8_t*cu[2]={buf[0],buf[1]},*bs[2]={buf[2],buf[3]},*cd[2]={buf[4],buf[5]};
  int n[2]; for(int r=0;r<2;r++){ int i=0,j=s->l[r]; const uint8_t*w=s->w[r]; while(j-i>1&&w[i]==(w[j-1]^1)){ i++; j--; } n[r]=j-i;
    if(n[0]+(r?n[1]:0)>WHCAP){ WHsat++; return 1023; } memcpy(cu[r],w+i,n[r]); }
  int tot=n[0]+n[1];
  for(;;){ int best=tot,bn[2]={0,0};
    for(int a=0;a<8;a++){ int l0=wh_img(cu[0],n[0],a,cd[0]),l1=wh_img(cu[1],n[1],a,cd[1]);
      if(l0+l1<best){ best=l0+l1; bn[0]=l0; bn[1]=l1; uint8_t*t0=bs[0],*t1=bs[1]; bs[0]=cd[0]; bs[1]=cd[1]; cd[0]=t0; cd[1]=t1; } }
    if(best>=tot) break; uint8_t*t0=cu[0],*t1=cu[1]; cu[0]=bs[0]; cu[1]=bs[1]; bs[0]=t0; bs[1]=t1; n[0]=bn[0]; n[1]=bn[1]; tot=best; }
  return (uint16_t)(tot>1023?1023:tot); }
typedef struct { uint64_t c; uint16_t v; } WHCache; static WHCache*WHC;
#define WHCB 18
static uint16_t wh_of(const St*s,uint64_t cls){ double t0=now(); WHcalls++;
  if(!WHC){ WHC=calloc((size_t)1<<WHCB,sizeof(WHCache)); if(!WHC) die("wh cache"); }
  WHCache*e=&WHC[fmix_a(cls)>>(64-WHCB)]; if(e->c==cls){ WHhits++; WHtime+=now()-t0; return e->v; }
  uint16_t v=wh_min(s); e->c=cls; e->v=v; WHtime+=now()-t0; return v; }
#define TRMAX 4096
static int NTR; static uint64_t TRh1[TRMAX],TRh2[TRMAX]; static int TRi[TRMAX];
static void load_trace(const char*fn){ FILE*f=fopen(fn,"r"); if(!f) die("trace file"); char line[256];
  while(NTR<TRMAX&&fgets(line,sizeof line,f)){ int i; unsigned long long a,b; if(sscanf(line,"%d %llx %llx",&i,&a,&b)!=3) continue;
    TRi[NTR]=i; TRh1[NTR]=a; TRh2[NTR]=b; NTR++; } fclose(f); }
static int trace_find(uint64_t h1,uint64_t h2){ for(int k=0;k<NTR;k++) if(TRh1[k]==h1&&TRh2[k]==h2) return TRi[k]; return -1; }
// ---- atlas end ----
static int cmpc(const void*a,const void*b){ uint64_t x=((Cand*)a)->key,y=((Cand*)b)->key; return x<y?-1:x>y; }
/* BEAM_CHAIN=1 (P2 mode 2 only): ordered-chain tie-break behind H, ahead of the fingerprint (Astra's Snell-Smith
   chain test, optimality/experiments/astra_snell_smith_chain). Sanov matrices X=[[1,2],[0,1]], Y=[[1,0],[2,1]];
   score = d(i, X^-1 rho(r0) i) + d(i, Y^-1 rho(r1) i), d = acosh(|A|_F^2 / 2); quantized to 10 bits (x4). Off by default. */
static int CHAIN=0;
/* BEAM_CHAIN=2 (atlas B69/B79/B83): trace mode. The Frobenius distance above depends on the rotation of each relator (a fixed
   frame, B83), so rotations that change nothing about the class move the score. Trace is conjugation-invariant (a scalar built
   from the operator alone, B79) and acosh(|tr|/2) = log of the spectral radius = half the SL2 rate -log|l2/l1| (B69).
   score = sum_i acosh(max(1, |tr rho(r_i)|/2)); 0 at the target (tr rho(x) = tr rho(y) = 2). Same quantization. */
static uint32_t chain_q(const St*s){ double tot=0;
  for(int r=0;r<2;r++){ double a=1,b=0,c=0,d=1;   /* start with the inverse of the target generator (mode 1) or I (mode 2) */
    if(CHAIN!=2){ if(r==0){ b=-2; } else { c=-2; } }
    for(int k=0;k<s->l[r];k++){ double e,f,g,h; switch(s->w[r][k]){
        case 0: e=1;f=2;g=0;h=1;break; case 1: e=1;f=-2;g=0;h=1;break; case 2: e=1;f=0;g=2;h=1;break; default: e=1;f=0;g=-2;h=1; }
      double na=a*e+b*g, nb=a*f+b*h, nc=c*e+d*g, nd=c*f+d*h; a=na;b=nb;c=nc;d=nd; }
    if(CHAIN==2){ double t=fabs(a+d)/2; tot+=t<=1?0:acosh(t); }
    else { double n2=(a*a+b*b+c*c+d*d)/2; tot+=n2<=1?0:acosh(n2); } }
  double q=tot*4; return q>1023?1023u:(uint32_t)q; }
static double LOOPW=0, LOOPZ=5;
/* BEAM_LOOP=w, BEAM_LOOPZ=z (ball mixer pair loop): klen = 16*len + 16*w*(log|2 - tr[rho r0, rho r1]| + 25),
   rho(x)=diag(e^a,e^-a), rho(y)=[[ch b,sh b],[sh b,ch b]], a=b=ln(z)/2. Off by default. */
static double loop_k(const St*s){ double M[2][4]; double a=log(LOOPZ)/2, ea=exp(a), ch=cosh(a), sh=sinh(a);
  for(int r=0;r<2;r++){ double p=1,q=0,u=0,v=1;
    for(int k=0;k<s->l[r];k++){ double e,f,g,h; switch(s->w[r][k]){
        case 0: e=ea;f=0;g=0;h=1/ea;break; case 1: e=1/ea;f=0;g=0;h=ea;break; case 2: e=ch;f=sh;g=sh;h=ch;break; default: e=ch;f=-sh;g=-sh;h=ch; }
      double np=p*e+q*g, nq=p*f+q*h, nu=u*e+v*g, nv=u*f+v*h; p=np;q=nq;u=nu;v=nv; }
    M[r][0]=p;M[r][1]=q;M[r][2]=u;M[r][3]=v; }
  double *A=M[0],*B=M[1]; double Ai[4]={A[3],-A[1],-A[2],A[0]}, Bi[4]={B[3],-B[1],-B[2],B[0]};
  double P[4]={A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3]};
  double Q[4]={Ai[0]*Bi[0]+Ai[1]*Bi[2],Ai[0]*Bi[1]+Ai[1]*Bi[3],Ai[2]*Bi[0]+Ai[3]*Bi[2],Ai[2]*Bi[1]+Ai[3]*Bi[3]};
  double tr=P[0]*Q[0]+P[1]*Q[2]+P[2]*Q[1]+P[3]*Q[3]; double k=fabs(2-tr);
  if(!isfinite(k)) return 200; double l=log(k>1e-11?k:1e-11); return l>200?200:l; }
static double REACHW=0, REACHZ=5;
/* BEAM_REACH=w, BEAM_REACHZ=z (grid ball field, grid movement): klen += 16*w*(reach(r0)+reach(r1)), reach(M) = d(i, M i) =
   acosh(|M|_F^2/2) for M = rho(word) at step ratio z. A sum of squares, so no cancellation; products rescaled to avoid overflow. */
static double reach_w(const uint8_t*w,int n){ double a=log(REACHZ)/2, ea=exp(a), ch=cosh(a), sh=sinh(a), p=1,q=0,u=0,v=1, ls=0;
  for(int k=0;k<n;k++){ double e,f,g,h; switch(w[k]){ case 0: e=ea;f=0;g=0;h=1/ea;break; case 1: e=1/ea;f=0;g=0;h=ea;break; case 2: e=ch;f=sh;g=sh;h=ch;break; default: e=ch;f=-sh;g=-sh;h=ch; }
    double np=p*e+q*g, nq=p*f+q*h, nu=u*e+v*g, nv=u*f+v*h; p=np;q=nq;u=nu;v=nv;
    double m=fabs(p); if(fabs(q)>m) m=fabs(q); if(fabs(u)>m) m=fabs(u); if(fabs(v)>m) m=fabs(v);
    if(m>1e100){ p/=1e100;q/=1e100;u/=1e100;v/=1e100; ls+=log(1e100); } }
  double lf=log(p*p+q*q+u*u+v*v)+2*ls-log(2.0);            /* ln(|M|_F^2/2) */
  if(lf>20) return lf+log(2.0); double x=exp(lf); return x<=1?0:acosh(x); }
static double reach_k(const St*s){ return reach_w(s->w[0],s->l[0])+reach_w(s->w[1],s->l[1]); }
static double RELW=0, RELB=0.5;
/* BEAM_REL=w (ball field, relative to the finish): klen += 16*w*( d(p, X^-1 rho(r0) p) + d(p, Y^-1 rho(r1) p) ), z = BEAM_REACHZ (default 5),
   base point p = BEAM_RELB steps of arm I from the centre (default 0.5). Sum of squares only: no cancellation; rescaled products. */
static double rel_w(int first,const uint8_t*w,int n){ double a=log(REACHZ)/2, ea=exp(a), ch=cosh(a), sh=sinh(a), ls=0, p,q,u,v;
  if(first==1){ p=1/ea;q=0;u=0;v=ea; } else { p=ch;q=-sh;u=-sh;v=ch; }          /* X^-1 or Y^-1 first */
  for(int k=0;k<n;k++){ double e,f,g,h; switch(w[k]){ case 0: e=ea;f=0;g=0;h=1/ea;break; case 1: e=1/ea;f=0;g=0;h=ea;break; case 2: e=ch;f=sh;g=sh;h=ch;break; default: e=ch;f=-sh;g=-sh;h=ch; }
    double np=p*e+q*g, nq=p*f+q*h, nu=u*e+v*g, nv=u*f+v*h; p=np;q=nq;u=nu;v=nv;
    double m=fabs(p); if(fabs(q)>m) m=fabs(q); if(fabs(u)>m) m=fabs(u); if(fabs(v)>m) m=fabs(v);
    if(m>1e100){ p/=1e100;q/=1e100;u/=1e100;v/=1e100; ls+=log(1e100); } }
  double b=exp(RELB*2*a/2);                                  /* g = diag(b,1/b): p = g(i); g^-1 M g */
  double gp=p, gq=q/(b*b), gu=u*b*b, gv=v;
  double lf=log(gp*gp+gq*gq+gu*gu+gv*gv)+2*ls-log(2.0);
  if(lf>20) return lf+log(2.0); double x=exp(lf); return x<=1?0:acosh(x); }
static double rel_k(const St*s){ return rel_w(1,s->w[0],s->l[0])+rel_w(2,s->w[1],s->l[1]); }
static double PEELW=0; static int PEELK=3;
/* BEAM_PEEL=w (ball standard, Schur peel): klen += 16*w*P, P = min over |k| <= BEAM_PEELK of
   |k| ln z + d(p, X^-1 A p) + d(p, Y^-1 B A^k p), and the mirror |k| ln z + d(p, X^-1 A B^k p) + d(p, Y^-1 B p); p = centre, z = BEAM_REACHZ. */
typedef struct { double m[4]; double ls; } SM;
static SM sm_id(void){ SM r={{1,0,0,1},0}; return r; }
static SM sm_mul(SM A,SM B){ SM r; r.m[0]=A.m[0]*B.m[0]+A.m[1]*B.m[2]; r.m[1]=A.m[0]*B.m[1]+A.m[1]*B.m[3]; r.m[2]=A.m[2]*B.m[0]+A.m[3]*B.m[2]; r.m[3]=A.m[2]*B.m[1]+A.m[3]*B.m[3]; r.ls=A.ls+B.ls;
  double mx=fabs(r.m[0]); for(int i=1;i<4;i++) if(fabs(r.m[i])>mx) mx=fabs(r.m[i]); if(mx>1e60){ for(int i=0;i<4;i++) r.m[i]/=1e60; r.ls+=log(1e60); } return r; }
static SM sm_inv(SM A){ SM r={{A.m[3],-A.m[1],-A.m[2],A.m[0]},-A.ls}; return r; }
static SM sm_gen(int c){ double a=log(REACHZ)/2, ea=exp(a), ch=cosh(a), sh=sinh(a); SM r={{1,0,0,1},0};
  switch(c){ case 0: r.m[0]=ea;r.m[3]=1/ea;break; case 1: r.m[0]=1/ea;r.m[3]=ea;break; case 2: r.m[0]=ch;r.m[1]=sh;r.m[2]=sh;r.m[3]=ch;break; default: r.m[0]=ch;r.m[1]=-sh;r.m[2]=-sh;r.m[3]=ch; } return r; }
static SM sm_word(const uint8_t*w,int n){ SM r=sm_id(); for(int k=0;k<n;k++) r=sm_mul(r,sm_gen(w[k])); return r; }
static double sm_d(SM M){ double lf=log(M.m[0]*M.m[0]+M.m[1]*M.m[1]+M.m[2]*M.m[2]+M.m[3]*M.m[3])+2*M.ls-log(2.0);
  if(lf>20) return lf+log(2.0); double x=exp(lf); return x<=1?0:acosh(x); }
static double peel_k(const St*s){ SM A=sm_word(s->w[0],s->l[0]), B=sm_word(s->w[1],s->l[1]), Xi=sm_gen(1), Yi=sm_gen(3);
  SM XA=sm_mul(Xi,A), YB=sm_mul(Yi,B); double dA=sm_d(XA), dB=sm_d(YB), best=dA+dB, lz=log(REACHZ);
  SM Ai=sm_inv(A), Bi=sm_inv(B), pB=B, nB=B, pA=A, nA=A;
  for(int k=1;k<=PEELK;k++){ pB=sm_mul(pB,A); nB=sm_mul(nB,Ai); pA=sm_mul(pA,B); nA=sm_mul(nA,Bi);
    double v; v=k*lz+dA+sm_d(sm_mul(Yi,pB)); if(v<best) best=v; v=k*lz+dA+sm_d(sm_mul(Yi,nB)); if(v<best) best=v;
    v=k*lz+sm_d(sm_mul(Xi,pA))+dB; if(v<best) best=v; v=k*lz+sm_d(sm_mul(Xi,nA))+dB; if(v<best) best=v; }
  return best; }
static double LOOPXW=0;
/* BEAM_LOOPX=w (ball standard, exact loop at z = 5): klen += 16*w*(L + 25), L = ln|2 - tr[rho r0, rho r1]| computed EXACTLY:
   rho(w) = M(w)/5^(|w|/2) with integer M; k*5^n = 4*5^n - tA^2 5^|B| - tB^2 5^|A| - tAB^2 + tA tB tAB (GMP). Unchanged by moves 0-5. */
static mpz_t P5[2*MAXW+8]; static int P5n=0;
static void p5_init(void){ if(P5n) return; for(int i=0;i<2*MAXW+8;i++){ mpz_init(P5[i]); if(i==0) mpz_set_ui(P5[0],1); else mpz_mul_ui(P5[i],P5[i-1],5); } P5n=1; }
static void iw_word(const uint8_t*w,int n,mpz_t M[4]){ static mpz_t t[4]; static int ini=0; if(!ini){ for(int i=0;i<4;i++) mpz_init(t[i]); ini=1; }
  mpz_set_ui(M[0],1); mpz_set_ui(M[1],0); mpz_set_ui(M[2],0); mpz_set_ui(M[3],1);
  for(int k=0;k<n;k++){ switch(w[k]){
    case 0: mpz_mul_ui(M[0],M[0],5); mpz_mul_ui(M[2],M[2],5); break;            /* right-multiply by diag(5,1) */
    case 1: mpz_mul_ui(M[1],M[1],5); mpz_mul_ui(M[3],M[3],5); break;            /* by diag(1,5) */
    default: { long sg = (w[k]==2)?2:-2;                                        /* by [[3,sg],[sg,3]] */
      for(int r=0;r<2;r++){ mpz_mul_si(t[0],M[2*r],3); mpz_addmul_ui(t[0],M[2*r+1],0); mpz_mul_si(t[1],M[2*r+1],sg); mpz_add(t[0],t[0],t[1]);
        mpz_mul_si(t[2],M[2*r],sg); mpz_mul_si(t[3],M[2*r+1],3); mpz_add(t[2],t[2],t[3]); mpz_set(M[2*r],t[0]); mpz_set(M[2*r+1],t[2]); } } } } }
static double loopx_k(const St*s){ static mpz_t A[4],B[4],tA,tB,tAB,K,u; static int ini=0;
  if(!ini){ for(int i=0;i<4;i++){ mpz_init(A[i]); mpz_init(B[i]); } mpz_init(tA); mpz_init(tB); mpz_init(tAB); mpz_init(K); mpz_init(u); ini=1; p5_init(); }
  int a=s->l[0], b=s->l[1], n=a+b; iw_word(s->w[0],a,A); iw_word(s->w[1],b,B);
  mpz_add(tA,A[0],A[3]); mpz_add(tB,B[0],B[3]);
  mpz_mul(tAB,A[0],B[0]); mpz_addmul(tAB,A[1],B[2]); mpz_addmul(tAB,A[2],B[1]); mpz_addmul(tAB,A[3],B[3]);
  mpz_mul_ui(K,P5[n],4); mpz_mul(u,tA,tA); mpz_mul(u,u,P5[b]); mpz_sub(K,K,u); mpz_mul(u,tB,tB); mpz_mul(u,u,P5[a]); mpz_sub(K,K,u);
  mpz_mul(u,tAB,tAB); mpz_sub(K,K,u); mpz_mul(u,tA,tB); mpz_mul(u,u,tAB); mpz_add(K,K,u);
  if(mpz_sgn(K)==0) return -20.7; long ex; double mant=mpz_get_d_2exp(&ex,K); double L=log(fabs(mant))+ex*log(2.0)-n*log(5.0); return L<-20.7?-20.7:L; }
int main(int argc,char**argv){
  const char*tf=argv[1]; uint64_t W=strtoull(argv[2],0,10); int DMAX=atoi(argv[3]); St s0; parse_state(argv,4,&s0);
  struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
  TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); if(TT.t==MAP_FAILED) die("mmap"); TT.N=stt.st_size/16;
  Tab V; tab_init(&V,1ULL<<24);
  Node*nodes=malloc(sizeof(Node)*(W*(uint64_t)(DMAX+1)+1)); uint64_t nn=0;
  uint64_t h1,h2; fp(&s0,&h1,&h2); tab_ins(&V,h1,h2,0,1); nodes[nn++]=(Node){store(&s0),0xFFFFFFFFu,255,(uint32_t)(s0.l[0]+s0.l[1]),0};
  uint64_t lo=0,hi=1; int bestAC=1<<30,bestSAC=1<<30; uint32_t acNode=0,sacNode=0; int acT=0,sacT=0,acMv=-1,sacMv=-1; St acSt,sacSt;
  Cand*C=malloc(sizeof(Cand)*W*14); St*tmpS=malloc(sizeof(St)*1); (void)tmpS;
  static St cur,nx,sw; St*kids=NULL; uint64_t kcap=0;
  // scratch arena for one depth's children; permanent arena (AR) holds kept states only
  uint8_t*SA=NULL; uint64_t SAn=0,SAcap=0; Tab L; tab_init(&L,1ULL<<23);
  // BEAM_LOOK=1: two-level key (height = best total length reachable in one more move, tiebreak = own length); overrides BEAM_P2
  int LOOK=getenv("BEAM_LOOK")?atoi(getenv("BEAM_LOOK")):0;
  int HP=getenv("BEAM_H")?atoi(getenv("BEAM_H")):0; BAL=getenv("BEAM_BAL")?atof(getenv("BEAM_BAL")):0;
  if(getenv("BEAM_MACROS")){ load_macros(getenv("BEAM_MACROS")); MACW=getenv("BEAM_MACW")?atof(getenv("BEAM_MACW")):1.0; C=realloc(C,sizeof(Cand)*W*(14+NMAC)); fprintf(stderr,"macros: %d\n",NMAC); }
  SHW=getenv("BEAM_SHADOW")?atof(getenv("BEAM_SHADOW")):0.0; if(SHW>0){ if(!getenv("BEAM_SHADOW_FILE")) die("BEAM_SHADOW_FILE"); load_probes(getenv("BEAM_SHADOW_FILE")); }
  LOOPXW=getenv("BEAM_LOOPX")?atof(getenv("BEAM_LOOPX")):0; if(LOOPXW>0) fprintf(stderr,"loopx: w=%.3f (exact)\n",LOOPXW);
  PEELW=getenv("BEAM_PEEL")?atof(getenv("BEAM_PEEL")):0; PEELK=getenv("BEAM_PEELK")?atoi(getenv("BEAM_PEELK")):3; if(PEELW>0) fprintf(stderr,"peel: w=%.3f K=%d\n",PEELW,PEELK);
  RELW=getenv("BEAM_REL")?atof(getenv("BEAM_REL")):0; RELB=getenv("BEAM_RELB")?atof(getenv("BEAM_RELB")):0.5; if(RELW>0) fprintf(stderr,"rel: w=%.3f base=%.2f\n",RELW,RELB);
  REACHW=getenv("BEAM_REACH")?atof(getenv("BEAM_REACH")):0; REACHZ=getenv("BEAM_REACHZ")?atof(getenv("BEAM_REACHZ")):5; if(REACHW>0) fprintf(stderr,"reach: w=%.3f z=%.4f\n",REACHW,REACHZ);
  LOOPW=getenv("BEAM_LOOP")?atof(getenv("BEAM_LOOP")):0; LOOPZ=getenv("BEAM_LOOPZ")?atof(getenv("BEAM_LOOPZ")):5; if(LOOPW>0) fprintf(stderr,"loop: w=%.3f z=%.4f\n",LOOPW,LOOPZ);
  P2M=getenv("BEAM_P2")?atoi(getenv("BEAM_P2")):0; CHAIN=getenv("BEAM_CHAIN")?atoi(getenv("BEAM_CHAIN")):0; if(CHAIN&&P2M!=2) die("BEAM_CHAIN needs BEAM_P2=2"); if(P2M&&P2M!=1&&P2M!=2&&P2M!=3) die("BEAM_P2 must be 1, 2 or 3"); if(getenv("BEAM_P2CUT")) P2CUT=atoi(getenv("BEAM_P2CUT"));
  if(P2M){ nodes[0].p2=p2_of(&s0); fprintf(stderr,"p2: mode %d cut %d start P2=%u P1m=%u\n",P2M,P2CUT,nodes[0].p2,p1m_of(&s0)); }
  QUOTA=getenv("BEAM_QUOTA")?atoi(getenv("BEAM_QUOTA")):0; WHM=getenv("BEAM_WH")?atoi(getenv("BEAM_WH")):0;
  ELITE=getenv("BEAM_ELITE")?strtoull(getenv("BEAM_ELITE"),0,10):0; if(ELITE&&QUOTA<=0) die("BEAM_ELITE needs BEAM_QUOTA");
  CLIMB=getenv("BEAM_CLIMB")?atoi(getenv("BEAM_CLIMB")):0; if(CLIMB) fprintf(stderr,"climb: inverted length key for depths 1..%d\n",CLIMB);
  DUALF=getenv("BEAM_DUAL")?atof(getenv("BEAM_DUAL")):0; if(DUALF<0||DUALF>=1||(DUALF>0&&LOOK)) die("BEAM_DUAL must be in (0,1), not with BEAM_LOOK");
  if(DUALF>0) fprintf(stderr,"dual: first eye %.3f of W by the main key, the rest by the plain key\n",DUALF);
  if(QUOTA<0||(WHM!=0&&WHM!=1)) die("BEAM_QUOTA must be >= 0 and BEAM_WH 0 or 1");
  if(QUOTA>0&&getenv("BEAM_NOV")&&atoi(getenv("BEAM_NOV"))>0) die("BEAM_QUOTA and BEAM_NOV together"); if(WHM&&LOOK) die("BEAM_WH and BEAM_LOOK together"); if(WHM&&P2M==3) die("BEAM_WH and BEAM_P2=3 together");
  int ATL=QUOTA>0||WHM; uint64_t*NCL=NULL; uint16_t*NWH=NULL;
  if(ATL){ NCL=malloc(8*(W*(uint64_t)(DMAX+1)+1)); NWH=malloc(2*(W*(uint64_t)(DMAX+1)+1)); if(!NCL||!NWH) die("atlas alloc");
    NCL[0]=at_class(&s0); NWH[0]=WHM?wh_of(&s0,NCL[0]):0; fprintf(stderr,"atlas: quota %d wh %d start WH=%u\n",QUOTA,WHM,NWH[0]); }
  if(getenv("BEAM_C16")){ C16Hdr ch; c16_load(&CT,getenv("BEAM_C16"),&ch); C16on=1;
    fprintf(stderr,"c16: %s ceiling %d states %llu maxdist %u complete %u\n",getenv("BEAM_C16"),CT.ceil,(unsigned long long)CT.n,ch.maxd,ch.complete); }
  if(getenv("BEAM_TRACE_FILE")){ uint64_t g1,g2; load_trace(getenv("BEAM_TRACE_FILE")); fp(&s0,&g1,&g2); fprintf(stderr,"trace: %d states; start state is index %d\n",NTR,trace_find(g1,g2)); }
  const int KS=LOOK?40:P2M?(((WHM&&P2M==1)||P2M==3)?17:27):(WHM?30:40);   /* key bits below the ranking fields (fingerprint tie-break) */
  static uint32_t trNt[256]; static int trI[256],trT[256]; static uint64_t trKey[256]; int ntrh=0;
  int NOISE=getenv("BEAM_NOISE")?atoi(getenv("BEAM_NOISE")):0; if(HP) NOISE*=16; /* priority is scaled x16 */ uint64_t SEED=getenv("BEAM_SEED")?strtoull(getenv("BEAM_SEED"),0,10)*0xD1B54A32D192ED03ULL:0;
  for(int d=1;d<=DMAX;d++){
    if(d>=bestAC && d+2>=bestSAC) break;
    Node*tmpN=malloc(sizeof(Node)*(hi-lo)*(14+NMAC)+1); uint64_t nt=0; SAn=0; memset(L.t,0,16*L.N); L.n=0;
    uint64_t*tCL=ATL?malloc(8*((hi-lo)*(14+NMAC)+1)):NULL; uint16_t*tWH=ATL?malloc(2*((hi-lo)*(14+NMAC)+1)):NULL; ntrh=0;
    if(ATL&&(!tCL||!tWH)) die("atlas alloc");
    uint64_t*tK2=DUALF>0?malloc(8*((hi-lo)*(14+NMAC)+1)):NULL; if(DUALF>0&&!tK2) die("dual alloc");
    for(uint64_t i=lo;i<hi;i++){ load(nodes[i].off,&cur); double parLX = LOOPXW>0 ? loopx_k(&cur) : 0;
      for(int m=0;m<14+NMAC;m++){ int ctd=nodes[i].td+1; if(m<14) apply(&cur,m,&nx); else { if(!apply_macro(&cur,m-14,&nx)) continue; ctd=nodes[i].td+MACL[m-14]; } fp(&nx,&h1,&h2);
        if(tab_find(&V,h1,h2)>=0){ if(NTR){ int ti=trace_find(h1,h2); if(ti>=0) fprintf(stderr,"TRACE d=%d i=%d visited\n",d,ti); } continue; }
        if(tab_ins(&L,h1,h2,1,1)>=0) continue;
        int t=tab_find(&TT,h1,h2); if(t>=0&&ctd+t<bestAC){ bestAC=ctd+t; acNode=(uint32_t)i; acT=t; acSt=nx; acMv=m; acC16=0; }
        swapst(&nx,&sw); uint64_t g1,g2; fp(&sw,&g1,&g2); int u=tab_find(&TT,g1,g2);
        if(u>=0&&ctd+u+2<bestSAC){ bestSAC=ctd+u+2; sacNode=(uint32_t)i; sacT=u; sacSt=nx; sacMv=m; sacC16=0; }
        if(C16on&&nx.l[0]+nx.l[1]<=CT.ceil){ c16look++;   /* BEAM_C16: ceiling finish (T wins ties) */
          int c=c16_lookup(&CT,&nx); if(c>=0&&ctd+c<bestAC){ bestAC=ctd+c; acNode=(uint32_t)i; acT=c; acSt=nx; acMv=m; acC16=1; c16ac++;
            fprintf(stderr,"c16: AC %d at d=%d (child length %d, ceiling distance %d)\n",bestAC,d,nx.l[0]+nx.l[1],c); }
          int c2=c16_lookup(&CT,&sw); if(c2>=0&&ctd+c2+2<bestSAC){ bestSAC=ctd+c2+2; sacNode=(uint32_t)i; sacT=c2; sacSt=nx; sacMv=m; sacC16=1; c16sac++;
            fprintf(stderr,"c16: SAC %d at d=%d (swapped child length %d, ceiling distance %d)\n",bestSAC,d,nx.l[0]+nx.l[1],c2); } }
        uint32_t len=nx.l[0]+nx.l[1]; uint64_t need=4+len;
        if(SAn+need>SAcap){ SAcap=SAcap?SAcap*2:(1ULL<<26); while(SAn+need>SAcap) SAcap*=2; SA=realloc(SA,SAcap); if(!SA) die("scratch"); }
        uint8_t*q=SA+SAn; q[0]=nx.l[0]&255; q[1]=nx.l[0]>>8; q[2]=nx.l[1]&255; q[3]=nx.l[1]>>8; memcpy(q+4,nx.w[0],nx.l[0]); memcpy(q+4+nx.l[0],nx.w[1],nx.l[1]);
        uint16_t cp2=0; if(P2M){ if((m>=2&&m<=5)||m>=14) cp2=p2_of(&nx); else { cp2=nodes[i].p2; P2inh++;
#ifdef P2_CHECK_INHERIT
          { static char a0[MAXW+1],a1[MAXW+1],A[MAXW+1],B[MAXW+1]; static uint64_t nchk,bad; p2_enc(nx.w[0],nx.l[0],a0); p2_enc(nx.w[1],nx.l[1],a1);
            int na=p2_cycred(a0,nx.l[0],A),nb=p2_cycred(a1,nx.l[1],B),v=(na>P2W||nb>P2W||!na||!nb)?P2SAT:p2_eval(A,na,B,nb,P2CUT); if(v<0||v>P2SAT) v=P2SAT;
            nchk++; if(v!=cp2&&++bad<=20) fprintf(stderr,"P2 inherit mismatch m=%d parent %u child %d\n",m,cp2,v);
            if((nchk&0xFFFFF)==0) fprintf(stderr,"P2 inherit check: %llu uncached recomputations, %llu mismatches\n",(unsigned long long)nchk,(unsigned long long)bad); }
#endif
        } }
        if(ATL){ if((m>=2&&m<=5)||m>=14){ tCL[nt]=at_class(&nx); tWH[nt]=WHM?wh_of(&nx,tCL[nt]):0; } else { tCL[nt]=NCL[i]; tWH[nt]=NWH[i]; } }
        tmpN[nt]=(Node){SAn,(uint32_t)i,(uint8_t)m,len,(uint16_t)ctd,cp2}; SAn+=need;
        // BEAM_NOISE=n, BEAM_SEED=s: add a seeded pseudo-random 0..n to the length key (route diversity)
        uint32_t klen=HP?hprio(&nx):len; if(SHW>0) klen+=(uint32_t)(SHW*(HP?16.0:1.0)*shadow(&nx)+0.5); if(NMAC) klen+=(uint32_t)(MACW*(HP?16.0:1.0)*(ctd-d)+0.5); if(NOISE){ uint64_t z=(h1^SEED)*0x9E3779B97F4A7C15ULL; z^=z>>29; klen+=(uint32_t)(z%(uint64_t)(NOISE+1)); }
        if(LOOPW>0){ double lk=loop_k(&nx); klen=(HP?klen:16*len)+(uint32_t)(16*LOOPW*(lk+25)+0.5); }
        if(REACHW>0){ if(LOOPW<=0&&!HP) klen=16*len; klen+=(uint32_t)(16*REACHW*reach_k(&nx)+0.5); }
        if(RELW>0){ if(LOOPW<=0&&REACHW<=0&&!HP) klen=16*len; klen+=(uint32_t)(16*RELW*rel_k(&nx)+0.5); }
        if(PEELW>0){ if(LOOPW<=0&&REACHW<=0&&RELW<=0&&!HP) klen=16*len; klen+=(uint32_t)(16*PEELW*peel_k(&nx)+0.5); }
        if(LOOPXW>0){ if(LOOPW<=0&&REACHW<=0&&RELW<=0&&PEELW<=0&&!HP) klen=16*len; double lx=(m<=5)?parLX:loopx_k(&nx); klen+=(uint32_t)(16*LOOPXW*(lx+25)+0.5); }
        uint64_t key=((uint64_t)klen<<40)|((h1^SEED)>>24); if(tK2) tK2[nt]=key;   /* BEAM_DUAL: the plain key of the second eye */
        if(WHM) key=((uint64_t)klen<<40)|((uint64_t)tWH[nt]<<30)|((h1^SEED)>>34);   /* BEAM_WH: klen | WH (10 bits) | 30 fp bits */
        // BEAM_P2: P2 (9 bits) | P1m (10 bits, mode 1 only) | existing klen (18 bits, saturated) | 27 fingerprint bits
        if(P2M){ uint64_t kl=klen>0x3FFFFu?0x3FFFFu:klen, pm=P2M!=2?p1m_of(&nx):0;
          key=((uint64_t)cp2<<55)|(pm<<45)|(kl<<27)|((h1^SEED)>>37);
          if(CHAIN&&P2M==2&&!WHM) key=((uint64_t)cp2<<55)|(kl<<37)|((uint64_t)chain_q(&nx)<<27)|((h1^SEED)>>37);  /* BEAM_CHAIN: P2 | klen | chain | 27 fp */
          if(P2M==3) key=((uint64_t)cp2<<55)|((uint64_t)comm_len(&nx)<<45)|(pm<<35)|(kl<<17)|((h1^SEED)>>47);  /* P2 | comm_len | P1m | klen | 17 fp */
          if(WHM){ uint64_t wv=tWH[nt]; key=P2M==2?(((uint64_t)cp2<<55)|(wv<<45)|(kl<<27)|((h1^SEED)>>37))      /* P2 | WH | klen | 27 fp */
                                                :(((uint64_t)cp2<<55)|(wv<<45)|(pm<<35)|(kl<<17)|((h1^SEED)>>47)); } }  /* P2 | WH | P1m | klen | 17 fp */
        if(CLIMB&&d<=CLIMB){ uint32_t kc=klen>=0xFFFFFu?0:0xFFFFFu-klen; key=((uint64_t)kc<<40)|((h1^SEED)>>24); if(tK2) tK2[nt]=key; }
        if(LOOK){ uint32_t best=len; St y; for(int m2=0;m2<14;m2++){ apply(&nx,m2,&y); uint32_t l2=y.l[0]+y.l[1]; if(l2<best) best=l2; }
          key=((uint64_t)best<<52)|((uint64_t)(len&4095)<<40)|(h1>>24); }
        if(NTR){ int ti=trace_find(h1,h2); if(ti>=0&&ntrh<256){ trNt[ntrh]=(uint32_t)nt; trI[ntrh]=ti; trT[ntrh]=t; trKey[ntrh]=key; ntrh++; } }
        C[nt]=(Cand){key,(uint32_t)nt}; nt++; } }
    uint64_t keep=nt<W?nt:W; static int64_t trRank[256],trLo[256],trHi[256],trQ[256]; static int trAdm[256]; uint64_t cutK1=0,cutW=0,k1tr=0;
    for(int j=0;j<ntrh;j++){ trRank[j]=trLo[j]=trHi[j]=trQ[j]=-1; trAdm[j]=-1; }
    if(nt>W){ qsort(C,nt,sizeof(Cand),cmpc);
      if(ntrh){ double DV=getenv("BEAM_DIV")?atof(getenv("BEAM_DIV")):1.0; k1tr=(uint64_t)(W*DV); if(k1tr>W) k1tr=W; cutK1=C[k1tr?k1tr-1:0].key; cutW=C[W-1].key;
        for(int j=0;j<ntrh;j++){ uint64_t p=0; while(p<nt&&C[p].idx!=trNt[j]) p++; trRank[j]=(int64_t)p; uint64_t hk=C[p].key>>KS,a=p,b=p+1;
          while(a>0&&(C[a-1].key>>KS)==hk) a--; while(b<nt&&(C[b].key>>KS)==hk) b++; trLo[j]=(int64_t)a; trHi[j]=(int64_t)b; } }
      uint64_t WS=DUALF>0?(uint64_t)(DUALF*W):W;   /* BEAM_DUAL: the first eye fills WS slots; WS == W otherwise */
      if(QUOTA>0){ // BEAM_QUOTA: admit in key order while the class has < q survivors; DIV samples its tail from the admitted list
        double DIV=getenv("BEAM_DIV")?atof(getenv("BEAM_DIV")):1.0; uint64_t k1=(uint64_t)(WS*DIV); if(k1>WS) k1=WS;
        static uint64_t*qk; static uint32_t*qc; static uint64_t qcap; uint64_t hs=1; while(hs<2*nt) hs<<=1;
        if(hs>qcap){ qk=realloc(qk,8*hs); qc=realloc(qc,4*hs); if(!qk||!qc) die("quota alloc"); qcap=hs; } memset(qk,0,8*hs);
        uint32_t*A=malloc(4*nt),*R=malloc(4*nt); uint64_t nA=0,nR=0,ncls=0; if(!A||!R) die("quota alloc");
        for(uint64_t q=0;q<nt;q++){ if(q<ELITE){ A[nA++]=(uint32_t)q; continue; } uint64_t c=tCL[C[q].idx],sl=fmix_a(c)&(hs-1); while(qk[sl]&&qk[sl]!=c) sl=(sl+1)&(hs-1);
          if(!qk[sl]){ qk[sl]=c; qc[sl]=0; ncls++; } if(qc[sl]<(uint32_t)QUOTA){ qc[sl]++; A[nA++]=(uint32_t)q; } else R[nR++]=(uint32_t)q; }
        for(int j=0;j<ntrh;j++){ for(uint64_t q=0;q<nA;q++) if(A[q]==(uint32_t)trRank[j]){ trAdm[j]=1; trQ[j]=(int64_t)q; break; }
          if(trAdm[j]<0) for(uint64_t q=0;q<nR;q++) if(R[q]==(uint32_t)trRank[j]){ trAdm[j]=0; trQ[j]=(int64_t)q; break; } }
        Cand*K=malloc(sizeof(Cand)*WS); uint64_t kk=0; if(!K) die("quota alloc");
        if(nA>=WS){ for(uint64_t q=0;q<k1;q++) K[kk++]=C[A[q]];
          if(k1<WS){ uint64_t rest=nA-k1,need=WS-k1; for(uint64_t q=0;q<need;q++) K[kk++]=C[A[k1+(uint64_t)((double)q*rest/need)]]; } }
        else { for(uint64_t q=0;q<nA;q++) K[kk++]=C[A[q]]; for(uint64_t q=0;q<nR&&kk<WS;q++) K[kk++]=C[R[q]]; }
        memcpy(C,K,sizeof(Cand)*kk); free(K); free(A); free(R);
        if(d%10==0) fprintf(stderr,"quota d=%d classes=%llu admitted=%llu\n",d,(unsigned long long)ncls,(unsigned long long)nA); } else {
      // diversity ("zag"): keep the best DIV fraction by length, fill the rest evenly from the longer remainder
      double DIV=getenv("BEAM_DIV")?atof(getenv("BEAM_DIV")):1.0; uint64_t k1=(uint64_t)(WS*DIV); if(k1>WS) k1=WS;
      if(k1<WS){ uint64_t rest=nt-k1, need=WS-k1; for(uint64_t q=0;q<need;q++){ uint64_t src=k1+(uint64_t)((double)q*rest/need); C[k1+q]=C[src]; } }
      // novelty quota: at most NOV states per shape bucket (lengths + exponent sums), rest filled in length order
      int NOV=getenv("BEAM_NOV")?atoi(getenv("BEAM_NOV")):0;
      if(NOV>0){ static uint16_t cnt[1<<20]; memset(cnt,0,sizeof cnt); Cand*K=malloc(sizeof(Cand)*WS); uint8_t*used=calloc(nt,1); uint64_t kk=0;
        for(uint64_t q=0;q<nt&&kk<WS;q++){ Node x=tmpN[C[q].idx]; uint8_t*z=SA+x.off; int l0=z[0]|(z[1]<<8), l1=z[2]|(z[3]<<8); int e[4]={0,0,0,0};
          for(int t=0;t<l0;t++){ uint8_t c=z[4+t]; e[(c>>1)]+=(c&1)?-1:1; } for(int t=0;t<l1;t++){ uint8_t c=z[4+l0+t]; e[2+(c>>1)]+=(c&1)?-1:1; }
          uint64_t b=((uint64_t)l0*1315423911ULL)^((uint64_t)l1*2654435761ULL)^((uint64_t)(e[0]+64)<<8)^((uint64_t)(e[1]+64)<<16)^((uint64_t)(e[2]+64)<<24)^((uint64_t)(e[3]+64)<<32);
          b=(b*0x9E3779B97F4A7C15ULL)>>44; if(cnt[b]<NOV){ cnt[b]++; K[kk++]=C[q]; used[q]=1; } }
        for(uint64_t q=0;q<nt&&kk<WS;q++) if(!used[q]) K[kk++]=C[q];
        memcpy(C,K,sizeof(Cand)*kk); free(K); free(used); } }
      if(DUALF>0){ // BEAM_DUAL second eye: best W-WS by the plain key among the candidates the first eye did not take
        uint8_t*taken=calloc(nt,1); if(!taken) die("dual alloc"); for(uint64_t k=0;k<WS;k++) taken[C[k].idx]=1;
        Cand*H=malloc(sizeof(Cand)*nt); uint64_t nh=0; if(!H) die("dual alloc");
        for(uint64_t t=0;t<nt;t++) if(!taken[t]) H[nh++]=(Cand){tK2[t],(uint32_t)t};
        qsort(H,nh,sizeof(Cand),cmpc); uint64_t W2=W-WS; double DIV=getenv("BEAM_DIV")?atof(getenv("BEAM_DIV")):1.0;
        uint64_t k2=(uint64_t)(W2*DIV); if(k2>W2) k2=W2; if(k2>nh) k2=nh;
        for(uint64_t q=0;q<k2;q++) C[WS+q]=H[q];
        if(k2<W2&&nh>k2){ uint64_t rest=nh-k2,need=W2-k2; if(need>rest) need=rest; for(uint64_t q=0;q<need;q++) C[WS+k2+q]=H[k2+(uint64_t)((double)q*rest/need)]; keep=WS+k2+need; }
        else keep=WS+k2;
        if(d%10==0) fprintf(stderr,"dual d=%d first=%llu second=%llu of %llu left\n",d,(unsigned long long)WS,(unsigned long long)(keep-WS),(unsigned long long)nh);
        free(H); free(taken); } }
    for(int j=0;j<ntrh;j++){ int64_t pos=-1; for(uint64_t k=0;k<keep;k++) if(C[k].idx==trNt[j]){ pos=(int64_t)k; break; }
      uint16_t tw=ATL?tWH[trNt[j]]:0;
      fprintf(stderr,"TRACE d=%d i=%d t=%d kept=%d pos=%lld rank=%lld nt=%llu W=%llu k1=%llu tie_lo=%lld tie_hi=%lld key=%016llx cutk1=%016llx cutW=%016llx ks=%d adm=%d qpos=%lld p2=%u wh=%u len=%u\n",
        d,trI[j],trT[j],pos>=0,(long long)pos,(long long)trRank[j],(unsigned long long)nt,(unsigned long long)W,(unsigned long long)k1tr,(long long)trLo[j],(long long)trHi[j],
        (unsigned long long)trKey[j],(unsigned long long)cutK1,(unsigned long long)cutW,KS,trAdm[j],(long long)trQ[j],tmpN[trNt[j]].p2,tw,tmpN[trNt[j]].len); }
    lo=nn; for(uint64_t k=0;k<keep;k++){ Node x=tmpN[C[k].idx]; uint8_t*q=SA+x.off; St t2; t2.l[0]=q[0]|(q[1]<<8); t2.l[1]=q[2]|(q[3]<<8);
        memcpy(t2.w[0],q+4,t2.l[0]); memcpy(t2.w[1],q+4+t2.l[0],t2.l[1]); x.off=store(&t2); fp(&t2,&h1,&h2); tab_ins(&V,h1,h2,(d>15?15:d),1); if(ATL){ NCL[nn]=tCL[C[k].idx]; NWH[nn]=tWH[C[k].idx]; } nodes[nn++]=x; }
    hi=nn; free(tmpN); free(tCL); free(tWH); free(tK2);
    uint32_t mn=~0u,mx=0; for(uint64_t i=lo;i<hi;i++){ if(nodes[i].len<mn) mn=nodes[i].len; if(nodes[i].len>mx) mx=nodes[i].len; }
    if(d%10==0||bestAC<(1<<30)) fprintf(stderr,"d=%d gen=%llu kept=%llu len[%u..%u] bestAC=%d bestSAC=%d arena=%lluMB\n",d,(unsigned long long)nt,(unsigned long long)keep,mn,mx,bestAC<(1<<30)?bestAC:-1,bestSAC<(1<<30)?bestSAC:-1,(unsigned long long)(ARn>>20));
    if(hi==lo) break; }
  if(WHM) fprintf(stderr,"wh: calls %llu (cache hits %llu, saturated %llu), %.1f s in WH\n",(unsigned long long)WHcalls,(unsigned long long)WHhits,(unsigned long long)WHsat,WHtime);
  if(P2M) fprintf(stderr,"p2: computed %llu (cache hits %llu, saturated %llu) inherited %llu, %.1f s in P2\n",(unsigned long long)P2calls,(unsigned long long)P2hits,(unsigned long long)P2satn,(unsigned long long)P2inh,P2time);
  // rebuild: prefix via parent chain, then exact finish through T_9
  if(C16on) fprintf(stderr,"c16: %llu lookups, %llu AC and %llu SAC improvements; final AC finish %s, SAC finish %s\n",(unsigned long long)c16look,
    (unsigned long long)c16ac,(unsigned long long)c16sac,bestAC<(1<<30)?(acC16?"C16":"T"):"none",bestSAC<(1<<30)?(sacC16?"C16":"T"):"none");
  for(int which=0;which<2;which++){ int best=which?bestSAC:bestAC; if(best>=(1<<30)){ printf("%s NONE\n",which?"SAC":"AC"); continue; }
    uint32_t pn=which?sacNode:acNode; St fin=which?sacSt:acSt; int t=which?sacT:acT;
    int pre[4096],np=0; // moves from start to parent node, then the move to fin
    // find the move from parent to fin
    load(nodes[pn].off,&cur); int mfin=which?sacMv:acMv;
    uint32_t q=pn; while(nodes[q].par!=0xFFFFFFFFu){ pre[np++]=nodes[q].mv; q=nodes[q].par; }
    int path[8192],L=0; for(int i=np-1;i>=-1;i--){ int mv=i>=0?pre[i]:mfin; if(mv<14) path[L++]=mv; else for(int j=0;j<MACL[mv-14];j++) path[L++]=MAC[mv-14][j]; }
    St c=fin; if(which) swapst(&fin,&c);
    int useC=which?sacC16:acC16;   /* BEAM_C16: descend in the ceiling table instead of T */
    for(int k=t;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&nx); int dd; if(useC) dd=c16_lookup(&CT,&nx); else { fp(&nx,&h1,&h2); dd=tab_find(&TT,h1,h2); } if(dd==k-1){ path[L++]=which?PI[m]:m; c=nx; ok=1; break; } } if(!ok){ printf("REBUILD_FAIL\n"); break; } }
    if(which){ path[L++]=15; path[L++]=15; }
    printf("%s %d PATH",which?"SAC":"AC",L); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); }
  return 0; }
