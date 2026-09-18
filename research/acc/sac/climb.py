"""Search for open rows, which all sit at a local minimum of total length.

Every unsolved row the harness profiled has zero length-reducing moves, so a
best-first search keyed on total length has no gradient and stalls. This
solver keys on the abelianised distance dM (exponent-sum matrix -> identity
under row operations) and tolerates length increases up to a slack bound,
meeting the same fixed ball around the trivial presentation.
"""
import json, re, sys, time, heapq, argparse
sys.path.insert(0, "tools/acc/eyes")
import replay as R

LET = {"x": 0, "x^-1": 1, "y": 2, "y^-1": 3}
TRIVIAL = ((0,), (2,))

def load_board(p):
    out = {}
    for line in open(p, errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        b = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        ws = [tuple(LET[t] for t in q.replace("= 1", "").strip().split())
              for q in b.split(";")]
        out[d["challenge_id"]] = (ws[0], ws[1])
    return out

def expsum(w):
    return (sum(1 if c == 0 else -1 if c == 1 else 0 for c in w),
            sum(1 if c == 2 else -1 if c == 3 else 0 for c in w))

def dM(st):
    """Row-operation distance of the exponent-sum matrix to the identity."""
    (a, b), (c, d) = expsum(st[0]), expsum(st[1])
    n = 0
    while n < 12:
        if (a, b, c, d) == (1, 0, 0, 1):
            return n
        # one Euclidean row-reduction step
        if abs(c) > abs(a) and a:
            q = round(c / a) if a else 0
            c, d = c - q * a, d - q * b
        elif abs(a) > abs(c) and c:
            q = round(a / c)
            a, b = a - q * c, b - q * d
        elif abs(b) > abs(d) and d:
            q = round(b / d)
            a, b = a - q * c, b - q * d
        elif abs(d) > abs(b) and b:
            q = round(d / b)
            c, d = c - q * a, d - q * b
        else:
            break
        n += 1
    return 12

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

def tail(ball, state):
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

def solve(r0, r1, ball, budget, slack):
    """Best-first on dM with a length-slack bound. Parent pointers, not
    stored move lists, so memory stays proportional to states visited."""
    start = (tuple(R.free_reduce(list(r0))), tuple(R.free_reduce(list(r1))))
    cap = len(start[0]) + len(start[1]) + slack
    if start in ball:
        return tail(ball, start)
    parent = {start: (None, None)}       # state -> (prev, move)
    depth = {start: 0}
    pq = [(dM(start), 0, start)]
    n = 0

    def rebuild(st):
        out = []
        while parent[st][0] is not None:
            st, m = parent[st]
            out.append(m)
        return list(reversed(out))

    while pq and n < budget:
        _, g, st = heapq.heappop(pq)
        n += 1
        if depth.get(st, 1 << 30) < g:
            continue
        a0, b0 = list(st[0]), list(st[1])
        for m in range(14):
            a, b = R.apply_move(a0, b0, m)
            if not a or not b or len(a) + len(b) > cap:
                continue
            k = (tuple(a), tuple(b))
            if k in depth and depth[k] <= g + 1:
                continue
            depth[k] = g + 1
            parent[k] = (st, m)
            if k in ball:
                t = tail(ball, k)
                if t is not None:
                    return rebuild(k) + t
            heapq.heappush(pq, (dM(k) * 4 + (len(a) + len(b)) // 4 + g, g + 1, k))
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--budget", type=int, default=120000)
    ap.add_argument("--slack", type=int, default=12)
    ap.add_argument("--ball-depth", type=int, default=7)
    ap.add_argument("--ball-cap", type=int, default=12)
    a = ap.parse_args()

    board = load_board("research/acc/sac/stable_ac.jsonl")
    ids = [l.strip() for l in open(a.ids) if l.strip()]
    si, sn = (int(v) for v in a.shard.split("/"))
    ids = [c for n, c in enumerate(ids) if n % sn == si]
    t0 = time.time()
    ball = build_ball(a.ball_depth, a.ball_cap)
    print(f"ball {len(ball):,}  targets {len(ids)}  ({time.time()-t0:.0f}s)", flush=True)
    solved = 0
    with open(a.out, "w") as f:
        for n, cid in enumerate(ids, 1):
            r0, r1 = board[cid]
            p = solve(r0, r1, ball, a.budget, a.slack)
            if p is None:
                if n % 20 == 0:
                    print(f"  .. {n}/{len(ids)} {solved} solved ({time.time()-t0:.0f}s)", flush=True)
                continue
            _a, _b, ok = R.replay(r0, r1, p)
            if not ok:
                print(f"  REJECT {cid}", flush=True)
                continue
            solved += 1
            f.write(json.dumps({"id": cid, "len": len(p) + 2, "moves": p + [16, 15]}) + "\n")
            f.flush()
            print(f"  +++ {cid} SOLVED {len(p)+2} moves  (open row)", flush=True)
    print(f"DONE {len(ids)} scanned, {solved} solved, {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
