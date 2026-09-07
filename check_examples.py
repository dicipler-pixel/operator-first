#!/usr/bin/env python3
"""Exact-rational finite examples. Standard library only; not a substitute for Lean."""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import json

@dataclass(frozen=True)
class QI:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))
    @staticmethod
    def coerce(x): return x if isinstance(x,QI) else QI(x)
    def __add__(self,x):
        x=self.coerce(x); return QI(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self): return QI(-self.re,-self.im)
    def __sub__(self,x): return self+-self.coerce(x)
    def __rsub__(self,x): return self.coerce(x)+-self
    def __mul__(self,x):
        x=self.coerce(x); return QI(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.coerce(x); d=x.re*x.re+x.im*x.im
        return self*QI(x.re/d,-x.im/d)

def matmul(a,b):
    return [[sum((a[i][j]*b[j][k] for j in range(len(b))),QI())
             for k in range(len(b[0]))] for i in range(len(a))]
def matsub(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def tr(a): return sum((a[i][i] for i in range(len(a))),QI())
def chart(z,w):
    z,w=QI.coerce(z),QI.coerce(w); d=1+z*w
    return [[QI(1)/d,w/d],[z/d,z*w/d]]
def moving(y): return chart(QI(0,y),QI(0,y*y))
checks={}
def check(name,conditions,data=None):
    values=list(conditions)
    assert all(values), name
    checks[name]={'status':'PASS','instances':len(values),'data':data}

charts=[chart(QI(F(a,7),F(b,11)),QI(F(c,13),F(d,17)))
        for a,b,c,d in [(1,2,3,4),(-2,1,5,-3),(0,1,0,-1),(3,0,-2,0),(0,0,0,0)]]
check('complex_chart_idempotency',(matmul(p,p)==p for p in charts))
check('complex_chart_trace',(tr(p)==QI(1) for p in charts))
check('exact_overlap_identity',
      (tr(matmul(p,q)).re==1-tr(matmul(matsub(q,p),matsub(q,p))).re/2
       for p in charts for q in charts))

rows=[]; identities=[]; remainders=[]; signs=[]
for v in [F(-1,5),F(-1,10),F(0),F(1,100),F(1,10),F(1,5)]:
    for t in [F(1,1000),F(-1,1000),F(1,10000),F(-1,10000)]:
        excess=tr(matmul(moving(v),moving(v+t))).re-1
        exact=t*t*(2*v+t)/((1-v**3)*(1-(v+t)**3))
        g=-2*v/(1-v**3)**2
        remainder=t**3*(1+5*v**3+6*v*v*t+2*v*t*t)/((1-v**3)**2*(1-(v+t)**3))
        identities.append(excess==exact)
        remainders.append(excess+g*t*t==remainder)
        if v>0: signs.append(excess>0)
        if v<0: signs.append(excess<0)
        rows.append({'v':str(v),'t':str(t),'g':str(g),'excess':str(excess),
                     'remainder_over_t2':str(remainder/(t*t))})
check('moving_chart_excess_formula',identities)
check('moving_chart_remainder_formula',remainders,rows)
check('moving_chart_nonzero_coefficient_signs',signs)
check('wall_cubic_sign_and_formula',
      (tr(matmul(moving(0),moving(t))).re-1==t**3/(1-t**3)
       for t in [F(1,10),F(-1,10),F(1,100),F(-1,100)]))

quartic=[]
for t in [F(1,10),F(-1,10),F(1,100),F(-1,100)]:
    p0=chart(0,0)
    plus=tr(matmul(p0,chart(t,-t**3))).re-1
    minus=tr(matmul(p0,chart(t,t**3))).re-1
    quartic += [plus==t**4/(1-t**4),plus>0,minus==-t**4/(1+t**4),minus<0]
check('null_coefficient_both_quartic_signs',quartic)

# z=t, w=-t*(1+sqrt(abs(t))) is differentiable at zero but not C² there.
# Choose t=+/-m^-4 to keep all arithmetic rational, including sqrt(abs(t)).
rough=[]
for m in [4,8,16,32,64]:
    for sign in [-1,1]:
        t=F(sign,m**4); root=F(1,m**2)
        p=chart(t,-t*(1+root)); excess=tr(matmul(chart(0,0),p)).re-1
        ratio=excess/(t*t)
        rough.append({'m':m,'sign':sign,'ratio':str(ratio),'error':str(ratio-1)})
check('differentiable_non_C2_example',
      (F(row['error'])>0 and F(row['error'])<F(2,row['m']**2) for row in rough),rough)

out=Path(__file__).resolve().parent/'evidence';out.mkdir(exist_ok=True)
report={'status':'PASS','arithmetic':'exact rational complex pairs; Python standard library',
        'groups':len(checks),'instances':sum(x['instances'] for x in checks.values()),'checks':checks}
(out/'examples.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
