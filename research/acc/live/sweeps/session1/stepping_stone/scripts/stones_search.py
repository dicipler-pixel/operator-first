#!/usr/bin/env python3
"""Idea A (stepping stones) and the lookup half of idea B.

Builds a Store of every state on every held verified road (AC roads ending at (x,y); the AC part of Stable lines
ending at (x,y) or (y,x)), keyed by the exact 16-symmetry normal form, plus optional backward-walk files from
walks.py (idea B).  Then, for each target row, runs a capped BFS outward from the target's official start
(depth <= D, every state's relator total <= cap, at most N states) and looks every reached state up in the Store.
A hit gives: target prefix (BFS path) + donor tail mapped by the symmetry + exact finish.  Every candidate is
replayed on the official core before it is written.

usage: stones_search.py --sair DIR --roads FILE --targets FILE [--walks F ...] --out PREFIX
                        [--depth 8] [--slack 6] [--capmin 0] [--maxstates 1500000] [--shard i/n]
targets file: lines `row,our_best,record` (row = ac-XXXXX or sac-XXXXX; our_best/record may be empty)."""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stones_lib as S  # noqa: E402


HALO = 0


def build_store(roads_file, walk_files, REL, log):
    st = S.Store()
    n = 0
    for cid, mv in S.read_roads(roads_file):
        a = []
        for m in mv:
            if m >= 14:
                break
            a.append(m)
        start = REL.get("ac-" + cid.split("-")[1])
        if start is None:
            continue
        end = S.run(start, a)
        if end not in (S.GOAL, S.YX):
            continue
        st.add_path(start, a, end, tag="ac-" + cid.split("-")[1])
        n += 1
    log("store: %d road paths -> %d normal-form states" % (n, len(st.d)))
    st.n_road = len(st.src)
    if HALO:
        k0 = len(st.d)
        st.add_halo(maxlen=HALO)
        log("store: radius-1 halo around road states (len<=%d) -> +%d states (total %d)" % (HALO, len(st.d) - k0, len(st.d)))
    for wf in walk_files or []:
        k0, nw = len(st.d), 0
        for line in open(wf):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fw = json.loads(line.split(":", 1)[1])          # forward walk moves from the goal
            end = S.run(S.GOAL, fw)
            back = [S.INV[m] for m in reversed(fw)]          # road from the walk's end back to the goal
            st.add_path(end, back, S.GOAL, tag="walk")
            nw += 1
        log("store: +%d walks from %s -> +%d new states (total %d)" % (nw, wf, len(st.d) - k0, len(st.d)))
    return st


def search(st, start, depth, cap, maxstates):
    """BFS from start. Returns (parents, best_hits sorted, stats)."""
    par = {start: None}
    frontier = [start]
    hits = {}
    nlook = 0
    done_depth = 0
    full = True
    for d in range(0, depth + 1):
        for s in frontier:
            h = st.d.get(S.norm(s))
            nlook += 1
            if h is not None:
                hits[s] = (d + h[0], d)
        if d == depth:
            break
        nxt = []
        for s in frontier:
            for m in range(14):
                t = S.apply(s, m)
                if t in par or S.L(t) > cap:
                    continue
                par[t] = (s, m)
                nxt.append(t)
        if len(par) > maxstates:
            full = False
            # still look the partial layer up, but stop expanding
            for s in nxt:
                h = st.d.get(S.norm(s))
                nlook += 1
                if h is not None:
                    hits[s] = (d + 1 + h[0], d + 1)
            done_depth = d
            break
        frontier = nxt
        done_depth = d + 1
        if not nxt:
            break
    return par, hits, dict(states=len(par), looked=nlook, depth_done=done_depth, complete=full)


