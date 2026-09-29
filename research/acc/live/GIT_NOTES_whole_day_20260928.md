# Git's notes on the whole day, 2026-09-28 (read from IDEAS.md end to end, ATLAS_AC_LEDGER.md, SCORE_ZOO.md)

Written by Git (session 3) at ~02:55Z on 29 Sep. The pre-compaction chat transcript is no longer on disk; what remains
is the compact summary plus the chat since 02:24Z. The day's full working record is IDEAS.md (all sessions), which I read
in full for these notes. Nothing here is new testing.

## 1. What WORKED today (points or real signal)

| What | Who / when | Atlas / idea source | Result |
|---|---|---|---|
| P2 key (best total after two multiplications, free rotations) | session 2, 05:30Z–07:20Z | B31, Plate IV, Plate XII | hump rows fall to a 1-min beam; ac-03305, ac-01629 records |
| P2 + QUOTA16 + ELITE5000 | session 2, 12:05Z | B16/B17 class quota ("protect what can be protected, release the rest") | never worse; ac-00487 26/27, sac-06045 41 |
| BEAM_DUAL 0.75 "two eyes" (half P2, half H) | session 2, 13:00Z | beam-loss trace B20 | shorter on 7/10, finds 04081, 08305; ac/sac-04191 tie (18:55Z) |
| Overlap splice | session 2, 11:10Z | the user's "can't bury the count" verses | ac-00487 27 -> 26 = record |
| Mirror transport / borrowed roads + windows | session 1 | B81 | 13 SAC ties, ac/sac-03028, ac-09989, 20 unsent AC ties |
| Stable AC thin board | the user, 03:50Z | user's insight | 95 rows where any AC <= SAC-3 beats SAC |
| Stable AC fast peel (2k + 3m/k) | session 2, 06:05Z | — | tool built; build budget per row computed |
| Commutator hump predictor | session 2, 02:00Z | the user's "Comutators" track | corr +0.36 (triage only) |
| comm_len as P2 tie-break (offline) | score zoo, 10:50Z | census | +0.20 climbing offline; DIED in the beam (P2=3) |
| Rotation compressor | session 1, 15:00Z | Smith-chart reading | 44 roads shortened, none to record |
| Layer-growth probe-and-predict | session 2, 02:20Z | "the leader controls the family" | 80M predicted vs 87M actual |

## 2. How the atlas cards were used today (and the limits of that use)

- ATLAS_AC_LEDGER.md judged all 132 lines (plates, B1–B96, repo cards): 23 METHOD, 20 DIAGNOSTIC, 18 PROCESS, **71 NONE**.
- **The 71 NONE lines were judged by reading, not run.** They were never built as eyes on AC data.
- The METHOD lines were tested in ONE framing: word/class scores ranking the record move among 14 siblings on 59 hump
  paths (sibling rank, top-3), then a beam A/B. A card that fails there is dead only in that framing.
- Tonight's framing is different: Sanov matrices of r0, r1 (faithful SL(2,Z) images), kappa = tr[A,B], eigenvector loss
  at the finish, Mixer 5.2 studies on solved vs unsolved routes. Cards marked NONE by session 2 (B26 exceptional point,
  B79 take the phase, B9 winding, B25 susceptibility, B72 gap as stiffness, B36 three mechanisms at one locus, B64,
  B71 orientation vs holonomy, B73, B90 clock exponent ...) read matrices, which is exactly what the Sanov lane produces.
  **They are untried in this framing.** (The user, 21:50 CDT: "you didn't try them so you don't know ... maybe made in a
  way that doesn't fit now; that's why we have 500 or more to choose from.")
- Mixer 5.2 holds 280 domain eyes (589 views) under concept names; many take "finite matrix data" (ce.reduction.*,
  ce.skew.*, ce.horizon.riesz_group, ce.upg.spectral_susceptibility, ce.cascade.*). None has been run on ACC matrices yet.

## 3. Dead today (do not rerun as new ideas; the opposite was or was not tried as noted)

- Invariant lower bounds (SL(2,p) shadows, finite quotients, exponent matrix): log-scale, bound/record 0.11.
- Macros (Bob40, Schur hump macros, mined n<=3 macros): crowd the beam. Lower MACW / few macros untried.
- Exit-count tie-breaks (B6, B22), learned linear descent (B12, B38): dead in the sibling-rank framing.
- Whitehead frame as key (B83, BEAM_WH), QUOTA=4, P2=3 comm_len key, P2=3+QUOTA16.
- Reverse search (humps sit mid-path), mirror pairs (22, none shorter), near-mirror bridges.
- Local repair of near misses (windows, corridors, echo): "the record paths are different roads".
- Snell R sin^2 theta as a next-move rank feature (Codex, 14:51Z): 0.4629 vs 0.4465; Smith third-eye sector: harmed 05558.
- Literal-run road for MS(n, YXXyx) (Fable 17:30Z): any road through (BS, y = x^(2^n-1)) costs >= 3*2^n - O(1).
- P2 above record ~45: no signal (session 1, 08:55Z).

## 4. Open leads written down today and not yet run

- Ledger top 8: #2 route by rate (needs a group-aware mass, not letter counts), #3 n-uniform prefix transfer across
  MS(n,w) (session 1's firstsolve.py lane partly did this: ac-02842, ac-03989 no path), #5 primitive-relator finish,
  #6 SL(2,p) shadow tie-break, #7 finite-order transfers inside humps, #8 hump in the stable slot.
- B67 holonomy of a hump (net conjugators); B62 partial correlation check.
- Codex 11:52Z: comm_len as a PHASE TRIGGER (c reaches 4 about 34 moves from the end on n=5), not as a score.
- Fable 17:30Z: the collapse configuration (x^m Y x^(m-1) Y, x^(m-1) Y) with half-peel finish m+3; recursion
  MS_n -> level-(n-1) mates in 2^n + O(1).
- Session 1 11:40Z #3: a beam key rewarding progress toward the invariant count y = x^(2^n-1) (proposed, not built).
- Lisitsa structure conjectures (paper blocked by network; needs the user to drop the PDF).

## 5. Rules the day taught (from the user and from mistakes)

- Check the beam's stderr ("macros: N", "p2:") before trusting an A/B (void macro arm, 08:30Z).
- A witness path's peak is not an exhausted cap (ChatGPT 00:52Z).
- Only delete the work dir of the row you stopped (03:10Z rm -rf mistake).
- Refresh the live board before targeting (session 1, 19:00Z: 856 AC records had dropped).
- Each idea its own eye, then mix; scalable; try the opposite before quitting; read the record before working.
- A test's verdict is scoped to the framing it ran in. "NONE" by reading is not "tested".
