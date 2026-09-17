#!/usr/bin/env python3
"""Conjugacy BFS — moves 6..13 ONLY.

Answers exactly one question: are two official starts the same ordered pair up to
slot-wise conjugation? That is NOT "are they AC-equivalent" — products 2-5 and
inversions 0-1 are off, because products change the Nielsen class in the strong sense
and can leave the conjugacy orbit.

State key is the FREELY REDUCED ORDERED PAIR. Never a cyclic hash, never conj_sig:
those are eyes and cannot transfer a CLOSED count.

  path found   => S and T are the same conjugacy problem, and CLOSED(S,C) copies to T at C
  path missing => "same signed-generator family" stays a HYPOTHESIS. It does not prove
                  they are different orbits; only that no conjugacy word within the
                  searched depth and cap connects them.
"""
import json,sys
from collections import deque
sys.path.insert(0,"/home/user/operator-first/tools/acc/eyes")
from replay import apply_move, free_reduce

CONJ=[6,7,8,9,10,11,12,13]          # the ONLY legal generators for this test

def key(s): return (tuple(free_reduce(list(s[0]))), tuple(free_reduce(list(s[1]))))

def conjugacy_bfs(S,T,cap=None,limit=3_000_000):
    S=key(S); T=key(T)
    if S==T: return []
    q=deque([(S,())]); seen={S}
    while q and len(seen)<limit:
        s,path=q.popleft()
        for m in CONJ:
            a,b=apply_move(list(s[0]),list(s[1]),m)
            ns=(tuple(a),tuple(b))
            if cap is not None and len(a)+len(b)>cap: continue
            if ns in seen: continue
            np=path+(m,)
            if ns==T: return list(np)
            seen.add(ns); q.append((ns,np))
    return None

def replay_check(S,path,T):
    a,b=[list(x) for x in S]
    for m in path: a,b=apply_move(a,b,m)
    return (tuple(a),tuple(b))==key(T)

def expsum(w):
    ex=sum(1 if c==0 else -1 if c==1 else 0 for c in w)
    ey=sum(1 if c==2 else -1 if c==3 else 0 for c in w)
    return ex,ey
def detM(s):
    (a,b),(c,d)=expsum(s[0]),expsum(s[1])
    return a*d-b*c

if __name__=="__main__":
    C2P={1:0,-1:1,2:2,-2:3}
    O={i["challengeId"]:i for i in json.load(open("snapshot_items_prev.json"))}
    def st(c):
        r=O[c]["initialRelators"]          # official snapshot, not a hand transcript
        return ([C2P[x] for x in r[0]],[C2P[x] for x in r[1]])
    base=sys.argv[1]; sibs=sys.argv[2].split(","); cap=int(sys.argv[3]) if len(sys.argv)>3 else None
    S=st(base); L="xXyY"
    def show(s): return ("".join(L[c] for c in s[0]),"".join(L[c] for c in s[1]))
    print(f"base {base}: {show(S)}  |det M| = {abs(detM(S))}")
    for cid in sibs:
        T=st(cid)
        d=abs(detM(T))
        p=conjugacy_bfs(S,T,cap=cap)
        if p is None:
            print(f"  {cid}: {show(T)}  |det M|={d}  -> NO conjugacy path found "
                  f"(hypothesis only; NOT proof of a different orbit)")
        else:
            ok=replay_check(S,p,T)
            print(f"  {cid}: {show(T)}  |det M|={d}  -> PATH len={len(p)} {p} "
                  f"replay={'OK' if ok else 'FAIL'}"
                  + ("  => CLOSED transfers" if ok else "  => DO NOT TRANSFER"))
