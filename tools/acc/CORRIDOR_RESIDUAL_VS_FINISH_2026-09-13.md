# Penultimate eye — residual vs finish, 2026-09-13

Definitions (per official training path, all replay via the official verifier):
- **residual** = moves before the earliest corridor state (exactly one relator a single letter);
- **official tail** = moves the training solution spends after entry;
- **exact finish** = shortest finish found by BFS from the entry state, capped at total length L_entry + cap
  (cap 0 = never above the entry length; cap 2 = up to two letters above).

## Aggregate (424 runs), min / median / max

| quantity | value |
|---|---|
| path length | 7 / 26.0 / 159 |
| residual (before corridor) | 2 / 18.0 / 152 |
| official tail | 1 / 7.0 / 17 |
| exact finish, cap 0 | 1 / 4.0 / 10 |
| exact finish, cap 2 | 1 / 4.0 / 10 |
| share of the finished path that is finish (cap 2), mean | 0.215 |
| runs where cap 0 already finishes | 424 / 424 |
| moves saved, cap 0 / cap 2 | 918 / 950 |

## By entry length L_entry (cap 2)

| L_entry | runs | residual median | official tail median | exact finish median | saved total |
|---:|---:|---:|---:|---:|---:|
| 3 | 76 | 11.0 | 5.0 | 3.0 | 88 |
| 4 | 118 | 23.5 | 7.0 | 4.0 | 308 |
| 5 | 174 | 27.0 | 7.0 | 5.0 | 403 |
| 6 | 31 | 12 | 9 | 7 | 85 |
| 7 | 6 | 7.0 | 9.5 | 8.0 | 9 |
| 8 | 13 | 6 | 11 | 8 | 41 |
| 9 | 5 | 6 | 12 | 9 | 14 |
| 10 | 1 | 14 | 12 | 10 | 2 |

## By path length (cap 2)

| path length | runs | residual median | exact finish median | finish share mean |
|---|---:|---:|---:|---:|
| 0–15 | 81 | 8 | 4 | 0.358 |
| 16–30 | 163 | 14 | 5 | 0.270 |
| 31–60 | 131 | 34 | 4 | 0.119 |
| 61–200 | 49 | 73 | 4 | 0.055 |

## Reading

- The corridor is cheap and nearly constant: exact finish median 4 moves whatever the path length, and it
  never needs to rise above the entry length (cap 0 finishes all 424). Residual grows with path length;
  finish does not. Cost sits **before** the corridor.
- The official solutions overspend only in the tail (median 7 vs 4). That is the whole 950-move saving.

## What this says about ac-00015 (inference, not a new computation)

Finish bound: from any corridor state of total length L, rotate-and-cancel is length non-increasing and
ends at (x^±1, y^±1); the only step that can rise is the final swap when the single letter sits in the
wrong slot, peak 4. So the target is reachable with peak ≤ max(L, 4). The training set agrees (cap 0,
424/424; max BFS nodes 2,852).

Certified fact from the length-well lane: the second well of ac-00015 (from the length-20 state) is
closed through cap 30 with 9,096,912 states and does not reach the target. If that component contained
any corridor state s, the bound gives a finishing path with peak ≤ max(L(s), 4) ≤ 30, so the target would
be in the component. Therefore **the cap-30 second well of ac-00015 contains no corridor state**. For
ac-00015 the corridor is not where the cost sits; the cost is reaching any corridor state at all, which
requires leaving the well above length 30. This is an inference from the certified closure plus the
finish bound; it has not been re-checked by scanning the 9M-state well for single-letter relators, and
should be, on the lane that holds the well dump (PR 44 / PR 47 frontier work).

## Handoff caveats (from the war-room reply, adopted)

1. All savings above are measured on training paths, which are near-monotone descents. Corridor
   shortening on the scored pool is untested: this repository holds no verified ac- candidate path yet,
   so no scored instance has been through the finisher.
2. Submission format rule (official README lines 48–52): the first verifying line per ID is selected and
   later lines for that ID are skipped even if shorter; later uploads can improve the record. A shortened
   path must therefore go in a **new upload**, never appended below the old line. The finisher always
   writes a fresh file.
3. Stable AC is a separate board with the same rule; `acc_finisher_sac_v1.py` is the counterpart
   (257 moves, empty-presentation target, corridor = some relator a single letter). Stable-training control:
   424 official stable solutions, 370 shortened, 53 kept, 1 hit the BFS node limit (kept unchanged), 1,320 moves
   saved, every output line re-verified by the official sac-r8-v1 verifier, 184 s.
