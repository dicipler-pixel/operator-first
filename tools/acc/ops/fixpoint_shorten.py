"""Fixpoint shortener (session 2): commute_clean (tools/acc/ops/commute_clean.py) + acc_window (window-14), repeated until neither shortens.
It took the step-2 BS roads ac-05698 128 -> 110 (BEAT 111) and ac-06792 137 -> 119 (then mid_restart -> 117, BEAT 118).
usage: ACC_S=<scratch dir with sair/ (official manifest) and chainbin/acc_window> python3 tools/acc/ops/fixpoint_shorten.py IN.jsonl OUT.jsonl
IN.jsonl lines: {"id": "ac-NNNNN", "ac": [moves]}. Prints "row L0 -> L1 -> ..." per road. Re-verify output with plan_offline before queueing."""
import json, re, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'scratch_utils'))
from commute_clean import clean
from acmoves import run
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
man = {c['challenge_id']: c for c in json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json'))['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}; E = {1: 0, -1: 1, 2: 2, -2: 3}
def window(cid, path):
    r0, r1 = man[cid]['initial_relators']; os.makedirs(S + '/work_win_' + cid, exist_ok=True)
    args = [S + '/chainbin/acc_window', S + '/work_win_' + cid, str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1], str(len(path)), *map(str, path)]
    p = subprocess.run(args, capture_output=True, text=True)
    m = re.search(r'FINALPATH ?([\d ]*)', p.stdout)
    return list(map(int, m.group(1).split())) if m else path
out = open(sys.argv[2], 'w')
for l in open(sys.argv[1]):
    x = json.loads(l); cid = x['id']; p = x['ac']
    R = tuple(''.join(L[i] for i in r) for r in man[cid]['initial_relators']); hist = [len(p)]
    while True:
        q = clean(window(cid, clean(p)))
        if run(R, q) != ('x', 'y') or len(q) >= len(p): break
        p = q; hist.append(len(p))
    print(cid, ' -> '.join(map(str, hist)), flush=True)
    out.write(json.dumps({'id': cid, 'ac': p, 'src': 'bs2 + commute_clean + window14'}) + '\n'); out.flush()
