# SCRIPT: KERNEL-CLASS-SEARCH-01
# One search per twin class: beam each twin (in its own pool coordinates) until one is
# solved, then transfer that path to every one of our rows in the class (twin_transfer),
# replay each line with the official core, write HITS and a JSON log line per attempt.
import json, sys, time
sys.path.insert(0, '.')
from drive import solve, run
from twin_transfer import transfer
from verifier.core import free_reduce
W, D, L, mode, tag, shard, nshard = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], int(sys.argv[6]), int(sys.argv[7])
def parse(desc):
    body = desc.split('|')[1].split('>')[0]; out = []
    for part in body.split(';'):
        w = []
        for t in part.replace('= 1', '').split():
            g = 1 if t[0] == 'x' else 2; w.append(-g if '^-1' in t else g)
        out.append(w)
    return out
pool = {}
for l in open('/home/claude/sair/competition/problems/ac.jsonl'):
    d = json.loads(l); pool[d['challenge_id']] = parse(d['description'])
rows = {r['id']: r for r in json.load(open('rows_101_213.json'))}
det = {d['id']: d for d in json.load(open('ms_detect.json'))}
tw = json.load(open('ms_twins.json'))
classes = {}
for rid, t in tw.items(): classes.setdefault(tuple(t), []).append(rid)
order = sorted(classes.items(), key=lambda kv: (-len(kv[1]), det[kv[1][0]]['n']))
done = set()
try:
    for l in open('class_%s.jsonl' % tag): done.add(json.loads(l)['twin'])
except FileNotFoundError: pass
out = open('class_%s.jsonl' % tag, 'a')
for ci, (twins, ours) in enumerate(order):
    if ci % nshard != shard: continue
    for twin in twins:
        if twin in done: continue
        T0 = pool[twin]
        p, st, sec = solve(T0, W, D, L, 1, mode, 3000)
        rec = dict(class_index=ci, twin=twin, ours=ours, tag=tag, W=W, D=D, maxlen=L, mode=mode, status=st, sec=round(sec, 1))
        if p is not None:
            rec['twin_path'] = p
            s0 = (free_reduce(tuple(T0[0])), free_reduce(tuple(T0[1])))
            rec['twin_path_ok'] = run(s0, p) == ((1,), (2,))
            rec['transfers'] = {}
            for rid in ours:
                line = transfer(rows[rid]['rel'], det[rid]['auto'], [tuple(T0[0]), tuple(T0[1])], p)
                rec['transfers'][rid] = line
                if line is not None:
                    with open('HITS.txt', 'a') as h: h.write('%s: %s\n' % (rid, line))
        out.write(json.dumps(rec) + '\n'); out.flush()
        if p is not None: break
