// acc_c16: ceiling finish table ("C16"). BFS from (x,y) over the states of total relator length <= CEIL (default 16),
// moving only through such states, layer by layer until closure (or a state/time budget), storing each state's BFS
// distance inside the ceiling graph. Every move has an inverse move (INV[] in acc_opt.c), so this distance is the
// distance *to* (x,y) inside the ceiling: an upper bound on the true AC distance. acc_beam's BEAM_C16=file finishes
// paths from any child that is short but farther than T8's radius from (x,y). Rival idea: nahom §2.1
// (research/acc/live/RIVAL_METHODS_20260928.md). Table layout and exact packed keys: c16_table.inc.
// Kernel (apply, INV, moves 0..13) is acc_opt.c = the verified ac-r2-v1 kernel.
//
// usage:
//   acc_c16 build OUT [CEIL=16] [NSLOTS=268435456] [BUDGET=0.88*NSLOTS]
//       env C16_TMAX = wall-clock seconds before stopping between layers (default 3600).
//       Prints per-layer counts, the max distance and a by-length histogram; compacts to load ~0.7 and writes OUT.
//   acc_c16 sample TFILE COUNT SEED OUT
//       Picks COUNT states (per-distance reservoirs of up to 8 each, the rest uniform), checks that every in-ceiling
//       neighbour is in the table with |d(nbr)-d| <= 1 (BFS consistency + closure), rebuilds the greedy descent
//       (first move to an in-ceiling neighbour at distance d-1) and writes "d l0 w.. l1 w.. | moves" per state.
//       The descent is then replayed by c16_verify_sample.py with the official verifier.
//   acc_c16 lookup TFILE l0 w.. l1 w..      prints the table distance (or -1) and the greedy descent
// build: gcc -O3 -march=native -o acc_c16 acc_c16.c
#define ACC_NO_MAIN
#include "acc_opt.c"
#include "c16_table.inc"

static uint64_t rng_s=0x243F6A8885A308D3ULL;
static inline uint64_t rng(void){ rng_s+=0x9E3779B97F4A7C15ULL; uint64_t z=rng_s; z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL; z=(z^(z>>27))*0x94d049bb133111ebULL; return z^(z>>31); }

static int build(int argc,char**argv){
  const char*out=argv[2]; int CEIL=argc>3?atoi(argv[3]):16; uint64_t NS=argc>4?strtoull(argv[4],0,10):(1ULL<<28);
  uint64_t BUD=argc>5?strtoull(argv[5],0,10):(uint64_t)(0.88*(double)NS);
  double TMAX=getenv("C16_TMAX")?atof(getenv("C16_TMAX")):3600.0;
  if(CEIL<2||CEIL>C16_MAXCEIL) die("CEIL must be in 2..22");
  if(BUD>(uint64_t)(0.9*(double)NS)) BUD=(uint64_t)(0.9*(double)NS);
  double t0=now(); C16 T; c16_alloc(&T,NS,CEIL);
  St g; g.l[0]=1; g.l[1]=1; g.w[0][0]=0; g.w[1][0]=2; c16_ins(&T,c16_pack(&g),0);
  static St cur,nx; uint64_t cnt[256]; memset(cnt,0,sizeof cnt); cnt[0]=1; int maxd=0,complete=0;
  printf("C16 build CEIL=%d NSLOTS=%llu (%.2f GB) BUDGET=%llu TMAX=%.0fs\n",CEIL,(unsigned long long)NS,8.0*NS/1e9,(unsigned long long)BUD,TMAX);
  printf("C16 layer 0: 1  cumulative 1\n"); fflush(stdout);
  for(int d=1;d<256;d++){ double t1=now(); uint64_t c=0,exp=0;
    for(uint64_t i=0;i<T.N;i++){ uint64_t a=T.t[i]; if(!a||(int)((a>>C16_DSH)&255)!=d-1) continue; exp++;
      c16_unpack(a&C16_KEY,&cur);
      for(int m=0;m<14;m++){ apply(&cur,m,&nx); if(nx.l[0]+nx.l[1]>CEIL) continue;
        if(c16_ins(&T,c16_pack(&nx),d)<0) c++; }
      if(T.n>=BUD) break; }
    cnt[d]=c; if(c) maxd=d;
    printf("C16 layer %d: %llu  cumulative %llu  (expanded %llu, %.1fs, load %.3f)\n",d,(unsigned long long)c,(unsigned long long)T.n,
      (unsigned long long)exp,now()-t1,(double)T.n/T.N); fflush(stdout);
    if(!c){ complete=1; break; }
    if(T.n>=BUD){ printf("C16 STOP state budget %llu reached inside layer %d (table incomplete)\n",(unsigned long long)BUD,d); break; }
    if(now()-t0>TMAX){ printf("C16 STOP time budget %.0fs reached after layer %d (table incomplete)\n",TMAX,d); break; } }
  uint64_t bylen[2*C16_MAXCEIL+2]; memset(bylen,0,sizeof bylen);
  for(uint64_t i=0;i<T.N;i++) if(T.t[i]) bylen[(T.t[i]&31)+((T.t[i]>>5)&31)]++;
  for(int L=0;L<=CEIL;L++) if(bylen[L]) printf("C16 total length %d: %llu states\n",L,(unsigned long long)bylen[L]);
  printf("C16 BFS %s: states=%llu maxdist=%d wall=%.1fs\n",complete?"CLOSED":"INCOMPLETE",(unsigned long long)T.n,maxd,now()-t0); fflush(stdout);
  // compact to load ~0.70 and write
  uint64_t N2=(uint64_t)((double)T.n/0.70)+1024; C16 U; c16_alloc(&U,N2,CEIL);
  for(uint64_t i=0;i<T.N;i++){ uint64_t a=T.t[i]; if(a) c16_ins(&U,a&C16_KEY,(int)((a>>C16_DSH)&255)); }
  if(U.n!=T.n) die("compaction count"); c16_free(&T);
  c16_save(&U,out,maxd,complete);
  printf("C16 WROTE %s slots=%llu (%.2f GB) states=%llu CEIL=%d maxdist=%d complete=%d total_wall=%.1fs\n",out,(unsigned long long)U.N,
    (8.0*U.N+64)/1e9,(unsigned long long)U.n,CEIL,maxd,complete,now()-t0);
  return 0; }

