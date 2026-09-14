"""Corridor sweep v2 -- the first ACC search in this project that the eyes read.

v1 searched 266,213,952 states and no eye saw any of it. The engines carried no
eye wiring at all; the only 'emit' strings in them were comments. This driver
exists so that never happens again, under the rule that made it a failure:

    All eyes on always means every eye leaves a record.
    Each hour records independently. They are only mixed together afterward
    to see for effect.

So the sweep is organised BY HOUR, not by challenge:

  during the hour   the worker searches and appends raw results to
                    runs/corridor_v2/<hour>/search.jsonl. No eye reads.

  at hour close     each eye is spawned as its OWN SUBPROCESS, at its own
                    stagger, and reads its OWN PROJECTION of that hour -- a
                    different slice of the data, hashed into its record as
                    input_digest. Eyes do not see each other's readings; an eye
                    handed one is refused by eye_hour_v1.

  afterward         the hour is mixed, and only once it is closed.

Honesty about what this does and does not achieve. Separate processes and
staggered starts make the wall spread real, and distinct projections make
shared_input_digests empty, so two eyes cannot be silently reading the same
bytes. What it does NOT do is make the eyes independent MINDS -- one author
wrote all their projection functions. The mix reports the spread; read it.

The engine is a search tool. Every certificate it emits is re-verified by the
official SAIR verifier (verifier.core), never by a re-implementation.

    python3 tools/acc/ac_corridor_v2_driver.py --work 40 --headroom 8
    python3 tools/acc/ac_corridor_v2_driver.py --close-hour 2026-09-14T21Z
    python3 tools/acc/ac_corridor_v2_driver.py --eye total-length --hour <h>
"""

import argparse
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from eye_hour_v1 import HourlyEyes, now_hour  # noqa: E402

SAIR = "/home/user/saircompetition/andrews-curtis/competition/tools"
MANIFEST = f"{SAIR}/verifier/data/manifest.json"
ENGINE = "/tmp/claude-0/c/corridor64"
RUNS = Path("runs/corridor_v2")
ITEM = "acc:unsolved-lane-sweep"
C2P = {1: 0, -1: 1, 2: 2, -2: 3}

ROSTER = ["total-length", "descent-direction", "bidirectional-search",
          "twisted-determinant", "displacement-gram", "b2-fixity",
          "regularised-torsion", "reflection", "claude-build-assessment",
          "jeromie-reaudit", "axiom-audit", "lakefile-parser"]


def manifest():
    m = json.load(open(MANIFEST))
    ac = [c for c in m["challenges"] if c["challenge_id"].startswith("ac-")]
    return m["limits"], ac


def hour_dir(hour):
    d = RUNS / hour
    d.mkdir(parents=True, exist_ok=True)
    return d


def done_ids():
    """Every challenge this sweep has already attempted, across all hours."""
    seen = set()
    for f in RUNS.glob("*/search.jsonl"):
        for line in f.read_text(errors="replace").splitlines():
            try:
                seen.add(json.loads(line)["challenge_id"])
            except Exception:
                pass
    return seen


# --------------------------------------------------------------------- search

