# Score zoo: 65 cheap state scores against record paths (2026-09-28)

Offline screen: this is discovery, not proof. Script: `research/acc/optimality/score_zoo.py` (one `nice -n 10` Python
process, 347 s). All numbers: `ledger/score_zoo_20260928.json`.

**Data.** The paths collected and replayed by `p2_hump_test.py`, checked with the official verifier core, one shortest path per row.
Board snapshot 04:28Z: **246 at-record paths** (5,946 steps, 790 climbing) and **59 hump paths** (climb ≥ 6; 1,684 steps).
The hump paths have 305 climbing steps: 125 are conjugations and 180 are multiplications.

**Metric.** At each step, every score is computed on all 14 children. We record the mid-rank of the move the record path took
(ties get the average rank). "top-3" is the rate of mid-rank ≤ 3. The 95% CIs come from a paired path bootstrap (1,000
resamples of the 59 hump paths). The survival rule is the atlas ledger's, fixed before its run: a key that keeps P2 first
survives if climbing top-3 ≥ K0 + 0.05 and all-steps top-3 ≥ K0 − 0.02, with K0 = (P2c8, P1m, raw).

## Ranked table (hump paths unless noted)

| key (lexicographic, lower first) | climbing top-3 | Δ vs K0 [95% CI] | climbing conj | climbing mult | all steps top-3 | Δ all [95% CI] | at-record all | extra Python ms/state |
|---|---|---|---|---|---|---|---|---|
| K0 = (P2, P1m, raw), ledger baseline | 0.413 | 0 | 0.032 | 0.678 | 0.593 | 0 | 0.651 | |
| (P2, P1m, H) = BEAM_P2=1 BEAM_H=1 | 0.436 | +0.02 [+0.00, +0.05] | 0.072 | 0.689 | 0.596 | +0.00 | 0.652 | |
| (P2, H) = BEAM_P2=2 BEAM_H=1 | 0.239 | −0.17 [−0.22, −0.13] | 0.000 | 0.406 | 0.471 | −0.12 | 0.510 | |
| P1m alone / P2c8 alone / raw alone | 0.292 / 0.230 / 0.000 | | 0.03 / 0 / 0 | | 0.361 / 0.248 / 0.436 | | | |
| **(P2, real2_d2, P1m, H)** | **0.643** | **+0.23 [+0.17, +0.29]** | **0.512** | 0.733 | **0.661** | **+0.07 [+0.04, +0.09]** | 0.706 | 0.66 |
| (P2, real2_d2, comm_len, P1m, raw) | 0.633 | +0.22 [+0.15, +0.29] | 0.560 | 0.683 | 0.666 | +0.07 [+0.05, +0.10] | 0.711 | 0.67 |
| (P2, real2_d1, P1m, H) | 0.630 | +0.22 [+0.16, +0.27] | 0.480 | 0.733 | 0.648 | +0.06 [+0.03, +0.08] | 0.696 | 0.75 |
| (P2, L2, comm_len, P1m, raw) | 0.630 | +0.22 [+0.14, +0.29] | 0.592 | 0.656 | 0.675 | +0.08 [+0.06, +0.12] | 0.725 | 0.35 |
| **(P2, comm_len, P1m, H)** | **0.616** | **+0.20 [+0.14, +0.27]** | 0.512 | 0.689 | 0.652 | +0.06 [+0.03, +0.09] | 0.691 | **0.008** |
| (P2, real1_d2, P1m, raw) | 0.616 | +0.20 [+0.14, +0.26] | 0.472 | 0.717 | 0.629 | +0.04 [+0.01, +0.06] | 0.682 | 0.58 |
| (P2, real2_d0, P1m, raw) | 0.570 | +0.16 [+0.11, +0.21] | 0.352 | 0.722 | 0.621 | +0.03 [+0.01, +0.05] | 0.675 | 0.46 |
| (P2, L2, P1m, raw) | 0.561 | +0.15 [+0.09, +0.21] | 0.456 | 0.633 | 0.658 | +0.07 [+0.04, +0.09] | 0.711 | 0.34 |
| (P2, L1, P1m, raw) | 0.531 | +0.12 [+0.08, +0.15] | 0.312 | 0.683 | 0.661 | +0.07 [+0.05, +0.09] | 0.699 | 0.02 |
| (P2, −branch, P1m, raw) | 0.521 | +0.11 [+0.05, +0.17] | 0.304 | 0.672 | 0.595 | +0.00 | 0.634 | 0.02 |
| (P2, L3, P1m, raw), hump paths only | 0.511 | +0.10 [+0.05, +0.14] | 0.312 | 0.650 | 0.682 | +0.09 [+0.07, +0.11] | | 3.8 |
| (L2, P2, P1m, raw) | 0.502 | +0.09 [+0.02, +0.16] | 0.496 | 0.506 | 0.653 | +0.06 | 0.720 | 0.34 |
| control: (P2, −raw, P1m, raw), a "climb lover" (fails) | 0.597 | +0.18 | 0.688 | 0.533 | 0.312 | −0.28 | 0.303 | |
| best primary: −xy_imb, post-hoc flip (fails) | 0.534 | +0.12 | 0.568 | 0.511 | 0.241 | −0.35 | 0.223 | |

