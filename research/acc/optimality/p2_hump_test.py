#!/usr/bin/env python3
"""P2 hump test (B31 hypothesis) + lead's E1 / U1 / C1 checks, 2026-09-28.

Hypothesis (atlas B31): conjugations only move a relator inside its conjugacy class; the
multiplications (moves 2-5) are the only class-changing moves.  So a potential that treats
cyclic rotations as free and counts only multiplications should stay flat over the humps of
shortest AC paths, where raw length climbs.

Definitions (rotations of both relators and relator inversion are free; words are handled by
their cyclic cores):
  P0cyc(s)  = |core r0| + |core r1|
  P_k(s)    = best total length after EXACTLY k multiplications r_i <- rot(r_i) * rot(r_j)^{+-1}
              (i != j).  Two variants of the length of the product just made:
                cyc  : cyclically reduced length
                free : plain free-reduced length of rot(r_i)*rot(r_j)^{+-1}
              the untouched relator always counts with its core length.
  P2 cut c  = level 1 cut to the c best distinct level-1 states (states canonical up to
              rotation, inversion and relator order) before expanding level 2; c = None = no cut.
  P1m(s)    = cheap approximation: stored r_i (not rotated) times a rotation of core(r_j)^{+-1},
              free length, plus |core r_j|.
Fact used for speed (checked against brute force in --selftest): over all rotation pairs the
best product length is |A|+|B|-2K, K = longest common cyclic subword of A and B^{-1}; the cyc
and free variants differ only when the shorter word is absorbed completely.

Sources: every ac path in root ACC_*.txt, research/acc/** and tools/acc/** (text lines
"ac-XXXXX: [...]", JSON fields ac/path/moves with an ac-XXXXX id; sac lines ending [16,15]
are converted by dropping the two stabilisation moves).  Each path is replayed with the
official verifier core (SAIR clone) and must end at (x, y).  One path per row: the shortest.

Primary set = rows whose best verified path equals the live board record (snapshot BOARD);
secondary = every verified row.  Also runs the lead's E1 / U1 / C1 checks on the same hump set.

usage: nice -n 10 python3 p2_hump_test.py [--sair DIR] [--out JSON] [--selftest] [--no-secondary] [--no-timing]
                                           [--c-bench C_BENCH_OUTPUT.txt]
"""
import argparse, glob, gzip, json, math, os, random, re, statistics, sys, time
from collections import Counter, defaultdict

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SAIR_DEFAULT = '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad/sair'
OUT_DEFAULT = os.path.join(REPO, 'research/acc/live/ledger/p2_hump_test_20260928.json')
BOARD = os.path.join(REPO, 'research/acc/live/boards/ac_20260928T0428Z.json.gz')

# ----------------------------------------------------------------------------- words (tuples)
GENS = (1, -1, 2, -2)


def free_reduce(w):
    o = []
    for a in w:
        if o and o[-1] == -a:
            o.pop()
        else:
            o.append(a)
    return tuple(o)


def invert(w):
    return tuple(-a for a in reversed(w))


def apply_move(state, m):
    """Local copy of verifier core.apply_move (ac-r2-v1); cross-checked on every replay."""
    r0, r1 = state
    if m == 0:
        return (invert(r0), r1)
    if m == 1:
        return (r0, invert(r1))
    if m == 2:
        return (free_reduce(r0 + r1), r1)
    if m == 3:
        return (free_reduce(r0 + invert(r1)), r1)
    if m == 4:
        return (r0, free_reduce(r1 + r0))
    if m == 5:
        return (r0, free_reduce(r1 + invert(r0)))
    if 6 <= m <= 9:
        g = GENS[m - 6]
        return (free_reduce((g,) + r0 + (-g,)), r1)
    if 10 <= m <= 13:
        g = GENS[m - 10]
        return (r0, free_reduce((g,) + r1 + (-g,)))
    raise ValueError(m)


# ----------------------------------------------------------------------------- words (strings)
LET = {1: 'a', -1: 'A', 2: 'b', -2: 'B'}


def enc(w):
    return ''.join(LET[a] for a in w)


def inv_s(s):
    return s[::-1].swapcase()


def cycred_s(s):
    i, j = 0, len(s)
    while j - i > 1 and s[i] == s[j - 1].swapcase():
        i += 1
        j -= 1
    return s[i:j]


def free_reduce_s(s):
    o = []
    for c in s:
        if o and o[-1] == c.swapcase():
            o.pop()
        else:
            o.append(c)
    return ''.join(o)


def canon(s):
    """Canonical cyclic word up to rotation and inversion (s cyclically reduced)."""
    n = len(s)
    if n == 0:
        return ''
    d = s + s
    best = min(d[i:i + n] for i in range(n))
    t = inv_s(s)
    d = t + t
    b2 = min(d[i:i + n] for i in range(n))
    return best if best <= b2 else b2


class Counters:
    pairs = 0       # rotation pairs whose junction overlap was computed
    words = 0       # product words built + canonicalised
    word_chars = 0
    lcs = 0         # longest-common-cyclic-subword calls
    lcs_cells = 0   # n*m cells an O(nm) DP would touch


