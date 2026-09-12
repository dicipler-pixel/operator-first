"""Build a labeled ACC eye-calibration table from solved certificates.

One row per state along each verified path; columns are the pinned eyes
(total length, hab, foxA, frozen cancellation eye, start-orbit flags), the
six Smith-layer one-step length responses from acc-smith-mixer-2026-09-12,
and the label `remaining` = moves left to the target. The table is the
raw input for a mixer (e.g. Compound Eye 500) or for the direct rank
correlations printed by --report.

    PYTHONPATH=<sair>/competition/tools python3 calibrate_eyes.py \
        --manifest <manifest> --certs a.jsonl [b.jsonl ...] --out rows.csv [--report]

Caveats that travel with the table: the certificates are length-first
search outputs, so total length correlates with `remaining` partly by
construction; `r0_off`/`r1_off` are relative to each path's own start and
flip once, so their within-path correlation with step is an artefact.
"""
import argparse, cmath, csv, json, math, statistics, sys
from collections import defaultdict

from verifier import core
import eyes

PAIRS = [((2, 3), "m01"), ((4, 5), "m10"), ((6, 7), "c0x"), ((8, 9), "c0y"), ((10, 11), "c1x"), ((12, 13), "c1y")]


def smith(state, scale=2.0):
    L0 = eyes.total(state); out = {}
    for (mp, mm), nm in PAIRS:
        dp = eyes.total(core.apply_move(state, mp)) - L0
        dm = eyes.total(core.apply_move(state, mm)) - L0
        q = (dp + dm) / (2 * scale); p = (dm - dp) / (2 * scale)
        Z = complex(math.exp(q), p); g = (Z - 1) / (Z + 1)
        out.update({f"sm_{nm}_dplus": dp, f"sm_{nm}_dminus": dm, f"sm_{nm}_radius": round(abs(g), 4), f"sm_{nm}_angle": round(cmath.phase(g), 4)})
    return out


def rows_for(cid, start, moves):
    st = start; states = [st]
    for m in moves:
        st = core.apply_move(st, m); states.append(st)
    if st != ((1,), (2,)):
        return None
    n = len(moves); out = []
    for i, s in enumerate(states):
        ce = eyes.cancellation_eye(s); fl = eyes.orbit_flags(s, start); L0 = eyes.total(s)
        r = {"challenge": cid, "step": i, "remaining": n - i, "path_len": n, "tot": L0, "len_r0": len(s[0]), "len_r1": len(s[1]),
             "hab": eyes.hab(s), "foxA": eyes.foxA(s), "cyc_tot": ce["cyclic_tot"], "k": ce["k"], "surplus": ce["surplus"],
             "floor": ce["floor"], "floor_gap": L0 - ce["floor"], "r0_off": int(fl["r0_off"]), "r1_off": int(fl["r1_off"]), "pair_off": int(fl["pair_off"])}
        r.update(smith(s)); r["min_child_delta"] = min(eyes.total(core.apply_move(s, m)) - L0 for m in range(14))
        out.append(r)
    return out


def spearman(a, b):
    def ranks(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for k, i in enumerate(o): r[i] = k
        return r
    a, b = ranks(a), ranks(b); ma, mb = statistics.mean(a), statistics.mean(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else 0.0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--manifest", required=True); ap.add_argument("--certs", nargs="+", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--report", action="store_true"); a = ap.parse_args()
    ch = {c["challenge_id"]: c for c in json.load(open(a.manifest))["challenges"]}
    best = {}
    for f in a.certs:
        for l in open(f):
            try: d = json.loads(l)
            except ValueError: continue
            if d.get("ok") and d.get("moves") and (d["challenge_id"] not in best or len(d["moves"]) < len(best[d["challenge_id"]])):
                best[d["challenge_id"]] = d["moves"]
    rows = []; failed = 0
    for cid, mv in sorted(best.items()):
        r = rows_for(cid, tuple(tuple(x) for x in ch[cid]["initial_relators"]), mv)
        if r is None: failed += 1
        else: rows.extend(r)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"certificates {len(best)}, failed replay {failed}, rows {len(rows)}", file=sys.stderr)
    if a.report:
        by = defaultdict(list)
        for r in rows: by[r["challenge"]].append(r)
        feats = [k for k in rows[0] if k not in ("challenge", "step", "remaining", "path_len")]
        print("feature            pooled   within-path mean (paths>=16 states)")
        for fe in feats:
            pooled = spearman([r[fe] for r in rows], [r["remaining"] for r in rows])
            within = [spearman([r[fe] for r in v], [r["remaining"] for r in v]) for v in by.values() if len(v) >= 16]
            print(f"{fe:18s} {pooled:+.3f}    {statistics.mean(within):+.3f}")


if __name__ == "__main__":
    main()
