#!/usr/bin/env python3
"""Raw per-step eye readings, and the reverse-engineering of shapes from them.

The operating rule this replaces: "prefer the child with the best total length."
On our OWN verified certificates that rule is wrong more often than right, so a
search built on it refuses the moves that actually worked.

Readings computed per step, all raw and none thresholded here:

  len_delta      immediate change in total relator length
  rank_by_len    where the taken move ranks among the 14 by immediate length
  turn           MOVE-SPACE ROTATION: how much the 14-entry profile of
                 "what each move would do to length" re-orients across the step.
                 Cosine distance on the centred profile, in [0,1]. This is the
                 quantity that sees a move rearranging the word so the NEXT
                 product move can cancel something, which length cannot see.
  ledger         abelianisation (exponent-sum matrix), the coarse invariant
  ledger_same    ledger unchanged across the step
  fiber_change   ledger unchanged BUT the actual nonabelian state changed --
                 merging states on the coarse ledger throws these away
  floor2/floor5  best total length within the next 2 / 5 steps
  collapse5      a strictly shorter state appears within 5 steps

Nothing here prunes or certifies. These are observations; replay decides.
"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from replay import apply_move, expsum


def profile(r0, r1):
    """For each of the 14 moves, the total length it would produce. Illegal or
    degenerate moves are recorded as a large value so they sit at the bottom."""
    out = []
    for m in range(14):
        try:
            a, b = apply_move(list(r0), list(r1), m)
        except ValueError:
            out.append(999)
            continue
        out.append(999 if (not a or not b) else len(a) + len(b))
    return out


def turn(p, q):
    """Cosine distance between two centred move profiles, mapped to [0,1]."""
    pv = [x for x in p]
    qv = [x for x in q]
    mp = sum(pv) / len(pv)
    mq = sum(qv) / len(qv)
    pu = [x - mp for x in pv]
    qu = [x - mq for x in qv]
    np_ = math.sqrt(sum(x * x for x in pu))
    nq_ = math.sqrt(sum(x * x for x in qu))
    if np_ == 0 or nq_ == 0:
        return 0.0
    cos = sum(a * b for a, b in zip(pu, qu)) / (np_ * nq_)
    cos = max(-1.0, min(1.0, cos))
    return (1.0 - cos) / 2.0


def ledger(r0, r1):
    return (expsum(r0), expsum(r1))


def read_trajectory(r0, r1, moves):
    """Raw readings for every step of one trajectory."""
    a, b = list(r0), list(r1)
    states = [(list(a), list(b))]
    for m in moves:
        a, b = apply_move(a, b, m)
        states.append((list(a), list(b)))
    tot = [len(s[0]) + len(s[1]) for s in states]
    profs = [profile(*s) for s in states]

    rows = []
    for i, m in enumerate(moves):
        p_before, p_after = profs[i], profs[i + 1]
        legal = [(profile_val, mm) for mm, profile_val in enumerate(p_before)
                 if profile_val < 999]
        legal.sort()
        rank = next((k for k, (_v, mm) in enumerate(legal) if mm == m), len(legal))
        lo_before, lo_after = ledger(*states[i]), ledger(*states[i + 1])
        fut = tot[i + 1:i + 6]
        rows.append({
            "step": i, "move": m,
            "len_before": tot[i], "len_after": tot[i + 1],
            "len_delta": tot[i + 1] - tot[i],
            "rank_by_len": rank, "n_legal": len(legal),
            "best_available_delta": (legal[0][0] - tot[i]) if legal else 0,
            "turn": turn(p_before, p_after),
            "ledger_same": lo_before == lo_after,
            "fiber_change": (lo_before == lo_after
                             and states[i] != states[i + 1]),
            "floor2": min(tot[i + 1:i + 3]) if tot[i + 1:i + 3] else tot[i],
            "floor5": min(fut) if fut else tot[i],
            "collapse5": bool(fut) and min(fut) < tot[i],
        })
    return rows
