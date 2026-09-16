"""Phase 2: canonical form of the unordered relator pair under the full symmetry group —
cyclic rotation, inversion, the 8 signed generator permutations, relator swap, after
free + cyclic reduction. Records WHICH element mapped the raw state to the canonical form."""
import hashlib
from replay import free_reduce, invert, cyclic_reduce

def _gen_maps():
    """The 8 signed generator permutations of F2, as letter->letter tables."""
    maps=[]
    for swap in (0,1):
        for sx in (0,1):
            for sy in (0,1):
                # image of the generator x, and of y, as letters
                ix = (2|sx) if swap else (0|sx)
                iy = (0|sy) if swap else (2|sy)
                img=[ix,iy]
                tbl=[]
                for c in range(4):
                    base=c>>1; sign=c&1
                    L=img[base]
                    tbl.append(L^1 if sign else L)
                maps.append(((swap,sx,sy),tuple(tbl)))
    return maps

GEN_MAPS=_gen_maps()

def _apply_map(w,tbl): return [tbl[c] for c in w]

def _rotations(w):
    n=len(w)
    if n==0: return [()]
    return [tuple(w[i:]+w[:i]) for i in range(n)]

def _reps(w,tbl):
    """All (rotation of) the mapped word and its inverse, cyclically reduced."""
    m=cyclic_reduce(_apply_map(w,tbl))
    out=[]
    for inv in (0,1):
        u=invert(m) if inv else m
        u=cyclic_reduce(u)
        for j,rot in enumerate(_rotations(u)):
            out.append((rot,inv,j))
    return out

def canonical(r0,r1):
    """Returns (canonical_pair, element) where element describes the symmetry taken."""
    best=None
    for gname,tbl in GEN_MAPS:
        A=_reps(r0,tbl); B=_reps(r1,tbl)
        for (wa,ia,ja) in A:
            for (wb,ib,jb) in B:
                for swapped in (0,1):
                    pair=(wb,wa) if swapped else (wa,wb)
                    key=(len(pair[0])+len(pair[1]), pair)
                    if best is None or key<best[0]:
                        best=(key,pair,{"gen":gname,"inv_r0":ia,"rot_r0":ja,
                                        "inv_r1":ib,"rot_r1":jb,"swap":swapped})
    return best[1],best[2]

def canonical_hash(r0,r1):
    pair,elem=canonical(r0,r1)
    s=repr(pair).encode()
    return hashlib.sha256(s).hexdigest(), elem
