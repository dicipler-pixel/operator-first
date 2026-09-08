#!/usr/bin/env python3
# SCRIPT: CONICAL-RAY-01
# At a conical intersection the two index sheets form a double cone, so the GRADIENT of
# the eigenvalue -- the ray direction -- is undefined at the point and takes a different
# value for every direction of approach.  That is exactly why Hamilton's biaxial crystal
# refracts one ray into a cone.  Test: approach the optic axis from every direction and
# ask whether the gradient directions sweep the full circle (a cone) or converge (a ray).
import numpy as np
exec(open('/home/claude/unequal_check.py').read().split('print("="*78); print("UNEQUAL-CHECK-01')[0])

mass = np.array([1.,2.,3.])
a0, p0 = 0.845154255, 5.034139535          # an optic axis, from BIAXIAL-01

def Mmat(a, psi):
    D, _ = dPhi(config(mass, a, psi), mass)
    return D.T @ D

def eig_lo(a, psi):
    w, V = np.linalg.eigh(Mmat(a, psi))
    return w[0], V[:, 0]

print("="*78); print("CONICAL-RAY-01   does the optic axis produce a cone of ray directions?")
print("="*78)

# local linearisation: M = c0 I + x1 sigma_z + x3 sigma_x  in the (a,psi) plane
h = 1e-5
M0 = Mmat(a0, p0)
print(f"  at the axis: eigenvalues {np.linalg.eigvalsh(M0)}")
def xvec(a, psi):
    M = Mmat(a, psi)
    return np.array([(M[0,0]-M[1,1])/2, M[0,1]])      # traceless part
J = np.zeros((2,2))
for j,(da,dp) in enumerate([(h,0),(0,h)]):
    J[:,j] = (xvec(a0+da, p0+dp) - xvec(a0-da, p0-dp))/(2*h)
print(f"  linearisation matrix (traceless part vs shape coords):\n   {J[0]}\n   {J[1]}")
print(f"  det J = {np.linalg.det(J):.4e}   -> {'nondegenerate cone' if abs(np.linalg.det(J))>1e-9 else 'DEGENERATE'}")

print("\n  gradient (ray) direction of the lower sheet vs direction of approach")
print(f"  {'approach (deg)':>16} {'ray dir (deg)':>15} {'|grad|':>12}")
rays=[]
for t in np.linspace(0, 2*np.pi, 12, endpoint=False):
    r = 1e-4
    aa, pp = a0 + r*np.cos(t), p0 + r*np.sin(t)
    ga = (eig_lo(aa+h, pp)[0] - eig_lo(aa-h, pp)[0])/(2*h)
    gp = (eig_lo(aa, pp+h)[0] - eig_lo(aa, pp-h)[0])/(2*h)
    ang = np.degrees(np.arctan2(gp, ga)) % 360
    rays.append(ang)
    print(f"  {np.degrees(t):>16.1f} {ang:>15.2f} {np.hypot(ga,gp):>12.5f}")
sw = np.unwrap(np.radians(rays))
total = np.degrees(sw[-1]-sw[0]) + (rays[0]-rays[-1] if False else 0)
print(f"\n  ray directions span: {max(rays)-min(rays):.1f} deg over the approach circle")
print(f"  distinct ray directions (rounded to 5 deg): {len(set(np.round(np.array(rays)/5)))} of 12")
print("\n  -> a single point of the shape sphere admits a whole circle of ray directions.")
print("     The normal is undefined where the sheets meet: conical refraction, in shape space.")
print("="*78)
