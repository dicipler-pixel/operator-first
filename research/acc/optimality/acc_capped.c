// Capped exhaustive BFS + exact finish: BFS from the start over states with total relator length
// <= CAP (uncapped T_9 lookups on every state). The first depth d at which min(d + dT) can no longer
// improve gives the shortest path whose capped prefix stays within CAP. Kernel shared with acc_opt.c.
// usage: acc_capped TFILE CAP BUDGET WORKDIR TAG l0 w.. l1 w..
#define ACC_NO_MAIN
#include "acc_opt.c"
static St cc,nn2,sw2;
static void swapst(const St*s,St*r){ r->l[0]=s->l[0]; r->l[1]=s->l[1]; for(int j=0;j<2;j++) for(int i=0;i<s->l[j];i++) r->w[j][i]=s->w[j][i]^2; }
static const uint8_t PI[14]={0,1,2,3,4,5,8,9,6,7,12,13,10,11};
int main(int argc,char**argv){
  const char*tf=argv[1]; int CAP=atoi(argv[2]); uint64_t BUD=strtoull(argv[3],0,10); const char*dir=argv[4],*tag=argv[5]; St s0; parse_state(argv,6,&s0);
  struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
  TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); TT.N=stt.st_size/16;
  tab_init(&SS,1ULL<<24); uint64_t h1,h2; fp(&s0,&h1,&h2); tab_ins(&SS,h1,h2,0,1);
  int bestAC=1<<30,bestSAC=1<<30,dAC=0,dSAC=0,tAC=0,tSAC=0; St mAC,mSAC;
  { int t=tab_find(&TT,h1,h2); if(t>=0){ bestAC=t; mAC=s0; dAC=0; tAC=t; } }
  FILE*o=openf(dir,tag,0,"wb"); wr_state(o,&s0); fclose(o); int d; int closed=0;
  // depth labels only go to 15 in 4 bits, so store the BFS depth mod 16 and keep parents implicit via layer files
  for(d=1;;d++){ if(d>=bestAC && d+2>=bestSAC) break;
    FILE*in=openf(dir,tag,d-1,"rb"); FILE*out=openf(dir,tag,d,"wb"); uint64_t c=0;
    while(rd_state(in,&cc)) for(int m=0;m<14;m++){ apply(&cc,m,&nn2); if(nn2.l[0]+nn2.l[1]>CAP) continue; fp(&nn2,&h1,&h2);
        if(tab_ins(&SS,h1,h2,d&15,1)>=0) continue; c++; wr_state(out,&nn2);
        int t=tab_find(&TT,h1,h2); if(t>=0&&d+t<bestAC){ bestAC=d+t; mAC=nn2; dAC=d; tAC=t; }
        swapst(&nn2,&sw2); uint64_t g1,g2; fp(&sw2,&g1,&g2); int u=tab_find(&TT,g1,g2); if(u>=0&&d+u+2<bestSAC){ bestSAC=d+u+2; mSAC=nn2; dSAC=d; tSAC=u; } }
    fclose(in); fclose(out);
    fprintf(stderr,"[%s] cap=%d d=%d +%llu total=%llu bestAC=%d bestSAC=%d\n",tag,CAP,d,(unsigned long long)c,(unsigned long long)SS.n,bestAC<(1<<30)?bestAC:-1,bestSAC<(1<<30)?bestSAC:-1);
    if(c==0){ closed=1; break; } if(SS.n>BUD){ break; } }
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
  for(int k=0;k<=d;k++) rmf(dir,tag,k);
  return 0; }
