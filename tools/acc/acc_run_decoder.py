#!/usr/bin/env python3
# SCRIPT: acc_run_decoder
"""Replay Andrews-Curtis move sequences into Compound Eye channel traces.

Every replay goes through the OFFICIAL SAIR verifier (``verifier.core`` for
``ac-`` ids, ``verifier.stable_core`` for ``sac-`` ids), imported from
``<sair>/competition/tools``.  No move is re-implemented here.

Outputs
  A. one Compound Eye import file per run, schema ``compound-eye-traces-v1``
     (the import shape validated by tools/compound-eye/projects/eye_mixer/
     mixer_core.js ``validate``; see --validate-node),
  B. one JSON line per run appended to a ledger (append-only; a line with the
     same challenge_id + source + moves hash is updated in place),
  C. SUMMARY.md with corpus statistics.

Usage
  python3 tools/acc/acc_run_decoder.py --sair <checkout> --training
  python3 tools/acc/acc_run_decoder.py --sair <checkout> --submission submission.txt
  python3 tools/acc/acc_run_decoder.py --sair <checkout> --candidates candidates.jsonl
  python3 tools/acc/acc_run_decoder.py --sair <checkout> --control   # ms-train-0160 table only

Python 3 standard library only.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, OrderedDict

DECODER_VERSION = "acc_run_decoder v1"
SCHEMA = "compound-eye-traces-v1"
MOVE_CLASS = {"inversion": "invert", "multiplication": "multiply",
              "conjugation": "conjugate", "stabilize": "stabilize",
              "destabilize": "destabilize"}
MOVE_CLASS_CODE = {"invert": 1, "multiply": 2, "conjugate": 3, "stabilize": 4, "destabilize": 5}
MAX_RELATORS = 8  # sac-r8-v1 rank bound; len_r0..len_r7 are always emitted


# ----------------------------------------------------------------------------
# official verifier import

def load_verifier(sair_root):
    tools = os.path.join(sair_root, "competition", "tools")
    if not os.path.isdir(os.path.join(tools, "verifier")):
        sys.exit("verifier package not found under %s" % tools)
    if tools not in sys.path:
        sys.path.insert(0, tools)
    from verifier import core, stable_core, specs  # noqa: E402
    # confirm the frozen shapes we rely on
    assert core.GENS == (1, -1, 2, -2) and core.NUM_MOVES == 14
    assert stable_core.NUM_MOVES == 257 and stable_core.TARGET == ()
    assert all("category" in row and "inverse" in row for row in core.MOVE_TABLE)
    return core, stable_core, specs


def spec_for_id(challenge_id):
    if challenge_id.startswith("sac-"):
        return "sac-r8-v1"
    return "ac-r2-v1"  # ac- and ms-train- (training) ids


# ----------------------------------------------------------------------------
# exact integer invariant: |det| of the exponent-sum relation matrix

def exponent_matrix(state, n_gens):
    rows = []
    for w in state:
        r = [0] * n_gens
        for a in w:
            r[abs(a) - 1] += 1 if a > 0 else -1
        rows.append(r)
    return rows


def int_det(m):
    """Bareiss fraction-free determinant of a square integer matrix."""
    n = len(m)
    if n == 0:
        return 1
    a = [row[:] for row in m]
    sign = 1
    prev = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return sign * a[n - 1][n - 1]


def abelian_ok(state, n_gens):
    """1 iff the relation matrix has Smith normal form all ones.  For a
    balanced presentation (n_gens relators) that is |det| == 1.  Invariant
    under every AC / stable AC move; a 0 flags a broken replay."""
    if len(state) != n_gens:
        return 0
    return 1 if abs(int_det(exponent_matrix(state, n_gens))) == 1 else 0


# ----------------------------------------------------------------------------
# replay

def replay(core, stable_core, spec, initial, moves):
    """Return (steps, error).  steps[0] is the initial state."""
    stable = spec == "sac-r8-v1"
    mod = stable_core if stable else core
    table = mod.MOVE_TABLE
    state = tuple(tuple(w) for w in initial)
    target = tuple() if stable else ((1,), (2,))

    def rank(s):
        return len(s)

    def row_for(s, n_gens):
        lens = [len(w) for w in s] + [0] * (MAX_RELATORS - len(s))
        tot = sum(len(w) for w in s)
        return {"total_length": tot, "lens": lens[:MAX_RELATORS], "n_generators": n_gens,
                "abelian_ok": abelian_ok(s, n_gens),
                "dist_to_target": 0 if s == target else tot}

    n_gens = 2 if not stable else rank(state)
    steps = []
    r = row_for(state, n_gens)
    r.update({"step": 0, "move_id": -1, "move_class": "start", "delta_total": 0, "cancellations": 0})
    steps.append(r)
    prev_tot = r["total_length"]
    for k, m in enumerate(moves, 1):
        if type(m) is not int or not (0 <= m < mod.NUM_MOVES):
            return steps, {"code": "E_BAD_MOVE_ID", "move_index": k - 1, "move": m}
        row = table[m]
        cat = row["category"]
        cls = MOVE_CLASS[cat]
        # letters that free reduction removes this step: operand letters in minus result letters out
        if cat == "multiplication":
            i, j = row["relator"], row["other"]
            operand = (len(state[i]) + len(state[j])) if i < len(state) and j < len(state) else 0
        elif cat == "conjugation":
            i = row["relator"]
            operand = (len(state[i]) + 2) if i < len(state) else 0
        else:
            operand = None
        if stable:
            new, reason = stable_core.apply_move(state, m)
            if reason is not None:
                return steps, {"code": "E_MOVE_NOT_APPLICABLE", "move_index": k - 1, "move": m, "reason": reason}
        else:
            new = core.apply_move(state, m)
        state = new
        n_gens = 2 if not stable else rank(state)
        r = row_for(state, n_gens)
        if operand is None:
            canc = 0
        else:
            i = row["relator"]
            canc = operand - len(state[i])
        r.update({"step": k, "move_id": m, "move_class": cls,
                  "delta_total": r["total_length"] - prev_tot, "cancellations": canc})
        steps.append(r)
        prev_tot = r["total_length"]
    return steps, None


def run_record(challenge, moves, spec, source, steps, err, verdict):
    tots = [s["total_length"] for s in steps]
    mx = max(tots)
    step_of_max = tots.index(mx)
    longest = cur = 0
    for s in steps[1:]:
        cur = cur + 1 if s["delta_total"] == 0 else 0
        longest = max(longest, cur)
    return OrderedDict([
        ("challenge_id", challenge["challenge_id"]), ("spec", spec), ("source", source),
        ("decoder", DECODER_VERSION),
        ("moves_hash", "sha256:" + hashlib.sha256(json.dumps(moves, separators=(",", ":")).encode()).hexdigest()),
        ("n_moves", len(moves)), ("n_steps", len(steps)),
        ("initial_length", tots[0]), ("final_length", tots[-1]),
        ("final_ok", bool(verdict.get("ok"))), ("verdict", verdict),
        ("replay_error", err),
        ("max_length_reached", mx), ("step_of_max", step_of_max),
        ("growth_before_shrink", mx - tots[0]),
        ("longest_plateau", longest),
        ("abelian_ok_all", all(s["abelian_ok"] == 1 for s in steps)),
        ("move_class_by_third", thirds(steps)),
        ("moves", moves), ("steps", steps),
    ])


def thirds(steps):
    mv = [s["move_class"] for s in steps[1:]]
    n = len(mv)
    out = {}
    if n == 0:
        return out
    b = [0, (n + 2) // 3, (2 * n + 2) // 3, n]
    for name, (lo, hi) in zip(("first", "middle", "last"), zip(b, b[1:])):
        out[name] = dict(Counter(mv[lo:hi]))
    return out


# ----------------------------------------------------------------------------
# outputs

def mixer_dataset(rec):
    steps = rec["steps"]
    x = [s["step"] for s in steps]
    src = "%s; official SAIR verifier replay (%s); provenance: %s" % (DECODER_VERSION, rec["spec"], rec["source"])
    stable = rec["spec"] == "sac-r8-v1"
    traces = [
        ("total_length", "Total relator length", "letters", [s["total_length"] for s in steps], "x"),
        ("len_r0", "Length of r0", "letters", [s["lens"][0] for s in steps], "y"),
        ("len_r1", "Length of r1", "letters", [s["lens"][1] for s in steps], "y"),
    ]
    if stable:
        for i in range(2, MAX_RELATORS):
            traces.append(("len_r%d" % i, "Length of r%d (0 when absent)" % i, "letters", [s["lens"][i] for s in steps], "y"))
    traces += [
        ("n_generators", "Number of generators (rank)", "count", [s["n_generators"] for s in steps], "y"),
        ("delta_total", "Change in total length this step", "letters", [s["delta_total"] for s in steps], "y"),
        ("cancellations", "Letters removed by free reduction this step", "letters", [s["cancellations"] for s in steps], "y"),
        ("abelian_ok", "Relation matrix unimodular (invariant; 0 = broken replay)", "flag", [s["abelian_ok"] for s in steps], "y"),
        ("dist_to_target", "Distance-to-target proxy (0 only at exact target, else total length)", "letters (proxy)", [s["dist_to_target"] for s in steps], "y"),
        ("move_id", "Move id applied at this step (-1 at step 0)", "move id", [s["move_id"] for s in steps], "y"),
        ("move_class_code", "Move class code 1 invert 2 multiply 3 conjugate 4 stabilize 5 destabilize (0 at step 0)", "code",
         [MOVE_CLASS_CODE.get(s["move_class"], 0) for s in steps], "y"),
    ]
    sid = re.sub(r"[^A-Za-z0-9_.-]+", "_", rec["challenge_id"] + "__" + rec["source"])
    return OrderedDict([
        ("schema", SCHEMA), ("id", sid),
        ("title", "%s (%s) — %d moves" % (rec["challenge_id"], rec["spec"], rec["n_moves"])),
        ("description", "Per-step channels of one Andrews-Curtis move sequence replayed through the official verifier. "
                        "dist_to_target is a proxy label, not a distance. Step 0 is the initial presentation."),
        ("context", OrderedDict([("object_id", rec["challenge_id"]), ("model_id", rec["spec"]),
                                 ("coordinate", "step"), ("x_unit", "moves applied"),
                                 ("source_stage", rec["source"].split(":")[0])])),
        ("x", x),
        ("traces", [OrderedDict([("id", tid), ("label", lab), ("unit", unit), ("source", src),
                                 ("values", vals), ("defaultRoute", route)])
                    for tid, lab, unit, vals, route in traces]),
    ])


def write_ledger(path, records):
    """Append-only ledger keyed by (challenge_id, source, moves_hash); an existing
    key is updated in place, everything else is preserved in order."""
    existing = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    existing.append(json.loads(line))
    index = {(r["challenge_id"], r["source"], r["moves_hash"]): i for i, r in enumerate(existing)}
    added = updated = 0
    for r in records:
        key = (r["challenge_id"], r["source"], r["moves_hash"])
        if key in index:
            existing[index[key]] = r
            updated += 1
        else:
            index[key] = len(existing)
            existing.append(r)
            added += 1
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in existing:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")
    os.replace(tmp, path)
    return added, updated, len(existing)


def summarize(records, path, source):
    ok = sum(1 for r in records if r["final_ok"])
    n = len(records)

    def dist(key):
        v = sorted(r[key] for r in records)
        if not v:
            return "n/a"
        q = lambda p: v[min(len(v) - 1, int(p * (len(v) - 1)))]
        return "min %d · q1 %d · median %d · q3 %d · max %d · mean %.1f" % (v[0], q(.25), q(.5), q(.75), v[-1], sum(v) / len(v))

    pos = {"first": Counter(), "middle": Counter(), "last": Counter()}
    for r in records:
        for part, c in r["move_class_by_third"].items():
            pos[part].update(c)
    classes = sorted({c for p in pos.values() for c in p})
    lines = ["# ACC run decoder — summary (%s)" % source, "",
             "Decoder: %s · replay kernel: official SAIR verifier · schema: %s" % (DECODER_VERSION, SCHEMA), "",
             "| quantity | value |", "|---|---|",
             "| runs decoded | %d |" % n,
             "| verifier ok | %d/%d |" % (ok, n),
             "| abelian_ok == 1 at every step | %d/%d |" % (sum(1 for r in records if r["abelian_ok_all"]), n),
             "| n_moves | %s |" % dist("n_moves"),
             "| initial_length | %s |" % dist("initial_length"),
             "| max_length_reached − initial_length (growth before shrinking) | %s |" % dist("growth_before_shrink"),
             "| step_of_max | %s |" % dist("step_of_max"),
             "| longest_plateau (consecutive delta_total == 0) | %s |" % dist("longest_plateau"),
             "", "## Move class frequency by position in run", "",
             "| class | first third | middle third | last third |", "|---|---:|---:|---:|"]
    for c in classes:
        lines.append("| %s | %d | %d | %d |" % (c, pos["first"][c], pos["middle"][c], pos["last"][c]))
    grow = sum(1 for r in records if r["growth_before_shrink"] > 0)
    lines += ["", "Runs whose total length rose above the initial length at some step: %d/%d." % (grow, n),
              "dist_to_target is a proxy (0 only at the exact target); it is not a distance."]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return "\n".join(lines)


def step_table(steps):
    hdr = "step move class      tot r0 r1 dTot canc abel dist"
    out = [hdr]
    for s in steps:
        out.append("%4d %4d %-10s %3d %2d %2d %4d %4d %4d %4d" % (
            s["step"], s["move_id"], s["move_class"], s["total_length"], s["lens"][0], s["lens"][1],
            s["delta_total"], s["cancellations"], s["abelian_ok"], s["dist_to_target"]))
    return "\n".join(out)


# ----------------------------------------------------------------------------
# inputs

def load_training(sair_root, spec):
    name = "training_424.json" if spec == "ac-r2-v1" else "stable_training_424.json"
    with open(os.path.join(sair_root, "competition", "examples", name), encoding="utf-8") as f:
        d = json.load(f)
    out = []
    for inst in d["instances"]:
        c = dict(inst)
        c["challenge_id"] = inst["training_id"]
        out.append((c, inst["moves"]))
    return out


def load_manifest(sair_root):
    with open(os.path.join(sair_root, "competition", "tools", "verifier", "data", "manifest.json"), encoding="utf-8") as f:
        m = json.load(f)
    return m["limits"], {c["challenge_id"]: c for c in m["challenges"]}


def training_index(sair_root):
    idx = {}
    for spec in ("ac-r2-v1", "sac-r8-v1"):
        for c, moves in load_training(sair_root, spec):
            idx[(c["challenge_id"], spec)] = c
    return idx


def parse_submission(path):
    runs = []
    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(\[.*\])\s*$", line)
            if not m:
                print("submission line %d skipped (format): %s" % (ln, line[:80]), file=sys.stderr)
                continue
            try:
                moves = json.loads(m.group(2))
            except ValueError:
                print("submission line %d skipped (moves not JSON)" % ln, file=sys.stderr)
                continue
            runs.append((m.group(1), moves))
    return runs


def parse_candidates(path):
    runs = []
    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                print("candidates line %d skipped (not JSON)" % ln, file=sys.stderr)
                continue
            if not isinstance(d, dict) or "challenge_id" not in d or "moves" not in d:
                print("candidates line %d skipped (needs challenge_id and moves)" % ln, file=sys.stderr)
                continue
            runs.append((d["challenge_id"], d["moves"]))
    return runs


def resolve_challenge(cid, manifest, tindex):
    spec = spec_for_id(cid)
    if cid in manifest:
        return manifest[cid], manifest[cid]["move_spec_version"]
    if (cid, spec) in tindex:
        return tindex[(cid, spec)], spec
    return None, spec


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sair", default=os.environ.get("SAIR_DIR", "/home/user/saircompetition/andrews-curtis"))
    ap.add_argument("--training", action="store_true", help="decode the 424 official AC training solutions (default)")
    ap.add_argument("--stable-training", action="store_true", help="decode the 424 Stable AC training solutions")
    ap.add_argument("--submission", help="official-format submission.txt")
    ap.add_argument("--candidates", help="hub candidates.jsonl (challenge_id, moves per line)")
    ap.add_argument("--control", action="store_true", help="print the ms-train-0160 control table and exit")
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "decoded"))
    ap.add_argument("--ledger", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "decoded_runs.jsonl"))
    ap.add_argument("--no-mixer-files", action="store_true")
    a = ap.parse_args()
    core, stable_core, specs = load_verifier(a.sair)
    limits, manifest = load_manifest(a.sair)
    tindex = training_index(a.sair)

    if a.control:
        c = tindex[("ms-train-0160", "ac-r2-v1")]
        moves = [6, 4, 2, 9, 1, 4, 1]
        steps, err = replay(core, stable_core, "ac-r2-v1", c["initial_relators"], moves)
        v = specs.get("ac-r2-v1").verify(c, moves, "ac-r2-v1", limits)
        print(step_table(steps))
        final = tuple(tuple(w) for w in c["initial_relators"])
        for m in moves:
            final = core.apply_move(final, m)
        print("final state:", [list(w) for w in final], "| verifier:", v)
        return

    jobs = []  # (challenge dict, spec, moves, source)
    if a.submission:
        for cid, moves in parse_submission(a.submission):
            c, spec = resolve_challenge(cid, manifest, tindex)
            if c is None:
                print("unknown challenge_id %s: skipped" % cid, file=sys.stderr)
                continue
            jobs.append((c, spec, moves, "submission:" + os.path.basename(a.submission)))
    if a.candidates:
        for cid, moves in parse_candidates(a.candidates):
            c, spec = resolve_challenge(cid, manifest, tindex)
            if c is None:
                print("unknown challenge_id %s: skipped" % cid, file=sys.stderr)
                continue
            jobs.append((c, spec, moves, "candidates"))
    if a.stable_training:
        for c, moves in load_training(a.sair, "sac-r8-v1"):
            jobs.append((c, "sac-r8-v1", moves, "training"))
    if a.training or not jobs:
        for c, moves in load_training(a.sair, "ac-r2-v1"):
            jobs.append((c, "ac-r2-v1", moves, "training"))

    os.makedirs(a.out_dir, exist_ok=True)
    records = []
    for c, spec, moves, source in jobs:
        steps, err = replay(core, stable_core, spec, c["initial_relators"], moves)
        verdict = specs.get(spec).verify(c, moves, spec, limits)
        rec = run_record(c, moves, spec, source, steps, err, verdict)
        records.append(rec)
        if not a.no_mixer_files:
            ds = mixer_dataset(rec)
            with open(os.path.join(a.out_dir, ds["id"] + ".json"), "w", encoding="utf-8") as f:
                json.dump(ds, f, indent=1)
    added, updated, total = write_ledger(a.ledger, records)
    src_label = ",".join(sorted({r["source"] for r in records}))
    text = summarize(records, os.path.join(a.out_dir, "SUMMARY.md"), src_label)
    print(text)
    print("\nledger %s: +%d added, %d updated, %d lines total" % (a.ledger, added, updated, total))
    bad = [r["challenge_id"] for r in records if not r["abelian_ok_all"]]
    if bad:
        print("ABELIAN INVARIANT BROKEN in: %s" % bad, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
