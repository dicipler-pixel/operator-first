# SCRIPT: CHARLIE_CUTFIRST -- the rotate-and-cut pattern, used as a presolve for acc_disk.
# Pattern (from the ac-03719 tie): when one relator contains a rotated copy of the other (or of its
# inverse), a few rotations (length-preserving conjugations) line it up and ONE multiplication removes it.
# cuts(state): every (rotate r0 by i) + (rotate r1 by j) + one multiplication, with its exact move
# prefix and cost; the resulting states are sorted by total length after the cut.
# run(row, ...): exact two-sided search (acc_disk + trivial ball radius 9) from the best cut states,
# forward depth = record - 9 - cost(prefix). A hit = prefix + found path, replayed by the official
# verifier. Not a certificate: the optimum need not start with the cut. Every result goes to the ledger.
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import charlie_run as cr
core = cr.core
GI = {1: 6, -1: 7, 2: 8, -2: 9}          # conjugation move for r0 by letter g; +4 for r1
BALL = os.path.join(HERE, 'runs', 'B36'); UNION = os.path.join(BALL, 'union9.bin')
OUT = os.path.join(HERE, 'runs', 'charlie_cutfirst.jsonl')

def rotations(word, rel):
    """(moves, rotated word) for every left and right rotation, via single-letter conjugations."""
    out = {tuple(word): []}
    w = tuple(word); mv = []
    for k in range(1, len(word)):          # left: conjugate by the inverse of the first letter
        g = -w[0]; mv = mv + [GI[g] + 4 * rel]; w = core.free_reduce((g,) + w + (-g,)); out.setdefault(w, mv)
    w = tuple(word); mv = []
    for k in range(1, len(word)):          # right: conjugate by the last letter
        g = w[-1]; mv = mv + [GI[g] + 4 * rel]; w = core.free_reduce((g,) + w + (-g,))
        if w not in out or len(out[w]) > len(mv): out[w] = mv
    return out

def cuts(state):
    r0, r1 = state; res = []
    R0 = rotations(r0, 0); R1 = rotations(r1, 1)
    for a, ma in R0.items():
        for b, mb in R1.items():
            for m in (2, 3, 4, 5):
                t = core.apply_move((a, b), m)
                res.append((len(t[0]) + len(t[1]), len(ma) + len(mb) + 1, ma + mb + [m], t))
    res.sort(key=lambda x: (x[0], x[1]))
    return res

def run(cid, record, cap, top=3, mem='1500'):
    c, limits = cr.load_row(cid); s0 = tuple(map(tuple, c['initial_relators']))
    seen = set(); tried = 0
    for tot, cost, prefix, st in cuts(s0):
        if tot >= len(s0[0]) + len(s0[1]) or st in seen: continue
        seen.add(st); tried += 1
        if tried > top: break
        maxd = record - 9 - cost
        if maxd < 0: continue
        rdir = os.path.join(HERE, 'runs', 'cut', '%s_%d' % (cid, tried)); subprocess.run(['rm', '-rf', rdir])
        t0 = time.time()
        out = cr.run([cr.BIN, 'bfs', rdir, cr.sstr(*st), str(cap), '--mem', mem, '--meet', UNION, '--maxlayer', str(maxd), '--minfree', '6'])
        res = [l for l in out.splitlines() if l.startswith('RESULT')][-1]
        rec = {'row': cid, 'record': record, 'cap': cap, 'cut_prefix': prefix, 'cut_total': tot, 'result': res, 'secs': round(time.time() - t0, 1)}
        if 'MEET' in res or 'TARGET' in res:
            a = int(res.split('layer=')[1].split()[0]); La = os.path.join(rdir, 'L_%04d.bin' % a)
            for t in range(10):
                o = cr.run([cr.BIN, 'intersect', La, os.path.join(BALL, 'L_%04d.bin' % t)])
                if not o.startswith('first'): continue
                key = o.split()[1]
                path = prefix + cr.moves_to(rdir, key) + [cr.INV[m] for m in reversed(cr.moves_to(BALL, key))]
                v = core.verify(c, path, 'ac-r2-v1', limits)
                rec.update(length=len(path), path=path, ok=v.get('ok'),
                           verdict='BEAT' if len(path) < record else 'TIE' if len(path) == record else 'LONGER')
                break
        with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
        print(cid, 'cut', tot, 'cost', cost, res.split(' layer')[0], rec.get('verdict', ''), rec.get('length', ''), '(%.0fs)' % rec['secs'], flush=True)
        if rec.get('ok'): print('%s: %s' % (cid, json.dumps(rec['path'])), flush=True)
        subprocess.run(['rm', '-rf', rdir])
        if rec.get('verdict') in ('BEAT', 'TIE'): return rec

if __name__ == '__main__':
    cid, record, cap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    top = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    run(cid, record, cap, top)
