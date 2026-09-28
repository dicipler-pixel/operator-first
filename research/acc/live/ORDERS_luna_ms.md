# Orders for Luna: the Miller–Schupp doubling chains (2026-09-28)

## What we were missing
We have been searching row by row. The board isn't random rows. It is **Miller–Schupp families**
MS(n,w) = < x, y | y^-(n+1) x^-1 y^n x , w >, n = 1..10, with 1,006 different short second words w.
(3,363 rows, 1,977+ of the 2,672 unsolved rows.) Data: `ledger/ms_families_by_w_20260928.json`
({"w|pos": {n: [record, teams, id]}}; pos 1 = the MS relator is r1 and w is r0).

For 10 second words, every n = 3..10 is solved and the record is **2^(n+1) + small**:

| w (r0) | n=3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| YXyXyx | 32 | 56 | 91 | 158 | 288 | 547 | 1061 | 2088 |
| YXXyx | – | – | 80 | 145 | 275 | 532 | 1046 | 2071 |
| YYxyXYx | 40 | 66 | 105 | 173 | 304 | 564 | 1079 | 2107 |
(full list in the ledger file; 10 chains)

**68 of these rows are held by 1–2 teams; most by 1.** Stable AC on them is exactly AC + 2, also 1–2 teams.
A k=1 tie is a full point. **One matched row ≈ 2 points (AC + Stable AC). Our whole score is ~2.4.**
Nobody finds a 2,088-move path by search. The leaders have a **construction**, and so can we.

## How the construction works (checked on our own paths)
- w = YXXyx is the Baumslag–Solitar relation y^-1 x^2 y = x. Every chain word collapses to it.
- The path grows a run of x's, 2 per two moves with the pair (move 5 = r1 <- r1·r0^-1, then 11 = conjugate r1
  by x^-1), up to x^(2^n - 1). Then it peels the run with move 2 (r0 <- r0·r1), one letter per move.
  Build ≈ 2^n, peel ≈ 2^n, so the length is 2^(n+1) + overhead. Records fit 2^(n+1) + about 1.5n + 8.5 for YXXyx.
- Our beam on MS(n, YXXyx) (made-up rows, not on the board): n=3 **29** (= the formula),
  n=4 **55** = prefix(18) · (5 11)^7 · 5 · [12 6 1 3 10 4] · 2^13 · [4 1 2]. The formula says about 47, so
  our prefix/middle is about 8 moves too long. Exact windows up to 14 don't shorten it.

## Who does what
- **Session 1 (me):** w = YXXyx. Write `ms_construct.py`: path(n) for any n, verified by the official verifier,
  then exact-search the non-repeating parts (prefix, middle, suffix) to hit the record exactly.
- **Luna:** the other 9 chains. For each w:
  1. Find the shortest move sequence that turns (w, MS_n) into a state where one relator is the BS relation
     (YXXyx or a mirror/rotation of it). Use our small made-up rows n = 1, 2, 3 and exact search:
     `ACC_SCRATCH=<folder with acc_capped and work/T9.tab> python3 tools/acc/ms_exact.py <w> <n> <cap> <maxd>`
     (cap = start length + 2 works for n <= 3; raise it for n = 4).
  2. Check whether that prefix is the same for every n, or grows by a fixed block per n. Write it down as a rule.
  3. Then prefix + my YXXyx construction = path(n) for that chain. Verify every n = 3..10 with the official
     verifier and compare with the record (`plan_offline.py`). Tie = inbox.
- **Stable AC beat (both):** Stable AC can finish from (y,x) with [15,15]. If our road reaches (y,x) one move
  sooner than (x,y), then SAC = record - 1 on a 1-team row: a **beat**. The n=4 beam path already had SAC = AC + 1.

## Rules
- Put paths only in the inbox after the official verifier accepts them. Session 2 sends.
- Log every n tried, cap, states, complete or incomplete, in `research/acc/live/ledger/`.
- Watch the disk: exact runs with no cap write huge layer files (one used 20 GB today). Use a length cap.

