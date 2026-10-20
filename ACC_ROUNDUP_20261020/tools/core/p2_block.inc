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
