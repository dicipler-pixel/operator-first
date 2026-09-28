## 2026-09-28 06:35Z, session 2 (lead): rank-3 super-relator build for MS(n, BS) (claimed, helper working)
- Building on Codex's generator (3a−1 per level because BS is re-conjugated between single crossings):
  the super-relator **S_a = X^a Y x^(2a) y** crosses y over the whole block x^a in ONE multiplication
  (r1 = P y x^a → r1·S_a = P x^(2a) y), and it doubles exactly: **S_(2a) = (X^a S_a x^a)·S_a** (free-reduces to
  X^(2a) Y x^(4a) y). S_1 = XYxxy = r0^-1. Rank 2 has no room for the second copy; Stable AC's stabilized slot
  does, if the helper generator g can be kept at a harmless end. Cost per level ≈ a (the X^a conjugation) + O(1),
  so the whole build ≈ 2^(n-1) + O(n), then the fast peel. That would beat every doubling-chain Stable AC record
  by a wide margin. **Claimed by session 2's helper** (`tools/acc/sac_ms_bs.py`); others please don't duplicate.

## 2026-09-28, Codex ABC: complete constructive generator for MS(n, YXXyx)
- `research/acc/optimality/yxxyx_chain.py` builds an ordinary AC certificate for every n>=2 and checks it with pinned official `core.verify`. At level j (a=2^j, k=n+1-j), `(YXXyx, Y^k X y^(k-1) x^a)` becomes `(YXXyx, Y^(k-1) X y^(k-2) x^(2a))` by `10^(a-1), 5, (11,5)^(a-1), 12`. This is an exact primitive-move identity, checked at every level n=2..10. The remaining `Yx^(2^n-1)` finishes via `6 2 10 10 5, 3^(2^n-3), 5 11 2`.
- Length is `4*2^n+2-n`. Scored n=5..10 all **pass the official verifier** and limits: 125, 252, 507, 1018, 2041, 4088 moves; peaks 63..2047, max work 1,961,556 (<5M). Snapshot records 80,145,275,532,1046,2071; thus **no submission line**. Metadata, hashes and exact command in `ledger/codex_yxxyx_generator_20260928.json`. The script emits the full move arrays for every n.
- Bottleneck is now explicit: rotating `a-1` trailing x's into place plus `(11,5)^(a-1)` costs 3a-1 per level. To tie the leaders, replace the rotation/crossing schedule with a block closer to a moves per level, or avoid a full final expansion. H-beam n=5 from the forced 18-move prefix found no finish at W=80,000/depth 70; bounded miss only.

## 2026-09-28, Codex ABC: YXXyx chain trace (official replay)
- `ledger/codex_yxxyx_trace.py` and `ledger/codex_yxxyx_trace_20260928.json` verify two uniform prefixes for synthetic MS(n, YXXyx), n=3..10: nine moves `5 1 12 4 1 10 5 12 10` give `(BS, x^3 Y^(n-1) X y^(n-2) x)`; an alternate 18 moves give `(BS, x^7 Y^(n-2) X y^(n-3) x)`. In both formulas the product is freely reduced; BS=`YXXyx`.
- An H-beam found an **officially verified 29-move n=3 path** (peak total length 19); the lead's 30-move path stays within cap 16, so this is an unrestricted shortening, not a cap-16 contradiction. Another found a **verified 55-move n=4 path** (peak 31). Both are synthetic/training instances, not submission lines. The n=4 certificate shows last build `5 [11,5]^7 12` (16 moves) from `x^7 YYXyx` to `Yx^15`, then 21 moves to `(x,y)`. The last build is the factor-of-two bottleneck; the same finish cannot be pasted into n=5 because the extra Y/y layer remains.
- n=5 H-beam from the original start found no path with T8 at W=20,000/depth 100 or W=80,000/depth 105 (the latter used DIV=.75, BAL=.2). These are beam misses, not bounds. A forced 18-move-prefix continuation is being tested separately.

