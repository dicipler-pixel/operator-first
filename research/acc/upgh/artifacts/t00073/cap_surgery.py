# t00073 builder adapter around Charlie's surgery.py (research/acc/live/charlie/v45/tools/surgery.py).
# Differences from the original, all deliberate:
#   * the ceiling K is an argument (original: K = peak + 2 = 33); here K = 37.
#   * tails use a trivial ball built under the SAME cap K (original: B36 with cap min(K,36)).
#   * tail balls are met on ball layer 9 only (not the union of layers 0..9), to save 3 GB of disk; the argument is
#     exact for any path of length >= 10 (the point at forward distance l-9 on a shortest path has ball depth exactly
#     9), and pairs with d <= 9 are checked separately by testing whether the root lies in ball layers 0..9.
#   * heads use the union of the head ball layers 0..9 (as the original), plus the same root-membership check.
#   * every acc_disk search is under a watchdog: budget stop at MAXST cumulative states, byte watchdog mid layer,
#     free-disk floor, global deadline.  The original never aborted a search (MAXST was tested after it finished).
#   * the window step (missing module window.py) is replaced by the exact uncapped acc_window (pairs <= 14 apart);
#     an uncapped no-shortcut result implies no capped (K = 37) window <= 11 shortcut.
# Usage: python3 cap_surgery.py head|tail|windows|control  [--deadline EPOCH]
import json, os, re, subprocess, sys, time

ART = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ART, '..', '..', '..', '..', '..'))
SAIR = os.environ.get('SAIR_TOOLS', os.path.expanduser('~/.cache/upgh/sair/competition/tools'))
sys.path.insert(0, SAIR)
from verifier import core
BIN = os.path.join(ART, 'bin', 'acc_disk')
WINBIN = os.path.expanduser('~/.cache/upgh/bin/acc_window')
WORK = os.path.join(ART, 'work')
ROW = 'ac-00975'
K = int(os.environ.get('K', '37')); MAXST = int(os.environ.get('MAXST', '80000000')); MEM = os.environ.get('MEM', '2500')
MAXL = int(os.environ.get('MAXL', '22')); MINFREE_GB = 4.0
TOKEN = '80897c20a0f71abc6b48d180'
INV = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12]
LET = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
ENC = {1: 0, -1: 1, 2: 2, -2: 3}
T0 = float(open(os.path.join(ART, 'T0.txt')).read())
DEADLINE = T0 + 2400
for i, a in enumerate(sys.argv):
    if a == '--deadline': DEADLINE = float(sys.argv[i + 1])
STOPF = os.path.join(REPO, 'research/acc/upgh/STOP')
_lasthb = [0.0]

def st(s): return ''.join(LET[a] for a in s[0]) + ',' + ''.join(LET[a] for a in s[1])
def tot(s): return len(s[0]) + len(s[1])
def stop_check():
    if os.path.exists(STOPF): raise SystemExit('STOP file present')
def heartbeat(force=False):
    if force or time.time() - _lasthb[0] > 240:
        _lasthb[0] = time.time()
        subprocess.run([sys.executable, os.path.join(REPO, 'tools/acc/upgh/upgh.py'), 'heartbeat', 't00073', TOKEN],
                       capture_output=True, text=True, cwd=REPO)
def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode: raise SystemExit('failed: %s\n%s' % (' '.join(cmd), p.stderr[-500:]))
    return p.stdout
def du(path):
    t = 0
    for f in os.listdir(path):
        try: t += os.path.getsize(os.path.join(path, f))
        except OSError: pass
    return t
def freegb():
    v = os.statvfs(WORK); return v.f_bavail * v.f_frsize / 1e9

man = json.load(open(os.path.join(SAIR, 'verifier/data/manifest.json')))
CH = [c for c in man['challenges'] if c['challenge_id'] == ROW][0]
S0 = tuple(map(tuple, CH['initial_relators']))
bundle = json.load(open(os.path.join(REPO, 'research/acc/live/charlie/charlie_surgery_bundle_20260929.json')))
ENTRY = [e for e in bundle if e.get('id') == ROW and e.get('side') == 'ac'][0]
ROUTE = ENTRY['moves']
def replay(s0, p):
    S = [s0]
    for m in p: S.append(core.apply_move(S[-1], m))
    return S
