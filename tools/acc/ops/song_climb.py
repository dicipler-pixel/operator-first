"""Song experiment (session 2): 'the shine goes up before it goes down / bump before the ground'.
ac-09400 (record 35): Charlie certified no path <= 35 with relator-total peak <= 34. So climb first: every distinct state
1..D moves from the start with total in [LO, HI], then beam each to (x,y) with DMAX = 35 - d. Report any full route <= 35.
usage: song_climb.py D LO HI W NPROC"""
import json, os, re, subprocess, sys, time
from multiprocessing import Pool
sys.path.insert(0, 'tools/acc/scratch_utils'); from acmoves import move, run
S = '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad'
D, LO, HI, W, NP = map(int, sys.argv[1:6]); T = 35
man = {c['challenge_id']: c for c in json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json'))['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}; E = {'x': '0', 'X': '1', 'y': '2', 'Y': '3'}
R0 = tuple(''.join(L[i] for i in r) for r in man['ac-09400']['initial_relators'])
seen = {R0: []}; frontier = [R0]; bumps = []
for d in range(1, D + 1):
    nxt = []
    for s in frontier:
        for mv in range(14):
            t = move(s, mv)
            if t in seen: continue
            seen[t] = seen[s] + [mv]; nxt.append(t)
            if LO <= len(t[0]) + len(t[1]) <= HI: bumps.append(t)
    frontier = nxt
print(json.dumps({'states': len(seen), 'bumps': len(bumps)}), flush=True)
def beam(s):
    pre = seen[s]; a, b = s; dmax = T - len(pre)
    p = subprocess.run([S + '/p2ybin/acc_beam', S + '/p2beam/T8.tab', str(W), str(dmax), str(len(a)), *[E[c] for c in a], str(len(b)), *[E[c] for c in b]],
                       capture_output=True, text=True)
    m = re.search(r'^AC (\d+) PATH ([\d ]*)', p.stdout, re.M)
    if not m: return (len(pre), None)
    full = pre + list(map(int, m.group(2).split()))
    return (len(pre), full if run(R0, full) == ('x', 'y') else None)
t0 = time.time(); best = None; n = 0
with Pool(NP) as pool:
    for d, full in pool.imap_unordered(beam, bumps, chunksize=4):
        n += 1
        if full and (best is None or len(full) < len(best)):
            best = full; print(json.dumps({'found': len(full), 'prefix': d, 'route': full}), flush=True)
        if n % 200 == 0: print(json.dumps({'done': n, 'of': len(bumps), 'best': len(best) if best else None, 's': round(time.time() - t0)}), flush=True)
print(json.dumps({'END': True, 'done': n, 'best': len(best) if best else None, 'route': best, 's': round(time.time() - t0)}), flush=True)
