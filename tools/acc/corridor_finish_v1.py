#!/usr/bin/env python3
# SCRIPT: corridor_finish
"""corridor_finish v1 — exact bounded BFS from each training run's penultimate-corridor entry
state to the target ((1,),(2,)), using only verifier.core.apply_move, with total length capped at
L_entry + cap.  Compares the shortest capped finish with the official tail (moves after entry).
Every found finish is re-verified by the official verify() on the full spliced path.
Python 3 stdlib only.  Exact results only; no heuristics.
"""
import json, os, sys, collections, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D

def bfs(core, start, target, cap, node_limit):
    seen = {start: None}; q = collections.deque([start]); n = 0
    while q:
        s = q.popleft(); n += 1
        if n > node_limit: return None, n
        for m in range(core.NUM_MOVES):
            t = core.apply_move(s, m)
            if sum(len(w) for w in t) > cap or t in seen: continue
            seen[t] = (s, m)
            if t == target:
                path = []; cur = t
                while seen[cur] is not None:
                    p, mm = seen[cur]; path.append(mm); cur = p
                return path[::-1], n
            q.append(t)
    return None, n

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    ap.add_argument("--cap", type=int, default=2); ap.add_argument("--node-limit", type=int, default=300000); a = ap.parse_args()
    core, stable_core, specs = D.load_verifier(a.sair); limits, _ = D.load_manifest(a.sair)
    target = ((1,), (2,)); out = []; shorter = equal = longer = unsolved = 0; saved_total = 0
    for c, moves in D.load_training(a.sair, "ac-r2-v1"):
        state = tuple(tuple(w) for w in c["initial_relators"]); states = [state]
        for m in moves: state = core.apply_move(state, m); states.append(state)
        entry = next(k for k, s in enumerate(states) if (len(s[0]) == 1) != (len(s[1]) == 1))
        L = sum(len(w) for w in states[entry]); tail = len(moves) - entry
        path, n = bfs(core, states[entry], target, L + a.cap, a.node_limit)
        rec = {"id": c["challenge_id"], "entry": entry, "L_entry": L, "official_tail": tail, "bfs_nodes": n}
        if path is None:
            unsolved += 1; rec["finish"] = None
        else:
            spliced = list(moves[:entry]) + path
            v = specs.get("ac-r2-v1").verify(c, spliced, "ac-r2-v1", limits)
            ok = getattr(v, "ok", None) if not isinstance(v, dict) else v.get("ok")
            rec.update({"finish": path, "finish_len": len(path), "spliced_len": len(spliced), "verify": str(v)[:80], "verify_ok": bool(ok)})
            if not ok: print("VERIFY FAIL", rec); sys.exit(2)
            if len(path) < tail: shorter += 1; saved_total += tail - len(path)
            elif len(path) == tail: equal += 1
            else: longer += 1
        out.append(rec)
    summ = {"cap_over_entry_length": a.cap, "runs": len(out), "finish_shorter_than_official": shorter, "equal": equal,
            "longer_or_needs_higher_cap": longer, "unsolved_within_cap": unsolved, "total_moves_saved": saved_total,
            "max_bfs_nodes": max(r["bfs_nodes"] for r in out)}
    json.dump({"summary": summ, "runs": out}, open(os.path.join(HERE, f"corridor_finish_v1_cap{a.cap}.json"), "w"), indent=1)
    print(json.dumps(summ, indent=1))
    for r in sorted([r for r in out if r["finish"] is not None and r["finish_len"] < r["official_tail"]], key=lambda r: r["official_tail"] - r["finish_len"], reverse=True)[:8]:
        print(r["id"], "entry", r["entry"], "L", r["L_entry"], "official tail", r["official_tail"], "->", r["finish_len"], "spliced", r["spliced_len"])
if __name__ == "__main__": main()
