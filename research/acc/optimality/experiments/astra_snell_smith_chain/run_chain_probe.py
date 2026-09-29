"""Private, reproducible Snell/Smith/ordered-word diagnostic; never submits.

Run from repository root with Python 3 + NumPy. Exact AC semantics come from
the separately pinned SAIR checkout. See PROTOCOL.md before interpreting results.
"""
import cmath
from collections import Counter
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import slater_geom as slater

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
PIN = 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
assert subprocess.check_output(['git', '-C', 'SAIR', 'rev-parse', 'HEAD'], text=True).strip() == PIN
sys.path.insert(0, str(ROOT/'SAIR/competition/tools'))
from verifier import core

I = (1, 0, 0, 1)
X = (1, 2, 0, 1)
Y = (1, 0, 2, 1)
TARGET = ((1,), (2,))
SCORES = ('length', 'abelian', 'chain', 'H', 'length_chain', 'H_chain')


def mul(p, q):
    a, b, c, d = p
    e, f, g, h = q
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


def inv(p):
    a, b, c, d = p
    assert a*d-b*c == 1
    return (d, -b, -c, a)


GEN = {1: X, -1: inv(X), 2: Y, -2: inv(Y)}


@lru_cache(maxsize=65536)
def word_matrix(word):
    m = I
    for letter in word:
        m = mul(m, GEN[letter])
    return m


def pair_matrix(state):
    return tuple(word_matrix(w) for w in state)


def word_disk_pair(state):
    keys = []
    for matrix, target in zip(pair_matrix(state), (X, Y)):
        a, b, c, d = mul(inv(target), matrix)
        keys.append((a*c+b*d, c*c+d*d))
    return tuple(keys)


def matrix_move(pair, move):
    a, b = pair
    if move == 0:
        return inv(a), b
    if move == 1:
        return a, inv(b)
    if move == 2:
        return mul(a, b), b
    if move == 3:
        return mul(a, inv(b)), b
    if move == 4:
        return a, mul(b, a)
    if move == 5:
        return a, mul(b, inv(a))
    if move < 10:
        g = GEN[core.GENS[move-6]]
        return mul(mul(g, a), inv(g)), b
    g = GEN[core.GENS[move-10]]
    return a, mul(mul(g, b), inv(g))


def ledger(state):
    return tuple(sum((1 if a == g else -1 if a == -g else 0) for a in w)
                 for w in state for g in (1, 2))


def chart_key(state):
    a, b, c, d = ledger(state)
    assert abs(a*d-b*c) == 1
    # Upper-half-plane point is (a*c+b*d + i)/(c*c+d*d), including
    # the anti-holomorphic extension when determinant is negative.
    return a*c+b*d, c*c+d*d


def hyp_from_identity(m):
    n = sum(x*x for x in m)
    return math.acosh(n/2) if n.bit_length() < 1000 else math.log(n)


