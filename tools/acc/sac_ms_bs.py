#!/usr/bin/env python3
"""Stable AC (sac-r8-v1) generator for MS(n, BS) = (YXXyx, Y^(n+1) X y^n x), any n >= 2.

Route (every move replayed with the official verifier.stable_core.apply_move, applicability asserted):
  1. rank-2 level build (Codex yxxyx_chain): level j, a = 2^j, block 10^(a-1) 5 (11 5)^(a-1) 12
     takes (BS, Y^k X y^(k-1) x^a) to (BS, Y^(k-1) X y^(k-2) x^(2a)); 3a-1 moves per level, ends at (BS, Y x^M),
     M = 2^n - 1.
  2. conversion 6 2 10 10 5 7 0 8: (BS, Y x^M) -> (y X^m, x), m = M - 1 (8 moves).
  3. rank-3 fast tail (tools/acc/sac_fast_peel.py idea, slots swapped): stabilize g, r2 = g X^k, swap each
     X^k block of r0 for one G (r0 <- r0 r2^-1, conjugate r0 by G), peel the rest, reduce r2 to g, peel the
     G's, destabilize g, y, x.  2k + 3(m div k) + (m mod k) + 5 moves.  The plain rank-2 finish (AC + 2) is
     used instead whenever it is shorter.

Why not the super-relator doubling (S_(2a) = (X^a S_a x^a) S_a, one multiplication per level)?  See
research/acc/live/ledger/sac_ms_bs_20260928.json ("obstruction").  In short: S_a (a >= 2) can never be a
relator without a stabilization letter (its exponent row is divisible by a, the relation matrix must stay
unimodular), a letter g occurring once can never be cancelled against a second use of the same tool
(the pair then contributes nothing), and the X^a conjugation that doubling needs drags g into the middle of
X^(2a), the X|Y seam, or the output block, where it blocks the next crossing.

usage: python3 tools/acc/sac_ms_bs.py --sair-root SAIR --n 10
       python3 tools/acc/sac_ms_bs.py --sair-root SAIR --all [--submission FILE] [--json-out FILE]
"""
import argparse
import json
import sys
from pathlib import Path

BS = (-2, -1, -1, 2, 1)
SCORED = {5: 'sac-01950', 6: 'sac-02033', 7: 'sac-06796', 8: 'sac-03079', 9: 'sac-06727', 10: 'sac-00106'}


def load_core(sair_root):
    sys.path.insert(0, str(Path(sair_root) / 'competition' / 'tools'))
    from verifier import stable_core
    return stable_core


def move_ids(sc):
    ids = {}
    for r in sc.MOVE_TABLE:
        c = r['category']
        if c == 'multiplication':
            ids[('mul', r['relator'], r['other'], r['invert_other'])] = r['id']
        elif c == 'conjugation':
            ids[('conj', r['relator'], r['conjugator'])] = r['id']
        elif c == 'inversion':
            ids[('inv', r['relator'])] = r['id']
        elif c == 'destabilize':
            ids[('destab', r['relator'])] = r['id']
        elif c == 'stabilize':
            ids[('stab',)] = r['id']
    # rows 0..13 are the ac-r2-v1 table (not re-listed by the enumeration above)
    ids.update({('inv', 0): 0, ('inv', 1): 1,
                ('mul', 0, 1, False): 2, ('mul', 0, 1, True): 3,
                ('mul', 1, 0, False): 4, ('mul', 1, 0, True): 5,
                ('conj', 0, 1): 6, ('conj', 0, -1): 7, ('conj', 0, 2): 8, ('conj', 0, -2): 9,
                ('conj', 1, 1): 10, ('conj', 1, -1): 11, ('conj', 1, 2): 12, ('conj', 1, -2): 13})
    return ids


def initial(n):
    return (BS, tuple([-2] * (n + 1) + [-1] + [2] * n + [1]))


def build(n):
    """Rank-2 level build to (BS, Y x^(2^n - 1)): 3a-1 moves per level a = 1, 2, ..., 2^(n-1)."""
    mv = []
    for j in range(n):
        a = 1 << j
        mv += [10] * (a - 1) + [5] + [11, 5] * (a - 1) + [12]
    return mv


CONVERT = [6, 2, 10, 10, 5, 7, 0, 8]          # (BS, Y x^M) -> (y X^(M-1), x)