CNT = Counters()


def lcs_cyc(A, B):
    """Longest common cyclic subword of cyclic words A and B, length <= min(|A|, |B|)."""
    n, m = len(A), len(B)
    CNT.lcs += 1
    CNT.lcs_cells += n * m
    if n == 0 or m == 0:
        return 0
    Ad, Bd = A + A, B + B
    lo, hi = 0, min(n, m)
    while lo < hi:
        k = (lo + hi + 1) // 2
        if any(Ad[i:i + k] in Bd for i in range(n)):
            lo = k
        else:
            hi = k - 1
    return lo


_P1 = {}


def p1_cores(A, B):
    """(P1cyc, P1free) of the state with cyclically reduced relators A, B (strings)."""
    key = (A, B) if A <= B else (B, A)
    r = _P1.get(key)
    if r is not None:
        return r
    n, m = len(A), len(B)
    s = min(n, m)
    kp, km = lcs_cyc(A, inv_s(B)), lcs_cyc(A, B)
    K = max(kp, km)
    free = n + m - 2 * K + s
    cyc = free
    if K == s:
        # absorption: the shorter word cancels completely, the remainder may reduce cyclically
        L, S = (A, B) if n >= m else (B, A)
        nl, ns = len(L), len(S)
        Ld = L + L
        for sgn, ks in ((1, kp), (-1, km)):
            if ks != s:
                continue
            T = inv_s(S) if sgn == 1 else S          # (S^sgn)^-1
            rots = {(T + T)[i:i + ns] for i in range(ns)}
            for t in range(nl):
                if Ld[t:t + ns] in rots:
                    rem = cycred_s(Ld[t + ns:t + nl])
                    if len(rem) + ns < cyc:
                        cyc = len(rem) + ns
    r = (cyc, free)
    _P1[key] = r
    return r


def level1(A, B, cut):
    """Distinct level-1 states after one multiplication.

    Returns (list for cyc variant, list for free variant), each sorted best-first and cut to
    `cut` (None = all); entries (total, key, coreX, coreY)."""
    combos = []
    for mod, oth in ((A, B), (B, A)):
        for sgn in (1, -1):
            C = oth if sgn == 1 else inv_s(oth)
            combos.append((mod, oth, C))
    buckets = defaultdict(list)
    absorb = []
    for ci, (mod, oth, C) in enumerate(combos):
        n, m = len(mod), len(C)
        if n == 0 or m == 0:
            continue
        lim = min(n, m)
        invC = C.swapcase()
        for p in range(n):
            for q in range(m):
                k = 0
                while k < lim and mod[(p - 1 - k) % n] == invC[(q + k) % m]:
                    k += 1
                CNT.pairs += 1
                ft = n + m - 2 * k + m
                if k == lim:
                    absorb.append((ft, ci, p, q, k))
                else:
                    buckets[ft].append((ci, p, q, k))
    states = {}
    canon_oth = {}

    def add(ft, ci, p, q, k):
        mod, oth, C = combos[ci]
        n, m = len(mod), len(C)
        w = (mod[p:] + mod[:p])[:n - k] + (C[q:] + C[:q])[k:]
        core = cycred_s(w)
        CNT.words += 1
        CNT.word_chars += len(w)
        co = canon_oth.get(ci)
        if co is None:
            co = canon_oth[ci] = canon(oth)
        cn = canon(core)
        key = (cn, co) if cn <= co else (co, cn)
        ct = len(core) + m
        e = states.get(key)
        if e is None:
            states[key] = [ct, ft, core, oth]
        else:
            if ct < e[0]:
                e[0] = ct
            if ft < e[1]:
                e[1] = ft

    for a in absorb:
        add(*a)
    for F in sorted(buckets):
        for (ci, p, q, k) in buckets[F]:
            add(F, ci, p, q, k)
        if cut is not None:
            nc = sum(1 for e in states.values() if e[0] <= F)
            nf = sum(1 for e in states.values() if e[1] <= F)
            if nc >= cut and nf >= cut:
                break
    cl = sorted((e[0], k_, e[2], e[3]) for k_, e in states.items())
    fl = sorted((e[1], k_, e[2], e[3]) for k_, e in states.items())
    if cut is not None:
        cl, fl = cl[:cut], fl[:cut]
    return cl, fl


_P2 = {}


def state_key(r0, r1):
    a, b = canon(cycred_s(enc(r0))), canon(cycred_s(enc(r1)))
    return (a, b) if a <= b else (b, a)


def p2(r0, r1, cut):
    """(P2cyc, P2free) with level-1 cut; memoised by state class (rotation/inversion/order)."""
    A, B = cycred_s(enc(r0)), cycred_s(enc(r1))
    ca, cb = canon(A), canon(B)
    key = ((ca, cb) if ca <= cb else (cb, ca), cut)
    r = _P2.get(key)
    if r is not None:
        return r
    cl, fl = level1(A, B, cut)
    pc = min(p1_cores(x, y)[0] for (_, _, x, y) in cl)
    pf = min(p1_cores(x, y)[1] for (_, _, x, y) in fl)
    r = (pc, pf)
    _P2[key] = r
    return r


