# Priced audit — the 09-16 board against this session's claims

Source: `acc-discovery-txt-v2`, `generatedAt 2026-09-16T04:15:00Z`,
`totalCount 10115`, `published: true`. Compared against the 09-12 board
(same contract, which additionally carried `initialRelators`, so initial
relator length `|r|` below is measured from it).

---

## 1. The fourteen certificates, re-priced

The earlier audit valued all fourteen at zero using the test *"the row is
solved."* That test is wrong: it does not separate **solved** from **solved
at or below the record**. Re-run against `currentBestLength`:

| challenge | mine | record 09-16 | k | record 09-12 | k | verdict |
|---|---|---|---|---|---|---|
| ac-00104 | 22 | 21 | 3 | 22 | 7 | worse by 1 |
| ac-00286 | 53 | 26 | 2 | 29 | 2 | worse by 27 |
| ac-01635 | 8 | **8** | 29 | 8 | 17 | **ties record** |
| ac-03919 | 61 | 27 | 3 | 29 | 1 | worse by 34 |
| ac-04308 | 23 | 21 | 3 | 22 | 2 | worse by 2 |
| ac-04359 | 17 | **17** | 14 | 17 | 6 | **ties record** |
| ac-05406 | 67 | 31 | 2 | 32 | 2 | worse by 36 |
| ac-06500 | 15 | **15** | 19 | 15 | 12 | **ties record** |
| ac-07445 | 13 | **13** | 21 | 13 | 12 | **ties record** |
| ac-08327 | 17 | **17** | 8 | 17 | 4 | **ties record** |
| ac-08491 | 8 | **8** | 28 | 8 | 17 | **ties record** |
| ac-08651 | 58 | 29 | 2 | 33 | 2 | worse by 29 |
| ac-09594 | 15 | **15** | 17 | 15 | 10 | **ties record** |
| ac-09868 | 25 | **25** | 5 | 25 | 2 | **ties record** |

**Eight tie the standing record, six are worse, none beat.** Scoring value is
still zero — the conclusion survives — but the reasoning that produced it did
not. The eight ties are record-length paths, not junk; they sit on saturated
rows (k rose on every one of them between the two boards) where the record is
very likely optimal. Three of the six misses were *at* record on 09-12 and
were passed since. Nothing here is submittable, and nothing here is wasted.

## 2. T1 is fully intact — but the cap claim below was a unit error

All **502** T1 rows are still `status: unsolved`, `kTeams: 0` on the 09-16
board. Four days, zero taken. Board-wide only 58 of 2730 unsolved rows fell.
A first verified path on any T1 row still takes the full point, uncontested.
That part stands.

> **CORRECTION (same day).** The first version of this section argued that
> the `len+8` cap "sits ~3x below where solutions live" because no solved row
> of `|r|`=15 has a `currentBestLength` inside `len+8`. **That compared two
> different units.** In `ac_corridor64_bidir_v2.c`, `CAP` bounds the *total
> relator length* of intermediate states (`if(lu+lb>CAP) return 0;`).
> `currentBestLength` is a *move count*. A 48-move path can live entirely
> inside a length cap of 24. The comparison proved nothing, and the
> recommendation it produced — "search to obs_med ≈ 48, not 24" — was wrong.
> `ACC_T1_PRICED_v1.txt`'s `obs_*` columns are move-count statistics and must
> not be read as cap advice.

The cap question was then settled properly, by calibrating the engine against
**solved rows used as ground truth** — rows where a path is known to exist and
its record move-count is published. Fourteen rows at `|r|`=16–20, bidirectional,
2M states/side, cap ladder `|r|+0 … |r|+16`:

| row | `\|r\|` | record | +0 | +2 | +4 | +6 | +8 | +12 | +16 |
|---|---|---|---|---|---|---|---|---|---|
| ac-00742 | 17 | 10 | **M10** | M10 | M10 | M10 | M10 | M10 | M10 |
| ac-01411 | 17 | 11 | **M11** | M11 | M11 | M11 | M11 | M11 | M11 |
| ac-10029 | 19 | 18 | **M18** | M18 | M18 | M18 | M18 | budget | budget |
| ac-06225 | 20 | 19 | **M19** | M19 | M19 | budget | budget | budget | budget |
| ac-07071 | 19 | 18 | CLOSED | **M21** | budget | budget | budget | budget | budget |
| ac-04275 | 19 | 21 | CLOSED | **M21** | M21 | budget | budget | budget | budget |
| ac-01059 | 19 | 22 | CLOSED | **M23** | budget | budget | budget | budget | budget |
| ac-10115 | 16 | 22 | M23 | M23 | M23 | **M22** | budget | budget | budget |
| ac-05170 | 19 | 15 | CLOSED | CLOSED | budget | budget | M17 | **M15** | budget |

Three things follow, and they invert the earlier advice:

1. **The engine reproduces published records.** On ground truth it finds paths
   at exactly the board's move count (M10, M11, M18, M19, M22). The search is
   sound; it is not missing easy solutions.
2. **The productive cap band is `|r|+0` to `|r|+6`** — narrow, essentially the
   original `len+8` discipline. That discipline was *right*.
3. **Widening the cap actively destroys the search.** Past `+6`, nearly every
   row collapses to `budget`: a larger cap legalises more moves, branching
   rises, and a fixed budget is spent at shallower depth. This confirms the
   independent finding already recorded in `ACC_PATH_LENGTH_BOUNDS_v1.md`
   ("for a fixed budget, a narrower cap reaches deeper").

The one genuine lesson is smaller and sharper than the wrong one: **a `CLOSED`
verdict at a single narrow cap is not final.** `ac-07071`, `ac-04275` and
`ac-01059` are all CLOSED at `|r|+0` and all solvable at `|r|+2`; `ac-05170`
is CLOSED at `+0` and `+2` and needs `+12`. Closure must be swept over a
ladder, not asserted at one cap.

## 3. The board is a shaving contest, not a solving contest

Between 09-12 and 09-16:

- **6909** of 7443 solved rows had their record cut — **927,344** total
  length shaved in four days.
- Only **58** rows moved unsolved → solved.
- Only **476** solved rows sat completely still.

Solving is rare and hard; shortening is happening at industrial scale. The
`kTeams` histogram says the same thing: 5269 rows have exactly one holder,
1437 have two, and the k ≥ 17 tail (63 rows) is all very short records — the
saturated region where the eight tying certificates sit.

**Steal candidates** are in `tools/acc/ACC_CHEAP_STEAL_v1.txt`, ranked by
`k` × bloat (`record/|r|`) × staleness. Tier A is 25 rows with a single
holder whose record has not moved in four days, led by `ac-01209` (record
134 on `|r|`=31, **4.3× bloat**), `ac-09619` (90 on 29), `ac-05923` (97 on
34), `ac-00699` (87 on 34). Tier C lists k=1 rows with records above 1000 —
enormous slack, but every one of them is being actively shaved, so a steal
there has a short half-life.

## 4. What changes

The earlier audit's bottom line ("SUBMIT NOW: NONE") is still correct. Its
diagnosis was not. It concluded the cheap regions had been *ruled out*; the
board says they were never searched. Two live routes, in priority order:

1. **T1 at a realistic cap.** 502 uncontested full points. Re-run the
   corridor search on the `|r|`=16–18 rows to `obs_med` (≈40–48), not 24.
2. **Tier A steals.** 25 single-holder rows sitting still with 1.2×–4.3×
   bloat. A steal needs only `record − 1`, and `ac-01209` has 103 moves of
   slack over its initial length.
