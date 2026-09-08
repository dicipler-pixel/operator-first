#!/usr/bin/env python3
"""
SOFIC-NEW-ROUTES-01
Rooted-gauge / holonomy experiment for permutation-valued 1-cochains.

Purpose
-------
1. Reproduce the exact rooted-gauge identity on complete 2-complexes.
2. Stress-test the same construction on random triangle complexes.
3. Demonstrate why naive finite-group "phase" invariants (e.g. permutation sign)
   are not Hamming-stable: one transposition has Hamming cost 2/n but flips sign.
4. Produce numerical evidence for a useful proposed research lemma:

   If a family of bounded-degree 2-complexes admits rooted spanning trees
   whose fundamental cycles have a uniformly bounded-overlap triangle filling,
   then a positive permutation-cocycle Cheeger lower bound should follow.

The last item is a RESEARCH PROPOSAL, not claimed as a theorem here.
"""

import itertools
import math
import random
from collections import deque
import numpy as np

SEED = 20260823
random.seed(SEED)
np.random.seed(SEED)

# ---------------- permutation primitives ----------------

def identity(n):
    return tuple(range(n))

def compose(p, q):
    """p o q"""
    return tuple(p[q[i]] for i in range(len(p)))

def inverse(p):
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return tuple(r)

def hamming(p, q):
    return sum(a != b for a, b in zip(p, q)) / len(p)

def sign(p):
    invs = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            invs += (p[i] > p[j])
    return -1 if invs % 2 else 1

def random_perm(n):
    p = list(range(n))
    random.shuffle(p)
    return tuple(p)

def triangle_holonomy(alpha, a, b, c):
    return compose(compose(alpha[(a,b)], alpha[(b,c)]), alpha[(c,a)])

# ---------------- graph / gauge primitives ----------------

