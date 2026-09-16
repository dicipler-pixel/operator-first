#!/usr/bin/env python3
"""
ACC WIDE NET — cap-K component fingerprint for all 10,115 problems.

WHY THIS AND NOT A DEEPER SEARCH
--------------------------------
Deep search on one row answers one row. This answers the board. Two problems whose
cap-K components are the same component are the SAME problem: one solve pays for
both. ac-02842 and ac-06556 were found to share a cap-19 component of 23,609,984
states. Nobody has swept the whole pool for that, and the class-size histogram tells
you where the multiplier is before you spend an hour climbing anything.

THE TRICK THAT MAKES IT CHEAP
-----------------------------
You cannot enumerate every problem's cap-16 component: the trivial component T_16 has
129,247,304 states and most easy rows live in it. So enumerate with a NODE BUDGET.

    closes under the budget  -> a small, isolated component. Record its exact size.
                                These are the hard rows, and the size is a fingerprint.
    blows past the budget    -> it is the giant class. Record GIANT and move on.

Work per problem is therefore bounded by the budget, the sweep is embarrassingly
parallel, and the interesting rows are exactly the cheap ones.

EXACT SIZE = SAME CLASS?  NO.
-----------------------------
Equal size is necessary, not sufficient. Two components can be isomorphic and
disjoint — measured, on ac-00945 vs ac-05233: identical size 386,320, identical
length profile, identical degree sequence, and set intersection ZERO. So this script
emits CANDIDATE classes. Confirm a candidate by intersecting the actual state sets
(--verify), which it will do for you on any size bucket small enough to hold.

USAGE
-----
    python acc_fingerprint.py --pool ac.jsonl --cap 16 --budget 2000000 --out fp.jsonl
    python acc_fingerprint.py --pool ac.jsonl --report fp.jsonl          # histogram
    python acc_fingerprint.py --pool ac.jsonl --verify fp.jsonl --size 26664

Pure standard library. Resumable: re-running skips rows already in --out.
"""
import argparse, json, os, re, sys
from collections import deque, defaultdict
from multiprocessing import Pool, cpu_count

# ---------------------------------------------------------------- move semantics
# Letters 0=x 1=x^-1 2=y 3=y^-1; inverse is XOR 1. Identical ordering to the official
# verifier's apply_move (core.py, ac-r2-v1): 0/1 invert, 2-5 multiply, 6-13 conjugate.
def free_reduce(w):
    o = []
    for c in w:
        if o and o[-1] == (c ^ 1): o.pop()
        else: o.append(c)
    return tuple(o)

def invert(w):
    return tuple(c ^ 1 for c in reversed(w))

def apply_move(st, m):
    r0, r1 = st
    if m == 0:  return (invert(r0), r1)
    if m == 1:  return (r0, invert(r1))
    if m == 2:  return (free_reduce(r0 + r1), r1)
    if m == 3:  return (free_reduce(r0 + invert(r1)), r1)
    if m == 4:  return (r0, free_reduce(r1 + r0))
    if m == 5:  return (r0, free_reduce(r1 + invert(r0)))
    if 6 <= m <= 9:
        g = m - 6;  return (free_reduce((g,) + r0 + (g ^ 1,)), r1)
    if 10 <= m <= 13:
        g = m - 10; return (r0, free_reduce((g,) + r1 + (g ^ 1,)))
    raise ValueError(m)

TARGET = ((0,), (2,))

# ---------------------------------------------------------------- pool parsing
_TOK = re.compile(r'([xy])(\^-1)?')
def parse_word(s):
    out = []
    for g, inv in _TOK.findall(s):
        c = 0 if g == 'x' else 2
        out.append(c + 1 if inv else c)
    return tuple(out)

def parse_pool(path):
    rows = []
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line: continue
        d = json.loads(line)
        body = d['description'].split('|', 1)[1].rsplit('>', 1)[0]
        parts = [p.replace('= 1', '').strip() for p in body.split(';')]
        if len(parts) != 2: continue
        rows.append((d['challenge_id'], (parse_word(parts[0]), parse_word(parts[1]))))
    return rows

# ---------------------------------------------------------------- the sweep
def component(start, cap, budget):
    """Enumerate the cap-bounded component. Returns (size, closed, hit_target)."""
    seen = {start}; q = deque([start]); hit = (start == TARGET)
    while q:
        s = q.popleft()
        for m in range(14):
            t = apply_move(s, m)
            if len(t[0]) + len(t[1]) > cap: continue
            if t in seen: continue
            seen.add(t)
            if t == TARGET: hit = True
            if len(seen) > budget: return len(seen), False, hit
            q.append(t)
    return len(seen), True, hit

