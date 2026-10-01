// Exact compact backward goal ball plus IDA. No competition data or roads.
// State payload: 72 letter bits + 6 total-length bits + 6 first-word bits.
// Parent slot, generating move, and depth fit in the remaining 44 bits.
#define main strong_shared_entry_not_used
#include "sol61_ida_strong.cpp"
#undef main
#include <bit>

struct CompactKey {uint64_t lo=0,hi=0;};
struct CompactSlot {uint64_t lo=0,hi=0;};
static_assert(sizeof(CompactSlot)==16);
static constexpr uint64_t compact_key_hi_mask=UINT64_C(0xff)|(UINT64_C(0xfff)<<52);
static constexpr uint32_t compact_absent=UINT32_MAX;
static bool compact_pack(const State&s,CompactKey&out){
 out={};const size_t n=s.a.size()+s.b.size();if(n==0||n>36||s.a.size()>36)return false;
 size_t at=0;for(const Word*w:{&s.a,&s.b})for(unsigned char c:*w){if(c<1||c>4)return false;uint64_t v=c-1;if(at<32)out.lo|=v<<(2*at);else out.hi|=v<<(2*(at-32));++at;}
 out.hi|=uint64_t(n)<<52;out.hi|=uint64_t(s.a.size())<<58;return true;
}
static State compact_unpack(const CompactKey&k){
 size_t total=(k.hi>>52)&63,first=(k.hi>>58)&63;
 if(total==0||total>36||first>total)throw std::runtime_error("invalid compact state lengths");
 State s;s.a.reserve(first);s.b.reserve(total-first);
 for(size_t i=0;i<total;++i){unsigned char c=1+((i<32?k.lo>>(2*i):k.hi>>(2*(i-32)))&3);(i<first?s.a:s.b).push_back(c);}return s;
}
static CompactKey compact_slot_key(const CompactSlot&s){return {s.lo,s.hi&compact_key_hi_mask};}
static uint32_t compact_parent(const CompactSlot&s){return uint32_t(s.hi>>8);}
static int compact_move(const CompactSlot&s){return int((s.hi>>40)&15);}
static int compact_depth(const CompactSlot&s){return int((s.hi>>44)&63);}
static uint64_t compact_mix(uint64_t z){z=(z^(z>>30))*UINT64_C(0xbf58476d1ce4e5b9);z=(z^(z>>27))*UINT64_C(0x94d049bb133111eb);return z^(z>>31);}
static uint64_t compact_hash(const CompactKey&k){return compact_mix(k.lo^std::rotl(compact_mix(k.hi),23));}
struct CompactInsert {uint32_t slot=compact_absent;bool inserted=false,limited=false;};
struct CompactBall {
 std::vector<CompactSlot>slots;size_t mask,used=0,loadlimit;
 explicit CompactBall(int log2):slots(size_t(1)<<log2),mask(slots.size()-1),loadlimit(slots.size()*85/100){}
 uint32_t find(const CompactKey&k)const{
  size_t pos=compact_hash(k)&mask;
  for(size_t probe=0;probe<slots.size();++probe,pos=(pos+1)&mask){const auto&s=slots[pos];if(s.lo==0&&s.hi==0)return compact_absent;if(s.lo==k.lo&&(s.hi&compact_key_hi_mask)==k.hi)return uint32_t(pos);}return compact_absent;
 }
 uint32_t find(const State&s)const{CompactKey k;return compact_pack(s,k)?find(k):compact_absent;}
 CompactInsert insert(const CompactKey&k,uint32_t parent,int move,int depth,size_t statelimit){
  if((k.lo==0&&k.hi==0)||(k.hi&~compact_key_hi_mask)||move<0||move>=14||depth<0||depth>63||parent>=slots.size())throw std::runtime_error("invalid compact insertion");
  size_t pos=compact_hash(k)&mask;
  for(size_t probe=0;probe<slots.size();++probe,pos=(pos+1)&mask){auto&s=slots[pos];
   if(s.lo==0&&s.hi==0){if(used>=loadlimit||used>=statelimit)return {compact_absent,false,true};s.lo=k.lo;s.hi=k.hi|(uint64_t(parent)<<8)|(uint64_t(move)<<40)|(uint64_t(depth)<<44);++used;return {uint32_t(pos),true,false};}
   if(s.lo==k.lo&&(s.hi&compact_key_hi_mask)==k.hi)return {uint32_t(pos),false,false};
  }return {compact_absent,false,true};
 }
};
struct CompactConfig{Config base;int goalslotslog2=28;};
struct CompactSolver {
 CompactConfig c;Solver shared;CompactBall ball;
 std::unordered_map<std::string,uint8_t>tt;std::vector<int>path,solution;
 uint32_t rootslot=compact_absent;int completeball=0;bool partialball=false;
 uint64_t nodes=0,ttclears=0;std::string ballstop="requested_radius";
 explicit CompactSolver(CompactConfig cc,State s,State t):c(cc),shared(cc.base,std::move(s),std::move(t)),ball(cc.goalslotslog2){}
 void makeball(){
  CompactKey root;if(!compact_pack(shared.goal,root))throw std::runtime_error("goal cannot be packed");
  auto added=ball.insert(root,0,0,0,c.base.ballstates);if(added.limited)throw std::runtime_error("table cannot hold root");rootslot=added.slot;
  std::vector<uint32_t>queue;queue.reserve(std::min(c.base.ballstates,ball.loadlimit));queue.push_back(rootslot);
  size_t begin=0,end=1;
  for(int d=1;d<=c.base.ball;++d){bool full=true;const size_t nextbegin=end;
   for(size_t i=begin;i<end;++i){if((i&4095)==0&&shared.expired()){full=false;ballstop="time_limit";break;}
    const uint32_t parent=queue[i];State s=compact_unpack(compact_slot_key(ball.slots[parent]));
    for(int m=0;m<14;++m){State child=move(s,m);if(child.a.size()+child.b.size()>size_t(c.base.ballcap))continue;
     CompactKey k;if(!compact_pack(child,k))throw std::runtime_error("bounded ball state cannot be packed");
     auto result=ball.insert(k,parent,m,d,c.base.ballstates);
     if(result.limited){full=false;ballstop=ball.used>=c.base.ballstates?"state_limit":"table_load_limit";break;}
     if(result.inserted)queue.push_back(result.slot);
    }if(!full)break;
   }
   std::cout<<"ball layer="<<d<<" total="<<ball.used<<" complete="<<(full?"yes":"no")<<" elapsed="<<shared.elapsed()<<" table_bytes="<<(ball.slots.size()*sizeof(CompactSlot))<<" queue_bytes="<<(queue.capacity()*sizeof(uint32_t))<<" stop="<<(full?"layer_complete":ballstop)<<"\n"<<std::flush;
   if(!full){partialball=true;break;}completeball=d;begin=nextbegin;end=queue.size();if(begin==end){ballstop="component_exhausted";break;}
  }
  std::vector<uint32_t>().swap(queue);
  std::cout<<"ball_finished total="<<ball.used<<" complete_radius="<<completeball<<" partial="<<(partialball?"yes":"no")<<" stop="<<ballstop<<" queue_released=yes elapsed="<<shared.elapsed()<<"\n"<<std::flush;
 }
 void suffix(uint32_t slot){
  solution=path;
  for(size_t steps=0;slot!=rootslot;++steps){if(slot>=ball.slots.size()||steps>=64)throw std::runtime_error("invalid compact suffix chain");const auto&s=ball.slots[slot];const uint32_t parent=compact_parent(s);const int m=compact_move(s);if(m>=14||parent>=ball.slots.size()||compact_depth(ball.slots[parent])+1!=compact_depth(s))throw std::runtime_error("compact suffix metadata mismatch");solution.push_back(im[m]);slot=parent;}
 }
 bool dfs(const State&s,const Matrix&e,const std::vector<int>&f,int rem,int last){
  ++nodes;if((nodes&16383)==0){if(shared.expired())return false;if((nodes&4194303)==0)std::cout<<"progress nodes="<<nodes<<" elapsed="<<shared.elapsed()<<" tt="<<tt.size()<<"\n"<<std::flush;}
  const uint32_t found=ball.find(s);if(found!=compact_absent&&compact_depth(ball.slots[found])<=rem){suffix(found);return true;}
  if(rem==0)return false;
  if(c.base.ballcap>=c.base.cap&&rem<=completeball)return false;
  if(shared.heuristic(e,f,s.a.size()+s.b.size())>rem)return false;
  if(c.base.ttstates){auto k=key(s);auto it=tt.find(k);if(it!=tt.end()&&it->second>=rem)return false;if(tt.size()>=c.base.ttstates){tt.clear();++ttclears;}tt[std::move(k)]=uint8_t(rem);}
  struct Child{State s;Matrix e;std::vector<int>f;int m,score;};std::vector<Child>children;children.reserve(14);
  for(int m=0;m<14;++m){if(last>=0&&m==im[last])continue;auto t=move(s,m);if(t.a==s.a&&t.b==s.b)continue;size_t len=t.a.size()+t.b.size();if(len>size_t(c.base.cap))continue;
   Matrix ee=emove(e,m);std::vector<int>ff;ff.reserve(shared.finite.size());for(size_t i=0;i<shared.finite.size();++i)ff.push_back(shared.finite[i].advance(f[i],m));
   int h=shared.heuristic(ee,ff,len);if(h>rem-1)continue;int score=h*1000+int(len)*10+m;
   uint32_t z=ball.find(t);if(z!=compact_absent)score=-100000+compact_depth(ball.slots[z]);children.push_back({std::move(t),ee,std::move(ff),m,score});
  }
  std::sort(children.begin(),children.end(),[](const Child&a,const Child&b){return a.score<b.score;});
  for(auto&t:children){path.push_back(t.m);bool foundchild=dfs(t.s,t.e,t.f,rem-1,t.m);path.pop_back();if(foundchild)return true;if(shared.interrupted)return false;}return false;
 }
 bool run(){
  shared.makepdb();if(shared.expired()){std::cout<<"STOP status=incomplete reason=time_limit_during_pdb nodes=0 elapsed="<<shared.elapsed()<<"\n";return false;}
  makeball();if(shared.expired()){std::cout<<"STOP status=incomplete reason=time_limit_during_ball nodes=0 elapsed="<<shared.elapsed()<<"\n";return false;}
  Matrix e=exponent(shared.start);std::vector<int>f;for(auto&p:shared.finite)f.push_back(p.eval(shared.start));
  int first=std::max(c.base.mindepth,shared.heuristic(e,f,shared.start.a.size()+shared.start.b.size()));
  for(int d=first;d<=c.base.depth;++d){tt.clear();uint64_t before=nodes;std::cout<<"search depth="<<d<<" cap="<<c.base.cap<<" ball_complete="<<completeball<<" elapsed="<<shared.elapsed()<<"\n"<<std::flush;
   if(dfs(shared.start,e,f,d,-1)){std::cout<<"FOUND length="<<solution.size()<<" elapsed="<<shared.elapsed()<<" nodes="<<nodes<<"\nMOVES [";for(size_t i=0;i<solution.size();++i){if(i)std::cout<<", ";std::cout<<solution[i];}std::cout<<"]\n";return true;}
   std::cout<<"search depth="<<d<<" nodes="<<(nodes-before)<<" status="<<(shared.interrupted?"incomplete":"complete_no_path")<<" cap="<<c.base.cap<<" elapsed="<<shared.elapsed()<<"\n"<<std::flush;if(shared.interrupted)break;
  }
  std::cout<<"STOP status="<<(shared.interrupted?"incomplete":"complete_no_path")<<" nodes="<<nodes<<" tt_clears="<<ttclears<<" cap="<<c.base.cap<<" elapsed="<<shared.elapsed()<<"\n";return false;
 }
};
#ifndef SOL61_COMPACT_NO_MAIN
int main(int argc,char**argv){try{
 CompactConfig c;c.base.ballstates=220000000;
 for(int i=1;i<argc;++i){std::string k=argv[i];if(i+1>=argc)throw std::runtime_error("missing flag value");std::string v=argv[++i];
  if(k=="--input")c.base.input=v;else if(k=="--depth")c.base.depth=std::stoi(v);else if(k=="--min-depth")c.base.mindepth=std::stoi(v);else if(k=="--cap")c.base.cap=std::stoi(v);else if(k=="--ball")c.base.ball=std::stoi(v);else if(k=="--ball-cap")c.base.ballcap=std::stoi(v);else if(k=="--ball-states")c.base.ballstates=std::stoull(v);else if(k=="--tt-states")c.base.ttstates=std::stoull(v);else if(k=="--seconds")c.base.seconds=std::stoi(v);else if(k=="--goal-slots-log2")c.goalslotslog2=std::stoi(v);else throw std::runtime_error("unknown flag: "+k);
 }
 if(c.base.input.empty()||c.base.depth<0||c.base.depth>254||c.base.mindepth<0||c.base.mindepth>c.base.depth||c.base.cap<2||c.base.ball<0||c.base.ball>63||c.base.ballcap<2||c.base.ballcap>36||c.base.seconds<1||c.base.ballstates<1||c.base.ballstates>=UINT32_MAX||c.goalslotslog2<4||c.goalslotslog2>30)throw std::runtime_error("invalid configuration");
 std::ifstream in(c.base.input);std::string a,b,x,y;if(!(in>>a>>b>>x>>y))throw std::runtime_error("input needs start0 start1 goal0 goal1 words");State s{parse(a),parse(b)},t{parse(x),parse(y)};
 if(s.a.size()+s.b.size()>size_t(c.base.cap))throw std::runtime_error("start exceeds cap");
 if(t.a.size()!=1||t.b.size()!=1)throw std::runtime_error("goal must have two unit relators");
 Matrix e=exponent(s),f=exponent(t);int64_t ds=int64_t(e[0])*e[3]-int64_t(e[1])*e[2],dt=int64_t(f[0])*f[3]-int64_t(f[1])*f[2];if(std::abs(ds)!=1||std::abs(dt)!=1)throw std::runtime_error("length bound requires determinant +/-1");
 std::cout<<"SOL61_COMPACT ac-r2-v1 start="<<show(s.a)<<","<<show(s.b)<<" goal="<<show(t.a)<<","<<show(t.b)<<" depth="<<c.base.depth<<" min_depth="<<c.base.mindepth<<" cap="<<c.base.cap<<" ball="<<c.base.ball<<" ball_cap="<<c.base.ballcap<<" ball_states="<<c.base.ballstates<<" goal_slots_log2="<<c.goalslotslog2<<" table_bytes="<<((size_t(1)<<c.goalslotslog2)*sizeof(CompactSlot))<<" tt_states="<<c.base.ttstates<<" seconds="<<c.base.seconds<<"\n"<<std::flush;
 CompactSolver solver(c,s,t);return solver.run()?0:2;
 }catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 1;}}
#endif
