"""Bounded exact search for <=3-move alternatives to t00312 level changes."""
import hashlib,json,resource,signal,sys,time
from collections import deque
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('interrupted')));signal.alarm(180)
core,specs,pins,selected=load_kernel();started=time.monotonic();records=0;last=0
def tick():
 global records,last
 records+=1
 if records>600000:raise RuntimeError('record cap')
 now=time.monotonic()
 if now-started>180:raise TimeoutError('wall cap')
 if now-last>.1:
  cp=json.loads((ROOT/'continuation/checkpoint.json').read_text())
  if cp['stopped'] or cp['active'] is not None or cp.get('intake_lease'):raise RuntimeError('stop/conflicting lease')
  last=now
rho=(-1,2,1,1,-2);rho2=(2,1,1,-2,-1)
def shortest(src,dst,depth=3):
 q=deque([(src,())]);seen={src}
 while q:
  s,p=q.popleft()
  if s==dst:return p
  if len(p)==depth:continue
  for m in range(14):
   tick();u=core.apply_move(s,m)
   if u not in seen:seen.add(u);q.append((u,p+(m,)))
 return None
rows=[]
for a in (1,2,4,8,16):
 for b in (2,3,4):
  for c in (2,3,4):
   s1=((2,)*b+(-1,)+(-2,)*(c-1)+(1,)*(2*a)+(-2,),rho)
   t1=core.apply_move(core.apply_move(core.apply_move(core.apply_move(s1,0),9),6),10)
   p1=shortest(s1,t1);rows.append({'orientation':'1_to_2','a':a,'b':b,'c':c,'path_le_3':p1})
   s2=((2,)*c+(1,)+(-2,)*(b-1)+(-1,)*(2*a)+(-2,),rho2)
   t2=core.apply_move(core.apply_move(core.apply_move(core.apply_move(s2,0),9),7),11)
   p2=shortest(s2,t2);rows.append({'orientation':'2_to_1','a':a,'b':b,'c':c,'path_le_3':p2})
signal.alarm(0);hits=[x for x in rows if x['path_le_3'] is not None]
result={'kind':'completed_bounded_exact_level_change_search','source':'UPGH t00312/t00329','checker_commit':pins['source_commit'],'cases':len(rows),'parameter_grid':{'a':[1,2,4,8,16],'b':[2,3,4],'c':[2,3,4]},'depth':3,'hits':hits,'no_path_le_3':len(rows)-len(hits),'records':records,'elapsed_seconds':time.monotonic()-started,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'limits':{'seconds':180,'memory_mib':1024,'records':600000},'model_workers':0,'row_searches':0,'scope':'Exact endpoints only on finite grid; does not prove global four-move minimum for every parameter or alternate construction.'}
(OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
