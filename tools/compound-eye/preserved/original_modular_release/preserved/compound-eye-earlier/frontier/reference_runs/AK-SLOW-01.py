# SCRIPT: AK-SLOW-01  -- careful exhaustive study of the smallest towers.
# LEMMA under test: with T0 empty, U=V has no crossing edges, so L(V) = span(generator labels);
# hence r>=2 and the generators must contain two independent directions.
# Then: minimum complete-forcing score for [2], [2,2], [3], [2,2] with X = {0,(1,0),(0,1),(1,1)}.
exec(open('akv2.py').read().split("print(\"CONTROL 1")[0])
import itertools
from fractions import Fraction

X = [(0,0),(1,0),(0,1),(1,1)]
NZ = [x for x in X if x != (0,0)]

def prefixes(dims, i):
    return list(itertools.product(*[range(1,dims[j]+1) for j in range(i)], range(1,dims[i])))

def study(dims, rmax=4, verbose_best=True):
    V = [tuple(e) for e in itertools.product(*[range(1,d+1) for d in dims])]
    n = len(V)
    P = [prefixes(dims,i) for i in range(len(dims))]
    npref = sum(len(p) for p in P)
    best = None; bestcfg = None; tested = 0
    for labels in itertools.product(X, repeat=npref):
        fs = []; idx = 0
        for i in range(len(dims)):
            fs.append({tuple(p): labels[idx+j] for j,p in enumerate(P[i])}); idx += len(P[i])
        # quick m
        mm = 0
        for i in range(len(dims)):
            tail = 1
            for j in range(i+1,len(dims)): tail *= dims[j]
            mm += sum(tail for p in P[i] if fs[i][tuple(p)] != (0,0))
        for r in range(2, rmax+1):
            if best is not None and Fraction(mm+r, n) >= best: continue
            for gens in itertools.combinations([(v,x) for v in V for x in NZ], r):
                tested += 1
                R = [{v:x} for (v,x) in gens]
                try: ak = AK(X, dims, fs, [], R)
                except AssertionError: continue
                T = ak.run()
                if len(T) != n: continue
                s = Fraction(ak.m()+r, n)
                if best is None or s < best:
                    best = s; bestcfg = (dict((k,v) for k,v in enumerate(fs)), gens, ak.m(), r)
    return best, bestcfg, tested, n

for dims in ([1],[2],[3],[2,2]):
    best, cfg, tested, n = study(dims, rmax=4)
    print("dims=%-8s n=%-3d  tested %-8d  BEST SCORE = %-8s (%.4f)" %
          (dims, n, tested, best, float(best) if best else float('nan')))
    if cfg:
        fs, gens, m, r = cfg
        print("      m=%d  r=%d   labels: %s" % (m, r, {i: {k:v for k,v in d.items() if v!=(0,0)} for i,d in fs.items()}))
        print("      generators: %s" % (list(gens),))
    print()