def _job(a):
    cid, st, cap, budget, delta = a
    n = len(st[0]) + len(st[1])
    # A global cap excludes most of the pool: starting lengths run 13..40, so cap 16
    # would reject everything above 16 before doing any work. The cap is therefore
    # RELATIVE to each row's own starting length. Sizes are comparable within an |r|
    # band, which is where classes live anyway (family members share |r|).
    if delta is not None: cap = n + delta
    if n > cap:
        return {"challenge_id": cid, "ini": n, "status": "start_above_cap"}
    size, closed, hit = component(st, cap, budget)
    return {"challenge_id": cid, "ini": n, "cap": cap,
            "size": size, "closed": closed, "reaches_target": hit,
            "status": "closed" if closed else "giant"}

def sweep(rows, cap, budget, out, workers, delta):
    done = set()
    if os.path.exists(out):
        for l in open(out):
            try: done.add(json.loads(l)["challenge_id"])
            except Exception: pass
        print(f"resuming: {len(done)} already done", flush=True)
    todo = [(c, s, cap, budget, delta) for c, s in rows if c not in done]
    print(f"{len(todo)} rows to do on {workers} workers", flush=True)
    with open(out, "a") as f, Pool(workers) as p:
        for i, r in enumerate(p.imap_unordered(_job, todo, chunksize=4), 1):
            f.write(json.dumps(r) + "\n")
            if i % 200 == 0: f.flush(); print(f"  {i}/{len(todo)}", flush=True)

# ---------------------------------------------------------------- reporting
def report(path):
    recs = [json.loads(l) for l in open(path)]
    closed = [r for r in recs if r.get("status") == "closed"]
    giant  = [r for r in recs if r.get("status") == "giant"]
    print(f"rows fingerprinted : {len(recs)}")
    print(f"  giant class      : {len(giant)}")
    print(f"  closed (small)   : {len(closed)}")
    print(f"  reach target     : {sum(1 for r in recs if r.get('reaches_target'))}")
    # bucket on (initial length, component size): a size collision across different
    # |r| is meaningless, since the cap differs.
    by = defaultdict(list)
    for r in closed: by[(r["ini"], r["size"])].append(r["challenge_id"])
    multi = {k: v for k, v in by.items() if len(v) > 1}
    print(f"\ndistinct component sizes among closed rows: {len(by)}")
    print(f"sizes shared by >1 row (CANDIDATE classes) : {len(multi)}")
    print(f"\n{'|r|':>5}{'class size':>12}{'rows':>6}  members (candidates — verify before trusting)")
    for (ini, size), ids in sorted(multi.items(), key=lambda kv: -len(kv[1]))[:40]:
        print(f"{ini:>5}{size:>12}{len(ids):>6}  {', '.join(sorted(ids)[:8])}"
              + (" …" if len(ids) > 8 else ""))
    if multi:
        big = max(multi.values(), key=len)
        print(f"\nlargest candidate class: {len(big)} rows -> one solve would pay {len(big)}x"
              f"  (IF the sets really coincide; run --verify)")

def verify(rows, path, size, cap, budget):
    """Intersect the ACTUAL state sets for every row in one size bucket."""
    recs = [json.loads(l) for l in open(path)]
    ids = [r["challenge_id"] for r in recs if r.get("size") == size and r.get("closed")]
    caps = {r["challenge_id"]: r["cap"] for r in recs if r.get("challenge_id") in set(ids)}
    st = dict(rows)
    print(f"size {size}: {len(ids)} rows -> {', '.join(ids)}")
    comps = {}
    for cid in ids:
        c = caps.get(cid, cap)
        seen = {st[cid]}; q = deque([st[cid]])
        while q:
            s = q.popleft()
            for m in range(14):
                t = apply_move(s, m)
                if len(t[0]) + len(t[1]) > c or t in seen: continue
                seen.add(t); q.append(t)
        comps[cid] = seen
        print(f"  {cid}: {len(seen)} states")
    base = ids[0]
    for cid in ids[1:]:
        inter = len(comps[base] & comps[cid])
        same = comps[base] == comps[cid]
        print(f"  {base} vs {cid}: intersection={inter}  IDENTICAL={same}"
              + ("  -> SAME component, one solve pays both" if same
                 else "  -> isomorphic but DISJOINT, no transfer without an explicit map"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", required=True)
    ap.add_argument("--cap", type=int, default=16)
    ap.add_argument("--delta", type=int, default=4,
                    help="cap = each row's own |r| + delta (default). Use --delta -1 for a global --cap.")
    ap.add_argument("--budget", type=int, default=2_000_000)
    ap.add_argument("--out")
    ap.add_argument("--report")
    ap.add_argument("--verify")
    ap.add_argument("--size", type=int)
    ap.add_argument("--workers", type=int, default=max(1, cpu_count() - 1))
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    rows = parse_pool(a.pool)
    if a.limit: rows = rows[:a.limit]
    print(f"pool: {len(rows)} problems")
    if a.report:  return report(a.report)
    if a.verify:  return verify(rows, a.verify, a.size, a.cap, a.budget)
    if not a.out: sys.exit("need --out, --report or --verify")
    sweep(rows, a.cap, a.budget, a.out, a.workers, None if a.delta < 0 else a.delta)
    report(a.out)

if __name__ == "__main__":
    main()
