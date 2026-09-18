"""Theorem census: run every eye on every target, record HIT or not, then sort.

One eye = one theorem/test with a stated hypothesis. Each eye returns a status
per target and never influences another eye. Statuses: HIT, SIGNAL, NO_SIGNAL,
INAPPLICABLE, BLOCKED, ERROR. The census is written before anything is mixed.
"""
import json, re, sys, collections
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
        ws = [tuple(LET[t] for t in q.replace("= 1", "").strip().split())
              for q in b.split(";")]
        out[d["challenge_id"]] = (ws[0], ws[1])
    return out

def expsum(w):
    return (sum(1 if c == 0 else -1 if c == 1 else 0 for c in w),
            sum(1 if c == 2 else -1 if c == 3 else 0 for c in w))

def dM(st):
    (a, b), (c, d) = expsum(st[0]), expsum(st[1])
    n = 0
    while n < 12:
        if (a, b, c, d) == (1, 0, 0, 1):
            return n
        if abs(c) > abs(a) and a:
            q = round(c / a); c, d = c - q * a, d - q * b
        elif abs(a) > abs(c) and c:
            q = round(a / c); a, b = a - q * c, b - q * d
        elif abs(b) > abs(d) and d:
            q = round(b / d); a, b = a - q * c, b - q * d
        elif abs(d) > abs(b) and b:
            q = round(d / b); c, d = c - q * a, d - q * b
        else:
            break
        n += 1
    return 12

def children(st):
    out = []
    r0, r1 = list(st[0]), list(st[1])
    for m in range(14):
        a, b = R.apply_move(r0, r1, m)
        if a and b:
            out.append((m, (tuple(a), tuple(b))))
    return out

def canon(st):
    """Canonical form modulo relator order, inversion and cyclic rotation."""
    def cyc(w):
        w = R.cyclic_reduce(list(w))
        if not w:
            return ()
        rots = [tuple(w[i:] + w[:i]) for i in range(len(w))]
        rots += [tuple(R.invert(list(r))) for r in rots]
        return min(rots)
    a, b = cyc(st[0]), cyc(st[1])
    return tuple(sorted((a, b)))

# ---- eyes -------------------------------------------------------------
def eye_det(st, ctx):
    (a, b), (c, d) = expsum(st[0]), expsum(st[1])
    det = a * d - b * c
    return ("HIT", det) if abs(det) == 1 else ("NO_SIGNAL", det)

def eye_dM1(st, ctx):
    n = dM(st)
    return ("HIT" if n <= 1 else "SIGNAL" if n <= 2 else "NO_SIGNAL", n)

def eye_downhill(st, ctx):
    tot = len(st[0]) + len(st[1])
    best = min((len(a) + len(b) for _m, (a, b) in children(st)), default=tot)
    return ("HIT" if best < tot else "NO_SIGNAL", best - tot)

def eye_plateau(st, ctx):
    tot = len(st[0]) + len(st[1])
    ups = sum(1 for _m, (a, b) in children(st) if len(a) + len(b) > tot)
    return ("HIT" if ups == len(children(st)) else "NO_SIGNAL", ups)

def eye_ball(st, ctx):
    d = ctx["ball"].get(st)
    return ("HIT", d) if d is not None else ("NO_SIGNAL", None)

def eye_child_in_ball(st, ctx):
    hits = [m for m, k in children(st) if k in ctx["ball"]]
    return ("HIT" if hits else "NO_SIGNAL", hits)

def eye_bare_generator(st, ctx):
    n = sum(1 for w in st if len(w) == 1)
    return ("HIT" if n else "NO_SIGNAL", n)

def eye_collision_solved(st, ctx):
    """Canonical form shared with a DIFFERENT row someone has already solved."""
    other = ctx["canon_solved"].get(canon(st))
    if other and other != ctx["cid"]:
        return ("HIT", other)
    return ("NO_SIGNAL", None)

def eye_child_collision(st, ctx):
    """A one-move child whose canonical form matches a solved row."""
    for m, k in children(st):
        o = ctx["canon_solved"].get(canon(k))
        if o and o != ctx["cid"]:
            return ("HIT", (m, o))
    return ("NO_SIGNAL", None)

def eye_cyclic_cancel(st, ctx):
    n = sum(len(w) - len(R.cyclic_reduce(list(w))) for w in st)
    return ("HIT" if n else "NO_SIGNAL", n)

def eye_balanced_len(st, ctx):
    return ("HIT" if len(st[0]) == len(st[1]) else "NO_SIGNAL",
            abs(len(st[0]) - len(st[1])))

def eye_short(st, ctx):
    tot = len(st[0]) + len(st[1])
    return ("HIT" if tot <= 16 else "SIGNAL" if tot <= 20 else "NO_SIGNAL", tot)

EYES = [("DET-UNIMOD", eye_det), ("ABEL-DM1", eye_dM1),
        ("DOWNHILL", eye_downhill), ("PLATEAU-STRICT", eye_plateau),
        ("BALL-MEMBER", eye_ball), ("CHILD-IN-BALL", eye_child_in_ball),
        ("BARE-GENERATOR", eye_bare_generator),
        ("CANON-COLLIDE-SOLVED", eye_collision_solved),
        ("CHILD-COLLIDE-SOLVED", eye_child_collision),
        ("CYCLIC-CANCEL", eye_cyclic_cancel),
        ("BALANCED-LEN", eye_balanced_len), ("SHORT-TOTAL", eye_short)]

def build_ball(depth=6, cap=12):
    seen = {TRIVIAL: 0}
    fr = [TRIVIAL]
    for d in range(1, depth + 1):
        nxt = []
        for st in fr:
            for _m, k in children(st):
                if len(k[0]) > cap or len(k[1]) > cap or k in seen:
                    continue
                seen[k] = d
                nxt.append(k)
        fr = nxt
    return seen

def main():
    board = load_board()
    status = {r["challengeId"].replace("ac-", "sac-"): r
              for r in json.load(open("tools/acc/acc_board_20260916_v1.json"))}
    ball = build_ball()
    solved_ids = [c for c in board if status.get(c, {}).get("status") == "solved"]
    canon_solved = {}
    for c in solved_ids:
        canon_solved.setdefault(canon(board[c]), c)
    ctx = {"ball": ball, "canon_solved": canon_solved}
    print(f"ball {len(ball):,}   solved canonical forms {len(canon_solved):,}", flush=True)

    out = open("research/acc/sac/EYE_CENSUS.jsonl", "w")
    tally = collections.defaultdict(collections.Counter)
    for n, (cid, pres) in enumerate(sorted(board.items()), 1):
        st = (tuple(R.free_reduce(list(pres[0]))), tuple(R.free_reduce(list(pres[1]))))
        ctx["cid"] = cid
        rec = {"id": cid, "solved": status.get(cid, {}).get("status") == "solved",
               "eyes": {}}
        for name, fn in EYES:
            try:
                s, v = fn(st, ctx)
            except Exception as e:
                s, v = "ERROR", str(e)
            rec["eyes"][name] = s
            tally[name][s] += 1
        out.write(json.dumps(rec) + "\n")
        if n % 2000 == 0:
            print(f"  {n}/{len(board)}", flush=True)
    out.close()
    print("\nEYE CENSUS — status counts over all 10,115 targets")
    for name, _ in EYES:
        c = tally[name]
        print(f"  {name:<22} HIT {c['HIT']:>6}  SIGNAL {c['SIGNAL']:>6}  "
              f"NO_SIGNAL {c['NO_SIGNAL']:>6}  ERROR {c['ERROR']}")

if __name__ == "__main__":
    main()
