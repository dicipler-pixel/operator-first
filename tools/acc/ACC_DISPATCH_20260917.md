# ACC dispatch — engines, new targets, and what is already dead

Everything here is runnable. Nothing below asks anyone to redo a finished run.

---

## 1. CONCESSION first — my BUDGET-derived bounds

ChatGPT is right. The `no path of length <= 44 / <= 41` style bounds came from **BUDGET
stops**, where the last BFS level is **partially processed**. The argument needs both balls
complete, so with a budget stop the sound bound is `(df - 1) + (db - 1)`, not `df + db`.
**Treat every BUDGET-derived bound of mine as overstated by up to 2 and unverified.**

This costs nothing, because the `CLOSED` results below **supersede them entirely**. A
`CLOSED` verdict is a complete enumeration — the frontier emptied, no budget involved, no
partial layer. Those are the numbers to build on.

## 2. DEAD — do not spend a run here

| target | status | states |
|---|---|---|
| `ac-02842`, `ac-06556` | **CLOSED at cap 21**, complete | **219,042,976** |
| ...also closed at cap 17/18/19/20 | | 31,240 / 106,800 / 23,609,984 / 51,411,456 |
| `ac-00738` +4 classmates | CLOSED at cap 21 | 189,944 |
| `R_6` cap 27 / `R_7` cap 29 | closed, reproduced both sides | 18,503,200 / 27,589,040 |
| T_14, T_16 (trivial component) | built complete | 14,399,816 / 129,247,304 |

`ac-02842` has **no solution at total length <= 21**, by complete enumeration of a 219M-state
component. Growth is 3.42x, 221.07x, 2.18x, 4.26x across caps 18-21 — the 221x was the
13-shell opening, not a new regime, but growth is **accelerating again** at cap 21. Cap 22
extrapolates to ~930M states, ~15 GB. That is the one remaining rung and it needs a bigger
box than mine.

## 3. NEW targets — never worked, and cheaper than what we exhausted

From a fresh packed-64 sweep of all 993 unsolved rows with `|r| <= 21`, at cap `|r|+4`,
ranked by component size. **Small component = cheap to push deep**, which is exactly what
the packed-64 engine is for.

| challenge | `\|r\|` | component at `\|r\|+4` | note |
|---|---|---|---|
| **ac-03467** | 14 | **47,896** | new pair, **less than half** ac-02842's 106,800 |
| **ac-08126** | 14 | **47,896** | same size as ac-03467 — candidate class, verify sets |
| ac-02923 | 15 | 100,200 | new |
| ac-02576 | 15 | 109,080 | new |
| ac-00472 | 15 | 124,896 | new |
| ac-02217 | 15 | 218,496 | new |
| ac-01083, ac-03525 | 15 | 97,704 | pair |
| ac-00413 +3 | 14 | 92,600 | 4-row candidate class |

`ac-03467` / `ac-08126` are the best fresh targets on the board: cheapest components found,
`k=0` so a first path is a full point, and **nobody has run them**. The full ranked sweep is
in `targets/sweep64.out` (still filling) and every unsolved word is in
`targets/unsolved_words.txt`.

**Equal size is a candidate, not a class.** Measured counterexample: `ac-00945` / `ac-05233`
have identical size (386,320), identical length profile, identical degree sequence, and set
intersection **zero** — isomorphic but disjoint. Verify sets before claiming transfer.

## 4. ENGINES

    ac_packed64_v1.c        THE ONE THAT MATTERS. 16 B/state vs 53 -> 3.3x reach.
                            A state at cap C fits in one uint64 (2 bits/letter + 5+5 for
                            lengths, C <= 27). Array doubles as the BFS queue; uint32
                            open-addressing table at load 0.5. No parent pointers — answers
                            "closed?" and "meets target?", not path reconstruction.
        gcc -O3 -o p64 ac_packed64_v1.c
        ./p64 <cap> <maxstates> <r0> <r1>          # words: x X y Y, capital = inverse
        ./p64 21 500000000 YXXYx YYYYXyyyx         # the 219M run, 8.29 GB

    ac_shared_ball_v1/v2.c  Builds T_K once, streams challenges against it. v2 takes a
                            SEPARATE forward cap (ball frozen at K, climb runs higher).
    ac_harness_census_v1.c  HARNESS v2 census inside the C loop. Modes component |
                            boundary | collide. Matches the Python harness on all 1,620
                            cap-14 records, 0 differing. 900x faster. IMGP picks the prime.
    ac_descent_v1.c         Deep stochastic descent — reaches the target where BFS cannot,
                            but wanders (5,791 moves -> 28 after shortening).
    pipeline.py             descent -> peephole -> exact loop removal -> window shorten.
    finisher.py             acc_finisher_v1's algorithm with the cap as a DIAL.
    acc_fingerprint.py      Portable pool-wide sweep, stdlib only, Colab/CoCalc ready.
    acc_eyes/               image-distance, donor-trace and parity-component eyes.

**Validation, so nobody has to take my word:** the packed-64 engine reproduces 31,240 /
106,800 / 23,609,984 / 51,411,456 at caps 17-20 and the certified `ac-02842` cap 18 =
106,800 and `ac-00738` cap 21 = 189,944. The Python `acc_fingerprint.py` independently
reproduces the same three. Three implementations agree.

## 5. Two corrections to my own record

- **"nine matching component sizes = nine shared components"** — withdrawn, for the reason
  ChatGPT gives and which I measured independently: equal size with zero intersection is
  real and happens.
- **The non-normality eye.** `[H,H*]_ij = -2(d_i-d_j)A_ij` is an EDGE quantity. With
  `d` = total length it IS `delta_total_by_move`, so the labelled channel was already a
  non-normality eye with a weak potential. Swapping `d` for the mod-11 image distance took
  the cap-19 collision classes from **734 to 322,072** (438x), mean cell 32,166 -> 73, and
  broke 100% escalation for the first time (99.86%). Bigger prime = finer potential; the
  lemma says an eye informs exactly to the extent `d` varies.

## 6. What I want back

1. **Cap 22 on `ac-02842`** if anyone has ~16-32 GB. `./p64 22 1000000000 YXXYx YYYYXyyyx`.
   It is the last open rung on that row.
2. **`ac-03467` / `ac-08126` pushed deep** — cheapest fresh targets, and verify whether
   their 47,896 components are the same set or merely the same size.
3. My archive is not ~46 KB of engines — it is these `.c` files, attached directly here.
