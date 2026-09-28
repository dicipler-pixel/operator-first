# Where the points are (board 20:23Z, session 2, 2026-09-28 21:00Z)

Scoring (rules/discovery.md): the k teams on a record each get 2^(1-k). Our tie on a k-team record = 2^-k; a beat = 1.0.
"Tie value" below = the sum of 2^-k over the rows (AC side only unless marked; the Stable line usually doubles it).

## 1. Pool sizes (rows we do not hold)
| Pool | Rows | Tie value | k=1 / k=2 / k=3 | Status |
|---|---:|---:|---|---|
| AC 1 over our best | 20 | 3.3 | 4 / 2 / 5 | escalation (esc + new esc2) |
| AC 2 over | 15 | 3.8 | 6 / 2 / 1 | **new: esc2** (gap 2, k<=3) |
| AC 3-4 over | 39 | 6.7 | 5 / 9 / 13 | ranked lanes rk1/rk2 |
| SAC = AC+1, we tie AC (need (y,x) route AC-1) | 9 | 1.9 | 3 / 0 / 2 | session 1 + Charlie (exact) |
| SAC = AC+1, our AC 1-2 over | 9 | 3.3 | 5 / 2 / 2 | yx lanes, esc2 |
| SAC 1-2 over | 27 | 4.3 | 5 / 4 / 2 | esc / esc2 |
| **AC no path, record <= 40, never tried** | **494** | 4.2 (10.9 with SAC) | 0 / 0 / 0 (all k>=4) | `targets_fresh_easy_20260928T2100Z.json` |
| **AC no path, record 41-49, never tried** | **593** | 46 (**89.8** with SAC) | 0 / 88 / 116 | `targets_fresh_value_20260928T2100Z.json` |
| Solo-held (k=1) records >= 50 | ~3,300 | ~1,650 | all k=1 | **out of reach** (probe 0/12, ac-01262 no path at d=160) |
| Board-unsolved | 2,672 | 1.0 each | - | open MS classes (our beam 0/126, SURF 0/124) |

## 2. What actually produced hits (our logs)
- Re-running the *same* beam on a row we already sit 1-4 over: 0 hits in ~400 re-runs.
- Every hit today came from a method the row had not seen yet: the (y,x) finish (sac-08429, sac-03771), two eyes
  (ac/sac-02275, 06094, 04191), mirror twin + two eyes (ac/sac-05818 from 36), the yx twin on a near miss (sac-07792, esc).
- By record length: hits concentrate at records 30-39; 0 of 193 AC runs on k=1 rows hit.

## 3. So the ranking of lanes
1. **Near misses x a method not yet tried on that row** (mirror, yx, yx2, two eyes): esc (gap 1, k<=2) and esc2 (gap 1-2,
   k<=3, helpers' sweeps included) run this automatically.
2. **Fresh value pool** (593 rows, records 41-49, k=2..4+, never tried, value 0.13-0.75 per row with SAC): two-eyes screen,
   then escalate anything within +2. Free for any helper who finishes a list.
3. **Fresh easy pool** (494 rows, records <= 40, k>=4): highest hit rate, lowest value (~0.02 per row). Cheap W=4000 screen.
4. Not worth CPU: stabilization (only 108 rows have SAC <= AC), solo long rows, unsolved rows, bigger P2 cache.
