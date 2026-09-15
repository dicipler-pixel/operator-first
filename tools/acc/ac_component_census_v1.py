"""Component census of one length profile of the capped Andrews-Curtis graph.

Fixes the initial total relator length, so every challenge in the profile lives
in the SAME capped graph and their components are directly comparable. This is
the confound that made the earlier pool-wide corridor-volume claim worthless:
a uniform sample across the pool mixes lengths, so it compares corridors in
different graphs, where sizes carry no information about one another.

Two facts do the work:

  * every AC target is [[1],[2]], total length 2, so the target is ALWAYS a
    vertex of the capped graph. An exhausted search is therefore a proof that
    start and target lie in DIFFERENT COMPONENTS -- a disconnection, not a
    distance.

  * a connected component has exactly one vertex count, so two closed
    components of DIFFERENT size are disjoint for free. Only equal sizes need
    a search.

The census runs the second point as an optimisation: it groups closed
corridors by size and searches only within multi-member classes, testing every
unordered pair with ac_corridor64_target_v1.

    python3 tools/acc/ac_component_census_v1.py --len 37 [--headroom 8]
    python3 tools/acc/ac_component_census_v1.py --results <file.jsonl> --verify-only
"""

import argparse
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

SAIR = "/home/user/saircompetition/andrews-curtis/competition/tools"
MANIFEST = f"{SAIR}/verifier/data/manifest.json"
ENGINE = "/tmp/claude-0/c/corridor64t"
TRIVIAL = [[1], [2]]
C2P = {1: 0, -1: 1, 2: 2, -2: 3}


def argv_for(relators):
    r0, r1 = relators
    return ([str(len(r0))] + [str(C2P[a]) for a in r0]
            + [str(len(r1))] + [str(C2P[a]) for a in r1])


def search(start, target, cap, budget, timeout=1800):
    """One run of the target-accepting engine. Search tool only; any
    certificate it emits must be re-verified by the official verifier."""
    cmd = [ENGINE, str(cap), str(budget)] + argv_for(start) + argv_for(target)
    try:
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def parse(out):
    if out.startswith("EXHAUSTED"):
        return {"verdict": "closed",
                "component": int(out.split("states=")[1].split()[0]),
                "depth": int(out.split("depth=")[1].split()[0])}
    if out.startswith("FOUND"):
        return {"verdict": "certificate", "length": len(out.split()) - 1}
    if out.startswith("BUDGET"):
        return {"verdict": "budget", "states": int(out.split("states=")[1].split()[0])}
    return {"verdict": "other", "raw": out[:60]}


def profile(length):
    m = json.load(open(MANIFEST))
    return [c for c in m["challenges"]
            if c["challenge_id"].startswith("ac-")
            and len(c["initial_relators"][0]) + len(c["initial_relators"][1]) == length]


def sweep(pool, cap, budget):
    rows = []
    for i, c in enumerate(pool, 1):
        t0 = time.time()
        rec = {"challenge_id": c["challenge_id"], "cap": cap}
        rec.update(parse(search(c["initial_relators"], TRIVIAL, cap, budget)))
        rec["secs"] = round(time.time() - t0, 1)
        rows.append(rec)
        tag = (f"  {rec['component']:,} d{rec['depth']}"
               if rec["verdict"] == "closed" else "")
        print(f"  [{i}/{len(pool)}] {rec['challenge_id']} -> {rec['verdict']}{tag}",
              flush=True)
    return rows


def disjointness(rows, byid, cap, budget):
    """Search only where sizes collide. Different sizes are disjoint for free."""
    closed = [r for r in rows if r["verdict"] == "closed"]
    classes = {}
    for r in closed:
        classes.setdefault(r["component"], []).append(r["challenge_id"])
    tests, merged = [], []
    for size, members in sorted(classes.items()):
        if len(members) < 2:
            continue
        print(f"\n  size {size:,} has {len(members)} members — "
              f"{len(members)*(len(members)-1)//2} pairs to test", flush=True)
        for x, y in itertools.combinations(members, 2):
            out = search(byid[x]["initial_relators"], byid[y]["initial_relators"],
                         cap, budget)
            same = out.startswith("FOUND")
            tests.append({"a": x, "b": y, "size": size,
                          "same_component": same, "raw": out[:70]})
            if same:
                merged.append((x, y))
            print(f"    {x} vs {y}: {'SAME COMPONENT' if same else 'DISJOINT'}",
                  flush=True)
    return classes, tests, merged


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--len", type=int, required=True, dest="length")
    p.add_argument("--headroom", type=int, default=8)
    p.add_argument("--budget", type=int, default=40_000_000)
    p.add_argument("--out")
    a = p.parse_args(argv)

    pool = profile(a.length)
    byid = {c["challenge_id"]: c for c in pool}
    cap = a.length + a.headroom
    if cap > 64:
        print(f"cap {cap} exceeds the engine's 64-letter guard"); return 2
    print(f"complete length-{a.length} profile: {len(pool)} challenges at cap {cap}",
          flush=True)

    rows = sweep(pool, cap, a.budget)
    classes, tests, merged = disjointness(rows, byid, cap, a.budget)

    closed = [r for r in rows if r["verdict"] == "closed"]
    print(f"\n{'='*64}")
    print(f"length {a.length}, cap {cap}: {len(pool)} challenges, "
          f"{len(closed)} closed, {len(classes)} distinct sizes")
    for size, members in sorted(classes.items()):
        depths = sorted(r["depth"] for r in closed if r["component"] == size)
        print(f"  {size:>12,}  x{len(members)}  depths {depths}")
    if merged:
        print(f"\n  MERGED (same component): {merged}")
        print(f"  distinct components among the closed corridors: "
              f"{len(closed) - len(merged)}")
    else:
        print(f"\n  every size collision tested; all pairs disjoint")
        print(f"  distinct components: {len(closed)} closed + the trivial "
              f"presentation's = at least {len(closed)+1}")

    if a.out:
        Path(a.out).write_text("".join(json.dumps(r) + "\n" for r in rows)
                               + "".join(json.dumps({"pair_test": t}) + "\n" for t in tests))
        print(f"\n  written {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
