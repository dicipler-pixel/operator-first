"""Decide whether each submitted path is the shortest that exists.

A SAC path is (rank-2 prefix to (x,y)) + [16, 15]; two destabilizes is the
minimum possible finish from (x,y), so minimality of the whole path reduces
to minimality of the prefix. Exhaustive bidirectional BFS looks for ANY
shorter prefix. Three outcomes per row:

  MINIMAL  - the whole space below our length was searched, nothing shorter
  SHORTER  - a strictly shorter path exists (and is printed: a free upgrade)
  UNKNOWN  - the search hit its node cap before exhausting the space
"""
import json, re, sys, time
sys.path.insert(0, "tools/acc/eyes")
import replay as R

TRIVIAL = ((0,), (2,))
INV = {0:0, 1:1, 2:3, 3:2, 4:5, 5:4, 6:7, 7:6, 8:9, 9:8, 10:11, 11:10, 12:13, 13:12}
LET = {"x": 0, "x^-1": 1, "y": 2, "y^-1": 3}
CAP = 40           # max letters per relator inside the search
NODE_CAP = 900_000

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

def neighbours(st):
    r0, r1 = list(st[0]), list(st[1])
    for m in range(14):
        a, b = R.apply_move(r0, r1, m)
        if not a or not b or len(a) > CAP or len(b) > CAP:
            continue
        yield m, (tuple(a), tuple(b))

def shorter_than(start, limit):
    """Exhaustive bidirectional BFS for a path start -> TRIVIAL of length
    < limit. Returns (moves, None) if found, (None, 'exhausted'|'capped')."""
    if start == TRIVIAL:
        return [], None
    fwd, bwd = {start: []}, {TRIVIAL: []}
    ff, bf = [start], [TRIVIAL]
    df = db = 0
    nodes = 0
    while df + db < limit - 1:
        if len(ff) <= len(bf):
            nxt = []
            for st in ff:
                for m, ns in neighbours(st):
                    if ns in fwd:
                        continue
                    nodes += 1
                    fwd[ns] = fwd[st] + [m]
                    if ns in bwd:
                        return fwd[ns] + [INV[x] for x in reversed(bwd[ns])], None
                    nxt.append(ns)
            ff = nxt
            df += 1
        else:
            nxt = []
            for st in bf:
                for m, ns in neighbours(st):
                    if ns in bwd:
                        continue
                    nodes += 1
                    bwd[ns] = bwd[st] + [m]
                    if ns in fwd:
                        return fwd[ns] + [INV[x] for x in reversed(bwd[ns])], None
                    nxt.append(ns)
            bf = nxt
            db += 1
        if nodes > NODE_CAP:
            return None, "capped"
        if not ff or not bf:
            return None, "exhausted"
    return None, "exhausted"

def main():
    board = load_board("research/acc/sac/stable_ac.jsonl")
    rows = []
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        head, _, _n = line.partition("#")
        cid, rest = head.split(":", 1)
        cid = cid.strip()
        if not cid.startswith("sac-"):
            continue
        rows.append((cid, json.loads(rest.strip())))
    rows.sort(key=lambda z: len(z[1]))
    si, sn = (int(v) for v in sys.argv[2].split("/")) if len(sys.argv) > 2 else (0, 1)
    rows = [r for n, r in enumerate(rows) if n % sn == si]

    t0 = time.time()
    out = open(sys.argv[3], "w")
    tally = {"MINIMAL": 0, "SHORTER": 0, "UNKNOWN": 0}
    for n, (cid, mv) in enumerate(rows, 1):
        prefix = mv[:-2]
        start = tuple(tuple(R.free_reduce(list(w))) for w in board[cid])
        found, why = shorter_than(start, len(prefix))
        if found is not None:
            verdict = "SHORTER"
            new = found + [16, 15]
        elif why == "exhausted":
            verdict, new = "MINIMAL", None
        else:
            verdict, new = "UNKNOWN", None
        tally[verdict] += 1
        rec = {"id": cid, "len": len(mv), "verdict": verdict}
        if new:
            rec["moves"] = new
            rec["newlen"] = len(new)
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if verdict == "SHORTER":
            print(f"  !{cid} {len(mv)} -> {len(new)}", flush=True)
        if n % 20 == 0:
            print(f"  .. {n}/{len(rows)}  {tally}  ({time.time()-t0:.0f}s)", flush=True)
    print(f"DONE {tally}  {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
