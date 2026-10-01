# t00285: interpolate certified anchors for MS(n, w), w = y^3 x y^-2 x^-1 (twin x^-1 y^-3 x y^2); rows ac-09632 (n=4), ac-05538 (n=5)

Idea credit: Bob (02:15Z). Builder: UPG-H, pinned verifier ~/.cache/upgh/sair (`verifier.core`, ac-r2-v1), T9 ~/.cache/upgh/T9.tab.
No path on either row verified in this task; no lines.txt was written. Everything below is a scoped miss or an exact
negative statement with its scope.

## 1. Which training instances are the same presentation family (exact symmetry)

Official starts (manifest): both rows have r0 = `YYYxyyXX` = y^-3 x y^2 x^-2; r1 = `Y^(n+1) X y^n x` (n=4: ac-09632, n=5: ac-05538).
Other rows with the same r0: n=7 ac-09090, n=8 ac-06811, n=9 ac-02630, n=10 ac-01923 (not in this contract). The
family has NO challenge at n=1,2,3,6; those are training-only.

Training rows (training_424.json, training frame (T0, T1) = (`X y^n x Y^(n+1)`, `x YY X yyy x`)):
twin form w = x^-1 y^-3 x y^2: ms-train-0341 n=1 (18 moves), 0342 n=2 (83), 0343 n=3 (21), 0344 n=6 (60).
Direct form w = y^3 x y^-2 x^-1 (T1 = `xxyyXYYY`): ms-train-0249 n=1 (17), 0250 n=3 (14), 0251 n=6 (100).
MS-1190 metadata (verifier data csv rows 617-623 and 869-875): this w at n=4 is open class 15_{11} (twin 15_{10}),
n=5 open 16_5 (twin 16_4), n=7 open 19_{45}/19_{50}; n=1,2,3,6 certified. So both contract rows are listed open
presentations.

Exact symmetry challenge <- twin training (verified with core.verify on manifest-shaped starts for n=1,2,3,6, fam.py):
- challenge r0 = x . T1^-1 . x^-1 (the w relator, inverted and conjugated by x);
- challenge r1 = y^-(n+1) . T0 . y^(n+1) (the MS relator rotated);
- the relators are SWAPPED relative to training.  The move set has no swap, so a training path transfers as
  `prefix(n) + swap(moves) + [0,2,5,2,8]` with prefix(n) = [7, 0] + [12]*(n+1) (undo the conjugations and the
  inversion: n+3 moves), swap = relator-role map {0<->1, 2<->4, 3<->5, 6<->10, 7<->11, 8<->12, 9<->13}, and the
  5-move canonical suffix ([y],[x]) -> ([x],[y]) from the move spec table.  Verified lengths: n=1 18->27, n=2 83->93,
  n=3 21->32, n=6 60->74, all ok=True on synthetic challenges with the official shape (and the identical mapping is
  what any n=4/5 training-frame path would use on the real rows).

## 2. Alignment of the n=3 (21) and n=6 (60) twin anchors (traces_twin_n3_n6_training_frame.txt)

