#!/usr/bin/env python3
# SCRIPT: acc_smith_snell
"""acc_smith_snell v1 — Smith-chart and Snell-law channels for the Compound Eye mixer.

Ideas (layered Smith chart, Snell law, penultimate corridor) are the repository
author's; this file only executes the mathematics.  Six-layer formula per
research/acc/ACC_SMITH_MIXER_PLAN.md (GPT lane); Map A per Grok lane.

Replays the 424 official ac-r2-v1 training solutions through the official
verifier (via acc_run_decoder_v2.replay, which calls verifier.core.apply_move)
and, at every replayed state, computes:

  * Map A (Grok, 2026-09-13):  gammaA_k = (L_k - L_{k-1}) / (L_k + L_{k-1})
  * six Smith layers from research/acc/ACC_SMITH_MIXER_PLAN.md:
        pair axes (2,3) (4,5) (6,7) (8,9) (10,11) (12,13)
        d+ = L(m+(P)) - L(P),  d- = L(m-(P)) - L(P)
        q = (d+ + d-) / (2 s),  p = (d- - d+) / (2 s),  s = 2
        Z = exp(q) + i p,  Gamma = (Z - 1) / (Z + 1)          (|Gamma| < 1)
    The one-move lookahead uses only verifier.core.apply_move.
  * "taken layer": the layer whose pair contains the move actually taken at
    step k (None for inversions and step 0); its Gamma is `smith_re`/`smith_im`.
  * Snell quantities on the taken layer, with refractive index n := total length:
        theta_in  = arg Gamma_layer(P_{k-1}),  theta_out = arg Gamma_layer(P_k)
        snell_in  = L_{k-1} * sin(theta_in),   snell_out = L_k * sin(theta_out)
        snell_sign_agree = 1 if sign(Im Gamma_layer(P_{k-1})) matches the move
        taken (m+ favored when p > 0, m- when p < 0), 0 if opposite, -1 if p == 0.

Display telemetry only: none of this is an invariant, a distance or a proof.
Exact replay stays authoritative.  Python 3 stdlib only.  New files only.
"""
import argparse, cmath, json, math, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D  # noqa: E402

VERSION = "acc_smith_snell v1"
PAIR_AXES = (("mul_r0_r1", 2, 3), ("mul_r1_r0", 4, 5), ("conj_r0_x", 6, 7),
             ("conj_r0_y", 8, 9), ("conj_r1_x", 10, 11), ("conj_r1_y", 12, 13))
SCALE = 2.0


def smith_layers(core, state):
    L0 = sum(len(w) for w in state)
    out = []
    for name, mp, mm in PAIR_AXES:
        dp = sum(len(w) for w in core.apply_move(state, mp)) - L0
        dm = sum(len(w) for w in core.apply_move(state, mm)) - L0
        q = (dp + dm) / (2.0 * SCALE)
        p = (dm - dp) / (2.0 * SCALE)
        Z = complex(math.exp(q), p)
        g = (Z - 1.0) / (Z + 1.0)
        if abs(g) >= 1.0 + 1e-12:
            raise AssertionError("Smith map escaped unit disk")
        out.append({"name": name, "mp": mp, "mm": mm, "dp": dp, "dm": dm, "q": q, "p": p, "re": g.real, "im": g.imag,
                    "radius": abs(g), "angle": cmath.phase(g)})
    return out


def layer_of_move(m):
    for i, (_, mp, mm) in enumerate(PAIR_AXES):
        if m in (mp, mm):
            return i, (+1 if m == mp else -1)
    return None, 0


