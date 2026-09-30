"""t00126 mirror-start driver.
usage: mirror.py ROW PHI W   (PHI in x|y|xy : which generators are inverted by the automorphism)
Builds S'=phi(S), runs acc_beam on S', windows the AC path on S', replays on S' with the pinned core,
maps every state back with phi, finds move ids, appends inversion move(s), replays the full route from S.
env BEAM_* passed through."""
import sys, os, re, json, subprocess, time
SAIR = os.environ.get('SAIR', '/root/.cache/upgh/sair')
sys.path.insert(0, SAIR + '/competition/tools')
from verifier import core
MAN = SAIR + '/competition/tools/verifier/data/manifest.json'
BIN = os.path.expanduser('~/.cache/upgh/bin'); TF = os.path.expanduser('~/.cache/upgh/T9.tab')
ART = '/home/user/operator-first/research/acc/upgh/artifacts/t00126'
E = {1: 0, -1: 1, 2: 2, -2: 3}; D = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
S = lambda r: ''.join(D[a] for a in r) or '1'
REC = {'ac-03913': 46, 'ac-02386': 34, 'ac-04316': 43}
row, phi_name, W = sys.argv[1], sys.argv[2], sys.argv[3]
inv_gens = set(abs(g) for g in ({'x': [1], 'y': [2], 'xy': [1, 2]}[phi_name]))
def phi_letter(a): return -a if abs(a) in inv_gens else a
def phi_word(w): return core.free_reduce(tuple(phi_letter(a) for a in w))
def phi_state(s): return (phi_word(s[0]), phi_word(s[1]))
man = json.load(open(MAN)); lim = man['limits']
ch = {c['challenge_id']: c for c in man['challenges']}[row]
S0 = (tuple(ch['initial_relators'][0]), tuple(ch['initial_relators'][1]))
Sm = phi_state(S0)
chm = dict(ch); chm['initial_relators'] = [list(Sm[0]), list(Sm[1])]
def enc(s): return [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
tag = f'{row}_{phi_name}_W{W}'
dm = str(REC[row] + int(os.environ.get('BEAM_FREE_DMAX', '20')))
t0 = time.time()
p = subprocess.run([BIN + '/acc_beam', TF, W, dm, *enc(Sm)], capture_output=True, text=True)
wall = round(time.time() - t0, 1)
open(f'{ART}/work/{tag}.out', 'w').write(p.stdout + '\n---STDERR---\n' + p.stderr[-3000:])
res = {'row': row, 'phi': phi_name, 'W': W, 'wall_s': wall, 'start_mirror': [S(Sm[0]), S(Sm[1])]}
def window(s, path):
  try:
    q = subprocess.run([BIN + '/acc_window', ART + '/work', *enc(s), str(len(path)), *map(str, path)], capture_output=True, text=True, timeout=int(os.environ.get('WIN_TIMEOUT', '75')))
    m = re.search(r'FINALPATH ?([\d ]*)', q.stdout)
    return list(map(int, m.group(1).split())) if m else path
  except subprocess.TimeoutExpired:
    return path
def replay(start, path):
    st = start; out = [st]
    for m in path:
        st = core.apply_move(st, m); out.append(st)
    return out
def map_back(raw):
    t = replay(Sm, raw)
    u = [phi_state(s) for s in t]   # phi involution
    assert u[0] == S0
    ids = []
    for k in range(len(raw)):
        found = [m for m in range(14) if core.apply_move(u[k], m) == u[k + 1]]
        if not found: return None, f'no move at step {k}'
        ids.append(found[0])
    fin = u[-1]; st = fin
    # inversion moves, found by testing
    tgt = ((1,), (2,))
    for m in (0, 1):
        if st[m] != tgt[m]:
            st2 = core.apply_move(st, m)
            if st2[m] == tgt[m]: ids.append(m); st = st2
    return ids, None
res['beam_paths'] = []
routes = []
for kind in ('AC',):
    for m in re.finditer(r'^%s (\d+) PATH ([\d ]+)' % kind, p.stdout, re.M):
        raw = list(map(int, m.group(2).split()))
        r = core.verify(chm, raw, ch['move_spec_version'], lim)
        ent = {'raw_len': len(raw), 'replay_S_mirror_ok': bool(r.get('ok'))}
        cands = [('raw', raw)]
        if len(raw) <= REC[row] + 12:
            w = window(Sm, raw)
            if w != raw and core.verify(chm, w, ch['move_spec_version'], lim).get('ok'):
                cands.append(('window', w)); ent['window_len'] = len(w)
        for nm, path in cands:
            if not core.verify(chm, path, ch['move_spec_version'], lim).get('ok'): continue
            ids, err = map_back(path)
            if ids is None: ent[nm + '_map_err'] = err; continue
            rr = core.verify(ch, ids, ch['move_spec_version'], lim)
            ent[nm + '_mapped_len'] = len(ids); ent[nm + '_mapped_ok'] = bool(rr.get('ok')); ent[nm + '_mapped_code'] = rr.get('code')
            if rr.get('ok'): routes.append((nm, ids))
        res['beam_paths'].append(ent)
# also try windowing the mapped route from the official start
best = {}
for nm, ids in list(routes):
    if len(ids) <= REC[row] + 12 and os.environ.get('WIN_S', '0') == '1':
        w = window(S0, ids)
        if w != ids and core.verify(ch, w, ch['move_spec_version'], lim).get('ok'):
            routes.append((nm + '+wS', w))
            res.setdefault('mapped_window_S', []).append(len(w))
uniq = {}
for nm, ids in routes: uniq.setdefault(tuple(ids), nm)
res['ok_routes'] = sorted(len(k) for k in uniq)
with open(f'{ART}/lines.txt', 'a') as f:
    for ids, nm in sorted(uniq.items(), key=lambda kv: len(kv[0])):
        f.write(f'# {row} phi={phi_name} W={W} src={nm} len={len(ids)} record={REC[row]}\n')
        f.write(f'{row}: {json.dumps(list(ids))}\n'); f.write(f's{row}: {json.dumps(list(ids) + [16, 15])}\n')
with open(f'{ART}/results.jsonl', 'a') as f: f.write(json.dumps(res) + '\n')
print(json.dumps(res), flush=True)
