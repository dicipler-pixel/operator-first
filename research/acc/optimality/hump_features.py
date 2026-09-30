"""Hump features of a start presentation ("Comutators" idea, 2026-09-28).

cyclic commutator load = min over cyclic rotations a of r0 and b of r1 of |free_reduce(a b a^-1 b^-1)|,
divided by 2 x (total start length). 1.0 = the relators share nothing. Lower = they nearly commute.

Across 292 verified known AC paths: corr(climb, cyclic load) = +0.36 (plain load +0.20);
corr(climb, start length) = -0.45. It predicts the typical climb, not the extreme humps (ac-03305
climbs +16 at load 0.67). Use it to order rows within a value tier (lower load first), not to set caps.

usage: hump_features.py MANIFEST targets.json [OUT.json]   (adds 'cload' and 'start' to each target)"""
import json, sys


def red(v):
    o = []
    for a in v:
        if o and o[-1] == -a:
            o.pop()
        else:
            o.append(a)
    return tuple(o)


def inv(v):
    return tuple(-a for a in reversed(v))


def cyc(w):
    w = list(w)
    while len(w) > 1 and w[0] == -w[-1]:
        w = w[1:-1]
    return tuple(w)


def cyclic_load(r0, r1):
    a0, b0 = cyc(r0), cyc(r1)
    best = min(len(red(a0[i:] + a0[:i] + b0[j:] + b0[:j] + inv(a0[i:] + a0[:i]) + inv(b0[j:] + b0[:j])))
               for i in range(len(a0)) for j in range(len(b0)))
    return best / (2 * (len(r0) + len(r1)))


if __name__ == '__main__':
    man = {c['challenge_id']: c['initial_relators'] for c in json.load(open(sys.argv[1]))['challenges']}
    T = json.load(open(sys.argv[2]))
    for t in T:
        r0, r1 = map(tuple, man[t['id']])
        t['start'] = len(r0) + len(r1)
        t['cload'] = round(cyclic_load(r0, r1), 3)
    json.dump(T, open(sys.argv[3] if len(sys.argv) > 3 else sys.argv[2], 'w'))
    print(len(T), 'targets annotated')
