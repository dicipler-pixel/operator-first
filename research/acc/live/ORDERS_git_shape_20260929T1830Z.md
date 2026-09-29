# ORDERS: Git (session 3) to any free lane, 2026-09-29 18:30Z: good-shape targets (192 rows, ~57 points)

**List: `research/acc/live/targets_git_shape_20260929T1830Z.json`.** These are AC rows we hold 1–5 over the record, nearest first:
50 rows at 1 over, 30 at 2, 34 at 3, 39 at 4 and 39 at 5. 63 of them are on no active list. AK(3)-class rows and the
owner's reserved rows are excluded. `sac_tie_free` marks rows where an AC tie also gives the SAC tie through + [16,15].

## Why these rows (the owner's Mixer 5.2, all 433 verified good runs loaded, 42 studies)
- Every good run has the same shape. κ (the relation) holds, then clears about 6 moves from the end. The exponent ledger climbs only
  a little (median +1 above its start) and peaks about 10 moves from the end, BEFORE κ clears. Scale rarely goes above
  its start (38% of good runs).
- Our longer paths break that shape, and they break it more the longer they are:

  | | good runs | 1–3 over | 4+ over |
  |---|---|---|---|
  | ledger climb (median) | +1 | +2 | +4 |
  | scale climbs above start | 38% | 54% | 59% |
  | ledger peaks after κ clears | 3% | 5% | 22% |

- Every row on this list has a best path of ours that misses at least one of the three traits (the list gives which ones).
  The reading is that a good-shaped road exists and our road is not it. Whether this closes rows is untested until the lanes run.

## How to run
1. Your current winning settings unchanged (two-eyes: H=1, DIV=0.8, P2=2, QUOTA=16, ELITE=5000, DUAL=0.75, DMAX = record + 2,
   BEAM_NOISE=2 seeds 11–14).
2. File order: not-on-active-list first, then nearest to record, then value.
3. Rows at 1–2 over are also candidates for window recovery and splice from our own path (`our_path_source`).

Return hits as usual: inbox lines `ac-NNNNN: [..]` / `sac-NNNNN: [..]`, official-core verified.
Never include ac-09839, ac-09311, ac-06403, ac-04718, ac-05378 or sac-02257 (the owner sends those).
A second list, for **unsolved** rows (first solves), follows when the twin run on all 2,672 unsolved rows finishes.
