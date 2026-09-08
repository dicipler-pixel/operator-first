# SCRIPT: AK-CUT-THEOREM-CHECK
# THEOREM (derived above): a vertex e in U = V\T can fall only if the CUT LATTICE
#   L(U) = span_Z{ x_j : g_j in U } + span_Z{ x_edge : edge crosses boundary of U }
# has rank 2.  Reason: summing w over U kills every interior edge (telescoping) and every
# edge with both ends outside U; only the cut survives.  And rank 1 is fatal because every
# label has s(x)=x1+x2 != 0, so a rank-1 lattice contains no (a,-a).
# TEST: instrument the verifier -- at every step, before declaring e forced, compute rank L(U)
# over Q and assert it is 2.  A single counterexample kills the theorem.
exec(open('akv2.py').read().split("print(\"CONTROL 1")[0])
import itertools
from fractions import Fraction

def cut_rank(ak, T, R0):
    U = [v for v in ak.V if v not in T]
    Us = set(U)
    vecs = []
    for r in R0:
        for v, x in r.items():
            if tuple(x) != (0,0) and tuple(v) in Us: vecs.append(list(x))
    for g in ak.edge_gens():
        ends = [v for v in g]
        inU = [v for v in ends if v in Us]
        if len(inU) == 1:
            x = g[inU[0]]; vecs.append(list(x))
    if not vecs: return 0
    M = Matrix = None
    # rank over Q of 2-column vectors
    import itertools as it
    rk = 0
    basis = []
    for v in vecs:
        if all(c == 0 for c in v): continue
        if not basis: basis.append(v); continue
        if len(basis) == 1:
            b = basis[0]
            if b[0]*v[1] - b[1]*v[0] != 0: basis.append(v)
    return len(basis)

def run_checked(ak, label):
    B = hnf([ak.vec(r) for r in ak.R0] + [ak.vec(g) for g in ak.edge_gens()])
    T = set(ak.T0); prog = True; order = []; viol = 0
    while prog and len(T) < len(ak.V):
        prog = False
        for e in ak.V:
            if e in T: continue
            free = T | {e}
            cols = []
            for v in ak.V:
                if v not in free: cols += [2*ak.idx[v], 2*ak.idx[v]+1]
            S = restrict_zero(B, cols)
            if not S: continue
            ei = ak.idx[e]
            K = kernel_of_functional(S, lambda w: w[2*ei] + w[2*ei+1])
            if any(w[2*ei] != 0 for w in K):
                rk = cut_rank(ak, T, ak.R0)
                if rk != 2: viol += 1; print("   VIOLATION at", e, " cut rank =", rk)
                order.append((e, rk))
                T.add(e); prog = True
    return T, order, viol

print("Checking the cut-rank theorem on every object we have that forces completely.\n")
X3 = [(0,0),(1,0),(0,1)]
cases = [
 ("AK(2) single vertex", AK(X3,[1],[{}],[],[{(1,):(1,0)},{(1,):(0,1)}])),
 ("path-2",              AK(X3,[2],[{(1,):(1,0)}],[],[{(1,):(1,0)},{(1,):(0,1)},{(2,):(0,1)}])),
]
tot_viol = 0
for name, ak in cases:
    T, order, viol = run_checked(ak, name)
    tot_viol += viol
    print("  %-22s forced %d/%d   cut ranks along the cascade: %s   violations: %d"
          % (name, len(T), len(ak.V), [rk for _, rk in order], viol))

print("\nNEGATIVE CONTROL -- a rank-1 cut must never force.")
ak = AK(X3,[2],[{(1,):(1,0)}],[],[{(1,):(1,0)}])   # only label (1,0) anywhere: L(U) rank 1
T, order, viol = run_checked(ak, "rank-1 only")
print("  all labels (1,0): forced %d/%d  (theorem predicts 0)  %s"
      % (len(T), len(ak.V), "PASS" if len(T) == 0 else "FAIL"))

print("\nLAST-VERTEX COROLLARY: when U={e}, the cut is exactly e's incident edges.")
print("  => the final vertex needs two independent directions on its OWN edges/generators.")
print("  total violations across all runs:", tot_viol)
