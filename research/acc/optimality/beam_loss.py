#!/usr/bin/env python3
"""Beam-loss diagnostic (atlas B20 + Plate XI: "is the road lost among ties, ranked wrong, or just short of width?").

Given a row and a known AC path (usually of record length), replay the path, write the fingerprints of its states
(same 128-bit fp() as acc_opt.c / acc_beam.c) to a trace file, and run acc_beam with BEAM_TRACE_FILE on each arm.
The beam prints one TRACE line per traced state per depth where that state is a candidate: rank in the sorted
candidate list, the tie block of its key without the fingerprint bits, the cut keys at k1 = W*DIV and at W, and
whether it survived the selection. From those lines this script reports, per arm:
  * how far the beam kept the path on time (state i kept at depth <= i), and whether it reached index N-R
    (R = finish-table radius; a generated state at that index is a table hit, so the beam then finds <= N);
  * the first state it dropped: depth, rank vs W and k1, tie block, key fields vs the cut, and a verdict:
      ties     - the state's key (fingerprint bits excluded) equals the key at the deterministic cut k1:
                 only the fingerprint tie-break dropped it;
      width    - rank < 2*k1: a beam about twice as wide would have kept it deterministically;
      ranked   - rank >= 2*k1: the key ranks it far down (factor rank/k1 reported);
      quota    - (BEAM_QUOTA arms) its class was already full; for admitted states width/ranked use the admitted position.
  decided_by names the first key field (P2, WH, comm_len, P1m, klen/hprio, else the fingerprint) where it differs from the cut.
Paths come from research/acc/live/queue/sent/*.txt, ACC_SUBMIT_API_*.txt (repo root) and
research/acc/live/ledger/crossrow_roads_ac_20260928.json (shortest path that replays to the target), or --path.

usage: beam_loss.py ROW [ROW ...] [--path "m m m ..."] [--arms H,P2=2] [--W 20000] [--depth-add 6]
                    [--bin ACC_BEAM] [--table T8.tab] [--radius 8] [--manifest M] [--timeout 1200] [--out OUT.json]
One beam at a time, nice -n 5; a run past --timeout is killed by PID and recorded as a timeout.
"""
import argparse, glob, json, os, re, subprocess, sys, tempfile, time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SCR = os.environ.get('ACC_SCRATCH', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
E = {1: 0, -1: 1, 2: 2, -2: 3}
ARMS = {'H': {}, 'P2=2': {'BEAM_P2': '2'}, 'P2=1': {'BEAM_P2': '1'},
        'P2=2+Q4': {'BEAM_P2': '2', 'BEAM_QUOTA': '4'}, 'P2=2+Q16': {'BEAM_P2': '2', 'BEAM_QUOTA': '16'},
        'P2=2+WH': {'BEAM_P2': '2', 'BEAM_WH': '1'}, 'P2=3': {'BEAM_P2': '3'}, 'P2=3+Q16': {'BEAM_P2': '3', 'BEAM_QUOTA': '16'}}
BASE = {'BEAM_H': '1', 'BEAM_DIV': '0.8'}
M64 = (1 << 64) - 1


# ---- kernel port (acc_opt.c apply: letters 0=x 1=X 2=y 3=Y, inverse = c^1) ----
def push(o, c):
    if o and o[-1] == c ^ 1: o.pop()
    else: o.append(c)


def apply(s, m):
    r = [list(s[0]), list(s[1])]
    if m in (0, 1):
        r[m] = [c ^ 1 for c in reversed(s[m])]; return r
    if m <= 5:
        j = 0 if m <= 3 else 1; k = 1 - j; o = list(s[j])   # s[j] is freely reduced
        b = s[k] if m in (2, 4) else [c ^ 1 for c in reversed(s[k])]
        for c in b: push(o, c)
        r[j] = o; return r
    j = 0 if m <= 9 else 1; g = (m - 6) & 3; o = []
    push(o, g)
    for c in s[j]: push(o, c)
    push(o, g ^ 1); r[j] = o; return r


# ---- fp() port (acc_opt.c) ----
def _fa(x):
    x ^= x >> 30; x = (x * 0xbf58476d1ce4e5b9) & M64; x ^= x >> 27; x = (x * 0x94d049bb133111eb) & M64; return x ^ (x >> 31)


def _fb(x):
    x ^= x >> 33; x = (x * 0xff51afd7ed558ccd) & M64; x ^= x >> 33; x = (x * 0xc4ceb9fe1a85ec53) & M64; return x ^ (x >> 33)


def fp(s):
    l0, l1 = len(s[0]), len(s[1])
    h1 = 0x243F6A8885A308D3 ^ ((l0 * 0x9E3779B97F4A7C15) & M64) ^ ((l1 << 40) & M64)
    h2 = (0x13198A2E03707344 + ((l1 * 0xC2B2AE3D27D4EB4F) & M64) + ((l0 << 44) & M64)) & M64
    idx = 0
    for w in s:
        for i in range(0, len(w), 32):
            c = 0
            for t, x in enumerate(w[i:i + 32]): c |= x << (2 * t)
            idx += 1
            h1 = _fa(h1 ^ c ^ ((idx * 0xD6E8FEB86659FD93) & M64))
            y = h2 ^ _fb((c * 0x9FB21C651E98DF25 + idx) & M64)
            y = ((y << 29) | (y >> 35)) & M64
            h2 = (y * 0x87C37B91114253D5 + 0x52DCE729) & M64
    h1 = _fa(h1 ^ 0xA0761D6478BD642F); h2 = _fb(h2 ^ idx)
    return h1 | 1, h2 & ~0xF & M64


# ---- paths ----
def load_challenges(man):
    return {c['challenge_id']: c for c in json.load(open(man))['challenges']}


def replay(ch, path):
    r0, r1 = ch['initial_relators']; s = [[E[t] for t in r0], [E[t] for t in r1]]; st = [s]
    for m in path:
        if not 0 <= m <= 13: return None
        s = apply(s, m); st.append(s)
    tgt = [[E[t] for t in r] for r in ch['target_relators']]
    return st if s == tgt else None


def find_paths(row):
    """All AC paths for row in the sent queue, root submission files and the cross-row roads ledger."""
    out = []
    files = sorted(glob.glob(os.path.join(REPO, 'research/acc/live/queue/sent/*.txt'))) + \
        sorted(glob.glob(os.path.join(REPO, 'ACC_SUBMIT_API_*.txt')))
    pat = re.compile(r'^\s*%s:\s*(\[[\d,\s]*\])' % re.escape(row))
    for fn in files:
        for line in open(fn, errors='replace'):
            m = pat.match(line)
            if m: out.append((json.loads(m.group(1)), os.path.relpath(fn, REPO)))
    roads = os.path.join(REPO, 'research/acc/live/ledger/crossrow_roads_ac_20260928.json')
    if os.path.exists(roads):
        for x in json.load(open(roads)):
            if x.get('id') == row and x.get('ac'): out.append((x['ac'], os.path.relpath(roads, REPO)))
    return out


# ---- beam ----
def enc(r0, r1): return [str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1]]


