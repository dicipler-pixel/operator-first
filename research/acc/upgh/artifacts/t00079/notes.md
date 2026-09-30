# t00079: MS(n, w = XYxYYY), first-solve template transfer from n=3 -- no full route; the template is n=3-only (proof below)

Starts (manifest a0fd6e6 `initial_relators`, verified): r0 = YYYXXYx for every row; r1 = MS(n) = Y^(n+1) X y^n x.
ac-08538 n=4, ac-03314 n=6, ac-02094 n=7, ac-09689 n=8, ac-06858 n=9, ac-07472 n=10 (all unsolved by every team);
ac-00028 n=3 (record 44, ours 52 -> Astra 51 at code_a7e9bffde8b90533), ac-07900 n=5 (record 38, 8 teams).
w = XYxYYY: r0 = X.w rotated (x = X Y x Y^3, i.e. y x^2 y^3 = x). MS-1190 csv (verifier data): this is w = x^{-1}y^{-1}xy^{-3},
rows 484-490: n=1 certified 20, n=2 certified 15, n=3 uncertified, **n=4 open class 14_1**, n=5 uncertified,
**n=6 open 17_{40}, n=7 open 19_{41}** (n=8..10 not in MS-1190). So n=4,6,7 sit in the MS-1190 open set, the
same status as AK(3) = 13_1; the team's rival notes record "class 14_1 none within 23 (158M states)".

## 1. Our n=3 route, phase by phase (replay: work/replay.py on the pinned core, 52 = Astra's 51 with one fewer build move)
- A (moves 1-12, r0-moves only, r1 = MS3 fixed): r0 YYYXXYx -> YXyxyyx.
- B (13-36, r1-moves only): MS3 -> y (yyx)^7 (22 letters, peak 27 during build).
- C+D (37-41): r0 <- r0.r1 = y (yyx)^8, three conjugations, r0 <- r0.r1^-1 = yyyxY.  E (42-52): conj to yyx, 7 peels (id 5), 6 3 3.
- Meaning: put z = y^2 x ("x = y^-2" reading). YXyxyyx = Y Z y z z in (y,z) letters, i.e. z^y = z^2: the BS(1,2) relator.
  MS(n) in (y,z) letters is Y^(n+1) Z y^n z (any n), and in BS(1,2) it equals y^-1 z^(1-2^n) (checked numerically for
  n=2..10 in the affine model, see transcript; y z^(2^n-1) is exactly the move-36 word for n=3, 2^3-1 = 7).
  So after phase A the presentation IS the MS(n, YXXyx) chain in the basis (y, z) (with y inverted): the family with
  Codex's constructive generator (research/acc/optimality/yxxyx_chain.py, 4*2^n+2-n moves; z-conjugation costs 3 letters).
  Phase B + collapse + peel is that chain's route in disguise (build 2^n-1 z's, peel them).

## 2. Why n=3 (and n=1) only: the phase-A conjugacy criterion
Phase A keeps r1 = MS(n) fixed, so the reachable r0 words are exactly the conjugates of r0^{+-1} in
BS(n,n+1) = <x,y | X y^n x = y^(n+1)>.  Every BS(1,2)-form of r0 in a basis (y, y^p x y^q) is (up to rotation/inverse)
one of the cyclic words T_m = x y X Y^m X Y or T'_m = x Y X y^m X y (m = p+q; m=2 is the route's YXyxyyx^-1).
All these and r0 are cyclically reduced HNN words with three stable letters, so Collins' criterion applies: the
y-runs between stable letters may only change by the transfers y^(k(n+1)) X = X y^(kn) and y^(kn) x = x y^(k(n+1)).
r0^-1 = X y x x y^3 has runs (1, 0, 3); T_m^-1 has (1, m, -1).  The x2..X run must move 3 -> -1 by multiples of
n+1, so **(n+1) | 4, i.e. n in {1, 3}**.  The mirror family T'_m needs n | 2 and (n+1) | 2: n = 1 only.
(Check on n=3: k1=k2=-1, k3=-2 solves it; and the route exists.)  Hence the x = y^-2 substitution template closes
for n = 3 only; it cannot close for n = 4, 6, 7, 8, 9, 10 with r0-moves alone.  That is the asymmetry.
Scope of the proof: r0-only phase A into a BS(1,2)-form in a basis (y, y^p x y^q). Routes that alter r1 first, or
BS-forms in other bases, are not excluded by it (only by the bounded searches below).

