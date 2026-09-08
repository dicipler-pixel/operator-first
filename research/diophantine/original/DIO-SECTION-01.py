# SCRIPT: DIO-SECTION-01
# What sits on the rank-1 cover of  z^2 + y^2 z + x^3 + x + 1 = 0.
# Fibre: w^2 = y^4 - 4(x^3+x+1);  cover y(u) = (3/2)(1-u^2)/(1+u^2), branch +-3/2, c=-1.
# Step 1: why +-3/2 is special, checked not asserted.
# Step 2: hunt small rational points on fibres over many rational u and look for a section.
from fractions import Fraction as F
import itertools, math
def issq(fr):
    if fr < 0: return None
    n,d=fr.numerator,fr.denominator
    a,b=math.isqrt(n),math.isqrt(d)
    return F(a,b) if a*a==n and b*b==d else None
def fy(y,x): return y**4 - 4*(x**3+x+1)
print('STEP 1  what is at y = 3/2')
y0=F(3,2)
print('  y^4 =',y0**4,' and 4(x^3+x+1) at x=1/4 =',4*(F(1,4)**3+F(1,4)+1))
print('  so (x,y,w) = (1/4, 3/2, 0) is on the surface: the branch points are exactly the two y')
print('  where the fibre acquires a rational 2-torsion point.  Check the cubic factors there:')
# cubic in x: -4x^3 -4x + (y^4-4);  root at x=1/4?
c=y0**4-4
print('  -4x^3-4x+(y^4-4) at x=1/4 :', -4*F(1,4)**3-4*F(1,4)+c)
print()
print('STEP 2  small rational points on fibres of the cover')
def cover_y(u): return F(3,2)*(1-u*u)/(1+u*u)
found={}
for a in range(-6,7):
    for b in range(1,7):
        if math.gcd(abs(a),b)!=1: continue
        u=F(a,b); y=cover_y(u)
        hits=[]
        for m in range(-40,41):
            for n in range(1,25):
                if math.gcd(abs(m),n)!=1: continue
                x=F(m,n); s=issq(fy(y,x))
                if s is not None: hits.append((x,s))
        if hits: found[u]=(y,hits)
for u in sorted(found)[:14]:
    y,h=found[u]
    print(f'  u={str(u):>6s}  y={str(y):>10s}  points x = '+', '.join(str(x) for x,_ in h[:6]))
print()
print('STEP 3  is there a section x(u)?  look at the x that appear for every u')
common=None
for u,(y,h) in found.items():
    s={x for x,_ in h}
    common = s if common is None else (common & s)
print('  x values present on EVERY sampled fibre:', sorted(common) if common else 'none')
