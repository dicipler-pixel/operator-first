# Positive/negative control of the pair test: for pairs whose route sub-path stays within the cap, T=g must intersect (route itself is a bridge of length g)
# and, as already proven uncapped for g<=14 and by the main run for g>=15, T=g-1 must not.  Uses the same acc_disk/union/intersect mechanics as bridge.py.
import json, os, subprocess, sys
from replay import *
ART = os.path.dirname(os.path.abspath(__file__)); BIN = os.path.join(ART, '..', 't00073', 'bin', 'acc_disk'); WORK = os.path.join(ART, 'work')
def run(c): 
    p = subprocess.run(c, capture_output=True, text=True); assert p.returncode == 0, p.stderr; return p.stdout
def ball(state, K, R, tag):
    d = os.path.join(WORK, 'ctl_' + tag); subprocess.run(['rm', '-rf', d]); run(['nice', '-n', '10', BIN, 'bfs', d, state, str(K), '--mem', '500', '--notarget', '--maxlayer', str(R)]); return d
def union(d, a, tag):
    ud = os.path.join(WORK, 'cu_' + tag); subprocess.run(['rm', '-rf', ud]); os.makedirs(ud)
    for t in range(a + 1): os.symlink(os.path.abspath(os.path.join(d, 'L_%04d.bin' % t)), os.path.join(ud, 'L_%04d.bin' % t))
    o = ud + '.bin'; run([BIN, 'union', ud, o]); subprocess.run(['rm', '-rf', ud]); return o
out = []
for row, K, prs in (('ac-05598', 33, [(3, 18), (4, 19), (5, 20)]), ('ac-03913', 34, [(3, 18), (5, 20), (8, 23), (10, 26)])):
    for r, CH, S0, ROUTE, S in rows():
        if r != row: continue
        for (i, j) in prs:
            g = j - i; mx = max(tot(s) for s in S[i:j + 1]); assert mx <= K, (row, i, j, mx)
            di = ball(st(S[i]), K, 9, 'i'); dj = ball(st(S[j]), K, 9, 'j')
            for T in (g, g - 1):
                a = (T + 1) // 2; b = T - a
                ui = union(di, a, 'i'); uj = union(dj, b, 'j'); q = run([BIN, 'intersect', ui, uj])
                out.append({'row': row, 'cap': K, 'i': i, 'j': j, 'gap': g, 'T': T, 'route_subpath_max_total': mx, 'intersects': q.startswith('first'), 'expected': T == g})
                print(out[-1], flush=True)
json.dump(out, open(os.path.join(ART, 'control.json'), 'w'), indent=1)
ok = all(o['intersects'] == o['expected'] for o in out); print('CONTROL', 'PASS' if ok else 'FAIL')
