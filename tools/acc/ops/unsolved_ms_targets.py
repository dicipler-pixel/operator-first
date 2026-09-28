"""Targets for an unsolved-MS lane: rows unsolved by every team whose MS(n,w) family has a solved n.
Ordered by distance to the nearest solved n, then that solved record. AK(3)-class rows are skipped (open problems).
usage: python3 tools/acc/ops/unsolved_ms_targets.py NAME COUNT   (run from the repo root; writes $ACC_S/work/NAME_targets.json)
Any path at all is a first solve (1.0), so ac_record/sac_record are set to 998 for watch_sweeps (it reads a missing path as 999)."""
import gzip, glob, json, os, sys
name, count = sys.argv[1], int(sys.argv[2])
d = json.load(open('research/acc/live/ledger/ms_families_by_w_20260928.json'))
def rows(f):
    x = json.load(gzip.open(f))["data"]; lst = next(v for v in x.values() if isinstance(v, list))
    return {r["challengeId"]: r["currentBestLength"] for r in lst}
A = rows(sorted(glob.glob("research/acc/live/boards/ac_2026*.json.gz"))[-1])
ak = {r if isinstance(r, str) else (r.get('id') or r.get('challenge_id'))
      for r in json.load(open('research/acc/live/AK3_CLASS_ROWS.json'))['rows']}
out = []
for w, v in d.items():
    st = {int(n): (A.get(v[n][2]), v[n][2]) for n in v}
    sol = {n: s for n, s in st.items() if s[0] is not None}
    for n, s in st.items():
        if s[0] is not None or not sol or s[1] in ak: continue
        m = min(sol, key=lambda k: abs(k - n)); out.append((abs(m - n), sol[m][0], s[1], w, n))
out.sort(); seen = set(); T = []
for g, l, cid, w, n in out:
    if cid in seen: continue
    seen.add(cid)
    T.append({'id': cid, 'record': 118, 'k': 0, 'ac_record': 998, 'sac_record': 998,
              'hint': f'MS({n},{w}); nearest solved n at distance {g}, record {l}'})
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
json.dump(T[:count], open(f'{S}/work/{name}_targets.json', 'w'))
print(len(T), 'candidates;', name, 'gets', min(count, len(T)), '; first', T[0])
