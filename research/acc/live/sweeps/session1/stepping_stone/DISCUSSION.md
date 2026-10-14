# Stepping-stone experiment: running discussion log

Running notes for the owner/coordinator. Each entry: what I saw, what surprised me, what I'd try next and why.

## 0. Setup (start)
- Targets parsed from TARGETS_ALL_ROWS_20261014.csv (note: file has CRLF line ends; a naive `awk`/`grep '$'` filter
  finds 0 rows). Group 1 = 78 rows with k_teams <= 2 and gap 1..8 (25 ac, 53 sac). Group 2 = unsolved ac rows with
  start length <= 16.
- Plan: one self-contained script (own fast move function cross-checked against the official core), a lookup of every
  state on every verified road under all 16 symmetries (+ cyclic/inverse canonical key), target-side capped BFS,
  then backward random walks from the goal (idea B) added to the same lookup.
- Coordinator caution (cyclic/inverse merging costs moves): taken. The store key is the EXACT 16-symmetry normal form
  only (letter maps + relator swap, which map roads to roads move-for-move). Rotations/inversions are not merged;
  the target-side search pays for them as ordinary conjugation/inversion moves. Every claimed road is rebuilt
  move-by-move and replayed on the official core. Own fast move function cross-checked against core.apply_move on
  20k random moves + symmetry move-map check on 16 images.

## 1. Calibration + launch (08:31Z)
- Store from ALL_VERIFIED_ROADS: 7,372 usable road paths -> only 79,401 distinct states up to the 16 symmetries
  (120k exact states). Every road-state lookup is one dict hit; normal form via bytes.translate runs ~400k/s.
- Target BFS speed ~45k states/s in plain Python (good enough; I did not build the C tools).
- Calibration on sac-02932 / ac-02932 / sac-07869 (5.0M / 3.3M states, depth 11-12, cap start+8): 240-270 hit
  states each, but every hit was a state on the row's OWN road family; best = our current road (ac-02932 97,
  sac-07869 97). sac-02932 gave 99 < our sac 100, but that is just ac 97 + [16,15], a twin conversion, not news.
  First impression: around the start of a hard low-k row the only verified states nearby are its own road's.
- Idea B walks generated (5 files, 10k walks each, 150-200 steps): band 12-18, profile 12-18, balanced 12-18 for the
  unsolved group; band 16-28, profile 16-28 for group 1. 2M-step band walk = 1.55M new distinct states;
  the profile-biased walk revisits more (0.80M new): biasing narrows the cloud.
- Running now: group 1 (59 distinct starts, 78 rows) 1 process; group 2 (146 unsolved) shards 0,1 of 3.
  Combined pass: each hit is attributed to road states (idea A) or walk states (idea B).

## 2. Coordinator literature note received (during pass 1) - what I adopt
- (1) Peak >= 26 for AK(3) (ac-00399) and the 550 open MS rows (incl. P1 ac-02089, P2 ac-08126): ADOPTED, and it
  bites harder than "raise the cap". A walk whose relator total never exceeds 18 lies on a road with peak <= 18, so
  my band 12-18 walks can NEVER produce a road for those rows, whatever the target-side cap. Pass 1 on group 2
  (cap start+6 <= 22, walks <= 18) is therefore a calibration/control only for those rows. (Also: AC-19 already
  enumerates all AC-trivial presentations of length <= 19, so a short unsolved start cannot sit in a low-peak
  component at all; the thin-component fact explains why pass-1 balls are tiny: 100-250k states complete to depth 12.)
  Pass 2 for group 2 uses walks allowed to climb to 34 and target BFS cap 28 (>= 26), labelled INCOMPLETE where the
  state budget is hit (it will be: the AK(3) class has ~729M orbits at cap 25).
- (2) Route diversity: ADOPTED for idea B. walks.py now has --seed-roads (waypoint seeding): each walk starts at a
  random state of a random held road (its known tail is prepended, reversed+inverted, so it is still a walk from the
  goal) and then wanders in the band. Pass 2 uses one goal-seeded climbing file and one waypoint-seeded file.
- (3) Cyclic-space planning with exact rotation cost: NOT adopted here (a 1-2 day build); my key stays exact-16, so
  rotations are paid as real conjugation moves by the BFS. Noted as the natural next build.

## 3. Group 2 pass 1 done (unsolved, start <= 16) - 08:40Z
- 146 rows, 29.3M target-side states in total, every row's depth-12 ball at cap start+6 (<= 22) COMPLETE
  (depth 12 finished inside the 2M budget; not an exhaustion of the capped component).
  Store: 79k road states + 1.55M (band) + 0.80M (profile) + balanced-walk states.
  Hits: 0 road states, 0 walk states. No new road.
- Not a surprise after the literature note: for AK(3)/MS rows no road can stay below 26, and every road state with
  length <= 22 that the store holds lies on a trivial row's road - the unsolved starts' low balls are separate thin
  components. This pass is a control, and it confirms the separation in our own data: the 146 low balls touch no
  verified state and no walk state at all.
