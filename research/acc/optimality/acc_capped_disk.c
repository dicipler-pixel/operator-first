// File-backed fixed visited-table pilot; same 123-bit fingerprint semantics.
// Positive paths require official verification; negative bounds retain the fingerprint caveat.
// Set VISITED_FILE=/path/visited.tab for MAP_SHARED, sized once from BUDGET.
// Capped exhaustive BFS + exact finish: BFS from the start over states with total relator length
// <= CAP (uncapped T_9 lookups on every state). The first depth d at which min(d + dT) can no longer
// improve gives the shortest path whose capped prefix stays within CAP. Kernel shared with acc_opt.c.
// usage: acc_capped TFILE CAP BUDGET WORKDIR TAG l0 w.. l1 w..
#define ACC_NO_MAIN
#include "acc_opt.c"
static St cc,nn2,sw2;
static void tab_init_disk(Tab*T,uint64_t N,const char*path){
  if(!path||!*path){ tab_init(T,N); return; }
  int f=open(path,O_RDWR|O_CREAT|O_TRUNC,0600);
  if(f<0) die("visited open");
  if(N>SIZE_MAX/16 || ftruncate(f,(off_t)(16*N))) die("visited truncate");
  T->N=N; T->n=0;
  T->t=mmap(0,(size_t)16*N,PROT_READ|PROT_WRITE,MAP_SHARED,f,0);
  close(f);
  if(T->t==MAP_FAILED) die("visited mmap");
  madvise(T->t,(size_t)16*N,MADV_RANDOM);
}
static void swapst(const St*s,St*r){ r->l[0]=s->l[0]; r->l[1]=s->l[1]; for(int j=0;j<2;j++) for(int i=0;i<s->l[j];i++) r->w[j][i]=s->w[j][i]^2; }
static const uint8_t PI[14]={0,1,2,3,4,5,8,9,6,7,12,13,10,11};
// ECHO_FILE ("id dist l0 w.. l1 w.." per line): states on or near our known routes, each with a known remaining
// distance to (x,y) (an upper bound). A BFS state that meets the echo at depth d gives a path d + dist; the
// Python side appends the known tail for that id. ("the echo from the back is still talking to you")
static uint64_t*EH1,*EH2; static uint16_t*ED; static uint32_t*EI; static uint64_t EN;
static void echo_load(const char*fn){ FILE*f=fopen(fn,"r"); if(!f) die("echo file"); uint64_t cnt=0; char line[65536];
  while(fgets(line,sizeof line,f)) cnt++; rewind(f); EN=1; while(EN<cnt*2+16) EN<<=1;
  EH1=calloc(EN,8); EH2=calloc(EN,8); ED=calloc(EN,2); EI=calloc(EN,4); if(!EH1||!EH2||!ED||!EI) die("echo alloc");
  while(fgets(line,sizeof line,f)){ char*p=line; unsigned id,dist; int off; if(sscanf(p,"%u %u%n",&id,&dist,&off)!=2) continue; p+=off;
    static St e; for(int r=0;r<2;r++){ int l; sscanf(p,"%d%n",&l,&off); p+=off; e.l[r]=l; for(int i=0;i<l;i++){ int v; sscanf(p,"%d%n",&v,&off); p+=off; e.w[r][i]=(uint8_t)v; } }
    uint64_t a,b; fp(&e,&a,&b); uint64_t k=a&(EN-1); while(EH1[k]||EH2[k]){ if(EH1[k]==a&&EH2[k]==b) break; k=(k+1)&(EN-1); }
    if(!(EH1[k]==a&&EH2[k]==b)||dist<ED[k]){ EH1[k]=a; EH2[k]=b; ED[k]=(uint16_t)dist; EI[k]=id; } }
  fclose(f); fprintf(stderr,"echo states loaded: %llu\n",(unsigned long long)cnt); }
static int echo_find(uint64_t a,uint64_t b,uint32_t*id){ if(!EN) return -1; uint64_t k=a&(EN-1);
  while(EH1[k]||EH2[k]){ if(EH1[k]==a&&EH2[k]==b){ *id=EI[k]; return ED[k]; } k=(k+1)&(EN-1); } return -1; }
