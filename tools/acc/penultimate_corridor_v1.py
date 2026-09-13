#!/usr/bin/env python3
# SCRIPT: penultimate_corridor
"""penultimate_corridor v1 — routing telemetry for the war-room 'penultimate state' eye.

Penultimate state := exactly one relator is a single letter and the other is not.
Reads the Smith/Snell v1 recipes (already replayed via the official verifier; no
move re-implementation here) and reports, per run: first entry step, run fraction
at entry, the other relator's length at entry, moves from entry to finish, whether
the run ever leaves the corridor again, and the move classes used after entry.
Telemetry only — never proof, never pruning.  Python 3 stdlib only.
"""
import glob, json, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
after_classes = {"invert": 0, "multiply": 0, "conjugate": 0}
finish_moves = {}
for f in sorted(glob.glob(os.path.join(HERE, "smith_snell_v1", "recipes", "*.json"))):
    d = json.load(open(f))["dataset"]
    tr = {t["id"]: t["values"] for t in d["traces"]}
    r0, r1, mv, cls = tr["len_r0"], tr["len_r1"], tr["move_id"], tr["move_class_code"]
    n = len(r0) - 1
    inside = [((a == 1) != (b == 1)) for a, b in zip(r0, r1)]
    entry = next((k for k, v in enumerate(inside) if v), None)
    if entry is None:
        rows.append({"id": d["id"], "steps": n, "entry": None}); continue
    other = r1[entry] if r0[entry] == 1 else r0[entry]
    # leaves = returns to a state where NEITHER relator is a single letter (states with both single letters, e.g. (x, y^-1), are target-adjacent and not counted)
    leaves = any((r0[k] != 1 and r1[k] != 1) for k in range(entry, n))
    both_single_before_end = any((r0[k] == 1 and r1[k] == 1) for k in range(entry, n))
    for k in range(entry + 1, n + 1):
        after_classes[{1: "invert", 2: "multiply", 3: "conjugate"}[cls[k]]] += 1
    finish_moves[mv[n]] = finish_moves.get(mv[n], 0) + 1
    rows.append({"id": d["id"], "steps": n, "entry": entry, "entry_fraction": round(entry / n, 3) if n else None,
                 "other_len_at_entry": other, "moves_after_entry": n - entry, "leaves_corridor": leaves,
                 "entry_move": mv[entry], "entry_class": cls[entry], "both_single_before_end": both_single_before_end})
ent = [r for r in rows if r["entry"] is not None]
summ = {"runs": len(rows), "runs_entering_corridor": len(ent), "runs_never_entering": len(rows) - len(ent),
        "entry_fraction_median": st.median(r["entry_fraction"] for r in ent),
        "other_len_at_entry": {"median": st.median(r["other_len_at_entry"] for r in ent), "max": max(r["other_len_at_entry"] for r in ent),
                               "hist": {str(k): sum(1 for r in ent if r["other_len_at_entry"] == k) for k in sorted({r["other_len_at_entry"] for r in ent})}},
        "moves_after_entry_median": st.median(r["moves_after_entry"] for r in ent), "moves_after_entry_max": max(r["moves_after_entry"] for r in ent),
        "runs_leaving_corridor_after_entry": sum(1 for r in ent if r["leaves_corridor"]),
        "runs_with_both_single_letters_before_final": sum(1 for r in ent if r["both_single_before_end"]),
        "entry_class_counts": {str(k): sum(1 for r in ent if r["entry_class"] == k) for k in (1, 2, 3)},
        "move_classes_after_entry": after_classes, "final_move_id_counts": dict(sorted(finish_moves.items())),
        "note": "corridor = exactly one relator is a single letter; telemetry only"}
json.dump({"summary": summ, "runs": rows}, open(os.path.join(HERE, "penultimate_corridor_v1.json"), "w"), indent=1)
print(json.dumps(summ, indent=1))
