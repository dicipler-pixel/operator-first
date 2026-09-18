"""Shorten an existing SAC path by re-searching every window of it.

Replay the path to get its state sequence, then for each window
(s_i .. s_{i+w}) run an exact bidirectional BFS between the endpoints.
If the true distance is shorter than the window, splice the shorter
connection in. Repeat until no window improves. Purely a rewrite of a
path that already works, so the result is always still a valid path.
"""
import json, re, sys, time
sys.path.insert(0, "tools/acc/eyes")
import replay_sac as S

RANK2 = list(range(14))          # moves legal at rank 2, excluding (de)stabilize
LET = {"x": 1, "x^-1": -1, "y": 2, "y^-1": -2}

def load_board(path):
    out = {}
    for line in open(path, errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        b = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        ws = [tuple(LET[t] for t in p.replace("= 1", "").strip().split())
              for p in b.split(";")]
        out[d["challenge_id"]] = tuple(ws)
    return out

def states_along(initial, moves):
    st = tuple(S.free_reduce(tuple(r)) for r in initial)
    seq = [st]
    for m in moves:
        st, reason = S.apply_move(st, m)
        if st is None:
            return None
        seq.append(st)
    return seq

def bfs_between(a, b, maxd):
    """Exact shortest move list a -> b within maxd, rank-2 moves, bidirectional."""
    if a == b:
        return []
    INV = {0:0, 1:1, 2:3, 3:2, 4:5, 5:4, 6:7, 7:6, 8:9, 9:8, 10:11, 11:10, 12:13, 13:12}
    def step(st):
        for m in RANK2:
            ns, _r = S.apply_move(st, m)
            if ns is None or any(len(w) == 0 or len(w) > 40 for w in ns):
                continue
            yield m, ns
    fwd, bwd = {a: []}, {b: []}
    ff, bf = [a], [b]
    for d in range(maxd):
        # expand the smaller side
        if len(ff) <= len(bf):
            nxt = []
            for st in ff:
                for m, ns in step(st):
                    if ns in fwd:
                        continue
                    fwd[ns] = fwd[st] + [m]
                    if ns in bwd:
                        return fwd[ns] + [INV[x] for x in reversed(bwd[ns])]
                    nxt.append(ns)
            ff = nxt
        else:
            nxt = []
            for st in bf:
                for m, ns in step(st):
                    if ns in bwd:
                        continue
                    bwd[ns] = bwd[st] + [m]
                    if ns in fwd:
                        return fwd[ns] + [INV[x] for x in reversed(bwd[ns])]
                    nxt.append(ns)
            bf = nxt
        if not ff or not bf:
            break
    return None

def compress(initial, moves, window=8, rounds=5):
    cur = list(moves)
    for _ in range(rounds):
        seq = states_along(initial, cur)
        if seq is None:
            return cur
        improved = False
        i = 0
        while i < len(cur):
            hi = min(i + window, len(cur))
            for j in range(hi, i + 1, -1):
                span = j - i
                # only rank-2 windows: skip any window containing a rank move
                if any(m >= 14 for m in cur[i:j]):
                    continue
                short = bfs_between(seq[i], seq[j], span - 1)
                if short is not None and len(short) < span:
                    cur = cur[:i] + short + cur[j:]
                    improved = True
                    break
            else:
                i += 1
                continue
            seq = states_along(initial, cur)
            if seq is None:
                return cur
        if not improved:
            break
    return cur

def main():
    board = load_board("research/acc/sac/stable_ac.jsonl")
    src = sys.argv[1]
    out = sys.argv[2]
    rows = []
    for line in open(src):
        line = line.strip()
        if not line:
            continue
        cid, rest = line.split(":", 1)
        rows.append((cid.strip(), json.loads(rest.strip())))
    t0 = time.time()
    wins = 0
    with open(out, "w") as f:
        for n, (cid, moves) in enumerate(rows, 1):
            tail = moves[-2:] if moves[-2:] == [16, 15] else []
            short = compress(board[cid], moves[:-2] if tail else moves) + tail
            ok, why = S.verify(board[cid], short)
            if not ok:
                print(f"  REJECT {cid}: {why}", flush=True)
                continue
            if len(short) < len(moves):
                wins += 1
                f.write(json.dumps({"id": cid, "len": len(short),
                                    "was": len(moves), "moves": short}) + "\n")
                f.flush()
                print(f"  +{cid}  {len(moves)} -> {len(short)}  (-{len(moves)-len(short)})"
                      f"  [{n}/{len(rows)}, {wins} wins, {time.time()-t0:.0f}s]", flush=True)
            elif n % 25 == 0:
                print(f"  .. {n}/{len(rows)}, {wins} wins, {time.time()-t0:.0f}s", flush=True)
    print(f"DONE {len(rows)} rows, {wins} shortened, {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
