// Beam search + exact finish. Forward beam from the start keeps the W states of smallest total
// relator length per depth (ties broken by fingerprint), deduplicated across all depths. Every
// generated state is looked up in T_9 (distance to (x,y)) and, via the generator swap, in T_9
// again (distance to (y,x)). A hit at depth d with ball distance t gives an AC path d+t (to (x,y))
// or a Stable AC path d+t+2 (via (y,x)). Kernel/fingerprint/table shared with acc_opt.c.
// usage: acc_beam TFILE W DMAX l0 w.. l1 w..
// Options (env): BEAM_H, BEAM_BAL, BEAM_DIV, BEAM_NOV, BEAM_NOISE, BEAM_SEED, BEAM_LOOK, BEAM_SHADOW(+_FILE),
// BEAM_MACROS(+BEAM_MACW), BEAM_P2 (+BEAM_P2CUT); see the comments at each. All off by default.
// build: gcc -O3 -march=native -o acc_beam acc_beam.c -lm
#define ACC_NO_MAIN
#include "acc_opt.c"
#include <math.h>
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
// ---- P2 end ----
static int cmpc(const void*a,const void*b){ uint64_t x=((Cand*)a)->key,y=((Cand*)b)->key; return x<y?-1:x>y; }
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
  P2M=getenv("BEAM_P2")?atoi(getenv("BEAM_P2")):0; if(P2M&&P2M!=1&&P2M!=2) die("BEAM_P2 must be 1 or 2"); if(getenv("BEAM_P2CUT")) P2CUT=atoi(getenv("BEAM_P2CUT"));
  if(P2M){ nodes[0].p2=p2_of(&s0); fprintf(stderr,"p2: mode %d cut %d start P2=%u P1m=%u\n",P2M,P2CUT,nodes[0].p2,p1m_of(&s0)); }
  int NOISE=getenv("BEAM_NOISE")?atoi(getenv("BEAM_NOISE")):0; if(HP) NOISE*=16; /* priority is scaled x16 */ uint64_t SEED=getenv("BEAM_SEED")?strtoull(getenv("BEAM_SEED"),0,10)*0xD1B54A32D192ED03ULL:0;
  for(int d=1;d<=DMAX;d++){
    if(d>=bestAC && d+2>=bestSAC) break;
    Node*tmpN=malloc(sizeof(Node)*(hi-lo)*(14+NMAC)+1); uint64_t nt=0; SAn=0; memset(L.t,0,16*L.N); L.n=0;
    for(uint64_t i=lo;i<hi;i++){ load(nodes[i].off,&cur);
      for(int m=0;m<14+NMAC;m++){ int ctd=nodes[i].td+1; if(m<14) apply(&cur,m,&nx); else { if(!apply_macro(&cur,m-14,&nx)) continue; ctd=nodes[i].td+MACL[m-14]; } fp(&nx,&h1,&h2);
        if(tab_find(&V,h1,h2)>=0) continue; if(tab_ins(&L,h1,h2,1,1)>=0) continue;
        int t=tab_find(&TT,h1,h2); if(t>=0&&ctd+t<bestAC){ bestAC=ctd+t; acNode=(uint32_t)i; acT=t; acSt=nx; acMv=m; }
        swapst(&nx,&sw); uint64_t g1,g2; fp(&sw,&g1,&g2); int u=tab_find(&TT,g1,g2);
        if(u>=0&&ctd+u+2<bestSAC){ bestSAC=ctd+u+2; sacNode=(uint32_t)i; sacT=u; sacSt=nx; sacMv=m; }
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
        tmpN[nt]=(Node){SAn,(uint32_t)i,(uint8_t)m,len,(uint16_t)ctd,cp2}; SAn+=need;
        // BEAM_NOISE=n, BEAM_SEED=s: add a seeded pseudo-random 0..n to the length key (route diversity)
        uint32_t klen=HP?hprio(&nx):len; if(SHW>0) klen+=(uint32_t)(SHW*(HP?16.0:1.0)*shadow(&nx)+0.5); if(NMAC) klen+=(uint32_t)(MACW*(HP?16.0:1.0)*(ctd-d)+0.5); if(NOISE){ uint64_t z=(h1^SEED)*0x9E3779B97F4A7C15ULL; z^=z>>29; klen+=(uint32_t)(z%(uint64_t)(NOISE+1)); }
        uint64_t key=((uint64_t)klen<<40)|((h1^SEED)>>24);
        // BEAM_P2: P2 (9 bits) | P1m (10 bits, mode 1 only) | existing klen (18 bits, saturated) | 27 fingerprint bits
        if(P2M){ uint64_t kl=klen>0x3FFFFu?0x3FFFFu:klen, pm=P2M==1?p1m_of(&nx):0;
          key=((uint64_t)cp2<<55)|(pm<<45)|(kl<<27)|((h1^SEED)>>37); }
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
  if(P2M) fprintf(stderr,"p2: computed %llu (cache hits %llu, saturated %llu) inherited %llu, %.1f s in P2\n",(unsigned long long)P2calls,(unsigned long long)P2hits,(unsigned long long)P2satn,(unsigned long long)P2inh,P2time);
  // rebuild: prefix via parent chain, then exact finish through T_9
  for(int which=0;which<2;which++){ int best=which?bestSAC:bestAC; if(best>=(1<<30)){ printf("%s NONE\n",which?"SAC":"AC"); continue; }
    uint32_t pn=which?sacNode:acNode; St fin=which?sacSt:acSt; int t=which?sacT:acT;
    int pre[4096],np=0; // moves from start to parent node, then the move to fin
    // find the move from parent to fin
    load(nodes[pn].off,&cur); int mfin=which?sacMv:acMv;
    uint32_t q=pn; while(nodes[q].par!=0xFFFFFFFFu){ pre[np++]=nodes[q].mv; q=nodes[q].par; }
    int path[8192],L=0; for(int i=np-1;i>=-1;i--){ int mv=i>=0?pre[i]:mfin; if(mv<14) path[L++]=mv; else for(int j=0;j<MACL[mv-14];j++) path[L++]=MAC[mv-14][j]; }
    St c=fin; if(which) swapst(&fin,&c);
    for(int k=t;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&nx); fp(&nx,&h1,&h2); if(tab_find(&TT,h1,h2)==k-1){ path[L++]=which?PI[m]:m; c=nx; ok=1; break; } } if(!ok){ printf("REBUILD_FAIL\n"); break; } }
    if(which){ path[L++]=15; path[L++]=15; }
    printf("%s %d PATH",which?"SAC":"AC",L); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); }
  return 0; }
