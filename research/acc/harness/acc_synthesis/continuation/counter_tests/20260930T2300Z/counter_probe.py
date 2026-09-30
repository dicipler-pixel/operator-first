"""Predeclared read-only forward/reverse score comparison. No route search."""
import sys,json,math,time,resource,hashlib
from pathlib import Path
from functools import lru_cache
resource.setrlimit(resource.RLIMIT_AS,(1024*1024*1024,1024*1024*1024))
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel
I=(1,0,0,1);X=(1,2,0,1);Y=(1,0,2,1)
def mul(a,b):
 p,q,r,s=a;t,u,v,w=b
 return(p*t+q*v,p*u+q*w,r*t+s*v,r*u+s*w)
def inv(a):
 p,q,r,s=a;return(s,-q,-r,p)
G={1:X,-1:inv(X),2:Y,-2:inv(Y)}
@lru_cache(None)
def rho(w):
 m=I
 for x in w:m=mul(m,G[x])
 return m
@lru_cache(None)
def score(state):
 return sum(math.acosh(sum(x*x for x in mul(inv(target),rho(w)))/2) for target,w in zip((X,Y),state))
def midrank(values,index):
 t=values[index];same=[math.isclose(v,t,rel_tol=1e-12,abs_tol=1e-12) for v in values]
 less=sum(v<t and not eq for v,eq in zip(values,same))
 return(less+0.5*(sum(same)-1))/(len(values)-1)
def mean(xs):return sum(xs)/len(xs) if xs else None
begin=time.monotonic();cp_before=(ROOT/'continuation/checkpoint.json').read_bytes();cp=json.loads(cp_before)
assert not cp['stopped'] and cp['active'] is None
core,spec,doc,starts=load_kernel()
inputs=json.loads((OUT/'inputs.json').read_text())
routes={len(x['moves']):x['moves'] for x in inputs['routes']}
assert set(routes)=={78,112}
start=tuple(tuple(x) for x in starts['ac-00009']['initial_relators'])
def trace(moves):
 states=[start]
 for m in moves:states.append(core.apply_move(states[-1],m))
 assert states[-1]==((1,),(2,))
 return states
old=set(trace(routes[112]));states=trace(routes[78]);rows=[]
for i,(state,m) in enumerate(zip(states,routes[78])):
 if state in old:continue
 assert time.monotonic()-begin<180
 choices=[core.apply_move(state,j) for j in range(14)]
 distances=[score(x) for x in choices];lengths=[sum(map(len,x)) for x in choices]
 a=midrank(distances,m);b=midrank([-x for x in distances],m)
 assert abs(a+b-1)<1e-12
 delta=lengths[m]-sum(map(len,state))
 rows.append({'step':i+1,'state':state,'recorded_move':m,'move_class':'climb' if delta>0 else 'shrink' if delta<0 else 'flat','delta_length':delta,'distance_scores':distances,'length_scores':lengths,'toward_rank':a,'away_rank':b,'length_rank':midrank(lengths,m)})
assert len(rows)<=78 and len(rows)*14<=1092
groups={}
for group in ['all','climb','flat','shrink']:
 subset=rows if group=='all' else [x for x in rows if x['move_class']==group]
 groups[group]={'count':len(subset),**{k:mean([x[k] for x in subset]) for k in ['toward_rank','away_rank','length_rank']}}
assert cp_before==(ROOT/'continuation/checkpoint.json').read_bytes()
main=groups['all']
winner='no_new_states' if not rows else 'toward' if main['toward_rank']<main['away_rank'] else 'away' if main['away_rank']<main['toward_rank'] else 'tie'
result={'kind':'completed_readonly_diagnostic','row':'ac-00009','primary_observed_winner':winner,'groups':groups,'rows':rows,'source_hashes':{p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ['protocol.json','inputs.json','counter_probe.py']},'official_commit':doc['source_commit'],'elapsed_seconds':time.monotonic()-begin,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'one_step_evaluations':len(rows)*14,'model_workers':0,'new_searches':0,'checkpoint_unchanged':True,'limits':'Selected related states on an already discovered route. Not independent trials, shortest-path labels or prospective search outcomes. No score enabled.'}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['rows','source_hashes']}))

