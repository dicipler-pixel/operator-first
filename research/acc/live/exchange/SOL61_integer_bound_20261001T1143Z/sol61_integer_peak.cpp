// Exact 96-bit tables. Goal paths are recovered through decreasing distances.
// Full state keys: 64 letter bits + 12 letter bits + two 6-bit word lengths.
#define SOL61_COMPACT_NO_MAIN
#include "sol61_compact.cpp"
#include <memory>

struct SlimKey {uint64_t lo;uint32_t hi;};
struct SlimSlot {uint32_t lo0=0,lo1=0,hi=0;};
static_assert(sizeof(SlimSlot)==12);
static constexpr uint32_t slim_mask=(1u<<24)-1;
static bool slim_pack(const State&s,SlimKey&out) {
 out={0,0};size_t n=s.a.size()+s.b.size(),first=s.a.size();
 if(n==0||n>38||first>38)return false;
 size_t at=0;
 for(const Word*w:{&s.a,&s.b})for(unsigned char c:*w) {
  if(c<1||c>4)return false;unsigned value=c-1;
  if(at<32)out.lo|=uint64_t(value)<<(2*at);
  else out.hi|=uint32_t(value)<<(2*(at-32));
  ++at;
 }
 out.hi|=uint32_t(n)<<12;out.hi|=uint32_t(first)<<18;return true;
}
static State slim_unpack(SlimKey k) {
 size_t n=(k.hi>>12)&63,first=(k.hi>>18)&63;
 if(n==0||n>38||first>n)throw std::runtime_error("invalid 38-letter exact key");
 State s;s.a.reserve(first);s.b.reserve(n-first);
 for(size_t i=0;i<n;++i) {
  unsigned char c=1+((i<32?k.lo>>(2*i):uint64_t(k.hi)>>(2*(i-32)))&3);
  (i<first?s.a:s.b).push_back(c);
 }
 return s;
}
static SlimKey slim_key(const SlimSlot&s){return {uint64_t(s.lo0)|(uint64_t(s.lo1)<<32),s.hi&slim_mask};}
static unsigned slim_value(const SlimSlot&s){return (s.hi>>24)&255;}
static uint64_t slim_hash(SlimKey k){return compact_mix(k.lo^std::rotl(compact_mix(k.hi),23));}
struct SlimTable {
 std::vector<SlimSlot>slots;size_t mask,used=0,limit;uint64_t hits=0,saturation=0;
 SlimTable(int log2,size_t count):slots(size_t(1)<<log2),mask(slots.size()-1),limit(std::min(count,slots.size()*85/100)){}
 uint32_t find(SlimKey k)const {
  size_t pos=slim_hash(k)&mask;
  for(size_t probe=0;probe<slots.size();++probe,pos=(pos+1)&mask) {
   auto &v=slots[pos];if(!v.lo0&&!v.lo1&&!v.hi)return compact_absent;
   if(v.lo0==uint32_t(k.lo)&&v.lo1==uint32_t(k.lo>>32)&&(v.hi&slim_mask)==k.hi)return uint32_t(pos);
  }
  return compact_absent;
 }
 uint32_t find(const State&s)const {SlimKey k;return slim_pack(s,k)?find(k):compact_absent;}
 CompactInsert insert(SlimKey k,unsigned value) {
  if(!k.hi||(k.hi&~slim_mask)||value>255)throw std::runtime_error("invalid slim insertion");
  size_t pos=slim_hash(k)&mask;
  for(size_t probe=0;probe<slots.size();++probe,pos=(pos+1)&mask) {
   auto &v=slots[pos];
   if(!v.lo0&&!v.lo1&&!v.hi) {
    if(used>=limit)return {compact_absent,false,true};
    v={uint32_t(k.lo),uint32_t(k.lo>>32),k.hi|(value<<24)};++used;return {uint32_t(pos),true,false};
   }
   if(v.lo0==uint32_t(k.lo)&&v.lo1==uint32_t(k.lo>>32)&&(v.hi&slim_mask)==k.hi)return {uint32_t(pos),false,false};
  }
  return {compact_absent,false,true};
 }
 bool dominated(const State&s,unsigned rem) {
  SlimKey k;if(!slim_pack(s,k))throw std::runtime_error("cache state exceeds 38 letters");
  auto r=insert(k,rem);if(r.limited){++saturation;return false;}
  if(r.inserted)return false;
  auto &v=slots[r.slot];if(slim_value(v)>=rem){++hits;return true;}
  v.hi=k.hi|(rem<<24);return false;
 }
 void reset(){std::fill(slots.begin(),slots.end(),SlimSlot{});used=0;hits=0;saturation=0;}
};

