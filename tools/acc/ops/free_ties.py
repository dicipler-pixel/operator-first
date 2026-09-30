"""Find scoring lines we already hold paths for but never sent: AC paths at or under the live AC record, and
SAC lines = AC path + [15,15] (or a stored SAC path) at or under the live SAC record. Writes candidate lines to
OUT (default $ACC_S/free_ties.txt); verify them with `sair_api.py plan` before queueing. Run from the repo root.
Sources: ACC_SUBMIT*, queue (sent and pending), inbox (and sent), crossrow road ledgers, ledger JSONs with paths,
scratch lane outputs (*_cap.jsonl, p2beam)."""
import glob, gzip, json, os, re, sys
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
OUT = sys.argv[1] if len(sys.argv) > 1 else S + '/free_ties.txt'
def rows(f):
    d = json.load(gzip.open(f))["data"]; lst = next(v for v in d.values() if isinstance(v, list))
    return {r["challengeId"]: (r["currentBestLength"], r["kTeams"]) for r in lst}
A = rows(sorted(glob.glob("research/acc/live/boards/ac_2026*.json.gz"))[-1])
B = rows(sorted(glob.glob("research/acc/live/boards/stable_ac_2026*.json.gz"))[-1])
sent = {}
for l in open('research/acc/live/SENT_ROWS.txt'):
    if l.startswith('#') or not l.strip(): continue
    t = l.split(); sent[t[0]] = int(t[1])
AC, SAC = {}, {}
def add(D, cid, p):
    if isinstance(p, list) and p and all(isinstance(x, int) for x in p):
        if cid not in D or len(p) < len(D[cid]): D[cid] = p
def walk(o, cid=None):
    if isinstance(o, dict):
        c = o.get('id') or o.get('challenge_id') or o.get('row') or cid
        if isinstance(c, str): c = c.split('#')[0]
        for k, v in o.items():
            if k in ('ac', 'ac_path', 'path') and isinstance(c, str) and c.startswith('ac-'): add(AC, c, v)
            elif k in ('sac', 'sac_path') and isinstance(c, str): add(SAC, 's' + c if c.startswith('ac-') else c, v)
            else: walk(v, c)
    elif isinstance(o, list):
        for v in o: walk(v, cid)
for f in (glob.glob("ACC_SUBMIT*.txt") + glob.glob("research/acc/live/queue/**/*.txt", recursive=True)
          + glob.glob("research/acc/live/inbox/**/*.txt", recursive=True)):
    for l in open(f):
        m = re.match(r"\s*(s?ac-\d+):\s*(\[.*\])", l)
        if m: add(SAC if m.group(1).startswith('sac') else AC, m.group(1), json.loads(m.group(2)))
for f in glob.glob("research/acc/live/ledger/*.json"):
    try: walk(json.load(open(f)))
    except Exception: pass
for f in glob.glob(S + "/work/*_cap.jsonl") + glob.glob(S + "/p2beam/*.jsonl") + glob.glob("research/acc/live/sweeps/*_cap.jsonl"):
    for l in open(f):
        try: walk(json.loads(l))
        except Exception: pass
lines = []
for cid, p in AC.items():
    rec = A.get(cid)
    if not rec or rec[0] is None: continue
    if len(p) <= rec[0] and sent.get(cid, 999) > len(p): lines.append((cid, p, rec))
    s = 's' + cid; rs = B.get(s)
    if not rs or rs[0] is None: continue
    sp = SAC.get(s)
    cand = [q for q in (sp, p + [15, 15]) if q]
    q = min(cand, key=len)
    if len(q) <= rs[0] and sent.get(s, 999) > len(q): lines.append((s, q, rs))
for cid, q in SAC.items():
    rs = B.get(cid)
    if rs and rs[0] is not None and len(q) <= rs[0] and sent.get(cid, 999) > len(q) and not any(l[0] == cid for l in lines):
        lines.append((cid, q, rs))
with open(OUT, 'w') as f:
    for cid, p, rec in sorted(lines):
        f.write(f"{cid}: [{','.join(map(str, p))}]\n")
print(f"{len(AC)} AC and {len(SAC)} SAC paths; {len(lines)} candidate lines -> {OUT}")
for cid, p, rec in sorted(lines): print(' ', cid, len(p), 'record', rec)