def p1(r0, r1):
    return p1_cores(cycred_s(enc(r0)), cycred_s(enc(r1)))


def p1m(r0, r1):
    """Cheap approximation: stored r_i times rotation of core(r_j)^{+-1}; free length + |core r_j|."""
    best = None
    for R, O in ((enc(r0), enc(r1)), (enc(r1), enc(r0))):
        core = cycred_s(O)
        m, n = len(core), len(R)
        lim = min(n, m)
        for C in (core, inv_s(core)):
            invC = C.swapcase()
            for q in range(m):
                k = 0
                while k < lim and R[n - 1 - k] == invC[(q + k) % m]:
                    k += 1
                t = n + m - 2 * k + m
                if best is None or t < best:
                    best = t
    return best


# ----------------------------------------------------------------------------- brute force (selftest)
def rots(s):
    return [s[i:] + s[:i] for i in range(len(s))] or ['']


def brute_level(states):
    """All states after one multiplication from each (A, B) core pair; returns list of
    (coreA', coreB', cyc_total, free_total)."""
    out = []
    for A, B in states:
        for mod, oth, first in ((A, B, True), (B, A, False)):
            for C in (oth, inv_s(oth)):
                for a in rots(mod):
                    for c in rots(C):
                        w = free_reduce_s(a + c)
                        core = cycred_s(w)
                        ct, ft = len(core) + len(oth), len(w) + len(oth)
                        out.append(((core, oth) if first else (oth, core), ct, ft))
    return out


def brute_p1(A, B):
    L = brute_level([(A, B)])
    return min(x[1] for x in L), min(x[2] for x in L)


def brute_p2_nocut(A, B):
    L1 = brute_level([(A, B)])
    seen = {}
    for (x, y), ct, ft in L1:
        seen[(x, y)] = 1
    bc = bf = None
    for (x, y) in seen:
        c, f = brute_p1(x, y)
        bc = c if bc is None else min(bc, c)
        bf = f if bf is None else min(bf, f)
    return bc, bf


# ----------------------------------------------------------------------------- collection
TEXT_RE = re.compile(r'(?<![A-Za-z0-9_])(s?ac)-(\d{5})["\']?\s*:?\s*\[([\d,\s]*)\]')
ID_RE = re.compile(r'^ac-\d{5}$')
PATH_KEYS = ('ac', 'path', 'moves', 'ac_path', 'best_path')


def conv(kind, moves):
    """Return an AC move list or None."""
    if not moves or not all(isinstance(m, int) and not isinstance(m, bool) for m in moves):
        return None
    if kind == 'sac':
        if len(moves) >= 2 and moves[-2:] == [16, 15] and all(0 <= m <= 13 for m in moves[:-2]):
            return moves[:-2]
        return None
    if all(0 <= m <= 13 for m in moves):
        return moves
    return None


def walk_json(obj, cur, sink, src):
    if isinstance(obj, dict):
        for idk in ('id', 'row', 'challenge_id', 'challengeId', 'target'):
            v = obj.get(idk)
            if isinstance(v, str) and ID_RE.match(v):
                cur = v
                break
        for k, v in obj.items():
            if k in PATH_KEYS and cur and isinstance(v, list):
                mv = conv('ac', v)
                if mv:
                    sink.append((cur, mv, src))
            elif k == 'sac' and cur and isinstance(v, list):
                mv = conv('sac', v)
                if mv:
                    sink.append((cur, mv, src + '#sac'))
            elif isinstance(v, (dict, list)):
                walk_json(v, cur, sink, src)
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)):
                walk_json(v, cur, sink, src)


def source_files():
    pats = ['ACC_*.txt', 'research/acc/**/*.txt', 'research/acc/**/*.md', 'research/acc/**/*.json',
            'research/acc/**/*.jsonl', 'tools/acc/**/*.txt', 'tools/acc/**/*.md', 'tools/acc/**/*.json',
            'tools/acc/**/*.jsonl']
    out = []
    for p in pats:
        out += glob.glob(os.path.join(REPO, p), recursive=True)
    return sorted(set(out))


