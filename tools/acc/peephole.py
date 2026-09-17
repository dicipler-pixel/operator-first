#!/usr/bin/env python3
"""Local peephole shortening: fix one window instead of re-searching the row.

A row sitting at +1 does not need a better global search. It needs ONE window of
its path to give up a single move. Global search has to rediscover the whole
34-move path; a peephole only has to beat a 9-move stretch of it.

For each window (i, j) of the current path, take the state at step i and the
state at step j and ask the CALIBRATED corridor for the exact shortest path
between them. That engine already accepts an arbitrary start AND target, so this
reuses it rather than adding another engine. If the corridor returns something
shorter than j - i, splice it in and continue from a fixed point.

Every splice is re-replayed against the row's ORIGINAL relators, and the result
is rejected outright if the endpoint moved. The cap for each window is set from
the window's own states -- max length inside it plus a slack -- because that is
the local |r|, not the row's.

Usage: peephole.py <r0> <r1> <moves.json|-> [--cap-slack N] [--window W]
"""
import sys, os, json, subprocess, tempfile
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from replay import apply_move, replay

COR = os.environ.get("COR2B", "/tmp/claude-0/-home-user-operator-first/"
                     "134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/acc_snap/cor2b")


def states_along(r0, r1, moves):
    a, b = list(r0), list(r1)
    out = [(list(a), list(b))]
    for m in moves:
        a, b = apply_move(a, b, m)
        out.append((list(a), list(b)))
    return out


def exact_between(s, t, cap, maxst=4000000, timeout=25):
    """Shortest path s -> t inside `cap`, or None. Uses the calibrated corridor."""
    args = [COR, str(cap), str(maxst),
            str(len(s[0])), *map(str, s[0]), str(len(s[1])), *map(str, s[1]),
            str(len(t[0])), *map(str, t[0]), str(len(t[1])), *map(str, t[1])]
    try:
        env = dict(os.environ, BESTMEET="1")
        out = subprocess.run(args, capture_output=True, text=True,
                             timeout=timeout, env=env).stdout
    except subprocess.TimeoutExpired:
        return None
    mv = None
    for line in out.splitlines():
        if line.startswith("MOVES"):
            mv = [int(x) for x in line.split()[1:]]
    if mv is None:
        return None
    # only trust a window the corridor proved, or one that is simply shorter
    return mv


def peephole(r0, r1, moves, window=10, slack=14, verbose=True):
    """slack defaults HIGH on purpose.

    A global search proved ac-06639 is 35 moves within total length <= |r|+8, so
    running a peephole at the same cap just reproduces that proof. The value of a
    window is that a high cap is CHEAP over 10 moves and ruinous over 35 -- if the
    record's length excursion is confined to one stretch, only a generous local
    cap can see it. Slack 6 found nothing here; that was the parameter's fault,
    not the method's.
    """
    moves = list(moves)
    end = states_along(r0, r1, moves)[-1]
    improved = True
    while improved:
        improved = False
        st = states_along(r0, r1, moves)
        n = len(moves)
        for i in range(n):
            for j in range(min(n, i + window), i + 2, -1):
                span = j - i
                s, t = (tuple(st[i][0]), tuple(st[i][1])), (tuple(st[j][0]), tuple(st[j][1]))
                cap = max(len(st[k][0]) + len(st[k][1]) for k in range(i, j + 1)) + slack
                mv = exact_between(([*st[i][0]], [*st[i][1]]),
                                   ([*st[j][0]], [*st[j][1]]), cap)
                if mv is None or len(mv) >= span:
                    continue
                cand = moves[:i] + mv + moves[j:]
                a, b, _ = replay(r0, r1, cand)
                if (tuple(a), tuple(b)) != (tuple(end[0]), tuple(end[1])):
                    continue          # a splice that moves the endpoint is a bug
                if verbose:
                    print(f"    window [{i},{j}) {span} -> {len(mv)} moves "
                          f"(cap {cap}), total {len(moves)} -> {len(cand)}", flush=True)
                moves = cand
                improved = True
                break
            if improved:
                break
    return moves


if __name__ == "__main__":
    r0 = [int(c) for c in sys.argv[1].split(",")]
    r1 = [int(c) for c in sys.argv[2].split(",")]
    mv = json.load(open(sys.argv[3])) if sys.argv[3] != "-" else \
        [int(x) for x in sys.stdin.read().split()]
    W = int(sys.argv[sys.argv.index("--window") + 1]) if "--window" in sys.argv else 10
    out = peephole(r0, r1, mv, window=W)
    _, _, ok = replay(r0, r1, out)
    print(f"peephole: {len(mv)} -> {len(out)} moves, replays to (x,y) = {ok}")
    print("MOVES " + " ".join(map(str, out)))
