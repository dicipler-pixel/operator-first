"""Depth-bounded beam search on the official kernel, meeting a reverse target basin.

Unlike solve_batch.py (best-first on relator length, which finds *a* path by
wandering), beam search advances one move per layer and keeps only the W
states with the smallest total relator length, so any path it finds has length
<= layer + basin radius. That is the right shape for beating short records.

    PYTHONPATH=<sair>/competition/tools python3 beam_batch.py --manifest ... \
        --ids ids.txt --out results.jsonl [--width 4000] [--depth 40] [--radius 7]
"""

import argparse
import json
import sys
import time

from verifier import core
from solve_batch import key, length, build_basin, finish_from_basin


def beam(initial, basin, width, max_depth, cap):
    start = (tuple(initial[0]), tuple(initial[1]))
    if key(start) in basin:
        return finish_from_basin(start, basin), 0
    seen = {key(start)}
    layer = [(start, [])]
    expanded = 0
    for _ in range(max_depth):
        cand = []
        for s, path in layer:
            expanded += 1
            for m in range(core.NUM_MOVES):
                t = core.apply_move(s, m)
                lt = length(t)
                if lt > cap:
                    continue
                k = key(t)
                if k in seen:
                    continue
                seen.add(k)
                p = path + [m]
                if k in basin:
                    return p + finish_from_basin(t, basin), expanded
                cand.append((lt, len(p), t, p))
        if not cand:
            break
        cand.sort(key=lambda x: (x[0], x[1]))
        layer = [(t, p) for _, _, t, p in cand[:width]]
    return None, expanded


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=4000)
    ap.add_argument("--depth", type=int, default=40)
    ap.add_argument("--cap", type=int, default=60)
    ap.add_argument("--radius", type=int, default=7)
    a = ap.parse_args()

    man = json.load(open(a.manifest))
    limits = man["limits"]
    ch = {c["challenge_id"]: c for c in man["challenges"]}
    ids = [l.strip() for l in open(a.ids) if l.strip() and not l.startswith("#")]
    t0 = time.time()
    basin = build_basin(a.radius)
    print(f"basin radius {a.radius}: {len(basin)} states in {time.time()-t0:.1f}s", file=sys.stderr, flush=True)
    solved = 0
    with open(a.out, "a", encoding="utf-8") as out:
        for cid in ids:
            c = ch[cid]
            t1 = time.time()
            moves, expanded = beam(c["initial_relators"], basin, a.width, a.depth, a.cap)
            rec = {"challenge_id": cid, "method": f"beam w={a.width} d={a.depth} r={a.radius}",
                   "expanded": expanded, "seconds": round(time.time() - t1, 2), "ok": False}
            if moves is not None:
                v = core.verify(c, moves, c["move_spec_version"], limits)
                rec["ok"] = bool(v.get("ok"))
                if v.get("ok"):
                    rec.update(length=v["length"], work=v["work"], certificate_hash=v["certificate_hash"], moves=moves)
                    solved += 1
            out.write(json.dumps(rec) + "\n"); out.flush()
            print(f"{cid} {'OK len=%d' % rec['length'] if rec['ok'] else 'unsolved'} expanded={expanded} {rec['seconds']}s",
                  file=sys.stderr, flush=True)
    print(f"solved {solved}/{len(ids)} in {time.time()-t0:.0f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
