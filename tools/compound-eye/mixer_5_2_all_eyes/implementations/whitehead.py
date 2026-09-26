#!/usr/bin/env python3
"""Whitehead graph and cut-vertex test for a SAIR ordered pair.

Vertices are the four letters x, X, y, Y. For each consecutive pair (a,b) in each
CYCLIC relator, the standard Whitehead graph adds an edge  a^{-1} -- b.  (The brief
writes it as "edge ab"; the inverse convention is the one under which Whitehead's
cut-vertex criterion is actually valid, so both are reported and any disagreement
is shown rather than hidden.)

  disconnected, or a cut vertex  ->  some Whitehead multiplier STRICTLY SHORTENS the pair.
                                     A Nielsen invitation. Not a certificate: the
                                     automorphism must still be compiled into official
                                     0-13 and replayed.
  connected and 2-connected      ->  a STRUCTURAL signal about free splittings ONLY.

*** RETRACTED: this file previously claimed 2-connected => Whitehead-minimal. That is
    FALSE. Minimality is decided by testing the finite Type-II Whitehead family for a
    length drop -- see wh_min.py. Measured counterexamples: ac-01083 and ac-03525 are both
    2-connected here and both shorten from cyclic total 15 to 14. Board-wide, this file
    reported 0 shortenable rows; the exact test finds 748 of 2,672. Use wh_min.py. ***

This is an eye on the NIELSEN metric. It never transfers a CLOSED count and it is never
a conjugacy test -- conjugation only rotates a core, so Wh is conjugation-invariant and
cannot tell ac-03467 from ac-08126.
"""
import json,sys
from collections import defaultdict
sys.path.insert(0,"/home/user/operator-first/tools/acc/eyes")
from replay import free_reduce
L="xXyY"

def cyclic_reduce(w):
    w=list(free_reduce(list(w)))
    while len(w)>=2 and w[0]==(w[-1]^1): w=w[1:-1]
    return w

def wh_edges(words, inverse_convention=True):
    E=defaultdict(int)
    for w in words:
        c=cyclic_reduce(w); n=len(c)
        if n<2: continue
        for i in range(n):
            a,b=c[i],c[(i+1)%n]
            u=(a^1) if inverse_convention else a
            E[tuple(sorted((u,b)))]+=1
    return E

def components(verts,E):
    adj=defaultdict(set)
    for (u,v) in E:
        if u!=v: adj[u].add(v); adj[v].add(u)
    seen=set(); comps=0
    for s in verts:
        if s in seen: continue
        comps+=1; st=[s]; seen.add(s)
        while st:
            x=st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
    return comps

def analyse(r0,r1,inv=True):
    E=wh_edges([r0,r1],inv)
    verts=sorted({u for e in E for u in e})
    base=components(verts,E)
    cuts=[]
    for v in verts:
        E2={e:c for e,c in E.items() if v not in e}
        v2=[u for u in verts if u!=v]
        if not v2: continue
        if components(v2,E2)>components(v2,{e:c for e,c in E.items() if v not in e}) or \
           components(v2,E2)>base:
            cuts.append(v)
    # recompute cleanly: a cut vertex raises the component count of the remaining graph
    cuts=[]
    for v in verts:
        v2=[u for u in verts if u!=v]
        E2={e:c for e,c in E.items() if v not in e}
        if v2 and components(v2,E2)>max(1,base):
            cuts.append(v)
    return E,verts,base,cuts

if __name__=="__main__":
    C2P={1:0,-1:1,2:2,-2:3}
    O={i["challengeId"]:i for i in json.load(open("snapshot_items_prev.json"))}
    ids=sys.argv[1].split(",")
    print(f"{'challenge':11}{'|V|':>4}{'comps':>6}{'cut vertices':>16}   verdict")
    for cid in ids:
        r=O[cid]["initialRelators"]
        r0=[C2P[x] for x in r[0]]; r1=[C2P[x] for x in r[1]]
        E,verts,base,cuts=analyse(r0,r1)
        if base>1 or cuts:
            v=f"SHORTENABLE (Nielsen invitation) cuts={[L[c] for c in cuts]}"
        else:
            v="2-CONNECTED -> Whitehead-minimal; tot-first is doomed; hump + T_R lane"
        print(f"{cid:11}{len(verts):>4}{base:>6}{str([L[c] for c in cuts]):>16}   {v}")
