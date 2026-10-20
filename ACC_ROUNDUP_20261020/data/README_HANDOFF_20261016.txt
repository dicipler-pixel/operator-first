MAD HATTERS HANDOFF TO BOB AND CASS - 16 Oct 2026, board pulled 07:25Z
=======================================================================
From now on Bob and Cass run every lane except the one Claude keeps (below). The owner relays files and approves sends.
Claude does the SAIR pulls and sends on request (one batch a day; 254 reads left on 16 Oct, reset 00:00 UTC).

STANDING (07:25Z): AC 0.7113 rank 18 (514 rows; next up ACC01-T00088 0.7400). Stable 4.1212 rank 12 (526 rows; next up ACC01-T00128 6.19).
READY TO SEND (verified, waiting for the owner's OK): sac-02375 35 = Stable record (7 teams), found by the (y,x) lane.

RESERVED FOR CLAUDE (please do not search these): the XYYxy Miller-Schupp ladder, rungs n=7 and n=8 (32 rows, records 124-268,
mostly held by one team, no Bluepug rows). Whitehead keys X^7 Y x^6 y|XYYxy and X^8 Y x^7 y|XYYxy.
  n=7: 02033 06018 05754 09166 05559 07279 08810 07432 05802 04252 01035 00308 03347 04287 07161 02961 09886 09978 00004 03758
  n=8: 06796 00676 09046 10057 08570 01137 04432 05876 02281 03625 09515 01197
Other rungs of the same ladder are free (07541 stays Cass's). Bluepug's overnight beats were rungs n=10/11 of this ladder:
one improvement to the shared middle of the road, carried to every disguised copy (11-13 moves each).

LANES FOR BOB AND CASS (priority order)
1. (y,x) Stable lane: rows where we already hold the AC record and the Stable record is AC+1. Restart from every state of our
   record road with the letters swapped (search aims at (y,x)); Stable line = prefix + mapped tail + [15,15]. Tool: descend2.py
   mode yx. It found sac-02375 at cut 1 within 10 minutes. Not yet run: 02288 08078 09758 07337 02528 04493 06927 02331 02446
   07119 (roads in OUR_BEST_ROADS). 7 more rows need the exact road we sent (ask Claude to download it): 04628 06961 07920 02440
   05441 06321 09628. 02909 already ran (5 settings, no gain).
2. Joint-trim loop (your method that gave 07541 -2 and the 01385 tie) on rows 1-3 moves over a record held by 1-3 teams:
   grab bags in MAD_HATTERS_TARGETS_20261015.txt, plus the 97 shortened donors in CROSSROAD_DONORS_20261015.txt.
   Check first how many new states reordering creates: on our long rows it made only 43-103 distinct states (no gain).
3. 07541 (Cass): AC 44 vs 42, Stable 45 vs 44, each record held by one team.
4. Family transfer v2 (Bluepug's lesson). Families = same Whitehead key = same problem in disguise; records inside a family
   differ a lot. Whole-road transfer failed 0 of 400 on 14 Oct (disguise overhead). Try carrying only the shared middle, or a
   donor road with few expensive conjugations. Best open families (points open = sum of 2^-k over rows we don't score):
     XXXXXXXXXYxxxxxxxxy|XXYYxxy  18 rows, records 55-104, 6.0 open
     XXXXXXXXYxxxxxxxy|XXYYxxy    18 rows, records 49-100, 5.8 open
     XXXXXXYxxxxxy|XXXXYXyy       13 rows, records 68-116, 5.0 open (no road of ours)
     XXXXXXXXXXYxxxxxxxxxy|XXXXXYXyy 10 rows, 91-114, 4.25 open
     XXXXXXXYxxxxxxy|XXXXXyXYY    10 rows, 177-218, 3.75 open
     XXXXXXXYxxxxxxy|XXXyXYY      16 rows, 45-74, 3.6 open
   Row lists: whitehead_min_20261014.json.gz (cid -> key, L0, Lmin).

STOP LIST (no return): the 29 famous rows (FAMOUS_29_ROWS: 19 AK(3) class, 10 Miller-Schupp length-14 classes); 03060;
00617/00956/04642 (5 settings, no gain); from-scratch beams on k4-7 rows (0 of 20 at record depth);
never touch 09839 02257 09311 06403 04718 05378 or their twins.

DATA (data/)
  ac_/stable_ac_20261016T0725Z.json.gz   live boards (record, kTeams per row)
  us_bluepug_20261016T0725Z.json.gz      our scoring rows and Bluepug's (both boards): {challengeId: [length, k, points]}
  OUR_BEST_ROADS_20261015.txt            our best verified AC and Stable road per row (3,033 lines)
  CROSSROAD_DONORS_20261015.txt          97 shorter roads from joining roads that share a state (none scores yet)
  MAD_HATTERS_TARGETS_20261015.txt       grab bags A-D with donor roads
  FAMOUS_29_ROWS_20261015.txt            why the 29 short unsolved rows are skipped
  whitehead_min_20261014.json.gz         Whitehead-minimal key of every start (families)
TOOLS (tools/) - reference code; needs the official SAIR verifier (core / stable_core) and challenge manifest; descend2 also
needs a beam engine (acc_beam + endgame table). No keys or API client are included.
  descend2.py      iterated restarts from every state of a road, (x,y) and (y,x) modes, settings ladder, link transfer
  peephole.py      radius-R meet-in-the-middle shortcut finder on one road
  reorder_tube.py  commuting-move reorderings + BFS inside the tube around them
  crossroad_join.py join roads through shared exact states
  whitehead_min.py / cov_transfer.py  family keys and road transfer between disguised copies
Every line must pass the official verifier before it is sent. AC and Stable are separate boards.