def run_beam(binary, table, ch, W, D, env_extra, trace_file, timeout):
    r0, r1 = ch['initial_relators']
    env = {k: v for k, v in os.environ.items() if not k.startswith('BEAM_')}
    env.update(BASE); env.update(env_extra); env['BEAM_TRACE_FILE'] = trace_file
    cmd = ['nice', '-n', '5', binary, table, str(W), str(D), *enc(r0, r1)]
    t0 = time.time(); p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    try:
        out, err = p.communicate(timeout=timeout); to = False
    except subprocess.TimeoutExpired:
        p.kill(); out, err = p.communicate(); to = True          # Popen.kill signals this PID only
    res = {'wall_s': round(time.time() - t0, 1), 'timeout': to, 'rc': p.returncode}
    for kind in ('AC', 'SAC'):
        m = re.search(r'^%s (\d+) PATH ([\d ]+)' % kind, out, re.M)
        res[kind.lower() + '_len'] = int(m.group(1)) if m else None
        res[kind.lower()] = list(map(int, m.group(2).split())) if m else None
    return res, err


def decode(key, env):
    """Ranking fields of a beam key (layouts in acc_beam.c)."""
    p2, wh = int(env.get('BEAM_P2', '0')), env.get('BEAM_WH', '0') == '1'
    if p2 == 0:
        d = {'klen': key >> 40}
        if wh: d['wh'] = (key >> 30) & 1023
    elif p2 == 2:
        d = {'p2': key >> 55, 'klen': (key >> 27) & 0x3FFFF}
        if wh: d['wh'] = (key >> 45) & 1023
    elif p2 == 3:
        d = {'p2': key >> 55, 'comm': (key >> 45) & 1023, 'p1m': (key >> 35) & 1023, 'klen': (key >> 17) & 0x3FFFF}
    else:
        d = {'p2': key >> 55}
        if wh: d.update(wh=(key >> 45) & 1023, p1m=(key >> 35) & 1023, klen=(key >> 17) & 0x3FFFF)
        else: d.update(p1m=(key >> 45) & 1023, klen=(key >> 27) & 0x3FFFF)
    if env.get('BEAM_H') == '1' and 'klen' in d: d['hprio'] = round(d['klen'] / 16.0, 2)
    return d


