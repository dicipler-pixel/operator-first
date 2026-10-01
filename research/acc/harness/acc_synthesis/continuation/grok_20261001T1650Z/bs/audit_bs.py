#!/usr/bin/env python3
"""Small exact identity audit; not a first-solve search."""
import hashlib, itertools, json, resource, sys, time
from collections import deque
from pathlib import Path

resource.setrlimit(resource.RLIMIT_AS, (192*1024**2, 192*1024**2))
resource.setrlimit(resource.RLIMIT_CPU, (20,20))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from official_checker import load_kernel, render
core, specs, _, _ = load_kernel()
mp = ROOT/'integration/repo/official_manifest.json'
manifest = json.loads(mp.read_text())
ids = ['ac-07824','ac-07659','ac-02412','ac-02917','ac-02901']
rows = {c['challenge_id']:c for c in manifest['challenges'] if c['challenge_id'] in ids}
states = {k:tuple(tuple(w) for w in c['initial_relators']) for k,c in rows.items()}
def im(w,s): return tuple(s[abs(a)-1]*(1 if a>0 else -1) for a in w)
def cyclic_match(a,b):
    ans=[]
    for inv in [False,True]:
        w=core.invert(a) if inv else a
        for k in range(len(w)):
            if w[k:]+w[:k]==b:
                ans.append({'invert':inv,'rotate_left':k,'prefix':render([w[:k]])[0]})
    return ans
equivalences=[]
base=states['ac-07824']
for rid,t in states.items():
    for xy in [(1,2),(2,1)]:
        for signs in itertools.product([1,-1],repeat=2):
            s=tuple(a*b for a,b in zip(xy,signs))
            a=tuple(im(w,s) for w in base)
            for swap in [False,True]:
                v=a[::-1] if swap else a
                matches=[cyclic_match(v[i],t[i]) for i in range(2)]
                if all(matches):
                    equivalences.append({'to':rid,'generator_images':render([(s[0],),(s[1],)]),'swap_relators':swap,'matches':matches})

# A tiny endpoint conversion only, capped explicitly and replayed by the core.
start=((2,),(1,)); goal=((1,),(2,)); q=deque([(start,[])])
seen={start}; endpoint=None; deadline=time.monotonic()+5
while q and time.monotonic()<deadline and len(seen)<50000:
    st,p=q.popleft()
    if st==goal:
        endpoint=p; break
    if len(p)==6: continue
    for m in range(14):
        nxt=core.apply_move(st,m)
        if sum(map(len,nxt))<=6 and nxt not in seen:
            seen.add(nxt); q.append((nxt,p+[m]))
if endpoint is not None:
    st=start
    for m in endpoint: st=core.apply_move(st,m)
    assert st==goal

out={'manifest_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),
     'checker_core_sha256':hashlib.sha256((ROOT/'vendor/verifier/core.py').read_bytes()).hexdigest(),
     'instances':{k:{'start':render(v),'instance_hash':rows[k]['instance_hash'],
          'abelianization':[[sum(a==g for a in w)-sum(a==-g for a in w) for g in (1,2)] for w in v]} for k,v in states.items()},
     'from_ac07824_signed_cyclic_equivalences':equivalences,
     'endpoint_YX_to_XY':{'moves':endpoint,'visited':len(seen),'depth_limit':6,'total_length_cap':6,'max_states':50000,'time_limit_s':5},
     'first_solve_search_performed':False,'scored_candidate':None}

def endpoint_fix(st):
    todo=deque([(st,[])]); visited={st}; deadline=time.monotonic()+2
    while todo and time.monotonic()<deadline and len(visited)<50000:
        s,p=todo.popleft()
        if s==goal: return p
        if len(p)==6: continue
        for m in range(14):
            n=core.apply_move(s,m)
            if sum(map(len,n))<=6 and n not in visited:
                visited.add(n); todo.append((n,p+[m]))
    raise RuntimeError('Endpoint diagnostic bound reached')

transfers=[]
for eq in equivalences:
    s=tuple({'x':1,'X':-1,'y':2,'Y':-2}[c] for c in eq['generator_images'])
    assert not eq['swap_relators']
    mapped=tuple(im(w,s) for w in base)
    forward=[]
    for i, options in enumerate(eq['matches']):
        choice=options[0]; w=mapped[i]
        if choice['invert']:
            forward.append(i); w=core.invert(w)
        k=choice['rotate_left']; offset=6+4*i
        if k<=len(w)-k:
            conjugators=tuple(-a for a in w[:k])
        else:
            conjugators=tuple(reversed(w[k:]))
        forward += [offset+core.GENS.index(g) for g in conjugators]
    st=mapped
    for m in forward: st=core.apply_move(st,m)
    assert st==states[eq['to']]
    prefix=[core.INVERSE_MOVE[m] for m in reversed(forward)]
    st=states[eq['to']]
    for m in prefix: st=core.apply_move(st,m)
    assert st==mapped
    move_map=list(range(6))+[6+core.GENS.index(im((g,),s)[0]) for g in core.GENS]+[10+core.GENS.index(im((g,),s)[0]) for g in core.GENS]
    for m in range(14):
        assert core.apply_move(mapped,move_map[m])==tuple(im(w,s) for w in core.apply_move(base,m))
    suffix=endpoint_fix(((s[0],),(s[1],)))
    st=((s[0],),(s[1],))
    for m in suffix: st=core.apply_move(st,m)
    assert st==goal
    transfers.append({'from_route_row':'ac-07824','to_route_row':eq['to'],
        'prefix_from_target_start_to_mapped_source':prefix,
        'source_move_to_target_move':move_map,'suffix_to_exact_xy':suffix,
        'total_additional_moves':len(prefix)+len(suffix),
        'exact_join_state':render(mapped),'replay_identity_passed':True})
out['transfers']=transfers
out['scaled_relator_obstruction']={
    'example':'XyyyyxYYYYYY','exponent_vector':[0,-2],
    'all_start_determinants_abs':1,
    'verdict':'Cannot occur as an entire relator in this AC orbit: determinant would be divisible by two.',
    'scope':'Does not forbid the scaled identity as a subword rewrite with a retained paid derivation.'}
path=Path(__file__).with_name('identity_audit.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
