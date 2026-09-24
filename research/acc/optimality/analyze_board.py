"""Rank full-board batch results (xy- = AC to (x,y), yx- = swapped start, i.e. AC to (y,x)).
Every candidate path is replayed by the official verifier (ac core / stable core) before listing.
usage: analyze_board.py SAIR board_a5.txt snapshot.json held_from_history.json OUTDIR"""
import json, sys, re, pathlib
sair, res, snap, heldf, outdir = sys.argv[1:6]; out = pathlib.Path(outdir)
sys.path.insert(0, sair + '/competition/tools'); from verifier import core, stable_core
man = json.load(open(sair + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
board = {x['challengeId']: x for x in json.load(open(snap))['data']['items']}
held = json.load(open(heldf))
PI = {6: 8, 8: 6, 7: 9, 9: 7, 10: 12, 12: 10, 11: 13, 13: 11}
xy, yx = {}, {}
for line in open(res):
    m = re.match(r'(xy|yx)-(\d+) S=\d+ meets=\d+ dist=(\d+) rebuild=\d+ path ?([\d ]*)', line)
    if m: (xy if m.group(1) == 'xy' else yx)[m.group(2)] = list(map(int, m.group(4).split()))
ac_new, ac_tie, sac_lines, notes = [], [], [], []
for n, p in xy.items():
    cid = 'ac-' + n; assert core.verify(CH[cid], p, 'ac-r2-v1', man['limits'])['ok']
    b = board.get(cid, {}); rec = b.get('currentBestLength'); k = b.get('kTeams')
    mine = held['ac'].get(cid)
    if rec is None: ac_new.append((cid, p, 'FIRST SOLVE (unsolved on 09-14 snapshot)'))
    elif len(p) < rec: ac_new.append((cid, p, f'NEW RECORD {len(p)} < {rec}'))
    elif len(p) == rec and (mine is None or mine > rec): ac_tie.append((cid, p, f'tie {rec}, k={k}'))
for n in set(xy) | set(yx):
    cid, sid = 'ac-' + n, 'sac-' + n; cands = []
    if n in xy: cands.append((xy[n] + [16, 15], 'xy+2'))
    if n in yx: cands.append(([PI.get(t, t) for t in yx[n]] + [15, 15], 'yx+2'))
    p, how = min(cands, key=lambda c: len(c[0]))
    v = stable_core.verify(CH[sid], p, 'sac-r8-v1', man['limits']); assert v['ok'], (sid, v)
    mine = held['sac'].get(sid)
    if mine is None or len(p) < mine: sac_lines.append((sid, p, f'{len(p)} via {how}; team held {mine}; AC board record {board.get(cid,{}).get("currentBestLength")}'))
def write(name, rows):
    (out / f'{name}.txt').write_text(''.join(f"{c}: {json.dumps(p).replace(' ', '')}\n" for c, p, _ in rows))
    (out / f'{name}_annotated.txt').write_text(''.join(f"{c}: {json.dumps(p).replace(' ', '')}  # {w}\n" for c, p, w in rows))
write('BOARD_AC_NEW_RECORDS', ac_new); write('BOARD_AC_TIES', ac_tie); write('BOARD_SAC', sac_lines)
print(f"xy hits {len(xy)}, yx hits {len(yx)}; AC new records/first solves {len(ac_new)}; AC ties {len(ac_tie)}; SAC lines {len(sac_lines)}")
for c, p, w in ac_new: print('  ***', c, len(p), w)
