"""Randomised wide-beam attack on one presentation.

The interior of ac-02555 is closed through total length 23, so any finishing
path has to leave that band. A frontier search has to remember every state it
passes; a beam does not, so it can travel much further from the start for the
same memory. The ceiling ratchets upward across restarts and ties are broken
randomly, so repeated restarts explore different excursions.

Meets a fixed ball around the trivial presentation, so it only has to get
close rather than land exactly.
"""
import json, re, sys, time, random
sys.path.insert(0, "tools/acc/eyes")
import replay as R

LET = {"x": 0, "x^-1": 1, "y": 2, "y^-1": 3}
TRIVIAL = ((0,), (2,))

def load(cid):
    for line in open("research/acc/sac/stable_ac.jsonl", errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d["challenge_id"] != cid:
            continue
        w = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        return tuple(tuple(LET[t] for t in q.replace("= 1", "").strip().split())
                     for q in w.split(";"))
    raise SystemExit("no such row")

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
                if k in seen:
                    continue
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
                cand.append((len(a) + len(b) + rng.random() * 3, k, path + [m]))
        if not cand:
            return None
        cand.sort(key=lambda z: z[0])
        cur = [(k, p) for _s, k, p in cand[:width]]
        seen.update(k for k, _p in cur)
        if len(seen) > 3_000_000:
            return None
    return None

def main():
    cid = sys.argv[1]
    seed = int(sys.argv[2])
    out_path = sys.argv[3]
    pres = load(cid)
    start = (tuple(R.free_reduce(list(pres[0]))), tuple(R.free_reduce(list(pres[1]))))
    base = len(start[0]) + len(start[1])
    ball = build_ball(6, 12)
    print(f"{cid} base length {base}, ball {len(ball):,}", flush=True)
    rng = random.Random(seed)
    t0 = time.time()
    tries = 0
    while True:
        for ceiling in (base + 10, base + 14, base + 18, base + 24, base + 30):
            for width in (300, 1500, 6000):
                tries += 1
                p = run(start, ball, width, 120, ceiling, rng)
                if p is None:
                    continue
                _a, _b, ok = R.replay(pres[0], pres[1], p)
                if not ok:
                    continue
                print(f"  +++ {cid} SOLVED {len(p)+2} moves "
                      f"(ceiling {ceiling}, width {width})", flush=True)
                with open(out_path, "w") as f:
                    f.write(json.dumps({"id": cid, "len": len(p) + 2,
                                        "moves": p + [16, 15]}) + "\n")
                return
            print(f"  .. {tries} runs, ceiling {ceiling}, "
                  f"{time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
