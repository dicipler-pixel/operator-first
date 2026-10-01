"""Beam from prefix states of a row. For each candidate (tag, prefix moves) run acc_beam from the state reached by the
prefix on the row's start; any AC tail is joined to the prefix and replayed with the pinned official core; verified
full paths are appended to OUT as text lines `ac-XXXXX: [...]` and `sac-XXXXX: [... + [16, 15]]`. Every attempt is
logged (state, W, DMAX, env, result) so a miss has an exact scope.
usage: beam_from.py ROW CANDS.json W DMAX OUT LOG [WALL_S] [PER_RUN_S]
CANDS.json: [{"tag": "...", "prefix": [moves]}, ...]  (prefix may be empty = the start)
env BEAM_DIV / BEAM_NOV / BEAM_LOOK / BEAM_SEED / BEAM_NOISE are passed through to acc_beam."""
import json, os, re, subprocess, sys, time
SAIR = '/root/.cache/upgh/sair'; BIN = os.path.expanduser('~/.cache/upgh/bin'); TF = os.path.expanduser('~/.cache/upgh/T9.tab')
STOP = '/home/user/operator-first/research/acc/upgh/STOP'
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
row, CANDS, W, DMAX, OUT, LOG = sys.argv[1:7]
WALL = float(sys.argv[7]) if len(sys.argv) > 7 else 1500; PER = float(sys.argv[8]) if len(sys.argv) > 8 else 600
E = {1: 0, -1: 1, 2: 2, -2: 3}
def enc(s): return [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
ch = CH[row]; st0 = tuple(tuple(r) for r in ch['initial_relators']); TGT = ((1,), (2,))
cands = json.load(open(CANDS))
envd = {k: os.environ.get(k) for k in ('BEAM_DIV', 'BEAM_NOV', 'BEAM_LOOK', 'BEAM_SEED', 'BEAM_NOISE')}
log = open(LOG, 'a'); t0 = time.time(); best = None
log.write(f"# {row} W={W} DMAX={DMAX} cands={len(cands)} env={json.dumps(envd)} per_run_s={PER} wall_s={WALL}\n"); log.flush()
for c in cands:
    pref = c['prefix']; s = st0
    for m in pref: s = core.apply_move(s, m)
    if time.time() - t0 > WALL: log.write("# wall limit reached\n"); break
    if os.path.exists(STOP): log.write("# STOP\n"); break
    t1 = time.time(); outp = ''; err = ''
    try:
        p = subprocess.run([BIN + '/acc_beam', TF, W, DMAX, *enc(s)], capture_output=True, text=True, timeout=PER)
        outp, err = p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        outp = 'TIMEOUT'
    m = re.search(r'^AC (\d+) PATH ([\d ]+)', outp, re.M)
    res = 'none' if outp != 'TIMEOUT' else 'timeout'
    if m:
        tail = list(map(int, m.group(2).split())); full = pref + tail
        v = core.verify(ch, full, 'ac-r2-v1', man['limits'])
        res = f"AC {len(full)} ok={v['ok']} verify={json.dumps(v)}"
        if v['ok']:
            sac = full + [16, 15]
            with open(OUT, 'a') as f:
                f.write(f"{row}: {json.dumps(full).replace(' ', '')}\n"); f.write(f"s{row}: {json.dumps(sac).replace(' ', '')}\n")
            if best is None or len(full) < best: best = len(full)
    last = [l for l in err.strip().splitlines() if l.startswith('d=')]
    log.write(f"tag={c['tag']} i={len(pref)} tot={len(s[0])+len(s[1])} -> {res} ({time.time()-t1:.0f}s) last={last[-1] if last else ''} state={' '.join(enc(s))} prefix={json.dumps(pref).replace(' ', '')}\n"); log.flush()
log.write(f"# done {row} best={best} wall={time.time()-t0:.0f}s\n")
print("DONE", row, "best", best)
