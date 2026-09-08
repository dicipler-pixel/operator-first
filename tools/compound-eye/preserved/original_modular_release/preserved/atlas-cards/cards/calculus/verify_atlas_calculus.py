"""Reproducible checks of the finite fragment and the supplied cards.

Run: python verify_atlas_calculus.py
Writes evidence/verification.json next to this script. These checks are not a
Lean formalization or a proof of uniform stability for a family of complexes.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
import importlib.util
import json
import platform
import random
import numpy as np
import sympy as sp
from atlas_calculus import Diagram

HERE = Path(__file__).resolve().parent
checks = []

def record(name, detail):
    checks.append({'name':name, 'passed':True, 'detail':detail})

chain = Diagram(('left','inside','right'), sp.Matrix([[4,-1,0],[-1,5,-2],[0,-2,3]]))
reduced = chain.eliminate(('inside',))
assert reduced.matrix == sp.Matrix([[sp.Rational(19,5),-sp.Rational(2,5)],[-sp.Rational(2,5),sp.Rational(11,5)]])
assert reduced.weight == 5 and chain.read() == reduced.read() == 41
record('chain_exact_reduction', 'S=[[19/5,-2/5],[-2/5,11/5]], weight=5, determinant=41.')

u,v,z = sp.symbols('u v z', real=True)
load = Diagram(('left','right'),sp.Matrix([[u,z],[z,v]]))
assert sp.expand(chain.attach(load).read()-reduced.attach(load).read()) == 0
record('arbitrary_boundary_load', 'Symbolic identity for every symmetric two-port load; physical domain restricted to admissible nonsingular/positive matrices.')

lam = sp.Symbol('lambda', nonnegative=True)
attached = chain.attach(Diagram(('right',),sp.Matrix([[lam]])))
assert attached.read() == 19*lam+41
record('demonstrator_load_formula', 'Both calculations give 41+19*lambda for every lambda>=0.')

net = Diagram(('left','i','j','right'),sp.Matrix([[7,-1,1,0],[-1,6,-2,1],[1,-2,5,-1],[0,1,-1,4]]))
assert all(net.matrix[:i,:i].det()>0 for i in range(1,5))
a = net.eliminate(('i',)).eliminate(('j',))
b = net.eliminate(('j',)).eliminate(('i',))
c = net.eliminate(('i','j'))
assert a == b == c and net.read() == c.read()
record('elimination_order', 'Two single-port orders and one block elimination agree, including the retained scalar.')

extension = Diagram(('right','external'),sp.Matrix([[3,-1],[-1,2]]))
assert chain.attach(extension).read() == reduced.attach(extension).read()
assert chain.attach(extension).eliminate(('inside','external')) == reduced.attach(extension).eliminate(('external',))
record('continuation_with_new_internal_port', 'An attached two-port system gives the same final response and scalar before or after replacement.')

try:
    reduced.attach(Diagram(('inside',),sp.Matrix([[1]])))
except ValueError:
    record('hidden_port_attachment_rejected','A continuation cannot secretly reconnect to a coordinate removed by the rewrite.')
else:
    raise AssertionError('An eliminated coordinate was reattached')

x = Diagram(('i','b'),sp.Matrix([[2,1],[1,2]]))
y = Diagram(('i','b'),sp.Matrix([[8,2],[2,2]]))
rx,ry = x.eliminate(('i',)),y.eliminate(('i',))
assert rx.matrix == ry.matrix == sp.Matrix([[sp.Rational(3,2)]])
assert (rx.weight,ry.weight,x.read(),y.read()) == (2,8,3,12)
record('false_control_response_only', 'Rejected: equal Schur responses imply equal determinant readouts. Explicit readouts are 3 and 12.')

try:
    Diagram(('i','b'),sp.Matrix([[0,1],[1,2]])).eliminate(('i',))
except ValueError:
    record('singular_pivot_rejected','A zero pivot is not silently simplified.')
else:
    raise AssertionError('Singular pivot accepted')

n,h,delta,base = sp.symbols('n h delta base', positive=True)
assert sp.simplify(((base+delta)/n-base/n)/(h/n)-delta/h)==0
record('B94_fixed_block_padding', 'Exact cancellation gives response/Hamming = delta/h, with fixed h and delta. No knot experiments are claimed.')

for L in range(2,25):
    P=np.roll(np.eye(L),1,axis=0)
    G=(P-np.eye(L)).T@(P-np.eye(L))/2
    observed=np.sort(np.linalg.eigvalsh(G/2))
    target=np.sort(np.sin(np.pi*np.arange(L)/L)**2)
    assert np.max(np.abs(observed-target))<1e-12
record('B95_cycle_spectrum','Independent numerical matrix spectra checked for each cycle length 2 through 24; general Fourier proof is in the note.')

P3=sp.Matrix([[0,0,1],[1,0,0],[0,1,0]])
G3=sp.simplify((P3-sp.eye(3)).T*(P3-sp.eye(3))/2)
assert (G3/2).eigenvals()=={sp.S.Zero:1,sp.Rational(3,4):2}
assert all(1-G3[i,j]**2==sp.Rational(3,4) for i,j in combinations(range(3),2))
assert sum(mult for eig,mult in (G3/2).eigenvals().items() if eig>=sp.Rational(7,10))==2
record('false_control_spectral_equals_packing','Rejected at epsilon=7/10: a three-cycle has spectral count 2 but three pairwise separated displacement rays.')

# Load definitions from the original submission; its main experiment suite does
# not run on import. Reuse the author's gauge implementation, with exact counts.
source = HERE.parent/'sources/2026-09-06/SOFIC-NEW-ROUTES-01.py'
spec=importlib.util.spec_from_file_location('submitted_sofic',source)
sofic=importlib.util.module_from_spec(spec)
spec.loader.exec_module(sofic)
rng=random.Random(20260906)
trial_count=0
for nv in (4,5,6,8,10):
    edges=list(combinations(range(nv),2))
    faces=list(combinations(range(nv),3))
    degree=5
    ident=tuple(range(degree))
    for trial in range(8):
        alpha={}
        for edge in edges:
            perm=list(ident); rng.shuffle(perm); perm=tuple(perm)
            alpha[edge]=perm; alpha[edge[::-1]]=sofic.inverse(perm)
        curvature_count=sum(sum(a!=b for a,b in zip(sofic.triangle_holonomy(alpha,*f),ident)) for f in faces)
        rooted_count=0
        for root in range(nv):
            beta,tr=sofic.rooted_gauge(nv,edges,alpha,root,degree)
            assert all(tr[(root,j)]==ident for j in range(nv) if j!=root)
            rooted_count+=sum(sum(a!=b for a,b in zip(tr[e],ident)) for e in edges)
        E=Fraction(rooted_count,nv*len(edges)*degree)
        curvature=Fraction(curvature_count,len(faces)*degree)
        assert E==Fraction(nv-2,nv)*curvature
        trial_count+=1
record('sofic_complete_complex_identity', f'{trial_count} deterministic cochains, nv=4,5,6,8,10; exact rational equality E=((nv-2)/nv)*curvature using the submitted gauge implementation.')

report={'python':platform.python_version(),'sympy':sp.__version__,'numpy':np.__version__, 'checks':checks,'all_passed':True,'new_lean_formalization':False,'not_run':['Original B94 knot experiments','Full original sofic random-complex stress suite','Original script quadratic-time large-n permutation-sign sweep'],'open':['Uniform bounded-overlap fillings for a specified family','Physical phase/count return maps and units','Extension from this finite determinant calculus to physical Fourier/Hankel limits']}
(HERE/'evidence').mkdir(exist_ok=True)
(HERE/'evidence/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