def enrich(core, initial, moves, steps):
    """Add Smith/Snell channels to decoder step rows; recomputes states via official apply_move."""
    state = tuple(tuple(w) for w in initial)
    layers_prev = smith_layers(core, state)
    rows = []
    for k, r in enumerate(steps):
        if k > 0:
            state = core.apply_move(state, moves[k - 1])
        layers = smith_layers(core, state) if k > 0 else layers_prev
        L = r["total_length"]
        Lp = steps[k - 1]["total_length"] if k > 0 else L
        gammaA = 0.0 if k == 0 else (L - Lp) / (L + Lp)
        row = {"gammaA": gammaA}
        for i, ly in enumerate(layers):
            for key in ("q", "p", "re", "im", "radius", "angle"):
                row[f"L{i}_{key}"] = ly[key]
        li, sgn = layer_of_move(moves[k - 1]) if k > 0 else (None, 0)
        if li is None:
            row.update({"taken_layer": -1, "smith_re": 0.0, "smith_im": 0.0, "smith_radius": 0.0, "smith_angle": 0.0,
                        "snell_in": 0.0, "snell_out": 0.0, "snell_sign_agree": -1})
        else:
            lo, ln = layers_prev[li], layers[li]
            agree = -1 if lo["p"] == 0 else (1 if (lo["p"] > 0) == (sgn > 0) else 0)
            row.update({"taken_layer": li, "smith_re": ln["re"], "smith_im": ln["im"], "smith_radius": ln["radius"],
                        "smith_angle": ln["angle"], "snell_in": Lp * math.sin(lo["angle"]),
                        "snell_out": L * math.sin(ln["angle"]), "snell_sign_agree": agree})
        row["run_fraction"] = k / max(1, len(steps) - 1)
        rows.append(row)
        layers_prev = layers
    return rows


def dataset(rec, steps, rows):
    base = D.mixer_dataset(rec)
    x = base["x"]
    def tr(id_, label, unit, vals, route="y", enabled=False):
        return {"id": id_, "label": label, "unit": unit, "source": VERSION + " (official verifier replay + one-move lookahead)",
                "values": vals, "defaultRoute": route, "defaultEnabled": enabled}
    traces = list(base["traces"])
    traces.append(tr("gammaA", "Map A reflection coefficient (L-Lprev)/(L+Lprev)", "reflection coefficient", [r["gammaA"] for r in rows], "x", True))
    traces.append(tr("smith_re", "Smith Re Gamma, layer of the move taken", "reflection coefficient", [r["smith_re"] for r in rows], "x", True))
    traces.append(tr("smith_im", "Smith Im Gamma, layer of the move taken", "reflection coefficient", [r["smith_im"] for r in rows], "y", True))
    traces.append(tr("smith_radius", "|Gamma| of the taken layer", "reflection coefficient", [r["smith_radius"] for r in rows]))
    traces.append(tr("smith_angle", "arg Gamma of the taken layer", "radians", [r["smith_angle"] for r in rows]))
    traces.append(tr("taken_layer", "pair-axis index of the move taken (-1 inversion/start)", "code", [r["taken_layer"] for r in rows]))
    traces.append(tr("snell_in", "L_prev * sin(arg Gamma_layer(P_prev))", "letters*sin", [r["snell_in"] for r in rows]))
    traces.append(tr("snell_out", "L * sin(arg Gamma_layer(P))", "letters*sin", [r["snell_out"] for r in rows]))
    traces.append(tr("snell_sign_agree", "1 = move taken agrees with sign(p) of its layer before the step; 0 = opposite; -1 = p==0/none", "flag", [r["snell_sign_agree"] for r in rows]))
    traces.append(tr("run_fraction", "k / (steps-1)", "fraction", [r["run_fraction"] for r in rows]))
    for i, (name, mp, mm) in enumerate(PAIR_AXES):
        traces.append(tr(f"L{i}_re", f"layer {i} {name} ({mp},{mm}) Re Gamma", "reflection coefficient", [r[f"L{i}_re"] for r in rows], "x"))
        traces.append(tr(f"L{i}_im", f"layer {i} {name} ({mp},{mm}) Im Gamma", "reflection coefficient", [r[f"L{i}_im"] for r in rows], "y"))
        traces.append(tr(f"L{i}_p", f"layer {i} {name} signed imbalance p", "display units", [r[f"L{i}_p"] for r in rows]))
        traces.append(tr(f"L{i}_q", f"layer {i} {name} common pressure q", "display units", [r[f"L{i}_q"] for r in rows]))
    base["traces"] = traces
    base["id"] = base["id"] + "__smith"
    base["title"] = base["title"] + " — Smith/Snell v1"
    base["description"] = (base.get("description", "") + " Smith layers: Z=exp(q)+ip, Gamma=(Z-1)/(Z+1), s=2 "
                           "(research/acc/ACC_SMITH_MIXER_PLAN.md). Display telemetry only; not an invariant, distance or proof.")
    return base


