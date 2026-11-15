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
  if(argc<6) die("usage: probe TABLE LURES AC_TARGET STABLE_TARGET EDITS len0 codes.. len1 codes..");
  struct stat st; int fd=open(argv[1],O_RDONLY); if(fd<0||fstat(fd,&st)) die("table");
  TT.t=mmap(0,st.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); TT.N=st.st_size/16;
  TA=atoi(argv[3]); TS=atoi(argv[4]); int ED=atoi(argv[5]); static St s0; parse_state(argv,6,&s0);
  PF=malloc(sizeof(St)*402); FILE*f=fopen(argv[2],"r"); char*line=0; size_t cap=0; long nl=0,nv=0;
  int seq[402],var[404];
  while(getline(&line,&cap,f)>0){ char tag[64]; char*p=line; int n=0; sscanf(p,"%63s",tag); p+=strlen(tag);
    while(*p){ while(*p==' ') p++; if(*p<'0'||*p>'9') break; if(n<400) seq[n++]=strtol(p,&p,10); else break; }
    if(n==0||n>=400) continue; nl++;
    PF[0]=s0; int np=n; for(int k=0;k<n;k++){ if(PF[k].l[0]>3000||PF[k].l[1]>3000){ np=k; break; } apply(&PF[k],seq[k],&PF[k+1]); } if(np<n) n=np;
    run(tag,seq,n,0); nv++;
    if(!ED) continue;
    for(int j=0;j<n;j++){ // deletion at j, substitution at j
      memcpy(var,seq,4*j); memcpy(var+j,seq+j+1,4*(n-j-1)); run(tag,var,n-1,j); nv++;
      for(int m=0;m<14;m++){ if(m==seq[j]) continue; memcpy(var,seq,4*n); var[j]=m; run(tag,var,n,j); nv++; } }
    for(int j=0;j<=n;j++) for(int m=0;m<14;m++){ memcpy(var,seq,4*j); var[j]=m; memcpy(var+j+1,seq+j,4*(n-j)); run(tag,var,n+1,j); nv++; } }
  fprintf(stderr,"lures %ld variants %ld best AC %d best Stable %d\n",nl,nv,bestA<(1<<30)?bestA:-1,bestS<(1<<30)?bestS:-1); return 0; }
