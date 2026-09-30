# t00138: interior helper generator (Stable move 14) vs our AC route + [16,15]

Rows: sac-03211 (record 52, ours 55 = AC 53 + 2), sac-02092 (record 50, ours 50 = AC 48 + 2),
sac-00282 (record 61, ours 61 = AC 59 + 2).  Contract paths re-verified with the pinned
official `verifier.stable_core.verify` under `sac-r8-v1` (all ok: 55 / 50 / 61 moves).

Kernel: the official `stable_core.apply_move` itself (it implements all 257 moves; 33 of them are
applicable at rank 3: ids 0-13, 23, 29, 30, 41, 42, 53-56, 137, 138, 149, 150, 161-166).
Every rebuilt path is checked with `stable_core.verify` (manifest limits).

## Prediction (written before running)

Null: no window of any of the three routes admits a one-helper replacement that saves >= 1
move, because everything a helper inserts into r0/r1 arrives wrapped in a g3 letter that can
only be cancelled by re-inserting the inverse content (right-multiplication by r2^{-1} or
inversion + right-multiplication), so the helper cannot net letters out of a relator.  A hit
would mean the g3-marker argument is wrong and 6650 boards at AC+2 are beatable.

## Step 1: exact all-pairs helper surgery (`helper_probe.py`)

For every pair of route states S_i, S_j (i < j; S_0 = start, S_n = the single-letter pair
before the tail) and additionally for the 8 canonical single-letter finals of the spec's
canonicalization table (finish cost 2/3/4), search exactly for

    14  B  destab    with B rank-3 moves, |B| = L,

from S_i + (g3) to any rank-3 state that destabilizes to S_j: (g,) inserted at relator index
p in {0,1,2} with g in {x, y, g3} and S_j relabeled (so the destabilize may drop the helper
OR drop x or y as a generator substitution).  Rank-2 moves before the stabilize / after the
destabilize commute with them, so this form is WLOG for exactly one helper.  Meet in the
middle: forward BFS depth DF from S_i + (g3), backward BFS (inverse moves) depth DB from
the 9 lifts of S_j; L = d_f + d_b.  A pair "saves" (j - i) - (L + 2) (finals: (n - i + 2) -
(L + 2 + finish)).  Relator-total cap: forward states <= tot(S_i)+1+8, backward states
<= tot(S_j)+1+8 (SLACK = 8).

Depth 3+3 (L <= 6; replacement cost <= 8, so every window of length <= 9 is searched
exhaustively for a saving, windows of length 10..n only for replacements of cost <= 8):

| row | route states | pairs checked (incl. 8 finals x i) | savings >= 1 | wall |
|---|---|---|---|---|
| sac-03211 | 54 | 1855 | 0 | 154 s |
| sac-02092 | 49 | 1560 | 0 | 143 s |
| sac-00282 | 60 | 2242 | 0 | 157 s |

Logs: `sac-XXXXX_probe_df3_db3.log`.  Forward sets had 4.4K-12.6K states per S_i.

Depth 4+4 (L <= 8; windows of length <= 11 exhaustive): see the `*_probe_df4_db4.log`
files and the section "4+4 outcome" below for exactly which targets j were finished
before the wall.

The rebuild+verify branch of the script was exercised on sac-02092 with SAVING_MIN=-2
(scratch, not an artifact): 9 pairs with L=1..2 were rebuilt, all `ok: True` at 52 moves
(= ours + 2, as the arithmetic predicts), e.g. `[14, 5, 17, 1, 4, ...]`.

## Step 2: repeated blocks (`route_blocks.py`, output in `route_blocks.out`)

- sac-03211: conjugation runs 12x4, 12x3, 13x4, 8x3 (all length <= 4, each inside an
  exhaustively searched window); repeated block [4,12,11]x3 at positions 21..27 (length 7,
  inside an exhaustive window); one length-8 subword (2,2,2,1,-2,-2,-2,-2) present at move 4,
  absent, rebuilt at move 22 (the window 4..22 is length 18: only replacements of cost <= 8
  (3+3) / <= 10 (4+4) were searched for it, i.e. a helper route through it of length 11..17
  is NOT excluded).
- sac-02092: no conjugation runs, no repeated block of length >= 4, no rebuilt length-8 subword.
- sac-00282: no conjugation runs; the tail is twelve consecutive `2` (r0 <- r0 r1 with r1 a
  single letter: stripping y^12 one letter per move, total 14 -> 2); block [8,4] twice.

No helper insertion at a repeated block was found by hand; the exact search covers every
such insertion whose interior is <= 6 (3+3) or <= 8 (4+4) rank-3 moves.

## Step 3: exponent register (sac-03211, and the y^12 tail of sac-00282)

No Stable move multiplies a relator by itself or by a power, and r2 after stabilize is the
bare letter g3; the only way to load r2 with y^m is m right-multiplications by a relator equal
to y^{+-1} (or m conjugations, which give y^m g3 y^-m, a commutator relation, not y^m).  So a
register holding y^m costs >= m moves to fill, and its content enters r0/r1 only as
(a g3 b)^{+-1}, whose g3 must be cancelled by the inverse content.  On the actual states:
sac-03211's runs are length 3-4 and were searched exhaustively (windows <= 9 at 3+3, no
saving); the twelve `2`s of sac-00282 (state (x y^-12, y) -> (x, y)) sit in a window of
length 12 + tail 2 = 14, searched only for replacements of cost <= 8 / <= 10.

## What this does and does not exclude

Excluded (exact): on these three routes, a single stabilize/destabilize pair (helper g3 or
generator substitution dropping x/y) whose interior has <= 6 rank-3 moves (3+3) / <= 8
(4+4, for the targets listed below) under the relator-total cap tot+1+8, on any window
between two route states or from any route state to any canonical final.

NOT excluded: interiors longer than the searched depth; two or more simultaneous helpers
(rank 4..8); relator totals above cap; routes that leave our AC path's states entirely
(a different AC route plus a helper); the long rebuilt-subword window 4..22 of sac-03211 and
the y^12 tail of sac-00282 for replacements of cost > 10.

## 4+4 outcome

The depth 4+4 pass was started on all three rows (sac-02092 first, then sac-03211 and
sac-00282 with an 840 s timeout) but was killed at the wall before ANY backward target
finished: sac-02092 built its 49 forward sets (45K-165K states each, 55 s) and spent ~13 min
inside the first backward targets; the other two had only just finished their forward sets
on the shared 4-core box.  So the 4+4 pass contributes NO coverage; the exact claim of this
task is the 3+3 one (L <= 6, replacement cost <= 8, all pairs, all three rows).  Partial
stdout of those runs: `sac-XXXXX.df4db4.out`; their logs `sac-XXXXX_probe_df4_db4.log`
contain headers only.

## Result

No Stable path shorter than our AC best + 2 was found on any row; `lines.txt` is empty.
A rerun worth doing: the same script at 4+4 or 5+4 in a compiled kernel, or on the two
specific long windows named above.
