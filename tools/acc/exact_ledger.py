"""Turn capgen.sh logs into one ledger line per exact capped run.

Each capgen run searched every state reachable from the row start whose total relator length stays
<= CAP, breadth-first to depth MAXD = REC - 9, then finished with the T9 table (all states within 9
moves of (x,y), no length cap on those last 9 moves). States are stored as 128-bit fingerprints.
  complete   : BFS reached depth MAXD+1 or closed (no new states) -> "no AC path of length <= REC whose
               first REC-9 moves stay under CAP" (bar a fingerprint collision)
  incomplete : stopped by the state budget before MAXD; only the depths reached are covered
usage: exact_ledger.py OUT.jsonl QUEUE.txt... -- LOG...   (QUEUE lines: ID REC "caps")"""
import json, re, sys
a = sys.argv[1:]; out = a[0]; k = a.index('--'); queues, logs = a[1:k], a[k + 1:]
rec = {}
for q in queues:
    for l in open(q):
        p = l.split()
        if len(p) >= 2 and p[1].isdigit(): rec[p[0]] = int(p[1])
runs = {}
for f in logs:
    for l in open(f, errors='ignore'):
        m = re.search(r'\[c(\d+)\] cap=(\d+) states=(\d+) depth=(\d+) (CLOSED|STOPPED)', l)
        if m:
            i, cap, n, d, how = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
            R = rec.get(i); maxd = R - 9 if R else None
            done = how == 'CLOSED' or (maxd is not None and d > maxd)
            runs[(i, cap)] = dict(id='ac-' + i, record_at_run=R, cap=cap, maxd=maxd, states=n, depth=d,
                                  status='complete' if done else 'incomplete', ac=None, sac=None, log=f.split('/')[-1])
            continue
        m = re.search(r'\[c(\d+)\] (AC|SAC) (NONE|(\d+).*)', l)
        if m:
            for (i, cap), r in runs.items():
                if i == m.group(1) and r[m.group(2).lower()] is None: r[m.group(2).lower()] = 'none' if m.group(3) == 'NONE' else int(m.group(4))
with open(out, 'w') as f:
    for r in sorted(runs.values(), key=lambda r: (r['id'], r['cap'])): f.write(json.dumps(r) + '\n')
c = sum(r['status'] == 'complete' for r in runs.values())
print(f'{len(runs)} runs: {c} complete, {len(runs) - c} incomplete; hits:', [ (r['id'], r['cap'], r['ac'], r['sac']) for r in runs.values() if r['ac'] not in (None, 'none') or r['sac'] not in (None, 'none')])
