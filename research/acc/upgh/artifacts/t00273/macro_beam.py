"""Macro-move beam for one row. A macro = conjugate ONE relator by a reduced word u (|u| <= CL, applied as single
conjugation moves 6..13) and then ONE multiplication move (2,3,4,5). States are scored by total length only after
the multiplication, so a route that climbs over a length hump during the conjugation is not pruned. Width WID per
macro depth, global dedup. Every state with total length <= FIN is finished by an exact BFS (depth <= 9) to (x,y);
any full path is replayed with the pinned official core and written to OUT as `ac-XXXXX: [...]` + `sac-...`.
The best KEEP states of every depth (by total length) are dumped to CANDS.json as prefixes for beam_from.py.
usage: macro_beam.py ROW WID CL DEPTH FIN KEEP OUT CANDS LOG [WALL_S]"""
import json, os, sys, time, itertools
from collections import deque
SAIR = '/root/.cache/upgh/sair'; STOP = '/home/user/operator-first/research/acc/upgh/STOP'
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
row = sys.argv[1]; WID, CL, DEPTH, FIN, KEEP = map(int, sys.argv[2:7]); OUT, CANDS, LOG = sys.argv[7:10]
WALL = float(sys.argv[10]) if len(sys.argv) > 10 else 600
ch = CH[row]; S0 = tuple(tuple(r) for r in ch['initial_relators']); GOAL = ((1,), (2,))
am = core.apply_move
# conjugator move sequences: reduced words over the 4 conjugation moves of a relator (6..9 for r0, 10..13 for r1);
# consecutive inverse conjugations (x then X) are useless, so skip them.
INV = {0: 1, 1: 0, 2: 3, 3: 2}
def conj_seqs(CL):
    out = [()]
    for L in range(1, CL + 1):
        for t in itertools.product(range(4), repeat=L):
            if any(t[i + 1] == INV[t[i]] for i in range(L - 1)): continue
            out.append(t)
    return out
SEQS = conj_seqs(CL); CL2 = int(os.environ.get('CL2', '0')); SEQS2 = conj_seqs(CL2)
def expand(s):
    for rel in (0, 1):
        base = 6 if rel == 0 else 10; base2 = 10 if rel == 0 else 6
        for t2 in SEQS2:
            s2 = s; mv2 = []
            for k in t2:
                s2 = am(s2, base2 + k); mv2.append(base2 + k)
            for t in SEQS:
                u = s2; mv = list(mv2)
                for k in t:
                    u = am(u, base + k); mv.append(base + k)
                for mm in (2, 3, 4, 5):
                    v = am(u, mm)
                    yield v, mv + [mm]
def finish(s, maxd=9):
    if s == GOAL: return []
    seen = {s: None}; q = deque([(s, 0)])
    while q:
        u, d = q.popleft()
        if d >= maxd: continue
        for m in range(14):
            v = am(u, m)
            if v in seen: continue
            seen[v] = (u, m)
            if v == GOAL:
                p = []; w = v
                while seen[w] is not None: w, m2 = seen[w]; p.append(m2)
                return p[::-1]
            if len(v[0]) + len(v[1]) <= FIN + 6: q.append((v, d + 1))
    return None
log = open(LOG, 'a'); t0 = time.time()
log.write(f"# {row} WID={WID} CL={CL} CL2={CL2} DEPTH={DEPTH} FIN={FIN} KEEP={KEEP} seqs={len(SEQS)}x{len(SEQS2)}\n"); log.flush()
front = {S0: []}; seen = {S0}; cands = []; found = []
for d in range(1, DEPTH + 1):
    if os.path.exists(STOP) or time.time() - t0 > WALL: log.write("# stop/wall\n"); break
    nxt = {}
    for s, pre in front.items():
        for v, mv in expand(s):
            if v in seen or v in nxt: continue
            nxt[v] = pre + mv
    ranked = sorted(nxt.items(), key=lambda kv: (len(kv[0][0]) + len(kv[0][1]), len(kv[1])))
    front = dict(ranked[:WID]); seen.update(front)
    tots = [len(s[0]) + len(s[1]) for s in front]
    log.write(f"{row} d={d} gen={len(nxt)} kept={len(front)} tot[{min(tots)}..{max(tots)}] t={time.time()-t0:.0f}s\n"); log.flush()
    for s, pre in ranked[:KEEP]:
        cands.append({'tag': f'macro_d{d}_tot{len(s[0])+len(s[1])}', 'prefix': pre})
    for s, pre in front.items():
        if len(s[0]) + len(s[1]) <= FIN:
            tail = finish(s)
            if tail is not None:
                full = pre + tail; v = core.verify(ch, full, 'ac-r2-v1', man['limits'])
                log.write(f"FOUND d={d} len={len(full)} ok={v['ok']} {json.dumps(v)} path={json.dumps(full).replace(' ','')}\n"); log.flush()
                if v['ok']:
                    found.append(full)
                    with open(OUT, 'a') as f:
                        f.write(f"{row}: {json.dumps(full).replace(' ', '')}\n"); f.write(f"s{row}: {json.dumps(full+[16,15]).replace(' ', '')}\n")
    if found: break
json.dump(cands, open(CANDS, 'w'))
log.write(f"# done {row} found={[len(p) for p in found]} wall={time.time()-t0:.0f}s cands={len(cands)}\n")
print("DONE", row, [len(p) for p in found])
