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

## 2. T1 is fully intact — and the cap discipline that built it was wrong

All **502** T1 rows are still `status: unsolved`, `kTeams: 0` on the 09-16
board. Four days, zero taken. Board-wide only 58 of 2730 unsolved rows fell.
First verified path on any T1 row still takes the full point, uncontested.

The reason the T1 search found nothing is the cap. T1 searched to `len+8`.
Measured against solved rows of the same initial length:

| `\|r\|` | solved rows | record ≤ `len+8` | ≤ 30 | ≤ 50 | median record |
|---|---|---|---|---|---|
| 15 | 38 | **0** | 8 | 33 | 40 |
| 16 | 54 | **2** | 5 | 33 | 48 |
| 17 | 70 | 7 | 13 | 50 | 39 |
| 18 | 79 | 6 | 6 | 52 | 40 |

At `|r|=15`, **not one** of the 38 solved rows has a record inside `len+8`.
The cap was set roughly at the all-time floor and about **3× below the
median** where solutions actually live.

So the forty "MS-open closure theorems at cap ≤ 15" and the eight family
disconnection results are sound as stated and near-vacuous as targeting
information: they prove no path exists in a band where, empirically, almost
no solved row has one either. They are not evidence these rows are hard. They
are evidence the search window was too narrow.

`tools/acc/ACC_T1_PRICED_v1.txt` reissues all 502 rows with `obs_min`,
`obs_med`, `obs_p75` columns — the observed record spread on solved rows of
the same `|r|`. **Search to `obs_med`, not `len+8`.**

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
