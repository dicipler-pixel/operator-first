#!/usr/bin/env python3
"""Infinite-chain Rice–Mele endpoint experiment; exact Fourier formula, arbitrary precision."""
import json, argparse
from pathlib import Path
from mpmath import mp

def family(params, max_L, dps):
    mp.dps=dps
    t1,t2,v=map(mp.mpf,params)
    A=t1*t1+t2*t2+v*v
    delta=mp.sqrt(A*A-4*t1*t1*t2*t2)
    scale=(A+delta)/2
    r=t1*t2/scale
    assert t1>0 and t2>0 and 0<r<1
    g={}
    for n in range(max_L//2+3):
        g[n]=(-r)**n*mp.rf(mp.mpf('.5'),n)/mp.factorial(n)*mp.hyp2f1(mp.mpf('.5'),n+mp.mpf('.5'),n+1,r*r)/mp.sqrt(scale)
    def f(n):return g[abs(n)]
    def block(L,shift=0):
        C=mp.matrix(L)
        for p in range(L):
            i,a=divmod(p+shift,2)
            for q in range(L):
                j,b=divmod(q+shift,2);d=i-j
                C[p,q]=(int(p==q)+(-1 if a==0 else 1)*v*f(d))/2 if a==b else (t1*f(d)+t2*f(d-1 if a==0 else d+1))/2
        return C
    return block,v/mp.sqrt(delta),r

def evaluate(C,g,n):
    p=mp.det(C);m=mp.det(mp.eye(C.rows)-C)
    assert p>0 and m>0
    a=(m-p)/(m+p);b=(-1)**n*a
    return {'L':C.rows,'n':n,'a':str(a),'b':str(b),'gamma':str(g),'R':str(b-g),'logp':str(mp.log(p)),'logm':str(mp.log(m))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-L',type=int,default=41);ap.add_argument('--dps',type=int,default=240);ap.add_argument('--out',default='probe.json');ap.add_argument('--cases',nargs='*',default=['.3,1,.4','.6,1,.4','.8,1,.4','.9,1,.4']);args=ap.parse_args()
    report={'method':'analytic hypergeometric Fourier coefficients; numerical evaluation, not interval certification','dps':args.dps,'cases':[]}
    for case in args.cases:
        params=case.split(',');block,g,r=family(params,args.max_L,args.dps);rows=[]
        for L in range(1,args.max_L+1,2):
            row=evaluate(block(L),g,(L-1)//2)
            if rows:row['ratio']=str(mp.mpf(row['R'])/mp.mpf(rows[-1]['R']))
            rows.append(row)
            print(case,L,'b',mp.nstr(mp.mpf(row['b']),12),'R',mp.nstr(mp.mpf(row['R']),8),'ratio',mp.nstr(mp.mpf(row.get('ratio','0')),10),flush=True)
        report['cases'].append({'params':params,'r':str(r),'gamma':str(g),'rows':rows})
        Path(args.out).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
