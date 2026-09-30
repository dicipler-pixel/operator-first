"""Compile an smbeam class road into official ac-r2-v1 moves with Git's road-keeping DP, verify with the official core,
then window-shorten (acc_window). usage: compile_road.py ROW ROADFILE"""
import json, re, subprocess, sys
import os; S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import skel_dp_local as k
E = {1: 0, -1: 1, 2: 2, -2: 3}
def parse(f):
    road = []; on = False
    for l in open(f):
        if l.startswith('ROAD'): on = True; continue
        if on and '|' in l:
            a, b = l.split('|'); road.append((tuple(int(t) for t in a.split()), tuple(int(t) for t in b.split())))
    return road
def window(r0, r1, p):
    q = subprocess.run([S + '/p2ybin/acc_window', S + '/work_sfwin', str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1], str(len(p)), *map(str, p)], capture_output=True, text=True)
    m = re.search(r'FINALPATH ?([\d ]*)', q.stdout); return list(map(int, m.group(1).split())) if m else p
def compile_row(cid, roadfile, grows=(1, 2, 3, 4)):
    c = k.T[cid]; st = tuple(tuple(r) for r in c['initial_relators']); tg = ((1,), (2,))
    road = parse(roadfile); R = []
    for s in road:
        cl = k.cls(s)
        if not R or R[-1] != cl: R.append(cl)
    if R[0] != k.cls(st): R.insert(0, k.cls(st))
    if R[-1] != k.cls(tg): return {'id': cid, 'err': 'end class'}, None
    for g in grows:
        out = k.solve(st, tg, R, GROW=g, SLACK=3, MAXC=16)
        if out is None: continue
        v = k.core.verify(c, out, 'ac-r2-v1', k.rl.LIMITS)
        if not (v.get('ok', v.get('valid', False)) or v.get('status') == 'ok'): continue
        w = window(*c['initial_relators'], out)
        v2 = k.core.verify(c, w, 'ac-r2-v1', k.rl.LIMITS)
        best = w if (v2.get('ok', v2.get('valid', False)) or v2.get('status') == 'ok') and len(w) < len(out) else out
        return {'id': cid, 'road': len(R), 'grow': g, 'dp_len': len(out), 'ac_len': len(best)}, best
    return {'id': cid, 'road': len(R), 'err': 'compile failed'}, None
if __name__ == '__main__':
    rec, out = compile_row(sys.argv[1], sys.argv[2]); print(json.dumps(rec)); print(json.dumps(out) if out else 'NOPATH')
