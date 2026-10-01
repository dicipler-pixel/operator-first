"""Synthetic algebra checks only; no challenge search or production mutation."""
import json,random,resource,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import official_checker
from helpers.paid_phase_lane_v1 import class_key,normalizer,recipes,cancel,inverse_path
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
core,*_=official_checker.load_kernel();rng=random.Random(1709);begin=time.monotonic();moves_checked=0
def replay(s,path):
 global moves_checked
 for m in path:
  moves_checked+=1;assert moves_checked<600000 and time.monotonic()-begin<180
  s=core.apply_move(s,m)
 return s
bases=[((1,2,1,-2),(2,1,2,-1)),((1,1),(2,2)),((1,),(2,)),((),(1,2))]
for n in range(160):
 base=bases[n%len(bases)];allowed=[0,1,6,7,8,9,10,11,12,13]
 s=replay(base,[rng.choice(allowed) for _ in range(rng.randrange(20))]);t=replay(base,[rng.choice(allowed) for _ in range(rng.randrange(20))]);key=class_key(s);assert class_key(t)==key
 for rel in (0,1):
  for direction in ('forward','reverse'):
   path=normalizer(s[rel],rel,direction,key[rel]);u=replay(s,path);assert u[rel]==key[rel] and u[1-rel]==s[1-rel]
 for arm,path in recipes(s,t,key).items():
  assert replay(s,path)==t,(arm,s,t,path)
  assert replay(t,inverse_path(path))==s
  assert cancel(path+inverse_path(path))==[]
print(json.dumps({'synthetic_pairs':160,'formulas_replayed':1120,'primitive_moves_checked':moves_checked,'elapsed_seconds':time.monotonic()-begin,'model_workers':0,'challenge_searches':0}))