S = replay(S0, ROUTE); N = len(ROUTE)
assert N == 35 and S[-1] == ((1,), (2,)) and list(map(list, S0)) == ENTRY['start']
assert core.verify(CH, ROUTE, 'ac-r2-v1', man['limits'])['ok']

def search(tag, start, cap, meet, maxlayer, maxst=MAXST):
    """acc_disk bfs under a watchdog. returns dict(result, states, secs, layers, ...). The dir is kept on MEET."""
    rdir = os.path.join(WORK, tag); subprocess.run(['rm', '-rf', rdir])
    cmd = ['nice', '-n', '10', BIN, 'bfs', rdir, start, str(cap), '--mem', MEM, '--meet', meet,
           '--maxlayer', str(maxlayer), '--minfree', str(MINFREE_GB), '--notarget']
    t0 = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    reason = None; logp = os.path.join(rdir, 'LOG.tsv')
    def layers():
        out = []
        try:
            for l in open(logp):
                f = l.split('\t')
                if len(f) == 5 and f[0].isdigit(): out.append((int(f[0]), int(f[1]), int(f[2])))
        except OSError: pass
        return out
    while p.poll() is None:
        time.sleep(1.0); heartbeat()
        if os.path.exists(STOPF): reason = 'STOP file'
        elif time.time() > DEADLINE: reason = 'global deadline'
        else:
            ly = layers(); cum = ly[-1][2] if ly else 1
            if cum >= maxst and ly[-1][0] < maxlayer:
                time.sleep(3)          # grace: a MEET/CLOSED at this very layer ends the process within milliseconds
                if p.poll() is not None: break
                reason = 'budget: cumulative %d >= MAXST %d after layer %d' % (cum, maxst, ly[-1][0])
            elif os.path.isdir(rdir) and du(rdir) > 1.5 * maxst * 16 + 1e8: reason = 'budget: on-disk bytes %.2f GB (> 1.5 x MAXST x 16 B) inside layer %d' % (du(rdir) / 1e9, len(ly) + 1)
            elif freegb() < 2.0: reason = 'disk: free %.1f GB < 2' % freegb()
        if reason:
            p.kill(); p.wait(); break
    out = p.stdout.read(); ly = layers()
    res = [l for l in out.splitlines() if l.startswith('RESULT')]
    rec = {'tag': tag, 'start': start, 'cap': cap, 'maxlayer': maxlayer, 'secs': round(time.time() - t0, 1),
           'layer_sizes': [x[1] for x in ly], 'states_completed': ly[-1][2] if ly else 1}
    if reason:
        rec.update(result='BUDGET_STOP' if reason.startswith('budget') else 'ABORT', reason=reason)
        subprocess.run(['rm', '-rf', rdir]); return rec
    if p.returncode or not res:
        rec.update(result='ERROR', reason='rc=%s %s' % (p.returncode, p.stderr.read()[-300:])); subprocess.run(['rm', '-rf', rdir]); return rec
    r = res[-1]; rec['raw'] = r; rec['result'] = r.split()[1]
    rec['states'] = int(r.split('states=')[1].split()[0])
    if 'layer=' in r: rec['meet_layer'] = int(r.split('layer=')[1].split()[0])
    if rec['result'] == 'DISKFULL': rec['reason'] = 'acc_disk clean stop (free disk < minfree + need)'
    if rec['result'] != 'MEET': subprocess.run(['rm', '-rf', rdir])
    return rec

def moves_to(dirn, state): return json.loads(run([BIN, 'path', dirn, state]).strip())
def root_depth_in_ball(state_str, ball, tag):
    """smallest t in 0..9 with the state in ball layer t, else None (ball = dir with L_0000..L_0009)."""
    rd = os.path.join(WORK, 'root_' + tag); subprocess.run(['rm', '-rf', rd])
    run([BIN, 'bfs', rd, state_str, '40', '--maxlayer', '0', '--notarget'])
    for t in range(10):
        o = run([BIN, 'intersect', os.path.join(rd, 'L_0000.bin'), os.path.join(ball, 'L_%04d.bin' % t)])
        if 'common 1' in o: subprocess.run(['rm', '-rf', rd]); return t
    subprocess.run(['rm', '-rf', rd]); return None

