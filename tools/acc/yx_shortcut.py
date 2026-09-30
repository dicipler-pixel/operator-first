# For an AC path of length L, find i and a route s_i -> (y, x) of length <= L-i-1 (exact meet in the middle),
# giving a Stable AC line of length <= L+1 (route to (y,x) + destabilize twice). Official core replays.
import json, sys, os
sys.path.insert(0, os.environ['SAIR'] + '/competition/tools'); from verifier import core
INV=(0,1,3,2,5,4,7,6,9,8,11,10,13,12)
def hop(start, T, fd, bd, cap):
    ln=lambda s: len(s[0])+len(s[1]); B={T:[]}; fr=[T]
    for d in range(bd):
        nf=[]
        for s in fr:
            for m in range(14):
                y=core.apply_move(s,m)
                if y in B or ln(y)>cap: continue
                B[y]=[INV[m]]+B[s]; nf.append(y)
        fr=nf
    F={start:[]}; fr=[start]
    for d in range(fd+1):
        hits=[F[s]+B[s] for s in fr if s in B]
        if hits: return min(hits,key=len)
        nf=[]
        for s in fr:
            for m in range(14):
                y=core.apply_move(s,m)
                if y in F or ln(y)>cap: continue
                F[y]=F[s]+[m]; nf.append(y)
        fr=nf
    return None
man=json.load(open(os.environ['SAIR']+'/competition/tools/verifier/data/manifest.json')); CH={c['challenge_id']:c for c in man['challenges']}
cid, path = sys.argv[1], json.loads(sys.argv[2]); target=int(sys.argv[3])   # target = SAC length to reach
s=tuple(tuple(w) for w in CH[cid]['initial_relators']); states=[s]
for m in path: s=core.apply_move(s,m); states.append(s)
L=len(path); YX=((2,),(1,))
for i in range(L-1, max(L-10,0)-1, -1):
    budget=target-2-i          # moves allowed from s_i to (y,x)
    if budget<0: continue
    fd=(budget+1)//2; bd=budget-fd
    r=hop(states[i], YX, fd, bd, 40)
    if r is not None and i+len(r)+2<=target:
        sac=path[:i]+r
        chk=((2,),(1,)) ; t=tuple(tuple(w) for w in CH[cid]['initial_relators'])
        for m in sac: t=core.apply_move(t,m)
        print(json.dumps({'id':'s'+cid,'len':len(sac)+2,'prefix':i,'route':r,'ok':t==YX,'line':sac}))
        break
else: print(json.dumps({'id':'s'+cid,'none_within':L-10}))
