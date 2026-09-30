# SCRIPT: BOB-BLOCK-SPLICE-01
# Block splice: shorten a verified AC path by replacing a stretch [i, k) with a
# shorter bridge made of single moves and/or whole library blocks, bridge found by
# meet-in-the-middle: forward steps from state_i meet backward (inverted) steps
# from state_k. Blocks are always applied to the real state with the official
# SAIR kernel (verifier.core.apply_move), cost = number of primitive moves.
# Repeats until nothing improves. Every output is replayed start -> ((1,),(2,)).
import os, sys, json, itertools
SAIR = os.environ.get('SAIR', 'Andrews-Curtis')
sys.path.insert(0, SAIR + '/competition/tools')
from verifier.core import apply_move, free_reduce, INVERSE_MOVE

TARGET = ((1,), (2,))

def run(state, seq):
    for m in seq:
        state = apply_move(state, m)
    return state

def states_of(start, path):
    S = [start]
    for m in path:
        S.append(apply_move(S[-1], m))
    return S

def inv_seq(seq):
    return tuple(INVERSE_MOVE[m] for m in reversed(seq))

def make_steps(blocks, prim_depth=2):
    steps = set()
    for d in range(1, prim_depth + 1):
        for t in itertools.product(range(14), repeat=d):
            if any(INVERSE_MOVE[t[a]] == t[a + 1] for a in range(d - 1)):
                continue
            steps.add(t)
    for b in blocks:
        steps.add(tuple(b))
    return sorted(steps, key=len)

def best_splice(start, path, steps, min_len=2, max_len=40):
    # returns (saving, i, k, bridge) for the largest saving found, or None
    S = states_of(start, path)
    L = len(path)
    idx = {}
    for k, s in enumerate(S):
        idx[s] = k                      # latest occurrence (loops give free savings)
    best = None
    # backward table: state T -> (k, cost, seq) with T --seq--> S[k]
    back = {}
    for k in range(L + 1):
        s = S[k]
        for st in steps:
            T = run(s, inv_seq(st))
            c = len(st)
            old = back.get(T)
            if old is None or (k - c) > (old[0] - old[1]):
                back[T] = (k, c, st)
    for i in range(L):
        s = S[i]
        # loop: state repeats later
        k = idx[s]
        if k > i and (best is None or k - i > best[0]):
            best = (k - i, i, k, ())
        for st in steps:
            T = run(s, st)
            c1 = len(st)
            # direct hit on the path
            k = idx.get(T)
            if k is not None and min_len <= k - i <= max_len:
                sav = (k - i) - c1
                if sav > 0 and (best is None or sav > best[0]):
                    best = (sav, i, k, st)
            # meet with a backward step
            hit = back.get(T)
            if hit is not None:
                k, c2, st2 = hit
                if min_len <= k - i <= max_len:
                    sav = (k - i) - c1 - c2
                    if sav > 0 and (best is None or sav > best[0]):
                        best = (sav, i, k, st + st2)
    return best

def splice_path(start, path, steps, log=None, **kw):
    path = tuple(path)
    while True:
        b = best_splice(start, path, steps, **kw)
        if b is None:
            return path
        sav, i, k, bridge = b
        new = path[:i] + tuple(bridge) + path[k:]
        S = states_of(start, path)
        assert run(S[i], bridge) == S[k]
        assert run(start, new) == run(start, path)
        if log is not None:
            log.append(dict(i=i, k=k, old_len=k - i, bridge=list(bridge), saving=sav, new_total=len(new)))
        path = new

def verify_line(relators, path):
    start = (free_reduce(tuple(relators[0])), free_reduce(tuple(relators[1])))
    return run(start, path) == TARGET
