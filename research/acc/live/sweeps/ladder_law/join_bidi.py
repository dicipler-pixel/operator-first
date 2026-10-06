#!/usr/bin/env python3
"""Cheapest join of a row start S0 onto a known trajectory traj[0..L] (restricted moves, total length <= cap):
minimise  dist(S0, traj[k]) + (L - k)  over k, by a bidirectional BFS whose backward side starts from every traj[k] with initial
distance (kmax - k) (a virtual sink). Exact for the given cap. Library: join(S0, traj, kset, cap) -> (prefix_moves, k) or None."""
import sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import bs_doubling as B
core = B.core
RM = (0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13)
INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}


def join(S0, traj, kset, cap, maxtotal=60, allowed=RM):
    kmax = max(kset)
    # forward: state -> (dist, parent, move); backward: state -> (dist, parent, move, k_origin)
    F = {S0: (0, None, None)}
    Bk = {}
    bstart = {}
    for k in kset:
        t = traj[k]
        d0 = kmax - k
        if t not in bstart or d0 < bstart[t][0]:
            bstart[t] = (d0, k)
    for t, (d0, k) in bstart.items():
        Bk[t] = (d0, None, None, k)
    ff = [S0]
    fd = 0
    # backward layers by distance
    blayers = {}
    for t, (d0, k) in bstart.items():
        blayers.setdefault(d0, []).append(t)
    bd = -1
    bfront = []
    best = None

    def total(s):
        return F[s][0] + Bk[s][0]

    for s in list(F):
        if s in Bk:
            best = (total(s), s)
    while fd + max(bd, 0) < maxtotal:
        if best and fd + bd + 1 >= best[0]:
            break
        # expand the cheaper side
        nb_next = len(bfront) + len(blayers.get(bd + 1, []))
        if len(ff) <= nb_next or bd >= maxtotal:
            nxt = []
            for s in ff:
                for mv in allowed:
                    t = core.apply_move(s, mv)
                    if t in F or len(t[0]) + len(t[1]) > cap:
                        continue
                    F[t] = (fd + 1, s, mv)
                    nxt.append(t)
                    if t in Bk and (best is None or total(t) < best[0]):
                        best = (total(t), t)
            ff = nxt
            fd += 1
            if not ff:
                break
        else:
            bd += 1
            cur = bfront + [t for t in blayers.get(bd, []) if Bk[t][0] == bd]
            nxt = []
            for s in cur:
                if s in F and (best is None or total(s) < best[0]):
                    best = (total(s), s)
                for mv in allowed:
                    t = core.apply_move(s, mv)
                    if len(t[0]) + len(t[1]) > cap:
                        continue
                    if t in Bk and Bk[t][0] <= bd + 1:
                        continue
                    Bk[t] = (bd + 1, s, INV[mv], Bk[s][3])
                    nxt.append(t)
                    if t in F and (best is None or total(t) < best[0]):
                        best = (total(t), t)
            bfront = nxt
    if not best:
        return None
    s = best[1]
    pre = []
    x = s
    while F[x][1] is not None:
        pre.append(F[x][2])
        x = F[x][1]
    pre.reverse()
    x = s
    while Bk[x][1] is not None:
        pre.append(Bk[x][2])
        x = Bk[x][1]
    k = Bk[x][3]
    assert x == traj[k]
    return pre, k
