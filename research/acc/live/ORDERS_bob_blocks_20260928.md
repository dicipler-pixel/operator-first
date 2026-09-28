# Orders for Bob: block splice (22:20Z, from session 1). Your block style, used where it can win.

Why this job: your move-rhythm study showed blocks are real (tandem repeats 589 vs 365, core macro 4,.,2,5,2).
Session 3 then showed your 30 macros do not help *as beam moves* (ac-07790: 58 = plain 58). So use blocks **after**
the search, to shorten near-miss paths: replace a stretch of a path with a shorter chain of library blocks that
reaches the same state. The move-by-move window shortener stops at ~14 moves; a block vocabulary can bridge 20-40.

## Input (one file, self-contained)
`research/acc/live/bob/bob_blocks_bundle_20260928.json`:
- `near_misses` (40): rows where our best path is 1-3 moves over the record, held by <= 4 teams; each has `start`
  (official relators, letters x=1, X=-1, y=2, Y=-2), `moves` (our path, SAIR ac-r2-v1 ids 0-13), `record`, `teams`.
- `record_paths` (250): our paths that are at record length (the block source).
- `block_library` (1,619): blocks of 3-10 moves that occur >= 3 times in record paths, with counts.
If you cannot reach the repo, the user will relay this file to you.

## Method
For each near miss, for each window [i, j) of the path with j - i between 8 and 40:
  let A = state after i moves, B = state after j moves;
  search A -> B with steps = single moves (0-13) or whole library blocks, cost = number of primitive moves;
  accept a replacement of cost < j - i (bidirectional search from A and B meets fastest).
Apply the best replacement, repeat until no window improves. Moves are state-dependent, so always apply blocks to the
actual state; never assume a block's effect.

## Checking and output
- Replay every shortened path with the official SAIR core (a0fd6e6, `competition/tools/verifier/core.py`,
  `apply_move`) from `start` to ((1,),(2,)).
- Length <= record: send `ac-NNNNN: [..]` (to the inbox if you can push; otherwise to the user). A Stable line is the
  same path + [16, 15].
- Any improvement at all (even above record): report row, old, new. Shorter roads help the pool.
- Every hour at :55 UTC: one line (rows done / 40, hits, improvements) in `research/acc/live/WORKING_bob.md` or to the user.
Order: the bundle is sorted by gap to record then by teams, so the first rows are worth the most.
