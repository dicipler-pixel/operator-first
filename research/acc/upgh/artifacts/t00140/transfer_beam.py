"""Transfer + repair: prefix states T_i of sibling (n=4) routes applied to the n=3 start (original route and all
single-deletion variants), filtered to total length <= MAXTOT, deduped, ordered by prefix length descending.
From each T_i run acc_beam to (x,y) with DMAX = record - i. Any full path (prefix + beam tail) is verified with the
pinned core and appended to OUT (text lines `ac-XXXXX: [...]`). Logs every state covered.
usage: transfer_beam.py ROW_N3 RECORD ROUTES_JSON W MAXTOT OUT LOG [MINREM] [WALL_S]
env BEAM_DIV/BEAM_SEED/BEAM_NOISE passed through."""
import json, os, re, subprocess, sys, time
SAIR = '/root/.cache/upgh/sair'; BIN = os.path.expanduser('~/.cache/upgh/bin'); TF = os.path.expanduser('~/.cache/upgh/T9.tab')
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
row, record, routes, W, MAXTOT, OUT, LOG = sys.argv[1], int(sys.argv[2]), json.loads(sys.argv[3]), sys.argv[4], int(sys.argv[5]), sys.argv[6], sys.argv[7]
MINREM = int(sys.argv[8]) if len(sys.argv) > 8 else 6
WALL = float(sys.argv[9]) if len(sys.argv) > 9 else 1500
E = {1: 0, -1: 1, 2: 2, -2: 3}
def enc(s): return [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
ch = CH[row]; st0 = tuple(tuple(r) for r in ch['initial_relators']); TGT = ((1,), (2,))
cands = {}  # state -> (prefix moves) shortest prefix
def walk(p, tag):
    s = st0
    for i, m in enumerate(p):
        s = core.apply_move(s, m)
        if len(s[0]) + len(s[1]) > MAXTOT: break
        if s == TGT: continue
        if s not in cands or len(cands[s][0]) > i + 1: cands[s] = (p[:i + 1], tag)
for r in routes:
    walk(r, 'orig')
    for d in range(len(r)): walk(r[:d] + r[d + 1:], 'del%d' % d)
order = sorted(cands.items(), key=lambda kv: (-len(kv[1][0]), len(kv[0][0]) + len(kv[0][1])))
log = open(LOG, 'a'); t0 = time.time(); best = None
log.write(f"# {row} record={record} W={W} MAXTOT={MAXTOT} candidates={len(order)} seed={os.environ.get('BEAM_SEED')} noise={os.environ.get('BEAM_NOISE')}\n"); log.flush()
for s, (pref, tag) in order:
    i = len(pref); rem = record - i
    if rem < MINREM: continue
    if time.time() - t0 > WALL: log.write("# wall limit reached\n"); break
    if os.path.exists('/home/user/operator-first/research/acc/upgh/STOP'): log.write("# STOP\n"); break
    t1 = time.time()
    try:
        p = subprocess.run([BIN + '/acc_beam', TF, W, str(rem), *enc(s)], capture_output=True, text=True, timeout=600)
        outp = p.stdout
    except subprocess.TimeoutExpired:
        outp = 'TIMEOUT'
    m = re.search(r'^AC (\d+) PATH ([\d ]+)', outp, re.M)
    res = 'none'
    if m:
        tail = list(map(int, m.group(2).split())); full = pref + tail
        v = core.verify(ch, full, 'ac-r2-v1', man['limits'])
        res = f"AC {len(full)} ok={v['ok']}"
        if v['ok']:
            with open(OUT, 'a') as f: f.write(f"{row}: {json.dumps(full).replace(' ', '')}\n")
            if best is None or len(full) < best: best = len(full)
    log.write(f"i={i} tag={tag} tot={len(s[0])+len(s[1])} rem={rem} -> {res} ({time.time()-t1:.0f}s) state={enc(s)}\n"); log.flush()
log.write(f"# done {row} best={best} wall={time.time()-t0:.0f}s\n")
print("DONE", row, "best", best)