def prefix(par, t):
    out = []
    while par[t] is not None:
        s, m = par[t]
        out.append(m)
        t = s
    return out[::-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sair", required=True)
    ap.add_argument("--roads", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--walks", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--depth", type=int, default=8)
    ap.add_argument("--slack", type=int, default=6)
    ap.add_argument("--capmin", type=int, default=0)
    ap.add_argument("--maxstates", type=int, default=1500000)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--recon", type=int, default=12, help="reconstruct this many best hits per target")
    ap.add_argument("--halo", type=int, default=0, help="add radius-1 halo of road states up to this length")
    a = ap.parse_args()
    global HALO
    HALO = a.halo
    t0 = time.time()
    logf = open(a.out + ".log", "w")

    def log(*x):
        msg = " ".join(map(str, x))
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    core, man = S.load_core(a.sair)
    from verifier import specs
    REL = S.rel_of(man)
    CH = {c["challenge_id"]: c for c in man["challenges"]}
    st = build_store(a.roads, a.walks, REL, log)
    log("store built %.0fs" % (time.time() - t0))
    i, n = map(int, a.shard.split("/"))
    tg = []
    for line in open(a.targets):
        f = line.strip().split(",")
        if not f[0] or f[0].startswith("#"):
            continue
        tg.append((f[0], int(f[1]) if len(f) > 1 and f[1] else None, int(f[2]) if len(f) > 2 and f[2] else None))
    n_road = st.n_road
    groups = {}
    for cid, ours, rec in tg:
        groups.setdefault("ac-" + cid.split("-")[1], []).append((cid, ours, rec))
    keys = list(groups)[i::n]
    roads_out = open(a.out + "_roads.txt", "w")
    summ = open(a.out + "_summary.tsv", "w")
    summ.write("row\tstart_len\tcap\tstates\tdepth_done\tcomplete\thits_road\thits_walk\tbest_road_src\t"
               "best_walk_src\tour_best\trecord\tforeign_hits\tbest_foreign_est\tforeign_donors\tnote\n")
    for acid in keys:
        tt = time.time()
        start = REL[acid]
        cap = max(S.L(start) + a.slack, a.capmin)
        par, hits, stats = search(st, start, a.depth, cap, a.maxstates)
        hr = {t: v for t, v in hits.items() if st.d[S.norm(t)][1] < n_road and True}
        hw = {t: v for t, v in hits.items() if st.d[S.norm(t)][1] >= n_road}
        hf = {t: v for t, v in hr.items() if st.tag_of(t) != acid}
        fdon = sorted({st.tag_of(t) for t in hf})
        for cid, ours, rec in groups[acid]:
            sac = cid.startswith("sac-")
            ends = (S.GOAL, S.YX) if sac else (S.GOAL,)
            res, note = {}, ""
            for kind, hh in (("road", hr), ("walk", hw)):
                best = None
                for t, (est, d) in sorted(hh.items(), key=lambda kv: kv[1])[: a.recon]:
                    tail = st.road_from(t, ends)
                    if tail is None:
                        continue
                    p = prefix(par, t) + tail
                    if sac:
                        e = S.run(start, p)
                        p = p + ([16, 15] if e == S.GOAL else [15, 15])
                    v = specs.verify_challenge(CH[cid], p, CH[cid]["move_spec_version"], man["limits"])
                    if not v.get("ok"):
                        note += " REPLAY-FAIL(%s) %s" % (kind, str(v)[:80])
                        continue
                    if best is None or len(p) < len(best):
                        best = p
                res[kind] = best
            cands = [b for b in res.values() if b]
            best = min(cands, key=len) if cands else None
            if best is not None and (ours is None or len(best) < ours):
                roads_out.write("%s: [%s]\n" % (cid, ",".join(map(str, best))))
                roads_out.flush()
                note += " NEW(shorter than ours)" if ours is not None else " NEW ROAD (row had none)"
            lr = len(res["road"]) if res.get("road") else None
            lw = len(res["walk"]) if res.get("walk") else None
            bf = min((v[0] for v in hf.values()), default=None)
            summ.write("%s\t%d\t%d\t%d\t%d\t%s\t%d\t%d\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s\n" % (
                cid, S.L(start), cap, stats["states"], stats["depth_done"], stats["complete"], len(hr), len(hw), lr, lw,
                ours, rec, len(hf), bf, " ".join(fdon[:8]), note.strip()))
            summ.flush()
            log("%s L=%d cap=%d states=%d depth=%d complete=%s hits road/walk=%d/%d best road/walk=%s/%s ours=%s rec=%s foreign=%d(best est %s) %s (%.0fs)" % (
                cid, S.L(start), cap, stats["states"], stats["depth_done"], stats["complete"], len(hr), len(hw), lr, lw,
                ours, rec, len(hf), bf, note, time.time() - tt))
        del par, hits
    log("done %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
