"""Reimplementation of tools/acc/acc_finisher_v1.py's algorithm against the verified
replay in tools/acc/eyes/replay.py (its own verifier.core dependency is absent here).

Same three steps: official replay -> earliest CORRIDOR state (exactly one relator is a
single letter) -> exact BFS from there to (x,y) with total length capped at L_entry+cap,
splicing only if strictly shorter.

The one change is that cap is a dial, not fixed at 2. REPORT_ACC's ac-09868 comparison --
40 moves peaking at 15 versus 25 moves peaking at 20 -- says the shorter path CLIMBS
HIGHER. A cap of +2 forbids that climb by construction, so it can only ever find the long
low road. Move count and peak length are recorded separately, never inferred from each
other.
"""
import sys
from collections import deque
sys.path.insert(0,"/home/user/operator-first/tools/acc/eyes")
from replay import apply_move, TARGET

def states(r0,r1,mv):
    a,b=list(r0),list(r1); out=[(tuple(a),tuple(b))]
    for m in mv:
        a,b=apply_move(a,b,m); out.append((tuple(a),tuple(b)))
    return out

def peak(st): return max(len(a)+len(b) for a,b in st)

def corridor_entry(st):
    """earliest state where EXACTLY ONE relator is a single letter (the finisher's rule)"""
    for k,s in enumerate(st):
        if (len(s[0])==1) != (len(s[1])==1): return k
    return None

def bfs_to_target(start,cap,node_limit=2_000_000):
    seen={start:[]}; q=deque([start])
    n=0
    while q:
        s=q.popleft()
        if s==TARGET: return seen[s],n
        for m in range(14):
            a,b=apply_move(list(s[0]),list(s[1]),m)
            if len(a)+len(b)>cap: continue
            t=(tuple(a),tuple(b))
            if t in seen: continue
            seen[t]=seen[s]+[m]; n+=1
            if n>node_limit: return None,n
            q.append(t)
    return None,n

def finish(r0,r1,mv,cap):
    st=states(r0,r1,mv)
    e=corridor_entry(st)
    if e is None: return None,{"reason":"no corridor entry"}
    L=sum(len(w) for w in st[e])
    tail,n=bfs_to_target(st[e],L+cap)
    if tail is None: return None,{"reason":"no exact finish","entry":e,"L_entry":L,"nodes":n}
    new=list(mv[:e])+tail
    ns=states(r0,r1,new)
    ok=ns[-1]==TARGET
    return (new if ok and len(new)<len(mv) else None), {
        "entry":e,"L_entry":L,"cap":L+cap,"orig_len":len(mv),"new_len":len(new),
        "orig_peak":peak(st),"new_peak":peak(ns),"nodes":n,"verified":ok}
