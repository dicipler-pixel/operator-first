#define ACC_NO_MAIN
#include "acc_opt.c"
static int lookup(const St*s){uint64_t a,b;fp(s,&a,&b);return tab_find(&TT,a,b);}
static int tail(St c,int t,int*out){int n=0;for(int d=t;d>0;d--){St next;int found=0;for(int m=0;m<14;m++){apply(&c,m,&next);if(lookup(&next)==d-1){out[n++]=m;c=next;found=1;break;}}if(!found)die("signed tail");}return n;}
int main(int argc,char**argv){
 if(argc!=2)die("expected T8");int fd=open(argv[1],O_RDONLY);struct stat st;if(fd<0||fstat(fd,&st))die("table");TT.t=mmap(0,st.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0);if(TT.t==MAP_FAILED)die("map");TT.N=st.st_size/16;
 int map[8][4],back[8][4],goalac[8];St goal[8];
 for(int q=0;q<8;q++){for(int c=0;c<4;c++){int g=c>>1;int z=((g^((q>>2)&1))<<1)|((c&1)^((q>>g)&1));map[q][c]=z;back[q][z]=c;}goal[q].l[0]=goal[q].l[1]=1;goal[q].w[0][0]=back[q][0];goal[q].w[1][0]=back[q][2];goalac[q]=lookup(&goal[q]);if(goalac[q]<0)die("missing basis");}
 St s;int z,idx=0;while(scanf("%d",&s.l[0])==1){for(int i=0;i<s.l[0];i++){if(scanf("%d",&z)!=1)return 2;s.w[0][i]=z;}if(scanf("%d",&s.l[1])!=1)return 2;for(int i=0;i<s.l[1];i++){if(scanf("%d",&z)!=1)return 2;s.w[1][i]=z;}
  int dist[8],best[2]={999,999},which[2]={0,0};St trans[8];
  for(int q=0;q<8;q++){trans[q].l[0]=s.l[0];trans[q].l[1]=s.l[1];for(int j=0;j<2;j++)for(int i=0;i<s.l[j];i++)trans[q].w[j][i]=map[q][s.w[j][i]];dist[q]=lookup(&trans[q]);if(dist[q]<0)continue;int costs[2]={goalac[q],2+(goal[q].w[0][0]&1)+(goal[q].w[1][0]&1)};for(int k=0;k<2;k++)if(dist[q]+costs[k]<best[k]){best[k]=dist[q]+costs[k];which[k]=q;}}
  printf("{\"i\":%d,\"d\":[",idx++);for(int q=0;q<8;q++)printf("%s%d",q?",":"",dist[q]);printf("]");
  for(int k=0;k<2;k++){printf(",\"%s\":",k?"sac":"ac");if(best[k]==999){printf("null");continue;}int q=which[k],p[32],n=tail(trans[q],dist[q],p);for(int j=0;j<n;j++)if(p[j]>=6)p[j]=6+4*((p[j]-6)/4)+back[q][(p[j]-6)&3];if(k){if(goal[q].w[0][0]&1)p[n++]=0;if(goal[q].w[1][0]&1)p[n++]=1;if((q>>2)&1){p[n++]=15;p[n++]=15;}else{p[n++]=16;p[n++]=15;}}else n+=tail(goal[q],goalac[q],p+n);if(n!=best[k])die("tail length");printf("[");for(int j=0;j<n;j++)printf("%s%d",j?",":"",p[j]);printf("]");}printf("}\n");}
 return 0;
}
