"""Replay bidir.cpp PATH outputs (prefix to a named state) + the paid finish on the pinned official core;
write every route that replays to (x,y) into lines.txt as ac-00003 / sac-00003 lines.
usage: mkroutes.py OUTFILE:SUFFIXNAME ...  (suffix 'G' = 12-move finish from G, 'S3' = 9 moves after the first 3 finish moves)"""
import sys, os, json, re
sys.path.insert(0, os.environ.get('SAIR', '/root/.cache/upgh/sair') + '/competition/tools')
from verifier import core
man = json.load(open(os.environ.get('SAIR', '/root/.cache/upgh/sair') + '/competition/tools/verifier/data/manifest.json'))
ch = [c for c in man['challenges'] if c['challenge_id'] == 'ac-00003'][0]
start = tuple(tuple(r) for r in ch['initial_relators'])
FIN = [5, 1, 6, 13, 13, 5, 3, 3, 3, 3, 3, 3]
out = []
for arg in sys.argv[1:]:
    fn, kind = arg.split(':')
    txt = open(fn).read()
    m = re.search(r'^PATH\s*(.*)$', txt, re.M)
    if not m: print(fn, 'no path'); continue
    pre = [int(t) for t in m.group(1).split()]
    fin = FIN if kind == 'G' else FIN[3:]
    mv = pre + fin
    s = start; mx = sum(map(len, s))
    for q in mv:
        s = core.apply_move(s, q); mx = max(mx, len(s[0]) + len(s[1]))
    ok = s == ((1,), (2,))
    print(fn, kind, 'prefix', len(pre), 'total', len(mv), 'peak', mx, 'replay ok', ok)
    if ok: out.append(mv)
seen = set()
with open('lines.txt', 'a') as f:
    for mv in out:
        if tuple(mv) in seen: continue
        seen.add(tuple(mv))
        f.write('ac-00003: %s\n' % json.dumps(mv))
        f.write('sac-00003: %s\n' % json.dumps(mv + [16, 15]))
