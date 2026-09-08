#!/usr/bin/env python3
# SCRIPT: DKIST-COMPARE-02
# The comparison run in the convention-free direction: from the independently
# computed shear-layer width to the predicted wavelength.
#
# SHEAR-LANE-01 fixes ONE dimensionless number with no observational input:
#       k_max * d = 0.450     =>     lambda / d = 2*pi/0.450 = 13.96
# d is the tanh half-width in U = tanh(y/d) and is convention-free.
# WHAT WAS AN INPUT: the observed spacings, used in the v1 width inversion.
# WHAT WAS NOT: the growth rates and the companion layer width, below.
# What is NOT convention-free is how a paper reports "shear layer width" from a
# tanh profile. Standard choices span 2d (scale width) to 4d (96% of the jump).
# So their 12 km maps to a BAND of d, hence a BAND of predicted wavelength.
import numpy as np
LAM_D = 2*np.pi/0.450          # 13.963, fixed by the computation
W_MURAM = 12.0                 # km, companion MURaM shear layer
LAM_OBS, LAM_LO, LAM_HI = 65.0, 25.0, 170.0   # peak and full observed span
print("="*76); print("DKIST-COMPARE-02   their width -> our wavelength"); print("="*76)
print(f"\n  fixed by the computation alone:  lambda/d = {LAM_D:.3f}")
print(f"  independently computed layer:  W_MURaM = {W_MURAM:.0f} km")
print(f"  observed wavelength:           peak {LAM_OBS:.0f} km  (span {LAM_LO:.0f}-{LAM_HI:.0f})")
print(f"\n  {'convention':<34} {'d (km)':>8} {'predicted lambda (km)':>22} {'vs 65':>9}")
convs=[("2d   scale width",2.0),("2.94d 90% of the jump",2.94),
       ("3d   common tanh reporting",3.0),("4d   96% of the jump",4.0)]
preds=[]
for name,f in convs:
    d=W_MURAM/f; lam=LAM_D*d; preds.append(lam)
    print(f"  {name:<34} {d:>8.2f} {lam:>22.1f} {lam/LAM_OBS:>8.2f}x")
lo,hi=min(preds),max(preds)
print(f"\n  predicted band from their 12 km: {lo:.1f} - {hi:.1f} km")
print(f"  observed peak 65 km lies inside the band: {lo <= LAM_OBS <= hi}")
print(f"  the convention that would make it exact: W = {W_MURAM/(LAM_OBS/LAM_D):.2f} d "
      f"(between the 2d and 4d conventions)")

print("\n  RUN THE OTHER WAY (our wavelength -> our width), for the record:")
d_from_obs = LAM_OBS/LAM_D
print(f"    observed lambda 65 km  =>  d = {d_from_obs:.2f} km")
print(f"    => 2d = {2*d_from_obs:.1f} km   2.94d = {2.94*d_from_obs:.1f} km   4d = {4*d_from_obs:.1f} km")
print(f"    their 12 km sits at {W_MURAM/d_from_obs:.2f} d, inside that range")

print("\n  WHAT IS ACTUALLY FALSIFIABLE, and is not yet tested:")
print("    the ratio lambda/d = 13.96 is a PREDICTION about the mode, not a fit.")
print("    Publishing d under a stated convention turns the band above into a")
print("    single number and the comparison into a pass or a fail.")
print(f"\n  growth-rate cross-check (independent of all width conventions):")
sig_obs=(0.014,0.054)          # s^-1, measured
U_lo,U_hi=0.67e3,3.0e3         # m/s apparent speeds
d_m=d_from_obs*1e3
print(f"    Michalke peak for a tanh layer: sigma_max ~ 0.19 * (dU/2) / d")
for U in (U_lo,U_hi):
    print(f"      dU = {U/1e3:.2f} km/s -> sigma = {0.19*(U/2)/d_m:.4f} s^-1")
print(f"    measured range: {sig_obs[0]}-{sig_obs[1]} s^-1")
print("="*76)
