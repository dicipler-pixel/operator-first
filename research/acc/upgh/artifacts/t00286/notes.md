# t00280 notes: level map for the MS(n, w) singletons, w = YYxxxYXX (ac-00766 n=2, ac-00764 n=3, ac-02598 n=4) and w' = YYxxyXXX (ac-06036 n=3)

Contract mismatch: `tasks/t00280.json` on disk names sac-09995 / beam_free; the launching agent's directive for t00280 was the
level-map plan on ac-00764 / ac-06036 / ac-02598 (session 1's idea). I followed the launcher's directive. No sac-09995 work was done.

Orientation. Official rows: ac-00764 = (r0, r1) = (w, P3), ac-02598 = (w, P4), ac-06036 = (w', P3) with P_n = Y^(n+1) X y^n x.
ac-00766 (n=2) is the other way round: (P2, w). Relator swap is the move relabelling 0<->1, 2<->4, 3<->5, 6..9<->10..13
(`swap.py`), but the target (x,y) is not swap-symmetric: the swapped n=2 route ends at (y,x), 5 moves from (x,y).
All made-up levels here use the official n=3/n=4 orientation (w, P_n).

## Session 1 facts used (research/acc/live/sweeps/session1/levelmap/README.md, updated during this task)
- ac-00764 and ac-06036: capped components CLOSED at caps 24, 26, 28, 30 (290.7M / 314.2M states at cap 30): every route peaks above 30 (start total 17).
- ac-02598 / ac-01449 / ac-04923: CLOSED at cap 32: every route peaks above 32 (start total 19).
- Both held ac-00766 routes re-verified here with the pinned verifier: 34 moves, peaks 29 (route A) and 26 (route B).

## Level 1 (made-up start (w, P1) = (YYxxxYXX, YYXyx), total 13)
acc_disk forward BFS at cap 22 (`disk_n1_w_cap22.log`): 27 layers, 110,360,090 states, stopped DISKFULL (2 GB guard) with
min_total 3 at layer 27 and (x,y) not reached, so MS(1,w) at cap 22 is >= 28. The single total-3 state of layer 27 is (y, Xy);
`acc_disk path` gives its 27-move path (`n1_w_path_to_total3.txt`) and [3,10,4] finishes: a 30-move route, replayed with core.apply_move
(`n1_w_route30_trace.txt`). Cap-22 optimum is 28..30.
Structure (trace in n1_w_route30_trace.txt):
- 0-3: w := w * P1(conj), conj, invert -> r0 = x y^2 x y X^3 y (w^-1 with the pump glued on).
- 4-13: TRANSPORT: five times (r0 *= R1 ; conj Y or X): each "X y" at the right end becomes "y^2 X" (P1: X y = y^2 X), the
  conjugation brings the next y to the right. Net effect: x^-3 pushed through w's y-runs, exponent doubling per X: y -> y^8 = y^(2^3).
  Result r0 = x y X y^8 X (y^8 = x Y X x in G).
- 14-19: r1 (P1 conj) *= r0 -> r1 = X y^8 (x = y^8), then r0 *= R1 -> r0 = y.
- 19-29: peel: 7 x (r1 *= R0) then [3,10,4]. Endgame length = k + 3 with k = 8.

## Level 2 (ac-00766, held route B, peak 26; trace in this file's companion output, see README held routes)
In (P2, w) orientation, G-terms:
- 0-7: PHASE 1 on w^-1 = x^2 y X^3 y^2: conj X -> x y X^3 y^2 x ; P2 "y^2 x -> x y^3" -> x y X^2 y^3 ; conj ; P2 "X y^2 -> y^3 X" ->
  r1 = x y X y^3 X y. (y^3 = x Y X Y x.) Both P2 uses consume w's own y^2 run (2 = n).
- 8-9: r0 := P2(conj) * R1 -> r0 = x Y^6 x Y X y (pump doubled: x y^-6 x y^-1 x^-1 y = 1; 6 = n(n+1)).
- 10-16: r1 := r1 * R0, conj x3, r1 *= r0, conj -> r1 = (cyclic) y^5 X y x Y X. Peak 26 at step 10 (r1 = x y X y^4 X y^6 X, r0 len 11).
- 17-21: r0 := r0(conj) * R1 -> r0 = Y^5 x Y^6 x (x y^-6 x = y^5).
- 22-24: r1 := r1(conj) * r0 -> r1 = x Y^6 (x = y^6).
- 25-33: endgame 9 moves = k + 3 with k = 6: inv1, conj, r0 *= r1 -> (x Y^5, y^6 X), r1 *= r0 -> (x Y^5, y), 5 x (r0 *= r1).
Route A differs only in phase 1/3 ordering (peak 29).

## The level map, and why it breaks at n = 3
Common shape of levels 1 and 2: (i) TRANSPORT w's y-runs through w's own x^-letters with P_n (X y^n -> y^(n+1) X, or y^n x -> x y^(n+1)),
one AC multiplication by a P-conjugate per transported run, plus 1-2 conjugations to bring the next run to the end of the word; (ii)
combine with the pump to derive x = y^k (k = 8 at n=1, k = 6 at n=2); (iii) endgame of k + 3 moves (peel y^k).
At n=1 the transported block is "r0 *= R1, conj" repeated 5 times (10 moves) = the inserted block relative to a 20-move skeleton.
At n=3 and n=4 step (i) is impossible as written: w = y^-2 x^3 y^-1 x^-2 has y-runs 1 and 2 only, and P_n moves only runs of
length divisible by n (X y^(nm) -> y^((n+1)m) X). Direct replay confirms it: the swapped n=2 route on the official ac-00764 start
diverges at its first multiplication (move 2: total 20 instead of 14; by move 10 total 52). The n=3 route must first manufacture a
run of length >= 3 from w's letters, which needs two relators to interact non-trivially before any transport, and session 1's
cap-30 closure says that happens above total 30. I did not find such a block in this task; no level-map candidate for ac-00764,
ac-06036 or ac-02598 was produced, so nothing was replayed or repaired on those rows.

## Other attempts (scoped misses, all bounded)
- bidi_all.py (pure Python) on the n=1 made-up starts at cap 22, bound 24: both timed out at 300 s at depth F13+B7 = 20 (6.3M states):
  `n1_w_cap22.log`, `n1_w2_cap22.log`. No RESULT.
- acc_disk n=1 and n=2 at cap 26: killed after 11 / 14 layers (27M / 25M states, growing x2.2 / x1.7 per layer; disk 4.8 GB free).
- acc_disk n=1 for w' = YYxxyXXX at cap 22: killed at layer 24 (min_total 4) for disk headroom (`disk_n1_w2_cap22.log`).
- acc_beam via research/acc/optimality/run_beam_raw.py on ac-00764 and ac-06036, W=50000, DMAX=62, H=1, DIV=0.8, SEED=103, NOISE=2,
  420 s timeout: see `beam_n3.log` / `beam_n3_out.jsonl` (ac-00764: nopath in 79 s).
No verified path on any official unsolved row. `lines.txt` therefore carries only the re-verified held ac-00766 routes (already held).

## Files
common.py (shim to the pinned verifier), bidi_all.py (copy of tools/acc/ms_pump/bidi_all.py), trace.py, swap.py, scan_layer.py
(decodes acc_disk layer keys: little-endian 128-bit), beam_targets.json, logs as named above.
