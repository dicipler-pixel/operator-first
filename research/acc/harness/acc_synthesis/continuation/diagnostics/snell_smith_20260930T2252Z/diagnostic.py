"""Read-only ordered-word Smith diagnostic. No solver recipes or route search."""
import sys,json,math,hashlib,time,resource
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(1024*1024*1024,1024*1024*1024))
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel
I=(1,0,0,1); X=(1,2,0,1);Y=(1,0,2,1)
def mul(u,v):
 a,b,c,d=u;e,f,g,h=v
 return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def inv(u):
 a,b,c,d=u;return(d,-b,-c,a)
G={1:X,-1:inv(X),2:Y,-2:inv(Y)}
def word(w):
 m=I
 for x in w:m=mul(m,G[x])
 return m
def point(m):
 a,b,c,d=m
 assert a*d-b*c==1
 nr,ni=b+c,a-d;dr,di=b-c,a+d;den=dr*dr+di*di
 re,im=F(nr*dr+ni*di,den),F(ni*dr-nr*di,den)
 radius2=re*re+im*im
 assert radius2==F(sum(v*v for v in m)-2,sum(v*v for v in m)+2)
 return re,im,radius2
def features(state):
 mats=(mul(inv(X),word(state[0])),mul(inv(Y),word(state[1])))
 pts=tuple(point(m) for m in mats)
 return {'lengths':tuple(map(len,state)),'matrix':mats,'radii2':tuple(p[2] for p in pts),'disk':tuple(p[:2] for p in pts),'distance_sum':sum(math.acosh(sum(v*v for v in m)/2) for m in mats)}
def plain(f):
 return {k: [[str(x) for x in pair] for pair in v] if k=='disk' else [str(x) for x in v] if k=='radii2' else v for k,v in f.items()}
start=time.monotonic();checkpoint=(ROOT/'continuation/checkpoint.json').read_bytes()
core,spec,doc,challenges=load_kernel()
routes=json.loads((ROOT/'continuation/routes.json').read_text())
seeds={tuple(x['moves']) for x in routes['routes'] if x['row_id']=='ac-00009'}
reports=[]
for moves in sorted(seeds,key=lambda x:(len(x),x)):
 state=tuple(tuple(w) for w in challenges['ac-00009']['initial_relators'])
 fs=[features(state)];states=[state]
 for m in moves:
  state=core.apply_move(state,m);states.append(state);fs.append(features(state))
 assert state==((1,),(2,))
 assert fs[-1]['disk']==((F(0),F(0)),(F(0),F(0)))
 counts={'changed_steps':0,'total_length_unchanged':0,'both_lengths_unchanged':0,'both_radii_unchanged':0,'disk_unchanged':0,'total_length_unchanged_disk_changed':0,'both_radii_unchanged_disk_changed':0}
 examples=[];trace=[]
 for i,m in enumerate(moves):
  a,b=fs[i],fs[i+1];changed=states[i]!=states[i+1];same_l=sum(a['lengths'])==sum(b['lengths']);same_pair=a['lengths']==b['lengths'];same_r=a['radii2']==b['radii2'];same_d=a['disk']==b['disk']
  counts['changed_steps']+=changed;counts['total_length_unchanged']+=same_l;counts['both_lengths_unchanged']+=same_pair;counts['both_radii_unchanged']+=same_r;counts['disk_unchanged']+=same_d;counts['total_length_unchanged_disk_changed']+=same_l and not same_d;counts['both_radii_unchanged_disk_changed']+=same_r and not same_d
  row={'step':i+1,'move':m,'before':plain(a),'after':plain(b),'state_changed':changed}
  if same_l and not same_d and len(examples)<3:examples.append(row)
  trace.append(row)
 assert all((states[i]==states[i+1])==(fs[i]['disk']==fs[i+1]['disk']) for i in range(len(moves)))
 reports.append({'length':len(moves),'moves_sha256':hashlib.sha256(json.dumps(moves,separators=(',',':')).encode()).hexdigest(),'counts':counts,'examples':examples,'trace':trace})
assert checkpoint==(ROOT/'continuation/checkpoint.json').read_bytes()
out={'row':'ac-00009','reports':reports,'route_source_sha256':hashlib.sha256((ROOT/'continuation/routes.json').read_bytes()).hexdigest(),'official_commit':doc['source_commit'],'checkpoint_unchanged':True,'searches':0,'model_workers':0,'elapsed_seconds':time.monotonic()-start,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'interpretation':'Exact representation distinguishes transitions hidden by lossy measurements; no heuristic success or physical-reflection claim.'}
(Path(__file__).parent/'result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='reports'}))
print(json.dumps([{'length':r['length'],'counts':r['counts']} for r in reports]))

