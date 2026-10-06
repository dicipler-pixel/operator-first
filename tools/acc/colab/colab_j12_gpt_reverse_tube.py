#!/usr/bin/env python3
import argparse, json, os, pathlib, subprocess, time, shutil
DEFAULT_TARGETS={'ac-03975':38,'ac-00669':39,'ac-03186':39,'ac-01876':40,'ac-04747':40,'ac-08500':42,'ac-09647':43,'ac-06272':45,'ac-08451':48,'ac-05309':52}
PIN='a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
CPP=r'''
#include <bits/stdc++.h>
using namespace std;
struct State{string a,b;};
static inline string red(const string&s){string o;o.reserve(s.size());for(signed char c:s){if(!o.empty()&&(signed char)o.back()==-c)o.pop_back();else o.push_back((char)c);}return o;}
static inline string invw(const string&w){string o;o.reserve(w.size());for(auto it=w.rbegin();it!=w.rend();++it)o.push_back((char)(-(signed char)*it));return o;}
static inline State mv(const State&s,int m){State t=s;static int gs[4]={1,-1,2,-2};if(m==0)t.a=invw(t.a);else if(m==1)t.b=invw(t.b);else if(m==2)t.a=red(t.a+t.b);else if(m==3)t.a=red(t.a+invw(t.b));else if(m==4)t.b=red(t.b+t.a);else if(m==5)t.b=red(t.b+invw(t.a));else if(m<=9){int g=gs[m-6];string z;z.push_back((char)g);z+=t.a;z.push_back((char)-g);t.a=red(z);}else{int g=gs[m-10];string z;z.push_back((char)g);z+=t.b;z.push_back((char)-g);t.b=red(z);}return t;}
static inline string key(const State&s){string k=s.a;k.push_back(0);k+=s.b;return k;}
static inline array<int,4> exps(const State&s){array<int,4>x{};for(signed char c:s.a){if(abs(c)==1)x[0]+=(c>0?1:-1);else x[1]+=(c>0?1:-1);}for(signed char c:s.b){if(abs(c)==1)x[2]+=(c>0?1:-1);else x[3]+=(c>0?1:-1);}return x;}
struct Sig{int x0,x1,x2,x3,la,lb;bool operator==(Sig const&o)const{return tie(x0,x1,x2,x3,la,lb)==tie(o.x0,o.x1,o.x2,o.x3,o.la,o.lb);}};
struct SH{size_t operator()(Sig const&s)const{size_t h=1469598103934665603ull;for(int v:{s.x0,s.x1,s.x2,s.x3,s.la,s.lb}){h^=(uint64_t)(v+257);h*=1099511628211ull;}return h;}};
static inline Sig sig(const State&s){auto e=exps(s);return {e[0],e[1],e[2],e[3],(int)s.a.size()/2,(int)s.b.size()/2};}
static vector<int> suffix(State s,const unordered_map<string,uint8_t>&rd){vector<int>o;auto it=rd.find(key(s));if(it==rd.end())return{};int d=it->second;while(d){bool ok=false;for(int m=0;m<14;m++){State t=mv(s,m);auto jt=rd.find(key(t));if(jt!=rd.end()&&jt->second+1==d){o.push_back(m);s=move(t);d--;ok=true;break;}}if(!ok)return{};}return o;}
static string enc(const vector<int>&p){ostringstream o;for(size_t i=0;i<p.size();i++){if(i)o<<',';o<<p[i];}return o.str();}
struct Node{State s;vector<uint8_t>p;double sc;};
static bool save_ckpt(const string&fn,int depth,const vector<Node>&layer){ofstream f(fn,ios::binary|ios::trunc);if(!f)return false;uint32_t magic=0x4a313247,n=layer.size();f.write((char*)&magic,4);f.write((char*)&depth,4);f.write((char*)&n,4);for(auto &x:layer){uint32_t la=x.s.a.size(),lb=x.s.b.size(),lp=x.p.size();f.write((char*)&la,4);f.write(x.s.a.data(),la);f.write((char*)&lb,4);f.write(x.s.b.data(),lb);f.write((char*)&lp,4);if(lp)f.write((char*)x.p.data(),lp);}return(bool)f;}
static bool load_ckpt(const string&fn,int&depth,vector<Node>&layer){ifstream f(fn,ios::binary);if(!f)return false;uint32_t magic,n;f.read((char*)&magic,4);if(magic!=0x4a313247)return false;f.read((char*)&depth,4);f.read((char*)&n,4);layer.clear();layer.reserve(n);for(uint32_t i=0;i<n;i++){Node x;uint32_t la,lb,lp;f.read((char*)&la,4);x.s.a.resize(la);f.read(x.s.a.data(),la);f.read((char*)&lb,4);x.s.b.resize(lb);f.read(x.s.b.data(),lb);f.read((char*)&lp,4);x.p.resize(lp);if(lp)f.read((char*)x.p.data(),lp);layer.push_back(move(x));}return(bool)f;}
int main(int argc,char**argv){if(argc<9)return 2;string id=argv[1];int record=stoi(argv[2]);string r0s=argv[3],r1s=argv[4],out=argv[5];int RCAP=stoi(argv[6]),RDEP=stoi(argv[7]),WIDTH=stoi(argv[8]);auto parse=[](string z){string s;stringstream q(z);string t;while(getline(q,t,','))if(!t.empty())s.push_back((char)stoi(t));return s;};State start{parse(r0s),parse(r1s)},goal{string(1,(char)1),string(1,(char)2)};
unordered_map<string,uint8_t>rd;rd.reserve(16000000);unordered_map<Sig,uint8_t,SH>sd;sd.reserve(4000000);vector<State>cur{goal};rd[key(goal)]=0;sd[sig(goal)]=0;
for(int d=0;d<RDEP;d++){vector<State>nx;nx.reserve(cur.size()*4);for(auto&s:cur)for(int m=0;m<14;m++){State t=mv(s,m);if((int)t.a.size()+(int)t.b.size()>RCAP)continue;string k=key(t);if(rd.emplace(k,(uint8_t)(d+1)).second){nx.push_back(t);auto sg=sig(t);auto it=sd.find(sg);if(it==sd.end()||it->second>d+1)sd[sg]=d+1;}}cerr<<"REV "<<d+1<<" new="<<nx.size()<<" total="<<rd.size()<<"\n";cur.swap(nx);}
string ck=out+"/"+id+"_frontier.bin";int depth=0;vector<Node>layer;if(!load_ckpt(ck,depth,layer)){layer.push_back({start,{},0});depth=0;}
auto score=[&](const State&s,int d){auto sg=sig(s);int best=99;for(int da=-1;da<=1;da++)for(int db=-1;db<=1;db++){Sig q=sg;q.la=max(0,q.la+da);q.lb=max(0,q.lb+db);auto it=sd.find(q);if(it!=sd.end())best=min(best,(int)it->second);}int L=s.a.size()+s.b.size();auto e=exps(s);int mat=abs(e[0]-1)+abs(e[1])+abs(e[2])+abs(e[3]-1);int det=abs(e[0]*e[3]-e[1]*e[2]);int one=999;for(int m=0;m<14;m++){State t=mv(s,m);one=min(one,(int)t.a.size()+(int)t.b.size());}int valley=max(0,L-one);return d+(best<99?2.2*best:22.0)+0.30*L+0.70*mat-0.65*valley+(det==1?0:25);};
for(;depth<=record;depth++){cerr<<"FWD "<<depth<<" layer="<<layer.size()<<"\n";for(auto &n:layer){auto it=rd.find(key(n.s));if(it!=rd.end()&&depth+(int)it->second<=record){auto sf=suffix(n.s,rd);vector<int>full;for(auto c:n.p)full.push_back(c);full.insert(full.end(),sf.begin(),sf.end());ofstream h(out+"/"+id+"_candidate.txt",ios::app);h<<id<<": ["<<enc(full)<<"]\n";return 0;}}if(depth==record)break;unordered_map<string,size_t>pos;pos.reserve((size_t)WIDTH*3);vector<Node>cand;cand.reserve((size_t)WIDTH*2);for(auto &n:layer){int last=n.p.empty()?-1:n.p.back();static int im[14]={0,1,3,2,5,4,7,6,9,8,11,10,13,12};for(int m=0;m<14;m++){if(last>=0&&m==im[last])continue;State t=mv(n.s,m);if(t.a.size()+t.b.size()>120)continue;string k=key(t);if(pos.count(k))continue;Node z{move(t),n.p,0};z.p.push_back((uint8_t)m);z.sc=score(z.s,depth+1);pos.emplace(move(k),cand.size());cand.push_back(move(z));}}if((int)cand.size()>WIDTH){nth_element(cand.begin(),cand.begin()+WIDTH,cand.end(),[](auto&a,auto&b){return a.sc<b.sc;});cand.resize(WIDTH);}layer.swap(cand);save_ckpt(ck,depth+1,layer);ofstream st(out+"/"+id+"_status.txt",ios::trunc);st<<"id="<<id<<"\nrecord="<<record<<"\ndepth="<<depth+1<<"\nlayer="<<layer.size()<<"\nreverse_states="<<rd.size()<<"\nstatus=INCOMPLETE\n";}return 1;}
'''
def ensure_repo(work):
    repo=work/'sair'
    if not repo.exists(): subprocess.run(['git','clone','-q','https://github.com/SAIRcompetition/Andrews-Curtis',str(repo)],check=True)
    subprocess.run(['git','-C',str(repo),'checkout','-q',PIN],check=True)
    return repo