## 2026-09-28 06:05Z, session 2 (lead): STABLE AC FAST PEEL — a beat lane on every doubling-chain row
- **Every doubling-chain Stable AC record is exactly the AC record + 2** (68 rows, n = 4..10, 10 chains). Nobody
  uses rank ≥ 3 on them (the team lead's point: most teams treat Stable AC as AC + 2). A shorter SAC road is a
  **beat = 1 point whatever k is.**
- **Fast peel** (`tools/acc/sac_fast_peel.py`, official `stable_core`, self-tested to the empty presentation):
  from (x, y X^m): stabilize g, make r2 = g X^k (k moves), swap each X^k block of r1 for one G (2 moves:
  r1 ← r1·r2^-1, conjugate r1 by G), peel the rest, reduce r2 to g, peel the G's, destabilize all.
  Cost ≈ 2k + 3m/k: m=63 → 44 (plain 65), 127 → 61 (129), 255 → 84 (257), 511 → 117 (513), **1023 → 164 (1025)**.
- **Build budget for a beat** (reach (x, y X^(2^n−1)) within this many moves, then append the fast peel):
  n=6 102–133 (slack 21 over the leaders' estimated build), n=7 215–247 (68), n=8 449–487 (173),
  n=9 930–968 (396), **n=10 1908–1952 (861)**. Per row: `ledger/sac_fastpeel_targets_20260928.json`.
  So our build may be ~1.85·2^n at n=10 and still beat. The naive build (2 moves/crossing, ~2^(n+1)+17) just
  misses; session 1's level construction (~1.5–2·2^n) should clear n = 8..10 on all 10 chains (~30 rows).
- **Ask, session 1:** make `ms_construct.py` stop at the state (x, y X^m) (or any r0 = x, r1 = y·X^m spelling) and
  write the prefix; I append the tail, verify the full `sac-` line with the official verifier, and send.
- Further gains: a second block level for the G's, and doing the build's x-mass in rank 3 as well.

## 2026-09-28 05:50Z, session 2 (lead): MS(n, YXXyx) — the level move is uniform in n; skip test
- The exact 9-move level path MS_3 → (BS, x^3 YYXyx) is `5 1 12 4 1 10 5 12 10`. **The same 9 moves on MS_4 give
  (BS, x^3 YYYXyyx)**: the level step does not depend on n. It alternates inversion (move 1) with
  multiplications, so one relator is worked from both ends without paying a conjugation per crossing. Move 4
  is the BS substitution y → x^-2 y x on the trailing y. Hypothesis: the leaders' ~1 move per x comes from this
  invert-and-multiply rhythm, applied at every level including the last (where our doubling pays 2 per x).
- **Skip test** (can we finish from (BS, x^a YYXyx) without doubling to YY x^(2a+1) y?): exact, a=1 (cap 13,
  complete): 12 moves, and the optimum *does* double first (5 11 5 12 → Yxxx, then an 8-move finish). a=3 running.
- Exact n=3 of MS(n, YXXyx) under cap 16: 30 moves (`5 1 12 4 1 10 5 12 7 5 6 5 11 5 11 5 1 6 12 3 10 4 2 2 2 2 2 4 1 2`),
  = the leaders' formula 2^(n+1)+n+11. Its finish gets r1 = X (x = 1) and peels r0 = xYx^5 with move 2.
- Exact n=2: 15 (`5 7 12 5 6 5 12 11 2 5 12 5 8 2 4`), finish steps down y=x^3 → y=x^2 → y=x (descent, not a peel).

## 2026-09-28, Codex ABC: borrowed-road joins through radius 7 remained behind
- Expanded the state-keyed suffix atlas of 478 officially valid AC roads (13,092 suffix states) with fresh prefixes. At radius 6/cap 35: ac-00766 visited 388,785 states, ac-00974 visited 581,530; best 34 and 26. At radius 7/cap 40: 3,035,716 and 4,578,426; best still 34 versus record 33 and 26 versus record 24. This tests joins into this particular atlas, not arbitrary new finish roads or global optimality. Code `ledger/codex_abc_crossjoin.py`; four raw JSON results `ledger/codex_abc_crossjoin_r{6,7}_{00766,00974}_20260928.json`. Do not spend more on the same small-radius atlas without new suffix roads.

## 2026-09-28, Codex ABC: T8/fixed visited passes a real stopped row, but no score
- On ac-00580 at total-length cap 28, the earlier T9 ledger stopped after depth 23 at 48,220,955 states. The T8/fixed-visited engine reproduced **exactly** that depth-23 count and continued into depth 24, stopping at a 60M-state budget after 95.61 seconds. No AC/SAC meet. This is a repeatable memory/scope improvement, not a complete search or proof. Full command, raw logs, and explicit incomplete status: `ledger/codex_abc_capped_trial.py`, `ledger/codex_abc_capped_trial_00580_20260928.*`.
- On Bob's ac-00766 near miss, cap 28 already had 426,246 states at depth 7; the next layer paged under shared 8 GB pressure. The run was interrupted and marked incomplete. A radius-8 goal ball plus a 25-step prefix could tie record 33, but this broad BFS is unlikely to reach such depth within our budget. Shift to route-specific joins or a different road, not a higher broad cap. `ledger/codex_abc_capped_trial_00766_20260928.*`.

## 2026-09-28 05:45Z, session 2 (lead): Miller–Schupp families — scale, the clean BS case, and the crux
- **650 rows in the MS families are held by 1–2 teams** (by n: n=5 115, n=6 105, n=8 77, n=7 71, n=4 67, n=1 65,
  n=3 56, n=9 52, n=10 36). Source: `ledger/ms_families_by_w_20260928.json`.
- **Cleanest case: first relator already BS.** 80 rows have r0 = YXXyx (y^-1 x^-2 y x, i.e. y x y^-1 = x^2);
  about 40 are held by one team. For w = YXXyx, r1 = Y^(n+1) X y^n x: BS gives y^n x = x^(2^n) y^n, so r1 is
  equivalent to **y = x^(2^n − 1)**. Path = push x left through y^n (2^n − 1 crossings "y x → x x y", each one
  multiplication by r0^-1 = XYxxy at the END of r1) → setup → peel 2^n − 2 (one x per move with r0 ≡ x).
  Records n=5..10: 80, 145, 275, 532, 1046, 2071 = 2^(n+1) + n + ~11, all k=1.
- **The crux:** a crossing only acts at the end of r1, and after one the word ends "…x x y", so the next x
  must be rotated in (1 conjugation): 2 moves per crossing → ~3·2^n total. The records need ~1 move per
  crossing. Whoever finds how to chain crossings without a rotation unlocks the whole family set.
- Running: exact capped search on the n=2 BS case (y = x^3) to see the optimal crossing pattern; H-beam
  from the n=4 BS stage of w = YXyXyx (record 56).
- Also worth a look: w = YYXYYxyyX has slowly growing records 42, 43, 76, 81, 134, 159 (n=5..10, all k=1):
  a different, non-doubling mechanism, and short enough for our beam.

## 2026-09-28 05:30Z, session 2 (lead): P2 SURVIVES; Miller–Schupp doubling chain, first phase is general
**P2 test** (`optimality/p2_hump_test.py`, `ledger/p2_hump_test_20260928.json`): 609 verified paths on 526 rows,
240 at the live record, 56 of them hump paths.
| score | median climb | climbing moves in top 3 |
|---|---|---|
| raw length | 9 | 0.00 |
| P1 | 2 | 0.22 |
| P1m (rotate the multiplier only) | 1.5 | 0.41 |
| P2 (cut 8) | 0 | 0.22 |
| P2 cut 8, then P1m, then raw | 0 | 0.41 |
- Kill conditions not met: P2 survives. Its ranking gain is on multiplication moves only (conjugations leave it
  unchanged). P2 predicts moves remaining better than length (leave-one-out error 3.18 vs 4.52).
- C cost: P2 cut 8 is 15–97 µs per state; only the 4 multiplication children need it. About 1–5 min per row at
  W=20,000, depth 40. **Next: `BEAM_P2` in `acc_beam.c` (P2 cut 8 → P1m → raw) and a matched A/B on hump rows.**
- Add-ons: E1 weak survive (min relator length rises on 96% of humps, but (min,max,P2) predicts best: 2.18);
  U1 dead (median same-relator run 2); C1 survives (humps: fewer hyperbolic, more finite-order transfers, p=0.005).

**Miller–Schupp doubling chain (building on session 1's find), w = YXyXyx, r1 = Y^(n+1) X y^n x:**
- Our n=3 path (ac-09243, 36; record 32) has 4 phases: reduce (18) → build r0 = Y x^7 (6) → set up r1 = X^6 y (5)
  → peel one x per move (6) + 1.
- **The reduce phase's first part is general:** moves `3,8,2,6,12,4` then `12` × n turn every n into
  r0 = y X Y^(n-1) x Y X y^n, r1 = XyxYX (the Baumslag–Solitar relator y x y^-1 = x^2). Checked n = 3..6.
- In the group, the target is r0 = Y x^(2^n − 1) (n=4: Y x^15), then the peel.
- **The crux is the build:** our build costs ~2 moves per new x (1 multiplication + 1 conjugation to rotate).
  The records (2^(n+1) + 16..40) imply ~1 move per x in build and peel. 2 per x gives ~3·2^n (n=10: ~3,100 vs 2,088).
- Running: H-beam from the n=4 BS-stage state (10 moves in), W=50k, depth 46 (record 56).

## 2026-09-28, Codex ABC: smaller goal ball for constrained memory
- Built T8 with `work/acc_opt tball 8 40000000 work/T8.tab work/abc_t8`: 24,587,144 goal states, 640,000,000 bytes, SHA-256 `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`. T9 has 214,977,551 states and 4,480,000,000 bytes. The smaller map removes 3.84 GB of table footprint while requiring up to one additional forward move for the same meet length.
- On a known ac-00236 15-move path at cap 25, the disk-backed capped engine found an officially accepted AC 15 and SAC 17 with both tables. T9 first saw AC 15 at forward depth 6 (2,561 cumulative states); T8 first saw it at depth 7 (7,615 cumulative). Same depth-7 final state count in the benchmark; wall times are confounded by file cache, so no speed claim. Code and raw results: `ledger/codex_abc_ball_split.py` and `ledger/codex_abc_ball_split_20260928.json`.
- Adam's first 100 unsolved rows, width 2,000/depth 80, yielded no AC or SAC path under either `BEAM_H=1` or `BEAM_H=1 BEAM_BAL=1` with T8; 200 complete bounded rows total. The T9 H pass reached 88 no-path rows and six 45-second timeouts before contention made the remaining six impractical. No inbox line. Stop these 100 rows per the handoff rule. The next useful test is T8 on a specific memory-limited capped row at a fixed budget, measuring whether the extra forward frontier is cheaper than keeping T9 resident.

## 2026-09-28, Codex helper: reserved high-slack Stable AC beat beam screen (no hits)

- Screened the six rows removed from the main sacbeat list: ac-00520, ac-00718, ac-01566, ac-00074, ac-03887, ac-03104. Target AC ceilings were SAC live record minus 3, so AC + [16,15] would strictly beat the Stable AC record.
- Baseline: pinned T9 finish table, `BEAM_H=1 BEAM_DIV=1.0 BEAM_BAL=0`, width 20,000, depth through each target ceiling + 2. All six returned `nopath`.
- Different second pass on the three loosest rows (ac-03104, ac-03887, ac-00074): `BEAM_H=1 BEAM_DIV=0.6 BEAM_BAL=0.75 BEAM_NOV=1 BEAM_NOISE=1 BEAM_SEED=20260928`, width 20,000, same depth policy. All three returned `nopath`.
- These are bounded beam misses, not proofs. No candidate path or verifier receipt was produced. Exact timings and thresholds: `research/acc/live/ledger/luna_sacbeat_screen_20260928.json`. Official SAIR commit: `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`; T9 SHA-256 matches the expected build.
- Follow-on: resume only after refreshing exclusions and worklists; do not interpret this screen as an exhaustive search.

## 2026-09-28, Codex ABC ledger correction
- `ledger/exact_capped_runs.jsonl` has 76 entries, 52 marked incomplete. Their median state count is 48,936,404.5; only one incomplete entry is at least 180M, with max 211,651,126. They stopped at different row budgets or limits. The shorthand “52 stopped at ~210M” is misleading; prioritize by actual budget, cap, and depth before rerunning with the disk-backed pilot.

## 2026-09-28, Codex ABC follow-up: rhythm transfer failed and BAL flag dependency
- On 478 real borrowed routes (237 ties, 241 trailing), the training nonundo transition score has tie-vs-trailing AUC 0.588. Shuffling tie/trail labels within 5-move record bins gives mean 0.577 and p = 0.567. No evidence this score ranks better roads in the current atlas; do not inject it into the beam without a stronger transfer test. Reproduce with `ledger/codex_abc_rhythm_transfer.py` and `ledger/codex_abc_rhythm_transfer_20260928.json`.
- Code inspection: `BEAM_BAL` contributes only inside `hprio`, which `acc_beam.c` calls only when `BEAM_H=1`. A standalone `BEAM_BAL=1` is identical to the vanilla length beam. The second unsolved sweep must set both `BEAM_H=1 BEAM_BAL=1`. A bounded width-2,000/depth-80 screen is in progress after width-20,000 runs paged under concurrent load. `run_beam_abc.py` records that width explicitly and skips expensive window work for a first unsolved hit.

## 2026-09-28, Codex ABC: short alternate joins, move rhythm, and visited-table memory
- **Bob join idea:** Replay all 478 officially valid borrowed AC paths to form a 13,092-state suffix atlas. Search exact distinct states to radius 5 from ac-00766 and ac-00974 (total relator length cap 60), then join any atlas suffix. Reached 124,740 and 130,399 states; best verified routes remain 34 (record 33) and 26 (record 24). Prior window-14 checks were already negative. Scope is radius 5 plus this atlas, not a global bound. Code/data: `ledger/codex_abc_crossjoin.py`, `ledger/codex_abc_crossjoin_20260928.json`.
- **Bob rhythm idea:** The 424 official training routes (all Miller–Schupp) have held-out one-step move prediction gain 0.482 bits/move versus within-route shuffle mean -0.0056 (1,000 shuffles, p < 0.002). Conditioning out immediate inverse moves leaves 0.401 versus -0.0052 bits/move. This is a real sequence pattern in training, but transfer to other challenge families is untested. Code/results in `ledger/codex_abc_rhythm.py` and `ledger/codex_abc_rhythm_20260928.json`.
- **Charlie memory idea:** Built `research/acc/optimality/acc_capped_disk.c`, an optional file-backed, fixed-size visited table sized from the state budget, preserving the existing 123-bit fingerprint convention. The cap-24 radius-7 pilot on ac-00974 matched original at 299,177 states. Wall time was unstable (disk repeat 73 s versus original 7 s under shared 8 GB pressure), so no large-row improvement claimed. Also piloted rank <=3 radius 5+5 on ac-00520/ac-00718: no meet; the latter had two word-cap overflows and no valid negative bound. Details in `ledger/codex_abc_disk_benchmark*.json` and `ledger/codex_abc_rank3_probe_20260928.json`.

## 2026-09-28 05:00Z, session 2 (lead): the team lead's older ACC repos (mad-hatters-acc-private, acwindow-lean)
- **47 unsolved AC rows are in the AK(3) class** (open problem). List and provenance:
  `research/acc/live/AK3_CLASS_ROWS.json`. Found by matching every start against acwindow-lean's exhaustive
  AK(3)-class walk (≤ 26 letters, 1.28M members); rechecked independently by the lead. **Skip them.**
  Next: extend the class walk past 26 letters to catch longer AK(3)-class rows (1,794 unsolved rows start ≤ 26).
- No old path ties or beats a live record (only ac-00276 at 52/104; record 39, we already tie it).
- **Primitive-relator finish** (acwindow-lean `evidence/genus/primitive.py`, Lemma A in `notes/ACWindow_note.md`): a state
  where one relator is primitive can always be finished, and the proof builds the path, so it is a much
  larger finish target than T9. Screen: 0 of 2,672 unsolved rows reach one within 2 moves or one multiplication
  at any rotation, so no shortcut now. It could still be a cheap stop test inside the beam. O(L) pre-filter: a
  primitive cyclic word has a letter that appears with only one sign. Path builder not written.
- Cyclic-class walk (`evidence/genus/house_walk_resumable.py`): groups rows into AC classes (solve one, get all). Not a valid
  relaxation for pruning the capped search. Its 5-minute pickle checkpoints are worth copying.
- Failed before, don't revive: genus/thickenability test (primitive appears at depth 2, genus 0 only at 6);
  cap-lift identity loops (Codex; no gain on 00037, 00313).
- acwindow-lean's Lean proofs: AK(n) → AK(−n−1) fold; a 9-move path for AK(3)'s image in C5*C5; `ACCWell`
  (the formal shape of our capped proofs, but it needs a move-count version). No new pruning rule.
- Prior art list worth reading: mad-hatters-acc-private `ACC_PRIOR_ART_CORRIDOR_HANDOFF_2026-09-13.md` (Carreras 2607.23611,
  Two-Hump, Myasnikov–Myasnikov–Shpilrain).

## 2026-09-28 04:55Z, session 2 (lead): ideas from the team lead's older Lean repos
Read: coxeter-rank2-lean, elemental-peeling-lean, upg-lean, relational-atlas-lean (no data in any; Lean + build checkers).
Being tested now on all known hump paths, together with P2:
- **E1, keep the two lengths separate** (elemental-peeling `resolvedLedger_le_commonFloor`,
  `no_common_record_predictor`). Does min(|r0|,|r1|) stay at or below its start while the total climbs?
  If so, reserve ~20% of the beam for the smallest min. Kill: min rises on most humps and (min,max)
  explains no more of the moves-remaining spread than L.
- **U1, one relator at a time** (upg `UPGFeedback`, `UPGBlockFeedback`: a block runs independently when its
  coupling is zero). Hold r1 fixed and search r0 with its 7 moves, then swap. Branching ~6 instead of 13, so
  exact BFS reaches ~10–11 plies in 180M states instead of ~7. Kill: median same-relator run under 3.
- **C1, exponent-sum class of humps** (coxeter-rank2 `Uaff_iterate`): T = M_end·M_start⁻¹ over each hump;
  ±I / finite / parabolic / hyperbolic. Filters Bob's macros by class. Kill: hump class mix = random segments.
- **E2, pair synergy** I(a,b) = L(abs) − L(as) − L(bs) + L(s), free inside P2. Tiebreak on flat P2 plateaus.
- Dropped: finite-quotient distances (dihedral, Heisenberg): their ceiling is ~log, same as invariant bounds.
  relational-atlas-lean: nothing usable for AC.

## 2026-09-28 04:45Z, session 2 (lead): the team lead's atlas (Drive PDF, 2026-08-27) applied to AC
Source: `research/acc/atlas_drive/THE_OPERATOR_FIRST_ATLAS_20260827.txt` (Plates I–XXI, bridges B1–B84, full text).
Quick checks on 7 known paths (exact: 03305, 01629, 05558, 07435, 08201; ours: 00145, 05064):
- **Dead first:** humps are not conjugation padding. The cyclically reduced total climbs as much as the raw
  total (03305 +16/+16, 05064 +14/+14). Ranking by cyclic length alone is out.
- **1. P2 lookahead (B31 + Plates XII, XIV).** Conjugations stay inside a conjugacy class; only
  multiplications change class. P_k = best total after k multiplications with free cyclic rotations.
  On 03305's exact path: raw climbs +16, P1 +10, **P2 climbs 0**; the two climbing moves rank 11th/10th of
  14 by raw length but tied-best by P2. Caveat: P2 is flat (ties 9–13 of 13 siblings), so use P2 first,
  length second. **Being validated on every known hump path now** (`optimality/p2_hump_test.py`).
  Kill: P2 median climb ≥ half the raw climb, or climbing moves not ranked better than by length.
- **2. Per-class beam quota (B16, B17, L4):** overflow piles into a few classes; give each class its own
  slots. Class = pair of cyclic conjugacy classes (finer than `BEAM_NOV`). Kill: the record path's class
  is still in the plain beam when the path is lost, or no gain at matched width.
- **3. Macro rate extrapolation (B69, Plate XV):** apply a macro once and twice, extrapolate, expand
  (macro, best repeat count) as one child. Pairs with Bob's library.
- **4. Whitehead-minimal frame (B83, Plate XVIII):** climbs +12 on 03305 (weaker than P2), 0 on the other
  four exact paths. It reaches a basis pair 8 moves before the end on 03305, so an exact Nielsen finish
  could reach past the 9-move table.
- **5. Where the beam loses the path (B20, Plate XI):** at each depth, the record-path state's rank and tie
  count in the beam at W and 2W. Lost among ties → add an axis (1 or 4); rank ≫ W → wrong score; saved by
  2W → only width.
- Knots, volumes, geometric tensors: invariants only, and invariant bounds are already ruled out.
- The 2026-09-12 bundle (atlas book) exists on Drive only as a 3.5 MB zip; needs a manual upload to read.

## 2026-09-28 04:20Z, session 2 (lead): Bob's macros go into the beam (test running)
- Bob's library plugs straight into `acc_beam` (`BEAM_MACROS`, `BEAM_MACW`): macros are official
  AC move indices 0–13 with length ≤ 8. File: top 40 by solution count with length ≥ 4
  (`2 5 2 8`, `4 1 2 0`, `0 2 5 2 8`, ...).
- A/B at matched width (W=20000, depth = live + 6, `BEAM_H=1 BEAM_DIV=0.8`): plain vs + Bob40, on
  the 9 near-miss rows of session 1's BAL test (ac-00145, 09189, 00147, 04276, 05702, 06045, 08995,
  09091, 00037). Kill condition: macros never shorter than plain and never find a path where plain
  finds none. Note: the macro arm evaluates (14 + 40) children per node, not 14, so it spends more
  work per kept state.
- Result goes here when done.

## 2026-09-28 — Bob — move rhythm (training_424)
Tested: repeated macros vs permutation and pair-preserving (doublet) shuffles, 1000 each, kill = no stat beats doublet at p<0.01.
Result: SURVIVES as blocks — tandem repeats 589 vs 365±17, shared 6-grams 326 vs 36±4 (p=0.001 floor); DIES as a beat — conjugation periodogram p=0.22.
Core macro: 4,·,2,5,2 (r1*=r0, r0*=r1, r1*=r0^-1, r0*=r1), across 20-43 distinct w. Library: ledger/bob_macro_library_20260928.json (977 macros).
Next (untested): top macros as acc_beam supermoves on stalled rows vs plain beam at matched budget.
Record: ledger/BOB_move_rhythm_20260928.md

## 2026-09-28 03:50Z, session 2 (lead): the team lead's Stable AC insight
- **Idea (the team lead):** many teams only do AC and never send the Stable AC line, so Stable AC is
  thinner.
- **Board check (7,443 rows solved on both):**
  - Average teams on a record: AC 3.05, Stable AC 2.85. Stable AC has fewer teams on 1,148 rows and
    more on 530.
  - **95 rows have a Stable AC record longer than AC record + 2.** All of them are held on AC by one
    team that never sent AC + [16,15].
  - On those rows, any AC path of length ≤ SAC record − 3 **beats** Stable AC (1 point), even if it is
    above the AC record. Slack above the AC record: 0 on 42 rows, 1 on 22, 2 on 10, ≥ 3 on 21 (e.g.
    ac-03179: AC 55, any AC ≤ 59 beats SAC 62; ac-04396: AC 68, ≤ 73 beats 76).
- **Running:**
  - `sacbeat`: H-beam W = 200k over the 95 rows, slack ≥ 3 first, shortest first. `tools/acc/ops/beam_list.sh`.
  - `k2ac`: AC rows held by 2 teams, record ≤ 36, AC only, with the SAC tie taken for free via + [16,15].
    7 new rows (another 15 are already in sweeps A/B); then sweep D resumes.
- For the helpers: the sacbeat list is `research/acc/live/sweeps/sacbeat_targets.json`. A route map that
  gets any AC path under `record` on one of these rows is worth a full point on Stable AC.

## 2026-09-28 03:10Z, session 2 (lead): reverse search? No, the humps sit mid-path
- **Idea** (the lead's "look in the glass"): search from the finish backwards, so the uncapped 9-move ball
  sits at the start. It would help if record paths climb near the start.
- **Checked on the 5 exact paths:** the peaks come at 30–52% of the way (03305 step 7 of 23, 01629 12/23,
  05558 12/24, 07435 12/26, 08201 11/31). A reverse search needs the same cap as the forward one.
  Closed.
- **ChatGPT's ac-06095 windows (gap 15–16, empty):** one more local repair coming back empty, which fits
  "the record paths are different roads". Suggestion for the helpers: stop local repair on near-misses
  and put helper time on unsolved rows that are close to solved ones, or on the deep 1–2-team rows with a
  fresh route (not a repair).
- **Ops:** sweep C finished its 77 rows (no new ties). Sweep B's remaining 261 rows are split: B keeps 130,
  new sweep D takes 131 (60M budget).
- **My mistake:** a cleanup `rm -rf cap_ac-0*` also deleted sweep A's live layer files (ac-01104, cap 31
  → FATAL, recorded as incomplete, so no false bound). Rule: only delete the work dir of the row whose
  sweep you stopped. Re-run ac-01104 at cap 31 later.

## 2026-09-28, ChatGPT helper: ac-06095 exact peak-window screen
- **Target:** reserved helper lane, ac-06095 47 vs record 42 (k=1); matching SAC is 49 vs 44 (k=1). No submission line found.
- **Input replay:** the candidate route reaches exact (x,y); its maximum total relator length is 31, first at state P[5]. Move set is the pinned ac-r2-v1 moves 0-13.
- **Gap 15:** checked windows [0,15] through [5,20], using radius 7 from each endpoint. Caps 31, 33, 35, 37, 40, 43, 46, 50, 60, 70, 80, 90 all had zero intersections. Cap 4096 was also empty and is effectively uncapped for these radius-7 balls: each endpoint has L<=31 and one move has L_next<=2L, so L<=3968 through depth 7. At cap 4096 the largest sides had 10,885,023 and 10,842,301 states.
- **Gap 16:** checked windows [0,16] through [5,21] with radii 7+8. All six were empty at caps 31, 40, and 50; largest B-side: 1,326,497, 8,802,044, and 18,151,396 states respectively. At cap 60, windows [0,16], [1,17], [2,18] were empty (largest side 30,320,682 states); the runtime disconnected before I captured the remaining three windows, so cap 60 is incomplete.
- **Result:** no shorter splice. The path remains 47. This is window-local, not a global optimality result. The table deduplicates 123-bit fingerprints, so record these as completed fingerprint searches rather than collision-free formal certificates.
- **Drive cross-check:** `ACC_WARROOM_ARCHAEOLOGY_LIVE_ROUTES_20260922.md` reports 73 H3(F5)-stationary, full-state-changing macros from 116 occurrences, but no shortening yield; these are recorded-state-specific and must be replayed at each use. Its higher-yield direction is to start from a certified ADVANCE port and meet the larger solved-side region T14/T16, not just (x,y). The first-pass basin atlas covers ac-02842 and root families, not ac-06095. The `ACWindow_note` is a proof-track note, not a path-shortening method.
- **Next macro experiment (not yet run):** mine short move strings from verified paths where total length rises then returns near its prior level. Treat each string as a beam supermove with cost equal to its actual move count, retain its full expansion for official replay, and keep a reserved high-height beam band so intermediate hump states do not have to survive ranking. Use the 73 recorded-state macros only as training examples; only the move strings are portable, and every application must be replayed from its new source state. A/B against the current score on exact hump controls ac-03305/ac-01629 plus a held-out row at equal node budgets. Success criterion: a verified path at or below live record, not just lower relator length.
- **Audit:** `research/acc/optimality/ac-06095_peak_window_audit_20260928.json`. Next exact action: finish cap 60 on the last three gap-16 windows after compute reconnects, then consider gap 17.
## 2026-09-28 03:15Z, session 2 (lead): Schur macros and the echo ("take it back")
- **Schur elimination as macro-moves** (atlas UPG-FEEDBACK). `mine_macros.py` mines up-and-back-down
  excursions (2–6 moves) from 210 known paths, expanded by the 16 move symmetries: 36,194 distinct.
  `acc_beam` now takes `BEAM_MACROS=file BEAM_MACW=w`. Each macro is one extra child and carries its
  true path length. Identical output with no macros. On ac-03305 (exact 23, beam 27), with macros mined
  leave-one-out: 27 at w = 0.5, 1, 2. A 4-row A/B on near-miss rows is running (old / macros / shadow).
- **Echo table** (the lead's verse: "the echo from the back is still talking to you"). States on or
  within r moves of our known routes, each with a known remaining distance, become extra targets for the
  exact capped search (`acc_capped` `ECHO_FILE=`, `build_echo.py`). A capped BFS state that meets the echo
  at depth d gives a path d + remaining, and the known tail completes it.
  - ac-05818 (record 34, ours 35): 7 routes (Codex map + ours), 122,317 echo states (r = 3).
  - Cap 25, depth 25, 55M states: best echo path 35 (our own route). No 34 exists whose first part stays
    within total length 25 and then joins a radius-3 neighbourhood of our routes. This complements
    Codex's corridor result (no 34 inside the radius-6 union).
- **Takeaway:** local repair of our near-miss paths (windows, corridors, echo, macros) keeps coming back
  empty. The record paths for these rows are different roads, not repairs of ours.

## 2026-09-28 02:45Z, session 2 (lead): the team lead's atlas, tested on AC
Seven ideas were read from the repo (atlas cards, UPG, Kakeya frontier, compound-eye originals). Tested:
- **Probe shadows as certified lower bounds** (OBS-PROBE-SPAN, ALG-FORCING-DUAL). Map words into
  SL(2,p) and BFS the finite shadow G×G. Correct, but capped by the shadow's diameter, which grows
  only logarithmically: 9 at p = 7 (113k states), 11 at p = 11 (1.7M). The mean bound/record is 0.11,
  which is inside T9's exact range, so there's nothing new to prune. General lesson: invariant-based lower
  bounds are log-scale, because one multiplication can double a word.
  Code: `research/acc/optimality/shadow_bounds.py`.
- **Two-layer capacity split** (GRAPH-SUBGRAPH-CAPACITY): charge only r0-moves, then only r1-moves,
  and add. It collapses to ≤ 2 per layer, since free moves on one word can prepare any multiplier for the
  other. The layers aren't independent. (The card's own failure mode warns about this.)
- **Probe shadows as a guide** (exterior probe of the hidden interior). A real signal: on 4,429 states
  ≥ 10 moves from the finish along known paths, corr(moves left, shadow sum over 4 probes) = +0.31, while
  word length gives +0.02. On hump states, shadow +0.24 and length −0.24 (length points the wrong
  way). Built into the beam as `BEAM_SHADOW=w BEAM_SHADOW_FILE=probes.bin` (off by default;
  identical output at w = 0). The first test, ac-03305 at W = 100k, stayed at 27 for w = 0.5–4 (exact
  23). Needs a broader A/B.
  Code: `shadow_probe_export.py`, `acc_beam.c`.
- **Next, the most promising: Schur elimination of the hump (UPG-FEEDBACK).** Remove the high states
  and replace them by effective macro-moves between low states. In practice: mine "up-and-back-down"
  segments from exact and known paths and let the beam take each as one step, so hump states never
  compete on length.

## 2026-09-28 02:45Z, session 2 (lead): checking the Smith-chart findings on beam-free paths
- **Why:** the 163 charted paths mostly came from our beam, so they carry its habits. The exact
  capped hits are BFS-shortest within their cap and have no scoring at all, so they're the fair check.
- **Result on 5 exact paths (ac-03305, 01629, 05558, 07435, 08201):**
  - The first word reaches length 1 at 87–97% of the way. **Confirmed**, though these last moves
    are inside T9 anyway.
  - Balance at the midpoint: 0.71–0.93 on flat rows, but **0.38 and 0.44 on the big-hump rows**
    (ac-03305 +16, ac-01629 +4). Balance holds only where the row is easy.
  - Climb shape: the big hump climbs in **single steps, zig-zagging** (longest climb run 1 on
    03305), not in 1–3-move bursts.
- **Orders for the beam change (session 1):** keep balance as a *mild* term. Add a reserved band of
  beam slots for states 5–16 letters above the start (slow zig-zag climbers). A/B test before switching:
  1. Old vs new scoring, same 3 seeds per row.
  2. Two groups: flat rows (known record, our beam 1–2 over) and hump rows (ac-03305, ac-01629,
     whose exact paths are known).
  3. Adopt the new scoring only if it doesn't lose on the hump rows.

## 2026-09-28 01:17Z, Codex helper: ac-09311 one-over corridor
- **Idea:** on k=1 rows with a 42-move record, use a larger H beam to reach a one-over witness and merge its route with a divergent finish.
- **Checked:** ac-09239, ac-09165, ac-09317 at width 100k gave no finish. ac-09311 gave verified AC 44 at width 100k and verified AC 43 at width 180k. These share 24 initial states, then diverge; the map is `research/acc/optimality/ac-09311_two_routes_map.json`.
- **Result:** neither is a score against record 42. Exact local windows through 14 found no shortcut. Radius-6 union had 54,987,511 states, 48,227,459 reached within 42 moves, no tie. No inbox line or SAIR POST. Only paths within this corridor are excluded.
- **Next:** seek a third finish that leaves the first 24-state shared opening, or return to exact sweep hits when they arrive. Always check `SENT_ROWS.txt` and fresh board before queueing.

## 2026-09-28 01:15Z, ChatGPT helper: detour height and a Pareto pilot
- **Drive research read:** `ACC-P000009 — Detour width on two Andrews–Curtis graphs` distinguishes arbitrary-word Lean conjugation from scored `ac-r2-v1` letter conjugation.
- **Derived bound:** on solution-relevant states, `L>=2`; each scored move gives `L_next<=2L`. Therefore a depth-`d` path from initial total `L0` has height at most `L0*2^d`. For ac-00145 (`L0=15`), even depth 38 has a finite but unusable cap of 4,123,168,604,160.
- **New idea tested:** keep nondominated exact-state labels `(moves, peak total length)`; target labels answer shortest-distance queries for every cap. On a synthetic five-step control, the Pareto profile `(4,8)` matched separate capped BFS (no path at caps 2–7 through depth 5; shortest 4 at cap 8).
- **Negative result:** the Pareto pilot used 71,638 transitions versus 55,005 for the separate cap searches (about 30% more) on this small case. Do not replace the current sweep on this evidence. The test and graph-bound analysis are in `research/acc/optimality/detour_height_pareto_note_20260928.md`; runnable script is `research/acc/optimality/pareto_height_pilot_20260928.py`.
- **Cap discipline:** this independently supports keeping witness peak separate from exact `closed_cap_through`. The ac-00145 31-height witness does not certify exhaustion below 31.
- **Outcome:** method test only; no scored path. Next step is a matched-cost comparison on a non-active short row if one opens.

## 2026-09-28 00:57Z, Codex helper: state exclusion and four-route corridor on ac-00145
- **Idea:** ban exact ordered states from a known route at selected depths in the H beam to discover a second path with a different middle or opening, then search the union of route neighborhoods for any number of lane switches.
- **Checked:** three new official-CLI-verified AC 40 routes (all already covered by our accepted 40). A single-state ban at depth 24 gave a lower-peak finish; banning depths 5–22 gave a route with 23 new states before rejoining around state 24. The [four-route graph](../optimality/ac-00145_four_routes_map.json) has 85 nodes/88 labeled edges. Radius-5 union: 6,682,338 states, no ≤39 path; radius-6 union: 59,899,612 states, 55,165,741 reached within 39, no path. This is a corridor bound, not a global shortestness proof.
- **Next:** ac-05064, our accepted 40 versus record 38 (k=2), starts with the same first relator and one sign difference in the second. A verified beam 40 has no shortcut in 429 windows of lengths 2–14. An uncapped depth-4 exact bridge check from all 40 route states found 16 joins near the shared goal (503,190 source-local states), but the best combined line is 40, so no ≤38 bridge. The phase beam found no finish; the 400k H beam found another AC 40. Banning route states 5–22 produced an independent AC 41 with peak 33. Both routes resisted local windows through 14; their radius-6 union had 51,512,374 states and no ≤39 route (48,681,575 visited). Map: `research/acc/optimality/ac-05064_two_routes_map.json`. Next: try low-k AC 42–43 records from the user's ac-09xxx list, beginning ac-09239.
- **Duplicate gate:** neither 40-move line is a new submission. Check `SENT_ROWS.txt` and official verifier on any shorter candidate before inboxing.

## 2026-09-28 00:52Z, ChatGPT helper: ac-00145 route-peak audit and cap distinction
- **Target status:** `SENT_ROWS.txt` has ac-00145 at 40 vs live 39, k=1; it is already active in Sweep B, so I did not launch another search.
- **Replay:** independently ran the candidate from `ACC_CANDIDATE_00145_20260926.txt` through the pinned official core (commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`). It reaches exact `(x,y)` in 40 moves; work 620; receipt hash `sha256:bbfbb1176ddd44ec9eb509086c7a677f560a50b1ba1f5a784b82331adfe51dd4`.
- **Height:** total relator lengths by state are in `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`. Peak is 31, first reached after move 24. Cap 31 contains the known route; cap 32 does too.
- **Cap correction to the 00:25 proposal:** a witness path's peak is not an exhaustive-search boundary. The 41 states on this route do not show that every state below total length 31 was searched. Track `known_route_peak` separately from `closed_cap_through`; skip a lower cap only when the exact run ledger certifies that cap is exhausted. For ac-00145, the peak gives a feasible ceiling for this witness, not a proof that lower caps are covered.
- **Outcome:** no new candidate or score; only the route-height audit. Full evidence: `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`.

## 2026-09-28 02:30Z, session 2 (lead): replies to the helpers, and combined exclusions
- **ChatGPT's cap correction is right.** My 00:25 "start above our path's peak" idea was wrong: a
  witness peak doesn't certify that lower caps are exhausted. The live sweep doesn't rely on it.
  Jump-ahead uses only the fact that a cap-C search contains every lower cap, and each run records
  `complete` per cap (= `closed_cap_through`). Probe-and-predict skips only caps it has not claimed.
- **Combined exclusions (exact capped search + Codex corridors):**
  - ac-00145 (record 39): every ≤ 39 path peaks at ≥ 23 (capped, closed through 22), **and** leaves
    the radius-6 union of four known routes (60M states).
  - ac-05064 (record 38): every ≤ 38 path peaks at ≥ 23 (capped), **and** leaves the radius-6 union
    of two routes (51M states).
  Neither is a global shortestness proof. Together they say the record paths are high and far
  from ours.
- **Suggestion for Codex:** start the next corridor from a state of the capped search's last closed
  layer that is *outside* the known-route union, since the record path must pass through one.
- **Pareto labels (ChatGPT):** noted. At 30% more transitions they won't replace the sweep.

# ACC ideas log (both sessions add one idea per turn; newest first)

Format: date/time, session, idea, what was checked, result, next step. Read the other session's
latest entry before starting your turn, and build on it when you can.

## 2026-09-28 02:20Z, session 2 (lead): "the leader controls the family" (team lead's riff)
- **Idea:** in a matrix family, the dominant eigenvalue governs long-run behaviour and the rest is
  noise (a Dunford/Riesz projection pulls it out). Capped BFS layers are powers of the capped
  transfer operator, so after the noisy first layers the growth follows a smooth "leader" curve.
- **Checked (ac-05818, cap 25):** layer growth ×2.4, 2.1, 2.0, 1.9, … 1.34. log(growth) decays
  almost linearly as the capped region fills.
- **Test:** fit that decay on the last 6 layers of a cheap 10M-state probe and extrapolate to depth
  MAXD. Cap 26: predicted 80M, actual 87M (completes). Cap 27: predicted 397M, actual > 196M
  (blows the budget). The prediction is right on both.
- **Change:** `run_capped_sweep.py` now probes each cap first. If the probe finishes, that's the
  answer. If the prediction is above 90% of the budget, the cap is skipped (`SKIPPED_PREDICTED`).
  No more full budget-sized runs that fail at the end. A step-down also always tries the start cap.
- **Also:** conservative matrix fields (Ramanujan Machine group) are path-independent matrix grids
  behind formulas for ζ(3), π and Catalan's constant. They're not used here yet.

## 2026-09-28 02:00Z, session 2 (lead): "Comutators" (the team lead's track, turned into a test)
- **Idea:** the lyric's measure of non-normality is the commutator. Measure how badly r0 and r1 fail
  to commute, and use it to predict the hump before searching.
- **Checked:** 292 verified known AC paths (climb = path peak − start). Cyclic commutator load is
  min over rotations of |[r0, r1]| / (2·start). Tool: `research/acc/optimality/hump_features.py`.
- **Result:** corr(climb, cyclic load) = **+0.36** (plain load +0.20; start length −0.45). The
  least-commuting quarter of rows climbs about 75% higher (7.9 vs 4.5). A linear model (start,
  length, load) reaches R² 0.34 but misses the extreme humps: ac-03305 needs +16 and the model
  predicts +3.6. On 27 of the 45 bounded rows, the proven climb is already above the model.
- **Where it fits:** triage, not caps. Within a value tier, sweep low-load rows first. The
  empirical correlation also goes into the Proof Track draft as an observation, not a theorem.

## 2026-09-28 01:35Z, session 2 (lead): the training roads (user hint)
- **Idea:** `competition/examples/training_424.json` in the official repo holds 424 known
  trivializations of Miller–Schupp MS(n,w) presentations. Every state on those paths has a known
  distance to (x, y), so they're ready-made roads. A scored start near a road state gets
  bridge + rest of the road.
- **Checked:** `research/acc/optimality/road_bridges.py`. It replays all 424 paths with the
  official kernel formulas and hashes every state, plus its relator-and-generator-swap image. Then
  it runs BFS to radius 2 from all 10,115 scored starts.
- **Result:** 4 scored starts sit within 1–2 moves of a road, but the roads are long (27–140) and the
  records are shorter already (ac-08327: 27 vs 17, ac-09594: 33 vs 15, ac-09868: 63 vs 25,
  ac-07667: 140 vs 45). No gain as they stand.
- **Next:**
  1. The scored pool looks like scrambled MS(n,w). If the scored starts are MS(n,w) instances after
     random moves, then identifying (n, w) for each row lets the training path for the same (n, w)
     plus an exact bridge solve it. Test: canonical MS form per row.
  2. Shorten the 4 road paths with window-14 and the capped search from the road states.
- **Proof track:** submissions are published in the SAIR Contributor Network. It isn't in the
  public API (probed 20 paths), and the website is blocked here.

## 2026-09-28 00:40Z, session 2 (lead): jump-ahead caps
- **Observation (38 finished rows):** a cap-C search already contains every lower cap. Climbing
  one cap at a time cost 2–3.5× the final cap's states (ac-03305: 556M total vs 160M for the last
  cap). All hits so far came 1–13 above the start (most within +4): 07435 +1, 05558 +2, 01629 +4,
  03305 +13.
- **Change:** `run_capped_sweep.py` now starts at start + CAP_JUMP and climbs. If that first cap
  runs out of budget, it steps down by 2 until one completes. Jumps: 8 for A (180M), 3 for B (70M,
  deep rows), 5 for C (25M). Expect about 2× the rows per hour.
- **ac-05818:** proved empty only through cap 26 (budget hit at 27, depth 25). The helper's routes
  reach 29, so the capped search can't cover this row. **Helper: keep the corridor/route method
  for rows with deep records (≥ 34).** The capped search is best at depth ≤ 22.
- **ac-09365:** the hit was sac 31, which we already tie. No gain.
- **Next idea:** give each tool the depth it's good at. Capped for records ≤ 31, corridor/route
  merging (helper) for 32–40, and nothing on ≥ 41 until the memory problem is solved.

## 2026-09-28 00:25Z, session 2 (lead), building on the helper's ac-05818 map
- **Helper result:** seven verified 35–36 routes for ac-05818 and a radius-6 corridor search
  (63M states) found no 34-move path.
- **Build-on:** every one of those routes stays at total length ≤ 29 (the start is 25). The record
  34 path (2 teams) probably climbs higher. The exact capped search covers that directly: raise the
  cap from 25 until the budget runs out. **ac-05818 is now first in sweep A (180M budget).**
- **Bridges r = 3:** 21 distinct pairs. The records of each pair differ by no more than the bridge
  length, so there's no gain. Bridges and mirrors are both closed.
- **Helper lines for 01734:** both (ac 36, sac 38) were already accepted from us (sac-01734 38 in
  submission 2558). To avoid repeats, check `research/acc/live/SENT_ROWS.txt` (every row SAIR
  accepted from us, with the live record) before preparing a line.
- **Next idea:** a route's peak total length tells the capped search which cap to use. For each
  row, run the first capped search just above our best path's peak. Everything below that peak is
  already covered by our own path's search.

## 2026-09-28 00:12Z, session 2 (lead)
- **Idea:** near-mirror bridges (built on the mirror idea below): pairs of starts at most r moves
  apart.
- **Checked:** r ≤ 2 across all 10,115 starts (`research/acc/optimality/find_bridges.py`).
- **Result:** one pair, ac-03765 ↔ ac-07258 (2 moves), and both rows are unsolved. No gain yet.
  r = 3 is running on the spare core.
- **Also:** sweep C found ac-07435 26 and sac-07435 28 (ties, k 6). Both are verified and queued
  (2 lines; the batch goes at 3).
- **Next:** if r = 3 also only links unsolved rows, treat each such cluster as one target. Solving any
  one row solves all of them (+1 each). Pick the cluster with the shortest start words and give it the
  big budget.

## 2026-09-28 00:05Z, session 2 (lead)
- **Idea:** mirror transport. If row A is an exact mirror of row B (swap x/y, invert x or y, swap
  the relators), a path for B becomes a path for A at 0–2 extra moves (Stable AC: +2 finish).
- **Checked:** all 10,115 starts under the 15 non-trivial symmetries.
- **Result:** 22 mirror pairs exist, and none gives a shorter path than the live records. The
  leaders already cover them. Dead end.
- **Next (session 2, spare core):** near-mirror bridges. If A's start is within r ≤ 3 moves of
  B's start, then path(A) ≤ r + path(B). Look for rows where record(A) > r + record(B), and for
  unsolved rows next to solved ones (1 point each). One BFS of radius 3 per start, hashed across
  all starts.
- **Question for session 1:** which of your 146 rows finished without a hit, and at what cap? If
  the direct Stable AC paths need caps 12+ above the start, say so and I'll put the big budget
  (180M) on the best ones.

## Standing results worth remembering
- The exact capped search found every tie since 23:30 (sac-03305 +0.5, ac/sac-01629 +0.19,
  ac/sac-05558 +0.06). The beam found none of them.
- Every AC hit also produces its Stable AC line (AC + [16,15]). It's automatic in the sweep.

## 2026-09-28 session 1: is rank 3 behind the short Stable AC records? (checked)
At rank 2 the only 2-move Stable AC finishes are from (x,y) and (y,x) (destabilize needs a relator equal to one
positive generator that appears nowhere else). So an exact rank-2 SAC optimum = min(d(x,y), d(y,x)) + 2.
Exact check (acc_capped, cap 400, fingerprints) on the 9 shortest rows with SAC record <= AC record + 1:
00894, 05911, 03448, 04860 so far all match their SAC record at rank 2 through (y,x) + [15,15].
Result: on short rows the "SAC gap" is the swap finish, not rank 3. Rank 3 is still untested on long rows.
Log: ledger/sac_rank2_probe_20260928.log

## 2026-09-28 session 1: cross-row lookup, radius 2, 467 own paths + 424 SAIR training paths
478 rows got a verified borrowed path, 17 new or shorter than ours, 0 ties. Nearest: ac-00766 34 (record 33,
via ac-03562), ac-00974 26 (record 24, via ac-01077). Exact window shortening on those is running.
Raw: ledger/crossrow_r2_20260928.json

## 2026-09-28 session 1: borrow a road, then shorten the joins (WORKED once)
ac-03028 had no path of ours. crossrow.py found start -> 1 move -> a state on ac-09650's path under mirror 5
(swap x<->y with signs), total 29. Exact window shortening (acc_window, all windows <= 14) cut it to 26 = record
(13 teams). SAC = AC + [16,15] = 28 = record. Official verifier: both accepted. In the inbox.
Why it works: the borrowed road was never tuned for this start, so the joins have slack that windows can remove.
Next: index radius (tools/acc/crossrow.py --iradius N) puts every state N moves off a known road in the index;
row radius 2 + index radius 2 reaches as far as row radius 4, at a fraction of the cost. Running on all rows.
Adam/Bob/Charlie: any new path you find, even a long one, feeds this. Put it in a jsonl with {"id","ac"} and tell us.
Window results on borrowed roads (acc_window, every window <= 14 moves, exact; raw in ledger/crossrow_windowed_20260928.jsonl):
ac-00766 34 -> 34 (record 33), ac-00974 26 -> 26 (record 24), ac-03028 29 -> 26 (TIE), ac-03919 32 -> 30 (record 27).
Bob: 00766/00974 need windows longer than 14 or a different road; short windows are done.

## 2026-09-28 session 1: mirrored roads give free Stable AC ties (WORKED: 13 new SAC ties + ac/sac-03028)
Stable AC can finish from (x,y) with [16,15] or from (y,x) with [15,15]. A mirror that switches x and y turns a road
to (x,y) into a road to (y,x) with no fix moves, so it can beat "AC path + 2". crossrow.py --slive now builds
both and verifies SAC with the official stable kernel. Row radius 2 + index radius 2 over all rows:
498 rows got a borrowed SAC path; 13 were at the live record and never sent (k 6-20). In the inbox.
Raw: ledger/crossrow_r2i2_sac_20260928.json
Next (running): cross-row echo. tools/acc/build_xecho.py puts all 21k road states x 16 mirrors (255k) in an
acc_capped ECHO_FILE so the exact capped BFS can meet another row's road deep in the search, not just 2 moves from
the start. First rows: ac-09989, 03919, 04251, 06903.
Stopped: unk15 beam (helper's 15 unsolved L0 16-18 rows; BEAM_H=1 DIV=1.0 BAL=1, width 200000, depth 600):
8 rows done in 3.5 h, 0 solutions (ac-00008 00066 00137 00254 00392 00045 00095 00164). Incomplete; rows 9-15 not run.
Raw: ledger/beam_unk15_20260928.jsonl

## 2026-09-28 session 1: unsent roads (WORKED: 20 AC ties to inbox, + ac/sac-09989)
Pooled every verified road we hold: repo lines, graph-map archive (60 AC routes), route maps, scratch runs:
677 roads on 496 rows (tools/acc/crossrow.py keeps extra roads per row as "id#n"). Lookup (row r2 + index r2):
20 AC rows where we hold a road at the live record that is not in our accepted history (16 never sent,
3 behind). Lesson: before new search, diff every road we hold against the accepted history.
Borrowed road + exact window also tied ac-09989 (24 -> 23 = record, via ac-01229).
Raw: ledger/crossrow_roads_{ac,sac}_20260928.json

## 2026-09-28 session 1: the board is Miller–Schupp families; the leaders have a 2^n construction (BIG)
- **Families.** 2,937 rows are exact MS(n,w): one relator is y^-(n+1) x^-1 y^n x (written Y^(n+1) X y^n x), n = 1..10,
  the other is a short word w. They hold **1,977 of the 2,672 unsolved rows**. The other 7,178 rows have no MS relator
  in plain form (695 unsolved). Borrowed roads work because rows in a family share one relator exactly.
- **Doubling chains.** For 10 second words w, every n = 3..10 is solved and the record is 2^(n+1) + small:
  w = YXyXyx: 32, 56, 91, 158, 288, 547, 1061, 2088 (= 2^(n+1) + 16, 24, 27, 30, 32, 35, 37, 40).
  **68 of those rows are held by at most 2 teams, most by 1.** A k=1 tie is worth a full point (our AC total is 0.565).
- **Mechanism (from our own n=3 path, ac-09243, 36 moves):** the words collapse to a Baumslag–Solitar relation
  YXXyx (y^-1 x^2 y = x) and y^-1 x^(2^n - 1); the power is built one letter at a time, then peeled one letter per
  move with r1 <- r1·r0. So the path must carry a word of length ~2^n; build + peel = 2^(n+1).
- **Running:** H-beam on the 28 chain rows with n = 4..6 (depth record + 20). If it solves n = 4, 5, the paths
  should show a repeated block; the template prefix + block^(2^n - c) + suffix then gives every n up to 10 directly.
- **Also open:** 106 second words where some n is solved and other n are not, e.g. w = YXYxYx: n=2 solved (24),
  n=3..10 all unsolved. A construction that works there is worth 1 point per row.
- Raw: ledger/ms_families_by_w_20260928.json ({"w|pos": {n: [record, teams, id]}}).
**CORRECTION 06:40Z: INVALID as an echo test.** My acc_capped binary predated ECHO_FILE support and ignored the echo; these are plain capped searches only (still valid as such). Rerunning with a rebuilt binary.
Cross-row echo result (session 1): exact capped BFS meeting 255k mirrored road states, 4 near-miss rows, no meet:
ac-09989 cap 29 complete (35M states), cap 31 incomplete; ac-03919 caps 18/20/22 complete; ac-04251 caps 21/23 complete;
ac-06903 caps 22/24 complete (52M). Scope: first REC-10 moves under the cap, then a road tail. Raw: ledger/xecho_20260928.log
Disk note: a Stable AC probe (ac-01962, cap 400, depth 9) wrote 20 GB of layer files and filled the disk; it was stopped
(incomplete) and the window queue and MS-chain beam died with ENOSPC. Keep a length cap on exact runs.

## 2026-09-28 session 1: what the unsolved rows are
- 2,672 unsolved rows. About 2,190 contain a Miller–Schupp relator (any spelling). The other 481 also repeat a few
  relators: (y^-1 x^-1)^m (yx)^(m-1) shapes appear in 38-50 rows each (m = 4..8), plus short words like YYYXyxyyx.
  These look like Akbulut–Kirby-type presentations (the AK(3) kind from the proof track), i.e. famous open cases.
- Consequence: blind beams on unsolved rows (Adam's lane, my half A: 118 rows, 0 solves) are unlikely to pay.
  The paying lane is the doubling chains, where the leaders have a construction and we can match it.
- Doubling engine arithmetic (MS(n, YXXyx)): in phase B, r1 = x^a Y^2 x^b y and each pair (5,11) maps (a,b) to
  (a-1, b+2), so 2a+b is fixed at 2^n - 1. Phase B only converts; the mass 2^n - 1 is created in phase A.
  Our n=4 path pays for the mass twice (A builds x^7 at ~1 move per x, B spends 2 moves per x converting).
  The leaders' ~2^(n+1) + 1.5n + 8.5 suggests they create the right-hand run directly. Exact n=4 search at caps
  21 (complete, no path <= 49 under cap 21), 23, 24, 25 is running to find it.
MS(4, YXXyx) exact facts (session 1, 05:40Z): see ORDERS_luna_ms.md "Update 05:40Z". Our construction is
~3*2^n; records ~2*2^n; the leaders' n=4 road must exceed total length 23 early. Road cycle: ac/sac-07004 ties (k14).

## 2026-09-28 06:10Z, session 1: MS(3, YXXyx) in 28 (exact, cap 20): the 1-move-per-x build
`5 1 12 2 5 8 3 6 3 6 3 0 12 2 6 8 2 7 5 6 6 2 4 4 4 4 4 4`. The build pairs (3, 6) grow X^2 in r0 per 2 moves;
the conjugation by x cancels a leading X, so there is no rotation cost. Then y = x^7 and y = x^6 collapse to x in one
move, and the peel is 6. Answers session 2's crux for n=3. n=4 needs more leading X's (details in ORDERS_luna_ms.md).
Other exact n=3 results: cap 16 -> 30, cap 18 -> AC none <= 29 (SAC 31), cap 20 -> 28. n=4: cap 21 none <= 49
(complete), cap 23 none <= 46 (depth 37, budget), cap 24 none <= 38 (depth 29, budget).
