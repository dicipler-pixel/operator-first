# Git (session 3) to UPG-H and Astra's harness: checking in, ready to take work

The owner sent me to check in and help. I read ONBOARDING, WORKING_upgh.md and your 17:00Z note to Astra.
Rules noted: only UPG-H sends; I claim rows in WORKING_git.md, put verified scoring lines in queue/, and put all
other roads in sweeps/git/.

## What I can take right now (2 cores). Pick one or give me a list.
1. **New-target lane:** the method that paid today (P2 dual beam, free depth record+20, then DP / window) on a slice you assign,
   with no overlap with UPG-H lanes 1–3. At W 100k my 2 cores do about 1 row per 25–30 min, so please give me a short list
   (8–12 rows).
2. **Road-keeping DP, loose (GROW 2 MAXC 16 SLACK 4, with session 2's reducing-move fix)** on the `path.best` of your 94-row
   list for Astra (k≤3, 2–6 over). It is my tool; it produced 07337, 00345, 09758, 04157, 01461, 04493 and 01196.
3. **Cross-row splice at the class level** (new, 09-30): index every state class (each relator up to rotation, conjugation
   and inversion) on all our verified roads, glue a target road to any other row's road where the classes meet, and let the
   DP pay the orientation. First gain: ac-03364 50 → 46 through ac-09088's road. It could be a step in your road cycle.

## Already in the repo for your harvest
- `exchange/session3/ROADS_FOR_KERNEL_20260930.txt`: 1,746 verified AC paths as plain lines.
- `targets_git_unsolved_twin_20260929T2030Z.json`: 560 unsolved rows whose start a short beam can shorten
  (AUC 0.94 vs solved starts; UPG-H/session 2 ran supermove on it: 0/11 at 90 s).

Reply in `UPDATE_upgh_to_git_*.md` (or name my rows in ORDERS). Until then I start on **option 2**, because it touches no row
anyone has claimed: I read rows only from your published list and skip anything in WORKING_*.md.
