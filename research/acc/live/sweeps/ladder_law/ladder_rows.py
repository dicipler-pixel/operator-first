#!/usr/bin/env python3
"""Per-row doubling roads on the MS(n, w*) ladder 'XXYxy' (n = 4..10), built from the canonical macro loop (loop_macro.py):
  1. map the row start into the canonical frame (symmetry g with g(MS canonical) = row up to cyclic words);
  2. exact bidirectional prefix (restricted moves) from it onto the canonical macro trajectory at step k (best k);
  3. the rest of the canonical loop to the pre-finish state; map all moves back to the row frame;
  4. finish in the row frame: fin2 mapped (+ exact short adapter), or the frame finish read off the exact m = 3 optimum
     F_(0,1,1,1)(m) = [2,0,7,5,12,2,8] + [11]*(m-1) + [3,8,11,4,2,0] + [5]*(m-1)  (relator-swap frame), whichever verifies shorter;
  5. Stable: the AC road + [16,15], or the mapped road ending at (y,x) + [15,15].
Every road is replayed on the pinned official core (ac-r2-v1 / sac-r8-v1) and compared with the live records.
usage: ladder_rows.py NMIN NMAX     scoring lines -> research/acc/live/inbox/upgh_ladder_<UTC>.txt"""
import datetime, glob, gzip, json, sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
sys.path.insert(0, "/home/user/operator-first/research/acc/live/sweeps/ladder_law")
import bs_doubling as B
import symmetry_recog as SR
from verifier import stable_core
from loop_bidi import bidi
from loop_macro import build
T = B.T
core = B.core
R = "/home/user/operator-first/"
REC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "research/acc/live/boards/ac_*.json.gz"))[-1]))["data"]["items"]}
SREC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "research/acc/live/boards/stable_ac_*.json.gz"))[-1]))["data"]["items"]}
FORBID = {"09839", "02257", "09311", "06403", "04718", "05378"}
TEST = ((1, 2, -1, -2, 2), (2, 2, 1))
GINV = {g: next(h for h in T.SYMS if T.apply_g(h, T.apply_g(g, TEST)) == TEST) for g in T.SYMS}
RMOVES = (0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13)


def frame_fin(g, m):
    if g == (0, 1, 1, 1):
        return [2, 0, 7, 5, 12, 2, 8] + [11] * (m - 1) + [3, 8, 11, 4, 2, 0] + [5] * (m - 1)
    return None


def loops(n):
    """all macro variants (flip, K) that verify, shortest first"""
    out = {}
    for flip in (False, True):
        for K in (0, 1, 2):
            try:
                p = build(n, K, flip)
            except Exception:
                p = None
            if p:
                out[tuple(p)] = 1
    return sorted((list(p) for p in out), key=len)


def best_loop(n):
    return loops(n)[0]


KMAX = 30
SLACK = 2


def run_row(cid, n, loop_list):
    m = 2 ** (n - 1)
    P = B.ms(n)
    pre = (tuple([-2] + [1] * m + [2, 2, -1]), (1, 1, -2, -1, 2))
    out = None
    for g in T.SYMS:
        if tuple(T.ccanon(x) for x in T.apply_g(g, P)) != tuple(T.ccanon(x) for x in T.REL[cid]):
            continue
        S0 = T.apply_g(GINV[g], T.REL[cid])
        bestpre = None
        for loop in loop_list:
            traj = [P]
            for mv in loop:
                traj.append(core.apply_move(traj[-1], mv))
            assert traj[-1] == pre
            for k in range(0, min(KMAX + 1, len(loop))):
                tgt = traj[k]
                cap = max(len(S0[0]) + len(S0[1]), len(tgt[0]) + len(tgt[1])) + SLACK
                p, _, _ = bidi(S0, tgt, cap, RMOVES)
                if p is not None and (bestpre is None or len(p) + len(loop) - k < len(bestpre[0]) + len(bestpre[2]) - bestpre[1]):
                    bestpre = (p, k, loop)
        if bestpre is None:
            continue
        loop = bestpre[2]
        canon = bestpre[0] + loop[bestpre[1]:]
        mapped = [T.mmap(g, mv) for mv in canon]
        cands = []
        tail = [T.mmap(g, mv) for mv in B.fin2(m)]
        e = T.REL[cid]
        for mv in mapped + tail:
            e = core.apply_move(e, mv)
        fin = T.finish(e)
        if fin is not None:
            cands.append(mapped + tail + fin)
        ff = frame_fin(g, m)
        if ff:
            cands.append(mapped + ff)
        for road in sorted(cands, key=len):
            if core.verify(T.CH[cid], road, "ac-r2-v1", T.man["limits"])["ok"]:
                # Stable: mapped fin2 ends at g(x, y); (y, x) -> + [15, 15]
                st_road = None
                endg = T.apply_g(g, T.GOAL)
                if endg == ((2,), (1,)):
                    st_road = mapped + tail + [15, 15]
                sac = "sac-" + cid[3:]
                stable = [road + [16, 15]] + ([st_road] if st_road else [])
                stable = [s for s in sorted(stable, key=len) if stable_core.verify(SR.CH[sac], s, "sac-r8-v1", SR.LIM).get("ok")]
                if out is None or len(road) < len(out[0]):
                    out = (road, stable[0] if stable else None, g, bestpre[1], len(bestpre[0]))
                break
    return out


def main():
    global KMAX, SLACK
    a, b = int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) > 3: KMAX = int(sys.argv[3])
    if len(sys.argv) > 4: SLACK = int(sys.argv[4])
    only = set(sys.argv[5].split(',')) if len(sys.argv) > 5 else None
    idx = {}
    for cid, p in T.REL.items():
        idx.setdefault(T.key(p), []).append(cid)
    lines = []
    for n in range(a, b + 1):
        ll = loops(n)
        loop = ll[0]
        print("n=%d canonical loop %d, road %d (%d variants)" % (n, len(loop), len(loop) + len(B.fin2(2 ** (n - 1))), len(ll)), flush=True)
        for cid in sorted(idx.get(T.key(B.ms(n)), [])):
            r = cid[-5:]
            if r in FORBID or (only and cid not in only):
                continue
            res = run_row(cid, n, ll[:3])
            rec, k = REC.get(r, (None, 0))
            srec, sk = SREC.get(r, (None, 0))
            if not res:
                print("  %s: no road" % cid, flush=True)
                continue
            road, st, g, kk, pl = res
            tag = "BEAT" if rec and len(road) < rec else ("TIE" if len(road) == rec else "over")
            stag = "-" if not st else ("BEAT" if srec and len(st) < srec else ("TIE" if len(st) == srec else "over"))
            print("  %s g=%s prefix %d->k%d: AC %d (rec %s k%s) %s | ST %s (rec %s k%s) %s" % (
                cid, g, pl, kk, len(road), rec, k, tag, len(st) if st else None, srec, sk, stag), flush=True)
            if tag != "over":
                lines.append("# n=%d AC %s: %d vs record %s (k%s)\n%s: [%s]\n" % (n, tag, len(road), rec, k, cid, ",".join(map(str, road))))
            if st and stag not in ("over", "-"):
                lines.append("# n=%d Stable %s: %d vs record %s (k%s)\nsac-%s: [%s]\n" % (n, stag, len(st), srec, sk, r, ",".join(map(str, st))))
    if lines:
        f = R + "research/acc/live/inbox/upgh_ladder_%s.txt" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        open(f, "w").write("# doubling-ladder roads (ladder_rows.py), replayed on the pinned official core\n" + "".join(lines))
        print("wrote", f)


if __name__ == "__main__":
    main()
