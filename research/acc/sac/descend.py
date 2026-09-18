"""Beam descent for rows that have a length gradient.

The census found 1,052 rows with at least one length-reducing move, and every
one of them is solved by somebody. For those a plain beam on total relator
length reaches the trivial presentation far more cheaply than a ball search.
"""
import json, re, sys, time, random
sys.path.insert(0, "tools/acc/eyes")
import replay as R

LET = {"x": 0, "x^-1": 1, "y": 2, "y^-1": 3}
TRIVIAL = ((0,), (2,))

def load_board():
    out = {}
    for line in open("research/acc/sac/stable_ac.jsonl", errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        b = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        out[d["challenge_id"]] = tuple(
            tuple(LET[t] for t in q.replace("= 1", "").strip().split())
            for q in b.split(";"))
    return out

def beam(start, width, steps, rng):
    cur = [(start, [])]
    seen = {start}
    for _ in range(steps):
        cand = []
        for st, path in cur:
            for m in range(14):
                a, b = R.apply_move(list(st[0]), list(st[1]), m)
                if not a or not b or len(a) > 60 or len(b) > 60:
                    continue
                k = (tuple(a), tuple(b))
                if k == TRIVIAL:
                    return path + [m]
                if k in seen:
                    continue
                cand.append((len(a) + len(b) + rng.random(), k, path + [m]))
        if not cand:
            return None
        cand.sort(key=lambda z: z[0])
        cur = [(k, p) for _s, k, p in cand[:width]]
        seen.update(k for k, _p in cur)
    return None

def main():
    board = load_board()
    ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    si, sn = (int(v) for v in sys.argv[2].split("/"))
    ids = [c for n, c in enumerate(ids) if n % sn == si]
    out = open(sys.argv[3], "w")
    rng = random.Random(1234 + si)
    t0 = time.time()
    solved = 0
    for n, cid in enumerate(ids, 1):
        st = (tuple(R.free_reduce(list(board[cid][0]))),
              tuple(R.free_reduce(list(board[cid][1]))))
        best = None
        for width in (24, 120, 600):
            p = beam(st, width, 90, rng)
            if p is not None and (best is None or len(p) < len(best)):
                best = p
                break
        if best is None:
            if n % 50 == 0:
                print(f"  .. {n}/{len(ids)} {solved} solved ({time.time()-t0:.0f}s)", flush=True)
            continue
        _a, _b, ok = R.replay(board[cid][0], board[cid][1], best)
        if not ok:
            continue
        solved += 1
        out.write(json.dumps({"id": cid, "len": len(best) + 2,
                              "moves": best + [16, 15]}) + "\n")
        out.flush()
        print(f"  +++ {cid} {len(best)+2} moves", flush=True)
    print(f"DONE {len(ids)} scanned, {solved} solved, {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