// Synchronized SL(2,5) and exponent-matrix mod7 graph, all14 move labels.
struct JointPDB {
 const FinitePDB&fp;const ModPDB&mp;
 std::vector<int>dense,codes;
 std::vector<uint16_t>nextf,nextm;
 std::vector<uint8_t>d;
 size_t visited=0;bool complete=false;int axis=0;size_t assignment;
 JointPDB(const Solver&s,size_t which=0):fp(s.finite.at(which)),mp(s.mods.at(0)),assignment(which) {
  if(fp.g->p!=5||mp.p!=7)throw std::runtime_error("unexpected joint quotient axes");
  dense.assign(mp.d.size(),-1);
  for(size_t i=0;i<mp.d.size();++i)if(mp.d[i]!=255){dense[i]=codes.size();codes.push_back(i);}
  axis=codes.size();
  nextf.resize(fp.d.size()*14);nextm.resize(size_t(axis)*14);
  for(size_t i=0;i<fp.d.size();++i)for(int m=0;m<14;++m)nextf[i*14+m]=fp.advance(i,m);
  for(int i=0;i<axis;++i)for(int m=0;m<14;++m) {
   int code=mp.code(emove(mp.decode(codes[i]),m));
   if(dense[code]<0)throw std::runtime_error("mod7 orbit not closed");
   nextm[size_t(i)*14+m]=dense[code];
  }
  d.assign(fp.d.size()*size_t(axis),255);
 }
 uint32_t advance(uint32_t z,int m)const {
  uint32_t a=z/axis,b=z%axis;
  return uint32_t(nextf[size_t(a)*14+m])*axis+nextm[size_t(b)*14+m];
 }
 uint32_t eval(const Matrix&e,const std::vector<int>&f)const {
  int b=dense.at(mp.code(e));if(b<0)throw std::runtime_error("exponent matrix outside mod7 orbit");
  return uint32_t(f.at(assignment))*axis+b;
 }
 bool build(Solver&s) {
  std::vector<uint32_t>queue;queue.reserve(d.size());
  std::vector<int>f(s.finite.size());f[assignment]=fp.eval(s.goal);uint32_t root=eval(exponent(s.goal),f);
  d[root]=0;queue.push_back(root);
  for(size_t h=0;h<queue.size();++h) {
   if((h&4095)==0&&s.expired()){visited=queue.size();return false;}
   uint32_t u=queue[h];
   for(int m=0;m<14;++m) {
    uint32_t v=advance(u,m);
    if(d[v]==255) {
     if(d[u]>=254)throw std::runtime_error("joint distance exceeds byte capacity");
     d[v]=d[u]+1;queue.push_back(v);
    }
   }
  }
  visited=queue.size();complete=true;
  std::cout<<"joint_pdb axes=SL2_5_and_exponent_mod7 assignment="<<assignment<<" nominal="<<d.size()<<" visited="<<visited<<" complete=yes distance_bytes="<<d.size()<<" elapsed="<<s.elapsed()<<"\n"<<std::flush;
  return true;
 }
 int h(const Matrix&e,const std::vector<int>&f)const {
  unsigned value=d[eval(e,f)];return value==255?(complete?1000:0):int(value);
 }
};


