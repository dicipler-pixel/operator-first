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
