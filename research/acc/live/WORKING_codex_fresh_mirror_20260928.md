# Codex fresh AC mirror probe — claimed 2026-09-28 21:20 UTC

Exclusive IDs: ac-00786 ac-03826 ac-00288 ac-06249 ac-09240 ac-03634 ac-05372 ac-05460.

These eight rows were checked against the current WORKING claims, Session 2's top-300 ranked targets and p2v list, Session 1's family slice, the Codex 80-row mirror assignment, Luna/Bob/Astra/Fable lists, and the active sweep lists. None overlap. Source: `targets_codex_fresh_mirror_20260928T2120Z.json`.

Method: mirrored-generator-and-relator AC twin, two-eyes beam BEAM_H=1 DIV=.8 P2=2 QUOTA=16 ELITE=5000 DUAL=.75, W=20000, depth ceiling equal to each AC record, pinned official verifier on any apparent tie or beat. Output `sweeps/codex_fresh_mirror_20260928.jsonl`; accepted lines go immediately to inbox. Only Session 2 submits.

This probe uses mirror orientation to test rows outside the sender's current mirror and near-escalation lanes. I will release rows when the probe finishes.

## First pass — 2026-09-28 21:37 UTC

8/8 mirror P2=2 rows complete: AC paths 47/41 (ac-00786), 49/42 (ac-03826), 46/42 (ac-03634), 47/42 (ac-05372); the other four bounded nopath. All four paths independently pass the pinned official verifier; zero tie or beat. Raw output in `sweeps/codex_fresh_mirror_20260928.jsonl`. A low-memory radius-3+4 exact window pass over the four paths found no improvement in windows at most eight moves; this is not global optimality. The full radius-6+7 pass on ac-00786 was interrupted for shared-memory pressure and is not a negative result.

Follow-up in progress: P2=3 commutator-length eye on ac-00786, then ac-03826 if useful. Same mirror transform and W=20,000. These are still within the exclusive eight-row claim; only Session 2 submits.

## Follow-on — 2026-09-28 21:50 UTC

P2=3 commutator-ranked eye on both k=1 rows gave bounded nopath (135s and 113s). P2=1 (P2, P1m, H) on ac-00786 gave a verifier-valid 48-move path, one worse than the original 47 and seven over the record; `sweeps/codex_fresh_p21_20260928.jsonl`. Opposite ranking via BEAM_WH=1 (Whitehead-minimal cyclic score) on ac-00786 is now running, same mirror transform, width and record ceiling. No inbox hit from this lane yet.

## Closed — 2026-09-28 22:00 UTC

Balanced-key variants on ac-00786 and ac-03634 reproduced 47/41 and 46/42; no cut. The exact bridge of depth <=3 between distinct ac-00786 routes also found no saving. AC mirror probing and variants on these eight IDs are **complete and released**. I moved to a separate eight-row Stable AC yx2 lane in `WORKING_codex_stable_yx2_20260928.md`; three IDs overlap my now-closed AC lane, no other worker claim overlap.
