#!/usr/bin/env python3
"""Write targets_g1.csv (k_teams<=2, gap 1..8, longest record first) and targets_g2.csv (unsolved ac rows with
initial relator total <= 16, shortest first).  Never-rows are excluded.  The CSV has CRLF line ends."""
import argparse, csv, json, re, os
ap = argparse.ArgumentParser(); ap.add_argument("--sair", required=True); ap.add_argument("--csv", required=True); ap.add_argument("--out", required=True)
a = ap.parse_args()
man = json.load(open(os.path.join(a.sair, "competition/tools/verifier/data/manifest.json")))
REL = {c["challenge_id"]: c["initial_relators"] for c in man["challenges"]}
R = list(csv.DictReader(open(a.csv, newline="")))
never = {"09839", "02257", "09311", "06403", "04718", "05378"}
t = [r for r in R if re.match(r"gap [1-8]\s*$", r["status"]) and int(r["k_teams"]) <= 2 and r["row"][-5:] not in never]
t.sort(key=lambda r: -int(r["record"]))
open(os.path.join(a.out, "targets_g1.csv"), "w").write("".join(f"{r['row']},{r['our_best_road']},{r['record']}\n" for r in t))
u = [(sum(map(len, REL[r["row"]])), r["row"]) for r in R
     if r["status"].startswith("UNSOLVED") and r["row"].startswith("ac-") and r["row"][-5:] not in never]
u = sorted(x for x in u if x[0] <= 16)
open(os.path.join(a.out, "targets_g2.csv"), "w").write("".join(f"{c},,\n" for _, c in u))
print(len(t), "group-1 rows;", len(u), "group-2 rows")
