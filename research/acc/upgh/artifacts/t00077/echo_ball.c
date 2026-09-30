// echo_ball.c -- C port of research/acc/optimality/build_echo.py's ball step (same semantics, same output format).
// Input  SRC: lines "b l0 w.. l1 w.." = unique route states (min remaining b over all verified routes), letter codes 0..3.
// For every source: BFS radius r=min(R, MAXREM-b) (states new within that source's own ball, first discovery = shortest k),
// rem = b+k; global best[x] = min rem (first source wins ties, like the Python '<'); keep 10 <= rem <= MAXREM.
// Output OUT.echo ("id rem l0 w.. l1 w..") and OUT.meta (per id: u16 src, u8 depth, u32 packed path of the moves src->x, 4 bits each).
// usage: echo_ball SRC OUT R MAXREM
#define ACC_NO_MAIN
#include "/home/user/operator-first/research/acc/optimality/acc_opt.c"
typedef struct { uint8_t*p; size_t n,cap; } Pool;   // packed states: u16 l0,u16 l1,w0,w1 ; + parallel path array
static size_t pool_add(Pool*P,const St*s){ size_t need=4+s->l[0]+s->l[1]; if(P->n+need>P->cap){ P->cap=P->cap?P->cap*2:(1<<20); while(P->n+need>P->cap) P->cap*=2; P->p=realloc(P->p,P->cap); if(!P->p) die("pool"); }
  size_t o=P->n; uint16_t h[2]={(uint16_t)s->l[0],(uint16_t)s->l[1]}; memcpy(P->p+o,h,4); memcpy(P->p+o+4,s->w[0],s->l[0]); memcpy(P->p+o+4+s->l[0],s->w[1],s->l[1]); P->n+=need; return o; }
static size_t pool_get(const Pool*P,size_t o,St*s){ uint16_t h[2]; memcpy(h,P->p+o,4); s->l[0]=h[0]; s->l[1]=h[1]; memcpy(s->w[0],P->p+o+4,h[0]); memcpy(s->w[1],P->p+o+4+h[0],h[1]); return 4+h[0]+h[1]; }
static uint64_t*LH; static uint64_t LN,Ln;     // local visited: h1,h2 (2 words per slot)
static int local_ins(uint64_t h1,uint64_t h2){ uint64_t i=(uint64_t)(((unsigned __int128)h1*LN)>>64);
  for(;;){ uint64_t a=LH[2*i]; if(!a){ LH[2*i]=h1; LH[2*i+1]=h2; Ln++; return 1; } if(a==h1&&LH[2*i+1]==h2) return 0; if(++i==LN) i=0; } }
