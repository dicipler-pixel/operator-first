# SCRIPT: SNELL-PEEL-01-GEOMETRY  (Slater-rule orbital geometry on the (Z,q) onion; no ionization energies used)
import numpy as np
L={'s':0,'p':1,'d':2,'f':3}; CAP={'s':2,'p':6,'d':10,'f':14}
MADELUNG=['1s','2s','2p','3s','3p','4s','3d','4p','5s','4d','5p','6s','4f','5d','6p','7s','5f','6d','7p']
COULOMB=sorted(MADELUNG,key=lambda o:(int(o[0]),L[o[1]]))
NSTAR={1:1.0,2:2.0,3:3.0,4:3.7,5:4.0,6:4.2,7:4.2}
def config(N,rule):
    occ={}; left=N
    for o in (MADELUNG if rule=='M' else COULOMB):
        if left<=0: break
        k=min(CAP[o[1]],left); occ[o]=k; left-=k
    return occ
# Slater groups in order
GROUPS=[('1s',),('2s','2p'),('3s','3p'),('3d',),('4s','4p'),('4d',),('4f',),('5s','5p'),('5d',),('5f',),('6s','6p'),('6d',),('7s','7p')]
GIDX={o:i for i,g in enumerate(GROUPS) for o in g}
def zeff(Z,occ,orb):
    g=GIDX[orb]; n=int(orb[0]); S=0.0
    for o,k in occ.items():
        if k==0: continue
        go=GIDX[o]; m=k-(1 if o==orb and k>0 else 0) if o==orb else k
        if o==orb: m=k-1
        if go==g: S+=m*(0.30 if orb=='1s' else 0.35)
        elif go>g: continue
        else:
            if orb[1] in 'sp':
                no=int(o[0]); S+=m*(0.85 if no==n-1 else 1.00)
            else: S+=m*1.00
    # same-group partner (e.g. 2p when orb is 2s) handled above since same group index
    return Z-S
def period(Z):
    for p,e in ((1,2),(2,10),(3,18),(4,36),(5,54),(6,86),(7,118)):
        if Z<=e: return p
def active(Z):
    n=period(Z)
    if n==1: return ['1s']
    a=[f'{n}s',f'{n}p']
    if n>=4: a=[f'{n-1}d']+a
    return a
MULT={'s':1,'p':3,'d':5}
def zetas(Z,q,rule,act):
    occ=config(Z-q,rule)
    return {o:zeff(Z,occ,o)/NSTAR[int(o[0])] for o in act}
def d2(za,zb,act):
    s=0.0
    for o in act:
        ns=NSTAR[int(o[0])]; a,b=za[o],zb[o]
        if a<=0 or b<=0: return np.nan
        c=(2*np.sqrt(a*b)/(a+b))**(2*ns+1); s+=MULT[o[1]]*(1-c*c)
    return s
def gqq(Z,q,rule):
    act=active(Z)
    if Z-q-1<0: return np.nan
    return d2(zetas(Z,q,rule,act),zetas(Z,q+1,rule,act),act)
def gZZ(Z,q,rule):
    act=active(Z)
    if period(Z+1)!=period(Z): return np.nan
    return d2(zetas(Z,q,rule,act),zetas(Z+1,q,rule,act),act)
