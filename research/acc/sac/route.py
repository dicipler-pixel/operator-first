"""Beam whose cost is the recorded routing eyes, not raw total length.

The census showed total relator length is flat on every unsolved row, so a
beam keyed on it has no gradient there. The scoring trial ranked the routing
eyes by recorded signal against remaining distance:

    len_r1 .808   floor .702   cyc_tot .663   tot .659
    cyc_x_balance .4505   cancel_trap .4338   advance_bias .3871

cyc_total was marked REDUNDANT at novelty 0, so it carries no weight of its
own here. Weights are those recorded signals, normalised.
"""
import json, re, sys, time, random
sys.path.insert(0, "tools/acc/eyes")
import replay as R

LET = {"x": 0, "x^-1": 1, "y": 2, "y^-1": 3}
TRIVIAL = ((0,), (2,))
W = {"len_r1": 0.808, "floor": 0.702, "tot": 0.659,
     "cyc_x_balance": 0.4505, "cancel_trap": 0.4338}

def cyc(w):
    return R.cyclic_reduce(list(w))

def feats(st):
    r0, r1 = st
    tot = len(r0) + len(r1)
    c0, c1 = cyc(r0), cyc(r1)
    cancel = (len(r0) - len(c0)) + (len(r1) - len(c1))
    ex = sum(1 if c == 0 else -1 if c == 1 else 0 for c in r0 + r1)
    ey = sum(1 if c == 2 else -1 if c == 3 else 0 for c in r0 + r1)
    best = tot
    for m in range(14):
        a, b = R.apply_move(list(r0), list(r1), m)
        if a and b:
            best = min(best, len(a) + len(b))
    return {"len_r1": len(r1), "floor": best, "tot": tot,
            "cyc_x_balance": abs(ex) + abs(ey), "cancel_trap": -cancel}

def cost(st):
    f = feats(st)
    return sum(W[k] * f[k] for k in W)

def build_ball(depth, cap):
    seen = {TRIVIAL: 0}
    fr = [TRIVIAL]
    for d in range(1, depth + 1):
        nxt = []
        for st in fr:
            for m in range(14):
                a, b = R.apply_move(list(st[0]), list(st[1]), m)
                if not a or not b or len(a) > cap or len(b) > cap:
                    continue
                k = (tuple(a), tuple(b))
                if k not in seen:
                    seen[k] = d
                    nxt.append(k)
        fr = nxt
    return seen

def tail(ball, st):
    out = []
    cur, d = st, ball[st]
    while d > 0:
        for m in range(14):
            a, b = R.apply_move(list(cur[0]), list(cur[1]), m)
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

def run(start, ball, width, steps, ceiling, rng):
    cur = [(start, [])]
    seen = {start}
    for _ in range(steps):
        cand = []
        for st, path in cur:
            for m in range(14):
                a, b = R.apply_move(list(st[0]), list(st[1]), m)
                if not a or not b or len(a) + len(b) > ceiling:
                    continue
                k = (tuple(a), tuple(b))
                if k in seen:
                    continue
                if k in ball:
                    t = tail(ball, k)
                    if t is not None:
                        return path + [m] + t
                cand.append((cost(k) + rng.random() * 2, k, path + [m]))
        if not cand:
            return None
        cand.sort(key=lambda z: z[0])
        keep = cand[:width // 2]
        rest = cand[width // 2:width * 6]
        if rest:
            keep += rng.sample(rest, min(len(rest), width - len(keep)))
        cur = [(k, p) for _s, k, p in keep]
        seen.update(k for k, _p in cur)
        if len(seen) > 1_200_000:
            return None
    return None

def load(cid):
    for line in open("research/acc/sac/stable_ac.jsonl", errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d["challenge_id"] == cid:
            w = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
            return tuple(tuple(LET[t] for t in q.replace("= 1", "").strip().split())
                         for q in w.split(";"))
    raise SystemExit("no such row")

def main():
    cid, seed, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    pres = load(cid)
    start = (tuple(R.free_reduce(list(pres[0]))), tuple(R.free_reduce(list(pres[1]))))
    base = len(start[0]) + len(start[1])
    ball = build_ball(6, 12)
    print(f"{cid} base {base} ball {len(ball):,} start cost {cost(start):.2f}", flush=True)
    rng = random.Random(seed)
    t0 = time.time()
    n = 0
    while True:
        for ceiling in (base + 10, base + 16, base + 22, base + 30):
            for width in (400, 2000, 8000):
                n += 1
                p = run(start, ball, width, 130, ceiling, rng)
                if p is None:
                    continue
                _a, _b, ok = R.replay(pres[0], pres[1], p)
                if ok:
                    print(f"  +++ {cid} SOLVED {len(p)+2} moves", flush=True)
                    with open(outp, "w") as f:
                        f.write(json.dumps({"id": cid, "len": len(p) + 2,
                                            "moves": p + [16, 15]}) + "\n")
                    return
            print(f"  .. {n} runs ceiling {ceiling} {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
