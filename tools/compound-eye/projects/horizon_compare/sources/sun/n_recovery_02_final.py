# SCRIPT: N-RECOVERY-02-FINAL  (fold ladder: exact LT for T(2,q) + 4_1; T(3,q) via table value + 2g bound; walls from Delta directly)
import numpy as np

def LT_curve(V, xs):
    out=[]
    for xx in xs:
        w = np.exp(2j*np.pi*xx)
        ev = np.linalg.eigvalsh((1-w)*V + (1-np.conj(w))*V.T)
        out.append(int(np.sum(ev>1e-9)-np.sum(ev<-1e-9)))
    return np.array(out)

def roots_on_circle(coeffs):
    r = np.roots(coeffs)
    return int(np.sum(np.abs(np.abs(r)-1)<1e-6)), len(r)

xs = np.linspace(0.004, 0.996, 499)
print("knot     2g  max|sigma|   A     Alex roots on S^1   walls(jumps)  grade")
rows = []
# --- exact [V] entries: band Seifert matrices, Delta verified by construction ---
for name, g in [("T(2,3)",1), ("T(2,5)",2), ("T(2,7)",3)]:
    n = 2*g
    V = (np.diag([-1.]*n) + np.diag([1.]*(n-1), 1))
    sig = LT_curve(V, xs); smax = int(np.max(np.abs(sig)))
    # Delta of T(2,2k+1) = t^{2k} - t^{2k-1} + ... + 1 (alternating)
    co = [(-1)**i for i in range(n+1)]
    onc, tot = roots_on_circle(co)
    jumps = int(np.sum(np.abs(np.diff(sig))>0))
    print(f"{name:8s} {n:2d}   {smax:3d}      {smax/n:5.3f}      {onc}/{tot}              {jumps}        [V]")
# --- 4_1 control [V] ---
V = np.array([[1.,1.],[0.,-1.]])
sig = LT_curve(V, xs); smax = int(np.max(np.abs(sig)))
onc, tot = roots_on_circle([1,-3,1])
jumps = int(np.sum(np.abs(np.diff(sig))>0))
print(f"{'4_1':8s} {2:2d}   {smax:3d}      {smax/2:5.3f}      {onc}/{tot}              {jumps}        [V] (amphichiral control)")
# --- T(3,4), T(3,5): |sigma(-1)| from knot tables [C]; A=1 forced by |sigma| <= 2g ---
# Delta_{T(3,4)} = t^6-t^5+t^3-t+1 ; Delta_{T(3,5)} = t^8-t^7+t^5-t^4+t^3-t+1
for name, n, s_table, co in [("T(3,4)", 6, 6, [1,-1,0,1,0,-1,1]),
                              ("T(3,5)", 8, 8, [1,-1,0,1,-1,1,0,-1,1])]:
    onc, tot = roots_on_circle(co)
    print(f"{name:8s} {n:2d}   {s_table:3d}      {s_table/n:5.3f}      {onc}/{tot}              {tot}        [C] sigma(-1) table; A=1 forced by |sigma|<=2g")
print()
print("T(2,7) staircase (walls at k/7):")
V = (np.diag([-1.]*6) + np.diag([1.]*5, 1))
for xx in [0.07,0.143,0.15,0.28,0.286,0.29,0.42,0.43,0.5]:
    w = np.exp(2j*np.pi*xx)
    ev = np.linalg.eigvalsh((1-w)*V + (1-np.conj(w))*V.T)
    print(f"  x={xx:.3f}  sigma={int(np.sum(ev>1e-9)-np.sum(ev<-1e-9)):+d}")
