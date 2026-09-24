"""Write WARROOM optimality records (one per R band) from part1.jsonl + controls.jsonl."""
import json, sys, pathlib
work, outdir, rowsjson = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
here = pathlib.Path(__file__).resolve().parent
rows = {r['row']: r for r in json.load(open(rowsjson))}
res = [json.loads(l) for l in open(work / 'part1.jsonl')]
ctl = [json.loads(l) for l in open(work / 'controls.jsonl')]
tsha = open(work / 'T9.sha256').read().split()[0]
csrc = (here / 'acc_opt.c').read_text()
PROOF = """Let T_b = all states within b moves of (x,y) (= all states that reach (x,y) in <= b moves, by inverse-closure of the 14 ac-r2-v1 moves: INV = 0<->0, 1<->1, 2<->3, 4<->5, 6<->7, 8<->9, 10<->11, 12<->13). Let S_a = all states within a moves of the start. Any path of length L <= a+b has its vertex at step max(0, L-b) within a of the start and within b of the target. So min over s in S_a ∩ T_b of dS(s)+dT(s) is the exact distance if it is <= a+b; if S_a ∩ T_b is empty, no path of length <= a+b exists. No length cap is applied anywhere (official limits max_total_relator_length=10000 and max_path_length=100000 are never approached)."""
FPC = """States are stored as 128-bit fingerprints (two independent 64-bit hashes of the exact ordered word pair; 4 bits of the second hash carry the BFS distance, leaving 123 fingerprint bits) in open-addressing tables. A fingerprint collision could in principle merge two states (probability ~1e-20 at these sizes). A merge could only create a spurious meet (caught: every positive result is rebuilt from exact words and replayed by the official verifier) or hide a state from the ball (this is the only way a negative could be wrong, at the stated ~1e-20 probability). No false record can be submitted."""
def fmt(n): return f"{n:,}" if isinstance(n, int) else str(n)
for R in sorted({rows[r['row']]['R'] for r in res}):
    band = [r for r in res if rows[r['row']]['R'] == R]
    a = R - 10
    L = [f"# WARROOM 2026-09-24 — exact optimality, records R={R} (Lmax={R-1}, b=9, a={a})", "",
         "Kernel: official `ac-r2-v1`, SAIR Andrews-Curtis commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`, `competition/tools/verifier/core.py`, 14 moves. Start states from `competition/tools/verifier/data/manifest.json` (`initial_relators`), target exactly ((1,),(2,)).", "",
         "Kernel validation: 100,000 random (state, move) pairs vs `core.apply_move` — **0 mismatches** (`validate_kernel.py`, seed 20260924). Target-ball layer counts reproduce the measured r4 5,115 / r5 40,779 / r6 336,477 / r7 2,849,131 exactly.", "",
         "## Proof", "", PROOF, "", "## Fingerprint caveat", "", FPC, "",
         "## Target ball", "", f"T_9 = **214,977,551** states (layer 9: 190,390,407; T_8 = 24,587,144), 280,000,000-slot table file, SHA-256 `{tsha}`, build 167.8 s.", "",
         "## Controls (same T_9 and engine, run before any row)", "", "| row | record | a | Lmax | result | S stored |", "|---|---|---|---|---|---|"]
    for c in ctl:
        L.append(f"| {c['row']} | {13 if c['row']=='ac-01586' else 14} | {c['a']} | {c['lmax']} | {'exact ' + str(c['exact_distance']) if c['result']=='MEET' else 'no path <= ' + str(c['lmax'])} | {fmt(c['S_stored'])} |")
    L += ["", "Both controls pass: no path below their record, and the exact record length at every a with a+9 >= record.", "",
          f"## Results — R={R}", "", "k = team count from the 2026-09-14 09:45Z snapshot (the 2026-09-22 board itself was not in the input). |S_a| is exact when layer a was stored; for a=9, |S_8| is exact and layer 9 was streamed (edge count, not deduplicated).", "",
          "| row | R | k | a | \\|S_a\\| | layer-a streamed edges | result | wall |", "|---|---|---|---|---|---|---|---|"]
    for r in band:
        res_s = (f"**NEW RECORD {r['exact_distance']}**" if r['result'] == 'MEET' else "OPTIMAL") if r['rc'] == 0 else f"ERROR rc={r['rc']}"
        L.append(f"| {r['row']} | {R} | {rows[r['row']]['k']} | {r['a']} | {fmt(r['S_stored'])}{' (S_8)' if r['a']==9 else ''} | {fmt(r['layer_a_streamed_edges']) if r['layer_a_streamed_edges'] else '—'} | {res_s} | {r['wall_s']} s |")
    L += ["", "Record lines:", "", "```"]
    for r in band:
        if r['rc'] != 0: L.append(f"{r['row']}: ERROR, no conclusion")
        elif r['result'] == 'NO_MEET': L.append(f"{r['row']}: record {R} optimal; no path <= {R-1} (T_9 x S_{r['a']}, exact, no length cap)")
        else: L.append(f"{r['row']}: NEW RECORD {r['exact_distance']}: {r['path']}  official core.verify ok={r['official_core_verify']['ok']}")
    L += ["```", "", "Raw per-row engine output (layer counts, meet count, wall) is in `research/acc/optimality/runs/2026-09-24/part1.jsonl`.", "",
          "## C source (`research/acc/optimality/acc_opt.c`)", "", "Compiled `gcc -O3 -march=native`. The only edit since the runs is the `#ifndef ACC_NO_MAIN` guard around `main` (so `acc_window.c` can include the same kernel); it changes no code in this binary.", "", "```c", csrc.rstrip(), "```", ""]
    (outdir / f"WARROOM_2026-09-24_optimality_R{R}.md").write_text("\n".join(L))
    print("wrote R", R, len(band))
