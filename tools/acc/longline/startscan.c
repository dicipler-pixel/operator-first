// Lure probe: replay move sequences (and one-edit variants) on a start state; at every prefix look the state up in the
// longline table (finish (x,y)) and its letter swap (finish (y,x)). Prints full rebuilt paths that reach the targets.
#define ACC_NO_MAIN
#include "acc_opt.c"
static Tab TT; static int PI[14]={0,1,2,3,4,5,8,9,6,7,12,13,10,11};
static void swapl(const St*a,St*b){ for(int j=0;j<2;j++){ b->l[j]=a->l[j]; for(int i=0;i<a->l[j];i++) b->w[j][i]=a->w[j][i]^2; } }
static int look(const St*s){ uint64_t h1,h2; fp(s,&h1,&h2); return tab_find(&TT,h1,h2); }
static int descend(St c,int t,int*out,int map){ static St nx; int n=0;
  for(int k=t;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&nx); if(look(&nx)==k-1){ out[n++]=map?PI[m]:m; c=nx; ok=1; break; } } if(!ok) return -1; } return n; }
static St*PF; static int bestA=1<<30,bestS=1<<30,TA,TS;
static void consider(const char*tag,const int*seq,int n,int k,const St*s){ static St sw; int t1=look(s); swapl(s,&sw); int t2=look(&sw);
  int tail[512],nt;
  if(t1>=0&&k+t1<=TA&&k+t1<bestA){ nt=descend(*s,t1,tail,0); if(nt==t1){ bestA=k+t1; printf("AC %d %s:",bestA,tag); for(int i=0;i<k;i++) printf(" %d",seq[i]); for(int i=0;i<nt;i++) printf(" %d",tail[i]); printf("\n"); fflush(stdout);} }
  int ts=-1,fin=0; if(t1>=0) { ts=t1; fin=0; } if(t2>=0&&(ts<0||t2<ts)){ ts=t2; fin=1; }
  if(ts>=0&&k+ts+2<=TS&&k+ts+2<bestS){ nt=fin?descend(sw,ts,tail,1):descend(*s,ts,tail,0); if(nt==ts){ bestS=k+ts+2; printf("STABLE %d %s:",bestS,tag); for(int i=0;i<k;i++) printf(" %d",seq[i]); for(int i=0;i<nt;i++) printf(" %d",tail[i]); printf(fin?" 15 15\n":" 16 15\n"); fflush(stdout);} } }
static void run(const char*tag,const int*seq,int n,int from){ static St c,nx; c=PF[from];
  for(int k=from;k<=n;k++){ consider(tag,seq,n,k,&c); if(k<n){ if(c.l[0]>3000||c.l[1]>3000) return; apply(&c,seq[k],&nx); c=nx; } } }
int main(int argc,char**argv){
  if(argc<3) die("usage: startscan TABLE STARTS");
  struct stat st; int fd=open(argv[1],O_RDONLY); if(fd<0||fstat(fd,&st)) die("table");
  TT.t=mmap(0,st.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); TT.N=st.st_size/16;
  FILE*f=fopen(argv[2],"r"); char*line=0; size_t cap=0; static St s0; static char*av[20000];
  while(getline(&line,&cap,f)>0){ int n=0; char*tok=strtok(line," \n"); while(tok&&n<20000){ av[n++]=tok; tok=strtok(0," \n"); }
    if(n<5) continue; TA=atoi(av[1]); TS=atoi(av[2]); parse_state(av,3,&s0); bestA=bestS=1<<30; int seq[1]={0};
    consider(av[0],seq,0,0,&s0); }
  return 0; }
