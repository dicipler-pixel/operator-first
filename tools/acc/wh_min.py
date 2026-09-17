#!/usr/bin/env python3
"""EXACT Whitehead minimisation for rank 2 — replaces the cut-vertex claim.

CORRECTION (ChatGPT, 2026-09-17). The previous eye asserted
    connected and no cut vertex  =>  Whitehead-minimal
That is too strong. Connectivity/cut structure is a structural signal about free
splittings. Minimality is decided by TESTING THE FINITE WHITEHEAD FAMILY for a length
drop. Type-I (signed permutations) preserve length; the Type-II multipliers are the ones
that can shorten.

Type-II, rank 2: pick a distinguished letter a, and a set A with a in A, a^-1 not in A.
Every other letter c maps to
    c        if c notin A and c^-1 notin A
    c a      if c in A, c != a
    a^-1 c   if c^-1 in A, c != a^-1
    a^-1 c a if both c and c^-1 in A
and a -> a. Applied to BOTH relators, then cyclically reduced.

Minimal  <=>  no Type-II map strictly lowers the cyclic total length.
"""
import sys
sys.path.insert(0,"/home/user/operator-first/tools/acc/eyes")
from replay import free_reduce
L="xXyY"
def cyc(w):
    w=list(free_reduce(list(w)))
    while len(w)>=2 and w[0]==(w[-1]^1): w=w[1:-1]
    return w

def type2_maps():
    """(name, letter -> word) for every legal (a,A) in rank 2, identity excluded."""
    out=[]
    for a in range(4):
        ai=a^1
        others=[c for c in range(4) if c!=a and c!=ai]
        for mask in range(1<<len(others)):
            A={a} | {others[i] for i in range(len(others)) if mask>>i & 1}
            if ai in A: continue
            img={}
            for c in range(4):
                if c==a or c==ai:
                    img[c]=[c]; continue
                cin=c in A; ciin=(c^1) in A
                if cin and ciin:   img[c]=[ai,c,a]
                elif cin:          img[c]=[c,a]
                elif ciin:         img[c]=[ai,c]
                else:              img[c]=[c]
            if all(img[c]==[c] for c in range(4)): continue
            out.append(((L[a],"".join(L[z] for z in sorted(A))),img))
    return out
MAPS=type2_maps()

def apply_map(w,img):
    out=[]
    for c in w: out.extend(img[c])
    return out

def cyclen(r0,r1): return len(cyc(r0))+len(cyc(r1))

def minimise(r0,r1):
    """Returns (is_minimal, best_drop, best_map_name, new_pair)."""
    base=cyclen(r0,r1); best=None
    for name,img in MAPS:
        n0=apply_map(r0,img); n1=apply_map(r1,img)
        c=cyclen(n0,n1)
        if c<base and (best is None or c<best[0]):
            best=(c,name,(cyc(n0),cyc(n1)))
    if best is None: return True,0,None,None
    return False,base-best[0],best[1],best[2]

if __name__=="__main__":
    import json
    C2P={1:0,-1:1,2:2,-2:3}
    O={i["challengeId"]:i for i in json.load(open("snapshot_items_prev.json"))}
    print(f"Type-II maps in the family: {len(MAPS)}\n")
    for cid in sys.argv[1].split(","):
        r=O[cid]["initialRelators"]
        r0=[C2P[x] for x in r[0]]; r1=[C2P[x] for x in r[1]]
        mn,drop,name,new=minimise(r0,r1)
        base=cyclen(r0,r1)
        if mn: print(f"{cid}: cyclic total {base}  -> MINIMAL (no Type-II drop)")
        else:
            print(f"{cid}: cyclic total {base}  -> SHORTENS by {drop} to {base-drop} "
                  f"via a={name[0]} A={{{name[1]}}}  new=({''.join(L[c] for c in new[0])},"
                  f"{''.join(L[c] for c in new[1])})")
