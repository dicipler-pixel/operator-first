# STANDING ORDERS: every member, every cycle (6 Oct 15:20Z; these replace all "extra" instructions)

Owner, 6 Oct: "go back through the songs again. Look at them, pick another move. Whatever seemed to work, make it time in with the normal instructions."

## One cycle = 30 to 40 minutes
1. **Long job.** Keep running your one long job (J8 Bob, J9 Charlie, J10 Kernel, J4 Sol, J5 Grok, Git's long-row lane).
2. **Song move.** At the start of every cycle:
   - Open `SONG_IDEAS_POOL.md` (songs 1–12), `research/acc/MOVES_MANUAL.md` Part 2 (what scores) and Part 4 (what does not), and `IDEAS.md`.
   - Pick **one move you have not yet run** on your current rows: a song line turned into one bounded experiment, sized to finish inside the cycle.
   - Run it beside the long job. Prefer the methods that scored: webs, construction + fixpoint, lost-line audit, (y,x) finish, noisy seeded beams.
   - Prefer the "open follow-ups" list in the pool.
   - Never repeat a Part 4 item without a new idea.
3. **Report.** Post one file, `<MEMBER>_update_<UTC>.txt`, to the hub or your folder:
   - long-job progress (COMPLETE / INCOMPLETE with scope and frontier);
   - the song move (song #, line, move, result or scope);
   - any road lines, as `ac-01234: [..]` / `sac-01234: [..]`.
4. **Lines.** Post every verified road, at any length (the webs only move on outside roads). UPG-H replays every line on the pinned verifier and submits about every 40 minutes. Do not call the SAIR API.

Rules: pin a0fd6e6f. Never touch 09839, 02257, 09311, 06403, 04718, 05378 or their twins. A miss is always capped by its scope.

## Suggested first song moves (from the pool's open items; choose another if you have a better line)

| member | song move to try next |
|---|---|
| Bob | **Song 7**, Kernel's peak-seeded bulge beam, or **song 6** "raise the cap we refused to lift": cap ladders on ac-03320 / 06036. |
| Charlie | **Song 7**, session 1's exact minimum-peak search on k1 rows with record ≤ 26. This fits your exact engine; you have never posted a song move. |
| Kernel | **Song 3**, your own four-constants pruning, so radius 5–6 bridges fit in memory on the gap-1 rows. |
| Sol | **Song 1**, persist the DFS stack between passes, or **song 6**, the neutral-plateau BFS. Both are still NOT RUN. |
| Grok | **Song 2**, a parameterized move grammar for MS families. UPG-H's ladder macro is a template: `research/acc/live/sweeps/ladder_law/loop_macro.py`. |
| Git | **Song 5**, Kernel's MS lift + fixpoint on the drifted lift (NOT RUN). |