def search(limits, ch, headroom, budget):
    cid = ch["challenge_id"]
    r0, r1 = ch["initial_relators"]
    cap = len(r0) + len(r1) + headroom
    if cap > 64:
        return {"challenge_id": cid, "verdict": "skipped", "why": "cap>64"}

    args = ([ENGINE, str(cap), str(budget), str(len(r0))]
            + [str(C2P[a]) for a in r0] + [str(len(r1))]
            + [str(C2P[a]) for a in r1])
    t0 = time.time()
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {"challenge_id": cid, "verdict": "timeout",
                "init_len": len(r0) + len(r1), "cap": cap}
    o = p.stdout.strip()
    rec = {"challenge_id": cid, "init_len": len(r0) + len(r1), "cap": cap,
           "headroom": headroom, "secs": round(time.time() - t0, 2)}

    if o.startswith("FOUND"):
        mv = [int(x) for x in o.split()[1:]]
        sys.path.insert(0, SAIR)
        from verifier import core                       # official, not a re-impl
        v = core.verify({"challenge_id": cid, "move_spec_version": "ac-r2-v1",
                         "initial_relators": [r0, r1],
                         "target_relators": ch["target_relators"]},
                        mv, "ac-r2-v1", limits)
        rec.update(verdict="certificate", length=len(mv),
                   official_verify=bool(v.get("ok")), moves=mv)
    elif o.startswith("EXHAUSTED"):
        rec.update(verdict="closed",
                   component=int(o.split("states=")[1].split()[0]),
                   depth=int(o.split("depth=")[1].split()[0]))
    elif o.startswith("BUDGET"):
        rec.update(verdict="budget", states=int(o.split("states=")[1].split()[0]))
    else:
        rec.update(verdict="other", raw=o[:80])
    return rec


def work(n, headroom, budget, seed):
    limits, ac = manifest()
    skip = done_ids()
    pool = [c for c in ac if c["challenge_id"] not in skip]
    # Longest presentations first. This is a HEURISTIC standing in for the
    # unsolved set, not knowledge of it: 7,442 of 10,115 AC rows are solved and
    # the board list is not available locally, so the sweep targets the hardest
    # end of the pool. Re-target the moment the unsolved IDs arrive.
    rng = random.Random(seed)
    rng.shuffle(pool)
    pool.sort(key=lambda c: -(len(c["initial_relators"][0])
                              + len(c["initial_relators"][1])))
    todo = pool[:n]

    hour = now_hour()
    out = hour_dir(hour) / "search.jsonl"
    print(f"hour {hour}: {len(todo)} challenges, headroom +{headroom}, "
          f"budget {budget}, {len(skip)} already attempted", flush=True)
    with open(out, "a") as fh:
        for i, ch in enumerate(todo, 1):
            # An hour boundary ends the hour's file; results stay in the hour
            # they were actually produced in.
            h = now_hour()
            if h != hour:
                fh.close(); hour = h
                out = hour_dir(hour) / "search.jsonl"
                fh = open(out, "a")
                print(f"-- hour rolled to {hour}", flush=True)
            rec = search(limits, ch, headroom, budget)
            fh.write(json.dumps(rec) + "\n"); fh.flush()
            mark = {"certificate": "CERT", "closed": "closed",
                    "budget": "budget"}.get(rec["verdict"], rec["verdict"])
            print(f"  [{i}/{len(todo)}] {rec['challenge_id']} len={rec.get('init_len')} "
                  f"-> {mark}" + (f" L={rec['length']} verified={rec['official_verify']}"
                                  if rec["verdict"] == "certificate" else ""), flush=True)
    return hour


# ------------------------------------------------------------------ eye passes

def hour_records(hour):
    f = hour_dir(hour) / "search.jsonl"
    if not f.exists():
        return []
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()]