int main(int argc,char**argv){
  const char*tf=argv[1]; int CAP=atoi(argv[2]); uint64_t BUD=strtoull(argv[3],0,10); const char*dir=argv[4],*tag=argv[5]; St s0; parse_state(argv,6,&s0);
  struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
  TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED,fd,0); TT.N=stt.st_size/16;
  uint64_t slots=(BUD*5)/4+1024; // load <= 0.80 through the requested budget
  tab_init_disk(&SS,slots,getenv("VISITED_FILE"));
  fprintf(stderr,"[%s] visited %llu slots %.2f GiB %s\n",tag,
    (unsigned long long)slots,(double)(16*slots)/(1ULL<<30),
    getenv("VISITED_FILE")?"MAP_SHARED disk-backed":"anonymous"); uint64_t h1,h2; fp(&s0,&h1,&h2); tab_ins(&SS,h1,h2,0,0);
  int bestAC=1<<30,bestSAC=1<<30,dAC=0,dSAC=0,tAC=0,tSAC=0; St mAC,mSAC;
  int bestE=1<<30,dE=0; uint32_t idE=0; St mE; if(getenv("ECHO_FILE")) echo_load(getenv("ECHO_FILE"));
  { int t=tab_find(&TT,h1,h2); if(t>=0){ bestAC=t; mAC=s0; dAC=0; tAC=t; } }
  FILE*o=openf(dir,tag,0,"wb"); wr_state(o,&s0); fclose(o); int d; int closed=0, budget_hit=0;
  // depth labels only go to 15 in 4 bits, so store the BFS depth mod 16 and keep parents implicit via layer files
  int MAXD=getenv("MAXD")?atoi(getenv("MAXD")):1<<30;
  for(d=1;;d++){ if(d>=bestAC && d+2>=bestSAC) break; if(d>MAXD) break;
    FILE*in=openf(dir,tag,d-1,"rb"); FILE*out=openf(dir,tag,d,"wb"); uint64_t c=0;
    while(!budget_hit&&rd_state(in,&cc)) for(int m=0;m<14;m++){ if(SS.n>=BUD){ budget_hit=1; break; } apply(&cc,m,&nn2); if(nn2.l[0]+nn2.l[1]>CAP) continue; fp(&nn2,&h1,&h2);
        if(tab_ins(&SS,h1,h2,d&15,0)>=0) continue; c++; wr_state(out,&nn2);
        int t=tab_find(&TT,h1,h2); if(t>=0&&d+t<bestAC){ bestAC=d+t; mAC=nn2; dAC=d; tAC=t; }
        swapst(&nn2,&sw2); uint64_t g1,g2; fp(&sw2,&g1,&g2); int u=tab_find(&TT,g1,g2); if(u>=0&&d+u+2<bestSAC){ bestSAC=d+u+2; mSAC=nn2; dSAC=d; tSAC=u; }
        if(EN){ uint32_t id; int e=echo_find(h1,h2,&id); if(e>=0&&d+e<bestE){ bestE=d+e; mE=nn2; dE=d; idE=id; } } }
    fclose(in); fclose(out);
    fprintf(stderr,"[%s] cap=%d d=%d +%llu total=%llu bestAC=%d bestSAC=%d\n",tag,CAP,d,(unsigned long long)c,(unsigned long long)SS.n,bestAC<(1<<30)?bestAC:-1,bestSAC<(1<<30)?bestSAC:-1);
    if(!budget_hit&&c==0){ closed=1; break; } if(budget_hit){ break; } }
  printf("[%s] cap=%d states=%llu depth=%d %s\n",tag,CAP,(unsigned long long)SS.n,d,closed?"CLOSED":"STOPPED");
  // rebuild prefixes: walk back through layer files by recomputing (search layer d-1 for a parent)
  for(int which=0;which<2;which++){ int best=which?bestSAC:bestAC; if(best>=(1<<30)){ printf("[%s] %s NONE\n",tag,which?"SAC":"AC"); continue; }
    int dd=which?dSAC:dAC, t=which?tSAC:tAC; St cur2=which?mSAC:mAC; int rev[512];
    for(int k=dd;k>0;k--){ FILE*in=openf(dir,tag,k-1,"rb"); int found=0; static St p,q;
      while(!found&&rd_state(in,&p)) for(int m=0;m<14;m++){ apply(&p,m,&q); if(st_eq(&q,&cur2)){ rev[k-1]=m; cur2=p; found=1; break; } }
      fclose(in); if(!found){ printf("REBUILD_FAIL\n"); return 5; } }
    int path[1024],L=0; for(int k=0;k<dd;k++) path[L++]=rev[k];
    St c=which?mSAC:mAC; if(which){ St tmp; swapst(&c,&tmp); c=tmp; }
    for(int k=t;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&nn2); fp(&nn2,&h1,&h2); if(tab_find(&TT,h1,h2)==k-1){ path[L++]=which?PI[m]:m; c=nn2; ok=1; break; } } if(!ok){ printf("REBUILD_FAIL2\n"); return 5; } }
    if(which){ path[L++]=15; path[L++]=15; }
    printf("[%s] %s %d PATH",tag,which?"SAC":"AC",L); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); }
  if(bestE<(1<<30)){ St cur2=mE; int rev[512];
    for(int k=dE;k>0;k--){ FILE*in=openf(dir,tag,k-1,"rb"); int found=0; static St p,q;
      while(!found&&rd_state(in,&p)) for(int m=0;m<14;m++){ apply(&p,m,&q); if(st_eq(&q,&cur2)){ rev[k-1]=m; cur2=p; found=1; break; } }
      fclose(in); if(!found){ printf("REBUILD_FAIL_ECHO\n"); break; } }
    printf("[%s] ECHO %d id %u prefix %d PATH",tag,bestE,idE,dE); for(int k=0;k<dE;k++) printf(" %d",rev[k]); printf("\n"); }
  for(int k=0;k<=d;k++) rmf(dir,tag,k);
  return 0; }
