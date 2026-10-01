# FIRST-SOLVE TARGETS (UPG-H lead, 01:40Z 1 Oct): unsolved rows, a first solve pays 1.0 per track

**The pattern (song-2 idea #3, t00140, and the comb data):** in MS(n,w), the pump leaves r1 carrying a y-run of n-2 next to x.
When w has a y-run of the same length next to an x, the route gets a shortcut (the n=4 coincidence that made ac-08510 35 < ac-01432 41).
Validation on solved rows with n >= 4: when that match holds, the record drops BELOW the n-1 record in **7 of 15**; without it, in **2 of 51**.
So unsolved rows where the match holds are the best first-solve bets. Their routes should be near or below the n-1 record, not on the growth trend.

Method ideas: (1) template transfer across families at the same n: our n=4 'lucky' routes ac-08510 35, ac-08051 38, ac-09177 42 (phases: collapse r0 against
the y^n pump with n-1 conjugations, build r0 = (XY)^(n+1) Y and r1 = y (yx)^n, tail of n moves 4 then 2, 0; see artifacts/t00140/notes.md); (2) session 1's exact
bidirectional pump search (tools/acc/ms_pump/bidi.py) adapted to w; (3) a wide free beam with DMAX = rec(n-1) + 15; (4) a kernel or class splice from the n-1 route.

| tier | row | n | w | rec(n-1) | our n-1 road |
|---|---|---|---|---|---|
| A | ac-09310 | 4 | x^{-1}y^{-1}xy^{-2} | 26 | 26 |
| A | ac-07430 | 4 | yxy^{2}x^{-1}y^{2} | 30 | 30 |
| A | ac-08606 | 4 | y^{-1}xy^{-2}x^{-1}y^{-2} | 30 | 31 |
| A | ac-02234 | 4 | x^{-1}y^{-1}xy^{2} | None | None |
| A | ac-02190 | 4 | yxy^{-2}x^{-1} | None | None |
| A | ac-09811 | 4 | yxy^{2}x^{-1} | None | None |
| A | ac-02055 | 4 | yx^{-1}y^{-1}xy^{2} | None | None |
| A | ac-07206 | 4 | yxy^{-2}x^{-1}y | None | None |
| A | ac-06615 | 4 | y^{-1}xy^{-2}x^{-1}y^{-1} | None | None |
| A | ac-02401 | 4 | y^{-1}xy^{-1}x^{-1}y^{-2} | None | None |
| A | ac-00675 | 4 | yx^{-1}y^{-1}xy^{-2} | None | None |
| A | ac-09010 | 4 | y^{-1}xy^{2}x^{-1}y^{-1} | None | None |
| A | ac-04621 | 4 | y^{2}x^{-1}y^{-1}xy^{-1} | None | None |
| A | ac-00474 | 4 | yxy^{-2}x^{-1}y^{-1} | None | None |
| A | ac-02710 | 4 | yxyx^{-1}y^{-2} | None | None |
| A | ac-00273 | 4 | yxyx^{-1}y^{2} | None | None |
| A | ac-02571 | 4 | yxy^{2}x^{-1}y^{-1} | None | None |
| A | ac-06469 | 4 | yxy^{2}x^{-1}y | None | None |
| A | ac-03320 | 4 | yxy^{2}x^{-1}y^{-2} | None | None |
| A | ac-04515 | 4 | x^{-2}y^{-2}x^{2}y^{-1} | None | None |
| A | ac-03367 | 4 | y^{3}xy^{2}x^{-1} | None | None |
| A | ac-03131 | 4 | y^{3}xy^{-2}x^{-1} | None | None |
| A | ac-02598 | 4 | y^{2}x^{2}yx^{-2} | None | None |
| A | ac-05007 | 4 | y^{2}x^{2}y^{-1}x^{-2} | None | None |
| A | ac-07080 | 4 | y^{2}x^{-1}y^{-1}xy^{2} | None | None |
| A | ac-02415 | 4 | y^{2}x^{-1}y^{-1}xy^{-2} | None | None |
| A | ac-09632 | 4 | x^{-1}y^{-3}xy^{2} | None | None |
| A | ac-01335 | 4 | x^{-1}y^{-3}xy^{-2} | None | None |
| A | ac-05780 | 4 | x^{-2}y^{-1}x^{2}y^{2} | None | None |
| A | ac-06673 | 4 | x^{-2}y^{-1}x^{2}y^{-2} | None | None |
| A | ac-01449 | 4 | x^{-2}y^{-2}x^{2}y | None | None |
| A | ac-04923 | 4 | yx^{2}y^{2}x^{-2} | None | None |
| A | ac-08159 | 4 | y^{-1}xy^{2}x^{-1}y^{-2} | None | None |
| A | ac-08648 | 4 | yx^{2}y^{-2}x^{-2} | None | None |
| A | ac-01152 | 4 | yxy^{-2}x^{-1}y^{2} | None | None |
| A | ac-02912 | 4 | yxy^{-2}x^{-1}y^{-2} | None | None |
| B | ac-04707 | 5 | yx^{-1}y^{-3}xy^{-1} | 79 | 95 |
| B | ac-02958 | 5 | y^{3}xyx^{-1}y^{-1} | 82 | 103 |
| B | ac-08922 | 5 | x^{-1}y^{-3}xy^{-1} | 87 | 123 |
| B | ac-08676 | 5 | y^{3}xyx^{-1} | 90 | 131 |
| B | ac-00775 | 5 | y^{-1}x^{-1}y^{-3}xy^{-1} | 96 | None |
| B | ac-06799 | 6 | yxy^{4}x^{-1} | 97 | None |
| B | ac-09227 | 5 | y^{3}xyx^{-1}y | 100 | None |
| B | ac-03228 | 6 | x^{-1}y^{-1}xy^{-4} | 100 | None |
| B | ac-00532 | 6 | x^{-1}y^{-4}xy^{-1} | 137 | None |
| B | ac-04948 | 6 | y^{4}xyx^{-1} | 139 | None |
| B | ac-01316 | 5 | y^{3}xy^{-1}x^{-1} | None | None |
| B | ac-02032 | 5 | x^{-1}y^{-3}xy | None | None |
| B | ac-04074 | 5 | yxyx^{-1}y^{-3} | None | None |
| B | ac-05165 | 5 | yxyx^{-1}y^{3} | None | None |
| B | ac-06764 | 6 | y^{4}xy^{-1}x^{-1} | None | None |
| B | ac-01124 | 5 | y^{3}xy^{-2}x^{-1} | None | None |
| B | ac-01600 | 5 | y^{3}xy^{-1}x^{-1}y | None | None |
| B | ac-00480 | 5 | y^{3}xy^{-1}x^{-1}y^{-1} | None | None |
| B | ac-05953 | 5 | y^{3}x^{-1}y^{-1}xy^{-1} | None | None |
| B | ac-04866 | 5 | y^{-1}xy^{-1}x^{-1}y^{-3} | None | None |
| B | ac-05741 | 5 | y^{-1}x^{-1}y^{-3}xy | None | None |
| B | ac-06247 | 6 | x^{-1}y^{-1}xy^{4} | None | None |
| B | ac-05538 | 5 | x^{-1}y^{-3}xy^{2} | None | None |
| B | ac-00146 | 6 | x^{-1}y^{-4}xy | None | None |
| B | ac-01226 | 6 | yxy^{-4}x^{-1} | None | None |
| B | ac-05081 | 5 | yx^{-1}y^{-3}xy | None | None |
| C | ac-02842 | 3 | x^{-1}y^{-1}xy^{-1} | 21 | 21 |
| C | ac-01083 | 3 | yxyx^{-1}y | 24 | 24 |
| C | ac-00692 | 3 | y^{-1}xy^{-1}x^{-1}y^{-2} | 26 | 28 |
| C | ac-01399 | 3 | yxyx^{-1}y^{2} | 27 | 27 |
| C | ac-06257 | 3 | yxyx^{-1}y^{3} | 28 | 29 |
| C | ac-09217 | 3 | y^{-1}xy^{-1}x^{-1}y^{-3} | 28 | 31 |
| C | ac-06570 | 3 | x^{-2}y^{-2}x^{2}y^{-1} | 32 | 36 |
| C | ac-00764 | 3 | y^{2}x^{2}yx^{-2} | 33 | 34 |
| C | ac-06556 | 3 | yxyx^{-1} | None | None |
| C | ac-06672 | 3 | yxyx^{-1}y^{-1} | None | None |
| C | ac-03525 | 3 | y^{-1}xy^{-1}x^{-1}y^{-1} | None | None |
| C | ac-09350 | 3 | y^{2}xy^{-1}x^{-1} | None | None |
| C | ac-01558 | 3 | yx^{-1}y^{-1}xy^{-1} | None | None |
| C | ac-04300 | 3 | x^{-1}y^{-2}xy | None | None |
| C | ac-02976 | 3 | y^{2}x^{-1}y^{-1}xy^{-1} | None | None |
| C | ac-07881 | 3 | y^{2}xy^{-1}x^{-1}y | None | None |
| C | ac-07311 | 3 | y^{2}xy^{-1}x^{-1}y^{-1} | None | None |
| C | ac-05983 | 3 | yx^{-1}y^{-2}xy | None | None |
| C | ac-03301 | 3 | yxyx^{-1}y^{-2} | None | None |
| C | ac-02803 | 3 | x^{-2}y^{-1}x^{2}y^{-1} | None | None |
| C | ac-08284 | 3 | x^{-2}y^{-1}x^{2}y | None | None |
| C | ac-00056 | 3 | yx^{2}yx^{-2} | None | None |
| C | ac-08038 | 3 | yxy^{-3}x^{-1} | None | None |
| C | ac-05468 | 3 | yx^{2}y^{-1}x^{-2} | None | None |
| C | ac-03824 | 3 | x^{-1}y^{-1}xy^{3} | None | None |
| C | ac-07807 | 3 | y^{-1}x^{-1}y^{-2}xy | None | None |
| C | ac-00320 | 3 | yxyx^{-1}y^{-3} | None | None |
| C | ac-00773 | 3 | yxyxy^{-1}x^{-2} | None | None |
| C | ac-07971 | 3 | yxyxyx^{-2} | None | None |
| C | ac-05938 | 3 | y^{2}x^{-1}y^{-2}xy | None | None |
| C | ac-08692 | 3 | y^{4}xyx^{-1} | None | None |
| C | ac-08882 | 3 | y^{3}x^{-1}y^{-1}xy^{-1} | None | None |
| C | ac-02024 | 3 | y^{2}x^{2}y^{-1}x^{-2} | None | None |
| C | ac-01519 | 3 | y^{2}xy^{-1}x^{-1}y^{2} | None | None |
| C | ac-07270 | 3 | y^{2}xy^{-1}x^{-1}y^{-2} | None | None |
| C | ac-05616 | 3 | yx^{2}yx^{-1}yx^{-1} | None | None |
| C | ac-08344 | 3 | y^{-2}xyx^{-1}y^{-2} | None | None |
| C | ac-07958 | 3 | x^{-1}y^{-1}x^{2}yx^{-1}y^{-1} | None | None |
| C | ac-05894 | 3 | x^{-1}y^{-1}x^{2}y^{-1}x^{-1}y^{-1} | None | None |
| C | ac-00724 | 3 | x^{-1}y^{-4}xy^{-1} | None | None |
| C | ac-07338 | 3 | x^{-1}y^{-1}x^{-1}y^{-1}x^{2}y | None | None |
| C | ac-01502 | 3 | x^{-1}y^{-1}x^{-1}y^{-1}x^{2}y^{-1} | None | None |
| C | ac-07556 | 3 | x^{-2}y^{-1}xyxy | None | None |
| C | ac-00912 | 3 | x^{-2}y^{-1}xyxy^{-1} | None | None |
| C | ac-07247 | 3 | x^{-2}y^{-1}x^{2}y^{2} | None | None |
| C | ac-06505 | 3 | x^{-2}y^{-1}x^{2}y^{-2} | None | None |
| C | ac-00953 | 3 | x^{-2}y^{-1}xy^{-1}xy | None | None |
| C | ac-03495 | 3 | x^{-2}y^{-1}xy^{-1}xy^{-1} | None | None |
| C | ac-06036 | 3 | x^{-2}y^{-2}x^{2}y | None | None |
| C | ac-02146 | 3 | yx^{2}y^{2}x^{-2} | None | None |
| C | ac-00045 | 3 | yx^{2}yx^{-1}y^{-1}x^{-1} | None | None |
| C | ac-00164 | 3 | yx^{2}yx^{-2}y | None | None |
| C | ac-08064 | 3 | yx^{2}yx^{-2}y^{-1} | None | None |
| C | ac-06835 | 3 | yx^{2}y^{-2}x^{-2} | None | None |
| C | ac-08820 | 3 | yx^{2}y^{-1}x^{-1}yx^{-1} | None | None |
| C | ac-09020 | 3 | yx^{2}y^{-1}x^{-1}y^{-1}x^{-1} | None | None |
| C | ac-06185 | 3 | yx^{2}y^{-1}x^{-2}y | None | None |
| C | ac-01253 | 3 | yx^{2}y^{-1}x^{-2}y^{-1} | None | None |
| C | ac-01761 | 3 | yxy^{-1}xyx^{-2} | None | None |
| C | ac-05924 | 3 | yxy^{-1}xy^{-1}x^{-2} | None | None |
| C | ac-06663 | 3 | yxy^{-3}x^{-1}y | None | None |
| C | ac-09906 | 3 | yxy^{-3}x^{-1}y^{-1} | None | None |
| C | ac-05319 | 3 | yx^{-1}y^{-1}xy^{3} | None | None |
| C | ac-07231 | 3 | yx^{-1}y^{-1}x^{2}yx^{-1} | None | None |
| C | ac-02319 | 3 | yx^{-1}y^{-1}x^{2}y^{-1}x^{-1} | None | None |
| C | ac-01310 | 3 | yx^{-2}y^{-1}x^{2}y | None | None |
| C | ac-03393 | 3 | yx^{-2}y^{-1}x^{2}y^{-1} | None | None |
| C | ac-02910 | 3 | y^{-1}xy^{3}x^{-1}y^{-1} | None | None |

Same row number = the Stable twin (sac-) is also unsolved: a first solve there is AC path + [16,15], so 2.0 points per row.


**02:00Z cross-check with Bob's independent comb list (ms1190_metadata + training_424, `BOB_ms_comb_90` on Drive):** 11 of his open rows are also tier A here:
ac-02055, ac-02234, ac-02571, ac-03320, ac-03367, ac-07080, ac-08159, ac-08606, ac-09010, ac-09632, ac-09811. Two methods agree, so these come first.
Bob's 11 'uncertified' (literature-solved) comb rows are all solved on the board (records 83-139, mostly k1): ties, not first solves.

## 02:20Z reality check (deep scout + ms1190_metadata `reported_class`)
The official metadata groups the 550 open MS rows into **261 known AC-equivalence classes** (the Two-Hump paper's "550 -> 261"). Every tier A row is in an OPEN class:
**14_1** (36 rows; 12 of ours: 00474 01152 01335 02055 02190 02234 02912 03367 07080 07206 08159 09010), **15_1** (22 rows: 00273 02401 02710 04621),
**15_10 / 15_11** (9 rows each: 00675 02415 02571 03131 03320 06469 06615 07430 08606 09310 09632 09811), and 8 singletons of minimal length 19
(01449 02598 04515 04923 05007 05780 06673 08648). The class names give the minimal total relator length in the class: these are the literature's
hard frontier (length 13 = AK(3)'s class, 14, 15). **A first solve here would be a research result, not a search trick.** Keep a small share on it
(UPG-H's Fable builder, Charlie's exact search on short caps), but the team's main effort goes to **ties for rank** (`UPDATE_upgh_to_all_*_RANK.md`).
Upside if it ever lands: a solve of one row in a class makes the whole class reachable via the class equivalences (36 rows in 14_1).
The 8 singleton length-19 classes are the least studied; prefer those over 14_1/15_1 if you spend time on first solves.

## 02:58Z correction from Sol 6.1 (owner's outside model)
The official data README calls `reported_class` **non-normative**: it was computed under a different move metric. So the class labels (14_1, 15_x, 17_x, 19_x) do **not** prove
those rows are AC-equivalent under the competition's 14 moves, and they give no official bounds. "Open" (status_at_freeze) still means no known trivialization.
Known provable families (Shehper et al., arXiv 2408.15332v2, Theorem B): MS(1,w), MS(n, y^-1 x y x^-1), MS(2, y^-k x^-1 y x y). None of those is an unsolved scored row.
The lucky-n pattern is a predictor, not a theorem.