// global table
static uint64_t*GH; static uint64_t GN,Gn; static uint8_t*Grem,*Gdep,*Gsrc; static uint32_t*Gpath; static uint64_t*Goff; static Pool GP;
int main(int argc,char**argv){
  if(argc<5){ fprintf(stderr,"usage\n"); return 2; }
  const char*srcf=argv[1],*out=argv[2]; int R=atoi(argv[3]),MAXREM=atoi(argv[4]);
  int LOG=getenv("LOCAL_LOG2")?atoi(getenv("LOCAL_LOG2")):26; LN=1ULL<<LOG; LH=calloc(LN*2,8); if(!LH) die("local alloc");
  int GLOG=getenv("GLOBAL_LOG2")?atoi(getenv("GLOBAL_LOG2")):25; GN=1ULL<<GLOG; GH=calloc(GN*2,8); Grem=calloc(GN,1); Gdep=calloc(GN,1); Gsrc=calloc(GN,1); Gpath=calloc(GN,4); Goff=calloc(GN,8);
  if(!GH||!Grem||!Gdep||!Gsrc||!Gpath||!Goff) die("global alloc");
  FILE*f=fopen(srcf,"r"); if(!f) die("src"); static St s0; int nsrc=0; int b;
  while(1){ if(fscanf(f,"%d",&b)!=1) break; int l0,l1,v; if(fscanf(f,"%d",&l0)!=1) break; for(int i=0;i<l0;i++){ if(fscanf(f,"%d",&v)!=1) die("rd"); s0.w[0][i]=v; }
    if(fscanf(f,"%d",&l1)!=1) break; for(int i=0;i<l1;i++){ if(fscanf(f,"%d",&v)!=1) die("rd"); s0.w[1][i]=v; } s0.l[0]=l0; s0.l[1]=l1;
    int r=R<MAXREM-b?R:MAXREM-b; int sidx=nsrc++; if(r<0||b+r<10){ fprintf(stderr,"src %d b=%d skipped\n",sidx,b); continue; }
    double t0=now(); memset(LH,0,LN*16); Ln=0;
    Pool cur={0},nxt={0}; uint32_t*cp=malloc(4),*np=NULL; size_t ccap=1,ncap=0,ncnt=0; size_t ccnt=1; cur.p=NULL;
    uint64_t h1,h2; fp(&s0,&h1,&h2); local_ins(h1,h2); pool_add(&cur,&s0); cp[0]=0;
    uint64_t gupd=0,lvl[16]={0}; lvl[0]=1;
    for(int k=0;k<=r;k++){
      // record layer k states into global best
      size_t off=0; for(size_t q=0;q<ccnt;q++){ static St s; size_t used=pool_get(&cur,off,&s); off+=used; int rem=b+k; if(rem<10||rem>MAXREM) continue;
        uint64_t g1,g2; fp(&s,&g1,&g2); uint64_t i=(uint64_t)(((unsigned __int128)g1*GN)>>64);
        for(;;){ uint64_t a=GH[2*i]; if(!a){ if(Gn*10>=GN*8) die("global table above load 0.8"); GH[2*i]=g1; GH[2*i+1]=g2; Gn++; Grem[i]=rem; Gdep[i]=k; Gsrc[i]=sidx; Gpath[i]=cp[q]; Goff[i]=pool_add(&GP,&s); gupd++; break; }
          if(a==g1&&GH[2*i+1]==g2){ if(rem<Grem[i]){ Grem[i]=rem; Gdep[i]=k; Gsrc[i]=sidx; Gpath[i]=cp[q]; gupd++; } break; } if(++i==GN) i=0; } }
      if(k==r) break;
      // expand
      off=0; nxt.n=0; ncnt=0; 
      for(size_t q=0;q<ccnt;q++){ static St s,t; size_t used=pool_get(&cur,off,&s); off+=used;
        for(int m=0;m<14;m++){ apply(&s,m,&t); uint64_t a1,a2; fp(&t,&a1,&a2); if(Ln*10>=LN*8) die("local table above load 0.8"); if(!local_ins(a1,a2)) continue;
          if(ncnt==ncap){ ncap=ncap?ncap*2:1024; np=realloc(np,ncap*4); if(!np) die("np"); } np[ncnt++]=cp[q]|((uint32_t)m<<(4*k)); pool_add(&nxt,&t); } }
      free(cur.p); cur=nxt; nxt.p=NULL; nxt.n=0; nxt.cap=0; free(cp); cp=np; np=NULL; ncap=0; ccnt=ncnt; lvl[k+1]=ncnt; }
    fprintf(stderr,"src %d b=%d r=%d ball=%llu updates=%llu global=%llu  %.1fs\n",sidx,b,r,(unsigned long long)Ln,(unsigned long long)gupd,(unsigned long long)Gn,now()-t0);
    free(cur.p); free(cp); }
  fclose(f);
  char p[4096]; snprintf(p,sizeof p,"%s.echo",out); FILE*fe=fopen(p,"w"); snprintf(p,sizeof p,"%s.meta",out); FILE*fm=fopen(p,"wb"); if(!fe||!fm) die("out");
  uint64_t id=0; for(uint64_t i=0;i<GN;i++){ if(!GH[2*i]) continue; if(Grem[i]<10||Grem[i]>MAXREM) continue; static St s; pool_get(&GP,Goff[i],&s);
    fprintf(fe,"%llu %d %d",(unsigned long long)id,(int)Grem[i],s.l[0]); for(int j=0;j<s.l[0];j++) fprintf(fe," %d",s.w[0][j]); fprintf(fe," %d",s.l[1]); for(int j=0;j<s.l[1];j++) fprintf(fe," %d",s.w[1][j]); fputc('\n',fe);
    uint16_t sr=Gsrc[i]; uint8_t dp=Gdep[i]; uint32_t pa=Gpath[i]; fwrite(&sr,2,1,fm); fwrite(&dp,1,1,fm); fwrite(&pa,4,1,fm); id++; }
  fclose(fe); fclose(fm); printf("echo states: %llu (sources %d, R=%d, MAXREM=%d)\n",(unsigned long long)id,nsrc,R,MAXREM); return 0; }
