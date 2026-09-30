import sys,os,json
sys.path.insert(0,'/root/.cache/upgh/sair/competition/tools'); from verifier import core
M=json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json'))
CH={c['challenge_id']:c for c in (M['challenges'] if isinstance(M,dict) and 'challenges' in M else M)}
L={1:'x',-1:'X',2:'y',-2:'Y'}; E={v:k for k,v in L.items()}
S=lambda t:''.join(L[a] for a in t); W=lambda s:tuple(E[c] for c in s)
def st(cid): c=CH[cid]; return tuple(tuple(r) for r in c['initial_relators']), tuple(tuple(r) for r in c['target_relators'])
def run(s,mv):
    for m in mv: s=core.apply_move(s,m)
    return s
def traj(s,mv):
    out=[(None,S(s[0]),S(s[1]))]
    for m in mv: s=core.apply_move(s,m); out.append((m,S(s[0]),S(s[1])))
    return out
