# t00115 middle-bridge search. Exact: d(s_i,s_j) <= T  iff  B_i^{<=a} and B_j^{<=b} (a+b=T) share a state, all under cap K.
# Balls: acc_disk bfs (disk-backed exact capped BFS, official move table).  Usage: bridge.py ROW CAP [--maxst N] [--deadline EPOCH] [--gmin 15 --gmax 24]
import json, os, subprocess, sys, time
from replay import *
ART = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ART, '..', '..', '..', '..', '..'))
BIN = os.path.join(ART, '..', 't00073', 'bin', 'acc_disk'); WORK = os.path.join(ART, 'work')
TOKEN = '2f344389985971a605763f70'; STOPF = os.path.join(REPO, 'research/acc/upgh/STOP')
INV = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12]
args = sys.argv[1:]; ROW = args[0]; K = int(args[1])
def opt(n, d): return type(d)(args[args.index(n) + 1]) if n in args else d
MAXST = opt('--maxst', 12000000); DEADLINE = opt('--deadline', 0.0); GMIN = opt('--gmin', 15); GMAX = opt('--gmax', 24); RMAX = opt('--rmax', 16)
_hb = [0.0]
def hb():
    if time.time() - _hb[0] > 200:
        _hb[0] = time.time(); subprocess.run([sys.executable, os.path.join(REPO, 'tools/acc/upgh/upgh.py'), 'heartbeat', 't00115', TOKEN], capture_output=True, cwd=REPO)
def chk():
    hb()
    if os.path.exists(STOPF): raise SystemExit('STOP')
    if DEADLINE and time.time() > DEADLINE: raise TimeoutError('deadline')
def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode: raise SystemExit('failed %s %s' % (cmd[:3], p.stderr[-300:]))
    return p.stdout
for r, CH, S0, ROUTE, S in rows():
    if r == ROW: break
L = len(ROUTE); OVER = {'ac-05598': 1, 'ac-03913': 2}[ROW]
def freegb(): v = os.statvfs(WORK); return v.f_bavail * v.f_frsize / 1e9

def layers(d):
    out = []
    try:
        for l in open(os.path.join(d, 'LOG.tsv')):
            f = l.split('\t')
            if len(f) == 5 and f[0].isdigit(): out.append(int(f[1]))
    except OSError: pass
    return out   # sizes of layers 1..n  (layer 0 has 1 state)

def build_ball(i):
    d = os.path.join(WORK, '%s_K%d_s%d' % (ROW, K, i))
    if os.path.exists(d + '/DONE'): return d
    subprocess.run(['rm', '-rf', d])
    p = subprocess.Popen(['nice', '-n', '10', BIN, 'bfs', d, st(S[i]), str(K), '--mem', '1200', '--notarget', '--maxlayer', str(RMAX), '--minfree', '3'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    why = None
    while p.poll() is None:
        time.sleep(0.5)
        try: chk()
        except (TimeoutError, SystemExit): p.kill(); p.wait(); raise
        ly = layers(d); cm = 1 + sum(ly)
        if cm >= MAXST and len(ly) < RMAX:
            time.sleep(1.5)
            if p.poll() is None: why = 'budget cum %d >= %d after layer %d' % (cm, MAXST, len(ly)); p.kill(); p.wait(); break
        if os.path.isdir(d) and sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d)) > 1.6 * MAXST * 16 + 2e8:
            why = 'budget bytes inside layer %d' % (len(ly) + 1); p.kill(); p.wait(); break
        if freegb() < 2.0: why = 'disk low'; p.kill(); p.wait(); break
    out = p.stdout.read()
    ly = layers(d)
    # drop the partial layer file left by a kill
    for f in os.listdir(d):
        if f.startswith('run_') or (f.startswith('L_') and int(f[2:6]) > len(ly)): os.remove(os.path.join(d, f))
    json.dump({'state': st(S[i]), 'tot': tot(S[i]), 'layers': [1] + ly, 'radius': len(ly), 'stop': why or 'finished'}, open(d + '/DONE', 'w'))
    return d
def info(d): return json.load(open(d + '/DONE'))
def cum(inf, a): return sum(inf['layers'][:a + 1])

def union(d, a, tag):
    ud = os.path.join(WORK, 'u_' + tag); subprocess.run(['rm', '-rf', ud]); os.makedirs(ud)
    for t in range(a + 1): os.symlink(os.path.abspath(os.path.join(d, 'L_%04d.bin' % t)), os.path.join(ud, 'L_%04d.bin' % t))
    out = ud + '.bin'; run([BIN, 'union', ud, out]); subprocess.run(['rm', '-rf', ud]); return out
def moves_to(d, state): return json.loads(run([BIN, 'path', d, state]).strip())