def recipe(ds):
    s = D.recipe_settings(ds, normalization="rms")
    return {"schema": "compound-eye-mixer-recipe-v1", "engine_version": "1.0.0", "dataset": ds, "settings": s, "baseline": None,
            "meaning": "A reproducible visual composition; weights, centering and smoothing are chosen display operations, not automatically physical laws."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    ap.add_argument("--out-dir", default=os.path.join(HERE, "smith_snell_v1"))
    ap.add_argument("--control", default="ms-train-0160")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    core, stable_core, specs = D.load_verifier(a.sair)
    os.makedirs(os.path.join(a.out_dir, "recipes"), exist_ok=True)
    limits, _manifest = D.load_manifest(a.sair)
    training = D.load_training(a.sair, "ac-r2-v1")
    summary = {"version": VERSION, "runs": 0, "steps": 0, "disk_violations": 0, "control": None,
               "snell": {"agree": 0, "disagree": 0, "undecided": 0, "strict_law_within_0p5": 0, "strict_law_total": 0},
               "radius_by_third": [[0.0, 0], [0.0, 0], [0.0, 0]], "delta_neg": 0, "delta_pos": 0, "delta_zero": 0,
               "mapA_axis_cells_40": None}
    cells = set()
    ledger = []
    for n, (c, moves) in enumerate(training):
        if a.limit and n >= a.limit:
            break
        cid = c["challenge_id"]
        steps, err = D.replay(core, stable_core, "ac-r2-v1", c["initial_relators"], moves)
        if err:
            print("REPLAY ERROR", cid, err); sys.exit(2)
        rows = enrich(core, c["initial_relators"], moves, steps)
        rec = D.run_record(c, moves, "ac-r2-v1", "training", steps, None, specs.get("ac-r2-v1").verify(c, moves, "ac-r2-v1", limits))
        ds = dataset(rec, steps, rows)
        rp = recipe(ds)
        fn = os.path.join(a.out_dir, "recipes", f"{cid}__training__smith_recipe.json")
        with open(fn, "w") as f:
            json.dump(rp, f, separators=(",", ":"))
        summary["runs"] += 1
        summary["steps"] += len(rows) - 1
        for k, r in enumerate(rows):
            if k == 0:
                continue
            if math.hypot(r["smith_re"], r["smith_im"]) >= 1.0:
                summary["disk_violations"] += 1
            d = steps[k]["delta_total"]
            summary["delta_neg" if d < 0 else "delta_pos" if d > 0 else "delta_zero"] += 1
            cells.add(int((r["gammaA"] + 1) * 20))
            if r["taken_layer"] >= 0:
                sn = summary["snell"]
                sn["agree" if r["snell_sign_agree"] == 1 else "disagree" if r["snell_sign_agree"] == 0 else "undecided"] += 1
                sn["strict_law_total"] += 1
                if abs(r["snell_in"] - r["snell_out"]) < 0.5:
                    sn["strict_law_within_0p5"] += 1
                t = min(2, int(r["run_fraction"] * 3))
                summary["radius_by_third"][t][0] += r["smith_radius"]; summary["radius_by_third"][t][1] += 1
        if cid == a.control:
            summary["control"] = [{"step": k, "L_prev": steps[k - 1]["total_length"] if k else None, "L": steps[k]["total_length"],
                                   "gammaA": rows[k]["gammaA"], "move": steps[k]["move_id"], "taken_layer": rows[k]["taken_layer"],
                                   "smith_re": round(rows[k]["smith_re"], 6), "smith_im": round(rows[k]["smith_im"], 6),
                                   "snell_sign_agree": rows[k]["snell_sign_agree"]} for k in range(len(rows))]
        ledger.append({"challenge_id": cid, "source": "training", "moves_hash": rec["moves_hash"], "steps": len(rows) - 1, "recipe": os.path.relpath(fn, HERE)})
    summary["mapA_axis_cells_40"] = len(cells)
    summary["radius_by_third"] = [round(s / n, 4) if n else None for s, n in summary["radius_by_third"]]
    with open(os.path.join(a.out_dir, "smith_snell_runs.jsonl"), "w") as f:
        for l in ledger:
            f.write(json.dumps(l) + "\n")
    with open(os.path.join(a.out_dir, "SUMMARY.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
