// Longline bait table: T8 (4-bit) converted to 8-bit distances, plus every road state within 255 of its finish,
// under all 16 AC symmetries (8 signed letter permutations x 2 relator orders). Distances relaxed to a fixpoint so
// every entry d>0 has a neighbour at exactly d-1 (the beam's exact descent rebuild needs that).
#define ACC_NO_MAIN
#include "acc_opt.c"
static void tab_set(Tab*T,uint64_t h1,uint64_t h2,int d){ uint64_t i=slot0(T,h1);
  for(;;){ uint64_t a=T->t[2*i]; if(!a){ T->t[2*i]=h1; T->t[2*i+1]=h2|(uint64_t)d; T->n++; return; }
    if(a==h1&&(T->t[2*i+1]&~0xFFULL)==h2){ if((int)(T->t[2*i+1]&0xFF)>d) T->t[2*i+1]=h2|(uint64_t)d; return; }
    if(++i==T->N) i=0; } }
static uint8_t*AR=0; static uint64_t ARn=0,ARc=0; static uint64_t*OFF=0; static uint64_t NS=0,NC=0;
static void keep(const St*s){ uint64_t need=4+s->l[0]+s->l[1]; if(ARn+need>ARc){ ARc=ARc?ARc*2:(1ULL<<28); AR=realloc(AR,ARc); if(!AR) die("arena"); }
  if(NS==NC){ NC=NC?NC*2:(1<<22); OFF=realloc(OFF,8*NC); if(!OFF) die("off"); }
  uint8_t*q=AR+ARn; q[0]=s->l[0]&255; q[1]=s->l[0]>>8; q[2]=s->l[1]&255; q[3]=s->l[1]>>8; memcpy(q+4,s->w[0],s->l[0]); memcpy(q+4+s->l[0],s->w[1],s->l[1]); OFF[NS++]=ARn; ARn+=need; }
static void get(uint64_t k,St*s){ uint8_t*q=AR+OFF[k]; s->l[0]=q[0]|(q[1]<<8); s->l[1]=q[2]|(q[3]<<8); memcpy(s->w[0],q+4,s->l[0]); memcpy(s->w[1],q+4+s->l[0],s->l[1]); }
static void sym(const St*a,int g,St*b){ int sw=g&1,sx=(g>>1)&1,sy=(g>>2)&1,ord=(g>>3)&1; uint8_t m[4];
  m[0]=(sw?2:0)|sx; m[1]=m[0]^1; m[2]=(sw?0:2)|sy; m[3]=m[2]^1;
  for(int j=0;j<2;j++){ int jj=ord?1-j:j; b->l[jj]=a->l[j]; for(int i=0;i<a->l[j];i++) b->w[jj][i]=m[a->w[j][i]]; } }