def meet_path(rdir, ball, a, tmin=0):
    La = os.path.join(rdir, 'L_%04d.bin' % a)
    for t in range(tmin, 10):
        q = run([BIN, 'intersect', La, os.path.join(ball, 'L_%04d.bin' % t)])
        if q.startswith('first'):
            key = q.split()[1]
            return t, moves_to(rdir, key), moves_to(ball, key)
    return None

def verified_line(route):
    v = core.verify(CH, route, 'ac-r2-v1', man['limits'])
    return v

def write_line(route, note):
    v = verified_line(route)
    Sx = replay(S0, route)
    rec = {'id': ROW, 'ac': route, 'length': len(route), 'peak': max(tot(s) for s in Sx), 'verify': v, 'note': note}
    with open(os.path.join(ART, 'lines.jsonl'), 'a') as f: f.write(json.dumps({'id': ROW, 'ac': route}) + '\n')
    with open(os.path.join(ART, 'lines.txt'), 'a') as f: f.write('%s: %s\n' % (ROW, json.dumps(route)))
    return rec

def lane(kind):
    out = os.path.join(ART, 'lane_%s.json' % kind); recs = []
    res = {'lane': kind, 'cap': K, 'maxst': MAXST, 'maxL': MAXL, 'start_epoch': time.time(), 'searches': [], 'certified_upto': 0,
           'shortened': None, 'ended_by': None}
    def save():
        res['wall_s'] = round(time.time() - res['start_epoch'], 1)
        json.dump(res, open(out, 'w'), indent=1)
    if kind == 'head':
        hb = os.path.join(WORK, 'headball')
        if not os.path.exists(os.path.join(hb, 'L_0009.bin')):
            subprocess.run(['rm', '-rf', hb])
            run([BIN, 'bfs', hb, st(S0), str(K), '--mem', MEM, '--notarget', '--maxlayer', '9', '--minfree', '4'])
        hu = os.path.join(hb, 'union.bin'); run([BIN, 'union', hb, hu]); meet = hu; ball = hb
        res['ball'] = {'dir': 'work/headball', 'layers_0_9_total': sum(os.path.getsize(os.path.join(hb, 'L_%04d.bin' % t)) // 16 for t in range(10)), 'meet': 'union of layers 0..9'}
        rootstate = lambda L: S[L]
    else:
        ball = os.path.join(WORK, 'B%d' % K)
        assert os.path.exists(os.path.join(ball, 'L_0009.bin')), 'trivial ball not built'
        meet = os.path.join(ball, 'L_0009.bin')
        res['ball'] = {'dir': 'work/B%d' % K, 'layers_0_9_total': sum(os.path.getsize(os.path.join(ball, 'L_%04d.bin' % t)) // 16 for t in range(10)), 'meet': 'layer 9 only'}
        rootstate = lambda L: S[N - L]
    save()
    # L <= 10: root membership in the ball (d <= 9)
    for L in range(1, MAXL + 1):
        stop_check(); heartbeat()
        s = rootstate(L)
        if tot(s) > K: res['ended_by'] = 'root above cap at L=%d' % L; break
        ent = {'L': L, 'root': st(s), 'root_total': tot(s)}
        t = root_depth_in_ball(st(s), ball, kind)
        ent['root_in_ball_depth'] = t
        if t is not None and t < L:
            ent['result'] = 'SHORTENED (d=%d < %d)' % (t, L); res['searches'].append(ent)
            # rebuild the route from the ball path
            if kind == 'head':
                bw = moves_to(ball, st(s)); new = bw + ROUTE[L:]
            else:
                bw = moves_to(ball, st(s)); tl = [INV[m] for m in reversed(bw)]; new = ROUTE[:N - L] + tl
            res['shortened'] = write_line(new, 'root-in-ball shortening L=%d' % L); res['ended_by'] = 'shortened'; save(); return res
        if L <= 10:
            ent['result'] = 'checked by root membership only (d > 9 or d >= L)'; res['searches'].append(ent)
            res['certified_upto'] = L if t is None or t >= L else res['certified_upto']
            save(); continue
        if time.time() > DEADLINE: res['ended_by'] = 'global deadline before L=%d' % L; break
        r = search('%s_L%d' % (kind, L), st(s), K, meet, L - 10)
        ent.update(r); res['searches'].append(ent); save()
        if r['result'] == 'MEET':
            rdir = os.path.join(WORK, r['tag'])
            tm, fw, bw = meet_path(rdir, ball, r['meet_layer'])
            if kind == 'head': seg = bw + [INV[m] for m in reversed(fw)]; new = seg + ROUTE[L:]
            else: seg = fw + [INV[m] for m in reversed(bw)]; new = ROUTE[:N - L] + seg
            ent['meet_ball_depth'] = tm; ent['segment_len'] = len(seg)
            subprocess.run(['rm', '-rf', rdir])
            if len(seg) < L:
                res['shortened'] = write_line(new, '%s L=%d cap %d segment %d -> %d' % (kind, L, K, L, len(seg)))
                res['ended_by'] = 'shortened'; save(); return res
            ent['note'] = 'meet with segment not shorter (%d >= %d)' % (len(seg), L)
            res['ended_by'] = 'meet without shortening at L=%d (unexpected)' % L; save(); break
        if r['result'] in ('MAXLAYER', 'CLOSED'):
            res['certified_upto'] = L
            continue
        res['ended_by'] = '%s at L=%d: %s' % (r['result'], L, r.get('reason', '')); break
    else:
        res['ended_by'] = 'finished L<=%d' % MAXL
    res.setdefault('ended_by', 'finished')
    save(); return res

def windows():
    out = os.path.join(ART, 'lane_windows.json'); t0 = time.time()
    wd = os.path.join(WORK, 'win'); subprocess.run(['rm', '-rf', wd]); os.makedirs(wd)
    args = [WINBIN, wd, str(len(S0[0])), *[str(ENC[x]) for x in S0[0]], str(len(S0[1])), *[str(ENC[x]) for x in S0[1]], str(N), *map(str, ROUTE)]
    p = subprocess.Popen(['nice', '-n', '10'] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    reason = None
    while p.poll() is None:
        time.sleep(2); heartbeat()
        if os.path.exists(STOPF): reason = 'STOP file'
        elif time.time() > DEADLINE: reason = 'global deadline'
        elif freegb() < 2.0: reason = 'disk low'
        if reason: p.kill(); p.wait(); break
    o = p.stdout.read(); e = p.stderr.read()
    open(os.path.join(ART, 'windows_acc_window.log'), 'w').write(o + '\n--stderr--\n' + e)
    rec = {'lane': 'windows', 'tool': 'acc_window (uncapped, all pairs <= 14 apart, plus repeated states)', 'cap_implied': 'uncapped >= 37', 'rc': p.returncode,
           'wall_s': round(time.time() - t0, 1), 'aborted': reason, 'shortcuts': re.findall(r'pass \d+: d\(s_\d+,s_\d+\)=\d+ < \d+', o),
           'final_path': None}
    m = re.search(r'FINALPATH ?([\d ]*)', o)
    if m and m.group(1).strip():
        fp = list(map(int, m.group(1).split())); rec['final_path'] = fp
        if len(fp) < N: rec['shortened'] = write_line(fp, 'acc_window uncapped')
    rec['tail_of_log'] = o.strip().splitlines()[-8:]
    json.dump(rec, open(out, 'w'), indent=1)
    return rec

def control():
    """mechanism controls: from s_13 (head) / s_22 (tail) the route has length 13 = L; a search to depth 4 (one more than
    the L=13 certificate, which needs depth 3) must MEET at layer 4 with segment length exactly 13 (= 4 + 9)."""
    out = os.path.join(ART, 'lane_control.json'); res = {'lane': 'control', 'cap': K, 'checks': []}
    hb = os.path.join(WORK, 'headball')
    if not os.path.exists(os.path.join(hb, 'L_0009.bin')):
        run([BIN, 'bfs', hb, st(S0), str(K), '--mem', MEM, '--notarget', '--maxlayer', '9', '--minfree', '4'])
    hu = os.path.join(hb, 'union.bin')
    if not os.path.exists(hu): run([BIN, 'union', hb, hu])
    ball = os.path.join(WORK, 'B%d' % K)
    # head control: s_13 <- s_0 (head route length 13), depth 4 with union and with layer 9 only
    for kind, s, meet, bdir, L in (('head_union', S[13], hu, hb, 13), ('head_L9', S[13], os.path.join(hb, 'L_0009.bin'), hb, 13),
                                   ('tail_L9', S[N - 13], os.path.join(ball, 'L_0009.bin'), ball, 13)):
        r = search('ctl_' + kind, st(s), K, meet, 4)
        ent = dict(r, kind=kind)
        if r['result'] == 'MEET':
            rdir = os.path.join(WORK, r['tag']); tm, fw, bw = meet_path(rdir, bdir, r['meet_layer'])
            if kind.startswith('head'): seg = bw + [INV[m] for m in reversed(fw)]; replay_ok = replay(S0, seg)[-1] == S[13]
            else: seg = fw + [INV[m] for m in reversed(bw)]; replay_ok = replay(S[N - 13], seg)[-1] == ((1,), (2,))
            ent.update(meet_ball_depth=tm, segment_len=len(seg), segment_replays=replay_ok, expected_len=L)
            subprocess.run(['rm', '-rf', rdir])
        res['checks'].append(ent); json.dump(res, open(out, 'w'), indent=1)
    return res

def windows_cap():
    """Independent exact capped window check (cap K): radius-5 balls B_5(s_i) under cap K (acc_disk layers, exact distances),
    then for every pair i<j, j-i <= 11 (W), a connection of length d <= j-i-1 <= 10 exists iff some state m has
    dist_i(m) + dist_j(m) <= j-i-1 with both distances <= 5.  Also flags pairs whose balls contain each other's state."""
    out = os.path.join(ART, 'lane_windows_cap%d.json' % K); t0 = time.time(); W = 11
    balls = []; sizes = []
    for i in range(N + 1):
        stop_check(); heartbeat()
        d = os.path.join(WORK, 'wb'); subprocess.run(['rm', '-rf', d])
        run(['nice', '-n', '10', BIN, 'bfs', d, st(S[i]), str(K), '--mem', '500', '--notarget', '--maxlayer', '5', '--minfree', '4'])
        dist = {}
        for t in range(6):
            b = open(os.path.join(d, 'L_%04d.bin' % t), 'rb').read()
            for o in range(0, len(b), 16): dist[b[o:o + 16]] = t
        balls.append(dist); sizes.append(len(dist))
    subprocess.run(['rm', '-rf', os.path.join(WORK, 'wb')])
    pairs = []; shortcuts = []
    for i in range(N + 1):
        for j in range(i + 1, min(N, i + W) + 1):
            gap = j - i; A, B = balls[i], balls[j]
            if len(A) > len(B): A, B = B, A
            best = 99
            for k, da in A.items():
                db = B.get(k)
                if db is not None and da + db < best: best = da + db
            pairs.append((i, j, gap, best))
            if best < gap: shortcuts.append({'i': i, 'j': j, 'gap': gap, 'dist_upper': best})
    rec = {'lane': 'windows_cap%d' % K, 'cap': K, 'W': W, 'method': 'exact radius-5 balls under cap, pairs j-i <= 11', 'ball_sizes': sizes,
           'pairs_checked': len(pairs), 'shortcuts': shortcuts, 'wall_s': round(time.time() - t0, 1),
           'control_pairs_gap_le_10': sum(1 for (_, _, g, b) in pairs if g <= 10), 'control_pairs_gap_le_10_with_dist_eq_gap': sum(1 for (_, _, g, b) in pairs if g <= 10 and b == g), 'verdict': 'shortcut' if shortcuts else 'certified: no window <= %d shortens the route under cap %d' % (W, K)}
    json.dump(rec, open(out, 'w'), indent=1)
    return rec

def _main():
    kind = sys.argv[1]; os.makedirs(WORK, exist_ok=True); heartbeat(True)
    r = {'head': lambda: lane('head'), 'tail': lambda: lane('tail'), 'windows': windows, 'control': control, 'windows_cap': windows_cap}[kind]()
    print(json.dumps({k: v for k, v in r.items() if k not in ('searches', 'checks')}, indent=1))


if __name__ == '__main__':
    _main()
