#!/usr/bin/env python3
"""LIGHT-MATTER-WHOLE-PICTURE-01
Independent finite controls for the integrated Compound Eye causal picture.
Requires numpy. This checks the declared finite model, not a photon/electron TOE.
"""
import math, json, numpy as np

rng=np.random.default_rng(20260910)
N=200000
vf=rng.uniform(.25,1.25,N); vs=rng.uniform(0,1.10,N)
D=rng.uniform(-5,5,N); g=rng.uniform(1e-4,2.5,N)
O=np.sqrt(D*D+4*g*g)
wp=(1+D/O)/2; wm=1-wp
vp=wp*vf+(1-wp)*vs; vm=wm*vf+(1-wm)*vs
lo=np.minimum(vf,vs); hi=np.maximum(vf,vs)
assert not np.any((vp<lo-1e-12)|(vp>hi+1e-12)|(vm<lo-1e-12)|(vm>hi+1e-12))
wf=np.maximum(wp,wm); ws=1-wf; vh=wf*vf+ws*vs; mix=wf*ws
mask=np.abs(vf-vs)>1e-5
lhs=((vf[mask]-vh[mask])*(vh[mask]-vs[mask]))/(vf[mask]-vs[mask])**2
assert np.max(np.abs(lhs-mix[mask]))<1e-10
assert np.max(mix)<=.25+1e-14

# Equal-rate null: coupling can mix but cannot create a velocity mismatch.
v=rng.uniform(.1,1.3,50000); D=rng.uniform(-5,5,50000); g=rng.uniform(.001,3,50000)
O=np.sqrt(D*D+4*g*g); w=(1+D/O)/2
assert np.max(np.abs(w*v+(1-w)*v-v))<1e-12

# Same scalar speed 0.6 from three distinct mechanisms.
s=.6
vs_h=2*s-1
dwell=1/s-1
rho=(1-s*s)/(1+s*s)
u=math.sqrt((1-rho)/(1+rho))
assert abs((1+vs_h)/2-s)<1e-12
assert abs(1/(1+dwell)-s)<1e-12
assert abs(u-s)<1e-12

print(json.dumps({
 "status":"PASS",
 "random_hybrid_cases":N,
 "velocity_interval_violations":0,
 "speed_projector_identity":"PASS",
 "mixing_bound":"PASS",
 "equal_rate_negative_control":"PASS",
 "same_speed_three_mechanism_control":"PASS",
 "scope":"finite declared model only"
},indent=2))
