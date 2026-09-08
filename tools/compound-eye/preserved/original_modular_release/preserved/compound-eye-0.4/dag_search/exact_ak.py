"""Strict public-format arithmetic Kakeya model and exact certificate producer.

Integer input; rational elimination; denominator-cleared integer certificates.
The independent checker is check_ak_certificate.py (standard library only).
No local seeding assumption is used. These are not Epoch's private verifiers.
"""
from fractions import Fraction
from itertools import product, combinations
from math import gcd, lcm, prod
import hashlib
import json
import sympy as sp


def integer(x):
    return type(x) is int


def pair(x):
    if not isinstance(x, (list, tuple)) or len(x) != 2 or not all(integer(z) for z in x):
        raise ValueError("Labels must be pairs of exact integers.")
    return tuple(x)


def validate(p):
    if p.get("schema") != "arithmetic-kakeya-tower-v1":
        raise ValueError("Expected arithmetic-kakeya-tower-v1 schema.")
    dims = p.get("dims")
    if not isinstance(dims, list) or not dims or not all(integer(d) and d > 0 for d in dims):
        raise ValueError("Dimensions must be a nonempty list of positive integers.")
    if prod(dims) > 128:
        raise ValueError("This finite implementation supports at most 128 vertices; larger inputs need an explicit adapter.")
    X = [pair(x) for x in p["X"]]
    if len(X) != len(set(X)) or (0, 0) not in X or any(a+b == 0 for a,b in X if (a,b) != (0,0)):
        raise ValueError("X must be distinct, include zero, and exclude nonzero forbidden-direction labels.")
    V = list(product(*(range(1,d+1) for d in dims)))
    vs = set(V)
    def vertex(v):
        if not isinstance(v, (list,tuple)) or not all(integer(z) for z in v) or tuple(v) not in vs:
            raise ValueError("Vertex outside the declared tower.")
        return tuple(v)
    levels = p["levels"]
    if len(levels) != len(dims):
        raise ValueError("Exactly one level table is required per dimension.")
    for i, entries in enumerate(levels):
        seen = set()
        for item in entries:
            key = tuple(item["prefix"])
            if len(key) != i+1 or not all(integer(z) for z in key):
                raise ValueError("Invalid prefix length or noninteger coordinate.")
            if any(not 1 <= key[j] <= dims[j] for j in range(i)) or not 1 <= key[i] < dims[i]:
                raise ValueError("Prefix outside its entire declared domain.")
            if key in seen or pair(item["label"]) not in X:
                raise ValueError("Duplicate prefix or edge label outside X.")
            seen.add(key)
    T = [vertex(v) for v in p["initial_known"]]
    if len(T) != len(set(T)) or len(T) >= len(V):
        raise ValueError("Initial known vertices must be distinct and leave a positive score denominator.")
    for g in p["generators"]:
        vertex(g["vertex"])
        if pair(g["label"]) not in X or pair(g["label"]) == (0,0):
            raise ValueError("Each generator needs a nonzero label from X.")
    # R is a list in the public verifiable setup. Duplicate entries retain their cost.
    return V


def build(p):
    V = validate(p)
    idx = {v:i for i,v in enumerate(V)}
    n = len(V)
    rows, edges = [], []
    for g in p["generators"]:
        row = [0]*(2*n)
        a = idx[tuple(g["vertex"])]; row[2*a:2*a+2] = g["label"]
        rows.append(row)
    for i, entries in enumerate(p["levels"]):
        for item in entries:
            label = pair(item["label"])
            if label == (0,0):
                continue
            prefix = tuple(item["prefix"])
            for tail in product(*(range(1,d+1) for d in p["dims"][i+1:])):
                a = idx[prefix+tail]
                b = idx[prefix[:-1]+(prefix[-1]+1,)+tail]
                edges.append((a,b,label))
                row = [0]*(2*n)
                row[2*a:2*a+2] = label
                row[2*b:2*b+2] = [-label[0],-label[1]]
                rows.append(row)
    return V, rows, edges


def constraints(rows, n, known, e):
    cols = [c for v in range(n) if v not in known and v != e for c in [2*v, 2*v+1]]
    C = [[r[c] for r in rows] for c in cols]
    C.append([r[2*e]+r[2*e+1] for r in rows])
    t = [r[2*e] for r in rows]
    return C, t


def solve(A, b, columns):
    if columns == 0:
        return [] if all(z == 0 for z in b) else None
    mat = sp.Matrix(A) if A else sp.zeros(0,columns)
    rhs = sp.Matrix(b) if b else sp.zeros(0,1)
    try:
        answer, parameters = mat.gauss_jordan_solve(rhs)
    except ValueError:
        return None
    return [sp.cancel(v.subs({p:0 for p in parameters})) for v in answer]


def integral(values):
    denominator = lcm(*(int(sp.denom(v)) for v in values)) if values else 1
    return [int(v*denominator) for v in values], denominator


def rank2(labels):
    nz = [x for x in labels if any(x)]
    if not nz:
        return 0
    a,b = nz[0]
    return 2 if any(a*y-b*x for x,y in nz[1:]) else 1


