"""Stabilised search: leave rank 2, work in rank 3, come back.

Every search in this repo so far has been rank-2 only, but Stable AC allows
stabilisation up to rank 8 and the move spec defines 257 moves. Adding a
generator is the one representation change the rules hand us for free, and the
external closures of the ac-02555 interior are all rank-2 or rank-3 capped
graphs over a restricted move set.

The move table is built from the published spec file rather than hand-written.
"""
import json, re, sys, time, random
sys.path.insert(0, "tools/acc/eyes")
import replay_sac as S

SPEC = json.load(open("research/acc/sac/stable_move_spec.json"))
TABLE = {r["id"]: r for r in SPEC["moves"]}
MAX_RANK = SPEC["max_rank"]
LET = {"x": 1, "x^-1": -1, "y": 2, "y^-1": -2}

def apply_move(state, m):
    row = TABLE.get(m)
    if row is None:
        return None, "bad id"
    cat = row["category"]
    k = len(state)
    if cat == "stabilize":
        if k >= MAX_RANK:
            return None, "max_rank"
        return state + ((k + 1,),), None
    i = row["relator"]
    if i >= k:
        return None, "rank"
    if cat == "destabilize":
        w = state[i]
        if len(w) != 1 or w[0] <= 0:
            return None, "precondition"
        g = w[0]
        for j, o in enumerate(state):
            if j != i and any(a == g or a == -g for a in o):
                return None, "precondition"
        rest = state[:i] + state[i + 1:]
        return tuple(S._relabel_after(w2, g) for w2 in rest), None
    if cat == "inversion":
        return state[:i] + (S.invert(state[i]),) + state[i + 1:], None
    if cat == "multiplication":
        j = row["other"]
        if j >= k:
            return None, "rank"
        o = state[j]
        if row["invert_other"]:
            o = S.invert(o)
        return state[:i] + (S.free_reduce(state[i] + o),) + state[i + 1:], None
    c = row["conjugator"]
    if abs(c) > k:
        return None, "gen"
    return state[:i] + (S.free_reduce((c,) + state[i] + (-c,)),) + state[i + 1:], None

def legal_moves(k):
    """Move ids that can apply at rank k."""
    out = []
    for m, row in TABLE.items():
        cat = row["category"]
        if cat == "stabilize":
            if k < MAX_RANK:
                out.append(m)
            continue
        if row.get("relator", 0) >= k:
            continue
        if cat == "multiplication" and row["other"] >= k:
            continue
        if cat == "conjugation" and abs(row["conjugator"]) > k:
            continue
        out.append(m)
    return out

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

def cost(state):
    return sum(len(w) for w in state) + 4 * len(state)

def search(start, width, steps, ceiling, rng):
    """Beam over the full move set, so stabilisation is available."""
    cur = [(start, [])]
    seen = {start}
    for _ in range(steps):
        cand = []
        for st, path in cur:
            for m in legal_moves(len(st)):
                ns, why = apply_move(st, m)
                if ns is None or any(len(w) == 0 for w in ns):
                    continue
                if sum(len(w) for w in ns) > ceiling:
                    continue
                if ns == ():
                    return path + [m]
                if ns in seen:
                    continue
                cand.append((cost(ns) + rng.random() * 3, ns, path + [m]))
        if not cand:
            return None
        cand.sort(key=lambda z: z[0])
        keep = cand[:width // 2]
        rest = cand[width // 2:width * 6]
        if rest:
            keep += rng.sample(rest, min(len(rest), width - len(keep)))
        cur = [(s, p) for _c, s, p in keep]
        seen.update(s for s, _p in cur)
        if len(seen) > 1_500_000:
            return None
    return None

def main():
    cid, seed, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    pres = load(cid)
    start = tuple(S.free_reduce(tuple(w)) for w in pres)
    base = sum(len(w) for w in start)
    print(f"{cid} base {base}, moves at rank 2 {len(legal_moves(2))}, "
          f"rank 3 {len(legal_moves(3))}", flush=True)
    rng = random.Random(seed)
    t0 = time.time()
    n = 0
    while True:
        for ceiling in (base + 8, base + 12, base + 16, base + 22):
            for width in (200, 800, 3000):
                n += 1
                p = search(start, width, 100, ceiling, rng)
                if p is None:
                    continue
                ok, why = S.verify(pres, p)
                if not ok:
                    print(f"  reject: {why}", flush=True)
                    continue
                print(f"  +++ {cid} SOLVED {len(p)} moves, rank-3 route", flush=True)
                with open(outp, "w") as f:
                    f.write(json.dumps({"id": cid, "len": len(p), "moves": p}) + "\n")
                return
            print(f"  .. {n} runs, ceiling {ceiling}, {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
