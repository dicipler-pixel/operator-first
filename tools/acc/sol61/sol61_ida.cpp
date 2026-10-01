// Independent non-beam ac-r2-v1 solver. No row data or known roads embedded.
// Build: g++ -O3 -std=c++20 sol61_ida.cpp -o sol61_ida
// Input file: four whitespace-separated words (start r0, start r1, goal r0, goal r1).
// Words use x X y Y; '-' means the empty word. Only free reduction is performed.
// Example CLI: --input control_words.txt --depth 23 --cap 32 --ball 8
//   --ball-cap 36 --ball-states 4000000 --tt-states 2000000 --seconds 600
// A stopped run never certifies the interrupted depth. Complete depths certify
// absence only under --cap, with all 14 moves and both words fully ordered.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using Clock=std::chrono::steady_clock;
using Word=std::string;
struct State { Word a,b; };
static constexpr int im[14]={0,1,3,2,5,4,7,6,9,8,11,10,13,12};
static constexpr unsigned char gg[4]={1,2,3,4};
static unsigned char inv(unsigned char a) { return ((a-1)^1)+1; }
static Word inverse(const Word&w) { Word o; o.reserve(w.size()); for(auto i=w.rbegin();i!=w.rend();++i)o.push_back(inv(*i));return o; }
static void append(Word&o,unsigned char a) { if(!o.empty() && (unsigned char)o.back()==inv(a))o.pop_back();else o.push_back(a); }
static Word reduce(const Word&w) { Word o;o.reserve(w.size());for(unsigned char a:w)append(o,a);return o; }
static Word mul(const Word&a,const Word&b,bool invert_b=false) { Word o=a;o.reserve(a.size()+b.size());if(invert_b){for(auto i=b.rbegin();i!=b.rend();++i)append(o,inv(*i));}else for(unsigned char c:b)append(o,c);return o; }
static Word conj(const Word&w,unsigned char g) { Word o;o.reserve(w.size()+2);append(o,g);for(unsigned char c:w)append(o,c);append(o,inv(g));return o; }
static State move(const State&s,int m) { State t=s;switch(m){case 0:t.a=inverse(s.a);break;case 1:t.b=inverse(s.b);break;case 2:t.a=mul(s.a,s.b);break;case 3:t.a=mul(s.a,s.b,true);break;case 4:t.b=mul(s.b,s.a);break;case 5:t.b=mul(s.b,s.a,true);break;default:if(m<10)t.a=conj(s.a,gg[m-6]);else t.b=conj(s.b,gg[m-10]);}return t; }
static std::string key(const State&s) { std::string k=s.a;k.push_back(0);k+=s.b;return k; }
static State unkey(const std::string&k) {auto z=k.find(char(0));return {k.substr(0,z),k.substr(z+1)};}
static Word parse(const std::string&s){Word w;if(s=="-")return w;for(char c:s){unsigned char q;if(c=='x')q=1;else if(c=='X')q=2;else if(c=='y')q=3;else if(c=='Y')q=4;else throw std::runtime_error("bad word character");w.push_back(q);}if(reduce(w)!=w)throw std::runtime_error("input word not freely reduced");return w;}
static std::string show(const Word&w){std::string o;for(unsigned char a:w)o.push_back("xXyY"[a-1]);return o.empty()?"-":o;}
using Matrix=std::array<int,4>;
static Matrix exponent(const State&s){Matrix e{};for(unsigned char a:s.a)e[(a-1)/2]+=(a&1)?1:-1;for(unsigned char a:s.b)e[2+(a-1)/2]+=(a&1)?1:-1;return e;}
static Matrix emove(Matrix a,int m){if(m<2){int q=2*m;a[q]=-a[q];a[q+1]=-a[q+1];}else if(m<6){int q=m<4?0:2,j=2-q,sign=(m&1)?-1:1;a[q]+=sign*a[j];a[q+1]+=sign*a[j+1];}return a;}
struct ModPDB { int p;std::vector<uint8_t>d;int norm(int x)const{x%=p;return x<0?x+p:x;}int code(const Matrix&a)const{int z=0;for(int x:a)z=z*p+norm(x);return z;}Matrix decode(int z)const{Matrix a;for(int i=3;i>=0;--i){a[i]=z%p;z/=p;}return a;}
 explicit ModPDB(int pp,const Matrix&goal):p(pp),d(size_t(p)*p*p*p,255){std::vector<int>q;int z=code(goal);d[z]=0;q.push_back(z);for(size_t h=0;h<q.size();++h){int u=q[h];auto a=decode(u);for(int m=0;m<6;++m){int v=code(emove(a,m));if(d[v]==255){d[v]=d[u]+1;q.push_back(v);}}}std::cout<<"mod_pdb p="<<p<<" states="<<q.size()<<"\n";}
 int h(const Matrix&a)const{return d[code(a)]==255?1000:d[code(a)];}
};
// Finite nonabelian pattern databases from SL(2,p); word evaluation commutes
// exactly with all 14 official moves. Their distances are lower bounds.
struct Group {int p,n;std::vector<Matrix>a;std::vector<int>ix;std::vector<uint16_t>mt,in;int one,x,y;
 int norm(int z)const{z%=p;return z<0?z+p:z;}int code(Matrix v)const{int z=0;for(int t:v)z=z*p+norm(t);return z;}int prod(int u,int v)const{return mt[size_t(u)*n+v];}
 explicit Group(int pp):p(pp),ix(size_t(p)*p*p*p,-1){for(int A=0;A<p;++A)for(int B=0;B<p;++B)for(int C=0;C<p;++C)for(int D=0;D<p;++D)if(norm(A*D-B*C)==1){Matrix z{A,B,C,D};ix[code(z)]=a.size();a.push_back(z);}n=a.size();one=ix[code({1,0,0,1})];x=ix[code({1,1,0,1})];y=ix[code({1,0,1,1})];mt.resize(size_t(n)*n);in.resize(n);for(int i=0;i<n;++i){auto A=a[i];in[i]=ix[code({A[3],-A[1],-A[2],A[0]})];for(int j=0;j<n;++j){auto B=a[j];mt[size_t(i)*n+j]=ix[code({A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3]})];}}}
};
struct FinitePDB {const Group*g;std::array<int,4>gens;std::vector<uint8_t>d;
 int advance(int z,int m)const{int a=z/g->n,b=z%g->n;if(m==0)a=g->in[a];else if(m==1)b=g->in[b];else if(m==2)a=g->prod(a,b);else if(m==3)a=g->prod(a,g->in[b]);else if(m==4)b=g->prod(b,a);else if(m==5)b=g->prod(b,g->in[a]);else{int c=gens[(m-6)%4];if(m<10)a=g->prod(g->prod(c,a),g->in[c]);else b=g->prod(g->prod(c,b),g->in[c]);}return a*g->n+b;}
 int evalword(const Word&w)const{int a=g->one;for(unsigned char c:w)a=g->prod(a,gens[c-1]);return a;}int eval(const State&s)const{return evalword(s.a)*g->n+evalword(s.b);}
 FinitePDB(const Group*ggg,int x,int y,const State&goal):g(ggg),gens{x,(int)g->in[x],y,(int)g->in[y]},d(size_t(g->n)*g->n,255){int z=eval(goal);std::vector<int>q;d[z]=0;q.push_back(z);for(size_t h=0;h<q.size();++h){int u=q[h];for(int m=0;m<14;++m){int v=advance(u,m);if(d[v]==255){d[v]=d[u]+1;q.push_back(v);}}}std::cout<<"finite_pdb SL2 p="<<g->p<<" x="<<x<<" y="<<y<<" states="<<q.size()<<"\n";}
 int h(int z)const{return d[z]==255?1000:d[z];}
};
struct BallRecord{uint32_t parent;uint8_t m,depth;};
struct Config{std::string input;int depth=23,cap=32,ball=8,ballcap=36,seconds=600;size_t ballstates=4000000,ttstates=2000000;};
struct Solver{
 Config c;State start,goal;Clock::time_point began;std::unordered_map<std::string,uint32_t>ball;std::vector<const std::string*>bk;std::vector<BallRecord>br;std::unordered_map<std::string,uint8_t>tt;std::vector<ModPDB>mods;Group g5{5},g7{7};std::vector<FinitePDB>finite;std::vector<int>path,solution;uint64_t nodes=0;int completeball=0;bool interrupted=false;uint64_t ttclears=0;
 explicit Solver(Config cc,State s,State t):c(cc),start(std::move(s)),goal(std::move(t)),began(Clock::now()){}
 double elapsed()const{return std::chrono::duration<double>(Clock::now()-began).count();}bool expired(){if(elapsed()>=c.seconds){interrupted=true;return true;}return false;}
 void makepdb(){auto e=exponent(goal);for(int p:{7,11,31})mods.emplace_back(p,e);for(const Group*g:{&g5,&g7}){finite.emplace_back(g,g->x,g->y,goal);finite.emplace_back(g,g->in[g->x],g->y,goal);}}
 void makeball(){ball.reserve(std::min<size_t>(c.ballstates,1000000));auto [it,_]=ball.emplace(key(goal),0);bk.push_back(&it->first);br.push_back({0,0,0});size_t begin=0,end=1;for(int d=1;d<=c.ball;++d){bool full=true;size_t nextbegin=end;for(size_t i=begin;i<end;++i){if((i&4095)==0&&expired()){full=false;break;}State s=unkey(*bk[i]);for(int m=0;m<14;++m){auto t=move(s,m);if(t.a.size()+t.b.size()>size_t(c.ballcap))continue;auto k=key(t);if(ball.find(k)!=ball.end())continue;if(br.size()>=c.ballstates){full=false;break;}uint32_t j=br.size();auto [jt,inserted]=ball.emplace(std::move(k),j);if(inserted){bk.push_back(&jt->first);br.push_back({uint32_t(i),uint8_t(m),uint8_t(d)});}}if(!full)break;}std::cout<<"ball layer="<<d<<" total="<<br.size()<<" complete="<<(full?"yes":"no")<<" elapsed="<<elapsed()<<"\n"<<std::flush;if(!full)break;completeball=d;begin=nextbegin;end=br.size();if(begin==end)break;} }
 int heuristic(const Matrix&e,const std::vector<int>&f,size_t length)const{int h=0;for(auto&p:mods)h=std::max(h,p.h(e));for(size_t i=0;i<finite.size();++i)h=std::max(h,finite[i].h(f[i]));uint64_t bound=2;int steps=0;while(bound<length&&steps<62){bound=std::max(bound+2,2*bound-1);++steps;}return std::max(h,steps);}
 bool dfs(const State&s,const Matrix&e,const std::vector<int>&f,int rem,int last){++nodes;if((nodes&16383)==0){if(expired())return false;if((nodes&4194303)==0)std::cout<<"progress nodes="<<nodes<<" elapsed="<<elapsed()<<" tt="<<tt.size()<<"\n"<<std::flush;}
  auto k=key(s);auto bit=ball.find(k);if(bit!=ball.end()&&br[bit->second].depth<=rem){solution=path;for(uint32_t j=bit->second;j!=0;j=br[j].parent)solution.push_back(im[br[j].m]);return true;}
  if(rem==0)return false;
  if(c.ballcap>=c.cap&&rem<=completeball)return false;
  if(heuristic(e,f,s.a.size()+s.b.size())>rem)return false;
  if(c.ttstates){auto it=tt.find(k);if(it!=tt.end()&&it->second>=rem)return false;if(tt.size()>=c.ttstates){tt.clear();++ttclears;}tt[std::move(k)]=uint8_t(rem);}
  struct Child{State s;Matrix e;std::vector<int>f;int m,score;};std::vector<Child>children;children.reserve(14);for(int m=0;m<14;++m){if(last>=0&&m==im[last])continue;auto t=move(s,m);if(t.a==s.a&&t.b==s.b)continue;auto len=t.a.size()+t.b.size();if(len>size_t(c.cap))continue;auto ee=emove(e,m);std::vector<int>ff;ff.reserve(finite.size());for(size_t i=0;i<finite.size();++i)ff.push_back(finite[i].advance(f[i],m));int h=heuristic(ee,ff,len);if(h>rem-1)continue;int score=h*1000+int(len)*10+m;auto z=ball.find(key(t));if(z!=ball.end())score=-100000+br[z->second].depth;children.push_back({std::move(t),ee,std::move(ff),m,score});}
  std::sort(children.begin(),children.end(),[](const Child&a,const Child&b){return a.score<b.score;});for(auto&t:children){path.push_back(t.m);bool found=dfs(t.s,t.e,t.f,rem-1,t.m);path.pop_back();if(found)return true;if(interrupted)return false;}return false;
 }
 bool run(){makepdb();makeball();if(interrupted)return false;auto e=exponent(start);std::vector<int>f;for(auto&p:finite)f.push_back(p.eval(start));int first=heuristic(e,f,start.a.size()+start.b.size());for(int d=first;d<=c.depth;++d){tt.clear();uint64_t before=nodes;std::cout<<"search depth="<<d<<" cap="<<c.cap<<" ball_complete="<<completeball<<" elapsed="<<elapsed()<<"\n"<<std::flush;if(dfs(start,e,f,d,-1)){std::cout<<"FOUND length="<<solution.size()<<" elapsed="<<elapsed()<<" nodes="<<nodes<<"\nMOVES [";for(size_t i=0;i<solution.size();++i){if(i)std::cout<<", ";std::cout<<solution[i];}std::cout<<"]\n";return true;}std::cout<<"search depth="<<d<<" nodes="<<(nodes-before)<<" status="<<(interrupted?"incomplete":"complete_no_path")<<" cap="<<c.cap<<" elapsed="<<elapsed()<<"\n"<<std::flush;if(interrupted)break;}std::cout<<"STOP status="<<(interrupted?"incomplete":"complete_no_path")<<" nodes="<<nodes<<" tt_clears="<<ttclears<<" elapsed="<<elapsed()<<"\n";return false;}
};
int main(int argc,char**argv){try{if(argc==3 && std::string(argv[1])=="--dump-neighbors"){std::ifstream in(argv[2]);std::string a,b;if(!(in>>a>>b))throw std::runtime_error("input needs start0 start1");State s{parse(a),parse(b)};for(int m=0;m<14;++m){auto t=move(s,m);std::cout<<m<<" "<<show(t.a)<<" "<<show(t.b)<<"\n";}return 0;}Config c;for(int i=1;i<argc;++i){std::string k=argv[i];if(i+1>=argc)throw std::runtime_error("missing flag value");std::string v=argv[++i];if(k=="--input")c.input=v;else if(k=="--depth")c.depth=std::stoi(v);else if(k=="--cap")c.cap=std::stoi(v);else if(k=="--ball")c.ball=std::stoi(v);else if(k=="--ball-cap")c.ballcap=std::stoi(v);else if(k=="--ball-states")c.ballstates=std::stoull(v);else if(k=="--tt-states")c.ttstates=std::stoull(v);else if(k=="--seconds")c.seconds=std::stoi(v);else throw std::runtime_error("unknown flag: "+k);}if(c.input.empty()||c.depth<0||c.depth>254||c.cap<2||c.ball<0||c.ball>254||c.ballcap<2||c.seconds<1||c.ballstates<1||c.ballstates>=UINT32_MAX)throw std::runtime_error("invalid configuration");std::ifstream in(c.input);std::string a,b,x,y;if(!(in>>a>>b>>x>>y))throw std::runtime_error("input needs start0 start1 goal0 goal1 words");State s{parse(a),parse(b)},t{parse(x),parse(y)};if(s.a.size()+s.b.size()>size_t(c.cap))throw std::runtime_error("start exceeds cap");if(t.a.size()!=1||t.b.size()!=1)throw std::runtime_error("goal must have two unit relators for length heuristic");if(t.a.size()+t.b.size()>size_t(c.ballcap))throw std::runtime_error("goal exceeds ball cap");auto e=exponent(s),f=exponent(t);int64_t ds=int64_t(e[0])*e[3]-int64_t(e[1])*e[2],dt=int64_t(f[0])*f[3]-int64_t(f[1])*f[2];if(std::abs(ds)!=1||std::abs(dt)!=1)throw std::runtime_error("solver length bound requires determinant +/-1 for start and goal");std::cout<<"SOL61_IDA ac-r2-v1 start="<<show(s.a)<<","<<show(s.b)<<" goal="<<show(t.a)<<","<<show(t.b)<<" depth="<<c.depth<<" cap="<<c.cap<<" ball="<<c.ball<<" ball_cap="<<c.ballcap<<" ball_states="<<c.ballstates<<" tt_states="<<c.ttstates<<" seconds="<<c.seconds<<"\n"<<std::flush;Solver solver(c,s,t);return solver.run()?0:2;}catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 1;}}
