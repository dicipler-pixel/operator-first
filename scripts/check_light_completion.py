from pathlib import Path
import sympy as s, json
G,H,c,e=s.symbols('g h c eta',positive=True)
ratio=1/((G+e)*(1+c*G))
derivative=s.factor(s.diff(ratio,G))
assert s.simplify(derivative+(1+c*e+2*c*G)/((G+e)**2*(1+c*G)**2))==0
# Exact same-metric, different-gap control: a=gap, g=1, alpha(0)=2 gap.
rows=[{'gap':d,'amplitude':d,'g':1,'static_alpha':2*d} for d in [1,2]]
# Lossless two-gap scalar response has exactly one tune-out between distinct active poles.
a,b,A,B=s.symbols('a b A B',positive=True);y=s.symbols('y')
f=A/(a-y)+B/(b-y);zero=(A*b+B*a)/(A+B)
assert s.simplify(f.subs(y,zero))==0
assert s.simplify(zero-a-A*(b-a)/(A+B))==0
assert s.simplify(b-zero-B*(b-a)/(A+B))==0
# At more active poles, derivative is positive on each open pole interval.
assert s.simplify(s.diff(f,y)-A/(a-y)**2-B/(b-y)**2)==0
out={'same_metric_control':rows,'rigidity_ratio_derivative':str(derivative),'two_pole_zero':str(zero),'two_pole_derivative':str(s.diff(f,y)),'status':'PASS','scope':'Exact algebra; rigidity control assumes squared transport singular value equals field metric.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