struct PrefixRoot {State s;std::vector<int>moves;int peak;};
struct PrefixFrontier {std::vector<PrefixRoot>roots;std::vector<int>early;bool found=false;};
// Exact shortest-prefix BFS. Equal-depth representatives may favor higher peaks.
// No frontier truncation: a shortest solution longer than p has a prefix here.
static PrefixFrontier prefix_frontier(const State&start,const State&goal,int cap,int p) {
 PrefixFrontier out;
 std::vector<PrefixRoot>all{{start,{},int(start.a.size()+start.b.size())}};
 std::unordered_map<std::string,size_t>seen{{key(start),0}};
 if(start.a==goal.a&&start.b==goal.b){out.found=true;return out;}
 size_t begin=0,end=1;
 for(int depth=1;depth<=p;++depth) {
  size_t nextbegin=all.size();
  for(size_t i=begin;i<end;++i) {
   PrefixRoot parent=all[i];
   for(int m=0;m<14;++m) {
    State t=move(parent.s,m);int len=t.a.size()+t.b.size();if(len>cap)continue;
    auto path=parent.moves;path.push_back(m);int peak=std::max(parent.peak,len);
    if(t.a==goal.a&&t.b==goal.b){out.found=true;out.early=std::move(path);return out;}
    auto k=key(t);auto found=seen.find(k);
    if(found==seen.end()){seen.emplace(std::move(k),all.size());all.push_back({std::move(t),std::move(path),peak});}
    else {
     auto &old=all[found->second];
     if(old.moves.size()==size_t(depth)&&peak>old.peak){old.moves=std::move(path);old.peak=peak;}
    }
   }
  }
  begin=nextbegin;end=all.size();
 }
 for(size_t i=begin;i<end;++i)out.roots.push_back(std::move(all[i]));
 std::sort(out.roots.begin(),out.roots.end(),[](const PrefixRoot&a,const PrefixRoot&b) {
  if(a.peak!=b.peak)return a.peak>b.peak;
  size_t na=a.s.a.size()+a.s.b.size(),nb=b.s.a.size()+b.s.b.size();
  if(na!=nb)return na<nb;return a.moves<b.moves;
 });
 return out;
}


// Every capped relator state has exponent L1 <= its total word length.
// Full BFS of that projected graph gives a bound specific to the same cap.
struct IntegerPDB {
 int cap,base;size_t visited=0;std::vector<uint8_t>d;
 explicit IntegerPDB(int c,const Matrix&goal):cap(c),base(2*c+1),d(size_t(base)*base*base*base,255) {
  if(l1(goal)>cap)throw std::runtime_error("integer goal outside projection cap");
  std::vector<uint32_t>q;uint32_t root=code(goal);d[root]=0;q.push_back(root);
  for(size_t h=0;h<q.size();++h) {
   uint32_t u=q[h];Matrix s=decode(u);
   for(int m=0;m<6;++m) {
    Matrix t=emove(s,m);if(l1(t)>cap)continue;uint32_t v=code(t);
    if(d[v]==255){if(d[u]>=254)throw std::runtime_error("integer bound exceeds byte range");d[v]=d[u]+1;q.push_back(v);}
   }
  }
  visited=q.size();
 }
 static int l1(const Matrix&e){int n=0;for(int v:e)n+=std::abs(v);return n;}
 uint32_t code(const Matrix&e)const {
  uint32_t z=0;for(int v:e){if(v < -cap||v>cap)throw std::runtime_error("integer coordinate outside domain");z=z*base+v+cap;}return z;
 }
 Matrix decode(uint32_t z)const {Matrix e;for(int i=3;i>=0;--i){e[i]=int(z%base)-cap;z/=base;}return e;}
 int h(const Matrix&e)const {if(l1(e)>cap)return 1000;unsigned v=d[code(e)];return v==255?1000:int(v);}
};

