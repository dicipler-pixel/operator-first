# SCRIPT: CHARLIE_EASY_EXACT -- exact two-sided search on short-start rows, climbing a cap ladder
# Forward frontier BFS from the row under total-length cap K (acc_disk), every new layer checked against B36
# (all states within 9 moves of ((x),(y)) under cap 36). Run to depth max(R - 9, 1) (R = AC record; depth >= 1
# because acc_disk checks the meet set on generated layers only).
#   MEET at first layer a, smallest ball depth t: a + t = exact shortest path length under cap K (K <= 36).
#   MAXLAYER: certified, no path of length <= R under cap K.   CLOSED: certified, no path at all under cap K.
# Hits: AC line verified by the official ac-r2-v1 core; Stable line = path + [16, 15] verified by sac-r8-v1
# (dropped to the inbox only when the Stable record is given; otherwise kept as a candidate in the record).
# Caps: start+FROM .. start+TO step 2 (env), stopping a row at a hit, an incomplete run, or > STOPST states.
# Usage: FROM=0 TO=2 python3 easy_exact.py ROW:RECORD[:SACRECORD][:FROM] ...
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import charlie_run as cr
sys.path.insert(0, cr.SAIR)
from verifier import stable_core
BIN = cr.BIN; BALL = os.path.join(HERE, 'runs', 'B36'); UNION = os.path.join(BALL, 'union9.bin')
WORK = os.path.join(HERE, 'runs', 'easy'); os.makedirs(WORK, exist_ok=True)
OUT = os.path.join(HERE, 'runs', 'charlie_easy_exact.jsonl'); INB = os.path.join(HERE, 'runs', 'surgery_inbox'); os.makedirs(INB, exist_ok=True)
MANI = json.load(open(os.path.join(cr.SAIR, 'verifier/data/manifest.json')))

def drop(line, rid):
    open(os.path.join(INB, '%s_charlie_%s.txt' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()), rid)), 'w').write(line + '\n')

def one(cid, R, SR, K):
    c, lim = cr.load_row(cid); start = cr.sstr(*c['initial_relators'])
    rdir = os.path.join(WORK, '%s_cap%d' % (cid, K)); subprocess.run(['rm', '-rf', rdir]); t0 = time.time()
    out = cr.run([BIN, 'bfs', rdir, start, str(K), '--mem', os.environ.get('MEM', '2500'), '--meet', UNION,
                  '--maxlayer', str(max(R - 9, 1)), '--minfree', '4'])
    res = [l for l in out.splitlines() if l.startswith('RESULT')][-1]
    log = [l.split('\t') for l in open(os.path.join(rdir, 'LOG.tsv')) if l[0].isdigit()]
    depth = int(log[-1][0]) if log else 0
    if log and log[-1][1] == '0': depth -= 1
    states = int(res.split('states=')[1].split()[0])
    rec = {'row': cid, 'ac_record': R, 'sac_record': SR, 'cap': K, 'result': res, 'depth_done': depth, 'states': states, 'by': 'charlie'}
    if 'MEET' in res or 'TARGET' in res:
        a = int(res.split('layer=')[1].split()[0]); La = os.path.join(rdir, 'L_%04d.bin' % a)
        for t in range(10):
            q = cr.run([BIN, 'intersect', La, os.path.join(BALL, 'L_%04d.bin' % t)])
            if not q.startswith('first'): continue
            key = q.split()[1]
            path = cr.moves_to(rdir, key) + [cr.INV[m] for m in reversed(cr.moves_to(BALL, key))]
            v = cr.core.verify(c, path, 'ac-r2-v1', lim)
            sid = 'sac-' + cid[3:]; sc = [z for z in MANI['challenges'] if z['challenge_id'] == sid][0]
            sp = path + [16, 15]; sv = stable_core.verify(sc, sp, 'sac-r8-v1', MANI['limits'])
            L = len(path)
            rec.update(length=L, exact_shortest_under_cap=(K <= 36), path=path, ac_ok=v.get('ok'), sac_ok=sv.get('ok'),
                       verdict='BEAT' if L < R else 'TIE' if L == R else 'LONGER')
            if v.get('ok') and L <= R:
                rec['line'] = '%s: %s' % (cid, json.dumps(path)); drop(rec['line'], cid)
            if sv.get('ok') and SR and len(sp) <= SR:
                rec['sac_line'] = '%s: %s' % (sid, json.dumps(sp)); drop(rec['sac_line'], sid)
            elif sv.get('ok') and L <= R:
                rec['sac_candidate'] = '%s: %s' % (sid, json.dumps(sp))
            break
    elif 'CLOSED' in res:
        rec['verdict'] = 'CERTIFIED: component under cap %d closed at %d states, no path at all' % (K, states)
    elif 'MAXLAYER' in res:
        rec['verdict'] = 'CERTIFIED: no path of length <= %d under cap %d' % (R, K)
    else:
        rec['verdict'] = 'INCOMPLETE: depth %d of %d (%s); no path of length <= %d under cap %d' % (depth, R - 9, res.split()[1], depth + 9, K)
    rec['secs'] = round(time.time() - t0, 1)
    subprocess.run(['rm', '-rf', rdir])
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
    print(cid, 'cap', K, rec.get('verdict'), rec.get('length', ''), 'states', states, '(%.0fs)' % rec['secs'], flush=True)
    for k in ('line', 'sac_line', 'sac_candidate'):
        if rec.get(k): print(rec[k], flush=True)
    return rec

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        p = arg.split(':'); cid, R = p[0], int(p[1])
        SR = int(p[2]) if len(p) > 2 and p[2] else None
        fr = int(p[3]) if len(p) > 3 else int(os.environ.get('FROM', '0'))
        c, _ = cr.load_row(cid); s = sum(len(r) for r in c['initial_relators'])
        for K in range(s + fr, s + int(os.environ.get('TO', '2')) + 1, 2):
            try:
                rec = one(cid, R, SR, K)
                if rec.get('line') or 'INCOMPLETE' in rec.get('verdict', '') or rec['states'] > int(os.environ.get('STOPST', '400000000')):
                    break
            except SystemExit as e:
                subprocess.run('rm -rf %s/%s_cap%d' % (WORK, cid, K), shell=True)
                print(cid, K, 'ENGINE FAILED', str(e)[:200], flush=True)
                with open(OUT, 'a') as f: f.write(json.dumps({'row': cid, 'cap': K, 'verdict': 'ENGINE FAILED', 'detail': str(e)[:300]}) + '\n')
                break
