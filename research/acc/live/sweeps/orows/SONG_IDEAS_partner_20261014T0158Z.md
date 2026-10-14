# Song ideas, partner (sealed 2026-10-14 01:58Z, before any run)

Song: "Same pulse underneath / How often it returns ..." (song round from UPG-H, 01:53Z).
Targets: few-team rows (k <= 2, gap 1-2): sac-09501 31, sac-07337 42, sac-09758 39, sac-06045 38, sac-01784 49, sac-05598 40, sac-02288 38, sac-08889 37, sac-09980 38.
Checked as not tried: FINDINGS.md, MOVES_MANUAL Part 4, METHODS_PLAYBOOK, catalog/closed_*.jsonl. Exponent sums appear only as the
P5 lower bound (capped matrix BFS) and as the BEAM_NOV shape bucket. No beam ranks by them, and no beam layers by real move cost
over multiplication-only states.

## Idea 1: FOLD, a rotation-folded multiplication beam
Line: "Sample too slow and the high folds onto the low" (with "Hidden motions stacked in me I had no word for").
- Idea: rotations (the cancelling conjugations, the fast "high" motion) take a beam slot each in our beams, so the beam spends its width on
  rotation intermediates. Fold them: one step = rotate r0 by a and r1 by b (paid, |a|+|b| real conjugation moves) and then one multiplication
  (or one inversion). Only the post-multiplication states compete, in layers by REAL move cost (bucket queue), ranked by total length.
  This matches UPG-H's finding that the leader's roads are almost all multiplications.
- Test: Python (exact free reduction; the final line is replayed on the official core/stable_core). Width 1,500-3,000, |a|,|b| <= 4,
  finish by exact BFS when total length <= 8, to (x,y) for AC and to (y,x) for Stable + [15,15]. Run on sac-09501, then on 09758, 07337 and 06045.
  Success = any line <= the record (or shorter than our best).

## Idea 2: BEAT, an abelian-shadow heuristic aimed at (y,x)
Lines: "Two pitches meet. The slow gap walks into the ear / That's how you read the high when the high won't sit near /
Bring it down. Count the throb. The unknown becomes a stair".
- Idea: the exponent-sum matrix E(state) is the slow beat note under the fast word dynamics. Multiplications and inversions are row operations,
  and conjugations leave it fixed. Its exact row-op distance to I (ending (x,y)) or to J = [[0,1],[1,0]] (ending (y,x)) is a countable stair.
  Add it to the beam key (key += w * 16 * dist_E), so that the beam prefers states whose abelian shadow is on schedule, aimed at J for Stable lines.
- Test: (a) count the throb: dist(E0, I) vs dist(E0, J) for each target row, and the number of multiplications in our roads vs that lower bound;
  (b) a copy of acc_beam.c with env BEAM_AB=w and BEAM_ABT=I|J (exact matrix-distance table by BFS, entries |e| <= 24),
  W 100000, dual-P2 settings, w in {1, 3}, on the swapped start (Stable via (y,x)) and the direct start, for 09501, 09758, 07337, 06045, 01784.

## Idea 3 (if time): STAIR, the abelian skeleton as an exact filter
Line: "Integer times a radio step, plus offset, plus the air" / "The unknown becomes a stair".
- Idea: an exact capped BFS (acc_capped) that keeps only states whose matrix distance to J is <= (remaining budget minus the minimum number of
  multiplications). This is admissible, so it is still exact, and it may prune enough to raise the cap on sac-09501.
- Test: the measured fraction of states pruned at cap 26. Run only if Idea 2a shows a tight bound.

## Results log (written during the hour; ideas above were sealed at 01:58Z, before any run)
- 02:05Z idea 2a (count the throb), exact matrix BFS |e| <= 24, distance of E0 to I / to J vs the conj-free moves (mults + inversions) in our best road:
  09501 4/4 vs 14; 09758 7/7 vs 17; 07337 8/8 vs 18; 06045 4/4 vs 18; 01784 4/**2** vs 24 ((y,x) road 22); 07385 9/9; 04493 4/4; 05598 6/8;
  02288 6/6; 08889 5/5; 09980 5/5; 08995 6/6; 03714 **2**/4; 00580 4/4; 04628 4/4. The abelian bound is far below the real multiplication count
  (roads use 2-5x more), so it is loose. Where I != J it points the way: 01784 prefers (y,x), and our (y,x) road is 2 shorter than our (x,y) road;
  03714 and 05598 prefer (x,y). By the sealed rule, idea 3 (exact abelian pruning) is NOT run, because the bound is too loose to prune.
- 02:09Z built acc_beam_ab (repo acc_beam.c + abelian term). With the term off, its output is byte-identical to a plain repo build (checked on 09501, W 3000).
- 02:14Z-02:28Z idea 1 FOLD vs an equal-width plain control (same Python length ranking, same exact finish balls radius 6), sac-09501 (target <= 34):
  FOLD W1500 R3: none within cost 34 (92 s). FOLD W3000 R4: none (about 300 s, 4.9M nodes). Plain W1500 / W3000 / W10000: none.
  Neither finds even a 34 here, where the C dual-P2 beam finds 31 at W 3000. Verdict: the length ranking is the bottleneck, not the slots spent on
  rotations. At these widths FOLD is no better than plain. It is not worth porting to C unless it is paired with the P2 key.
- 02:13Z-02:45Z idea 2b BEAT A/B (repo dual-P2 engine; control = term off; AB1 = +1 length unit per abelian step in the plain key; ABP2 = +2 per step in the P2 field; depth = SAC record):
  W 10000 (AC / Stable vs records):
  | row | ctrl | AB1 | ABP2 |
  |---|---|---|---|
  | 09501 (30/31), target J | 30/32 | 31/32 | 36/38 |
  | 09758 (38/39), J | none | none | none |
  | 07337 (41/42), J | none | none | none |
  | 06045 (36/38), J | 40/42 | 42/44 | none |
  | 01784 (48/49), J | 57/59 | none | none |
  | 05598 (38/40), I | none | none | none |
  | 02288 (37/38), J | 38/40 | 38/40 | 39/41 |
  W 50000: 06045 ctrl 38/39, AB1 38/39. W 100000: 09501 ctrl 30/32, AB1 30/32 (the same line).
  Verdict: the abelian term never helps. AB1 at best equals the control and ABP2 is always worse. MISS; the idea is dead in this form.
  Side result: the control (the real dual-P2 engine) reaches AC 30 = record (k17, already held) on 09501 at W 10000, and 06045 Stable 39 / AC 38 at W 50000.
  Those are the first true dual-P2 runs on these rows, since the old cached binary ignored BEAM_P2.
  08889 (36/37), J, W 10000: ctrl 38/40, AB1 38/40, ABP2 43/45.
- 02:44Z stopped the W 50k and W 100k A/B processes: the idea is dead. Idea 3 was not run (sealed rule: bound too loose).
