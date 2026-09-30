# SCRIPT: CHARLIE_CORES -- apply the cheapest big cut to every pool row; group rows by the reduced core
# (cyclic words up to rotation, relator inversion, relator swap, and the 8 letter automorphisms)
import json, os, sys, collections
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import cutfirst, charlie_run as cr
M=json.load(open(os.path.join(cr.SAIR, 'verifier/data/manifest.json')))
rows=[c for c in M['challenges'] if c['challenge_id'].startswith('ac-')]
def inv(w): return tuple(-a for a in reversed(w))
def cyc_canon(w):
    if not w: return ()
    rs=[w[i:]+w[:i] for i in range(len(w))]; rs+= [inv(x) for x in rs]; return min(rs)
MAPS=[]
for perm in ((1,2),(2,1)):
    for sx in (1,-1):
        for sy in (1,-1):
            MAPS.append({1:sx*perm[0],-1:-sx*perm[0],2:sy*perm[1],-2:-sy*perm[1]})
def core_key(st):
    best=None
    for f in MAPS:
        a=cyc_canon(tuple(f[x] for x in st[0])); b=cyc_canon(tuple(f[x] for x in st[1]))
        k=min((a,b),(b,a)); k=(len(k[0])+len(k[1]),k)
        if best is None or k<best: best=k
    return best
groups=collections.defaultdict(list); info={}
for c in rows:
    s=tuple(map(tuple,c['initial_relators'])); tot=len(s[0])+len(s[1])
    cs=cutfirst.cuts(s); t,cost,prefix,st=cs[0]
    if t>=tot: continue
    # cyclically reduce is NOT a move; keep the exact state but group by its cyclic class
    k=core_key(st); groups[k].append(c['challenge_id']); info[c['challenge_id']]=(tot,t,cost)
json.dump({str(i):v for i,(k,v) in enumerate(sorted(groups.items(),key=lambda kv:-len(kv[1])))},open(os.path.join(HERE, 'runs/cores_groups.json'),'w'))
sizes=collections.Counter(len(v) for v in groups.values())
print('pool rows',len(rows),'rows with a cut',len(info),'distinct cores',len(groups))
print('group size histogram',sorted(sizes.items(),reverse=True)[:12])
for k,v in sorted(groups.items(),key=lambda kv:-len(kv[1]))[:8]:
    print(len(v),'rows, core total',k[0],v[:8])
target=[k for k,v in groups.items() if 'ac-03719' in v][0]
print('ac-03719 core total',target[0],'group',groups[target])