def cut_witnesses(p, V, edges):
    if len(V) > 16:
        return {"status":"not_exhausted", "reason":"subset enumeration limited to 16 vertices"}
    idx = {v:i for i,v in enumerate(V)}
    unknown = [i for i,v in enumerate(V) if list(v) not in p["initial_known"]]
    bad = []
    for mask in range(1,1<<len(unknown)):
        S = {unknown[j] for j in range(len(unknown)) if mask>>j&1}
        labels = [tuple(g["label"]) for g in p["generators"] if idx[tuple(g["vertex"])] in S]
        labels += [lab for a,b,lab in edges if (a in S) != (b in S)]
        r = rank2(labels)
        if r < 2:
            bad.append({"subset":[list(V[i]) for i in sorted(S)], "rank":r})
    return {"status":"exhausted", "subsets_checked":(1<<len(unknown))-1,
            "obstructions":bad, "logical_role":"necessary for completion, not sufficient"}


def certify(p, include_cuts=True):
    V, rows, edges = build(p)
    idx = {v:i for i,v in enumerate(V)}
    known = {idx[tuple(v)] for v in p["initial_known"]}
    n = len(V)
    steps = []
    while True:
        changed = False
        for e in range(n):
            if e in known:
                continue
            C,t = constraints(rows,n,known,e)
            answer = solve(C+[t], [0]*len(C)+[1], len(rows))
            if answer is None:
                continue
            coefficients, denominator = integral(answer)
            witness = [sum(c*row[j] for c,row in zip(coefficients,rows)) for j in range(2*n)]
            assert witness[2*e] == denominator and witness[2*e+1] == -denominator
            steps.append({"vertex":list(V[e]), "coefficients":coefficients,
                          "witness":witness, "nonzero_a":denominator})
            known.add(e); changed = True
        if not changed:
            break
    stalled = []
    for e in range(n):
        if e in known:
            continue
        C,t = constraints(rows,n,known,e)
        # Dual identity D*t = sum weights_i*C_i proves the target coordinate
        # vanishes on every vector satisfying the support and (1,1) constraints.
        CT = [list(col) for col in zip(*C)] if rows else []
        weights = solve(CT,t,len(C))
        assert weights is not None
        integers, denominator = integral(weights)
        stalled.append({"vertex":list(V[e]), "constraint_weights":integers,"target_multiplier":denominator})
    m, r, q = len(edges),len(p["generators"]),n-len(p["initial_known"])
    score = Fraction(m+r,q)
    complete = len(known) == n
    report = {"schema":"compound-eye-ak-certificate-v1", "problem":p,
              "input_sha256":hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
              "arithmetic":"exact integer input and integer certificates; rational elimination only inside producer",
              "source_rules":"https://epoch.ai/frontiermath/open-problems/arithmetic-kakeya",
              "n":n,"m":m,"r":r,"t":n-q,"score":str(score),
              "forcing_complete":complete,"forced_vertices":[list(V[i]) for i in sorted(known)],
              "steps":steps,"stalled_dual_certificates":stalled,
              "goal1_score_passes":40*(m+r) <= 67*q,
              "goal1_candidate_passes_public_conditions":complete and 40*(m+r)<=67*q,
              "official_epoch_verifier_run":False,
              "status":"complete_forcing_above_target" if complete and score>Fraction(67,40) else
                       "candidate_meets_public_target" if complete else "incomplete_forcing",
              "scope":"The private Epoch verifier has not been run. No search-space exhaustion follows from this one certificate."}
    if include_cuts:
        report["cut_eye"] = cut_witnesses(p,V,edges)
    return report


def from_legacy(X,dims,fs,T,R,name=""):
    return {"schema":"arithmetic-kakeya-tower-v1","name":name,"X":[list(x) for x in X],"dims":list(dims),
            "levels":[[{"prefix":list(k),"label":list(v)} for k,v in table.items()] for table in fs],
            "initial_known":[list(v) for v in T],
            "generators":[{"vertex":list(next(iter(r))),"label":list(next(iter(r.values())))} for r in R]}


def controls():
    X3=[(0,0),(1,0),(0,1),(1,1)]
    X4=X3+[(1,2)]
    p2=from_legacy(X3,[2,3],[{(1,):(1,0)},{(1,1):(0,1),(1,2):(1,1),(2,1):(0,1),(2,2):(0,1)}],[],
                   [{(1,2):(1,0)},{(2,1):(1,1)},{(1,1):(1,1)},{(1,3):(0,1)}],"Katz-Tao figure 2 as encoded in supplied appendix A.1")
    p3=from_legacy(X4,[2,2],[{(1,):(1,0)},{(1,1):(1,2),(2,1):(0,1)}],[],
                   [{(1,2):(1,1)},{(2,2):(1,1)},{(1,1):(0,1)}],"Katz-Tao figure 3 as encoded in supplied appendix A.1")
    return {"kt_11_6":p2,"kt_7_4":p3}
