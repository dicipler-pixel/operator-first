# SCRIPT: CHARLIE_SURGERY -- exact local surgery on a held route (AC or Stable, either finish), official verifiers.
# A route s_0 -> s_n (s_n = ((x),(y)) or ((y),(x))) is shortened in three exact ways, repeated until nothing changes:
#   WINDOWS: every stretch s_i..s_j with j - i <= W: bidirectional in-memory BFS (official apply_move) under cap K,
#            covers every connection shorter than j - i; a shorter one is spliced in.
#   TAILS:   s_{n-L} -> end. acc_disk searches forward from s_{n-L} (relators swapped when the end is (y,x), a symmetry
#            of the move set) to depth L-1-9 and meets B36 (all states within 9 moves of ((x),(y)) under cap 36).
#            First meet layer a + smallest ball depth t = exact shortest tail under cap min(K, 36). No meet = certified.
#   HEADS (the opposite end): a radius-9 ball H around s_0 under cap K is built once; acc_disk searches from s_L to
#            depth L-1-9 and meets H. Same argument: exact shortest s_0 -> s_L under cap K.
# Depth >= 1 is required (acc_disk checks the meet set on generated layers only). Each search is stopped at MAXST
# states; the largest L reached with no shortening is recorded as the certified local optimality of that end.
# Output: the final route, the finished line (ac: route; sac: route + [16,15] at (x,y), + [15,15] at (y,x)) replayed
# by the official ac-r2-v1 / sac-r8-v1 verifier, and a record per route in runs/charlie_surgery.jsonl.
# Usage: python3 surgery.py BUNDLE_FILE [first_line last_line]
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import charlie_run as cr
sys.path.insert(0, cr.SAIR)
from verifier import stable_core
from sac_yx import swap_move
from window import shorten as win_shorten
BIN = cr.BIN; BALL = os.path.join(HERE, 'runs', 'B36'); UNION = os.path.join(BALL, 'union9.bin')
WORK = os.path.join(HERE, 'runs', os.environ.get('SURG_WORK', 'surg')); os.makedirs(WORK, exist_ok=True)
OUT = os.path.join(HERE, 'runs', 'charlie_surgery.jsonl'); INB = os.path.join(HERE, 'runs', 'surgery_inbox'); os.makedirs(INB, exist_ok=True)
MANI = json.load(open(os.path.join(cr.SAIR, 'verifier/data/manifest.json')))
W = int(os.environ.get('W', '11')); MAXST = int(os.environ.get('MAXST', '120000000')); MEM = os.environ.get('MEM', '2500')
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
def st(s): return ''.join(L[a] for a in s[0]) + ',' + ''.join(L[a] for a in s[1])
def tot(s): return len(s[0]) + len(s[1])
def replay(s0, p):
    S = [s0]
    for m in p: S.append(cr.core.apply_move(S[-1], m))
    return S
END = {'x,y': ((1,), (2,)), 'y,x': ((2,), (1,))}

def bfs(rdir, start, cap, meet, maxlayer):
    subprocess.run(['rm', '-rf', rdir])
    o = cr.run([BIN, 'bfs', rdir, start, str(cap), '--mem', MEM, '--meet', meet, '--maxlayer', str(maxlayer), '--minfree', '4', '--notarget'])
    res = [l for l in o.splitlines() if l.startswith('RESULT')][-1]
    return res, int(res.split('states=')[1].split()[0])

def meet_path(rdir, ball, res, maxt=9):
    """moves rdir-root -> key, moves ball-root -> key, for the first ball depth t that meets layer a"""
    a = int(res.split('layer=')[1].split()[0]); La = os.path.join(rdir, 'L_%04d.bin' % a)
    for t in range(maxt + 1):
        q = cr.run([BIN, 'intersect', La, os.path.join(ball, 'L_%04d.bin' % t)])
        if q.startswith('first'):
            key = q.split()[1]
            return cr.moves_to(rdir, key), cr.moves_to(ball, key)
    return None