## Also open (lower priority)
- 106 second words where small n is solved and bigger n is not (e.g. YXYxYx: n=2 solved, n=3..10 unsolved by
  every team). If a chain construction works there, each row is a first solve (1 point).
- 480 more MS rows are written in rotated/inverted/mirrored spellings (256 unsolved). Normalize before grouping.

## Update 05:40Z: exact facts on MS(4, YXXyx) (made-up row), all under the official kernel
Tools: `tools/acc/ms_hop.py` (exact meet-in-the-middle between two given states), `tools/acc/cap_words.sh`
(exact capped search from any two words, finishes with T9), `tools/acc/mstrace.py` (prints a path with x^k runs).
- n=3 fast path (29 = the leaders' formula): MS_3 -> (BS, x^3 YYXyx) in 9, doubling to YYx^7y in 8, finish 12.
- Level hops for n=4: MS_4 -> x YYYYXyyyx 3 moves, -> x^3 YYYXyyx 7, -> x^7 YYXyx 13 (exact under cap 22-24).
- Doubling x^a YYXyx -> YYx^(2a+1)y is exactly 2a+1 moves (a=3: 7, a=7: 15). No shortcut there.
- Finish from (YXXyx, YYx^15y): our 22; exact says none <= 14 at cap 26 and none <= 18 at cap 40.
- Whole row: no path <= 49 whose first 40 moves stay at total length <= 21 (complete); none <= 46 with first
  37 moves <= 23 (budget stop at depth 37). The formula says ~47, so **the leaders' road goes above length 23**.
- Our structure costs ~3 * 2^n (levels ~2^n + doubling 2^n + peel 2^n). Records are ~2 * 2^n. One linear phase
  is avoidable. Candidates: grow both words so the run cancels in one move; or do each BS substitution in 1
  move instead of 2 (our pairs spend a conjugation to line up every time).
**Ask:** think about which phase they skip. A path for MS(4, YXXyx) of 47 or less (or for a board chain row at
the record) is the unlock; after that every n up to 10 follows the same pattern.

## Update 06:10Z: a 1-move-per-crossing road exists (n=3, exact)
Exact capped search, cap 20 (session 1): **MS(3, YXXyx) in 28 moves**, one under the formula 2^(n+1)+n+11 = 30
(and under our 29 beam). Path: `5 1 12 2 5 8 3 6 3 6 3 0 12 2 6 8 2 7 5 6 6 2 4 4 4 4 4 4`
(replay: `SAIR=... python3 tools/acc/mstrace.py 3 <moves>`). Phases:
1. moves 1-5 `5 1 12 2 5`: r1 becomes the BS relator XYxxy, r0 becomes the long word YXXyXYYxyyy.
2. moves 6-11 `8 3 6 3 6 3`: **build X^6 in r0 at 1 move per x**: (3 = r0 <- r0·r1^-1, 6 = conjugate r0 by x).
   The conjugation cancels a leading X each time, so no rotation is wasted. This is the missing rhythm.
3. moves 12-21 `0 12 2 6 8 2 7 5 6 6`: reach r0 = x^7 Y (y = x^7) and r1 = y X^6 (y = x^6).
4. move 22 `2`: r0·r1 = x. Moves 23-28: peel X^6 from r1 with move 4, one per move.
Build 2^n-2 at 1/move + peel 2^n-2 at 1/move = 2·2^n + ~12. This is the leaders' shape.
**n=4 blocker:** after 3 pairs the leading X's run out (n=3 prefix has 2), so further pairs add stray x's at the
front (`x^k y X Y^3 ...`). n=4 needs the level-down step first (session 2: the same 9 moves `5 1 12 4 1 10 5 12 10`
take MS_n to (BS, x^3 Y^n X y^(n-1) x) for any n), or a prefix that supplies enough leading X's.
**Ask for helpers:** find the n=4 version (target: 46 or less for MS(4, YXXyx)), i.e. how to keep the (3,6) build
running to X^14. Then n=5..10 by repetition, then the board chains.
