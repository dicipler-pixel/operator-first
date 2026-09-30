#!/usr/bin/env python3
"""t00138 helper probe: can one interior stabilize/destabilize pair shorten a
Stable (sac-r8-v1) route below our rank-2 AC route + 2?

Exact meet-in-the-middle search on top of the pinned official kernel
(verifier.stable_core.apply_move).  For every pair of states S_i, S_j
(i < j) along our best AC path P we look for a rank-3 route

    14  B  destab           (B = rank-3 moves, |B| = L)

from S_i to S_j (or from S_i to one of the 8 canonical single-letter
finals with their known finish cost) with L <= DF + DB.  Any rank-2 moves
before the stabilize or after the destabilize commute with them, so this
form is without loss of generality for a route that uses exactly one
helper (one stabilize, one destabilize).

Backward seeds for S_j: every rank-3 state that destabilizes to S_j, i.e.
insert (g,) at relator index p (p in 0..2, g in 1..3) and relabel the
letters of S_j that are >= g up by one.  So the helper may be g3, or the
destabilize may drop x or y (a generator substitution).

A found route saves (j - i) - (L + 2) moves.  We report every pair with
saving >= 1 and rebuild + verify the whole Stable path with
stable_core.verify.  Anything shorter than our AC best + 2 is written to
lines.txt as `sac-XXXXX: [moves]`.

Usage: helper_probe.py ROW DF DB CAP_SLACK OUTDIR
"""
import json, os, sys, time
sys.path.insert(0, os.path.expanduser('~/.cache/upgh/sair/competition/tools'))
from verifier import core, stable_core

apply = stable_core.apply_move
SAVING_MIN = int(os.environ.get('SAVING_MIN', '1'))  # debug: lower to exercise rebuild

# ---------------------------------------------------------------- moves
def rank3_moves():
    st = ((1, 2), (2, 1), (3,))
    out = []
    for m in range(stable_core.NUM_MOVES):
        cat = stable_core.MOVE_TABLE[m]['category']
        if cat in ('stabilize', 'destabilize'):
            continue
        s, reason = apply(st, m)
        if reason is None:
            out.append(m)
    return out

R3 = rank3_moves()
INV = stable_core.INVERSE_MOVE
assert len(R3) == 33, len(R3)

# the 8 canonical finals and their finish cost (spec canonicalization_table)
CANON = {((1,), (2,)): 2, ((2,), (1,)): 2,
         ((-2,), (1,)): 3, ((-1,), (2,)): 3, ((1,), (-2,)): 3, ((2,), (-1,)): 3,
         ((-2,), (-1,)): 4, ((-1,), (-2,)): 4}
CANON_PATH = {((1,), (2,)): [16, 15], ((2,), (1,)): [16, 15],
              ((-2,), (1,)): [0, 16, 15], ((-1,), (2,)): [0, 16, 15],
              ((1,), (-2,)): [1, 16, 15], ((2,), (-1,)): [1, 16, 15],
              ((-2,), (-1,)): [0, 1, 16, 15], ((-1,), (-2,)): [0, 1, 16, 15]}


def enc(state):
    # compact key: letters shifted to 1..17 (0 separates relators)
    return bytes(a + 9 for w in state for a in w + (-9,))


def tot(state):
    return sum(len(w) for w in state)


def lifts(S2):
    """All rank-3 states that destabilize (one move) to rank-2 state S2.
    Returns list of (state3, destab_move_id)."""
    out = []
    for g in (1, 2, 3):
        rel = tuple(tuple(a + 1 if a >= g else (a - 1 if a <= -g else a) for a in w) for w in S2)
        for p in (0, 1, 2):
            s3 = rel[:p] + ((g,),) + rel[p:]
            out.append((s3, 15 + p))
    return out


def bfs(seeds, depth, cap, inverse=False):
    """dict key -> (dist) for all states within `depth` moves of seeds under
    the relator-total cap.  If inverse, uses inverse moves (backward search)."""
    seen = {}
    frontier = []
    for s in seeds:
        k = enc(s)
        if k not in seen:
            seen[k] = 0
            frontier.append(s)
    moves = [INV[m] for m in R3] if inverse else R3
    for d in range(1, depth + 1):
        nxt = []
        for s in frontier:
            for m in moves:
                t, _ = apply(s, m)
                if tot(t) > cap:
                    continue
                k = enc(t)
                if k not in seen:
                    seen[k] = d
                    nxt.append(t)
        frontier = nxt
    return seen


def find_path(start, target_key, depth, cap):
    """DFS with iterative deepening: exact move list from start to the state
    with key target_key in <= depth forward moves."""
    for dl in range(0, depth + 1):
        stack = [(start, [])]
        while stack:
            s, p = stack.pop()
            if enc(s) == target_key:
                return p
            if len(p) == dl:
                continue
            for m in R3:
                t, _ = apply(s, m)
                if tot(t) > cap:
                    continue
                stack.append((t, p + [m]))
    return None