def tails(s0, route, end, K, log):
    """try tails L = 11.. ; return (new_route or None, certified_L)"""
    S = replay(s0, route); n = len(route); cert = 0; Kt = min(K, 36)
    for Lt in range(11, n + 1):
        s = S[n - Lt]
        if tot(s) > Kt: break
        root = (s[1], s[0]) if end == 'y,x' else s
        rdir = os.path.join(WORK, 'tail'); res, ns = bfs(rdir, st(root), Kt, UNION, Lt - 10)
        if 'MEET' in res:
            fw, bw = meet_path(rdir, BALL, res); tl = fw + [cr.INV[m] for m in reversed(bw)]
            if end == 'y,x': tl = [swap_move(m) for m in tl]
            subprocess.run(['rm', '-rf', rdir])
            if len(tl) < Lt:
                log('  tail from %d: %d -> %d (cap %d, %d states)' % (n - Lt, Lt, len(tl), Kt, ns))
                return route[:n - Lt] + tl, cert
        subprocess.run(['rm', '-rf', rdir])
        if 'MAXLAYER' in res or 'CLOSED' in res: cert = Lt
        else: break
        if ns > MAXST: break
    return None, cert

def heads(s0, route, K, log):
    S = replay(s0, route); n = len(route); cert = 0
    hb = os.path.join(WORK, 'headball'); subprocess.run(['rm', '-rf', hb])
    cr.run([BIN, 'bfs', hb, st(s0), str(K), '--mem', MEM, '--notarget', '--maxlayer', '9', '--minfree', '4'])
    hu = os.path.join(hb, 'union.bin'); cr.run([BIN, 'union', hb, hu])
    try:
        for Lh in range(11, n + 1):
            s = S[Lh]
            if tot(s) > K: break
            rdir = os.path.join(WORK, 'head'); res, ns = bfs(rdir, st(s), K, hu, Lh - 10)
            if 'MEET' in res:
                fw, bw = meet_path(rdir, hb, res)      # fw: s_L -> key ; bw: s_0 -> key
                hd = bw + [cr.INV[m] for m in reversed(fw)]
                subprocess.run(['rm', '-rf', rdir])
                if len(hd) < Lh:
                    log('  head to %d: %d -> %d (cap %d, %d states)' % (Lh, Lh, len(hd), K, ns))
                    return hd + route[Lh:], cert
            subprocess.run(['rm', '-rf', rdir])
            if 'MAXLAYER' in res or 'CLOSED' in res: cert = Lh
            else: break
            if ns > MAXST: break
    finally:
        subprocess.run(['rm', '-rf', hb])
    return None, cert

def finish(cid, side, end, route):
    if side == 'AC':
        c, lim = cr.load_row(cid); v = cr.core.verify(c, route, 'ac-r2-v1', lim); return cid, route, v.get('ok')
    sid = 'sac-' + cid[3:]; sc = [z for z in MANI['challenges'] if z['challenge_id'] == sid][0]
    p = route + ([16, 15] if end == 'x,y' else [15, 15]); v = stable_core.verify(sc, p, 'sac-r8-v1', MANI['limits'])
    return sid, p, v.get('ok')

