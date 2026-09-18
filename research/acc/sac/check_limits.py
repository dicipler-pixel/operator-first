"""Check a SAC submission file against every published Discovery Track limit."""
import json, re, sys, os
sys.path.insert(0, "tools/acc/eyes")
import replay_sac as S

LIMITS = {"lines": 500, "moves": 100_000, "length": 10_000,
          "work": 5_000_000, "rank": 8, "bytes": 10_000_000}
LET = {"x": 1, "x^-1": -1, "y": 2, "y^-1": -2}

def load_board(p):
    out = {}
    for line in open(p, errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        b = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        out[d["challenge_id"]] = tuple(
            tuple(LET[t] for t in q.replace("= 1", "").strip().split())
            for q in b.split(";"))
    return out

def main():
    f = sys.argv[1] if len(sys.argv) > 1 else "research/acc/sac/SAC_SUBMIT_FINAL.txt"
    board = load_board("research/acc/sac/stable_ac.jsonl")
    rows = []
    for line in open(f):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        head, _, _note = line.partition("#")
        cid, rest = head.split(":", 1)
        rows.append((cid.strip(), json.loads(rest.strip())))

    worst = {"moves": 0, "length": 0, "work": 0, "rank": 0}
    fails = []
    for cid, mv in rows:
        st = tuple(S.free_reduce(tuple(w)) for w in board[cid])
        work = sum(len(w) for w in st)
        worst["moves"] = max(worst["moves"], len(mv))
        for m in mv:
            st, why = S.apply_move(st, m)
            if st is None:
                fails.append((cid, m, why))
                break
            tot = sum(len(w) for w in st)
            work += tot
            worst["length"] = max(worst["length"], tot)
            worst["rank"] = max(worst["rank"], len(st))
        else:
            if st != ():
                fails.append((cid, None, "did not reach the empty presentation"))
        worst["work"] = max(worst["work"], work)

    got = {"lines": len(rows), "bytes": os.path.getsize(f), **worst}
    bad = [k for k in LIMITS if got[k] > LIMITS[k]]
    for k in ("lines", "moves", "length", "work", "rank", "bytes"):
        print(f"  {k:<8} {got[k]:>12,}  limit {LIMITS[k]:>12,}  "
              f"{'OVER' if k in bad else 'ok'}")
    print(f"  replay failures: {len(fails)}")
    if fails:
        print("  ", fails[:5])
    return 1 if (bad or fails) else 0

if __name__ == "__main__":
    sys.exit(main())
