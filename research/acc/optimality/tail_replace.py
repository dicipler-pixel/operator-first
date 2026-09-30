"""Long-window tail replacement: for each state s_i on a path, exact capped search from s_i to (x,y)
(capped BFS prefix + exact uncapped T_9 finish). If found length d < n-i, splice. Repeats until no gain.
usage: tail_replace.py SAIR BIN TFILE WORK row pathjson CAPSLACK BUDGET"""
import json, os, subprocess, sys, re
SAIR, BIN, TF, WORK, row, pj, slack, bud = sys.argv[1:9]
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
E = {1: 0, -1: 1, 2: 2, -2: 3}
path = json.loads(pj); st0 = tuple(tuple(r) for r in CH[row]['initial_relators'])
def states(p):
    s = [st0]
    for m in p: s.append(core.apply_move(s[-1], m))
    return s
improved = True
while improved:
    improved = False; S = states(path); n = len(path)
    order = range(0, n - 10)
    if os.environ.get("TAIL_ORDER") == "rev":   # opt-in: short, cheap tails first (default order unchanged)
        order = reversed(order)
    for i in order:
        st = S[i]; peak = max(len(a) + len(b) for a, b in S[i:]); cap = peak + int(slack)
        need = n - i - 1  # must find a path from s_i of length <= need
        args = [BIN + '/acc_capped', TF, str(cap), bud, WORK, 'tail', str(len(st[0])), *[str(E[t]) for t in st[0]], str(len(st[1])), *[str(E[t]) for t in st[1]]]
        p = subprocess.run(args, capture_output=True, text=True, env={'MAXD': str(need)})
        m = re.search(r'\] AC (\d+) PATH ([\d ]+)', p.stdout)
        if m and int(m.group(1)) <= need:
            new = path[:i] + list(map(int, m.group(2).split()))
            v = core.verify(CH[row], new, 'ac-r2-v1', man['limits'])
            if v['ok'] and len(new) < n:
                print(f"{row} splice at {i}: {n} -> {len(new)} (cap {cap})", flush=True); path = new; improved = True; break
        print(f"{row} i={i} cap={cap} no gain ({p.stdout.splitlines()[0][:80] if p.stdout else 'no output'})", flush=True)
print("FINAL", row, len(path), json.dumps(path).replace(' ', ''), flush=True)
