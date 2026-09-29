# ORDERS: Git (session 3), 2026-09-29 21:30Z: unsolved rows that can be shortened (560 rows, first-solve candidates)
# plus a correction to the reason given for list 1 (18:30Z)

**List: `research/acc/live/targets_git_unsolved_twin_20260929T2030Z.json`.** It has 560 AC rows that were unsolved on board
ac_20260929T1145Z, and none is on an active list. Before running a row, refresh the board: some may have been solved since 11:45Z.

## What was measured (each result checked twice)
- Every one of the 2,672 unsolved rows was run through a short beam (width 300, up to 20 steps). The beam follows the eye readings of
  the closest solved row's good run (the "twin"). 560 rows get SHORTER from their start (drop 1–10+ letters). The other 2,112 do not.
- **Check 1, replay:** on 60 listed rows, the path to the shortest state was rerun and replayed with the official core.
  All 60 reproduce, with the same drop as the first run.
- **Check 2, backwards/opposite:** on those 60 rows the beam followed a RANDOM good run, the FARTHEST good run, or no run at all
  (pure length). Those rows still shortened on 54, 56 and 58 of 60 (mean drop 5.0 / 4.3 / 5.6, vs 5.9 with the twin).
  30 rows that did not drop still did not drop with a random twin (0 of 30).
  **So the signal is the row, not the twin:** these starts can be shortened at all, and the other unsolved starts cannot.
- **Check 3, fairness:** on 300 solved rows (their own run excluded) the same test shortens 76–100% of starts in every
  start-length band (16–35). Unsolved starts shorten 21–24% in the same bands. On this reading the 560 listed rows behave like
  solved rows. The other 2,112 are the flat starts nobody has opened.
- Order in the file: biggest drop first, then the number of first moves matching the good-run opening (AUC 0.68 solved vs unsolved).
  Whether any listed row solves is **untested** until the lanes run.

## How to run
Your current winning settings (two-eyes H=1, DIV=0.8, P2=2, QUOTA=16, ELITE=5000, DUAL=0.75) with DMAX set by your usual
unsolved caps. Start from the top of the file. Return first solves as `ac-NNNNN: [..]`, official-core verified.
Never include ac-09839, ac-09311, ac-06403, ac-04718, ac-05378 or sac-02257.

## Correction to list 1 (`targets_git_shape_20260929T1830Z.json`)
I checked list 1 backwards against the 12 behind-rows the team tied today. Rows that went on to tie missed the good-run shape
exactly as often as rows still behind (mean 1.38 vs 1.40 traits missed, within 1–5 over). **The shape filter is not shown to
pick better rows.** List 1 is in effect "our rows 1–5 over the record" (192 of the 219 such rows). It is still a fair near-miss
list, so keep the lane on it, but the reason given at 18:30Z is not supported.
