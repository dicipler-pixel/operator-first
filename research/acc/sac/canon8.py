"""Canonical form under the full symmetry group used by the external work.

Quotients by relator order, cyclic rotation, relator inversion, and the eight
signed permutations of the generators (x<->y, x->x^-1, y->y^-1). Strictly
coarser than the cyclic-only form, so it can expose collisions that one misses.
Letters: 0=x 1=X 2=y 3=Y.
"""
import sys
sys.path.insert(0, "tools/acc/eyes")
import replay as R

def _swap(c):      return {0: 2, 1: 3, 2: 0, 3: 1}[c]
def _negx(c):      return {0: 1, 1: 0, 2: 2, 3: 3}[c]
def _negy(c):      return {0: 0, 1: 1, 2: 3, 3: 2}[c]

def _gens():
    out = []
    for sw in (False, True):
        for nx in (False, True):
            for ny in (False, True):
                def f(c, sw=sw, nx=nx, ny=ny):
                    if sw: c = _swap(c)
                    if nx: c = _negx(c)
                    if ny: c = _negy(c)
                    return c
                out.append(f)
    return out

PERMS = _gens()

def _cyc_min(w):
    w = R.cyclic_reduce(list(w))
    if not w:
        return ()
    rots = [tuple(w[i:] + w[:i]) for i in range(len(w))]
    rots += [tuple(R.invert(list(r))) for r in rots]
    return min(rots)

def canon8(st):
    best = None
    for p in PERMS:
        a = _cyc_min([p(c) for c in st[0]])
        b = _cyc_min([p(c) for c in st[1]])
        k = tuple(sorted((a, b)))
        if best is None or k < best:
            best = k
    return best


# --- move transport under the symmetry -------------------------------------
# Letters 0=x 1=X 2=y 3=Y. Moves: 0,1 invert r0,r1; 2..5 multiply;
# 6..9 conjugate r0 by x,X,y,Y; 10..13 conjugate r1 by x,X,y,Y.

def relabel_moves(moves, perm, swap_relators):
    """Rewrite a move list so it acts the same way on a relabelled state."""
    out = []
    for m in moves:
        if m in (0, 1):
            n = m
        elif m in (2, 3, 4, 5):
            n = m
        elif 6 <= m <= 9:
            n = 6 + perm(m - 6)
        else:
            n = 10 + perm(m - 10)
        if swap_relators:
            n = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3}.get(n,
                 n + 4 if 6 <= n <= 9 else n - 4 if 10 <= n <= 13 else n)
        out.append(n)
    return out

def apply_perm_state(st, perm, swap_relators):
    a = tuple(perm(c) for c in st[0])
    b = tuple(perm(c) for c in st[1])
    return (b, a) if swap_relators else (a, b)


def target_fix(perm, swap_relators):
    """Moves that carry the relabelled target back to (x, y).

    A relabelling sends (x, y) to (p(x), p(y)); SAC needs the path to end on
    (x, y) exactly, so inverted generators are corrected with moves 0 and 1.
    Returns None when the image is not a signed permutation of the target.
    """
    a, b = perm(0), perm(2)
    if swap_relators:
        a, b = b, a
    fix = []
    if a == 1:
        fix.append(0)
    elif a != 0:
        return None
    if b == 3:
        fix.append(1)
    elif b != 2:
        return None
    return fix
