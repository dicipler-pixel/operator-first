# SCRIPT: CHARLIE_LEDGER_RUN -- finish the board's stalled exact capped runs with acc_disk.
# For a row with board record R under cap K (from ledger/exact_capped_runs.jsonl):
#   forward: exact frontier BFS from the row under total-length cap K, all layers kept on disk,
#            checked against the trivial ball B (radius 9, cap 36) layer by layer, to depth R - 9.
#   The first forward layer a that meets B gives the exact shortest length within the cap:
#   L* = a + t_min, t_min = smallest ball depth among the meeting states (any path of length
#   L < L* would have met at forward layer max(0, L - 9) < a). No meet by depth R - 9 = certified:
#   no path of length <= R under cap K. DISKFULL = incomplete (the depth reached is recorded).
#   Every path is rebuilt from the layer files and replayed by the official verifier first.
# Usage: python3 ledger_run.py ROW_ID [ROW_ID ...]   (reads exact_capped_runs_from_board.jsonl)
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import charlie_run as cr
BIN = cr.BIN; BALL = os.path.join(HERE, 'runs', 'B36'); UNION = os.path.join(BALL, 'union9.bin'); R_BALL = 9
WORK = os.path.join(HERE, 'runs', 'ledger'); os.makedirs(WORK, exist_ok=True)
BOARD = {json.loads(l)['id']: json.loads(l) for l in open(os.environ.get('CHARLIE_BOARD', os.path.abspath(os.path.join(HERE, '../../../research/acc/live/ledger/exact_capped_runs.jsonl')))) if l.strip()}
OUT = os.path.join(HERE, 'runs', 'charlie_ledger_rows.jsonl')

def one(cid):
    b = BOARD[cid]; R, K = b['record_at_run'], b['cap'] + int(os.environ.get('CAPPLUS', '0')); maxd = R - R_BALL
    c, limits = cr.load_row(cid); start = cr.sstr(*c['initial_relators'])
    rdir = os.path.join(WORK, cid + '_cap%d' % K); subprocess.run(['rm', '-rf', rdir])
    t0 = time.time()
    out = cr.run([BIN, 'bfs', rdir, start, str(K), '--mem', os.environ.get('MEM', '3000'), '--meet', UNION, '--maxlayer', str(maxd), '--minfree', '6'])
    dt = time.time() - t0
    res = [l for l in out.splitlines() if l.startswith('RESULT')][-1]
    log = [l.split('\t') for l in open(os.path.join(rdir, 'LOG.tsv')) if l[0].isdigit()]
    depth = int(log[-1][0]) if log else 0
    if log and log[-1][1] == '0': depth -= 1
    rec = {'row': cid, 'record': R, 'cap': K, 'forward_depth_needed': maxd, 'ball': 'trivial radius 9 under cap 36',
           'result': res, 'forward_depth_done': depth, 'states': int(log[-1][2]) if log else 1, 'secs': round(dt, 1),
           'board_run': {'states': b['states'], 'depth': b['depth'], 'status': b['status']}}
    if 'MEET' in res or 'TARGET' in res:
        a = int(res.split('layer=')[1].split()[0]); La = os.path.join(rdir, 'L_%04d.bin' % a)
        for t in range(R_BALL + 1):
            o = cr.run([BIN, 'intersect', La, os.path.join(BALL, 'L_%04d.bin' % t)])
            if not o.startswith('first'): continue
            key = o.split()[1]
            path = cr.moves_to(rdir, key) + [cr.INV[m] for m in reversed(cr.moves_to(BALL, key))]
            v = cr.core.verify(c, path, 'ac-r2-v1', limits)
            rec.update(forward_layer=a, ball_depth=t, length=len(path), path=path, verify=v,
                       verdict=('BEAT' if len(path) < R else 'TIE' if len(path) == R else 'LONGER'))
            if v.get('ok'): rec['line'] = '%s: %s' % (cid, json.dumps(path))
            break
    elif 'CLOSED' in res:
        rec['verdict'] = 'CERTIFIED: component under cap %d closed at %d states, no path at all under the cap' % (K, rec['states'])
    elif 'MAXLAYER' in res:
        rec['verdict'] = 'CERTIFIED: no path of length <= %d under cap %d' % (R, K)
    else:
        rec['verdict'] = 'INCOMPLETE: forward depth %d of %d (%s)' % (depth, maxd, res.split()[1])
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
    print(cid, rec.get('verdict'), rec.get('length', ''), 'states', rec['states'], '(%.0fs)' % dt, flush=True)
    if rec.get('line'): print(rec['line'], flush=True)
    # keep disk free: layers are only needed for path recovery, which is done
    subprocess.run(['rm', '-rf', rdir])

if __name__ == '__main__':
    for cid in sys.argv[1:]:
        try:
            one(cid)
        except SystemExit as e:
            print(cid, 'ENGINE FAILED (logged, moving on):', str(e)[:200], flush=True)
            with open(OUT, 'a') as f: f.write(json.dumps({'row': cid, 'verdict': 'ENGINE FAILED', 'detail': str(e)[:300]}) + '\n')