int main(int argc,char**argv){
  if(argc<5) die("usage: bait OLD_T8 RECORDS OUT NSLOTS");
  uint64_t N=strtoull(argv[4],0,10); Tab T; tab_init(&T,N);
  struct stat st; int fd=open(argv[1],O_RDONLY); if(fd<0||fstat(fd,&st)) die("old table");
  uint64_t*o=mmap(0,st.st_size,PROT_READ,MAP_SHARED,fd,0); uint64_t ON=st.st_size/16, nold=0;
  for(uint64_t i=0;i<ON;i++) if(o[2*i]){ tab_set(&T,o[2*i],o[2*i+1]&~0xFFULL,(int)(o[2*i+1]&0xF)); nold++; }
  munmap(o,st.st_size); close(fd); fprintf(stderr,"T8 entries %llu\n",(unsigned long long)nold);
  FILE*f=fopen(argv[2],"r"); if(!f) die("records"); char*line=0; size_t cap=0; static St s,g,e,ge; uint64_t nrec=0,nins=0,nskip=0;
  while(getline(&line,&cap,f)>0){ int r,ef; char*p=line; r=strtol(p,&p,10); ef=strtol(p,&p,10); while(*p==' ') p++;
    for(int j=0;j<2;j++){ int n=0; while(*p>='0'&&*p<='3'){ s.w[j][n++]=*p-'0'; p++; } s.l[j]=n; while(*p==' ') p++; }
    e.l[0]=1; e.l[1]=1; e.w[0][0]=ef?2:0; e.w[1][0]=ef?0:2; nrec++;
    for(int k=0;k<16;k++){ sym(&e,k,&ge); uint64_t h1,h2; fp(&ge,&h1,&h2); int c=tab_find(&T,h1,h2); if(c<0){ nskip++; continue; }
      int d=r+c; if(d>255){ nskip++; continue; } sym(&s,k,&g); fp(&g,&h1,&h2); int old=tab_find(&T,h1,h2);
      if(old>=0&&old<=d) continue; if(old<0){ if(T.n*10>=T.N*9) die("table full"); keep(&g); } tab_set(&T,h1,h2,d); nins++; } }
  fprintf(stderr,"records %llu, inserts/lowerings %llu, skipped %llu, kept states %llu, table %llu/%llu\n",(unsigned long long)nrec,(unsigned long long)nins,(unsigned long long)nskip,(unsigned long long)NS,(unsigned long long)T.n,(unsigned long long)T.N);
  static St c,nx;
  { uint32_t*DK=malloc(4*NS); for(uint64_t k=0;k<NS;k++){ get(k,&c); uint64_t h1,h2; fp(&c,&h1,&h2); DK[k]=(uint32_t)tab_find(&T,h1,h2); }
    uint64_t cnt[257]={0}; for(uint64_t k=0;k<NS;k++) cnt[DK[k]+1]++; for(int d=1;d<257;d++) cnt[d]+=cnt[d-1];
    uint64_t*O2=malloc(8*NS); for(uint64_t k=0;k<NS;k++) O2[cnt[DK[k]]++]=OFF[k]; free(OFF); OFF=O2; free(DK);
    fprintf(stderr,"sorted %llu states by distance\n",(unsigned long long)NS); }
  for(int pass=1;;pass++){ uint64_t ch=0;
    for(uint64_t k=0;k<NS;k++){ get(k,&c); uint64_t h1,h2; fp(&c,&h1,&h2); int d=tab_find(&T,h1,h2), best=d;
      for(int m=0;m<14;m++){ apply(&c,m,&nx); uint64_t a,b; fp(&nx,&a,&b); int dn=tab_find(&T,a,b); if(dn>=0&&dn+1<best) best=dn+1; }
      if(best<d){ tab_set(&T,h1,h2,best); ch++; } }
    fprintf(stderr,"relax pass %d: %llu lowered\n",pass,(unsigned long long)ch); if(!ch) break; }
  uint64_t bad=0; int hist[256]={0};
  for(uint64_t k=0;k<NS;k++){ get(k,&c); uint64_t h1,h2; fp(&c,&h1,&h2); int d=tab_find(&T,h1,h2); hist[d]++; if(d==0) continue; int ok=0;
    for(int m=0;m<14&&!ok;m++){ apply(&c,m,&nx); uint64_t a,b; fp(&nx,&a,&b); if(tab_find(&T,a,b)==d-1) ok=1; } if(!ok) bad++; }
  fprintf(stderr,"descent check: %llu states without an exact d-1 neighbour\n",(unsigned long long)bad);
  fprintf(stderr,"hook distances:"); for(int d=0;d<256;d++) if(hist[d]) fprintf(stderr," %d:%d",d,hist[d]); fprintf(stderr,"\n");
  if(bad) die("inconsistent");
  FILE*out=fopen(argv[3],"wb"); if(!out) die("out"); fwrite(T.t,16,T.N,out); fclose(out); fprintf(stderr,"wrote %s\n",argv[3]); return 0; }