def one(parts, log=print):
    cid, side, end, have, target, k, r0, r1, hx = parts[:9]
    route = [int(ch, 16) for ch in hx]; c, _ = cr.load_row(cid); s0 = tuple(map(tuple, c['initial_relators']))
    assert st(s0) == r0 + ',' + r1, 'relators differ from manifest'
    S = replay(s0, route); assert S[-1] == END[end], 'route does not reach its stated end'
    assert len(route) == int(have)
    peak = max(tot(s) for s in S); K = peak + 2; t0 = time.time()
    rec = {'row': cid, 'side': side, 'ends': end, 'have': int(have), 'target': int(target), 'k': int(k), 'peak': peak, 'cap': K, 'W': W}
    log('%s %s %s have %s target %s k %s peak %d' % (cid, side, end, have, target, k, peak))
    steps = []; tc = hc = 0
    while True:
        new = win_shorten(s0, route, K, W, log=lambda m: (steps.append('window ' + m), log('  window ' + m)))
        if len(new) < len(route): route = new; continue
        new, tc = tails(s0, route, end, K, log)
        if new: steps.append('tail %d' % (len(route) - len(new))); route = new; continue
        new, hc = heads(s0, route, K, log)
        if new: steps.append('head %d' % (len(route) - len(new))); route = new; continue
        break
    assert replay(s0, route)[-1] == END[end]
    rid, line, ok = finish(cid, side, end, route)
    rec.update(final=len(route), steps=steps, windows_certified_upto=W, tail_certified_upto=tc, head_certified_upto=hc,
               route=route, verifier_ok=ok, secs=round(time.time() - t0, 1),
               verdict=('TIE' if len(route) == int(target) else 'BEAT' if len(route) < int(target) else
                        ('IMPROVED' if len(route) < int(have) else 'LOCALLY OPTIMAL')))
    if ok and len(route) <= int(target):
        rec['line'] = '%s: %s' % (rid, json.dumps(line))
        open(os.path.join(INB, '%s_charlie_%s.txt' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()), rid)), 'w').write(rec['line'] + '\n')
    elif ok and len(route) < int(have):
        rec['improved_line'] = '%s: %s' % (rid, json.dumps(line))
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
    log('  => %s final %d (target %s) windows<=%d tails<=%d heads<=%d verifier %s (%.0fs)' % (rec['verdict'], len(route), target, W, tc, hc, ok, rec['secs']))
    if rec.get('line'): log(rec['line'])
    return rec

if __name__ == '__main__':
    lines = [l.split() for l in open(sys.argv[1]) if l.startswith('ac-')]
    a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, len(lines))
    cache = {}
    for i, parts in enumerate(lines, 1):
        if not (a <= i <= b) or parts[9] == 'CHARLIE_DONE': continue
        key = (parts[0], parts[2], parts[8])
        try:
            if key in cache:       # same route, same end, other side: reuse the surgery, finish and verify for this side
                prev = cache[key]; rid, line, ok = finish(parts[0], parts[1], parts[2], prev['route'])
                rec = dict(prev, side=parts[1], target=int(parts[4]), k=int(parts[5]), verifier_ok=ok, reused_from=prev['side'])
                rec.pop('line', None); rec.pop('improved_line', None)
                fin = len(prev['route']); tg = int(parts[4])
                rec['verdict'] = 'TIE' if fin == tg else 'BEAT' if fin < tg else ('IMPROVED' if fin < int(parts[3]) else 'LOCALLY OPTIMAL')
                if ok and fin <= tg:
                    rec['line'] = '%s: %s' % (rid, json.dumps(line))
                    open(os.path.join(INB, '%s_charlie_%s.txt' % (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()), rid)), 'w').write(rec['line'] + '\n')
                elif ok and fin < int(parts[3]): rec['improved_line'] = '%s: %s' % (rid, json.dumps(line))
                with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
                print('%s %s (same route as the %s line) => %s final %d target %s verifier %s' % (parts[0], parts[1], prev['side'], rec['verdict'], fin, tg, ok), flush=True)
                if rec.get('line'): print(rec['line'], flush=True)
                continue
            cache[key] = one(parts, log=lambda m: print(m, flush=True))
        except (SystemExit, AssertionError) as e:
            subprocess.run('rm -rf %s/*' % WORK, shell=True)
            print(i, parts[0], parts[1], 'FAILED:', str(e)[:200], flush=True)
            with open(OUT, 'a') as f: f.write(json.dumps({'row': parts[0], 'side': parts[1], 'status': 'FAILED', 'detail': str(e)[:300]}) + '\n')