Common opening (training frame): [9, 11, 1, 12] for all four twin anchors (n=1,2,3,6). After it the state is
(`Y X y^n x Y^n`, `y X X Y^3 x y`) for every n, total unchanged.
- n=3 then plays 4 (r1 <- r1 r0): `y X X Y^3 . y^3 x Y^3` -> `y X Y Y Y` (the y^3 of w cancels the Y^3 of MS(3)),
  then 13 -> r1 = `XYY`, i.e. x = y^-2, at move 6 (Bob's "move 7" is the inverted form `yyx`). The finish from
  (`YXyyyxYYY`, `yyx`) is 15 moves and purely mechanical (one-x collapse).
- n=6 instead plays 0, 1, 2 (invert both, r0 <- r0 r1) giving r0 = `y^n X Y^(n-3) x x Y` for general n, then 9, 6, 12 and
  2 (r0 <- r0 r1): the Y^(n-3) of r0 meets the y^3 of w, which cancels exactly only when n = 6, giving r0 = `x y^5 x Y Y`
  (x y^5 x = y^2) at move 11.  Moves 12-21 reach (`YYxyyXXY`, `XYYYXXY`), 22-51 are a 30-move middle game that
  accumulates conjugates of a 6-letter r0 (`xyXYxy`, a commutator-like word) into r1, until r1 = `XYY` at move 51;
  the finish (9 moves) is again the one-x collapse.
- n=2 (83) is a third mechanism: the same opening, then 4, 13 gives r1 = `XXYxY` and a 70-move middle game that
  ends with r1 = `XYY` at move 76.

Group reading (phi(g) = x^-1 g x): MS gives phi(y^n) = y^(n+1); w gives phi(y^3) = y^2 x^-1.  n=3: phi(y^3) two ways
=> x = y^-2 in two multiplications.  n=6: phi(y^6) = y^7 = (y^2 x^-1)^2 => x y^5 x = y^2 (the move-11 relator).
n=4: phi(y) = phi(y^4) phi(y^3)^-1 = y^5 x y^-2 (or phi(y) = x y^3 from phi(y^-3) phi(y^4)); n=5: phi(y^5) = (y^2 x^-1)^3
is a 3-x relator.  Neither gives a one-x relator by a single multiplication, which is exactly what the replays show.

## 3. Growth law: there is none of the pumped-block kind (negative result, exact)

The literal move lists were replayed on the n=4 and n=5 training-frame starts (replay_anchors_at_n.py/.txt):
- n=1, n=2, n=3 anchors: the state shape (y-runs compressed) diverges from the anchor's own trace at step 5, the
  first multiplication, because the cancellation y^3 . Y^n is n=3-specific;
- n=6 anchor: diverges at step 11 (needs Y^(n-3) . y^3 = 1).  Its first 8 moves [9,11,1,12,0,1,2,9] are n-generic and
  are the lowest-total states found anywhere: n=4 -> (`yyyXYxx`, `YXyyyxxY`) total 15 (= the MS-1190 class label 15),
  n=5 -> (`yyyyXYYxx`, `YXyyyxxY`) total 17.
- All anchors run away after divergence (end totals 46..4662), so there is no tail to repair; the restart states
  above were used instead.  The n=3 and n=6 middle games are different mechanisms, not one block repeated f(n)
  times, so interpolating "between" them is not defined.  No candidate path was built from a law because none exists.
- Peak totals of the anchors: n=2 peak 15 = start 15, n=3 peak 17 = start 17, n=6 peak 23 = start 23: every certified
  route in this family has zero hump.  By section 4, n=4 has no zero-, +1-, +2- or +3-hump route at all.

## 4. Search attempts (all on the official starts; every output file is in this directory)

Encoding for the C tools: x=0 X=1 y=2 Y=3; ac-09632 start `8 3 3 3 0 2 2 1 1 11 3 3 3 3 3 1 2 2 2 2 0`,
ac-05538 start `8 3 3 3 0 2 2 1 1 13 3 3 3 3 3 3 1 2 2 2 2 2 0`.  Restart states in intermediate_states.txt
(prefixes recorded in harvest.py).

| run | row | settings | result | scope |
|---|---|---|---|---|
| acc_beam from start (beam_09632_w20000_div0.6.*) | ac-09632 | W 20000, DMAX 600, BEAM_DIV 0.6, T9 finish | AC NONE, SAC NONE, d=600 reached | beam width 20000 only |
| acc_capped CAP 22 (capped_09632_cap22.*) | ac-09632 | MAXD 60, budget 60M | STOPPED at d=61, 3,418,076 states, AC NONE | superseded by the closure below |
| acc_capped CAP 22 (capped_09632_cap22_maxd140.*) | ac-09632 | MAXD 140, budget 90M | **CLOSED at depth 83, 3,651,832 states, AC NONE, SAC NONE** | exact: no AC path from ac-09632 whose prefix stays within total length 22 (the T9 tail is uncapped); the start is 19, so any route needs a hump >= +4 |
| onex_bfs.py cap 21 (onex_09632_cap21.txt) | ac-09632 | all 14 moves, depth 40, 1.22M states | no state with a one-x relator | depth-limited |
| onex_bfs.py cap 22 (onex_09632_cap22.txt) | ac-09632 | to closure | **closed at depth 83 with 3,651,832 states (independent Python kernel, same count as acc_capped), no one-x relator state** | exact within cap 22: Bob's collapse set is unreachable without a hump >= +4 |
| onex_bfs.py cap 23 (onex_05538_cap23.txt) | ac-05538 | see file | see section 5 | |
| acc_beam from the total-15 restart (beam_09632_tot15_div0.6.*) | ac-09632 | prefix 15 moves, W 20000, DMAX 300 | AC NONE, SAC NONE | beam |
| acc_beam from the total-17 restart (beam_05538_tot17_div0.6.*) | ac-05538 | prefix 16 moves, W 20000, DMAX 300 | see section 5 | beam |
| acc_beam from start (beam_05538_start_div0.6.*) | ac-05538 | W 20000, DMAX 400 | see section 5 | beam |
| acc_beam BEAM_H=1 (beam_09632_start_H1.*) | ac-09632 | W 20000, DMAX 300 | see section 5 | beam |
| acc_capped CAP 24 (capped_09632_cap24.*) | ac-09632 | MAXD 400, budget 90M, 1000 s | see section 5 | |

All runs: at most two of my processes at a time (the other builder had three acc_beam processes on the 4 cores
throughout).  harvest.py rebuilds prefix + reported moves for every `AC d PATH` line and verifies with the pinned
core; verify_log.txt holds its log.  Nothing verified, so no lines.txt.

## 5. Final results of the runs that were still open when section 4 was written

- Restart/start beams (beam_chain.log): ac-09632 from the total-15 state: AC NONE, SAC NONE at d=300; ac-05538 from the
  total-17 state: AC NONE, SAC NONE at d=300; ac-05538 from the start (W 20000, DMAX 400): AC NONE, SAC NONE;
  ac-09632 from the start with BEAM_H=1: AC NONE, SAC NONE at d=300.  All width-20000 beams, scoped misses only.
- onex_bfs.py ac-05538 cap 23 (onex_05538_cap23.txt): state budget 4.5M reached at depth 79, no one-x relator state
  (bounded, not closed; the frontier was still 18k wide).
- acc_capped CAP 24 ac-09632 (capped_09632_cap24.*): **CLOSED at depth 145, 32,074,048 states, AC NONE, SAC NONE.**
  Exact: no AC path from ac-09632 whose prefix stays within total length 24; with start 19 every route needs a peak >= 25.
  (The anchors n=2,3,6 have peak = start.  This is the concrete reason n=4 is open: its route, if found, has a hump
  of at least +6, which width-20000 lowest-total beams discard.)
- Direct-form symmetry (direct_map.py/.txt): challenge (r0, r1) = ((yinv T1)^-1, (yinv T0)^-1) exactly, yinv = the
  automorphism y -> y^-1 (move ids 8<->9, 12<->13).  Transfer: [0,1] + swap(yinv(moves)) + [2,5,2,8]; verified n=1
  17->23, n=3 14->20, n=6 100->106 (ok=True).  Replaying the direct n=3/n=6 lists on the n=4/n=5 rows never goes
  below the start total, so they give no restart states.
- acc_capped CAP 24 ac-05538 (capped_05538_cap24.*): **CLOSED at depth 109, 9,632,608 states, AC NONE, SAC NONE.**
  Exact: no AC path from ac-05538 whose prefix stays within total length 24 (start 21): any route has a peak >= 25.
- acc_capped CAP 25 ac-09632 (capped_09632_cap25.*): **CLOSED at depth 159, 118,139,720 states, AC NONE, SAC NONE**
  (budget 150M, 840 s).  Exact: no AC path from ac-09632 whose prefix stays within total length 25: any route has a
  peak >= 26, i.e. a hump of at least +7 over the start 19.

## 6. Summary and what would reopen this

- Prediction before running: null (no verified path on either row within the limits); outcome: null, as predicted.
- The interpolation premise does not hold for this family: the certified n=3 and n=6 routes use n-specific
  cancellations (y^3 against Y^n at n=3; Y^(n-3) against y^3 at n=6) and have different middle games; the n=2 route is
  a third mechanism.  There is no pumped block and no growth law; literal replays diverge at step 5 (n=1,2,3 lists) or
  step 11 (n=6 list).  The common 8-move prefix of the n=6 route is the only transferable piece (it reaches the
  lowest totals seen: 15 on n=4, 17 on n=5).
- Exact negative scope established with the pinned tools and an independent Python kernel: ac-09632 has no route
  with peak <= 25 (118M-state closure), ac-05538 none with peak <= 24 (9.6M-state closure); the one-x collapse set
  is unreachable within cap 22 on ac-09632 (closed) and within 4.5M states at cap 23 on ac-05538 (bounded).
  All certified anchors have zero hump, so n=4/5 routes are qualitatively different from the anchors.
- Worth doing next (not done here): a cap-26/27 closure on ac-09632 needs > 150M states (growth x3.7 per cap unit:
  3.65M -> 32M -> 118M) and more than one lease; beams with BEAM_BAL / high-hump tolerance from the total-15 and
  total-17 restart states; a 3-x-relator target set (phi(y) = x y^3 at n=4, phi(y^5) = (y^2 X)^3 at n=5) instead of
  the one-x set.  A real n=4 or n=5 anchor from any team (event new_path on ac-09632 / ac-05538) would make the
  alignment worth redoing with a third mechanism in hand.
