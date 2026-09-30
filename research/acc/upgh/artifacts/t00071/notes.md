# t00071: generator path(n) for MS(n, YXXyx), Fable 5.1 builder, 2026-09-30

Official verifier a0fd6e6 (SAIR=/root/.cache/upgh/sair, core + stable_core). All lengths below are replays that
reached the target on those cores; the harness re-checks everything. Code: gen.py in this directory.

## Start check
Every board row start equals the made-up MS_n start exactly (r0 = YXXyx, r1 = Y^(n+1) X y^n x), no rotation or
relabelling: sac/ac-01950 n=5, 02033 n=6, 06796 n=7, 03079 n=8, 06727 n=9, 00106 n=10 (asserted against the
manifest initial_relators in verify_log.txt).

## Generator (rule)
r0 stays the BS relator YXXyx through the whole build. Two rotation families of the level-k relator:
  F1(k,a) = x^a Y^k X y^(k-1) x       F2(k,a) = Y^k X y^(k-1) x^(a+1)   (F1(1,a) = x^a Y, F2(1,a) = Y x^a)
  Stage A  = 5 7 12 5 6 5 12               MS_n -> F2(n-1, 3)            7 moves (holds for every n tested, 3..10)
  Pump P2  = 1 (4 10)^a 1 5 12 10          F2(k,a) -> F1(k-1, 2a+1)     2a+5 moves   (the (4 10) pump of Git's prelude)
  Pump P1  = 5 (11 5)^a 12                 F1(k,a) -> F2(k-1, 2a+1)     2a+2 moves   (Git's (5 11) pump + the 12)
  Pumps alternate P2, P1, P2, ... from level n-1 down to level 1 (a = 3, 7, 15, ..., 2^(n-1)-1).
  Odd n ends at F1(1, 2^n-1) = x^(2^n-1) Y; one move 13 turns it into F2(1, 2^n-1) = Y x^(2^n-1).
  AC finish (Git seed-11 exact): 6 2 10 1 4 -> (x Y x^(2^n-3), X); strip 2 x(2^n-3); 4 1 2.
  SAC finish, two variants, shorter one kept per row:
    v1: same AC collapse, then mirrored fast peel on (x Y x^p, X) with helper r2 = g x^k (fast_tail_prestrip);
    v2: Git SAC-56 collapse 6 2 7 5 12 -> (Y x^(2^n-2), x), then mirrored fast peel there (fast_tail_git).
  Both are the sac_fast_peel.py idea with relator roles swapped (the collapse lands on (Y x^p, x), not (x, y X^p)).
n=4 reproduces Git's W100k seed-11 route move for move (AC 55, SAC 56). n=3 gives 32/33 (the exact 28 exists).

## Lengths (official replay)
n | prefix to level 1 | AC total | AC record | SAC total | SAC record | prepeel budget (ledger) | our pre-tail cost
3 |   18 |   32 |   -  |   33 |   -  |   -  |  24
4 |   34 |   55 |   -  |   56 |   -  |   -  |  39
5 |   69 |  107 |   80 |  108 |   82 |   48 |  75
6 |  133 |  202 |  145 |  184 |  147 |  102 | 138
7 |  264 |  398 |  275 |  331 |  277 |  215 | 270
8 |  520 |  781 |  532 |  611 |  534 |  449 | 525
9 | 1035 | 1553 | 1046 | 1158 | 1048 |  930 |1041
10| 2059 | 3088 | 2071 | 2230 | 2073 | 1908 |2064
Rows written to lines.txt: ac-/sac- 01950, 02033, 06796, 03079, 06727, 00106 (12 lines, all verified). None is at or
under its record by these numbers; the harness decides.

## Where the hypothesis fails
Hypothesis: prelude + (5 11)x(2^(n-1)-1) + collapse reaches the pre-strip state in about 2^n + O(n).
It fails at the first n above 4, at the prelude, not at the pump. Concretely for n=5:
  MS_5 --A(7)--> F2(4,3) = Y^4 X y^3 x^4 --P2(3), 11--> F1(3,7) = x^7 Y^3 X y^2 x --P1(7), 16--> F2(2,15) = YY X y x^16
  --P2(15), 35--> F1(1,31) = x^31 Y. Prefix 69 > budget 48 before any collapse.
The level-2 state with a = 2^(n-1)-1 is only reached after pumps at levels n-1, n-2, ..., 3 with a = 3, 7, ..., 2^(n-2)-1.
Each pump costs 2a + O(1) (2 moves per BS cell: multiply, then re-align by conjugation), and those a's sum to 2^(n-1)-n,
so the "prelude" alone costs about 2^n, the same as the final level-2 pump. Pre-strip = 2^(n+1) + O(n) (measured 2064 at
n=10, 2059 of it before the collapse), AC = 3*2^n + O(n), SAC = 2^(n+1) + fast tail + O(n). This is exactly the 3*2^n
literal-run road of Fable's 2026-09-28 17:30Z note (2^n - 1 cells at >= 2 moves per cell, then a 2^n peel); the fast
peel removes the third 2^n only, which leaves the SAC line about 2^n/8 above the record (n=10: 2230 vs 2073).
The records' differences T(n) - T(n-1) = 2^n + 1 or 2 say the leaders pay one 2^n per level, so their road cannot
re-pump each level at 2 moves per cell with r0 fixed at BS; r0 has to change (Git's "lever" reading). Not tested here.

## Not done / scoped
- No exact shortening of the constants (A, P2 overhead 5, collapse). At most a handful of moves per level; cannot
  close 27 (n=5 AC), 26 (n=5 SAC), 157 (n=10 SAC).
- No search for a non-literal-run road (both relators long, or r0 changed early). That is the open problem.
- Made-up n=3,4 paths (not board rows) are only in verify_log.txt.

Files: gen.py (generator + verification), lines.txt (12 lines), paths.jsonl (same, JSON lines), verify_log.txt.