def bfs_tree(nv, edges, root):
    adj = {v: [] for v in range(nv)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    parent = {root: None}
    q = deque([root])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in parent:
                parent[v] = u
                q.append(v)
    if len(parent) != nv:
        raise ValueError("graph is disconnected")
    return parent

def rooted_gauge(nv, edges, alpha, root, nperm):
    """
    beta(root)=I and beta(v)=alpha(v,parent(v))*beta(parent(v)).
    Then beta.alpha is identity on the BFS tree.
    """
    parent = bfs_tree(nv, edges, root)
    beta = {root: identity(nperm)}

    def get_beta(v):
        if v in beta:
            return beta[v]
        p = parent[v]
        beta[v] = compose(alpha[(v,p)], get_beta(p))
        return beta[v]

    for v in range(nv):
        get_beta(v)

    transformed = {}
    for u, v in edges:
        transformed[(u,v)] = compose(
            compose(inverse(beta[u]), alpha[(u,v)]),
            beta[v]
        )
        transformed[(v,u)] = inverse(transformed[(u,v)])

    return beta, transformed

def random_cochain(nv, edges, nperm):
    alpha = {}
    for u, v in edges:
        p = random_perm(nperm)
        alpha[(u,v)] = p
        alpha[(v,u)] = inverse(p)
    return alpha

def curvature(alpha, triangles, nperm):
    I = identity(nperm)
    if not triangles:
        return float("nan")
    return float(np.mean([
        hamming(triangle_holonomy(alpha, a, b, c), I)
        for a, b, c in triangles
    ]))

def rooted_energy(nv, edges, alpha, nperm):
    """
    Average Hamming norm of the rooted-gauged cochain over all roots.
    This is an upper bound on distance to the cocycles whenever the
    complex has trivial first permutation cohomology; in general it is
    still a diagnostic of how much local curvature is needed to gauge
    away the connection.
    """
    I = identity(nperm)
    vals = []
    for root in range(nv):
        _, tr = rooted_gauge(nv, edges, alpha, root, nperm)
        vals.append(np.mean([hamming(tr[e], I) for e in edges]))
    return float(np.mean(vals))

# ---------------- experiments ----------------

def complete_complex_test():
    print("=" * 78)
    print("A. COMPLETE 2-COMPLEX ROOTED-GAUGE IDENTITY")
    print("=" * 78)
    print("For K_{d+1}^{(2)}, the paper's identity predicts")
    print("    rooted_energy / curvature = (d-1)/(d+1).")
    print()
    for nv in [4, 5, 6, 8, 10]:
        edges = list(itertools.combinations(range(nv), 2))
        triangles = list(itertools.combinations(range(nv), 3))
        ratios = []
        for _ in range(40):
            alpha = random_cochain(nv, edges, 5)
            c = curvature(alpha, triangles, 5)
            e = rooted_energy(nv, edges, alpha, 5)
            if c > 1e-12:
                ratios.append(e / c)
        observed = max(ratios)
        predicted = (nv - 2) / nv
        print(f"K_{nv}: observed={observed:.12f}  predicted={predicted:.12f}"
              f"  error={abs(observed-predicted):.3e}")
    print()

def random_complex_stress():
    print("=" * 78)
    print("B. RANDOM TRIANGLE-COMPLEX STRESS TEST")
    print("=" * 78)
    print("The random complexes keep the complete 1-skeleton but sample triangles.")
    print("This is NOT a proof of a Cheeger bound; it tests whether rooted gauges")
    print("remain quantitatively tied to curvature when triangles become sparse.")
    print()
    nv = 12
    nperm = 5
    edges = list(itertools.combinations(range(nv), 2))
    alltri = list(itertools.combinations(range(nv), 3))

    for p in [0.05, 0.10, 0.20, 0.30, 0.50, 1.0]:
        ratios = []
        counts = []
        for _ in range(12):
            triangles = [t for t in alltri if random.random() < p]
            if not triangles:
                continue
            # Connectedness is automatic because the 1-skeleton is complete.
            local = []
            for _ in range(25):
                alpha = random_cochain(nv, edges, nperm)
                c = curvature(alpha, triangles, nperm)
                if c <= 1e-12:
                    continue
                e = rooted_energy(nv, edges, alpha, nperm)
                local.append(e / c)
            if local:
                ratios.append(max(local))
                counts.append(len(triangles))
        if ratios:
            print(f"p={p:4.2f}  triangles~{np.mean(counts):6.1f}"
                  f"  max observed ratio: {max(ratios):.4f}"
                  f"  median max-ratio: {np.median(ratios):.4f}")
    print()

def phase_kill():
    print("=" * 78)
    print("C. NAIVE INTEGER/PHASE INVARIANTS: HAMMING KILL")
    print("=" * 78)
    print("Take the identity permutation I and a single transposition τ.")
    print("Then d_H(I,τ)=2/n, but sign(I)=+1 and sign(τ)=-1.")
    print("Thus parity/sign can flip at vanishing normalized Hamming cost.")
    print()
    for n in [10, 100, 1000, 10000]:
        p = list(range(n))
        p[0], p[1] = p[1], p[0]
        p = tuple(p)
        print(f"n={n:5d}  Hamming={hamming(identity(n),p):.8f}"
              f"  sign(I)={sign(identity(n)):+d}  sign(tau)={sign(p):+d}")
    print()
    print("Conclusion: a useful 'phase' cannot be a pointwise finite-group")
    print("invariant. It must be a genuinely global quantity whose change")
    print("requires a macroscopic Hamming cost, or an expansion inequality.")
    print()

def proposed_lemma():
    print("=" * 78)
    print("D. PROPOSED ROOTED-GAUGE / FILLING LEMMA")
    print("=" * 78)
    print("""
Let X be a connected finite 2-complex and alpha a Sym(n)-valued 1-cochain.
For every root x choose a spanning tree T_x and gauge beta_x that trivializes
alpha on T_x.

For an edge e not in T_x, its transformed value is the holonomy of the
fundamental cycle C(x,e). If C(x,e) admits a triangular filling F(x,e),
bi-invariance plus the triangle inequality gives

    d_H(hol(C(x,e)), I)
       <= sum_{Delta in F(x,e)} d_H(delta alpha(Delta), I).

Average this over (x,e). If there is a uniform overlap bound

    every triangle belongs to at most M_x,e-weighted fillings,

then

    average_root || beta_x . alpha ||
       <= C_fill || delta alpha ||.

Since distance to cocycles is at most the average rooted gauge energy,
a positive uniform C_fill^{-1} would imply a positive h_1 bound.

This is deliberately stated as a proposed synthesis. The missing work is
to choose the gauges/fillings so that C_fill is uniform in the family and
to handle nontrivial first cohomology correctly (where the target is Z^1,
not merely B^1).
""")
    print()

def main():
    complete_complex_test()
    random_complex_stress()
    phase_kill()
    proposed_lemma()
    print("=" * 78)
    print("END: SOFIC-NEW-ROUTES-01")
    print("=" * 78)

if __name__ == "__main__":
    main()
