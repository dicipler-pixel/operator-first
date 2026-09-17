// Earth–Moon 19: actual planar-layer search, standard C++17.
// Build: g++ -O3 -std=c++17 planar_search.cpp -o planar_search
// Usage: planar_search input.faces seed proposals mode output.json
// Modes: single, macro, hybrid, weighted. Output contains a replayable path.
// Labels are 0..18. Input is the 68 face triples of two spherical triangulations.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
#include <stdexcept>
#include <chrono>
using namespace std;
constexpr int N=19,M=171,F=34;
int EU[M],EV[M],EI[N][N],tid[N][N][N];
int pc(uint32_t x){return __builtin_popcount(x);} int low64(uint64_t x){return __builtin_ctzll(x);}
struct Flip{int layer,k,old,neu,i,j;array<int,3> fi,fj;};
struct Step{int type,w,a,b,c,d;};
struct Tri{
 array<array<int,3>,F> f; array<uint64_t,M> inc{};array<int,51> es{};array<int,M> pos{};
 void faceadd(int i,int sign){auto a=f[i];for(int k=0;k<3;k++){int e=EI[a[k]][a[(k+1)%3]];if(sign>0)inc[e]|=1ull<<i;else inc[e]&=~(1ull<<i);}}
 void rebuild(){inc.fill(0);pos.fill(-1);for(int i=0;i<F;i++){sort(f[i].begin(),f[i].end());faceadd(i,1);}int n=0;for(int e=0;e<M;e++)if(inc[e]){if(__builtin_popcountll(inc[e])!=2||n>=51)throw runtime_error("face incidence");pos[e]=n;es[n++]=e;}if(n!=51)throw runtime_error("edge count");}
 bool proposal(int k,int w,Flip &r)const{int e=es[k];uint64_t z=inc[e];int i=low64(z);z&=z-1;int j=low64(z);int a=-1,b=-1;for(int v:f[i])if(v!=EU[e]&&v!=EV[e])a=v;for(int v:f[j])if(v!=EU[e]&&v!=EV[e])b=v;if(a==b||a<0||b<0)return false;int en=EI[a][b];if(inc[en])return false;r={w,k,e,en,i,j,f[i],f[j]};return true;}
 void apply(const Flip&r){faceadd(r.i,-1);faceadd(r.j,-1);f[r.i]={EU[r.old],EU[r.neu],EV[r.neu]};f[r.j]={EV[r.old],EU[r.neu],EV[r.neu]};sort(f[r.i].begin(),f[r.i].end());sort(f[r.j].begin(),f[r.j].end());faceadd(r.i,1);faceadd(r.j,1);es[r.k]=r.neu;pos[r.neu]=r.k;pos[r.old]=-1;}
 void undo(const Flip&r){faceadd(r.i,-1);faceadd(r.j,-1);f[r.i]=r.fi;f[r.j]=r.fj;faceadd(r.i,1);faceadd(r.j,1);es[r.k]=r.old;pos[r.old]=r.k;pos[r.neu]=-1;}
 void swaplabels(int a,int b){for(auto &ff:f)for(int&v:ff){if(v==a)v=b;else if(v==b)v=a;}rebuild();}
};
struct State{
 Tri t[2];array<uint32_t,N> h{};int triangles=0,overlap=0;
 void recalc(){overlap=0;for(int i=0;i<N;i++)h[i]=((1u<<N)-1)^(1u<<i);for(int e=0;e<M;e++){if(t[0].inc[e]&&t[1].inc[e])overlap++;if(t[0].inc[e]||t[1].inc[e]){h[EU[e]]&=~(1u<<EV[e]);h[EV[e]]&=~(1u<<EU[e]);}}triangles=0;for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)if(h[a]>>b&1)triangles+=pc(h[a]&h[b]);triangles/=3;}
 pair<int,int> delta(const Flip&r)const{bool a=t[1-r.layer].inc[r.old],b=t[1-r.layer].inc[r.neu];return {(a?0:pc(h[EU[r.old]]&h[EV[r.old]]))-(b?0:pc(h[EU[r.neu]]&h[EV[r.neu]])),int(b)-int(a)};}
 void changeh(int e,bool add){int a=EU[e],b=EV[e];if(add){h[a]|=1u<<b;h[b]|=1u<<a;}else{h[a]&=~(1u<<b);h[b]&=~(1u<<a);}}
 void apply(const Flip&r){auto d=delta(r);if(!t[1-r.layer].inc[r.old])changeh(r.old,true);if(!t[1-r.layer].inc[r.neu])changeh(r.neu,false);t[r.layer].apply(r);triangles+=d.first;overlap+=d.second;}
 void undo(const Flip&r){t[r.layer].undo(r);if(!t[1-r.layer].inc[r.old])changeh(r.old,false);if(!t[1-r.layer].inc[r.neu])changeh(r.neu,true);auto d=delta(r);triangles-=d.first;overlap-=d.second;}
 void audit()const{State s=*this;s.t[0].rebuild();s.t[1].rebuild();s.recalc();if(s.h!=h||s.triangles!=triangles||s.overlap!=overlap)throw runtime_error("incremental drift");}
};
Step stepof(const Flip&r){return {0,r.layer,EU[r.old],EV[r.old],EU[r.neu],EV[r.neu]};}
void write(const string &path,const State&s,const vector<Step>&moves,int seed,long long it,long long attempts,long long legal,long long accepted,long long audits,string mode,double seconds,bool final){ofstream o(path);if(!o)throw runtime_error("output");o<<"{\"n\":19,\"producer\":\"planar_search_cpp\",\"mode\":\""<<mode<<"\",\"seed\":"<<seed<<",\"iteration_of_best\":"<<it<<",\"attempted_proposals\":"<<attempts<<",\"legal_atomic_proposals\":"<<legal<<",\"accepted_atomic_moves\":"<<accepted<<",\"full_recounts\":"<<audits<<",\"seconds\":"<<seconds<<",\"run_complete\":"<<(final?"true":"false")<<",\"independent_triples\":"<<s.triangles<<",\"overlap\":"<<s.overlap<<",\"union_edges\":"<<102-s.overlap<<",\"faces\":[";for(int w=0;w<2;w++){if(w)o<<",";o<<"[";for(int i=0;i<F;i++){if(i)o<<",";auto f=s.t[w].f[i];o<<"["<<f[0]<<","<<f[1]<<","<<f[2]<<"]";}o<<"]";}o<<"],\"path\":[";for(size_t k=0;k<moves.size();k++){if(k)o<<",";auto m=moves[k];o<<"["<<m.type<<","<<m.w<<","<<m.a<<","<<m.b<<","<<m.c<<","<<m.d<<"]";}o<<"]}\n";}
int main(int argc,char**argv){try{
 if(argc!=6){cerr<<"usage: planar_search input.faces seed proposals single|macro|hybrid|weighted output.json\n";return 2;}
 int ei=0;for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){EU[ei]=a;EV[ei]=b;EI[a][b]=EI[b][a]=ei++;}
 int ti=0;for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++){array<int,3>x={a,b,c};do{tid[x[0]][x[1]][x[2]]=ti;}while(next_permutation(x.begin(),x.end()));ti++;}
 State initial;ifstream in(argv[1]);for(int w=0;w<2;w++)for(auto &f:initial.t[w].f)for(int &v:f){if(!(in>>v)||v<0||v>=N)throw runtime_error("bad input");}for(auto &t:initial.t)t.rebuild();initial.recalc();initial.audit();
 int seed=stoi(argv[2]);long long total=stoll(argv[3]);string mode=argv[4],out=argv[5];if(total<1|| (mode!="single"&&mode!="macro"&&mode!="hybrid"&&mode!="weighted"))throw runtime_error("parameters");
 mt19937_64 rng(seed);auto unit=[&](){return generate_canonical<double,53>(rng);};
 State s=initial,best=initial;vector<Step>path,bestpath;long long accepted=0,legal=0,attempts=0,audits=1,bit=0;
 auto begin=chrono::steady_clock::now();auto elapsed=[&](){return chrono::duration<double>(chrono::steady_clock::now()-begin).count();};
 auto keep=[&](long long it,const vector<Step>&extra){if(make_pair(s.triangles,s.overlap)<make_pair(best.triangles,best.overlap)){s.audit();audits++;best=s;bestpath=path;bestpath.insert(bestpath.end(),extra.begin(),extra.end());bit=it;write(out,best,bestpath,seed,bit,attempts,legal,accepted,audits,mode,elapsed(),false);cout<<"BEST "<<seed<<" "<<mode<<" step "<<it<<" triples "<<best.triangles<<" overlap "<<best.overlap<<" path "<<bestpath.size()<<endl;}};
 vector<double> weights(969,1.);array<array<long long,M>,2>tabu{};
 long long period=mode=="weighted"?20000:200000;
 for(long long it=0;it<total;it++){
  attempts++;
  if(it&&it%period==0){s=initial;path.clear();weights.assign(969,1.);for(auto& a:tabu)a.fill(0);}
  if(mode=="weighted"){
   // Breakout: persistent unsatisfied triples gain weight; true count remains the target.
   if(it%7==0)for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)if(s.h[a]>>b&1){uint32_t z=s.h[a]&s.h[b]&(~0u<<(b+1));while(z){int c=__builtin_ctz(z);z&=z-1;weights[tid[a][b][c]]+=.7;}}
   if(it%300==299)for(auto&w:weights)w=1.+.85*(w-1.);
   double low=1e100;Flip chosen{};bool got=false;int ties=0;
   for(int w=0;w<2;w++)for(int k=0;k<51;k++){
    Flip r;if(!s.t[w].proposal(k,w,r))continue;legal++;auto d=s.delta(r);
    if(tabu[w][r.old]>it&&s.triangles+d.first>=best.triangles)continue;
    double change=.15*d.second;
    if(!s.t[1-w].inc[r.old]){uint32_t z=s.h[EU[r.old]]&s.h[EV[r.old]];while(z){int c=__builtin_ctz(z);z&=z-1;change+=weights[tid[EU[r.old]][EV[r.old]][c]];}}
    if(!s.t[1-w].inc[r.neu]){uint32_t z=s.h[EU[r.neu]]&s.h[EV[r.neu]];while(z){int c=__builtin_ctz(z);z&=z-1;change-=weights[tid[EU[r.neu]][EV[r.neu]][c]];}}
    if(change<low-1e-8){low=change;chosen=r;got=true;ties=1;}else if(abs(change-low)<1e-8&&rng()%++ties==0)chosen=r;
   }
   if(!got)continue;s.apply(chosen);vector<Step>extra={stepof(chosen)};keep(it+1,extra);path.push_back(extra[0]);accepted++;tabu[chosen.layer][chosen.neu]=it+3+rng()%13;
  }else{
   double temp=1.9*(1.-double(it%period)/period)+.035;
   if(mode=="hybrid"&&rng()%30==0){
    int w=rng()%2,a=rng()%N,b=rng()%(N-1);if(b>=a)b++;int oldt=s.triangles,oldo=s.overlap;
    s.t[w].swaplabels(a,b);s.recalc();vector<Step>extra={{1,w,a,b,0,0}};legal++;keep(it+1,extra);
    double delta=s.triangles-oldt+.15*(s.overlap-oldo);
    if(s.triangles==0||delta<=0||unit()<exp(-delta/temp)){path.push_back(extra[0]);accepted++;}else{s.t[w].swaplabels(a,b);s.recalc();}
   }else{
    int len=mode=="single"?1:(rng()%10<5?1:2+rng()%6);int oldt=s.triangles,oldo=s.overlap;vector<Flip>rs;vector<Step>extra;
    for(int j=0;j<len;j++){int w=rng()%2;Flip r;if(!s.t[w].proposal(rng()%51,w,r))continue;legal++;s.apply(r);rs.push_back(r);extra.push_back(stepof(r));keep(it+1,extra);if(s.triangles==0)break;}
    double delta=s.triangles-oldt+.15*(s.overlap-oldo);
    if(s.triangles==0||delta<=0||unit()<exp(-delta/temp)){path.insert(path.end(),extra.begin(),extra.end());accepted+=rs.size();}else for(auto r=rs.rbegin();r!=rs.rend();++r)s.undo(*r);
   }
  }
  if(it%10000==9999){s.audit();audits++;}
  if(best.triangles==0)break;
 }
 s.audit();best.audit();audits+=2;write(out,best,bestpath,seed,bit,attempts,legal,accepted,audits,mode,elapsed(),true);
 cout<<"DONE "<<seed<<" "<<mode<<" best "<<best.triangles<<" overlap "<<best.overlap<<" attempts "<<attempts<<" legal "<<legal<<" accepted "<<accepted<<" seconds "<<elapsed()<<endl;
 return 0;
 }catch(exception&e){cerr<<"ERROR "<<e.what()<<endl;return 2;}}