def tail_cost(m, k):
    q, rem = divmod(m, k)
    return 2 * k + 3 * q + rem + 5


def best_k(m):
    return min(range(1, m + 1), key=lambda k: tail_cost(m, k))


def fast_tail(ID, m, k=None):
    """Moves from the rank-2 state (y X^m, x) [r0 = y X^m, r1 = x] to the empty presentation."""
    k = k or best_k(m)
    q, rem = divmod(m, k)
    mv = [ID[('stab',)]]                           # (y X^m, x, g)
    mv += [ID[('mul', 2, 1, True)]] * k            # r2 = g X^k
    for _ in range(q):                             # r0 = G^q y X^rem
        mv += [ID[('mul', 0, 2, True)], ID[('conj', 0, -3)]]
    mv += [ID[('mul', 0, 1, False)]] * rem         # r0 = G^q y
    mv += [ID[('mul', 2, 1, False)]] * k           # r2 = g
    mv += [ID[('conj', 0, 2)]]                     # r0 = y G^q
    mv += [ID[('mul', 0, 2, False)]] * q           # r0 = y
    mv += [ID[('destab', 2)], ID[('destab', 0)], ID[('destab', 0)]]
    return mv


def plain_finish(M):
    """Codex finish (BS, Y x^M) -> (x, y), then destabilize x and y (AC + 2)."""
    return [6, 2, 10, 10, 5] + [3] * (M - 2) + [5, 11, 2] + [15, 15]


def replay(sc, state, moves):
    for i, m in enumerate(moves):
        nxt, why = sc.apply_move(state, m)
        assert nxt is not None, 'move %d (%d) not applicable: %s' % (i, m, why)
        state = nxt
    return state


def generate(sc, n):
    ID = move_ids(sc)
    M = (1 << n) - 1
    b = build(n)
    st = replay(sc, initial(n), b)
    assert st == (BS, tuple([-2] + [1] * M)), (n, st)
    c = replay(sc, st, CONVERT)
    assert c == (tuple([2] + [-1] * (M - 1)), (1,)), (n, c)
    fast = CONVERT + fast_tail(ID, M - 1)
    plain = plain_finish(M)
    finish, kind = (fast, 'fast-rank3') if len(fast) < len(plain) else (plain, 'plain-rank2')
    path = b + finish
    end = replay(sc, initial(n), path)
    assert end == (), (n, end)
    return path, {'n': n, 'build': len(b), 'finish': len(finish), 'finish_kind': kind,
                  'fast_k': best_k(M - 1), 'length': len(path)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sair-root', default='SAIR')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--n', type=int)
    g.add_argument('--all', action='store_true')
    ap.add_argument('--submission', type=Path, help='write sac-XXXXX: [...] lines for scored n')
    ap.add_argument('--json-out', type=Path)
    args = ap.parse_args()
    sc = load_core(args.sair_root)
    manifest = json.loads((Path(args.sair_root) / 'competition/tools/verifier/data/manifest.json').read_text())
    rows = {c['challenge_id']: c for c in manifest['challenges']}
    ns = range(4, 11) if args.all else (args.n,)
    out, lines = [], []
    for n in ns:
        path, info = generate(sc, n)
        cid = SCORED.get(n)
        if cid:
            ch = rows[cid]
            assert tuple(tuple(w) for w in ch['initial_relators']) == initial(n)
        else:
            ch = {'challenge_id': 'synthetic-ms-bs-%d' % n, 'move_spec_version': 'sac-r8-v1',
                  'initial_relators': [list(w) for w in initial(n)], 'target_relators': []}
        res = sc.verify(ch, path, 'sac-r8-v1', manifest['limits'])
        info.update({'challenge_id': ch['challenge_id'], 'verify': res})
        out.append(dict(info, moves=path))
        if cid:
            lines.append('%s: %s' % (cid, json.dumps(path, separators=(',', ':'))))
        print('n=%d %s length=%d (build %d + finish %d %s) ok=%s' % (
            n, ch['challenge_id'], info['length'], info['build'], info['finish'], info['finish_kind'], res['ok']))
    if args.submission:
        args.submission.write_text('\n'.join(lines) + '\n')
    if args.json_out:
        args.json_out.write_text(json.dumps(out) + '\n')


if __name__ == '__main__':
    main()