def collect():
    raw = []
    nfiles = 0
    for f in source_files():
        try:
            txt = open(f, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        rel = os.path.relpath(f, REPO)
        before = len(raw)
        for mt in TEXT_RE.finditer(txt):
            kind, num, body = mt.group(1), mt.group(2), mt.group(3)
            try:
                mv = [int(x) for x in body.replace(' ', '').split(',') if x != '']
            except ValueError:
                continue
            mv = conv(kind, mv)
            if mv:
                raw.append(('ac-' + num, mv, rel + ('#sac' if kind == 'sac' else '')))
        if f.endswith('.json') or f.endswith('.jsonl'):
            docs = []
            try:
                docs = [json.loads(txt)]
            except ValueError:
                for line in txt.splitlines():
                    line = line.strip()
                    if line.startswith('{') or line.startswith('['):
                        try:
                            docs.append(json.loads(line))
                        except ValueError:
                            pass
            for d in docs:
                walk_json(d, None, raw, rel)
        if len(raw) > before:
            nfiles += 1
    return raw, nfiles


def replay(init, moves, official):
    st = (tuple(init[0]), tuple(init[1]))
    states = [st]
    for m in moves:
        nx = apply_move(st, m)
        if official is not None:
            assert official.apply_move(st, m) == nx, 'move semantics mismatch'
        st = nx
        states.append(st)
    return states


# ----------------------------------------------------------------------------- stats helpers
def tot(s):
    return len(s[0]) + len(s[1])


def mid_rank(vals, idx):
    v = vals[idx]
    better = sum(1 for x in vals if x < v)
    ties = sum(1 for x in vals if x == v) - 1
    return 1 + better + ties / 2.0, 1 + better


def med(xs):
    return statistics.median(xs) if xs else None


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def rnd(x, d=3):
    return None if x is None else round(x, d)


def exp_matrix(st):
    return [[sum(1 for a in r if a == 1) - sum(1 for a in r if a == -1),
             sum(1 for a in r if a == 2) - sum(1 for a in r if a == -2)] for r in st]


def classify_T(Ms, Me):
    (a, b), (c, d) = Ms
    det = a * d - b * c
    assert det in (1, -1), 'exponent matrix not unimodular'
    inv = [[d * det, -b * det], [-c * det, a * det]]           # exact inverse since det = +-1
    T = [[Me[0][0] * inv[0][0] + Me[0][1] * inv[1][0], Me[0][0] * inv[0][1] + Me[0][1] * inv[1][1]],
         [Me[1][0] * inv[0][0] + Me[1][1] * inv[1][0], Me[1][0] * inv[0][1] + Me[1][1] * inv[1][1]]]
    dT = T[0][0] * T[1][1] - T[0][1] * T[1][0]
    if dT == -1:
        T = [[T[0][0] * T[0][0] + T[0][1] * T[1][0], T[0][0] * T[0][1] + T[0][1] * T[1][1]],
             [T[1][0] * T[0][0] + T[1][1] * T[1][0], T[1][0] * T[0][1] + T[1][1] * T[1][1]]]
    tr = T[0][0] + T[1][1]
    if T in ([[1, 0], [0, 1]], [[-1, 0], [0, -1]]):
        return 'pmI'
    if abs(tr) <= 1:
        return 'finite'
    if abs(tr) == 2:
        return 'parabolic'
    return 'hyperbolic'


def spread(rows, keyf, fallbacks):
    """Pooled within-bin SD (ANOVA residual, df N-G), eta^2, and leave-one-out MAE of the bin
    mean (singletons fall back to the next coarser key, then the global mean)."""
    y = [r['rem'] for r in rows]
    N = len(y)
    gm = sum(y) / N
    sst = sum((v - gm) ** 2 for v in y)
    groups = defaultdict(list)
    for r in rows:
        groups[keyf(r)].append(r['rem'])
    ssw = sum(sum((v - sum(g) / len(g)) ** 2 for v in g) for g in groups.values())
    G = len(groups)
    fb_groups = [defaultdict(list) for _ in fallbacks]
    for r in rows:
        for gi, f in enumerate(fallbacks):
            fb_groups[gi][f(r)].append(r['rem'])
    err = 0.0
    for r in rows:
        v = r['rem']
        pred = None
        for kf, gd in [(keyf, groups)] + list(zip(fallbacks, fb_groups)):
            g = gd[kf(r)]
            if len(g) > 1:
                pred = (sum(g) - v) / (len(g) - 1)
                break
        if pred is None:
            pred = (sum(y) - v) / (N - 1)
        err += abs(v - pred)
    return {'bins': G, 'pooled_sd': rnd(math.sqrt(ssw / max(1, N - G))), 'eta2': rnd(1 - ssw / sst),
            'loo_mae': rnd(err / N), 'total_sd': rnd(math.sqrt(sst / (N - 1)))}


# ----------------------------------------------------------------------------- main analysis
def load_official(sair):
    try:
        sys.path.insert(0, os.path.join(sair, 'competition', 'tools'))
        from verifier import core as official
        return official
    except Exception:
        return None


def selftest(paths, nstates=60, seed=7):
    """Check the fast P1 / P2(no cut) against brute force over all rotation pairs."""
    rng = random.Random(seed)
    pool = [s for p in paths for s in p['states'] if 2 < tot(s) <= 22]
    rng.shuffle(pool)
    nbad = 0
    for s in pool[:nstates]:
        A, B = cycred_s(enc(s[0])), cycred_s(enc(s[1]))
        if brute_p1(A, B) != p1_cores(A, B):
            nbad += 1
        if tot(s) <= 16 and brute_p2_nocut(A, B) != p2(s[0], s[1], None):
            nbad += 1
    return {'states_checked': min(nstates, len(pool)), 'mismatches': nbad}


def values(s, want):
    out = {}
    if 'raw' in want:
        out['raw'] = tot(s)
    if 'P0cyc' in want:
        out['P0cyc'] = len(cycred_s(enc(s[0]))) + len(cycred_s(enc(s[1])))
    if 'P1' in want or 'P1f' in want:
        out['P1'], out['P1f'] = p1(*s)
    if 'P1m' in want:
        out['P1m'] = p1m(*s)
    if 'P2c8' in want or 'P2f8' in want:
        out['P2c8'], out['P2f8'] = p2(s[0], s[1], 8)
    if 'P2c40' in want or 'P2f40' in want:
        out['P2c40'], out['P2f40'] = p2(s[0], s[1], 40)
    if 'P2c' in want or 'P2f' in want:
        out['P2c'], out['P2f'] = p2(s[0], s[1], None)
    return out

def collect_rows(official, man, board):
    """1-2. collect, replay, dedupe by row (shortest verified; ties -> lexicographically smallest)."""
    raw, nfiles = collect()
    distinct, bad, per_row = set(), [], {}
    for rid, mv, src in raw:
        k = (rid, tuple(mv))
        if k in distinct:
            continue
        distinct.add(k)
        if rid not in man:
            bad.append((rid, src, 'no manifest row'))
            continue
        states = replay(man[rid], mv, official)
        if states[-1] != ((1,), (2,)):
            bad.append((rid, src, 'not at (x,y)'))
            continue
        cur = per_row.get(rid)
        if cur is None or (len(mv), mv) < (len(cur['moves']), cur['moves']):
            per_row[rid] = {'row': rid, 'moves': mv, 'src': src, 'states': states}
    for p in per_row.values():
        p['record'] = board.get(p['row'])
        p['at_record'] = p['record'] is not None and len(p['moves']) <= p['record']
        p['raw'] = [tot(s) for s in p['states']]
    rows_all = sorted(per_row.values(), key=lambda p: p['row'])
    collection = {'raw_lines': len(raw), 'files_with_paths': nfiles, 'distinct_row_paths': len(distinct),
                  'replay_failures': len(bad), 'rows_verified': len(rows_all),
                  'rows_at_board_record': sum(1 for p in rows_all if p['at_record']),
                  'board_snapshot': os.path.relpath(BOARD, REPO), 'official_core_crosscheck': official is not None,
                  'note': 'session-1 163-path data file is not in the repo (only path_chart_163.svg); '
                          'the at-record set below supersedes it'}
    return rows_all, collection, bad


def rel(m):
    """U1: which relator a move changes."""
    return 0 if m in (0, 2, 3, 6, 7, 8, 9) else 1


def runs(ms):
    out, cur, n = [], None, 0
    for m in ms:
        r = rel(m)
        if r == cur:
            n += 1
        else:
            if n:
                out.append(n)
            cur, n = r, 1
    if n:
        out.append(n)
    return out


def run_stats(rl):
    if not rl:
        return None
    c = Counter(rl)
    mw = sorted(x for x in rl for _ in range(x))
    return {'runs': len(rl), 'median': med(rl), 'mean': rnd(mean(rl)), 'move_weighted_median': med(mw),
            'hist': {str(k): c[k] for k in sorted(c)}}


def segments(p):
    """Maximal hump excursions (a, b): total(s_a) <= start < total(s_a+1 .. s_b-1), total(s_b) <= start."""
    r, s0, segs, t = p['raw'], p['raw'][0], [], 0
    while t < len(r) - 1:
        if r[t] <= s0 < r[t + 1]:
            b = t + 1
            while r[b] > s0:
                b += 1
            segs.append((t, b))
            t = b
        else:
            t += 1
    return segs


def analyse(paths, hump_thr, nocut_rank, label, series=True):
    T0 = time.time()
    for p in paths:
        p['hump'] = max(p['raw']) - p['raw'][0] >= hump_thr
    humps = [p for p in paths if p['hump']]
    print(label, 'paths', len(paths), 'hump', len(humps), flush=True)

    # 4. climbs along hump paths
    path_keys = ('raw', 'P0cyc', 'P1', 'P1f', 'P1m', 'P2c8', 'P2f8', 'P2c40', 'P2f40', 'P2c', 'P2f')
    per_path = []
    for i, p in enumerate(humps):
        seq = [values(s, path_keys) for s in p['states']]
        p['seq'] = seq
        climbs = {k: max(v[k] for v in seq) - seq[0][k] for k in path_keys}
        e = {'row': p['row'], 'len': len(p['moves']), 'record': p['record'], 'src': p['src'],
             'start': p['raw'][0], 'peak': max(p['raw']), 'climb': climbs}
        if series:
            e['series'] = {k: [v[k] for v in seq] for k in ('raw', 'P0cyc', 'P1', 'P1m', 'P2c8', 'P2c40', 'P2c')}
        per_path.append(e)
        if i % 25 == 0:
            print('  climb', i, p['row'], round(time.time() - T0, 1), flush=True)
    for p in paths:
        if not p['hump']:
            p['seq'] = [values(s, ('raw', 'P2c40')) for s in p['states']]

    # 4b. sibling ranks; a rank key is a tuple of value names, always followed by raw as tiebreak
    rank_keys = [('raw',), ('P1',), ('P1m',), ('P2c8',), ('P2c40',), ('P2f40',)]
    if nocut_rank:
        rank_keys.append(('P2c',))
    rank_keys += [('P1', 'P1m'), ('P2c8', 'P1m')]
    need = sorted({v for k in rank_keys for v in k} | {'raw'})
    names = ['>'.join(k) for k in rank_keys]
    steps = []
    for i, p in enumerate(humps):
        for t, m in enumerate(p['moves']):
            s = p['states'][t]
            vals = [values(apply_move(s, j), need) for j in range(14)]
            rawv = [v['raw'] for v in vals]
            rec = {'row': p['row'], 't': t, 'move': m, 'climb': rawv[m] > tot(s),
                   'above_start': max(tot(s), rawv[m]) > p['raw'][0]}
            for k, nm in zip(rank_keys, names):
                kv = [tuple(v[x] for x in k) + (v['raw'],) for v in vals]
                rec['rank_' + nm], rec['rank_' + nm + '_opt'] = mid_rank(kv, m)
                rec['rank_' + nm + '_only'] = mid_rank([tuple(v[x] for x in k) for v in vals], m)[0]
            steps.append(rec)
        if i % 25 == 0:
            print('  rank', i, p['row'], round(time.time() - T0, 1), flush=True)

    def rank_summary(sel):
        out = {'steps': len(sel)}
        if not sel:
            return out
        for nm in names:
            col = 'rank_' + nm
            rs = [r[col] for r in sel]
            d = {'mean_rank': rnd(mean(rs)), 'top3': rnd(mean([1.0 if x <= 3 else 0.0 for x in rs])),
                 'top7': rnd(mean([1.0 if x <= 7 else 0.0 for x in rs])),
                 'top3_optimistic': rnd(mean([1.0 if x <= 3 else 0.0 for x in (r[col + '_opt'] for r in sel)]))}
            if nm != 'raw':
                only = [r[col + '_only'] for r in sel]
                d['mean_rank_no_raw_tiebreak'] = rnd(mean(only))
                d['top3_no_raw_tiebreak'] = rnd(mean([1.0 if x <= 3 else 0.0 for x in only]))
            out[nm] = d
        return out

    ranks = {'all_steps': rank_summary(steps),
             'climbing_steps': rank_summary([r for r in steps if r['climb']]),
             'climbing_mult_moves': rank_summary([r for r in steps if r['climb'] and 2 <= r['move'] <= 5]),
             'climbing_conj_moves': rank_summary([r for r in steps if r['climb'] and r['move'] >= 6]),
             'above_start_steps': rank_summary([r for r in steps if r['above_start']])}

    climb_summary = {}
    for k in path_keys:
        cs = [pp['climb'][k] for pp in per_path]
        climb_summary[k] = {'median': med(cs), 'mean': rnd(mean(cs)), 'max': max(cs) if cs else None,
                            'frac_zero_or_less': rnd(mean([1.0 if c <= 0 else 0.0 for c in cs])),
                            'frac_ge6': rnd(mean([1.0 if c >= 6 else 0.0 for c in cs]))}

    # 5. kill condition (fixed before the run): dead if median climb >= raw median / 2, or the
    #    top-3 fraction on climbing steps is not higher than raw's
    raw_med = climb_summary['raw']['median']
    cl = ranks['climbing_steps']
    verdicts = {}
    for nm in names[1:]:
        ck = nm.split('>')[0]
        c1 = climb_summary[ck]['median'] >= raw_med / 2.0
        c2 = not (cl[nm]['top3'] > cl['raw']['top3'])
        verdicts[nm] = {'median_climb': climb_summary[ck]['median'], 'raw_median_climb': raw_med,
                        'dead_by_climb': c1, 'top3_climbing': cl[nm]['top3'], 'raw_top3_climbing': cl['raw']['top3'],
                        'dead_by_rank': c2, 'survives': not (c1 or c2)}

    # E1: min(|r0|,|r1|) on humps; spread of moves-remaining given L, (min,max), (min,max,P2)
    e1_paths = []
    for p in humps:
        m0 = min(len(x) for x in p['states'][0])
        above = [min(len(x) for x in s) - m0 for s, r in zip(p['states'], p['raw']) if r > p['raw'][0]]
        allm = [min(len(x) for x in s) - m0 for s in p['states']]
        e1_paths.append({'row': p['row'], 'min_rise_in_hump': max(above) if above else 0, 'min_rise_path': max(allm)})
    e1 = {'hump_paths': len(e1_paths),
          'frac_min_never_above_start_in_hump': rnd(mean([1.0 if e['min_rise_in_hump'] <= 0 else 0.0 for e in e1_paths])),
          'frac_min_rise_le2_in_hump': rnd(mean([1.0 if e['min_rise_in_hump'] <= 2 else 0.0 for e in e1_paths])),
          'frac_min_never_above_start_whole_path': rnd(mean([1.0 if e['min_rise_path'] <= 0 else 0.0 for e in e1_paths])),
          'median_min_rise_in_hump': med([e['min_rise_in_hump'] for e in e1_paths]),
          'spread_note': 'moves-remaining = path length - step; pooled_sd = ANOVA residual SD (df N-G); '
                         'loo_mae = leave-one-out bin-mean error, singleton bins fall back to coarser bins'}
    srows = []
    for p in paths:
        N = len(p['moves'])
        for t, (s, v) in enumerate(zip(p['states'], p['seq'])):
            a, b = sorted((len(s[0]), len(s[1])))
            srows.append({'rem': N - t, 'L': a + b, 'mm': (a, b), 'P2': v['P2c40'], 'hump': p['hump']})
    fL, fM, fP = (lambda r: r['L']), (lambda r: r['mm']), (lambda r: r['P2'])
    fMP, fLP = (lambda r: (r['mm'], r['P2'])), (lambda r: (r['L'], r['P2']))
    for nm, rows in (('spread_all_states', srows), ('spread_hump_path_states', [r for r in srows if r['hump']])):
        e1[nm] = {'N': len(rows), 'L': spread(rows, fL, []), 'P2': spread(rows, fP, []),
                  'L_P2': spread(rows, fLP, [fL]), 'min_max': spread(rows, fM, [fL]),
                  'min_max_P2': spread(rows, fMP, [fM, fL])}
    rises = 1 - e1['frac_min_never_above_start_in_hump']
    sp = e1['spread_all_states']
    e1['kill'] = {'min_rises_in_most_humps': rises > 0.5,
                  'min_max_no_better_than_L': sp['min_max']['loo_mae'] >= sp['L']['loo_mae'],
                  'dead': rises > 0.5 and sp['min_max']['loo_mae'] >= sp['L']['loo_mae']}

    # U1: run lengths of consecutive moves touching the same relator
    all_runs, hump_all_runs, seg_runs = [], [], []
    for p in paths:
        all_runs += runs(p['moves'])
    for p in humps:
        hump_all_runs += runs(p['moves'])
        for a, b in segments(p):
            seg_runs += runs(p['moves'][a:b])
    u1 = {'all_paths_overall': run_stats(all_runs), 'hump_paths_overall': run_stats(hump_all_runs),
          'inside_hump_segments': run_stats(seg_runs),
          'segment_note': 'hump segment = moves a..b-1 of a maximal excursion above the start total'}
    u1['kill'] = {'median_run_inside_humps': u1['inside_hump_segments']['median'],
                  'dead': u1['inside_hump_segments']['median'] < 3}

    # C1: exponent-sum transfer class over hump excursions vs random segments of equal length
    rng = random.Random(2026)
    hump_cls, rand_cls, seg_list = Counter(), Counter(), []
    for p in humps:
        Ms = [exp_matrix(s) for s in p['states']]
        for a, b in segments(p):
            hump_cls[classify_T(Ms[a], Ms[b])] += 1
            seg_list.append((p, b - a))
    for p, ln in seg_list:
        Ms = [exp_matrix(s) for s in p['states']]
        for _ in range(50):
            a = rng.randrange(0, len(p['states']) - ln)
            rand_cls[classify_T(Ms[a], Ms[a + ln])] += 1
    cats = ('pmI', 'finite', 'parabolic', 'hyperbolic')
    nh, nr = sum(hump_cls.values()), sum(rand_cls.values())
    probs = [rand_cls[c] / nr for c in cats]
    tv = 0.5 * sum(abs(hump_cls[c] / nh - rand_cls[c] / nr) for c in cats)
    ge = 0
    for _ in range(4000):
        cnt = Counter(rng.choices(range(4), weights=probs, k=nh))
        if 0.5 * sum(abs(cnt[i] / nh - probs[i]) for i in range(4)) >= tv - 1e-12:
            ge += 1
    c1 = {'hump_segments': nh, 'random_segments': nr,
          'hump_counts': {c: hump_cls[c] for c in cats},
          'hump_mix': {c: rnd(hump_cls[c] / nh) for c in cats}, 'random_mix': {c: rnd(rand_cls[c] / nr) for c in cats},
          'tv_distance': rnd(tv), 'mc_p_value': rnd((ge + 1) / 4001.0, 4),
          'segment_len_median': med([ln for _, ln in seg_list]),
          'method': 'segment = state before the total first exceeds start .. first state back at <= start; '
                    'random = 50 same-length windows per hump segment from the same path; p = Monte Carlo TV test'}
    c1['kill'] = {'dead': c1['mc_p_value'] > 0.05, 'rule': 'mix matches random segments (MC p > 0.05)'}

    return {'counts': {'paths_analysed': len(paths), 'hump_paths': len(humps), 'hump_steps': len(steps),
                       'climbing_steps': sum(1 for r in steps if r['climb']),
                       'climbing_mult_steps': sum(1 for r in steps if r['climb'] and 2 <= r['move'] <= 5)},
            'climb_summary': climb_summary, 'rank_summary': ranks, 'kill_verdicts': verdicts,
            'E1': e1, 'E1_per_path': e1_paths, 'U1': u1, 'C1': c1, 'per_path': per_path,
            'wall_s': round(time.time() - T0, 1)}


def timing_block(rows_all, per_bin=40, seed=11):
    """6. Python time per state (fresh caches), stratified by raw total 20..69, plus op counts."""
    rng = random.Random(seed)
    bins = defaultdict(list)
    for p in rows_all:
        for s in p['states']:
            for c in [s] + [apply_move(s, j) for j in (2, 3, 4, 5)]:
                L = tot(c)
                if 20 <= L <= 69:
                    bins[L // 10 * 10].append(c)
    out = {}
    for b in sorted(bins):
        pool = bins[b]
        rng.shuffle(pool)
        res = defaultdict(list)
        ops = defaultdict(list)
        for s in pool[:per_bin]:
            for name, fn in (('P1', lambda: p1(*s)), ('P1m', lambda: p1m(*s)),
                             ('P2c8', lambda: p2(s[0], s[1], 8)), ('P2c40', lambda: p2(s[0], s[1], 40)),
                             ('P2nocut', lambda: p2(s[0], s[1], None))):
                _P1.clear()
                _P2.clear()
                c0 = (CNT.pairs, CNT.words, CNT.word_chars, CNT.lcs, CNT.lcs_cells)
                t = time.perf_counter()
                fn()
                res[name].append(time.perf_counter() - t)
                ops[name].append([y - x for x, y in zip(c0, (CNT.pairs, CNT.words, CNT.word_chars, CNT.lcs, CNT.lcs_cells))])
        out['%d-%d' % (b, b + 9)] = {
            name: {'n': len(ts), 'py_ms_median': rnd(1000 * med(ts), 3),
                   'pairs': med([o[0] for o in ops[name]]), 'words': med([o[1] for o in ops[name]]),
                   'word_chars': med([o[2] for o in ops[name]]), 'lcs_calls': med([o[3] for o in ops[name]]),
                   'lcs_cells': med([o[4] for o in ops[name]])} for name, ts in res.items()}
        print('  timing', b, {k: v['py_ms_median'] for k, v in out['%d-%d' % (b, b + 9)].items()}, flush=True)
    _P1.clear()
    _P2.clear()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sair', default=SAIR_DEFAULT)
    ap.add_argument('--out', default=OUT_DEFAULT)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--hump', type=int, default=6)
    ap.add_argument('--no-secondary', action='store_true', help='skip the all-verified-rows secondary pass')
    ap.add_argument('--no-timing', action='store_true')
    ap.add_argument('--c-bench', help='text output of the C microbenchmark (p2bench.c) to embed')
    args = ap.parse_args()
    T0 = time.time()
    official = load_official(args.sair)
    man = {c['challenge_id']: c['initial_relators']
           for c in json.load(open(os.path.join(args.sair, 'competition/tools/verifier/data/manifest.json')))['challenges']}
    board = {c['challengeId']: c['currentBestLength'] for c in json.load(gzip.open(BOARD))['data']['items']}
    rows_all, collection, bad = collect_rows(official, man, board)
    print('collected', collection, flush=True)
    at_rec = [p for p in rows_all if p['at_record']]
    st = selftest(at_rec) if args.selftest else None
    if st:
        print('selftest', st, flush=True)

    primary = analyse(at_rec, args.hump, True, 'at_record')
    secondary = None
    if not args.no_secondary:
        sec = analyse(rows_all, args.hump, False, 'all_rows', series=False)
        secondary = {k: sec[k] for k in ('counts', 'climb_summary', 'rank_summary', 'kill_verdicts', 'E1', 'U1', 'C1', 'wall_s')}
    timing = None if args.no_timing else timing_block(rows_all)

    out = {'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'script': os.path.relpath(__file__, REPO),
           'hypothesis': 'B31: multiplications are the only class-changing moves; P2 should stay flat over humps',
           'definitions': __doc__, 'hump_threshold': args.hump, 'collection': collection,
           'replay_failures': bad[:50], 'selftest': st,
           'primary_at_record': primary, 'secondary_all_verified_rows': secondary,
           'timing_python_per_state': timing,
           'timing_c_bench': open(args.c_bench).read().splitlines() if args.c_bench else None,
           'wall_s': round(time.time() - T0, 1)}
    with open(args.out, 'w') as f:
        json.dump(out, f, indent=1)
    print(json.dumps({'counts': primary['counts'], 'kill': primary['kill_verdicts']}, indent=1))
    print('wrote', args.out, 'wall', out['wall_s'])


if __name__ == '__main__':
    main()
