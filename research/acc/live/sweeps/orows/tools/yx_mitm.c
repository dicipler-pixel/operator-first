// yx_mitm (orows, 2026-10-14): exact capped meet in the middle, AC (x,y) and Stable via (y,x)+[15,15].
// Kernel/fingerprint/table: acc_opt.c verbatim (included).
//  Backward ball TB: BFS from (x,y) over states with total length <= CB, radius <= RB (depth kept in the table; layer files
//    are deleted as soon as the next layer is built). The ball around (y,x) is the x<->y swap of the ball around (x,y)
//    (move map PI). The uncapped T8 table (radius 8 around (x,y)) is also consulted.
//  Forward ball: BFS from the start over states with total length <= CF, depth <= A (layer files kept for the rebuild).
//  Every forward state s at depth d is looked up: AC   d + min(T8(s), TB(s));   Stable  d + min(T8(sw s), TB(sw s)) + 2.
// SCOPE of a miss: no AC route of length <= L to (x,y) [Stable: route to (y,x), line L+2] that splits at some d <= A_done with
//   the first d moves inside total length CF and the remaining L-d moves either <= 8 (uncapped) or <= RB_done inside CB.
// usage: yx_mitm T8FILE CF A CB RB WORKDIR l0 w.. l1 w..    env BUDF, BUDB (state budgets), LOGF, LOGB (initial log2 slots)
#define ACC_NO_MAIN
#include "acc_opt.c"
static const uint8_t PI[14]={0,1,2,3,4,5,8,9,6,7,12,13,10,11};
static void swapst(const St*s,St*r){ r->l[0]=s->l[0]; r->l[1]=s->l[1]; for(int j=0;j<2;j++) for(int i=0;i<s->l[j];i++) r->w[j][i]=s->w[j][i]^2; }
static Tab TB,SF; static St a,b,c2;
static int dist2(const St*s,int*which){ uint64_t h1,h2; fp(s,&h1,&h2); int t=tab_find(&TT,h1,h2), u=tab_find(&TB,h1,h2);
  int best=99; *which=-1; if(t>=0&&t<best){ best=t; *which=0; } if(u>=0&&u<best){ best=u; *which=1; } return best; }
// walk from s to (x,y) through table W (0 = T8, 1 = TB) with strictly decreasing depth; append moves (mapped by map)
static int walk(St s,int d,int which,const uint8_t*map,int*path,int L){ uint64_t h1,h2; static St n;
  const Tab*W=which?&TB:&TT;
  for(int k=d;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&s,m,&n); fp(&n,&h1,&h2); if(tab_find(W,h1,h2)==k-1){ path[L++]=map[m]; s=n; ok=1; break; } }
    if(!ok) return -1; }
  if(!(s.l[0]==1&&s.l[1]==1&&s.w[0][0]==0&&s.w[1][0]==2)) return -2; return L; }