def parse_trace(err):
    start = re.search(r'trace: (\d+) states; start state is index (-?\d+)', err)
    recs, visited = [], []
    for line in err.splitlines():
        if not line.startswith('TRACE '): continue
        toks = line.split()[1:]
        kv = dict(t.split('=', 1) for t in toks if '=' in t)
        if 'visited' in toks: visited.append((int(kv['d']), int(kv['i']))); continue
        r = {k: (int(v, 16) if k in ('key', 'cutk1', 'cutW') else int(v)) for k, v in kv.items()}
        recs.append(r)
    return (int(start.group(1)), int(start.group(2))) if start else (None, None), recs, visited


def analyse(N, radius, recs, visited, env, W):
    need = max(N - radius - 1, 0)                   # states 1..need must be kept; generating state need+1 hits the table
    kept_at = {}
    for r in recs:
        if r['kept']: kept_at.setdefault(r['i'], r['d'])
    for d, i in visited: kept_at.setdefault(i, -1)   # visited = already kept at an earlier depth
    on_time = 0
    for i in range(1, need + 1):
        if i in kept_at and kept_at[i] <= i: on_time = i
        else: break
    chain = 0                                       # kept at any depth (the beam may follow the road late)
    for i in range(1, need + 1):
        if i in kept_at: chain = i
        else: break
    res = {'N': N, 'need_index': need, 'kept_on_time_through': on_time, 'kept_any_depth_through': chain,
           'reached_finish_zone': chain >= need,
           'late_states': sorted(i for i, d in kept_at.items() if d > i and i <= need)}
    if chain >= need: return res
    i = chain + 1
    cands = [r for r in recs if r['i'] == i]
    res['first_dropped_index'] = i
    if not cands:
        res['drop'] = {'verdict': 'never_candidate', 'note': 'state %d never generated as a candidate (parent state %d kept at depth %s)' % (i, i - 1, kept_at.get(i - 1))}
        return res
    # the drop that matters: the candidate record at the depth right after its parent was kept
    pd = kept_at.get(i - 1, 0) if i > 1 else 0
    r = next((c for c in cands if c['d'] == pd + 1), cands[0])
    k1 = r['k1'] if r['rank'] >= 0 else W
    drop = {'depth': r['d'], 'rank': r['rank'], 'nt': r['nt'], 'W': r['W'], 'k1': k1, 'tie_lo': r['tie_lo'], 'tie_hi': r['tie_hi'],
            'tie_count': r['tie_hi'] - r['tie_lo'] if r['rank'] >= 0 else None, 'table_dist': r['t'], 'len': r['len'],
            'fields': decode(r['key'], env), 'cut_k1_fields': decode(r['cutk1'], env), 'cut_W_fields': decode(r['cutW'], env)}
    if env.get('BEAM_QUOTA'): drop.update(admitted=r['adm'], quota_pos=r['qpos'])
    pos = r['qpos'] if env.get('BEAM_QUOTA') else r['rank']     # with a quota the selection runs over the admitted list
    if r['rank'] < 0: drop['verdict'] = 'dropped_without_sort'
    elif env.get('BEAM_QUOTA') and r['adm'] == 0: drop['verdict'] = 'quota'
    elif not env.get('BEAM_QUOTA') and r['tie_lo'] < k1 <= r['rank']: drop['verdict'] = 'ties'
    elif pos < 2 * k1: drop['verdict'] = 'width'
    else: drop['verdict'] = 'ranked'
    drop['rank_over_k1'] = round(pos / k1, 2) if k1 and pos >= 0 else None
    # first ranking field (in key order) where the state differs from the deterministic cut: what decided the drop
    f, c = drop['fields'], drop['cut_k1_fields']
    order = [k for k in ('p2', 'wh', 'comm', 'p1m', 'klen') if k in f]
    if 'wh' in f and 'p2' not in f: order = ['klen', 'wh']
    drop['decided_by'] = next((k for k in order if f[k] != c[k]), 'fingerprint')
    drop['other_depths'] = [{'d': c['d'], 'rank': c['rank'], 'kept': c['kept']} for c in cands if c is not r][:10]
    res['drop'] = drop
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rows', nargs='+')
    ap.add_argument('--path', help='explicit AC path (space- or comma-separated moves) for a single row')
    ap.add_argument('--arms', default='H,P2=2')
    ap.add_argument('--W', type=int, default=20000)
    ap.add_argument('--depth-add', type=int, default=6, help='depth cap = path length + this')
    ap.add_argument('--bin', default=os.path.join(SCR, 'acc_beam_x'))
    ap.add_argument('--table', default=os.path.join(SCR, 'p2beam/T8.tab'))
    ap.add_argument('--radius', type=int, default=8, help='finish-table radius (T8 = 8)')
    ap.add_argument('--manifest', default=os.path.join(SCR, 'sair/competition/tools/verifier/data/manifest.json'))
    ap.add_argument('--timeout', type=int, default=1200)
    ap.add_argument('--out', default=None)
    ap.add_argument('--keep-trace', action='store_true', help='store every TRACE record in the output')
    a = ap.parse_args()
    CH = load_challenges(a.manifest); results = []
    for row in a.rows:
        ch = CH[row]
        if a.path:
            cands = [(list(map(int, re.split(r'[,\s]+', a.path.strip(' []')))), 'cli')]
        else:
            cands = find_paths(row)
        good = [(p, src) for p, src in cands if replay(ch, p)]
        if not good:
            print(row, 'no replayable AC path found', file=sys.stderr); results.append({'row': row, 'error': 'no path'}); continue
        path, src = min(good, key=lambda x: len(x[0]))
        states = replay(ch, path); N = len(path)
        tf = tempfile.NamedTemporaryFile('w', suffix='.trace', delete=False)
        for i, s in enumerate(states):
            h1, h2 = fp(s); tf.write('%d %016x %016x\n' % (i, h1, h2))
        tf.close()
        entry = {'row': row, 'path_len': N, 'path_source': src, 'path': path,
                 'lengths_along_path': [len(s[0]) + len(s[1]) for s in states], 'arms': {}}
        for arm in a.arms.split(','):
            env = dict(BASE, **ARMS[arm])
            res, err = run_beam(a.bin, a.table, ch, a.W, N + a.depth_add, ARMS[arm], tf.name, a.timeout)
            (ntr, sidx), recs, visited = parse_trace(err)
            if sidx != 0: raise SystemExit('fingerprint port mismatch: start state index %s (trace %s states)' % (sidx, ntr))
            an = analyse(N, a.radius, recs, visited, env, a.W)
            an.update({k: res[k] for k in ('ac_len', 'sac_len', 'wall_s', 'timeout', 'rc')})
            an['env'] = env
            if a.keep_trace: an['trace'] = recs; an['visited'] = visited
            entry['arms'][arm] = an
            d = an.get('drop', {})
            print('%s %-9s beam AC %s%s | road N=%d need %d: on time through %d, any depth through %d | %s' % (
                row, arm, an['ac_len'], ' (timeout)' if an['timeout'] else '', N, an['need_index'], an['kept_on_time_through'],
                an['kept_any_depth_through'],
                'reached finish zone' if an['reached_finish_zone'] else 'drop i=%d d=%s rank %s/k1 %s ties [%s,%s) -> %s (by %s) %s vs cut %s' % (
                    an['first_dropped_index'], d.get('depth'), d.get('rank'), d.get('k1'), d.get('tie_lo'), d.get('tie_hi'),
                    d.get('verdict'), d.get('decided_by'), d.get('fields'), d.get('cut_k1_fields'))), flush=True)
        os.unlink(tf.name)
        results.append(entry)
    if a.out:
        json.dump(results, open(a.out, 'w'), indent=1)


if __name__ == '__main__':
    main()
