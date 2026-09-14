"""Exhaustive bidirectional BFS on challenges nobody has solved.
Forward BFS from the initial presentation, level by level, each level tested
for membership in the precomputed depth-7 backward ball around the target.
A hit at forward depth d gives a certificate of length d + back[state]."""
import sys, json, time, pickle
sys.path.insert(0,"/home/user/saircompetition/andrews-curtis/competition/tools")
from verifier import core
TARGET=((1,),(2,)); AM=core.apply_move
def L(s): return len(s[0])+len(s[1])

man=json.load(open("/home/user/saircompetition/andrews-curtis/competition/tools/verifier/data/manifest.json"))
LIM=man["limits"]; idx={c["challenge_id"]:c for c in man["challenges"]}
print("loading back7...",flush=True); t0=time.time()
back=pickle.load(open("/tmp/claude-0/back7.pkl","rb"))
print(f"back7={len(back):,} loaded {time.time()-t0:.0f}s",flush=True)

def descend(s):
    out=[]; d=back[s]
    while d>0:
        for m in range(14):
            t=AM(s,m)
            if back.get(t,99)==d-1: out.append(m); s=t; d-=1; break
        else: raise RuntimeError("stuck")
    return out

def hunt(cid, cap_extra, node_budget, maxdepth):
    c=idx[cid]; start=tuple(tuple(w) for w in c["initial_relators"])
    cap=L(start)+cap_extra
    if start in back:
        mv=descend(start); return mv
    par={start:None}; fr=[start]; total=1
    for d in range(1,maxdepth+1):
        nx=[]
        for s in fr:
            for m in range(14):
                t=AM(s,m)
                if L(t)>cap or t in par: continue
                par[t]=(s,m); nx.append(t)
                if t in back:
                    path=[]; cur=t
                    while par[cur] is not None:
                        p,mm=par[cur]; path.append(mm); cur=p
                    return path[::-1]+descend(t)
        fr=nx; total+=len(nx)
        print(f"    {cid} fwd depth {d}: frontier={len(nx):,} total={total:,} cap={cap}",flush=True)
        if total>node_budget:
            print(f"    {cid}: node budget hit, stopping",flush=True); return None
        if not nx:
            print(f"    {cid}: SPACE EXHAUSTED at depth {d} -- PROOF: no certificate exists with every intermediate total length <= {cap}",flush=True)
            return None
    return None

# shortest unsolved first
import os
targets=[(c,0) for c in os.environ.get("CIDS","ac-00008").split(",")]
cap_extra=int(sys.argv[1]) if len(sys.argv)>1 else 8
budget=int(sys.argv[2]) if len(sys.argv)>2 else 4_000_000
for cid,ln in targets:
    print(f"\n=== {cid} (init len {ln}) ===",flush=True)
    t0=time.time()
    mv=hunt(cid,cap_extra,budget,int(os.environ.get("MAXD","80")))
    if mv is None:
        print(f"  {cid}: no certificate within budget ({time.time()-t0:.0f}s)",flush=True); continue
    c=idx[cid]
    v=core.verify({"challenge_id":cid,"move_spec_version":"ac-r2-v1",
        "initial_relators":c["initial_relators"],"target_relators":c["target_relators"]},
        mv,"ac-r2-v1",LIM)
    print(f"  *** {cid} SOLVED len={len(mv)} verify_ok={v.get('ok')} ({time.time()-t0:.0f}s)",flush=True)
    if v.get("ok"):
        json.dump({"challenge_id":cid,"moves":mv,"length":len(mv)},
                  open(f"/tmp/claude-0/SOLVED_{cid}.json","w"))