static void prst(FILE*f,const St*s){ for(int j=0;j<2;j++){ fprintf(f," %d",s->l[j]); for(int i=0;i<s->l[j];i++) fprintf(f," %d",s->w[j][i]); } }

static int sample(int argc,char**argv){
  C16 T; C16Hdr h; c16_load(&T,argv[2],&h); int COUNT=atoi(argv[3]); rng_s^=strtoull(argv[4],0,10)*0xD1B54A32D192ED03ULL;
  FILE*o=fopen(argv[5],"w"); if(!o) die("sample out");
  enum{ PER=8 }; static uint64_t res[256][PER]; static uint64_t seen[256]; uint64_t*uni=malloc(8*(size_t)COUNT); uint64_t nseen=0;
  for(uint64_t i=0;i<T.N;i++){ uint64_t a=T.t[i]; if(!a) continue; int d=(int)((a>>C16_DSH)&255);
    if(seen[d]<PER) res[d][seen[d]]=a; else { uint64_t r=rng()%(seen[d]+1); if(r<PER) res[d][r]=a; } seen[d]++;
    if(nseen<(uint64_t)COUNT) uni[nseen]=a; else { uint64_t r=rng()%(nseen+1); if(r<(uint64_t)COUNT) uni[r]=a; } nseen++; }
  uint64_t*pick=malloc(8*(size_t)COUNT); int np=0;
  for(int d=0;d<256&&np<COUNT;d++) for(uint64_t k=0;k<seen[d]&&k<PER&&np<COUNT;k++) pick[np++]=res[d][k];
  int nstrat=np; for(int k=0;np<COUNT;k++){ int dup=0; for(int q=0;q<nstrat;q++) if(pick[q]==uni[k]) dup=1; if(!dup) pick[np++]=uni[k]; }
  static St s,n; int path[256]; uint64_t nbrs=0,nin=0,bad_close=0,bad_diff=0,bad_desc=0; int hist[256]; memset(hist,0,sizeof hist);
  for(int q=0;q<np;q++){ uint64_t a=pick[q]; int d=(int)((a>>C16_DSH)&255); c16_unpack(a&C16_KEY,&s); hist[d]++;
    for(int m=0;m<14;m++){ apply(&s,m,&n); if(n.l[0]+n.l[1]>T.ceil) continue; nbrs++; int e=c16_lookup(&T,&n);
      if(e<0){ bad_close++; continue; } nin++; if(e<d-1||e>d+1) bad_diff++; }
    int r=c16_descend(&T,&s,d,path); if(r){ bad_desc++; continue; }
    fprintf(o,"%d",d); prst(o,&s); fprintf(o," |"); for(int i=0;i<d;i++) fprintf(o," %d",path[i]); fprintf(o,"\n"); }
  fclose(o);
  printf("C16 SAMPLE n=%d (stratified %d, uniform %d) table states=%llu CEIL=%u maxdist=%u complete=%u\n",np,nstrat,np-nstrat,
    (unsigned long long)T.n,h.ceil,h.maxd,h.complete);
  printf("C16 SAMPLE in-ceiling neighbours=%llu in-table=%llu missing(closure fail)=%llu |dd|>1=%llu descent_fail=%llu\n",
    (unsigned long long)nbrs,(unsigned long long)nin,(unsigned long long)bad_close,(unsigned long long)bad_diff,(unsigned long long)bad_desc);
  printf("C16 SAMPLE distance histogram:"); for(int d=0;d<256;d++) if(hist[d]) printf(" %d:%d",d,hist[d]); printf("\n");
  printf("C16 TABLE distance counts:"); for(int d=0;d<256;d++) if(seen[d]) printf(" %d:%llu",d,(unsigned long long)seen[d]); printf("\n");
  return (bad_close||bad_diff||bad_desc)?1:0; }

static int lookup(int argc,char**argv){ (void)argc; C16 T; c16_load(&T,argv[2],NULL); static St s; parse_state(argv,3,&s);
  int d=c16_lookup(&T,&s); printf("C16 distance %d\n",d); if(d>0){ int path[256]; int r=c16_descend(&T,&s,d,path);
    printf("C16 descent rc=%d PATH",r); for(int i=0;i<d;i++) printf(" %d",path[i]); printf("\n"); } return 0; }

int main(int argc,char**argv){
  if(argc>=3&&!strcmp(argv[1],"build")) return build(argc,argv);
  if(argc>=6&&!strcmp(argv[1],"sample")) return sample(argc,argv);
  if(argc>=5&&!strcmp(argv[1],"lookup")) return lookup(argc,argv);
  fprintf(stderr,"usage: acc_c16 build OUT [CEIL] [NSLOTS] [BUDGET] | sample TFILE COUNT SEED OUT | lookup TFILE l0 w.. l1 w..\n"); return 2; }
