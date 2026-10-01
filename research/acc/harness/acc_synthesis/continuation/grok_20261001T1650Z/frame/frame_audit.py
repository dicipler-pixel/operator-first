"""Deterministic replay only; no solver search or checkpoint mutation."""
import hashlib, json, resource, signal, sys, time
from pathlib import Path
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
resource.setrlimit(resource.RLIMIT_AS, (192*1024**2, 192*1024**2))
signal.alarm(10)
started = time.monotonic()
sys.path.insert(0, str(ROOT))
from official_checker import load_kernel, render
core, specs, pins, selected = load_kernel()
manifest = ROOT/'integration/repo/official_manifest.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == pins['source_manifest_sha256']
man = json.loads(manifest.read_text())
ch = next(c for c in man['challenges'] if c['challenge_id'] == 'ac-04042')
doc = json.loads((ROOT/'continuation/proof_audit_20261001T0540Z/input.json').read_text())
route = next(r['ac'] for r in doc['routes'] if r['id'] == 'ac-04042')
state = tuple(tuple(r) for r in ch['initial_relators'])
trace = [{'index':0,'state':render(state)}]
before9 = []
for i,m in enumerate(route):
    if m == 9: before9.append({'before_move_index_zero_based':i,'state':render(state),'next_moves':route[i:i+6]})
    state = core.apply_move(state,m)
    trace.append({'index':i+1,'move':m,'state':render(state)})
def apply(s, moves):
    for m in moves: s=core.apply_move(s,m)
    return s
rho=(-1,2,1,1,-2)
rho2=(2,1,1,-2,-1)
cases=[]
for a in [1,2,4,8,16]:
    for b in [2,3,4]:
        for c in [2,3,4]:
            old=((1,)*(a-1)+(2,)*b+(-1,)+(-2,)*c+(1,),rho)
            pass_moves=[m for _ in range(a-1) for m in (2,7)]+[2]
            end=apply(old,pass_moves)
            full=apply(end,[0,9,6,10])
            cheap=apply(end,[0,10])
            assert full!=cheap
            A=((1,)*a+(2,)*b+(-1,)+(-2,)*c,rho)
            invA=(core.invert(A[0]),rho2)
            assert apply(A,[0,10])==invA
            assert apply(invA,[11,0])==A
            new_A_pass=[m for _ in range(a) for m in (7,2)]+[9,0,10]
            A_target=((-1,)*(2*a)+(2,)*(c-1)+(1,)+(-2,)*(b-1),rho2)
            assert apply(A,new_A_pass)==A_target
            cases.append({'a':a,'b':b,'c':c,'old_boundary':render(end),
                'old_next':render(full),'cheap_next':render(cheap),
                'old_cost':len(pass_moves)+4,'monomial_frame_cost':len(new_A_pass)})
result={'kind':'deterministic_frame_audit','checker_commit':pins['source_commit'],
    'manifest_sha256':pins['source_manifest_sha256'],
    'source_route':{'row':'ac-04042','length':len(route),'moves':route,
        'receipt':core.verify(ch,route,ch['move_spec_version'],man['limits']),
        'before_move9':before9,'trace':trace},
    'finite_cases':cases,'frame_identity_cases':len(cases),
    'improved_route':None,'search_performed':False,
    'elapsed_seconds':time.monotonic()-started,
    'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
    'bounds':{'seconds':10,'memory_mib':192}}
load_kernel()
(OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('source_route','finite_cases')}))
print(json.dumps({'before_move9':before9,'route_receipt':result['source_route']['receipt']}))
print(json.dumps(trace))
