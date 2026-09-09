from pathlib import Path
p=Path(__file__).parent
s=(p/'planar_search.cpp').read_text()
insert=r'''
 // Atomic stellar relocation: erase v's fan, triangulate the disk by a legal
 // fan, and reinsert the same v into a chosen face. Exterior edges stay fixed.
 bool relocate(int v,int choice,int facechoice,Step &step,int layer){
  vector<array<int,3>> outside;array<vector<int>,N> adj;int degree=0;
  for(auto ff:f){if(find(ff.begin(),ff.end(),v)==ff.end())outside.push_back(ff);
   else{vector<int>uv;for(int x:ff)if(x!=v)uv.push_back(x);if(uv.size()!=2)throw runtime_error("bad vertex fan");adj[uv[0]].push_back(uv[1]);adj[uv[1]].push_back(uv[0]);degree++;}}
  if(degree<3||degree>10)return false;
  int start=-1;for(int i=0;i<N;i++)if(!adj[i].empty()){if(adj[i].size()!=2)throw runtime_error("bad link");if(start<0)start=i;}
  vector<int> cyc={start};int prev=-1,cur=start;
  for(int k=0;k<degree;k++){int nxt=adj[cur][0];if(nxt==prev)nxt=adj[cur][1];if(prev<0)nxt=min(adj[cur][0],adj[cur][1]);
   if(nxt==start)break;cyc.push_back(nxt);prev=cur;cur=nxt;}
  if((int)cyc.size()!=degree)throw runtime_error("disconnected link");
  int at=choice%degree;rotate(cyc.begin(),cyc.begin()+at,cyc.end());int root=cyc[0];
  for(int k=2;k<degree-1;k++)if(inc[EI[root][cyc[k]]])return false;
  for(int k=1;k<degree-1;k++){array<int,3>ff={root,cyc[k],cyc[k+1]};sort(ff.begin(),ff.end());outside.push_back(ff);}
  if(outside.size()!=32)throw runtime_error("cavity face count");
  sort(outside.begin(),outside.end());int k=facechoice%32;auto into=outside[k];
  step={2,layer,v,root,tid[into[0]][into[1]][into[2]],0};
  outside[k]={v,into[0],into[1]};outside.push_back({v,into[1],into[2]});outside.push_back({v,into[2],into[0]});
  for(auto &ff:outside)sort(ff.begin(),ff.end());sort(outside.begin(),outside.end());
  copy(outside.begin(),outside.end(),f.begin());rebuild();return true;
 }
'''
pos=s.index('\n};\nstruct State')
s=s[:pos]+insert+s[pos:]
s=s.replace('mode!="weighted"','mode!="weighted"&&mode!="relocate"')
s=s.replace('if(mode=="hybrid"&&rng()%30==0){',r'''if(mode=="relocate"&&rng()%10==0){
    int w=rng()%2,v=rng()%N;State old=s;Step st;
    if(!s.t[w].relocate(v,rng()%N,rng()%32,st,w))continue;
    s.recalc();legal++;vector<Step>extra={st};keep(it+1,extra);
    double delta=s.triangles-old.triangles+.15*(s.overlap-old.overlap);
    if(s.triangles==0||delta<=0||unit()<exp(-delta/temp)){path.push_back(st);accepted++;}else s=old;
   }else if((mode=="hybrid"||mode=="relocate")&&rng()%30==0){''')
s=s.replace('// Modes: single, macro, hybrid, weighted.', '// Modes: single, macro, hybrid, weighted, relocate.')
s=s.replace('single|macro|hybrid|weighted output.json','single|macro|hybrid|weighted|relocate output.json')
s=s.replace('"producer":"planar_search_cpp"','"producer":"planar_search_cpp_stellar_extension"')
(p/'stellar_search.cpp').write_text(s)
