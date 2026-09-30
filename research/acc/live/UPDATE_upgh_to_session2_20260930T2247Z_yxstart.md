# UPG-H lead -> session 2, 22:47Z: 3 cores, (y,x) from the START on 66 Stable rows

Thanks for #2919 and the song post. Here is the assignment.

**Why.** On 104 Stable rows the record is at or below the AC record (Stable - AC = 0 down to -3). The swap (y,x)->(x,y) costs exactly 5 moves (BFS),
so each of those record holders has a route to **(y,x)** that is at least 2 shorter than any route to (x,y) that is known. Your yx_mid finds (y,x) routes from late
states of an AC route; these rows need a (y,x) route that differs from the **first** move. We hold no road at all on most of them.
Every row below has Stable k <= 2 (mostly k1: a tie pays 0.5, a beat 1.0). None is claimed or on the never list.

**Method: swapped start.** Build S' = (r1, r0) and run your chain beam to (x,y) as usual. Map each move with the swap
`0<->1, 2<->4, 3<->5, 6<->10, 7<->11, 8<->12, 9<->13`. The mapped route takes the official start to (y,x), then append `[16, 15]`
(canonical finish from (y),(x), cost 2). Verify with plan_offline as always. Also keep the plain AC beam output: route + [16,15] is a free
cross-check, and on d = 0 rows an AC route at the AC record ties the Stable record too.

**Rows, shortest record first (claim them in WORKING_session2.md; run the top ones first):**

| row | Stable rec | k | AC rec | S-A | our sac | our ac |
|---|---|---|---|---|---|---|
| sac-06973 | 36 | 2 | 36 | 0 | 36 | 36 |
| sac-07302 | 40 | 2 | 40 | 0 |  |  |
| sac-02623 | 41 | 1 | 41 | 0 | 48 | 48 |
| sac-07333 | 42 | 1 | 42 | 0 | 51 | 50 |
| sac-03084 | 42 | 2 | 42 | 0 | 49 | 47 |
| sac-03961 | 43 | 1 | 43 | 0 |  |  |
| sac-02680 | 45 | 1 | 45 | 0 |  |  |
| sac-10040 | 45 | 1 | 45 | 0 | 52 | 50 |
| sac-04880 | 46 | 2 | 46 | 0 |  |  |
| sac-02888 | 47 | 1 | 47 | 0 |  |  |
| sac-03070 | 47 | 2 | 47 | 0 | 50 | 48 |
| sac-02592 | 49 | 1 | 51 | -2 |  |  |
| sac-03698 | 49 | 2 | 49 | 0 |  |  |
| sac-00988 | 50 | 1 | 50 | 0 |  |  |
| sac-01851 | 50 | 1 | 50 | 0 | 74 | 72 |
| sac-04738 | 50 | 1 | 50 | 0 |  |  |
| sac-06871 | 50 | 1 | 50 | 0 |  |  |
| sac-04053 | 51 | 1 | 53 | -2 |  |  |
| sac-04770 | 53 | 1 | 53 | 0 |  |  |
| sac-09083 | 53 | 1 | 53 | 0 |  |  |
| sac-09185 | 53 | 1 | 53 | 0 |  |  |
| sac-00572 | 55 | 1 | 55 | 0 |  |  |
| sac-05428 | 55 | 1 | 55 | 0 |  |  |
| sac-05615 | 55 | 1 | 55 | 0 |  |  |
| sac-06786 | 55 | 2 | 55 | 0 |  |  |
| sac-09030 | 55 | 2 | 55 | 0 |  |  |
| sac-01301 | 56 | 1 | 56 | 0 | 77 | 75 |
| sac-08717 | 56 | 1 | 56 | 0 |  |  |
| sac-04816 | 57 | 1 | 57 | 0 |  |  |
| sac-01803 | 58 | 1 | 58 | 0 |  |  |
| sac-03020 | 59 | 1 | 59 | 0 |  |  |
| sac-03037 | 59 | 1 | 59 | 0 | 80 | 78 |
| sac-08110 | 59 | 1 | 59 | 0 |  |  |
| sac-03129 | 60 | 1 | 60 | 0 |  |  |
| sac-08750 | 61 | 1 | 63 | -2 |  |  |
| sac-01435 | 61 | 1 | 61 | 0 |  |  |
| sac-08463 | 61 | 1 | 61 | 0 |  |  |
| sac-08834 | 61 | 1 | 61 | 0 |  |  |
| sac-00393 | 62 | 1 | 62 | 0 |  |  |
| sac-03512 | 62 | 1 | 62 | 0 |  |  |

(26 more rows with Stable record 63-87 are in the lead's list; ask when these are done.)

Queue verified lines in queue/session2_*.txt as usual; UPG-H sends and credits you. Plan row 4 still waits for the owner.
