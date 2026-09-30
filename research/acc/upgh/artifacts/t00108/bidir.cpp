// Exact capped bidirectional BFS between two AC states on the ac-r2-v1 move set (14 atomic moves).
// Letters: x=0 X=1 y=2 Y=3 (inverse = ^1). Every intermediate state (both sides) has total length <= CAP.
// usage: bidir CAP MAXTOT MAXSTATES START_R0 START_R1 SRC1 [SRC2 ...]
//   SRC = R0,R1@LEVEL  (LEVEL = known remaining distance of that source; first source sets the base level)
//   prints: RESULT total <n> fwd_depth <a> bwd_level <b> cap <CAP> ; PATH <moves> (start -> meeting -> source)
//   or NONE reason (closed = both capped components exhausted; maxtot; maxstates)
#include <bits/stdc++.h>
using namespace std;
typedef unsigned char u8; typedef uint64_t u64; typedef uint32_t u32;
static int CAP;
struct St { u8 l[2]; u8 w[2][64]; };
static inline void rinv(const u8*a,int n,u8*o){ for(int i=0;i<n;i++) o[i]=a[n-1-i]^1; }
// o = reduce(a+b), returns length
static int cat(const u8*a,int na,const u8*b,int nb,u8*o){ int k=0; memcpy(o,a,na); k=na; for(int i=0;i<nb;i++){ if(k&&o[k-1]==(b[i]^1)) k--; else o[k++]=b[i]; } return k; }
static bool applym(const St&s,int m,St&r){
  u8 t[130]; int n;
  r=s;
  if(m==0){ rinv(s.w[0],s.l[0],r.w[0]); return true; }
  if(m==1){ rinv(s.w[1],s.l[1],r.w[1]); return true; }
  if(m==2||m==3){ u8 b[64]; const u8*bp=s.w[1]; if(m==3){ rinv(s.w[1],s.l[1],b); bp=b; } n=cat(s.w[0],s.l[0],bp,s.l[1],t); if(n+s.l[1]>CAP) return false; memcpy(r.w[0],t,n); r.l[0]=n; return true; }
  if(m==4||m==5){ u8 b[64]; const u8*bp=s.w[0]; if(m==5){ rinv(s.w[0],s.l[0],b); bp=b; } n=cat(s.w[1],s.l[1],bp,s.l[0],t); if(n+s.l[0]>CAP) return false; memcpy(r.w[1],t,n); r.l[1]=n; return true; }
  int j=(m<=9)?0:1; int g=(m<=9)?m-6:m-10; // generator codes 0..3 = x X y Y
  // reduce(g w g^-1)
  u8 u[70]; int k=0; const u8*w=s.w[j]; int nw=s.l[j];
  if(nw&&w[0]==(g^1)){ // g cancels with first letter
    for(int i=1;i<nw;i++) u[k++]=w[i];
  } else { u[k++]=g; for(int i=0;i<nw;i++) u[k++]=w[i]; }
  // append g^-1
  if(k&&u[k-1]==g) { /* g followed by g^-1 cancels */ k--; } else u[k++]=g^1;
  int other=s.l[1-j];
  if(k+other>CAP) return false;
  memcpy(r.w[j],u,k); r.l[j]=k; return true;
}
static const int INV[14]={0,1,3,2,5,4,7,6,9,8,11,10,13,12};
static inline u64 mix(u64 x){ x^=x>>33; x*=0xff51afd7ed558ccdULL; x^=x>>33; x*=0xc4ceb9fe1a85ec53ULL; x^=x>>33; return x; }
static void hsh(const St&s,u64&a,u64&b){ u64 h1=1469598103934665603ULL,h2=0x9e3779b97f4a7c15ULL; for(int j=0;j<2;j++){ h1=mix(h1^(s.l[j]+77)); h2=mix(h2+s.l[j]*1315423911ULL+5); for(int i=0;i<s.l[j];i++){ h1=(h1^s.w[j][i])*1099511628211ULL; h2=mix(h2^(u64)s.w[j][i]*0x100000001b3ULL+i); } h1=mix(h1); } a=h1; b=h2; }
struct Node{ u64 a,b; int32_t par; u8 mv; };
struct Side{
  vector<Node> nodes; vector<u32> tab; u64 mask; 
  void init(int lg){ tab.assign(1ULL<<lg,0xFFFFFFFFu); mask=(1ULL<<lg)-1; }
  int find(u64 a,u64 b) const { u64 k=a&mask; while(tab[k]!=0xFFFFFFFFu){ const Node&n=nodes[tab[k]]; if(n.a==a&&n.b==b) return tab[k]; k=(k+1)&mask; } return -1; }
  void grow(){ u64 nm=(mask+1)*2-1; vector<u32> t2(nm+1,0xFFFFFFFFu); for(u32 i=0;i<nodes.size();i++){ u64 k=nodes[i].a&nm; while(t2[k]!=0xFFFFFFFFu) k=(k+1)&nm; t2[k]=i; } tab.swap(t2); mask=nm; }
  int add(u64 a,u64 b,int par,u8 mv){ if((nodes.size()+1)*2>mask+1) grow(); u64 k=a&mask; while(tab[k]!=0xFFFFFFFFu) k=(k+1)&mask; nodes.push_back({a,b,par,mv}); tab[k]=nodes.size()-1; return nodes.size()-1; }
};
static bool parse_word(const string&s,u8*o,int&n){ n=0; for(char c:s){ int v=c=='x'?0:c=='X'?1:c=='y'?2:c=='Y'?3:-1; if(v<0) return false; o[n++]=v; } return true; }
int main(int argc,char**argv){
  if(argc<7){ fprintf(stderr,"usage\n"); return 2; }
  CAP=atoi(argv[1]); int MAXTOT=atoi(argv[2]); u64 MAXST=strtoull(argv[3],0,10);
  auto mk=[&](const string&a,const string&b,St&s){ int n; memset(&s,0,sizeof s); parse_word(a,s.w[0],n); s.l[0]=n; parse_word(b,s.w[1],n); s.l[1]=n; };
  St start; mk(argv[4],argv[5],start);
  struct Src{ St s; int lvl; }; vector<Src> srcs;
  for(int i=6;i<argc;i++){ string t=argv[i]; size_t at=t.find('@'), cm=t.find(','); Src sr; mk(t.substr(0,cm),t.substr(cm+1,at-cm-1),sr.s); sr.lvl=atoi(t.c_str()+at+1); srcs.push_back(sr); }
  sort(srcs.begin(),srcs.end(),[](const Src&a,const Src&b){return a.lvl<b.lvl;});
  int base=srcs[0].lvl;
  Side F,B; F.init(20); B.init(20);
  auto rec=[&](const St&s,vector<u8>&buf){ buf.push_back(s.l[0]); buf.push_back(s.l[1]); buf.insert(buf.end(),s.w[0],s.w[0]+s.l[0]); buf.insert(buf.end(),s.w[1],s.w[1]+s.l[1]); };
  auto rd=[&](const vector<u8>&buf,size_t&p,St&s){ s.l[0]=buf[p++]; s.l[1]=buf[p++]; memcpy(s.w[0],&buf[p],s.l[0]); p+=s.l[0]; memcpy(s.w[1],&buf[p],s.l[1]); p+=s.l[1]; };
  vector<u8> ff,fb; // frontiers
  u64 a,b; hsh(start,a,b); F.add(a,b,-1,0); rec(start,ff); int fd=0; size_t nf=1;
  size_t si=0; int blvl=base; size_t nb=0;
  while(si<srcs.size()&&srcs[si].lvl==base){ hsh(srcs[si].s,a,b); if(B.find(a,b)<0){ B.add(a,b,-1,0); rec(srcs[si].s,fb); nb++; } si++; }
  long best=1L<<30; int bi_f=-1,bi_b=-1;
  { hsh(start,a,b); int j=B.find(a,b); if(j>=0){ best=0+ (0); bi_f=0; bi_b=j; } }
  // dict of lvl per backward node is implicit: layers; store layer index via vector
  vector<int> blv; blv.assign(B.nodes.size(),base);
  auto total_of=[&](int fdepth,int blevel){ return fdepth+blevel; };
  int result_found=(best<(1L<<30));
  vector<int> fdep; fdep.push_back(0);
  while(!result_found){
    if((u64)(F.nodes.size()+B.nodes.size())>MAXST){ printf("NONE maxstates fwd_depth %d bwd_level %d fstates %zu bstates %zu cap %d\n",fd,blvl,F.nodes.size(),B.nodes.size(),CAP); return 0; }
    if(fd+(blvl-base)>=MAXTOT){ printf("NONE maxtot fwd_depth %d bwd_level %d fstates %zu bstates %zu cap %d\n",fd,blvl,F.nodes.size(),B.nodes.size(),CAP); return 0; }
    if(nf==0&&nb==0){ printf("NONE closed fwd_depth %d bwd_level %d fstates %zu bstates %zu cap %d\n",fd,blvl,F.nodes.size(),B.nodes.size(),CAP); return 0; }
    bool expandF = (nf>0) && (nb==0 || nf<=nb);
    if(expandF){
      vector<u8> nfb; size_t nn=0; size_t p=0; St cur,nx; int nd=fd+1;
      size_t start_idx=F.nodes.size();
      // need parent indices: frontier nodes are the last nf nodes of F in order
      size_t firstIdx=F.nodes.size()-nf; size_t idx=firstIdx;
      while(p<ff.size()){ rd(ff,p,cur); for(int m=0;m<14;m++){ if(!applym(cur,m,nx)) continue; hsh(nx,a,b); if(F.find(a,b)>=0) continue; int id=F.add(a,b,idx,m); rec(nx,nfb); nn++; int j=B.find(a,b); if(j>=0){ long tot=nd+blv[j]-base; if(tot<best){ best=tot; bi_f=id; bi_b=j; } } } idx++; }
      ff.swap(nfb); nf=nn; fd=nd;
    } else {
      vector<u8> nbb; size_t nn=0; size_t p=0; St cur,nx; int nl=blvl+1;
      size_t firstIdx=B.nodes.size()-nb; size_t idx=firstIdx;
      while(p<fb.size()){ rd(fb,p,cur); for(int m=0;m<14;m++){ if(!applym(cur,m,nx)) continue; hsh(nx,a,b); if(B.find(a,b)>=0) continue; int id=B.add(a,b,idx,INV[m]); blv.push_back(nl); rec(nx,nbb); nn++; int j=F.find(a,b); if(j>=0){ long tot=fd+(nl-base); if(tot<best){ best=tot; bi_f=j; bi_b=id; } } } idx++; }
      while(si<srcs.size()&&srcs[si].lvl==nl){ hsh(srcs[si].s,a,b); if(B.find(a,b)<0){ int id=B.add(a,b,-1,0); blv.push_back(nl); rec(srcs[si].s,nbb); nn++; int j=F.find(a,b); if(j>=0){ long tot=fd+(nl-base); if(tot<best){ best=tot; bi_f=j; bi_b=id; } } } si++; }
      fb.swap(nbb); nb=nn; blvl=nl;
    }
    fprintf(stderr,"cap %d fwd d=%d n=%zu | bwd lvl=%d n=%zu | totF=%zu totB=%zu best=%ld\n",CAP,fd,nf,blvl,nb,F.nodes.size(),B.nodes.size(),best<(1L<<30)?best:-1L);
    if(best<(1L<<30)) result_found=1;
  }
  // path
  vector<int> fm; for(int i=bi_f;F.nodes[i].par>=0;i=F.nodes[i].par) fm.push_back(F.nodes[i].mv); reverse(fm.begin(),fm.end());
  vector<int> bm; for(int i=bi_b;B.nodes[i].par>=0;i=B.nodes[i].par) bm.push_back(B.nodes[i].mv);
  int srcLevelOfChain=blv[bi_b]; 
  printf("RESULT prefix_len %zu (fwd %zu bwd_steps %zu) bwd_level_of_meet %d base %d cap %d\nPATH",fm.size()+bm.size(),fm.size(),bm.size(),srcLevelOfChain,base,CAP);
  for(int m:fm) printf(" %d",m); for(int m:bm) printf(" %d",m); printf("\n");
  return 0;
}
