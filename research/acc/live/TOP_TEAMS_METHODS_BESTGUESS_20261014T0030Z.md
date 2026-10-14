# Top teams' methods: best guess from their scores (14 Oct 2026, 00:30Z)

**Data.** SAIR "team scoring challenges" for the AC top 3: memcon.ai 5,545 rows, AC-Solver =D 5,473, ACC01-T00118 5,167. Plus the live board (00:13Z) and our 6 Oct board.

**Caveat.** We cannot see anyone's roads. Everything below is inferred from which rows they hold, at what length, and with how many other teams.

## What the scores show

**1. The points are in long rows held alone.**

| | memcon.ai | AC-Solver =D | T00118 |
|---|---:|---:|---:|
| Score (AC) | 1016 | 840 | 504 |
| Rows held alone (k1) | 653 | 493 | 188 |
| Points from k1 rows | 653 | 493 | 188 |
| Solo rows <= 40 moves | 2 | 1 | 0 |
| Median solo-row length | 136 | 120 | 83 |
| Solo rows on MS ladders | 95 | 37 | 16 |

- Short rows are saturated. Everyone ties them, so a tie there pays < 0.002.
- The three teams overlap on about 4,400 rows each: the common rows everyone solves.

**2. The board moved a lot this week.**
- 1,685 AC records dropped between 6 and 14 Oct, saving 22,486 moves in total.
- memcon.ai is now sole holder of 651 of those rows, AC-Solver =D of 180 and T00118 of 137.

**3. memcon.ai has a new doubling-ladder construction.** It is sole holder on every rung we track, on all five Miller–Schupp ladders. Best record per rung:

| n | XXYxy | XYXYxy | XYYXyxY | XYYXYxy | XYXyxY | 2^n |
|---|---:|---:|---:|---:|---:|---:|
| 6 | 124 | 136 | 148 | 151 | 135 | 64 |
| 7 | 221 | 233 | 247 | 249 | 233 | 128 |
| 8 | 406 | 420 | 434 | 437 | 420 | 256 |
| 9 | 710 | 726 | 740 | 743 | 724 | 512 |
| 10 | 1332 | 1348 | 1364 | 1367 | 1347 | 1024 |

- On 6 Oct the n = 10 records were 2,071–2,106. Ours and the public construction (P000013, BS doubling) cost about 2^(n+1) + small.
- Every rung of every ladder now fits **record ≈ 2^n + c · 2^(n/2), with c ≈ 9 to 11**. Checks of (record − 2^n) / 2^(n/2):
  - XXYxy: 7.5, 8.2, 9.4, 8.8, 9.6;
  - XYXYxy: 9.4 to 10.2.
- **Best guess:**
  - They halved the main term. Each doubled letter now costs about one move instead of two (the multiplication without its separate rotation).
  - The rotations are paid once per block of about √m letters, giving the 2^(n/2) term. This is a two-scale (baby-step / giant-step) arrangement of the same rewrite y⁻¹xy = x².
  - P000013 noted that an m + O(1) finish would give about 1.5 · 2^n. memcon went further, to about 1 · 2^n.

## Per-team guess

- **memcon.ai (#1).** A better construction on structured families (the ladder law above), plus a long-row shortening pipeline on everything else. Their solo rows are long (median 136, record about 4.7 × start length), which fits construction seeds polished by exact local re-optimization.
- **AC-Solver =D (#2).**
  - The name points to the public AC-Solver code (Shehper et al. 2024: greedy and BFS search, PPO policy, path "supermoves").
  - They have 493 solo rows (median 120) but few ladder rows (37). That fits a strong generic, possibly learned, search on mid-long rows, without the new ladder construction.
- **ACC01-T00118 (#3).** Mid-length specialist: solo median 83, record about 2.8 × start length (the lowest of the three), and many 3–5-team ties. Probably a strong beam or exact hybrid on 40–150-move rows.

## What it means for us

1. Our points from shared short-row ties are near zero by design: 472 of our 496 AC rows have k >= 10. The payoff is on rows with 1–2 teams.
2. **Highest-value research target: rebuild the 2^n + ~10 · 2^(n/2) ladder construction.**
   - memcon holds 95 solo rows on MS ladders. A tie pays 0.5 each and a beat pays 1.0.
   - We already have the exact ladder tools in `research/acc/live/sweeps/ladder_law/` (loop_bidi, loop_macro, join_bidi, frame finishes).
   - Plan: search the small rungs (n = 3–5) for loops that leave our restricted model (r1 is multiplied; blocks are rotated together). Read off the block structure, then extend it like loop_macro.
3. For the few-team over-record rows (Bob's list and the sub-agent's 18 rows), keep shortening our own roads. Those pay 0.25–0.5 per tie.

## Addendum 00:55Z: where memcon's ladder gain sits (UPG-H)

**1. One construction, five ladders.** On every rung, the other four ladders sit a near-constant amount above XXYxy:
- XYXYxy: +11 (n=5), +12, +12, +14, +16, +16 (n=10);
- the other three ladders: about +15 to +35.
- So they build one construction and convert each ladder to it with a fixed-cost opening. Our `join_bidi` does exactly this kind of join.

**2. The gain looks like it is in the finish.** Suppose they keep a doubling loop like ours, which costs about 2m with m = 2^(n-1). Then their finish costs:

| n | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|
| Their finish (est.) | 35 | 52 | 83 | 139 | 185 | 294 |
| As a multiple of √m | 8.8 | 9.2 | 10.4 | 12.3 | 11.6 | 13.0 |
| fin2 = 2m + 11 | 43 | 75 | 139 | 267 | 523 | 1035 |

That shape fits a baby-step / giant-step finish:
- first build a "block rule" that halves x^(2k) to x^k in one multiplication, at a cost of about k;
- then apply it about m/k times, for a total of about √m.

**3. Probe.** A plain beam (W 200k) from our pre-finish state at m = 16 finds no finish at all, not even fin2's 43. A beam will not discover this; it needs a constructed finish.

**Open question to solve next:** an AC-move schedule that turns r1 = x x Y X y into a k-block rule, using r0 as the helper, at a cost of about k. AC moves cannot multiply r1 by itself, so r0 must carry the intermediate.
