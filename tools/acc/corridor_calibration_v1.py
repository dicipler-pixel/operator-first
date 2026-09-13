#!/usr/bin/env python3
# SCRIPT: corridor_calibration
"""corridor_calibration v1 — exact finish-distance distribution for every ordinary-AC corridor state
of residual R (one relator a single letter g in either slot, the other a freely reduced word of length R
whose exponent sum in the *other* generator is ±1, so the pair presents the trivial group).
Forward BFS from each state to the target ((1,),(2,)) under the 14 official moves with total length
capped at (R+1)+cap.  Independent cross-check of the reverse-BFS table reported by the ChatGPT lane.
Python 3 stdlib only.
"""
import argparse, collections, itertools, json, os, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D
TARGET = ((1,), (2,)); GENS = (1, -1, 2, -2)

def words(R):
    for w in itertools.product(GENS, repeat=R):
        if all(a != -b for a, b in zip(w, w[1:])): yield w

def corridor_states(R):
    for g in GENS:
        other = 2 if abs(g) == 1 else 1
        for w in words(R):
            if abs(sum(1 if a == other else -1 if a == -other else 0 for a in w)) != 1: continue
            if R == 1 and len(w) == 1 and abs(w[0]) == abs(g): continue
            yield ((g,), w); yield (w, (g,))

def bfs_dist(core, start, cap, limit):
    if start == TARGET: return 0, 1
    seen = {start}; q = collections.deque([(start, 0)]); n = 0
    while q:
        s, d = q.popleft(); n += 1
        if n > limit: return None, n
        for m in range(core.NUM_MOVES):
            t = core.apply_move(s, m)
            if sum(len(w) for w in t) > cap or t in seen: continue
            if t == TARGET: return d + 1, n
            seen.add(t); q.append((t, d + 1))
    return None, n

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    ap.add_argument("--rmax", type=int, default=8); ap.add_argument("--cap", type=int, default=2); ap.add_argument("--limit", type=int, default=200000); a = ap.parse_args()
    core, _, _ = D.load_verifier(a.sair); rows = []
    print("| R | corridor states | shortest | median | 90% <= | worst | unsolved within cap |"); print("|---:|---:|---:|---:|---:|---:|---:|")
    for R in range(1, a.rmax + 1):
        ds = []; uns = 0
        for s in corridor_states(R):
            d, n = bfs_dist(core, s, R + 1 + a.cap, a.limit)
            if d is None: uns += 1
            else: ds.append(d)
        ds.sort(); p90 = ds[int(0.9 * (len(ds) - 1))]
        row = {"R": R, "states": len(ds) + uns, "min": ds[0], "median": st.median(ds), "p90": p90, "max": ds[-1], "unsolved": uns}
        rows.append(row); print(f"| {R} | {row['states']} | {row['min']} | {row['median']} | {p90} | {row['max']} | {uns} |", flush=True)
    json.dump({"cap": a.cap, "rows": rows}, open(os.path.join(HERE, f"corridor_calibration_v1_cap{a.cap}.json"), "w"), indent=1)

if __name__ == "__main__": main()
