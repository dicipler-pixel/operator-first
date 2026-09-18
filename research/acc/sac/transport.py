"""Splice an open row into a path we already hold.

Index every exact state visited along our known solutions. Then BFS out from
each unsolved row; the first time we land on an indexed state, the rest of
that known path finishes the job. Exact state equality, so the spliced path
replays or it does not.
"""
import json, re, sys, time
sys.path.insert(0, "tools/acc/eyes")
import replay as R

LET = {"x": 0, "x^-1": 1, "y": 2, "y^-1": 3}

def load_board():
    out = {}
    for line in open("research/acc/sac/stable_ac.jsonl", errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        b = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        ws = [tuple(LET[t] for t in q.replace("= 1", "").strip().split())
              for q in b.split(";")]
        out[d["challenge_id"]] = (ws[0], ws[1])
    return out

def build_index(board, paths):
    """state -> moves remaining to reach (x, y)."""
    idx = {}
    for cid, mv in paths.items():
        st = (tuple(R.free_reduce(list(board[cid][0]))),
              tuple(R.free_reduce(list(board[cid][1]))))
        seq = [st]
        for m in mv:
            a, b = R.apply_move(list(st[0]), list(st[1]), m)
            st = (tuple(a), tuple(b))
            seq.append(st)
        for i, s in enumerate(seq):
            rest = mv[i:]
            if s not in idx or len(rest) < len(idx[s]):
                idx[s] = list(rest)
    return idx

def main():
    board = load_board()
    paths = {}
    for line in open("research/acc/sac/BEST.txt"):
        line = line.strip()
        if not line:
            continue
        c, r = line.split(":", 1)
        c = c.strip()
        mv = json.loads(r.strip())
        sid = c if c.startswith("sac-") else "sac-" + c.split("-")[1]
        mv = mv[:-2] if c.startswith("sac-") else mv     # keep the rank-2 prefix
        if sid not in paths or len(mv) < len(paths[sid]):
            paths[sid] = mv
    idx = build_index(board, paths)
    print(f"indexed {len(idx):,} states from {len(paths)} known paths", flush=True)

    status = {r["challengeId"].replace("ac-", "sac-"): r["status"]
              for r in json.load(open("tools/acc/acc_board_20260916_v1.json"))}
    targets = [c for c in sorted(board) if status.get(c) != "solved"]
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    t0 = time.time()
    found = 0
    out = open("research/acc/sac/TRANSPORT.jsonl", "w")
    for n, cid in enumerate(targets, 1):
        start = (tuple(R.free_reduce(list(board[cid][0]))),
                 tuple(R.free_reduce(list(board[cid][1]))))
        seen = {start: []}
        frontier = [start]
        hit = None
        for _d in range(depth):
            nxt = []
            for st in frontier:
                for m in range(14):
                    a, b = R.apply_move(list(st[0]), list(st[1]), m)
                    if not a or not b or len(a) > 40 or len(b) > 40:
                        continue
                    k = (tuple(a), tuple(b))
                    if k in seen:
                        continue
                    seen[k] = seen[st] + [m]
                    if k in idx:
                        hit = seen[k] + idx[k]
                        break
                    nxt.append(k)
                if hit:
                    break
            if hit:
                break
            frontier = nxt
        if hit:
            _a, _b, ok = R.replay(board[cid][0], board[cid][1], hit)
            if ok:
                found += 1
                out.write(json.dumps({"id": cid, "len": len(hit) + 2,
                                      "moves": hit + [16, 15]}) + "\n")
                out.flush()
                print(f"  +++ {cid} SOLVED {len(hit)+2} moves (OPEN ROW)", flush=True)
        if n % 200 == 0:
            print(f"  .. {n}/{len(targets)} {found} found ({time.time()-t0:.0f}s)", flush=True)
    print(f"DONE {len(targets)} open rows, {found} spliced, {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
