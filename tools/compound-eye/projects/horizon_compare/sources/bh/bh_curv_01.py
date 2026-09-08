# SCRIPT: BH-CURV-01 -- fresh derivation of the Jacobi curvature term on Sigma_4
# via O'Neill for the submersion S^{d^2-1} (flat sphere of X's, ||X||_F=1) -> Sigma
# under X -> RX (SO(d) left action), base coordinate G = X^T X (the audited invariant).
# GATES:
# G1: d=2 control -- Kendall shape sphere sectional curvature == 4 (exact known value)
# G2: symmetry K_curv(a,b) = K_curv(b,a)
# G3: row/column along V vanishes (R(V,V)V structure)
# G4: quotient metric g_ab = <H_a,H_b> reported (tests the paper's silent g=I assumption)
# G5: blow-up structure of shear entries as w1 -> w2 (exponent + which entries)
import mpmath as mp
import numpy as np
mp.mp.dps = 40

def frob(A,B): return float('nan') # placeholder (numpy used below)

def make_basis3():
    import numpy as np
    E1 = np.diag([1,-1,0])/np.sqrt(2)
    E2 = np.diag([1,1,-2])/np.sqrt(6)
    E3 = np.zeros((3,3)); E3[0,1]=E3[1,0]=1/np.sqrt(2)
    E4 = np.zeros((3,3)); E4[0,2]=E4[2,0]=1/np.sqrt(2)
    E5 = np.zeros((3,3)); E5[1,2]=E5[2,1]=1/np.sqrt(2)
    return [E1,E2,E3,E4,E5]

def skew_basis(d):
    import numpy as np
    out=[]
    for i in range(d):
        for j in range(i+1,d):
            O=np.zeros((d,d)); O[i,j]=1; O[j,i]=-1
            out.append(O)
    return out

class Submersion:
    def __init__(self,d):
        import numpy as np
        self.d=d; self.np=np
        self.sk=skew_basis(d)
    def lift(self,X,E):
        # solve X^T H + H^T X = E (sym, d(d+1)/2 eqs), X H^T - H X^T = 0 (skew, d(d-1)/2 eqs)
        np=self.np; d=self.d
        rows=[]; rhs=[]
        def vec(i,j):
            z=np.zeros((d,d)); z[i,j]=1; return z
        cols=[(i,j) for i in range(d) for j in range(d)]
        Msys=np.zeros((d*d,d*d))
        b=np.zeros(d*d)
        r=0
        for i in range(d):
            for j in range(i,d):
                for c,(k,l) in enumerate(cols):
                    Hc=vec(k,l)
                    val=(X.T@Hc + Hc.T@X)[i,j]
                    Msys[r,c]=val
                b[r]=E[i,j]; r+=1
        for i in range(d):
            for j in range(i+1,d):
                for c,(k,l) in enumerate(cols):
                    Hc=vec(k,l)
                    val=(X@Hc.T - Hc@X.T)[i,j]
                    Msys[r,c]=val
                b[r]=0.0; r+=1
        h=np.linalg.solve(Msys,b)
        return h.reshape(d,d)
    def sphere_proj(self,X,Z):
        return Z - (self.np.sum(X*Z))*X
    def vert_proj(self,X,Z):
        np=self.np
        Vb=[O@X for O in self.sk]
        G=np.array([[np.sum(a*b) for b in Vb] for a in Vb])
        rhs=np.array([np.sum(a*Z) for a in Vb])
        c=np.linalg.solve(G,rhs)
        V=sum(ci*vi for ci,vi in zip(c,Vb))
        return V
    def A_tensor(self,X,H1,E2,eps=1e-6):
        # A_{H1} (lift field of E2) = vert( sphere-covariant derivative along H1 )
        np=self.np
        Xp=X+eps*H1; Xp=Xp/np.linalg.norm(Xp)
        Xm=X-eps*H1; Xm=Xm/np.linalg.norm(Xm)
        Lp=self.lift(Xp,E2); Lm=self.lift(Xm,E2)
        D=(Lp-Lm)/(2*eps)
        D=self.sphere_proj(X,D)
        return self.vert_proj(X,D)

def sigma4_curvature(w, Vcoef, eps=1e-6):
    import numpy as np
    d=3; sub=Submersion(3)
    s=np.sqrt(np.array(w)); X=np.diag(s)
    Es=make_basis3()
    Hs=[sub.lift(X,E) for E in Es]
    g=np.array([[np.sum(Hs[a]*Hs[b]) for b in range(5)] for a in range(5)])
    HV=sum(c*H for c,H in zip(Vcoef,Hs))
    AV=[sub.A_tensor(X,HV,Es[b],eps) for b in range(5)]
    K=np.zeros((5,5))
    gV=np.array([np.sum(HV*Hs[a]) for a in range(5)]); VV=np.sum(HV*HV)
    for a in range(5):
        for b in range(5):
            sph=VV*g[a,b]-gV[a]*gV[b]
            K[a,b]=sph+3*np.sum(AV[a]*AV[b])
    return K,g

