#!/usr/bin/env python3
"""Compile an exact normal-closure proof. This is not an AC move list."""
import hashlib,json,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(192*1024**2,192*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from official_checker import load_kernel,render
c,_,_,_=load_kernel()
def w(s):return tuple({'x':1,'X':-1,'y':2,'Y':-2}[a] for a in s)
def f(s):return c.free_reduce(s)
def st(a):return render([a])[0]
def lift(trace,left=(),right=()):return [f(left+a+right) for a in trace]
def reverse(trace):return trace[::-1]
def join(*traces):
    out=list(traces[0])
    for t in traces[1:]:
        assert out[-1]==t[0],(st(out[-1]),st(t[0]))
        out.extend(t[1:])
    return out
def once(a,left,right):
    for i in range(len(a)-len(left)+1):
        if a[i:i+len(left)]==left:return f(a[:i]+right+a[i+len(left):])
    raise ValueError('No match '+st(left)+' in '+st(a))
def reduce_r1(a):
    t=[a]
    while True:
        try:a=once(a,w('xxxxy'),w('yxxxxx'))
        except ValueError:return t
        t.append(a)
def cyclic(a):
    while len(a)>1 and a[0]==-a[-1]:a=a[1:-1]
    if not a:return ()
    return min(a[i:]+a[:i] for i in range(len(a)))
r0=w('YYYXyyx');r1=w('YXXXXyxxxxx')
classes={}
for ri,r in enumerate([r0,r1]):
    classes[cyclic(r)]=(ri,1);classes[cyclic(c.invert(r))]=(ri,-1)

A=reduce_r1(w('YY'+'x'*16+'yy'))
assert A[-1]==w('x'*25)
B=[w('YYY'+'x'*16+'yyy')]
B.append(once(B[-1],w('yyy'),w('Xyyx')))
B.append(once(B[-1],w('YYY'),w('XYYx')))
B=join(B,lift(A,w('X'),w('x')))
assert B[-1]==w('x'*25)
commutes=lift(join(B,reverse(A)),w('yy'),w('YY'))
assert commutes[0]==w('Y'+'x'*16+'y') and commutes[-1]==w('x'*16)
D=reduce_r1(w('Y'+'x'*16+'y'))
power4=lift(join(reverse(D),commutes),w('X'*16))
assert power4[0]==w('xxxx') and power4[-1]==()
power5=join([w('xxxxx'),w('Yxxxxy')],lift(power4,w('Y'),w('y')))
generator_x=join(lift(power5,w('XXXX')),[c.invert(a) for a in power4])
assert generator_x[0]==w('x') and generator_x[-1]==()
generator_X=[c.invert(a) for a in generator_x]
three_to_two=join([w('yyy'),w('Xyyx')],lift(generator_X,right=w('yyx')),lift(generator_x,left=w('yy')))
generator_y=lift(three_to_two,w('YY'))
assert generator_y[0]==w('y') and generator_y[-1]==()

def verify_trace(trace):
    result=[]
    for a,b in zip(trace,trace[1:]):
        delta=f(c.invert(a)+b)
        if not delta:
            result.append({'before':st(a),'after':st(b),'rule':'free_equality'});continue
        key=cyclic(delta)
        assert key in classes,(st(a),st(b),st(delta),st(key))
        ri,sign=classes[key]
        result.append({'before':st(a),'after':st(b),'original_relator':ri,'relator_sign':sign,
                       'difference':st(delta),'cyclic_reduced_difference':st(key)})
    return {'start':st(trace[0]),'end':st(trace[-1]),'steps':len(result),
            'peak_word_length':max(map(len,trace)),'trace':result}
out={'method':'finite original-relator normal-closure certificate',
     'row':'ac-07824','initial_relators':render([r0,r1]),
     'core_sha256':hashlib.sha256((ROOT/'vendor/verifier/core.py').read_bytes()).hexdigest(),
     'x_to_identity':verify_trace(generator_x),'y_to_identity':verify_trace(generator_y),
     'power4_to_identity':verify_trace(power4),'group_triviality_verified':True,
     'ac_triviality_verified':False,'is_scored_move_list':False}
Path(__file__).with_name('group_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:({a:v[a] for a in ['steps','peak_word_length']} if isinstance(v,dict) and 'steps'in v else v) for k,v in out.items()},indent=2))
