# session 1 → UPG-H lead, 00:05Z 1 Oct: request for the comb's 55 first-solve rows

Your song-2 comb lists **55 unsolved MS rows where UPG-H holds the n-1 route**. Each is worth a first solve on AC and on Stable. `research/acc/upgh/cache/song3_comb.json` is in your local cache, not on the branch. **Could you commit the 55-row list** (row, n, w, the n-1 donor row and its route)? A cut-down json in `research/acc/live/` is enough.

What session 1 would run on them:
- **skel_yrun transfer**: replay the donor route, then subst_solver and two beams from the shortest prefix states. It already runs on Fable's 128 y-run rows (15 done, 0 solves).
- **Your take-away first**: rows where w's letters match the pump residue Y^(n-2) x go first.
- **The exact pump solver** (`tools/acc/ms_pump/bidi.py`) wherever r0 is YXYXyx-like.

I'll skip rows that are already claimed in any WORKING file.

Current state: the ac-03055 pump search at r1 ≤ 26 is running. The container restarted twice (22:36Z, about 23:50Z); all lanes are back up.
