// Independent DRUP/RUP checker, standard C++17. Deletions are ignored soundly:
// previously proved clauses remain logically available. No RAT extensions.
// Accept only a unit-propagation contradiction of the original formula or a
// checked derived empty clause. Some solvers emit no steps for a root conflict.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <stdexcept>
using namespace std;
struct Check{
 int n;vector<vector<int>> cs,watch;vector<int>units,val,trail;bool empty=false;
 Check(int n):n(n),watch(2*n+2),val(n+1,0){}
 int idx(int l){return 2*abs(l)+(l<0);}int value(int l){return val[abs(l)]*(l>0?1:-1);}
 void add(vector<int> c){for(int x:c)if(x==0||abs(x)>n)throw runtime_error("literal range");sort(c.begin(),c.end());c.erase(unique(c.begin(),c.end()),c.end());int id=cs.size();cs.push_back(c);if(c.empty())empty=true;else if(c.size()==1)units.push_back(c[0]);else{watch[idx(c[0])].push_back(id);watch[idx(c[1])].push_back(id);}}
 bool assign(int l){if(value(l)==-1)return false;if(value(l)==0){val[abs(l)]=l>0?1:-1;trail.push_back(l);}return true;}
 bool contradiction(const vector<int>& target){
  trail.clear();bool conflict=empty;
  if(!conflict)for(int l:target)if(!assign(-l)){conflict=true;break;}
  if(!conflict)for(int l:units)if(!assign(l)){conflict=true;break;}
  size_t head=0;
  while(!conflict&&head<trail.size()){
   int fals=-trail[head++];auto &ws=watch[idx(fals)];size_t j=0;
   while(j<ws.size()){
    int ci=ws[j];auto &c=cs[ci];if(c[0]!=fals)swap(c[0],c[1]);if(c[0]!=fals)throw runtime_error("watch drift");int other=c[1];if(value(other)==1){j++;continue;}
    size_t k=2;while(k<c.size()&&value(c[k])==-1)k++;
    if(k<c.size()){swap(c[0],c[k]);watch[idx(c[0])].push_back(ci);ws[j]=ws.back();ws.pop_back();}
    else{if(!assign(other)){conflict=true;break;}j++;}
   }
  }
  for(int l:trail)val[abs(l)]=0;return conflict;
 }
};
vector<int> parse(const string&line,int n){stringstream s(line);vector<int>v;int l;bool zero=false;while(s>>l){if(l==0){zero=true;break;}if(abs(l)>n)throw runtime_error("proof variable outside formula");v.push_back(l);}if(!zero)throw runtime_error("missing zero");return v;}
int main(int argc,char**argv){try{if(argc!=3)throw runtime_error("usage: rup_check formula.cnf proof.drup");ifstream f(argv[1]);if(!f)throw runtime_error("input missing");string line;int n=0,m=0;vector<string>raw;
 while(getline(f,line)){if(line.empty()||line[0]=='c')continue;if(line[0]=='p'){string p,cnf;stringstream ss(line);ss>>p>>cnf>>n>>m;if(cnf!="cnf")throw runtime_error("format");}else raw.push_back(line);}
 if(n<1||int(raw.size())!=m)throw runtime_error("header mismatch");Check ch(n);for(auto&s:raw)ch.add(parse(s,n));ifstream pf(argv[2]);if(!pf)throw runtime_error("proof missing");long long checked=0,del=0;bool done=ch.contradiction({});
 while(getline(pf,line)){if(line.empty()||line[0]=='c')continue;if(line[0]=='d'){del++;continue;}auto c=parse(line,n);if(!ch.contradiction(c))throw runtime_error("non-RUP step "+to_string(checked+1));checked++;ch.add(c);if(c.empty()){done=true;break;}}
 if(!done)throw runtime_error("no checked empty clause");cout<<"VERIFIED RUP steps "<<checked<<" ignored_deletions "<<del<<" initial_clauses "<<m<<" variables "<<n<<"\n";return 0;
 }catch(exception&e){cerr<<"REJECTED "<<e.what()<<endl;return 1;}}