n=5 is a different coincidence (the IDEAS.md "r0's Y^5 cancels r1's y^5" kind): r0 gives Y^3 = X y x^2, so
y^(n+1) = (y^3)^k when n = 3k-1, and MS(n) collapses to (yx)^k y^(3k-1): n=2 -> yxyy (the certified 15),
n=5 -> (yx)^2 y^5 (9 letters), n=8 -> (yx)^3 y^8 (14 letters).  So n = 2, 5, 8 share a mechanism; n=8 (ac-09689)
is the one unsolved row where the n=5 record's first step transfers (verified below), but the finish from
(r0, (yx)^3 y^8) is open and was not searched here.

## 3. What ran (all nice -n 10, one process, pinned core SAIR=/root/.cache/upgh/sair, pure Python)
| run | result | scope |
|---|---|---|
| work/mhop.py phase A n=3, r0-only moves {0,2,3,6,7,8,9}, 7+7, cap 30 -> target (YXyxyyx, MS3) | LEN 12 = our phase A | sanity |
| same at n=4 -> (YXyxyyx, MS4) | NONE within 14 | cap 30, r0-only, bounded |
| work/bsgoal.py n=3: r0-only BFS to ANY T_m / T'_m rotation/inverse, |m|<=8, depth 12, cap 30 | HIT depth 3: `0 9 2` (r0 = YXyxyyyx = T_3^-1 rotated, basis (y, y^p x y^q), p+q = 3) | a 3-move phase A for n=3 (route shortening lead, not this task) |
| work/bsgoal.py n=4, same goal set, depth 14, cap 30 (51,614 states, complete to depth 14) | NONE | bounded; agrees with the criterion |
| work/mhop.py n=5 all moves 6+6 cap 24 -> (YYYXXYx, yxyxyyyyy) | LEN 11 `1 4 6 6 10 8 4 9 7 7 1` ok | verified partial road on ac-07900 |
| work/mhop.py n=8 all moves 7+7 cap 30 -> (YYYXXYx, yxyxyxyyyyyyyy) | NONE within 14 | cap 30 too tight (start is 26 letters) |
| work/mhop.py n=8 all moves 8+8 cap 34 -> same goal | LEN 16 `1 4 6 6 8 10 4 6 8 4 9 7 9 7 7 1` ok | **verified 16-move prefix on ac-09689** to (r0, (yx)^3 y^8), 21 letters; NOT a full route |

No full route on any of the six rows, so no lines.txt.  The two verified prefixes above are partial roads only
(n8_collapse_hop.out holds the raw n=8 line).  No acc_capped / acc_beam run was started (wall).

## 4. Where it breaks and what is worth doing next
- Template transfer (phase A -> chain -> peel) is dead for n != 3 by section 2; do not spend beams on it.
- n=8 (ac-09689): the 16-move prefix reaches (Y^3 X^2 Y x, (yx)^3 y^8).  The n=5 record (38) finishes from
  (r0, (yx)^2 y^5) in <= 27 moves; recovering that finish (acc_beam on ac-07900 from the 11-move state, or an
  exact cap ladder) and testing whether it lifts k=2 -> k=3 is the one concrete lead for a first solve.
- n=4, 6, 7 are MS-1190 open classes 14_1, 17_{40}, 19_{41}: expect no cheap route; a solve there would be a
  new result on a listed open presentation.  n=9, 10 have no coincidence of either kind (n+1 = 10, 11).
- Side lead for ac-00028 (n=3): phase A in 3 moves (`0 9 2`) into the basis (y, y^3 x) instead of 12 into (y, y^2 x);
  z-conjugation then costs 4 letters instead of 3, so the net gain is unknown; not run.
