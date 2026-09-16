"""SECOND ENGINE — deliberately independent of ac_shared_ball_v1.c.

Different language, different state representation (immutable tuples of letters, not
two packed uint64 words), different hashing (Python's own dict, not a hand-rolled
open-addressing table), different traversal bookkeeping. It shares no code and no data
structure with the C engine; the only thing in common is the definition of the fourteen
AC moves, which is the thing being cross-checked.

It also answers a question the C engine never asked. That engine reported component
SIZES. Equal sizes are consistent with one graph under two names and equally consistent
with two isomorphic-but-distinct graphs. This enumerates the component as a SET and
compares the sets directly.
"""
import sys,json
def fr(w):
    o=[]
    for c in w:
        if o and o[-1]==(c^1): o.pop()
        else: o.append(c)
    return tuple(o)
def iv(w): return tuple(c^1 for c in reversed(w))
def nbrs(st,cap):
    a,b=st; out=[]
    la,lb=len(a),len(b)
    out.append((iv(a),b)); out.append((a,iv(b)))
    for w,other,slot in ((fr(a+b),lb,0),(fr(a+iv(b)),lb,0),
                         (fr(b+a),la,1),(fr(b+iv(a)),la,1)):
        if len(w)+other<=cap:
            out.append((w,b) if slot==0 else (a,w))
    for g in range(4):
        w=fr((g,)+a+(g^1,))
        if len(w)+lb<=cap: out.append((w,b))
    for g in range(4):
        w=fr((g,)+b+(g^1,))
        if len(w)+la<=cap: out.append((a,w))
    return out
def component(start,cap,limit):
    seen={start}; stack=[start]
    while stack:
        s=stack.pop()
        for t in nbrs(s,cap):
            if t not in seen:
                seen.add(t)
                if len(seen)>limit: return seen,False
                stack.append(t)
    return seen,True
if __name__=="__main__":
    C2P={1:0,-1:1,2:2,-2:3}
    O={i["challengeId"]:i for i in json.load(open("snapshot_items_prev.json"))}
    ids=sys.argv[1].split(","); cap=int(sys.argv[2]); limit=int(sys.argv[3])
    comps={}
    for cid in ids:
        rel=O[cid]["initialRelators"]
        st=(fr([C2P[x] for x in rel[0]]),fr([C2P[x] for x in rel[1]]))
        c,done=component(st,cap,limit)
        comps[cid]=c
        print(f"{cid} cap={cap} states={len(c)} closed={done}",flush=True)
    a,b=ids[0],ids[1]
    A,B=comps[a],comps[b]
    print(f"\nsame size      : {len(A)==len(B)}")
    print(f"IDENTICAL SET  : {A==B}")
    if A!=B:
        print(f"  |A\\B|={len(A-B)}  |B\\A|={len(B-A)}  |A&B|={len(A&B)}")
    tgt=((0,),(2,))
    print(f"target in A    : {tgt in A}")
    print(f"target in B    : {tgt in B}")