- Pass 2 running: cap 28, depth up to 40, 1.5M states per row (INCOMPLETE by design), store = roads + radius-1
  halo of road states (<= 30) + climbing walks (12-34) + waypoint-seeded walks (14-34).
- Group 1 (k<=2, gap 1-8) pass 1 so far: every hit lands on the row's OWN road family; best found = our current
  road in every row (no foreign donor gives anything shorter). Waiting for the rest.

## 4. Group 1 pass 1 done (78 rows, 59 starts; k<=2, gap 1-8) - 09:01Z
- 1,744 s, 59 BFS (92.0M states) (cap start+8, depth <= 12, 1.5M-state budget: 25 starts complete to depth 12, 34 INCOMPLETE at depth
  9-11). Store: road states + 2.4M idea-B walk states (band 16-28 and profile 16-28).
- Hits: 15-655 road-state hits per start; 0 walk-state hits in all 59 starts.
- Result: 13 roads shorter than our held road, all verified, NONE scoring (plan_offline: +3..+7 over record).
  7 are mere twin conversions (AC road + [16,15] already held). Genuinely new: ac-04676 73 (ours 74),
  ac-00617 61 (ours 63), sac-04676 75, sac-08757 71, sac-00617 63, sac-04219 51, sac-02909 43.
- Surprise: the gaps (3-7 moves) are nowhere near closed by stepping stones. The verified-road states around a
  hard low-k start are essentially its own road family; the 1-2 move gains are local shortcuts between our own
  lineages, not jumps onto another row's road.
- Next (running): same pass with a radius-1 halo around every road state <= 40 and per-hit donor-row
  attribution, to measure how many hits come from FOREIGN rows (the actual stepping-stone claim).

## 5. Group 2 pass 2 (cap 28, deep) and group 1 halo census done - 09:31Z
- Group 2 pass 2: 146 rows, 341.6M target-side states (about 2.3M per row), BFS depth 7-9 reached at cap 28
  (INCOMPLETE everywhere, as expected: the capped component explodes past length 20). Store = 79k road states +
  560k radius-1 halo + 2.58M climbing-walk states (12-34) + waypoint-seeded walk states (14-34).
  Hits: 0 road, 0 halo, 0 walk. No first solve.
- Group 1 halo census (same budgets as pass 1, + radius-1 halo of every road state <= 40, donor attribution):
  87,356 hits (vs 10,446 without halo); all 59 starts have FOREIGN-row hits. So the stepping stones exist -
  foreign roads do pass within ~12 moves of every hard start - but they lead nowhere shorter: the best foreign
  estimate is at most 2-4 moves under our held road and never reaches the record. The foreign donors are mostly
  the same few lineages (ac-00042, ac-00183, ac-00713, ac-00963 ...) whose roads run through common low states
  near (x,y); a target reaches them, then pays a long common tail.
- Halo added 3 shorter roads (sac-08054 54, sac-07541 47, sac-04628 41 vs record 40 = gap 1), still none scoring.
- Lower-bound check: for every group-1 row, every hit's estimate (prefix + donor tail, before finish and the +2
  Stable suffix) is a LOWER bound on the reconstructed length. The best FOREIGN-hit estimate never reaches the
  record in any row (ac: est > record; sac: est + 2 > record), and the 12 lowest-estimate hits per row were all
  rebuilt and replayed, so the absence of scoring lines is not a reconstruction artefact inside these balls.
- Now running (last stage): the 17 gap-1/2 rows (13 starts) with a bigger budget (5M states, cap start+10,
  depth <= 20, halo, 80 reconstructions per row).

## 6. Final stage + controls - 10:08Z
- Gap-1/2 rows (17 rows, 13 starts) at 5-22M states each, cap start+10, depth <= 19, halo, 80 rebuilds per row:
  nothing beyond the 1.5M runs. The closest foreign estimates were sac-09758 37 (record 39; the lower bound est+2 = 39
  was not attained - all 80 rebuilds needed a finish move, best 40 = ours) and sac-08078 34 (+2 = 36 vs record 34).
- Positive control for B (walks only, no roads, 80 solved short rows): blind walks rebuild a road in 10/80 rows,
  5 of them at the record. All 5 are rows with records 8-17. So B works exactly where the answer is short, and
  nowhere near our targets. Control A (roads + halo, same rows) is not clean, because own roads stay in the store.
- Totals: 16 new verified roads, 0 scoring lines (best sac-04628 41 vs record 40), 0 first solves.
- What I would try next and why: target-centred route diversity (lineage-capped beam + waypoint rebeam + splice,
  per the literature note) for the gap rows, and a cyclic-space substitution planner for long and unsolved rows.
  Both ideas tested here spend their budget at the goal end or on what we already hold. The missing roads need
  budget at the target end and above the peak.