def starts(repo):
    d=json.load(open(repo/'competition/tools/verifier/data/manifest.json'))
    return {c['challenge_id']:c['initial_relators'] for c in d['challenges']}
def verify(repo,cand,out):
    if not cand.exists(): return False,''
    sub=out/'verify.txt';shutil.copy2(cand,sub)
    p=subprocess.run(['python3','-m','verifier','--manifest','competition/tools/verifier/data/manifest.json','--submission',str(sub)],cwd=repo,env={**os.environ,'PYTHONPATH':str(repo/'competition/tools')},capture_output=True,text=True)
    t=p.stdout+'\n'+p.stderr
    return '"ok": true' in t.lower() or "'ok': True" in t,t
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--hub',default='/content/drive/MyDrive/Mad Hatters ACC Shared Hub');ap.add_argument('--work',default='/content/j12_gpt');ap.add_argument('--rev-cap',type=int,default=16);ap.add_argument('--rev-depth',type=int,default=9);ap.add_argument('--width',type=int,default=180000);ap.add_argument('--targets',nargs='*');a=ap.parse_args()
    work=pathlib.Path(a.work);work.mkdir(parents=True,exist_ok=True);out=pathlib.Path(a.hub)/'J12_GPT_REVERSE_TUBE';out.mkdir(parents=True,exist_ok=True);repo=ensure_repo(work);ss=starts(repo)
    cpp=work/'j12_reverse_tube.cpp';eng=work/'j12_reverse_tube';cpp.write_text(CPP);subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(eng)],check=True)
    targets=DEFAULT_TARGETS if not a.targets else {z.split(':')[0]:int(z.split(':')[1]) for z in a.targets}
    for cid,rec in targets.items():
        if cid in {'ac-09839','ac-02257','ac-09311','ac-06403','ac-04718','ac-05378'}: continue
        r0,r1=ss[cid];enc=lambda w:','.join(map(str,w));log=out/f'{cid}_engine.log'
        with open(log,'a') as f: subprocess.call([str(eng),cid,str(rec),enc(r0),enc(r1),str(out),str(a.rev_cap),str(a.rev_depth),str(a.width)],stdout=f,stderr=f)
        cand=out/f'{cid}_candidate.txt';ok,vt=verify(repo,cand,out)
        if cand.exists():(out/f'{cid}_verifier.txt').write_text(vt)
        stamp=time.strftime('%Y%m%dT%H%M%SZ',time.gmtime());status=(out/f'{cid}_status.txt').read_text() if (out/f'{cid}_status.txt').exists() else ''
        (pathlib.Path(a.hub)/f'J12_GPT_REPORT_{stamp}.txt').write_text(f'J12 GPT reverse-tube lane\nTarget {cid}, record {rec}\nMethod: exact reverse tube cap={a.rev_cap}, depth={a.rev_depth}; forward climb guided by reverse signatures and one-step valley score.\n{status}\nCandidate present={cand.exists()} official_ok={ok}\n')
        if ok:
            (pathlib.Path(a.hub)/f'J12_GPT_HIT_{stamp}.txt').write_text(cand.read_text()+'\n'+vt);print('VERIFIED HIT',cid,cand.read_text().strip())
if __name__=='__main__':main()
