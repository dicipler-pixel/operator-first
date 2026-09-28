# SCRIPT: CHARLIE_RUN -- one row through acc_disk, two-sided, verified by the official verifier.
# Usage: python3 charlie_run.py ROW_ID CAP [--meet-cap C] [--mem MB] [--work DIR] [--maxlayer N] [--below T]
#   Start side: exact frontier BFS from the row under total-length cap CAP (layers on disk).
#   Trivial side: the full closed component of ((x),(y)) under cap C, built once and kept (T_C/union.bin).
#   Stops at the first start-side layer that touches the trivial component (MEET), reaches the
#   trivial itself (TARGET), empties (CLOSED: certified, no solution inside cap CAP), or hits --below.
#   A found path = start->meet (from start layers) + meet->trivial (inverse of trivial->meet),
#   replayed under the official verifier before it is printed. Nothing unverified is ever printed.
import json, os, subprocess, sys, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
SAIR = os.environ.get('SAIR_TOOLS', '/home/claude/acc/sair/competition/tools')
sys.path.insert(0, SAIR)
from verifier import core
BIN = os.path.join(HERE, 'acc_disk')
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
INV = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12]

def load_row(cid):
    for mf in (os.path.join(SAIR, 'verifier/data/manifest.json'), os.path.join(SAIR, '../examples/training_manifest.json')):
        m = json.load(open(mf))
        for c in m['challenges']:
            if c['challenge_id'] == cid:
                return c, m['limits']
    raise SystemExit('row not found: ' + cid)

def sstr(r0, r1): return ''.join(L[a] for a in r0) + ',' + ''.join(L[a] for a in r1)

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode: raise SystemExit('failed: %s\n%s' % (' '.join(cmd), p.stderr))
    return p.stdout

def moves_to(dirn, state):
    out = run([BIN, 'path', dirn, state]).strip()
    return json.loads(out)

def main():
    a = sys.argv[1:]
    cid, cap = a[0], int(a[1]); opt = dict(zip(a[2::2], a[3::2]))
    meet_cap = int(opt.get('--meet-cap', 12)); mem = opt.get('--mem', '1500'); work = opt.get('--work', os.path.join(HERE, 'runs'))
    os.makedirs(work, exist_ok=True)
    c, limits = load_row(cid)
    start = sstr(*c['initial_relators'])
    tdir = os.path.join(work, 'T%d' % meet_cap); union = os.path.join(tdir, 'union.bin')
    if meet_cap > 0 and not os.path.exists(union):
        run([BIN, 'bfs', tdir, 'x,y', str(meet_cap), '--mem', mem, '--notarget'])
        run([BIN, 'union', tdir, union])
    rdir = os.path.join(work, '%s_cap%d' % (cid, cap))
    if os.path.exists(rdir): subprocess.run(['rm', '-rf', rdir])
    cmd = [BIN, 'bfs', rdir, start, str(cap), '--mem', mem]
    if meet_cap > 0: cmd += ['--meet', union]
    if opt.get('--lean') == '1': cmd += ['--lean']
    for k in ('--maxlayer', '--below'):
        if k in opt: cmd += [k, opt[k]]
    t0 = time.time(); out = run(cmd); dt = time.time() - t0
    res = [l for l in out.splitlines() if l.startswith('RESULT')][-1]
    print(res, '(%.1fs)' % dt)
    rec = {'row': cid, 'cap': cap, 'meet_cap': meet_cap, 'start': start, 'result': res, 'secs': round(dt, 1),
           'log': open(os.path.join(rdir, 'LOG.tsv')).read()}
    if ' state=' in res and ('TARGET' in res or 'MEET' in res):
        st = res.split(' state=')[1].strip()
        if opt.get('--lean') == '1':
            rec['note'] = 'lean run: layers deleted; rerun without --lean with --maxlayer set to the hit layer to recover start->meet path'
            print(rec['note'])
            with open(os.path.join(work, 'charlie_ledger.jsonl'), 'a') as f: f.write(json.dumps(rec) + '\n')
            return
        first = moves_to(rdir, st)
        second = [] if 'TARGET' in res else [INV[m] for m in reversed(moves_to(tdir, st))]
        path = first + second
        v = core.verify(c, path, 'ac-r2-v1', limits)
        rec.update(path=path, verify=v)
        print('verifier:', json.dumps(v))
        if v.get('ok'):
            line = '%s: %s' % (cid, json.dumps(path))
            print(line); rec['line'] = line
    with open(os.path.join(work, 'charlie_ledger.jsonl'), 'a') as f:
        f.write(json.dumps(rec) + '\n')

if __name__ == '__main__':
    main()
