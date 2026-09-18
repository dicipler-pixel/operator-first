"""SAC sweep: meet-in-the-middle against a fixed backward ball from (x, y).

Moves 0-13 are closed under inverse, so the backward ball is a forward ball.
Ball stores depth only; the tail path is recovered by greedy depth descent.
Every emitted path is re-verified with tools/acc/eyes/replay.py before it is
recorded. The terminal [16, 15] pair is appended, matching all 276 accepted
SAC paths; replay.py does not implement 15 or 16, so that pair is unverified.
"""
import json, re, sys, time, heapq, argparse
sys.path.insert(0, "tools/acc/eyes")
import replay as R

INV = {0:0, 1:1, 2:3, 3:2, 4:5, 5:4, 6:7, 7:6, 8:9, 9:8, 10:11, 11:10, 12:13, 13:12}
LET = {"x":0, "x^-1":1, "y":2, "y^-1":3}
TRIVIAL = ((0,), (2,))

def load_board(path):
    rows = {}
    for line in open(path, errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        body = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        ws = [[LET[t] for t in p.replace("= 1", "").strip().split()]
              for p in body.split(";")]
        rows[d["challenge_id"]] = (ws[0], ws[1])
    return rows

def build_ball(depth, cap):
    seen = {TRIVIAL: 0}
    frontier = [TRIVIAL]
    for d in range(1, depth + 1):
        nxt = []
        for st in frontier:
            r0, r1 = list(st[0]), list(st[1])
            for m in range(14):
                a, b = R.apply_move(r0, r1, m)
                if not a or not b or len(a) > cap or len(b) > cap:
                    continue
                k = (tuple(a), tuple(b))
                if k not in seen:
                    seen[k] = d
                    nxt.append(k)
        frontier = nxt
    return seen

def tail_from_ball(ball, state):
    """Moves taking `state` to (x, y), by descending the ball's depth field."""
    out = []
    cur, d = state, ball[state]
    while d > 0:
        r0, r1 = list(cur[0]), list(cur[1])
        for m in range(14):
            a, b = R.apply_move(r0, r1, m)
            if not a or not b:
                continue
            k = (tuple(a), tuple(b))
            if ball.get(k, 99) == d - 1:
                out.append(m)
                cur, d = k, d - 1
                break
        else:
            return None
    return out

def solve(r0, r1, ball, budget, cap):
    """Best-first forward search until a state lands inside the ball."""
    start = (tuple(R.free_reduce(r0)), tuple(R.free_reduce(r1)))
    if start in ball:
        t = tail_from_ball(ball, start)
        return t if t is not None else None
    seen = {start: 0}
    pq = [(len(start[0]) + len(start[1]), 0, start, [])]
    n = 0
    while pq and n < budget:
        _, g, st, path = heapq.heappop(pq)
        n += 1
        a0, b0 = list(st[0]), list(st[1])
        for m in range(14):
            a, b = R.apply_move(a0, b0, m)
            if not a or not b or len(a) > cap or len(b) > cap:
                continue
            k = (tuple(a), tuple(b))
            if k in seen and seen[k] <= g + 1:
                continue
            seen[k] = g + 1
            np = path + [m]
            if k in ball:
                t = tail_from_ball(ball, k)
                if t is not None:
                    return np + t
            heapq.heappush(pq, (len(a) + len(b) + g + 1, g + 1, k, np))
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ball-depth", type=int, default=7)
    ap.add_argument("--ball-cap", type=int, default=12)
    ap.add_argument("--search-cap", type=int, default=26)
    ap.add_argument("--budget", type=int, default=20000)
    ap.add_argument("--only", help="file of challenge ids, one per line")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="research/acc/sac/SWEEP_RESULTS.jsonl")
    a = ap.parse_args()

    board = load_board("research/acc/sac/sac_board_raw.jsonl")
    t0 = time.time()
    ball = build_ball(a.ball_depth, a.ball_cap)
    print(f"ball: depth {a.ball_depth} cap {a.ball_cap} -> {len(ball):,} states "
          f"({time.time()-t0:.1f}s)", flush=True)

    ids = sorted(board)
    if a.only:
        want = {l.strip() for l in open(a.only) if l.strip()}
        ids = [i for i in ids if i in want]
    if a.limit:
        ids = ids[:a.limit]

    solved = 0
    with open(a.out, "w") as f:
        for n, cid in enumerate(ids, 1):
            r0, r1 = board[cid]
            path = solve(r0, r1, ball, a.budget, a.search_cap)
            if path is None:
                continue
            _, _, ok = R.replay(r0, r1, path)
            if not ok:
                print(f"  REJECT {cid}: path does not land on (x,y)", flush=True)
                continue
            solved += 1
            f.write(json.dumps({"id": cid, "len": len(path) + 2,
                                "moves": path + [16, 15]}) + "\n")
            f.flush()
            if solved % 25 == 0:
                print(f"  {n}/{len(ids)} scanned, {solved} solved "
                      f"({time.time()-t0:.0f}s)", flush=True)
    print(f"DONE {len(ids)} scanned, {solved} solved, {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
