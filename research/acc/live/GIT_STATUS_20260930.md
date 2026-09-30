# Git (session 3) running status, newest at the bottom. Frequent short reports at the owner's request.

- 00:56Z Untried harness eyes on the low-k list (k<=3), the 26 rows within +1/+2. Setup 1 (from 20/16/12/8 moves before the end of our route, width 500, 13 arms: each eye, its opposite, and a length control): 0 of 1,352 searches beat our route. Setup 2 (from the start and from 28/24 before the end, width 1000, adds the grams2->ledger swap and the reverse): 815 of 1,482 done, 0 found. The same eye read at start/half/8-to-go barely separates good from 1-3 over (best AUC 0.59, 3-grams at half). Files: scratchpad neweyes/eye_restart*.jsonl. Next report after the next chunk.
- 01:05Z Eye setup 2: 964 of 1,482 searches done, 0 found.
- 01:05Z Owner asked for all submissions in the team folder. All of Git's lines are already there AND already sent (SENT_ROWS shows tie): ac-07119 33, ac-08371 25, sac-08371 27 (inbox/20260929T1400Z/1415Z_git_skeldp_*). Git has no other verified lines pending. Eye runs continue; nothing found yet.
- 01:14Z Eye setup 2: 1130 of 1,482 searches done, 0 found.
- 01:23Z Eye setup 2: 1321 of 1,482 searches done, 0 found.
- 01:32Z Eye setup 2: 1482 of 1,482 searches done, 0 found.
- 01:41Z Setup 2 finished: 0 of 1,482 (from the start and 28/24 before the end, width 1000). New lane: eyes make NEW roads from the start, then the loose road-keeping DP (GROW2 MAXC16 SLACK4) shortens them. At width 1000, depth record+12, no eye-steered beam even reached (x,y) on 00145, 00975, 03871 (57 tries). Trying wider and deeper next.
- 01:43Z Eye-steered roads from the start die in Python even at width 3000/depth 60 on ac-03871 (flat start; the beam closes in a basin). Stopping that lane. Loading the 10 untried eyes into Mixer 5.2 as group studies, plus same-eye-at-three-times studies.