def hpriority(state):
    length = sum(map(len, state))
    K = MK = 0
    cnt = [0, 0]
    blocks = [0, 0]
    for w in state:
        if not w:
            continue
        k = 0
        for i, a in enumerate(w):
            g = abs(a)-1
            cnt[g] += 1
            if abs(w[i-1]) != abs(a):
                k += 1
                blocks[g] += 1
        if k == 0:
            blocks[abs(w[0])-1] += 1
        K += k//2
        MK = max(MK, k//2)
    thin = 0 if cnt[0] <= cnt[1] else 1
    S = cnt[thin]/blocks[thin] if blocks[thin] else 0
    imbalance = abs(cnt[0]-cnt[1])/length
    return int(16*(length+2.53*K+6.418*MK+8.458*S+3.292*imbalance))


def features(state):
    length = sum(map(len, state))
    # Round only the displayed/scored distance to avoid asymmetric float ties.
    chain = round(sum(hyp_from_identity(mul(inv(t), r))
                      for r, t in zip(pair_matrix(state), (X, Y))), 12)
    abelian = sum(a*a for a in ledger(state))
    h = hpriority(state)
    return dict(length=length, abelian=abelian, chain=chain, H=h,
                length_chain=(length, chain), H_chain=(h, chain))


def slater_check():
    errors = []
    orbital_links = 0
    for rule in ('M', 'C'):
        for Z in range(1, 87):
            act = slater.active(Z)
            for q in range(Z):
                za = slater.zetas(Z, q, rule, act)
                zb = slater.zetas(Z, q+1, rule, act)
                if any(za[o] <= 0 or zb[o] <= 0 for o in act):
                    continue
                reformulated = 0.0
                for o in act:
                    a, b = za[o], zb[o]
                    gamma = (b-a)/(b+a)
                    exponent = 2*slater.NSTAR[int(o[0])]+1
                    reformulated += slater.MULT[o[1]]*(1-(1-gamma*gamma)**exponent)
                    orbital_links += 1
                errors.append(abs(float(slater.d2(za, zb, act))-reformulated))
    assert max(errors) < 1e-11
    a, b, c = 1.0, 4.0, 2.0
    g1, g2 = (b-a)/(b+a), (c-b)/(c+b)
    composed = (g1+g2)/(1+g1*g2)
    assert abs(composed-(c-a)/(c+a)) < 1e-15
    return dict(state_links=len(errors), orbital_links=orbital_links,
                max_absolute_error=max(errors),
                scalar_demo=dict(values=[a,b,c], gammas=[g1,g2],
                                 composed=composed, direct=(c-a)/(c+a)))


def optical_stack(layers, angle_deg):
    indices = [1.0]+[n for n, d in layers]+[1.5]
    transverse = math.sin(math.radians(angle_deg))
    adm = [math.sqrt(n*n-transverse*transverse) for n in indices]
    phases = [2*math.pi*adm[j+1]*d/550 for j, (n, d) in enumerate(layers)]
    M = np.eye(2, dtype=complex)
    for j, delta in enumerate(phases):
        q = adm[j+1]
        M = M @ np.array([[math.cos(delta), -1j*math.sin(delta)/q],
                          [-1j*q*math.sin(delta), math.cos(delta)]])
    yin = (M[1,0]+M[1,1]*adm[-1])/(M[0,0]+M[0,1]*adm[-1])
    r_matrix = (adm[0]-yin)/(adm[0]+yin)
    r = (adm[-2]-adm[-1])/(adm[-2]+adm[-1])
    for j in reversed(range(len(layers))):
        r0 = (adm[j]-adm[j+1])/(adm[j]+adm[j+1])
        phase = cmath.exp(2j*phases[j])
        r = (r0+r*phase)/(1+r0*r*phase)
    assert abs(r-r_matrix) < 1e-12
    return dict(reflectance=abs(r)**2, reflection=[r.real,r.imag],
                matrix_recursion_error=abs(r-r_matrix),
                snell_transverse=transverse)


def exact_ball():
    start = time.monotonic()
    distance = {TARGET: 0}
    front = [TARGET]
    sizes = [1]
    for d in range(1, 7):
        nex = []
        for s in front:
            for move in range(14):
                q = core.apply_move(s, move)
                if q not in distance:
                    distance[q] = d
                    nex.append(q)
        front = nex
        sizes.append(len(front))
        print('exact ball depth', d, 'layer', len(front), flush=True)
    cases = [s for s, d in distance.items() if d == 5]
    stats = {name: 0.0 for name in SCORES}
    center = 0
    matrices = set()
    disks = set()
    charts = set()
    no_length_descent = 0
    for s in cases:
        matrices.add(pair_matrix(s))
        disks.add(word_disk_pair(s))
        charts.add(chart_key(s))
        center += chart_key(s) == (0, 1)
        children = [core.apply_move(s, m) for m in range(14)]
        f = [features(c) for c in children]
        good = [distance[c] == 4 for c in children]
        no_length_descent += not any(g and sum(map(len,c)) < sum(map(len,s))
                                    for g,c in zip(good,children))
        for name in SCORES:
            best = min(x[name] for x in f)
            chosen = [i for i,x in enumerate(f) if x[name] == best]
            stats[name] += sum(good[i] for i in chosen)/len(chosen)
    assert len(matrices) == len(cases)
    assert len(disks) == len(cases)
    return dict(layer_sizes=sizes, total_states=len(distance), test_depth=5,
                test_states=len(cases), matrix_pair_collisions=len(cases)-len(matrices),
                exact_word_disk_pair_collisions=len(cases)-len(disks),
                distinct_abelian_chart_points=len(charts), false_center_states=center,
                states_without_length_decreasing_optimal_move=no_length_descent,
                optimal_descent_probability={k:v/len(cases) for k,v in stats.items()},
                wall_s=time.monotonic()-start)


def route_probe(input_name='routes.json', output_prefix=''):
    manifest = json.loads((ROOT/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
    challenges = {c['challenge_id']:c for c in manifest['challenges']}
    routes = json.loads((HERE/input_name).read_text())
    records = []
    states = set()
    hidden = 0
    transitions = 0
    changed = 0
    move_checks = 0
    center = []
    certificates = []
    for row in routes:
        check = core.verify(challenges[row['id']],row['ac'],'ac-r2-v1',manifest['limits'])
        assert check['ok'], (row['id'],check)
        certificates.append(dict(id=row['id'],check=check))
        s = tuple(map(tuple,challenges[row['id']]['initial_relators']))
        for i, move in enumerate(row['ac']):
            states.add(s)
            if chart_key(s) == (0,1) and s != TARGET:
                center.append(dict(id=row['id'],step=i,left=len(row['ac'])-i,
                                   length=sum(map(len,s)),state=s))
            children = [core.apply_move(s,m) for m in range(14)]
            for m, c in enumerate(children):
                assert matrix_move(pair_matrix(s),m) == pair_matrix(c)
                move_checks += 1
            values = [features(c) for c in children]
            nex = children[move]
            transitions += 1
            changed += nex != s
            hidden += nex != s and chart_key(nex) == chart_key(s)
            record = dict(id=row['id'],step=i,left=len(row['ac'])-i,
                          climb=sum(map(len,nex))>sum(map(len,s)),conjugation=move>=6)
            for name in SCORES:
                chosen = values[move][name]
                lower = sum(x[name]<chosen for x in values)
                equal = sum(x[name]==chosen for x in values)
                record[name] = (lower+0.5*(equal-1))/13
            records.append(record)
            s = nex
        assert s == TARGET
    groups = {}
    for name, pred in [('all',lambda r:True),('climb',lambda r:r['climb']),
                       ('far',lambda r:r['left']>=10),
                       ('climbing_conjugation',lambda r:r['climb'] and r['conjugation'])]:
        rr = [r for r in records if pred(r)]
        groups[name] = dict(steps=len(rr),mean_rank_fraction={
            s:sum(r[s] for r in rr)/len(rr) if rr else None for s in SCORES})
    # Paired path bootstrap; routes, not correlated individual steps, are units.
    rng = np.random.default_rng(20260929)
    paired = []
    for row in routes:
        rr = [r for r in records if r['id']==row['id'] and r['left']>=10]
        if rr:
            paired.append(sum(r['chain']-r['length'] for r in rr)/len(rr))
    bs = np.mean(rng.choice(paired,(2000,len(paired)),replace=True),axis=1)
    (HERE/(output_prefix+'route_step_scores.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in records))
    (HERE/(output_prefix+'verification.json')).write_text(json.dumps(certificates,indent=2)+'\n')
    return dict(routes=len(routes),transitions=transitions,full_state_changes=changed,
                chart_invisible_changes=hidden,chart_invisible_fraction=hidden/changed,
                nonterminal_center_occurrences=len(center),
                distinct_nonterminal_center_states=len({tuple(map(tuple,c['state'])) for c in center}),
                center_example=max(center,key=lambda c:c['left']) if center else None,
                official_matrix_move_crosschecks=move_checks,
                unique_states=len(states),groups=groups,
                far_chain_minus_length_path_mean=float(np.mean(paired)),
                far_chain_minus_length_path_bootstrap95=np.quantile(bs,[.025,.975]).tolist())


def main():
    result = dict(sair_commit=PIN, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    result['slater_identity'] = slater_check()
    result['optics'] = {str(a):dict(AB=optical_stack([(1.38,95),(2.1,65)],a),
                                     BA=optical_stack([(2.1,65),(1.38,95)],a)) for a in (0,45)}
    result['exact_ball'] = exact_ball()
    result['routes'] = route_probe()
    result['heldout_routes'] = route_probe('heldout_routes.json', 'heldout_')
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    main()