int main(int argc,char**argv){
  const char*tf=argv[1]; int CF=atoi(argv[2]),A=atoi(argv[3]),CB=atoi(argv[4]),RB=atoi(argv[5]); const char*dir=argv[6]; St s0; parse_state(argv,7,&s0);
  uint64_t BUDF=getenv("BUDF")?strtoull(getenv("BUDF"),0,10):150000000ULL, BUDB=getenv("BUDB")?strtoull(getenv("BUDB"),0,10):150000000ULL;
  int LOGF=getenv("LOGF")?atoi(getenv("LOGF")):24, LOGB=getenv("LOGB")?atoi(getenv("LOGB")):24; double T0=now();
  struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
  TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); TT.N=stt.st_size/16; TT.n=0;
  // ---- backward capped ball around (x,y) ----
  tab_init(&TB,1ULL<<LOGB); St g; g.l[0]=1; g.l[1]=1; g.w[0][0]=0; g.w[1][0]=2; uint64_t h1,h2; fp(&g,&h1,&h2); tab_ins(&TB,h1,h2,0,1);
  FILE*o=openf(dir,"B",0,"wb"); wr_state(o,&g); fclose(o); int RBd=0, bpart=0;
  for(int d=1;d<=RB;d++){ FILE*in=openf(dir,"B",d-1,"rb"); FILE*out=openf(dir,"B",d,"wb"); uint64_t cnt=0;
    while(rd_state(in,&a)) for(int m=0;m<14;m++){ apply(&a,m,&b); if(b.l[0]+b.l[1]>CB) continue; fp(&b,&h1,&h2);
      if(tab_ins(&TB,h1,h2,d,1)<0){ cnt++; wr_state(out,&b); if(TB.n>BUDB){ bpart=1; goto bend; } } }
    bend: fclose(in); fclose(out); rmf(dir,"B",d-1);
    fprintf(stderr,"[B] cap=%d r=%d +%llu total=%llu (%.0fs)\n",CB,d,(unsigned long long)cnt,(unsigned long long)TB.n,now()-T0);
    if(bpart){ RBd=d-1; fprintf(stderr,"[B] budget hit inside radius %d: radius %d is the last complete one\n",d,RBd); break; }
    RBd=d; if(cnt==0) break; }
  rmf(dir,"B",RBd); rmf(dir,"B",RBd+1);
  printf("BACKWARD cap=%d radius_done=%d states=%llu\n",CB,RBd,(unsigned long long)TB.n); fflush(stdout);
  // ---- forward capped ball from the start ----
  tab_init(&SF,1ULL<<LOGF); fp(&s0,&h1,&h2); tab_ins(&SF,h1,h2,0,1); o=openf(dir,"F",0,"wb"); wr_state(o,&s0); fclose(o);
  int bestA=99,bestS=99,dA=0,dS=0,wA=0,wS=0,tA=0,tS=0; St mA,mS; int w;
  { int t=dist2(&s0,&w); if(t<99){ bestA=t; mA=s0; dA=0; tA=t; wA=w; } swapst(&s0,&c2); int u=dist2(&c2,&w); if(u<99){ bestS=u+2; mS=s0; dS=0; tS=u; wS=w; } }
  int Ad=0, fpart=0;
  for(int d=1;d<=A;d++){ FILE*in=openf(dir,"F",d-1,"rb"); FILE*out=openf(dir,"F",d,"wb"); uint64_t cnt=0;
    while(rd_state(in,&a)) for(int m=0;m<14;m++){ apply(&a,m,&b); if(b.l[0]+b.l[1]>CF) continue; fp(&b,&h1,&h2);
      if(tab_ins(&SF,h1,h2,d&15,1)>=0) continue; cnt++; wr_state(out,&b); if(SF.n>BUDF) fpart=1;
      int t=dist2(&b,&w); if(d+t<bestA){ bestA=d+t; mA=b; dA=d; tA=t; wA=w; }
      swapst(&b,&c2); int u=dist2(&c2,&w); if(d+u+2<bestS){ bestS=d+u+2; mS=b; dS=d; tS=u; wS=w; } if(fpart) goto fend; }
    fend: fclose(in); fclose(out); Ad=fpart?d-1:d; if(fpart) fprintf(stderr,"[F] budget hit inside depth %d: depth %d is the last complete one\n",d,Ad);
    fprintf(stderr,"[F] cap=%d d=%d +%llu total=%llu bestAC=%d bestSAC=%d (%.0fs)\n",CF,d,(unsigned long long)cnt,(unsigned long long)SF.n,bestA,bestS,now()-T0);
    if(cnt==0||fpart) break; }
  printf("FORWARD cap=%d depth_done=%d states=%llu\n",CF,Ad,(unsigned long long)SF.n);
  printf("RESULT bestAC=%d bestSAC=%d (99 = none within the scope)\n",bestA,bestS);
  for(int which=0;which<2;which++){ int best=which?bestS:bestA; if(best>=99) continue;
    int dd=which?dS:dA, t=which?tS:tA, ww=which?wS:wA; St cur=which?mS:mA; int rev[512];
    for(int k=dd;k>0;k--){ FILE*in=openf(dir,"F",k-1,"rb"); int found=0; static St p,q;
      while(!found&&rd_state(in,&p)) for(int m=0;m<14;m++){ apply(&p,m,&q); if(st_eq(&q,&cur)){ rev[k-1]=m; cur=p; found=1; break; } }
      fclose(in); if(!found){ printf("REBUILD_FAIL\n"); return 5; } }
    int path[1024],L=0; for(int k=0;k<dd;k++) path[L++]=rev[k];
    St e=which?mS:mA; static const uint8_t ID[14]={0,1,2,3,4,5,6,7,8,9,10,11,12,13};
    if(which){ St tmp; swapst(&e,&tmp); e=tmp; }
    L=walk(e,t,ww,which?PI:ID,path,L); if(L<0){ printf("REBUILD_FAIL2 %d\n",L); return 5; }
    if(which){ path[L++]=15; path[L++]=15; }
    printf("%s %d PATH",which?"SAC":"AC",L); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); }
  for(int k=0;k<=Ad+1;k++) rmf(dir,"F",k);
  printf("WALL %.0fs\n",now()-T0); return 0; }
