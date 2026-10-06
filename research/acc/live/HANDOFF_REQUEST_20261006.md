MAD HATTERS ACC: HANDOFF REQUEST (from Jeremy, 6 Oct)

We are putting everything the team knows into one Moves Manual, so nobody relearns or repeats work. Please read it first. It is in the Drive hub as `00_ACC_MOVES_MANUAL_v1_20261006.md`, and in the repo at research/acc/MOVES_MANUAL.md.

Then write ONE handoff with everything you have that is NOT already in the manual. Do not start new searches for this; just write down what you already have. Label everything honestly: COMPLETE, INCOMPLETE or idea-only.

Save it as `HANDOFF_<YOURNAME>_<UTC>.md` in the Mad Hatters ACC Shared Hub, or paste it here if you cannot write files.

1. WHO: your name and model, the dates you worked, and the rows you worked on.

2. YOUR MOVES (methods). One block per method that produced anything:
   - the name and the idea in one paragraph;
   - the exact command or script, and where the code lives (file path or Drive file);
   - settings that worked (beam width, depth, caps, seeds, move set) and speed (states per second);
   - what it produced (rows, lengths, ties/beats).

3. LINES AND ROADS. Every verified road you hold, at ANY length, not just records, one per line:
   `ac-XXXXX: [moves]` or `sac-XXXXX: [moves]`
   Include roads ending at (y,x) and alternate lineages. Mark any that tie or beat the record. Roads that are not records still help, because our global web turns outside roads into ties on other rows.

4. COMPLETED MISSES. Each search that FINISHED with no shorter road:
   - the row;
   - the start/end states or window;
   - depth, length cap, move set and states counted.
   These go into the "do not redo" catalog.

5. UNFINISHED WORK WORTH FINISHING. For each incomplete search or half-built idea:
   - the row and what is left to do;
   - where the checkpoint or frontier is (file plus hash);
   - an estimated time to finish on one CPU core;
   - your honest chance it scores: high, medium or low, and why.

6. UNSOLVED ROWS. Any idea for rows nobody has solved (ac-00738/06611, 10099, 06412, 09632, 00764, 05538, 03320, 06036, and the no-road rows 09026/02552), even untested.

7. TIPS AND TRAPS. What you learned the hard way: bugs, wrong conventions, verifier pitfalls, slow paths, things NOT to do.

8. EXACT RESULTS. Any construction, identity, lower bound or certificate you can state exactly, with its scope.

RULES:
- No SAIR submissions or API calls; Jeremy submits.
- Never touch 09839, 02257, 09311, 06403, 04718, 05378 or their twins.
- Use the pin a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e.

SPECIFIC ASKS (if this is you):
- Kernel: `song10_rules_L4.json` (2,482 rules); results of the 6 Oct plateau / bulge / near-Stable order; the KERNEL-WEB scripts.
- Sol 6.1: the list of 207 closed probes; ac-03060 caps 40–46 status; the integer-bound tool version.
- Astra / GPT: the 60-target packet; the GPT_30 closed-window list (1,527 misses); which of the 29 incomplete rows are closest to finishing.
- Grokboto / SuperGrok: which saved sqlite frontiers (sac-06936 i4–i8, 02717, 09980) are worth resuming, and how long each would take.
- Bob: the song-8 deeper climb results; the 775-row ladder inventory and donor arrays that Sol noted were missing.
- Charlie: your certificates (ac-09400, 03871, 02341, 08889) with caps and state counts.
- Session 2: the fixpoint status on ac-05169 (Fable 133) and ac-06018 (152); the loop scripts' exact usage.
- Git: the rank-3 catalyst and splice_orient script paths; ac-03786 status.
- Dot: your finite-quotient maps (9,520 checks) and how to rerun them.
- DeepSeek: the Stable splice audit details.
- Gemini: whether any of the GEMINI_30 queue ever ran, and where its output is.
