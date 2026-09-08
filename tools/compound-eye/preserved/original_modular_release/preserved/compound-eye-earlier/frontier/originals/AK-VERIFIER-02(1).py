# SCRIPT: AK-VERIFIER-02   (exact, no search in op 2)
import itertools
from fractions import Fraction
from math import gcd

def hnf(rows):
    M = [list(r) for r in rows if any(r)]
    if not M: return []
    nc = len(M[0]); pr = 0
    for c in range(nc):
        while True:
            nz = [r for r in range(pr, len(M)) if M[r][c] != 0]
            if not nz: break
            if len(nz) == 1:
                M[pr], M[nz[0]] = M[nz[0]], M[pr]; pr += 1; break
            nz.sort(key=lambda r: abs(M[r][c])); p = nz[0]
            for r in nz[1:]:
                q = M[r][c] // M[p][c]
                for j in range(nc): M[r][j] -= q*M[p][j]
        if pr >= len(M): break
    return sorted([r for r in M if any(r)])

def kernel_of_functional(rows, phi):
    """basis of { integer combos of rows : sum c_i phi(row_i) = 0 }, returned as vectors."""
    vals = [phi(r) for r in rows]
    if all(v == 0 for v in vals): return [list(r) for r in rows]
    out = []
    piv = next(i for i,v in enumerate(vals) if v != 0)
    for i,v in enumerate(vals):
        if i == piv: continue
        g = gcd(abs(v), abs(vals[piv])) or 1
        a, b = vals[piv]//g, v//g          # a*v - b*vals[piv] = 0
        out.append([a*rows[i][t] - b*rows[piv][t] for t in range(len(rows[i]))])
    return hnf(out)

def restrict_zero(rows, cols):
    M = [list(r) for r in rows]
    for c in cols:
        if not M: return []
        nz = [r for r in range(len(M)) if M[r][c] != 0]
        while len(nz) > 1:
            nz.sort(key=lambda r: abs(M[r][c])); p = nz[0]
            for r in nz[1:]:
                q = M[r][c] // M[p][c]
                for j in range(len(M[r])): M[r][j] -= q*M[p][j]
            nz = [r for r in range(len(M)) if M[r][c] != 0]
        if nz: M = [M[r] for r in range(len(M)) if r != nz[0]]
        M = [r for r in M if any(r)]
    return hnf(M)

class AK:
    def __init__(self, X, dims, fs, T, R):
        self.X = [tuple(x) for x in X]
        assert (0,0) in self.X
        for (a,b) in self.X:
            if (a,b) != (0,0): assert a+b != 0, "X element with a+b=0: %s" % ((a,b),)
        self.d = list(dims); self.k = len(dims); self.fs = fs
        self.V = [tuple(e) for e in itertools.product(*[range(1,d+1) for d in self.d])]
        self.idx = {v:i for i,v in enumerate(self.V)}
        self.T0 = set(map(tuple, T))
        self.R0 = [{tuple(v): tuple(x) for v,x in r.items()} for r in R]
        for r in self.R0:
            assert len([1 for v,x in r.items() if tuple(x)!=(0,0)]) == 1
    def n(self):
        p=1
        for d in self.d: p*=d
        return p
    def m(self):
        tot=0
        for i in range(self.k):
            tail=1
            for j in range(i+1,self.k): tail*=self.d[j]
            for pref,x in self.fs[i].items():
                if tuple(x)!=(0,0): tot+=tail
        return tot
    def vec(self, fd):
        v=[0]*(2*len(self.V))
        for w,x in fd.items():
            i=self.idx[tuple(w)]; v[2*i]+=x[0]; v[2*i+1]+=x[1]
        return v
    def edge_gens(self):
        out=[]
        for i in range(self.k):
            for pref,x in self.fs[i].items():
                x=tuple(x)
                if x==(0,0): continue
                a=list(pref)
                for tail in itertools.product(*[range(1,self.d[j]+1) for j in range(i+1,self.k)]):
                    e1=tuple(a)+tail; e2=tuple(a[:-1]+[a[-1]+1])+tail
                    if e1 in self.idx and e2 in self.idx:
                        out.append({e1:x, e2:(-x[0],-x[1])})
        return out
    def run(self):
        B = hnf([self.vec(r) for r in self.R0] + [self.vec(g) for g in self.edge_gens()])
        T = set(self.T0); prog=True
        while prog and len(T) < len(self.V):
            prog=False
            for e in self.V:
                if e in T: continue
                free = T | {e}
                cols=[]
                for v in self.V:
                    if v not in free: cols += [2*self.idx[v], 2*self.idx[v]+1]
                S = restrict_zero(B, cols)
                if not S: continue
                ei = self.idx[e]
                K = kernel_of_functional(S, lambda w: w[2*ei] + w[2*ei+1])
                if any(w[2*ei] != 0 for w in K):
                    T.add(e); prog=True
        return T
    def report(self, name):
        T=self.run(); ok=(len(T)==len(self.V))
        num=self.m()+len(self.R0); den=self.n()-len(self.T0)
        s=Fraction(num,den)
        print("  %-22s n=%-4d m=%-4d |R|=%-3d |T0|=%-3d forced %d/%d  complete=%-5s score=%s = %.5f"
              %(name,self.n(),self.m(),len(self.R0),len(self.T0),len(T),len(self.V),ok,s,float(s)))
        return ok,s

print("CONTROL 1 -- trivial AK(2): single vertex, both generators on it, (1,-1)=(1,0)-(0,1)")
X=[(0,0),(1,0),(0,1)]
AK(X,[1],[{}],[],[{(1,):(1,0)},{(1,):(0,1)}]).report("AK(2) single vertex")

print("\nCONTROL 2 -- does the edge operation actually fire? path of 2 with an edge")
AK(X,[2],[{(1,):(1,0)}],[],[{(1,):(1,0)},{(1,):(0,1)},{(2,):(0,1)}]).report("path-2")

print("\nCONTROL 3 -- op 2 must NOT fire when it shouldn't (negative control)")
AK(X,[1],[{}],[],[{(1,):(1,0)}]).report("one generator only")
