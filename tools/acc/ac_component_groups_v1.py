"""Find multi-member components: challenges that share a component, hence a
certificate.

A component holding n challenges is an n-for-one target. A certificate for any
member transfers to all the others along the connecting path, and that path is
bounded by the cap for free -- so the transfer needs no separate search and no
separate length budget beyond what the cap already grants.

Naive pairwise testing costs O(n^2) enumerations. This does one enumeration per
COMPONENT: take an unassigned challenge, enumerate its component with every
other unassigned challenge as a simultaneous target, assign the hits, repeat.

Two asymmetries matter and are handled differently:

  EXHAUSTED  the component closed, so hits are complete: every target not hit
             is PROVED to be in a different component at this cap.
  BUDGET     the enumeration ran out of nodes. Hits are still valid -- finding
             a target proves shared membership regardless -- but misses prove
             nothing. Those targets stay unassigned rather than being split.

So positive grouping is available even where the component is too large to
close, and only the disjointness half needs a completed enumeration.

    python3 tools/acc/ac_component_groups_v1.py --len 14 [--headroom 8]
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

SAIR = "/home/user/saircompetition/andrews-curtis/competition/tools"
MANIFEST = f"{SAIR}/verifier/data/manifest.json"
ENGINE = "/tmp/claude-0/c/corridor64m"
C2P = {1: 0, -1: 1, 2: 2, -2: 3}


def av(relators):
    r0, r1 = relators
    return ([str(len(r0))] + [str(C2P[a]) for a in r0]
            + [str(len(r1))] + [str(C2P[a]) for a in r1])


def enumerate_component(start, targets, cap, budget, timeout=3600):
    """One pass: enumerate start's component, reporting which targets it holds."""
    args = [ENGINE, str(cap), str(budget)] + av(start) + [str(len(targets))]
    for t in targets:
        args += av(t)
    try:
        out = subprocess.run(args, capture_output=True, text=True,
                             timeout=timeout).stdout.strip()
    except subprocess.TimeoutExpired:
        return {"verdict": "timeout", "hits": {}}
    hits, verdict = {}, {"verdict": "other", "raw": out[:60]}
    for line in out.splitlines():
        if line.startswith("HIT"):
            _, k, d = line.split()
            hits[int(k)] = int(d)
        elif line.startswith("EXHAUSTED"):
            verdict = {"verdict": "closed",
                       "component": int(line.split("states=")[1].split()[0]),
                       "depth": int(line.split("depth=")[1].split()[0])}
        elif line.startswith("BUDGET"):
            verdict = {"verdict": "budget",
                       "states": int(line.split("states=")[1].split()[0])}
    verdict["hits"] = hits
    return verdict


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--len", type=int, required=True, dest="length")
    p.add_argument("--headroom", type=int, default=8)
    p.add_argument("--budget", type=int, default=40_000_000)
    p.add_argument("--out")
    a = p.parse_args(argv)

    man = json.load(open(MANIFEST))
    pool = [c for c in man["challenges"]
            if c["challenge_id"].startswith("ac-")
            and len(c["initial_relators"][0]) + len(c["initial_relators"][1]) == a.length]
    cap = a.length + a.headroom
    if cap > 64:
        print(f"cap {cap} exceeds the engine's 64-letter guard"); return 2
    print(f"length-{a.length} profile: {len(pool)} challenges at cap {cap}", flush=True)

    unassigned = list(range(len(pool)))
    groups, runs = [], []
    while unassigned:
        i = unassigned[0]
        rest = unassigned[1:]
        if not rest:
            groups.append({"members": [pool[i]["challenge_id"]], "verdict": "singleton"})
            break
        t0 = time.time()
        res = enumerate_component(pool[i]["initial_relators"],
                                  [pool[j]["initial_relators"] for j in rest],
                                  cap, a.budget)
        secs = round(time.time() - t0, 1)
        members = [pool[i]["challenge_id"]]
        dists = {}
        for k, d in sorted(res["hits"].items()):
            members.append(pool[rest[k]]["challenge_id"])
            dists[pool[rest[k]]["challenge_id"]] = d
        grp = {"representative": pool[i]["challenge_id"], "members": members,
               "size": len(members), "verdict": res["verdict"],
               "transfer_distances": dists, "secs": secs}
        if res["verdict"] == "closed":
            grp["component"] = res["component"]; grp["depth"] = res["depth"]
        groups.append(grp)
        runs.append(grp)
        flag = "  <-- MULTI-MEMBER" if len(members) > 1 else ""
        print(f"  {pool[i]['challenge_id']}: {res['verdict']}, "
              f"{len(members)} member(s) [{secs}s]{flag}", flush=True)
        if res["verdict"] == "closed":
            # complete enumeration: misses are proved disjoint, so drop them all
            hit_idx = {rest[k] for k in res["hits"]}
            unassigned = [j for j in unassigned if j != i and j not in hit_idx]
        else:
            # incomplete: only the hits are decided
            hit_idx = {rest[k] for k in res["hits"]}
            unassigned = [j for j in unassigned if j != i and j not in hit_idx]

    multi = [g for g in groups if g.get("size", 1) > 1]
    print(f"\n{'='*62}")
    print(f"length {a.length}, cap {cap}: {len(pool)} challenges -> {len(groups)} groups")
    print(f"multi-member components: {len(multi)}")
    for g in sorted(multi, key=lambda g: -g["size"]):
        print(f"  {g['size']}x  {g['members']}")
        print(f"       transfer distances: {g['transfer_distances']}")
    if a.out:
        Path(a.out).write_text("".join(json.dumps(g) + "\n" for g in groups))
        print(f"\n  written {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