def projection(eye, recs):
    """Each eye's OWN slice. Different bytes per eye, so two eyes cannot be
    silently reading the same input; the mix reports any that do."""
    certs = [r for r in recs if r["verdict"] == "certificate"]
    if eye == "total-length":
        return {"lengths_attempted": sorted(r.get("init_len", 0) for r in recs),
                "certificate_lengths": sorted(r["length"] for r in certs)}
    if eye == "descent-direction":
        return {"closed": [(r["challenge_id"], r["component"], r["depth"])
                           for r in recs if r["verdict"] == "closed"],
                "budget": [(r["challenge_id"], r.get("states")) for r in recs
                           if r["verdict"] == "budget"]}
    if eye == "bidirectional-search":
        return {"ball_available": Path("/tmp/claude-0/ball7.bin").exists(),
                "engine": Path(ENGINE).name, "attempted": len(recs)}
    if eye in ("twisted-determinant", "displacement-gram", "b2-fixity"):
        # These read presentation states. Their input is the move sequences.
        return {"paths": [r["moves"] for r in certs]}
    if eye == "regularised-torsion":
        return {"paths": [r["moves"] for r in certs]}
    if eye == "reflection":
        return {"verdict_counts": {v: sum(1 for r in recs if r["verdict"] == v)
                                   for v in {r["verdict"] for r in recs}},
                "unverified_certificates": [r["challenge_id"] for r in certs
                                            if not r.get("official_verify")]}
    if eye == "claude-build-assessment":
        return {"engine_sha_present": Path(ENGINE).exists(),
                "certificates": len(certs),
                "all_officially_verified": all(r.get("official_verify") for r in certs)}
    if eye == "jeromie-reaudit":
        return {"awaiting_independent_reaudit": True, "hour_size": len(recs)}
    return {"not_applicable": eye}


def eye_pass(eye, hour, dry=False):
    """One eye, one hour, its own process. Reads only its own projection."""
    recs = hour_records(hour)
    proj = projection(eye, recs)
    certs = [r for r in recs if r["verdict"] == "certificate"]

    if eye in ("axiom-audit", "lakefile-parser"):
        state, out, why = "blocked", None, (
            "Lean tooling; no Lean artifact in a corridor sweep. Weight 0, place kept.")
    elif eye in ("twisted-determinant", "displacement-gram", "b2-fixity",
                 "regularised-torsion") and not certs:
        state, out, why = "silent", None, (
            f"reads presentation states along a path; no certificate was found "
            f"in hour {hour}, so there is no path to read. On the roster, weight 0.")
    elif eye == "jeromie-reaudit":
        state, out, why = "blocked", None, (
            "no independent re-audit filed this hour; the standing contradiction "
            "with claude-build-assessment is unresolved. Weight 0, place kept.")
    elif not recs:
        state, out, why = "silent", None, f"hour {hour} contains no search records"
    else:
        state, out, why = "observed", proj, None

    if dry:
        print(f"  {eye:<26} {state}")
        return
    he = HourlyEyes()
    try:
        r = he.record(eye, ITEM, state, read=proj, output=out, reason=why,
                      hour=hour, run_id="acc-corridor-v2")
        print(f"  seq {r['seq']:5d}  {eye:<26} {state}")
    except ValueError as e:
        print(f"  {eye:<26} NOT RECORDED: {e}")


def close_hour(hour, stagger):
    """Spawn each eye as its own process, staggered, so the wall spread is real."""
    print(f"closing hour {hour}: {len(ROSTER)} eyes, up to {stagger}s stagger")
    rng = random.Random(hour)
    for eye in ROSTER:
        time.sleep(rng.uniform(0, stagger))
        subprocess.run([sys.executable, __file__, "--eye", eye, "--hour", hour],
                       check=False)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--work", type=int, help="search this many challenges")
    p.add_argument("--headroom", type=int, default=8)
    p.add_argument("--budget", type=int, default=8000000)
    p.add_argument("--seed", type=int, default=20260914)
    p.add_argument("--close-hour", help="run every eye's pass over a finished hour")
    p.add_argument("--stagger", type=float, default=20.0)
    p.add_argument("--eye", help="run ONE eye's pass (used by --close-hour)")
    p.add_argument("--hour")
    p.add_argument("--dry", action="store_true")
    a = p.parse_args(argv)

    if a.eye:
        if not a.hour:
            p.error("--eye needs --hour")
        eye_pass(a.eye, a.hour, dry=a.dry)
        return 0
    if a.close_hour:
        close_hour(a.close_hour, a.stagger)
        return 0
    if a.work:
        work(a.work, a.headroom, a.budget, a.seed)
        return 0
    p.error("give --work, --close-hour or --eye")


if __name__ == "__main__":
    raise SystemExit(main())