def main():
    row, DF, DB, SLACK, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    man = json.load(open(os.path.expanduser('~/.cache/upgh/sair/competition/tools/verifier/data/manifest.json')))
    idx = {c['challenge_id']: c for c in man['challenges']}
    lim = man['limits']
    ct = json.load(open('/home/user/operator-first/research/acc/upgh/tasks/t00138.json'))
    ctx = ct['context'][row]
    P = ctx['our_best_moves']
    chal = idx[row]
    assert stable_core.verify(chal, P, 'sac-r8-v1', lim)['ok']
    # rank-2 prefix of P (strip the trailing destabilizes)
    n = len(P)
    while n > 0 and P[n - 1] >= 14:
        n -= 1
    AC = P[:n]
    tail = P[n:]
    states = [tuple(tuple(w) for w in chal['initial_relators'])]
    for m in AC:
        s, r = apply(states[-1], m)
        assert r is None and len(s) == 2
        states.append(s)
    assert states[-1] in CANON, states[-1]
    t0 = time.time()
    log = open(os.path.join(outdir, f'{row}_probe_df{DF}_db{DB}.log'), 'w')
    def out(*a):
        msg = ' '.join(str(x) for x in a)
        print(msg); log.write(msg + '\n'); log.flush()
    out(f'row {row} AC len {n} tail {tail} record {ctx["record"]} ours {len(P)}; DF={DF} DB={DB} cap=tot+1+{SLACK}')
    out('rank-3 move ids used:', R3)

    # forward sets from every S_i + (g3)
    F = []
    for i, S in enumerate(states):
        s3 = S + ((3,),)
        F.append(bfs([s3], DF, tot(s3) + SLACK))
    out(f'forward sets built: {len(F)} sizes min/max {min(map(len,F))}/{max(map(len,F))} t={time.time()-t0:.1f}s')

    hits = []
    best_saving = 0
    # backward sets for every S_j (j >= 1) and for the canonical finals
    targets = [(j, states[j], 0) for j in range(1, len(states))]
    for cs, c in CANON.items():
        targets.append((('final', cs), cs, c))
    checked_pairs = 0
    for tj, S, cfin in targets:
        seeds = lifts(S)
        cap = tot(S) + 1 + SLACK
        B = bfs([s for s, _ in seeds], DB, cap, inverse=True)
        jmax = tj if isinstance(tj, int) else len(states) - 1
        for i in range(0, jmax):
            Fi = F[i]
            if isinstance(tj, int):
                base = tj - i                       # rank-2 cost of P[i:tj]
            else:
                base = (len(states) - 1 - i) + len(tail)  # our cost from S_i to empty
            # search min L
            bestL = None
            small, big = (Fi, B) if len(Fi) < len(B) else (B, Fi)
            for k, d in small.items():
                e = big.get(k)
                if e is not None:
                    L = d + e
                    if bestL is None or L < bestL:
                        bestL = L
            checked_pairs += 1
            if bestL is None:
                continue
            new = bestL + 2 + cfin
            saving = base - new
            if saving >= SAVING_MIN:
                out(f'SAVING {saving}: i={i} j={tj} base={base} helper_cost={new} (L={bestL})')
                hits.append((i, tj, base, new, bestL, cfin))
                best_saving = max(best_saving, saving)
    out(f'pairs checked {checked_pairs}; hits {len(hits)}; t={time.time()-t0:.1f}s')

    # rebuild and verify any hit
    lines = []
    for (i, tj, base, new, bestL, cfin) in hits:
        S = states[tj] if isinstance(tj, int) else tj[1]
        # find meeting state and both halves
        Fi = F[i]
        seeds = lifts(S)
        cap = tot(S) + 1 + SLACK
        B = bfs([s for s, _ in seeds], DB, cap, inverse=True)
        meet = None
        for k, d in Fi.items():
            e = B.get(k)
            if e is not None and d + e == bestL:
                meet = (k, d, e); break
        k, d, e = meet
        s3 = states[i] + ((3,),)
        half1 = find_path(s3, k, d, tot(s3) + SLACK)
        mid, _ = states[i] + ((3,),), None
        for m in half1:
            mid, _ = apply(mid, m)
        # second half: forward from mid to one of the seeds in e moves
        half2 = None; dest = None
        for sd, dm in seeds:
            p2 = find_path(mid, enc(sd), e, cap)
            if p2 is not None:
                half2, dest = p2, dm; break
        assert half2 is not None
        if isinstance(tj, int):
            full = AC[:i] + [14] + half1 + half2 + [dest] + AC[tj:] + tail
        else:
            full = AC[:i] + [14] + half1 + half2 + [dest] + CANON_PATH[tj[1]]
        r = stable_core.verify(chal, full, 'sac-r8-v1', lim)
        out(f'REBUILT i={i} j={tj}: len {len(full)} verify {r}')
        out(f'   path {full}')
        if r['ok'] and len(full) < len(P) and SAVING_MIN >= 1:
            lines.append(f'{row}: {json.dumps(full)}')
    if lines:
        with open(os.path.join(outdir, 'lines.txt'), 'a') as f:
            f.write('\n'.join(lines) + '\n')
    out(f'done row {row}: best_saving={best_saving} shorter_paths_written={len(lines)} wall={time.time()-t0:.1f}s')
    log.close()


if __name__ == '__main__':
    main()
