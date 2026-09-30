import sys, json
sys.path.insert(0,'/root/.cache/upgh/sair/competition/tools')
from verifier import core
m=json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json'))
C={c['challenge_id']:c for c in m['challenges']}
L={1:'x',-1:'X',2:'y',-2:'Y'}
st0=tuple(tuple(r) for r in C['ac-06045']['initial_relators'])
def replay(p):
    s=st0
    for mv in p: s=core.apply_move(s,mv)
    return s
def w(r): return ''.join(L[t] for t in r)
seeds={'b12':[5,12,12,12,12,0,2,6,1,13,11,5],'c12':[5,12,12,12,12,0,2,6,6,8,1,5],'d12':[5,12,12,12,12,0,2,6,6,8,2,5],'a12':[1,2,5,8,8,8,8,5,10,9,7,3]}
exp={'b12':('YYxyyyyyx','XYXXYYY'),'c12':('yxYYxyyyy','XXYYYXY'),'d12':('yxyyyxx','YYYYXyyXY'),'a12':('XYXXYYY','YYxyyyyyx')}
for k,p in seeds.items():
    s=replay(p); got=(w(s[0]),w(s[1])); print(k,len(p),got,exp[k],got==exp[k])
