# What Bluepug (ACC01-T00156) does: study from public scores (22 Nov 2026)

**Data:**
- Bluepug's scoring rows on both boards, pulled 15:09Z (`teams/bluepug_20261122T1509Z.json.gz`).
- Their 16 Oct rows (`teams/us_bluepug_20261016T0725Z.json.gz`).
- 112 saved leaderboards (`teams/lb_series_*.json`).
- Today's live boards.

**Caveat:** we cannot see their roads, only which rows they hold, at what length and with how many teams.

## 1. Timeline
- They first appear on 14 Oct: rank 5, AC 211, 3,169 rows.
- On 16 Oct: rank 3 on AC (457), rank 2 on Stable (562).
- By 14 Nov they were #1 with AC 1,319 and Stable 2,287.
- Today: AC 1,472 (6,919 rows), Stable 2,424 (7,308 rows). Next team: memcon.ai, AC 406 and Stable 224.
- They are still climbing: from 14 Nov to today, records fell on 314 AC rows (3,200 moves saved) and Bluepug is now alone on 221 of them. On Stable, 339 rows fell (2,993 moves) and they are alone on 310.

## 2. Breadth: they match or beat the record almost everywhere
- They hold the record on 6,919 of 7,443 solved AC rows (93%) and 7,308 of 7,443 Stable rows (98%).
- Their solo rows are not one family. The start-length quartiles of their solo rows (26/29/33) match all solved rows (25/29/32). It is a general pipeline run on every row.
- Points: AC 1,081 from 1,081 solo rows, the rest from k2 (482 rows) and up. Stable 2,122 from 2,122 solo rows.
- Their solo rows are long. AC record quartiles 85/111/193, against a median of 59 over all solved rows.

## 3. Stable: they use the extra generators (stabilize, rank above 2)
On rows they hold on both boards: their AC road + 2 minus their Stable road.

| AC road length | rows | median saving | share saving >= 8 | Stable/AC ratio (median) |
|---|---:|---:|---:|---:|
| < 40 | 1,051 | 0 | 0.00 | |
| 40–80 | 4,249 | 0 | 0.01 | |
| 80–150 | 1,134 | 3 | 0.40 | 0.96 |
| 150+ | 449 | 69 | 0.91 | 0.74 (150–300), 0.60 (300+) |

- If the saving came only from finishing at rank 2, they would have carried it over to AC. A saving of 8 or more (915 rows, about 900 Stable points) means the road goes above rank 2.
- The saving grows with length: 26% on 150–300-move roads, 40% on 300+.
- We have never used moves 14 and up, except the final destabilizes [16,15].

## 4. Where we stand
- We have a solution on 757 AC and 763 Stable rows. All are short rows shared by many teams, which is why our score is 0.11.
- We have submitted on only 7 of their 1,081 AC solo rows and 7 of their 2,122 Stable solo rows.
- A tie on one of their solo rows pays 0.25, more than our whole AC score. A beat pays 1.0.
- 524 solved AC rows are not Bluepug's: 440 are held alone by others (long, median 128; memcon ladders are among them). There are 2,672 unsolved AC rows, with no first solves on the whole board since 14 Nov.

## Lessons
1. The points are on long rows. Short rows are saturated, so polishing ties there cannot move our score.
2. Bluepug wins by running one strong general long-row shortener on every row, and keeps improving it (about 20 points a day on AC).
3. On Stable they use stabilization, which is worth 25–40% on long roads. That is a concrete technique gap we can close.
4. Others still beat them on 440 AC rows (structured families such as memcon's doubling ladders). A specialised construction can beat a general pipeline.

## 5. Gap test (tools/acc/bluepug_gap.py, results in research/acc/bluepug/)
- Our C beam (standard config: H, DIV 0.8, QUOTA 16, ELITE 5000, DUAL 0.75), width 5000, depth up to 2 × record, on 18 random rows Bluepug holds alone (6 each with records 80–110, 110–160 and 160–260).
- **We found a road on 1 of 18 rows.** On ac-00700 we got 111 against their 86 (rank-2 Stable 113 against their 73).
- On the other 17, the beam's shortest state stays at about 16–21 letters for 80+ moves and never reaches the finish table. These rows need the words to grow before they shrink, and our beam cannot get over that hump. Bluepug can.

## 6. Where Stable beats AC: the BS(n, n+1) family
- r1 = Y^(n+1) X y^n x, i.e. x⁻¹ yⁿ x = yⁿ⁺¹ (the Miller–Schupp first relator). 2,372 rows, n = 2..10.
- For a fixed r0, AC records grow by about ×1.7 per step in n. Stable records grow by about +125 moves per step: **linear, not exponential**.

| r0 | n=7 | n=8 | n=9 | n=10 |
|---|---|---|---|---|
| YXyXyx | 233 / 180 | 383 / 282 | 641 / 407 | 1122 / 534 |
| YXYxyX | 240 / 168 | 396 / 284 | 635 / 414 | 1117 / 542 |
| YYxyXYx | 249 / 195 | 403 / 296 | 659 / 424 | 1141 / 551 |

(Each cell is AC / Stable.)

- This family gives Bluepug 188 AC points and 333 Stable points. Their other Stable savings are spread over rows of 80+ moves.
- The literature says Miller–Schupp presentations are stably AC-trivial (Myasnikov–Myasnikov–Shpilrain, arXiv math/0302080; Shehper et al., arXiv 2408.15332, Thm 7; AK(3) stably trivial, arXiv 2501.18601). The linear growth fits a uniform one-stabilization construction.
- Not yet read: arxiv.org is blocked from this session's tools.

## 7. Blind extra-generator beam (tools/acc/stab_beam.py)
- A length-ranked beam that may stabilize to rank 3, against the same beam at rank 2, on ac-00700 at width 300.
- Both get stuck at about 18 letters. The search spends its width on rank-3 states, but extra letters alone do not get it over the hump.
- The saving needs the specific construction, not blind search.