elig = [i for i in range(3, L - 2) if tot(S[i]) <= K]      # both ends at least 3 moves from the route's ends
pairs = [(i, j) for i in elig for j in elig if GMIN <= j - i <= GMAX]
pairs.sort(key=lambda p: (-(p[1] - p[0]), p[0]))
need = sorted({x for p in pairs for x in p})
res = {'row': ROW, 'cap': K, 'route_len': L, 'over': OVER, 'maxst_ball': MAXST, 'rmax': RMAX, 'eligible_states': elig, 'n_pairs': len(pairs), 'balls': {}, 'pairs': [], 'shortened': []}
out = os.path.join(ART, 'res_%s_K%d.json' % (ROW, K))
def save(): res['wall_s'] = round(time.time() - t0, 1); json.dump(res, open(out, 'w'), indent=1)
t0 = time.time(); print(ROW, 'cap', K, 'eligible', elig, 'pairs', len(pairs), flush=True)
try:
    if not pairs: res['ended_by'] = 'no pair has both ends within the cap'; save(); raise SystemExit(0)
    # pairs, largest gap first
    cacheU = {}
    for (i, j) in pairs:
        chk(); g = j - i; T = g - OVER
        di, dj = build_ball(i), build_ball(j); fi, fj = info(di), info(dj)
        rec = {'i': i, 'j': j, 'gap': g, 'target_T': T, 'tot_i': tot(S[i]), 'tot_j': tot(S[j]), 'Ri': fi['radius'], 'Rj': fj['radius']}
        best = None
        for a in range(0, min(T, fi['radius']) + 1):
            b = T - a
            if b < 0 or b > fj['radius']: continue
            c = cum(fi, a) + cum(fj, b)
            if best is None or c < best[0]: best = (c, a, b)
        if best is None:
            rec.update(result='NOT_REACHED', why='Ri+Rj=%d < T=%d (ball budget stops: %s / %s)' % (fi['radius'] + fj['radius'], T, fi['stop'], fj['stop']))
            res['balls'][i] = {'tot': fi['tot'], 'radius': fi['radius'], 'cum': cum(fi, fi['radius']), 'stop': fi['stop']}; res['balls'][j] = {'tot': fj['tot'], 'radius': fj['radius'], 'cum': cum(fj, fj['radius']), 'stop': fj['stop']}
            res['pairs'].append(rec); save(); continue
        res['balls'][i] = {'tot': fi['tot'], 'radius': fi['radius'], 'cum': cum(fi, fi['radius']), 'stop': fi['stop']}; res['balls'][j] = {'tot': fj['tot'], 'radius': fj['radius'], 'cum': cum(fj, fj['radius']), 'stop': fj['stop']}
        c, a, b = best; rec.update(a=a, b=b, states=c)
        if c > 2 * MAXST: rec.update(result='NOT_REACHED', why='pair budget'); res['pairs'].append(rec); save(); continue
        t1 = time.time()
        ui = cacheU.get((i, a)) or union(di, a, 'i%d_%d' % (i, a)); cacheU = {(i, a): ui}
        uj = union(dj, b, 'j%d_%d' % (j, b))
        q = run([BIN, 'intersect', ui, uj]); os.remove(uj)
        if q.startswith('first'):
            m = q.split()[1]; pi = moves_to(di, m); pj = moves_to(dj, m)
            bridge = pi + [INV[x] for x in reversed(pj)]; new = ROUTE[:i] + bridge + ROUTE[j:]
            v = core.verify(CH, new, 'ac-r2-v1', man['limits'])
            rec.update(result='SHORTCUT', bridge_len=len(bridge), new_len=len(new), verify_ok=v['ok'])
            res['shortened'].append({'i': i, 'j': j, 'gap': g, 'bridge': bridge, 'new_len': len(new), 'route': new, 'verify_ok': v['ok']})
            if v['ok'] and len(new) < L:
                with open(os.path.join(ART, 'lines.txt'), 'a') as f:
                    f.write('%s: %s\n' % (ROW, json.dumps(new))); f.write('s%s: %s\n' % (ROW, json.dumps(new + [16, 15])))
        else:
            rec.update(result='CERTIFIED_NO_SHORTER_BRIDGE' )
        rec['secs'] = round(time.time() - t1, 1); res['pairs'].append(rec); save()
        print(rec, flush=True)
    res['ended_by'] = 'finished'
except TimeoutError:
    res['ended_by'] = 'wall_limit (deadline)'
except SystemExit as e:
    res['ended_by'] = 'stopped: %s' % e
save()
for f in os.listdir(WORK):
    if f.startswith('u_'): subprocess.run(['rm', '-rf', os.path.join(WORK, f)])
print(json.dumps({k: v for k, v in res.items() if k not in ('pairs', 'balls', 'shortened')}))