import numpy as np
print("=== GATE G1: Kendall d=2 control (expect sectional curvature 4) ===")
sub2=Submersion(2)
for (a,b) in [(0.7,0.3),(0.5,0.5),(0.9,0.1)]:
    X=np.diag([np.sqrt(a),np.sqrt(b)])
    # base tangent basis on trace-one symmetric 2x2: diag direction + offdiag
    F1=np.diag([1,-1])/np.sqrt(2)
    F2=np.array([[0,1],[1,0]])/np.sqrt(2)
    H1=sub2.lift(X,F1); H2=sub2.lift(X,F2)
    g11=np.sum(H1*H1); g22=np.sum(H2*H2); g12=np.sum(H1*H2)
    A12=sub2.A_tensor(X,H1,F2)
    num=(1.0*(g22*g11-g12**2))+3*np.sum(A12*A12) # sphere K=1 sectional part + O'Neill
    K_sec=num/(g11*g22-g12**2)
    print(f" w=({a},{b}): sectional K = {K_sec:.10f}")

print("\n=== Sigma_4: curvature quadratic form K_curv(a,b) for generic V ===")
w=(0.5,0.3,0.2)
V=np.array([0.3,-0.2,0.4,0.1,-0.5]); V=V/np.linalg.norm(V)
K,g=sigma4_curvature(w,V)
print("quotient metric g_ab (GATE G4 -- is it identity?):")
print(np.array2string(g,precision=6,suppress_small=True))
print("K_curv:")
print(np.array2string(K,precision=6,suppress_small=True))
print("GATE G2 symmetry: max|K-K^T| =",np.max(np.abs(K-K.T)))
KV=K@np.linalg.solve(g,np.array([np.sum(V[a]*g[a]) for a in range(5)])) if False else None
# G3: contract with V in the metric sense: K acting paired with V-lift should vanish
gV=g@V
print("GATE G3 |K . (g^{-1} gV)| structure: |K @ V| =",np.max(np.abs(K@np.linalg.solve(g,gV))))

print("\n=== GATE G5: blow-up as w1 -> w2 (V purely in shape direction E1) ===")
Vs=np.array([1.0,0,0,0,0])
for dlt in [1e-1,1e-2,1e-3,1e-4]:
    w=(0.4+dlt/2,0.4-dlt/2,0.2)
    K,g=sigma4_curvature(w,Vs,eps=min(1e-6,dlt*1e-3))
    print(f" w1-w2={dlt:.0e}: K33={K[2,2]:.6e} K44={K[3,3]:.6e} K55={K[4,4]:.6e} g33={g[2,2]:.6e}")

print("\n=== GATE G6: the TRUE wall -- blow-up at the coplanar stratum w3 -> 0 ===")
print("metric prediction: g22 = sum (E2)_ii^2/(4 w_i) contains 4/(24 w3) = 1/(6 w3) -> infinity")
Vg=np.array([0.3,-0.2,0.4,0.1,-0.5]); Vg=Vg/np.linalg.norm(Vg)
for w3 in [1e-1,1e-2,1e-3,1e-4]:
    w=(0.55,0.45-0, w3); w=(0.55*(1-w3)/1.0, 0.45*(1-w3)/1.0, w3)
    K,g=sigma4_curvature(w,Vg,eps=min(1e-6,w3*1e-2))
    pred=1/(6*w3)
    print(f" w3={w3:.0e}: g22={g[1,1]:.6e} (1/(6w3)={pred:.3e}) K44={K[3,3]:.4e} K55={K[4,4]:.4e} K22={K[1,1]:.4e}")
print("fit: K44*w3, K55*w3 ->")
vals=[]
for w3 in [1e-2,1e-3,1e-4]:
    w=(0.55*(1-w3), 0.45*(1-w3), w3)
    K,g=sigma4_curvature(w,Vg,eps=min(1e-6,w3*1e-2))
    vals.append((w3,K[3,3]*w3,K[4,4]*w3,g[1,1]*6*w3))
for v in vals: print(f" w3={v[0]:.0e}: K44*w3={v[1]:.6f} K55*w3={v[2]:.6f} g22*6*w3={v[3]:.6f}")
