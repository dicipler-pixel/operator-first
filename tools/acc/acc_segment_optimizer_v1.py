#!/usr/bin/env python3
# SCRIPT: acc_segment_optimizer
"""acc_segment_optimizer v1 — exact whole-path shortening for ordinary-AC certificates.

For every accepted path: (1) cut any revisited state (an exact loop); (2) slide a window of W moves over
the whole path and, for each window [i, i+W], search for a strictly shorter move sequence from states[i]
to states[i+W] by meet-in-the-middle BFS over the 14 official moves (backward side uses the official
inverse ids, which invert exactly on freely reduced states), with every intermediate state's total
length capped at the window's own maximum (+extra).  A found segment is spliced in and the scan restarts
around it, until no window improves.  Final path re-verified by the official verify(); only accepted
paths are written.  Never overwrites.  Python 3 stdlib only.
"""
import argparse, json, os, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D
G = {}

def init(sair):
    core, sc, specs = D.load_verifier(sair); limits, manifest = D.load_manifest(sair)
    G.update(core=core, verify=specs.get("ac-r2-v1").verify, limits=limits, manifest=manifest, inv=[r["inverse"] for r in core.MOVE_TABLE])

def L(s): return sum(len(w) for w in s)

def states_of(core, c, moves):
    s = tuple(tuple(w) for w in c["initial_relators"]); out = [s]
    for m in moves: s = core.apply_move(s, m); out.append(s)
    return out

def cut_loops(moves, states):
    """Remove the longest loops first: if a state repeats at i<j, drop moves[i:j]."""
    changed = True
    while changed:
        changed = False; first = {}
        for k, s in enumerate(states):
            if s in first:
                i = first[s]; moves = moves[:i] + moves[k:]; states = states[:i] + states[k:]; changed = True; break
            first[s] = k
    return moves, states

def meet(core, inv, start, goal, maxlen, cap, node_limit):
    """Shortest path start->goal of length <= maxlen with all states <= cap, or None. Bidirectional BFS."""
    if start == goal: return []
    fw = {start: None}; bw = {goal: None}; ff = [start]; bf = [goal]; df = db = 0; n = 0
    def build(mid):
        p = []; cur = mid
        while fw[cur] is not None: s, m = fw[cur]; p.append(m); cur = s
        p.reverse(); cur = mid
        while bw[cur] is not None: s, m = bw[cur]; p.append(inv[m]); cur = s   # bw stores the move applied FROM goal side (an inverse); re-invert
        return p
    while ff and bf and df + db < maxlen:
        if len(ff) <= len(bf):
            nxt = []
            for s in ff:
                for m in range(core.NUM_MOVES):
                    t = core.apply_move(s, m); n += 1
                    if L(t) > cap or t in fw: continue
                    fw[t] = (s, m)
                    if t in bw: return build(t)
                    nxt.append(t)
            ff = nxt; df += 1
        else:
            nxt = []
            for s in bf:
                for m in range(core.NUM_MOVES):
                    t = core.apply_move(s, m); n += 1
                    if L(t) > cap or t in bw: continue
                    bw[t] = (s, m)
                    if t in fw: return build(t)
                    nxt.append(t)
            bf = nxt; db += 1
        if n > node_limit: return None
    return None

def optimize(args):
    cid, moves, W, extra, node_limit = args
    core, inv = G["core"], G["inv"]; c, spec = D.resolve_challenge(cid, G["manifest"], {})
    if c is None or spec != "ac-r2-v1": return {"challenge_id": cid, "action": "passthrough"}, moves
    v0 = G["verify"](c, moves, spec, G["limits"])
    if not v0.get("ok"): return {"challenge_id": cid, "action": "rejected_original"}, None
    n0 = len(moves); states = states_of(core, c, moves); moves, states = cut_loops(list(moves), states); loops = n0 - len(moves)
    i = 0; windows = 0; splices = 0; t0 = time.time()
    while i + 2 <= len(moves):
        j = min(len(moves), i + W); seg = states[i:j + 1]; cap = max(L(s) for s in seg) + extra
        windows += 1
        p = meet(core, inv, states[i], states[j], j - i - 1, cap, node_limit)
        if p is not None and len(p) < j - i:
            moves = moves[:i] + p + moves[j:]; states = states_of(core, c, moves); splices += 1; i = max(0, i - W)
        else:
            i += 1
    v1 = G["verify"](c, moves, spec, G["limits"])
    rec = {"challenge_id": cid, "len": n0, "loops_cut": loops, "windows": windows, "splices": splices, "new_len": len(moves), "saved": n0 - len(moves), "verify_ok": bool(v1.get("ok")), "seconds": round(time.time() - t0, 1)}
    if not v1.get("ok"): rec["action"] = "splice_rejected"; return rec, None
    rec["action"] = "shortened" if len(moves) < n0 else "kept"; return rec, moves

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    ap.add_argument("--submission", required=True); ap.add_argument("--window", type=int, default=10); ap.add_argument("--extra-cap", type=int, default=0)
    ap.add_argument("--node-limit", type=int, default=400_000); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--out", required=True); a = ap.parse_args()
    if os.path.exists(a.out): print("refusing to overwrite", a.out); sys.exit(2)
    runs = D.parse_submission(a.submission); t0 = time.time()
    with Pool(a.workers, initializer=init, initargs=(a.sair,)) as pool:
        results = pool.map(optimize, [(cid, m, a.window, a.extra_cap, a.node_limit) for cid, m in runs], chunksize=1)
    init(a.sair)
    rep = {"tool": "acc_segment_optimizer v1", "window": a.window, "extra_cap": a.extra_cap, "paths": len(runs), "shortened": 0, "kept": 0, "rejected": 0, "moves_saved": 0, "loops_cut": 0, "runs": []}
    out = []
    for (cid, orig), (rec, final) in zip(runs, results):
        rep["runs"].append(rec)
        if rec["action"] == "shortened": rep["shortened"] += 1; rep["moves_saved"] += rec["saved"]; rep["loops_cut"] += rec["loops_cut"]
        elif rec["action"] == "kept": rep["kept"] += 1
        elif rec["action"] != "passthrough": rep["rejected"] += 1
        if final is not None: out.append(f"{cid}: {json.dumps(final, separators=(',', ':'))}")
    rep["seconds"] = round(time.time() - t0, 1)
    open(a.out, "w").write(f"# acc_segment_optimizer v1 (window {a.window}, meet-in-the-middle, cap = window's own peak +{a.extra_cap}); every line re-verified\n" + "\n".join(out) + "\n")
    json.dump(rep, open(a.out + ".report.json", "w"), indent=1); print(json.dumps({k: v for k, v in rep.items() if k != "runs"}, indent=1))
if __name__ == "__main__": main()