struct SlimConfig{CompactConfig base;int ttlog2=23,prefixdepth=4;uint64_t prefixnodes=5000000;};
struct JointSlimSolver {
 SlimConfig config;Config c;Solver shared;SlimTable ball;
 std::unique_ptr<SlimTable>cache;std::unique_ptr<JointPDB>joint,joint2;std::unique_ptr<IntegerPDB>integer;std::vector<int>path,solution;
 int completeball=0;bool partialball=false;uint64_t nodes=0,prefixend=0;bool prefixinterrupted=false;
 JointSlimSolver(SlimConfig cc,State s,State t):config(cc),c(cc.base.base),shared(c,std::move(s),std::move(t)),ball(cc.base.goalslotslog2,c.ballstates){}
 void makeball() {
  SlimKey root;if(!slim_pack(shared.goal,root))throw std::runtime_error("invalid goal");
  auto add=ball.insert(root,0);if(add.limited)throw std::runtime_error("root cannot fit");
  std::vector<uint32_t>queue;queue.reserve(ball.limit);queue.push_back(add.slot);
  size_t begin=0,end=1;std::string stop="requested_radius";
  for(int d=1;d<=c.ball;++d) {
   bool full=true;size_t nextbegin=end;
   for(size_t i=begin;i<end;++i) {
    if((i&4095)==0&&shared.expired()){full=false;stop="time_limit";break;}
    State s=slim_unpack(slim_key(ball.slots[queue[i]]));
    for(int m=0;m<14;++m) {
     State t=move(s,m);if(t.a.size()+t.b.size()>size_t(c.ballcap))continue;
     SlimKey k;if(!slim_pack(t,k))throw std::runtime_error("goal-ball state exceeds exact key capacity");
     auto r=ball.insert(k,d);if(r.limited){full=false;stop="state_or_load_limit";break;}
     if(r.inserted)queue.push_back(r.slot);
    }
    if(!full)break;
   }
   std::cout<<"ball layer="<<d<<" total="<<ball.used<<" complete="<<(full?"yes":"no")<<" elapsed="<<shared.elapsed()<<" table_bytes="<<ball.slots.size()*sizeof(SlimSlot)<<"\n"<<std::flush;
   if(!full){partialball=true;break;}
   completeball=d;begin=nextbegin;end=queue.size();if(begin==end){stop="component_exhausted";break;}
  }
  std::vector<uint32_t>().swap(queue);
  std::cout<<"ball_finished total="<<ball.used<<" complete_radius="<<completeball<<" partial="<<(partialball?"yes":"no")<<" stop="<<stop<<" queue_released=yes elapsed="<<shared.elapsed()<<"\n"<<std::flush;
 }
 void suffix(const State&initial,uint32_t slot) {
  solution=path;State s=initial;unsigned depth=slim_value(ball.slots[slot]);
  while(depth) {
   bool found=false;
   for(int m=0;m<14;++m) {
    State t=move(s,m);uint32_t p=ball.find(t);
    if(p!=compact_absent&&slim_value(ball.slots[p])+1==depth) {
     solution.push_back(m);s=std::move(t);--depth;found=true;break;
    }
   }
   if(!found)throw std::runtime_error("no exact goal-ball predecessor");
  }
  if(s.a!=shared.goal.a||s.b!=shared.goal.b)throw std::runtime_error("goal reconstruction ended incorrectly");
 }
 int bound(const Matrix&e,const std::vector<int>&f,size_t len)const {return std::max(std::max(shared.heuristic(e,f,len),std::max(joint->h(e,f),joint2->h(e,f))),integer->h(e));}
 bool search(const State&s,const Matrix&e,const std::vector<int>&f,int rem,int last) {
  ++nodes;if(prefixend&&nodes>prefixend){prefixinterrupted=true;return false;}if((nodes&16383)==0) {
   if(shared.expired())return false;
   if((nodes&4194303)==0)std::cout<<"progress nodes="<<nodes<<" elapsed="<<shared.elapsed()<<" tt="<<cache->used<<" hits="<<cache->hits<<" saturation="<<cache->saturation<<"\n"<<std::flush;
  }
  uint32_t z=ball.find(s);if(z!=compact_absent&&slim_value(ball.slots[z])<=unsigned(rem)){suffix(s,z);return true;}
  if(rem==0)return false;
  if(c.ballcap>=c.cap&&rem<=completeball)return false;
  if(bound(e,f,s.a.size()+s.b.size())>rem)return false;
  if(cache->dominated(s,rem))return false;
  struct Child{State s;Matrix e;std::vector<int>f;int m,score;};std::vector<Child>children;children.reserve(14);
  for(int m=0;m<14;++m) {
   if(last>=0&&m==im[last])continue;
   State t=move(s,m);if(t.a==s.a&&t.b==s.b)continue;
   size_t len=t.a.size()+t.b.size();if(len>size_t(c.cap))continue;
   Matrix ee=emove(e,m);std::vector<int>ff;ff.reserve(shared.finite.size());
   for(size_t i=0;i<shared.finite.size();++i)ff.push_back(shared.finite[i].advance(f[i],m));
   int h=bound(ee,ff,len);if(h>rem-1)continue;
   int score=h*1000+int(len)*10+m;uint32_t p=ball.find(t);
   if(p!=compact_absent)score=-100000+slim_value(ball.slots[p]);
   children.push_back({std::move(t),ee,std::move(ff),m,score});
  }
  std::sort(children.begin(),children.end(),[](const Child&a,const Child&b){return a.score<b.score;});
  for(auto&t:children){path.push_back(t.m);bool hit=search(t.s,t.e,t.f,rem-1,t.m);path.pop_back();if(hit)return true;if(shared.interrupted||prefixinterrupted)return false;}
  return false;
 }
 bool run() {
  shared.makepdb();if(shared.expired()){std::cout<<"STOP status=incomplete reason=time_limit_during_pdb\n";return false;}
  joint=std::make_unique<JointPDB>(shared);if(!joint->build(shared)){std::cout<<"STOP status=incomplete reason=time_limit_during_joint_pdb\n";return false;}
  joint2=std::make_unique<JointPDB>(shared,1);if(!joint2->build(shared)){std::cout<<"STOP status=incomplete reason=time_limit_during_second_joint_pdb\n";return false;}
  integer=std::make_unique<IntegerPDB>(c.cap,exponent(shared.goal));
  std::cout<<"integer_pdb cap="<<c.cap<<" states="<<integer->visited<<" complete=yes bytes="<<integer->d.size()<<" elapsed="<<shared.elapsed()<<"\n"<<std::flush;
  makeball();if(shared.expired()){std::cout<<"STOP status=incomplete reason=time_limit_during_ball\n";return false;}
  cache=std::make_unique<SlimTable>(config.ttlog2,c.ttstates);
  Matrix e=exponent(shared.start);std::vector<int>f;for(auto&p:shared.finite)f.push_back(p.eval(shared.start));
  int first=std::max(c.mindepth,shared.heuristic(e,f,shared.start.a.size()+shared.start.b.size()));

  bool anyincomplete=false;
  for(int d=first;d<=c.depth;++d) {
   auto prefixes=prefix_frontier(shared.start,shared.goal,c.cap,std::min(d,config.prefixdepth));
   if(prefixes.found)solution=prefixes.early;
   size_t completed=0,partial=0;uint64_t before=nodes;
   std::cout<<"prefix_frontier depth="<<std::min(d,config.prefixdepth)<<" roots="<<prefixes.roots.size()<<" truncated=no order=descending_peak prefix_nodes="<<config.prefixnodes<<"\n"<<std::flush;
   bool hit=prefixes.found;
   for(size_t i=0;!hit&&i<prefixes.roots.size();++i) {
    if(shared.expired())break;
    cache->reset();prefixinterrupted=false;prefixend=config.prefixnodes?nodes+config.prefixnodes:0;
    auto &root=prefixes.roots[i];path=root.moves;
    Matrix ee=exponent(root.s);std::vector<int>ff;for(auto &p:shared.finite)ff.push_back(p.eval(root.s));
    uint64_t startnodes=nodes;
    hit=search(root.s,ee,ff,d-int(path.size()),path.empty()?-1:path.back());
    if(!hit&&!prefixinterrupted&&!shared.interrupted)++completed;else if(!hit)++partial;
    std::cout<<"prefix_result index="<<i<<" peak="<<root.peak<<" start_total="<<root.s.a.size()+root.s.b.size()<<" nodes="<<nodes-startnodes<<" status="<<(hit?"found":(prefixinterrupted||shared.interrupted)?"incomplete":"complete_no_path")<<" elapsed="<<shared.elapsed()<<"\n"<<std::flush;
    if(shared.interrupted)break;
   }
   if(hit) {
    std::cout<<"FOUND length="<<solution.size()<<" elapsed="<<shared.elapsed()<<" nodes="<<nodes<<"\nMOVES [";
    for(size_t i=0;i<solution.size();++i){if(i)std::cout<<", ";std::cout<<solution[i];}std::cout<<"]\n";return true;
   }
   bool incomplete=shared.interrupted||partial||completed!=prefixes.roots.size();anyincomplete|=incomplete;
   std::cout<<"search depth="<<d<<" nodes="<<nodes-before<<" status="<<(incomplete?"incomplete":"complete_no_path")<<" cap="<<c.cap<<" prefix_completed="<<completed<<" prefix_partial="<<partial<<" prefix_total="<<prefixes.roots.size()<<" elapsed="<<shared.elapsed()<<"\n"<<std::flush;
   if(shared.interrupted)break;
  }
  std::cout<<"STOP status="<<(anyincomplete||shared.interrupted?"incomplete":"complete_no_path")<<" nodes="<<nodes<<" cap="<<c.cap<<" elapsed="<<shared.elapsed()<<"\n";return false;
 }

};
#ifndef SOL61_SLIM_NO_MAIN
int main(int argc,char**argv){try {
 SlimConfig config;auto&c=config.base;c.base.ballstates=180000000;c.base.ttstates=225000000;
 for(int i=1;i<argc;++i) {
  std::string k=argv[i];if(i+1>=argc)throw std::runtime_error("missing flag value");std::string v=argv[++i];
  if(k=="--input")c.base.input=v;else if(k=="--depth")c.base.depth=std::stoi(v);
  else if(k=="--min-depth")c.base.mindepth=std::stoi(v);else if(k=="--cap")c.base.cap=std::stoi(v);
  else if(k=="--ball")c.base.ball=std::stoi(v);else if(k=="--ball-cap")c.base.ballcap=std::stoi(v);
  else if(k=="--ball-states")c.base.ballstates=std::stoull(v);else if(k=="--tt-states")c.base.ttstates=std::stoull(v);
  else if(k=="--seconds")c.base.seconds=std::stoi(v);else if(k=="--goal-slots-log2")c.goalslotslog2=std::stoi(v);
  else if(k=="--prefix-depth")config.prefixdepth=std::stoi(v);else if(k=="--prefix-nodes")config.prefixnodes=std::stoull(v);else if(k=="--tt-slots-log2")config.ttlog2=std::stoi(v);else throw std::runtime_error("unknown flag: "+k);
 }
 if(config.prefixdepth<0||config.prefixdepth>4||c.base.input.empty()||c.base.depth<0||c.base.depth>254||c.base.mindepth<0||c.base.mindepth>c.base.depth||c.base.cap<2||c.base.cap>38||c.base.ball<0||c.base.ball>63||c.base.ballcap<2||c.base.ballcap>38||c.base.seconds<1||c.base.ballstates<1||c.base.ballstates>=UINT32_MAX||c.goalslotslog2<4||c.goalslotslog2>30||config.ttlog2<4||config.ttlog2>30)throw std::runtime_error("invalid configuration");
 std::ifstream in(c.base.input);std::string a,b,x,y;if(!(in>>a>>b>>x>>y))throw std::runtime_error("input needs four words");
 State s{parse(a),parse(b)},t{parse(x),parse(y)};
 if(s.a.size()+s.b.size()>size_t(c.base.cap))throw std::runtime_error("start exceeds cap");
 if(t.a.size()!=1||t.b.size()!=1)throw std::runtime_error("goal must have two unit relators");
 Matrix e=exponent(s),f=exponent(t);if(std::abs(int64_t(e[0])*e[3]-int64_t(e[1])*e[2])!=1||std::abs(int64_t(f[0])*f[3]-int64_t(f[1])*f[2])!=1)throw std::runtime_error("determinant must be +/-1");
 std::cout<<"SOL61_INTEGER_PEAK ac-r2-v1 slot_bytes=12 depth="<<c.base.depth<<" min_depth="<<c.base.mindepth<<" cap="<<c.base.cap<<" ball="<<c.base.ball<<" goal_log2="<<c.goalslotslog2<<" tt_log2="<<config.ttlog2<<" tt_states="<<c.base.ttstates<<" prefix_depth="<<config.prefixdepth<<" prefix_nodes="<<config.prefixnodes<<" saturation=continue_search seconds="<<c.base.seconds<<"\n"<<std::flush;
 JointSlimSolver solver(config,s,t);return solver.run()?0:2;
}catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 1;}}
#endif