**Definitions of the winners** (all word-level; they see the stored words, not only the class):
- `real2_dk` = the fewest non-multiplication moves (inversions 0–1, conjugations 6–13), up to k, after which one literal
  multiplication (2–5) lands in a level-1 class that P2 promises. The promised classes are those among the P2 cut-8 list whose
  P1 equals P2. The score is k+1 if no such route exists within k moves. `real1` targets the best single product instead.
- `comm_len` = cyclically reduced length of r0·r1·r0⁻¹·r1⁻¹ on the stored words. It measures the literal junction cancellation
  across all four products.
- `L1/L2/L3` = true k-move lookahead: the minimum total length over all 14^k continuations.

## Reading

1. **P2's blind spot is the conjugation step.** On climbing conjugation steps, K0 puts the record move in the top 3 only
   3% of the time, and the beam's current P2=1 key only 7% (P2 ties all 10 conjugation and inversion children). `real2`,
   `comm_len` and `L2` lift this to 46–59%. They also gain on climbing multiplications (0.68 → up to 0.73) and on all steps (+0.06–0.08).
2. **No primary key replaces P2-first.** Eighteen primary keys beat P1m's 0.292 on climbing steps. Seven do so with a CI
   clear of zero: a priori fourier_low 0.370, −branch 0.367 and entropy 0.364, and the post-hoc flips −xy_imb 0.534,
   −abel_mass 0.479, −offdiag 0.384 and −abel_euclid 0.374. All of them fall to ≤ 0.24 on all steps (P1m 0.361, K0 0.593), the same failure as the "climb lover"
   control. The one balanced primary is L2 (0.331 climbing, 0.527 all, 0.512 on climbing conjugations): it beats P1m and P2c8
   alone on both measures but loses to K0. P2 must stay first.
3. **None of the 38 class-level scores helps as a tie-break.** This covers WH, P2wh, P2mir, P3, overlap, syllables, the exponent
   matrix, Fourier, primitive-likeness, finite-shadow classes and symmetry. They can only reorder the 4 multiplications. The best, −offdiag (a post-hoc flip), reaches 0.449 on
   climbing but only 0.542 on all steps; P2wh reaches 0.430/0.607. None survives. As potentials, P3c8 (within-hump-path Spearman with moves left 0.95), P2wh (0.93) and P2c8 (0.92)
   are the smoothest, and `n_prim` is −0.87. P3 costs 3 ms/state in Python.

## Recommended beam change

Put a word-level tie-break **between P2 and P1m** (BEAM_P2=1 layout: P2 | new | P1m | klen):
- **Now, O(L):** `comm_len` (10 bits). Offline gain +0.20 climbing and +0.06 all steps.
- **Next:** `real2_d1` or `real2_d2` (2 bits). Keep the class hashes of P2's level-1 minimisers from `p2_eval`
  (conjugation children inherit them). Per child, hash the 4 literal products (d0), the 44 products after one
  non-multiplication move (d1), or the 444 after two (d2), and test membership. Then break ties with `comm_len`.
- The (P2, H) key of BEAM_P2=2 scores worst offline (0.239). The live A/B found P2=2 ≥ P2=1, so the offline ranking is only
  a proxy. The new key still needs a matched beam A/B on the hump rows before adoption.

## Lead's extra questions

- **L2/L3** as primary keys: 0.331 and 0.223 on climbing, so they fail. As P2 tie-breaks they are good (table), but
  `real2` and `comm_len` are better on climbing conjugation steps than L3.
- **Symmetric "cage" states** (r1 ~ σ(r0)^±1 for one of the 8 signed letter permutations). Record paths do not avoid them;
  they enter them *more* often than their siblings do. Cage states are 286 of 6,192 path states and all sit in the endgame:
  with more than 6 moves left, only 1 step of 4,470 has a cage child. Where one exists, the record child is a cage state
  94% of the time against 10% of its siblings. Wider symmetry (stabiliser > 1 far from the finish) goes the same way: 0.71
  record vs 0.51 siblings. Ranking symmetric states lower does not help: (P2, stab, P1m, raw) scores 0.410/0.581, and selfsym
  0.413/0.522, which hurts. No relator is ever conjugate to its own inverse (a free-group fact; `self_inv` ≡ 0).
- **P2 climb** max_t P2(s_t) − P2(s_0) on the 59 hump paths, with P2c8 (P2c40 in brackets): 0 on 39 (42), 1 on 10 (8), 2 on 5 (4),
  3 on 1, 4 on 2, 5 on 1, 11 on 1. A capped search with P2 ≤ P2(start) + c contains the record path for **66% (71%) at c = 0,
  83% at c = 1, 92% at c = 2, 97% at c = 4 and 98% at c = 5**. The outliers are ac-00282 (c = 11, record 59), ac-00061
  (5), and ac-00478 and ac-02315 (4). Over all 246 at-record paths: 83% at c = 0, 95% at c = 1, 97% at c = 2.

Caveats: this is ranking on known paths, not beam outcomes. 536 configurations were screened, and post-hoc sign flips
are flagged in the JSON. The CIs of the top six keys clear K0 by ≥ 0.14 on climbing steps. Some record paths came from beams keyed on length, H or P1m,
which would bias the screen toward the baselines, not the new scores.
