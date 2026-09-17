#!/usr/bin/env python3
"""Finite/structural continuation audit for QG archive recovery sections 11-37.

This checker preserves useful mathematical shapes and negative knowledge. It does
not prove physical identifications, APS/Mostow theorem contracts, gravity, MOND,
particle ontology, or emergent gauge/Lorentz/Dirac claims.
"""
from pathlib import Path
import cmath,json,math

HERE=Path(__file__).resolve().parent
SOURCE_SHA256='3f74061c0515b2e9b4be424f256315c7d5c7daee8e51f6bbd6b578314025e79b'

def req(cond,name,checks):
    if not cond: raise AssertionError(name)
    checks.append(name)

def proj(theta):
    c,s=math.cos(theta),math.sin(theta)
    return ((c*c,c*s),(c*s,s*s))

def mmul2(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def tr2(a): return a[0][0]+a[1][1]

def overlap(p0,theta): return tr2(mmul2(p0,proj(theta)))

def H(theta):
    c,s=math.cos(theta),math.sin(theta)
    return ((-c*c+s*s,-2*c*s),(-2*c*s,-s*s+c*c))

def eig2(a):
    t=a[0][0]+a[1][1];d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    q=math.sqrt(max(0,t*t-4*d));return ((t-q)/2,(t+q)/2)

def outer(v):
    return tuple(tuple(v[i]*v[j].conjugate() for j in range(2)) for i in range(2))

def main():
    c=[]

    # 12-14: spectral flow belongs naturally to paths/morphisms.
    sf1,sf2=2,-1
    req(sf1+sf2==1,'SF concatenation additivity toy',c)
    req(-sf1==-2,'SF reversal sign',c)
    loop_sf=3
    req(loop_sf!=0,'nonzero loop obstructs naive endpoint path independence',c)

    # 15: distinguishability can parameterize a clock only on a monotone segment.
    p0=proj(0)
    mono=[overlap(p0,(math.pi/2)*j/20) for j in range(21)]
    req(all(mono[i]>=mono[i+1]-1e-12 for i in range(20)),'monotone projector distinguishability path',c)
    nonmono=[overlap(p0,t) for t in [0,math.pi/8,math.pi/4,math.pi/8,0]]
    req(not all(nonmono[i]>=nonmono[i+1]-1e-12 for i in range(len(nonmono)-1)),'nonmonotone path rejected as one-way clock',c)

    # 16-17: eigenvalue-null direction can have living projector/QGT motion.
    e0=eig2(H(0));e1=eig2(H(.37))
    req(max(abs(e0[i]-e1[i]) for i in range(2))<1e-12,'isospectral rotation',c)
    eps=1e-6;pa,pb=proj(0),proj(eps)
    dp=tuple(tuple((pb[i][j]-pa[i][j])/eps for j in range(2)) for i in range(2))
    dp_norm=sum(x*x for row in dp for x in row)
    req(dp_norm>1.9,'projector tangent nonzero on spectral-null direction',c)
    sigma_null=0.0
    req(sigma_null==0 and dp_norm>0,'spectral stress null while QGT direction lives',c)

    # 18-20: preserve failed scale routes as negative controls.
    ratios={}
    for r in [20,40,80]:
        ratio=r*r*math.exp(-r);ratios[str(r)]=ratio
        req(ratio<1e-5,f'exponential faster than r^-2 at r={r}',c)
    fixed_volume=8.0;L=fixed_volume**(1/3)
    req(L==2.0,'fixed hyperbolic volume gives fixed derived scale',c)
    req(abs((10**-3)/(10**-2)-0.1)<1e-15,'r^-3 differs from r^-2 scaling',c)

    # 21: commensurability/locking remains a legitimate finite-model question.
    ratio=3/2
    req(abs(2*ratio-3)<1e-12,'3:2 commensurability closes after finite counts',c)

    # 24-25: full torus winding and cancellation carry more than the old trichotomy.
    pairs=[(p,q) for p in range(-2,3) for q in range(-2,3)]
    req((2,1) in pairs and len(pairs)==25,'Z2 winding contains sectors beyond {-1,0,1}',c)
    events=[1,-1]
    req(sum(events)==0 and sum(abs(x) for x in events)==2,'zero total index with nontrivial paired events',c)

    # 26: oscillation requires a declared ordering/measure parameter.
    tau=[0,.25,.5,.75,1.0];signal=[math.sin(2*math.pi*t) for t in tau]
    req(abs(signal[0]-signal[-1])<1e-12,'periodicity defined relative to declared parameter',c)

    # 27: toy additive flow labels have category/groupoid algebra shape.
    a,b,d=2,-3,5
    req((a+b)+d==a+(b+d),'flow-label composition associative',c)
    req(a+0==a and a+(-a)==0,'identity and inverse labels',c)

    # 28: endpoint projector can erase ordered path history.
    pp,pm=proj(math.pi/2),proj(-math.pi/2)
    endpoint_dist=sum((pp[i][j]-pm[i][j])**2 for i in range(2) for j in range(2))
    req(endpoint_dist<1e-24,'opposite paths same projector endpoint',c)
    req((math.pi/2)!=(-math.pi/2),'ordered path record distinguishes same endpoint',c)

    # 30,32: echo/self-dual algebraic shape.
    J=lambda n:-n
    for n in [-4,-1,0,2,7]: req(J(J(n))==n,f'echo involution n={n}',c)
    req(J(3)==-3,'echo reverses flow',c)
    req(J(0)==0,'zero-flow toy fixed under echo',c)

    # 33: correct double-cover sign shape, explicitly not an emergence proof.
    Rgamma=-1
    req(Rgamma==-1 and Rgamma*Rgamma==1,'double-cover sign pattern shape',c)

    # 34: a two-dimensional complex space does not force determinant one.
    M=((2+0j,0j),(0j,1+0j));det=M[0][0]*M[1][1]-M[0][1]*M[1][0]
    req(det!=1,'GL2C example outside SL2C',c)

    # 35: a bare integer action has no intrinsic infinitesimal/half-step.
    integer_powers=set(range(-3,4))
    req(.5 not in integer_powers,'bare Z action lacks intrinsic half-step',c)

    # 36: phase redundancy leaves a rank-one projector invariant.
    v=(1/math.sqrt(2),1j/math.sqrt(2));P=outer(v);chi=.73
    vp=tuple(cmath.exp(1j*chi)*x for x in v);Pp=outer(vp)
    phase_err=max(abs(P[i][j]-Pp[i][j]) for i in range(2) for j in range(2))
    req(phase_err<1e-15,'projector invariant under U1 phase',c)

    # 37: full gluing of two one-torus-boundary objects consumes both boundaries.
    boundary_after_full_glue=1+1-2
    req(boundary_after_full_glue==0,'full torus gluing leaves closed boundary count in toy bookkeeping',c)
    req(boundary_after_full_glue!=1,'naive gluing not closed in one-torus-boundary object class',c)

    out={
      'status':'PASS','campaign':'QG-ARCHIVE-RECOVERY-11-37-01','source_sha256':SOURCE_SHA256,
      'checks':len(c),'checks_list':c,
      'key_results':{
        'isospectral_projector_tangent_norm2':dp_norm,
        'same_endpoint_distance2':endpoint_dist,
        'exp_over_rminus2':ratios,
        'u1_projector_error':phase_err,
        'boundary_components_after_full_glue_toy':boundary_after_full_glue,
        'paired_zero_total_flow':{'events':events,'net':sum(events)}},
      'scope':'Finite algebraic/structural controls and negative tests. Historical theorem contracts and physical interpretations are not proved by this script.'}
    (HERE/'qg_archive_recovery_11_37_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
