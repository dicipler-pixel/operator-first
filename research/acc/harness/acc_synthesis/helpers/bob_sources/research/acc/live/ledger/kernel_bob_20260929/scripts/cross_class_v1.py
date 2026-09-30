# SCRIPT: KERNEL-CROSS-CLASS-01
# Cross-row transfer through changes of generators. Sources = our 250 record-length paths +
# 40 near-miss paths (bundle). For each source row A and each small automorphism psi
# (images of x, y of length <= 3), find pool rows B whose relators equal psi(A) up to letter
# symmetry, rotation, inversion and relator order. Transfer A's path to B (twin_transfer),
# shorten with the reach-2 block splice, replay with the official core, record the length.
import json, sys, time
sys.path.insert(0, '.'); sys.path.insert(0, '/home/claude/bob_splice')
from ms_detect import red, inv, sub, cyc_forms, autos
from twin_transfer import transfer, SYMS, sym_imgs
from ms_route import run, T
from load_bundle_v1 import near, rec, lib
from block_splice_v1 import make_steps, splice_path
from verifier.core import free_reduce
def parse(desc):
    body = desc.split('|')[1].split('>')[0]; out = []
    for part in body.split(';'):
        w = []
        for t in part.replace('= 1', '').split():
            g = 1 if t[0] == 'x' else 2; w.append(-g if '^-1' in t else g)
        out.append(w)
    return out
def apply_sym(w, s):
    sw, sx, sy = s; o = []
    for a in w:
        g = abs(a); sg = 1 if a > 0 else -1
        o.append(((2 if sw else 1) * sg * sx) if g == 1 else ((1 if sw else 2) * sg * sy))
    return o
def key(R): return frozenset([min(cyc_forms(R[0])), min(cyc_forms(R[1]))])
pool = {}
for l in open('/home/claude/sair/competition/problems/ac.jsonl'):
    d = json.loads(l); pool[d['challenge_id']] = parse(d['description'])
bykey = {}
for cid, R in pool.items():
    for s in SYMS:
        bykey.setdefault(key([apply_sym(R[0], s), apply_sym(R[1], s)]), set()).add(cid)
sources = {r['id']: r['path'] for r in rec}
for n in near: sources.setdefault(n['id'], n['path'])
best_known = {r['id']: len(r['path']) for r in rec}
records = {n['id']: n['record'] for n in near}
steps = make_steps(lib)
done = set()
try:
    for l in open('cross_class_v1.jsonl'): done.add(json.loads(l)['source'])
except FileNotFoundError: pass
out = open('cross_class_v1.jsonl', 'a'); t0 = time.time(); tried = 0
for A, pA in sources.items():
    if A in done: continue
    RA = pool[A]
    targets = set()
    for a, b in autos:
        img = {1: a, 2: b}
        for B in bykey.get(key([sub(RA[0], img), sub(RA[1], img)]), ()):
            if B != A: targets.add((B, tuple(map(tuple, (a, b)))))
    seenB = set()
    for B, _ in sorted(targets):
        if B in seenB: continue
        RB = pool[B]
        # find psi with psi(B) ~ A
        psi = None
        for a, b in autos:
            if key([sub(RB[0], {1: a, 2: b}), sub(RB[1], {1: a, 2: b})]) in [key([apply_sym(RA[0], s), apply_sym(RA[1], s)]) for s in SYMS]:
                psi = (a, b); break
        if psi is None: continue
        line = transfer(RB, psi, [tuple(RA[0]), tuple(RA[1])], pA)
        tried += 1
        if line is None: continue
        s0 = (free_reduce(tuple(RB[0])), free_reduce(tuple(RB[1])))
        short = list(splice_path(s0, line, steps, max_len=40))
        ok = run(s0, short) == T
        seenB.add(B)
        out.write(json.dumps(dict(source=A, source_len=len(pA), target=B, psi=[list(psi[0]), list(psi[1])], raw_len=len(line), len=len(short), ok=ok, target_record=records.get(B), our_best=best_known.get(B), path=short)) + '\n'); out.flush()
print('sources', len(sources), 'transfers tried', tried, round(time.time() - t0), 's')
