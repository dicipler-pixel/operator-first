# SCRIPT: UPG-PROVE-02 (the framework on PUBLISHED data: Yi et al. arXiv:2301.06090
# Raman-lattice QAH band, calibrated t0=0.09, tso=-0.05, delta=-0.2 in E_r units;
# their measured C = -1.00 +/- 0.02)
import numpy as np

t0, tso = 0.09, -0.05

def hvec(qx, qy, dlt):
    return np.array([2*tso*np.sin(qy),
                     2*tso*np.sin(qx),
                     dlt/2 - 2*t0*(np.cos(qx) + np.cos(qy))])

def band_data(dlt, N=201):
    qs = np.linspace(-np.pi, np.pi, N, endpoint=False)
    h = np.array([[hvec(qx, qy, dlt) for qy in qs] for qx in qs])
    nrm = np.linalg.norm(h, axis=2)
    gapm = 2*nrm.min()
    n = -h/nrm[:, :, None]
    dq = qs[1] - qs[0]
    dnx = (np.roll(n, -1, axis=0) - np.roll(n, 1, axis=0))/(2*dq)
    dny = (np.roll(n, -1, axis=1) - np.roll(n, 1, axis=1))/(2*dq)
    gxx = 0.25*np.sum(dnx*dnx, axis=2)
    gyy = 0.25*np.sum(dny*dny, axis=2)
    gxy = 0.25*np.sum(dnx*dny, axis=2)
    F = -0.5*np.sum(n*np.cross(dnx, dny), axis=2)
    detg = gxx*gyy - gxy**2
    ratio = np.abs(F)/(2*np.sqrt(np.maximum(detg, 1e-300)))
    C = np.sum(F)*dq*dq/(2*np.pi)
    volg = np.sum(np.sqrt(np.maximum(detg, 0)))*dq*dq/np.pi
    return C, volg, ratio, gapm

print("=== calibrated band (delta = -0.2 E_r); published C = -1.00 +/- 0.02 ===")
C, volg, ratio, gap = band_data(-0.2)
print(f"  framework Chern (winding currency) = {C:+.5f}")
print(f"  pointwise saturation |F| = 2 sqrt(det g):")
print(f"    mean = {ratio.mean():.8f}   min = {ratio.min():.8f}   max = {ratio.max():.8f}")
print(f"  quantum volume vol_g = {volg:.5f}   vs  |C| = {abs(C):.5f}")

qs = np.linspace(-np.pi, np.pi, 201, endpoint=False)
h = np.array([[hvec(qx, qy, -0.2) for qy in qs] for qx in qs])
n = -h/np.linalg.norm(h, axis=2)[:, :, None]
dq = qs[1] - qs[0]
dnx = (np.roll(n, -1, 0) - np.roll(n, 1, 0))/(2*dq)
dny = (np.roll(n, -1, 1) - np.roll(n, 1, 1))/(2*dq)
F = -0.5*np.sum(n*np.cross(dnx, dny), axis=2)
print(f"  F <= 0 everywhere: {bool(np.all(F <= 1e-12))}")
print()

print("=== rigidity at the walls: gap closings at delta = 0 and -8 t0 = -0.72 ===")
for dlt in [-0.6, -0.71, -0.719, -0.4, -0.2, -0.05, -0.005]:
    C, volg, ratio, gap = band_data(dlt, N=141)
    R = 1/(gap**2 + 1e-12)
    print(f"  delta={dlt:+7.3f}:  C = {C:+7.4f}   gap = {gap:.5f}"
          f"   R = {R:11.2f}   vol_g = {volg:.4f}")
print()

print("=== trivial side (|delta| > 0.72): C -> 0, vol_g stays positive ===")
for dlt in [-0.85, -1.0]:
    C, volg, ratio, gap = band_data(dlt, N=141)
    print(f"  delta={dlt:+7.3f}:  C = {C:+7.4f}   vol_g = {volg:.4f}")
