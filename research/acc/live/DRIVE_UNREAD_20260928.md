# Unread Drive items: what they hold and what to act on (2026-09-28)

Helper for the lead session, read-only. No SAIR API calls and nothing submitted. The notes below give derived
numbers and short quotes only; the raw files stay in Drive. Board used: `boards/ac_20260928T1213Z` and
`stable_ac_20260928T1213Z`. Scratch work is in `$SCRATCH/drive/`: `replay_cascade.py`, `cascade_replay.json`,
`root_family_118.json`, `unsolved_signed_rot_classes.json` and the unzipped `t002c/`.

## Ranked leads

| # | Lead | Value | How to test |
|---|---|---|---|
| 1 | **Skip 85 more unsolved rows (R_n family, n = 4..10).** The Drive file `ACC_BRANCH_ROOT_FAMILY_118.json` (15 Sep; ids 10UrcnwmKMse14zV-l5LLyqAEA5p7WXgy and 10H0biLiI2cLEW13PPLZfHqkKQWpIdhfa) maps 118 unsolved rows onto the 8 roots `(x^2 y X y, x y^n X Y^(n+1))`. Each row has an extended-move transport, and all 118 are still unsolved on AC and SAC today. 14 of them are already on the AK3 list and 21 on the `rn_p2_deep` list, which leaves **85 new**. Team policy treats R_n as open problems. | Saves compute. 7 of the 85 are in current target files: 1 in `targets_codex_oddeasyB.json`, 6 in `WORKING_session1.md`. | Replay each row's `extended_transport`. This needs the extended moves 14–18 (the auto_norm Nielsen shears), or `crossrow.py`-style normalisation to the root. Then add the rows to the skip list. |
| 2 | **Group unsolved rows into cheap classes before searching.** My own computation: signed letter maps, cyclic rotation, relator inversion and relator order split the 2,672 unsolved AC rows into **1,655 classes**. **821 classes** have more than one member and cover **1,838 rows** (largest class: 6). Any solve carries over to its class-mates for a few fix moves (`crossrow.py` already does this transport), and each class-mate is a first solve on both AC and SAC. The Drive map records a coarser Nielsen grouping: 2,673 rows in 1,156 groups (`UNSOLVED_SIGNED_NIELSEN_CLASSES.json`, not found in Drive). | Cuts duplicated unsolved-lane work by about 38%, and ranks classes by size. | Classes are in scratch `unsolved_signed_rot_classes.json`. Give each lane one member per class. After any unsolved hit, run `crossrow.py` over the class. |
| 3 | **Exact "no path under this cap" facts for unsolved rows.** These are from the Whitehead return (17 Sep) and Charlie's C001 (23 Sep). **ac-02923**: its cap-24 component is closed (10,932,384 states) and does not contain (x,y). **ac-02217**: the same at cap 23 (13,978,168 states). **ac-01657, ac-06572, ac-00719, ac-03471**: their cap-15 components are complete, closed and certified by two kernels, and none contains (x,y). All six are still unsolved. | Stops capped sweeps from re-proving these caps. | Start `acc_capped` at cap 25, 24 and 16 respectively, or leave the rows out of the capped lanes. |
| 4 | **ac-02217 class.** 02217, 06576 and 07698 have the same signed/rotation key. 09571 and 09723 join them only through Nielsen moves (per the Drive class record). One solve would give 5 AC + 5 SAC first solves, up to about 10 points. | High, if it can be solved. | It is hard. The Whitehead return found nothing from 144,316 Whitehead-minimal hard ports: 0 suffix hits to depth 4 (30.8M states), and radius-8 checks were complete only to depth 3. Try it only with a new idea, such as a primitive-relator stop in the beam (8f #5). |
| 5 | **The 148 cascade paths as extra path memory.** They are valid second paths for `overlap_splice.py` and `crossrow.py` (148 rows). | Expected to be about 0. The gap to the record is at least 5 on every row we don't already tie. | Append them to the path pool and rerun the splice. |

**No verified path ties or beats anything new.** The only record-length cascade paths are the 5 ties we already
hold (AC and SAC, k 30–35).

## Item by item

### 1. "CURRENT_TASK — ACC Atlas Handoffs" (Google Doc, v7, 23 Sep)
- **What it is:** a coordination index for the ChatGPT-run worker lanes Adam, Bob and Charlie, with work orders,
  budgets and hashes.
  - Adam: A005, capped one- and two-move bridges from saved A003 states into the A004 library.
  - Charlie: C001, the "mountain-pass" landscape on A002 paths.
  - Bob: M001 reviewed. His C1 schedule gave 259 vs 243 positive queries on 6 development rows. It was not adopted.
- **Follow-ups found in Drive:**
  - `A005_ADAM_RECEIPT_v1.md`: **0 bridges** at radius 0, 1 and 2 from 2,206,126 saved states to the 8,408-key
    library (cap 27), and no path.
  - `CHARLIE_C001_VERDICT.md`: 21 capped components certified closed at cap 15. Five root-to-destination
    passes are exact at height 16. ac-08323 reaches a basin of length-13 presentations over an exact pass of
    height 16, but ac-08323 is already solved (29, k14). This is a landscape diagnostic with no path to (x,y). The
    cap facts in lead 3 come from here.
  - `CHARLIE_T002_VERDICT.md` and its return zip: T002 was a team test on **ac-05137**, root
    `YYXyx / YYYxYxYXXX`. It gives a 41-move descent from the seed to length 13, and root-to-length-13 routes of
    73–83 moves.
  - `T002_VERIFIED_SOLUTION_AND_REVIEW_20260923.zip` is over the 10 MB connector limit.
    `AC05137_MAGMA_93_VERIFIED_20260924.zip` indicates a 93-move solution. The board has ac-05137 at 39 (k3) and
    our accepted line is 42, so there is **nothing to act on**.

### 2. MAD_HATTERS_ATLAS_CASCADE_MORE_AC.txt (12 Sep, 148 lines `ac-NNNNN: [moves]`)
- **Replay:** every path was replayed with `acmoves.run` from the manifest's initial relators. **All 148 reach
  (x, y).**
- **Against the board:** 0 beat, 5 tie and 143 above.
  - The 5 ties are ac-01808 14, ac-04705 13, ac-06305 15, ac-07248 14 and ac-09621 14, with k 32–35. All are
    already in SENT_ROWS, and so are their SAC lines at +2.
  - 72 rows are shorter than our accepted line, but all are still behind the record (for example 184 vs our 187,
    record 51). The closest are ac-08143 37 vs 32 (k16), ac-03644 38 vs 32, ac-09035 38 vs 31, ac-03945 35 vs 28
    (ours 32) and ac-00946 41 vs 31 (ours 38).
- **Structure:** these are no-climb descents. The median peak minus start is 0, and every path enters the
  single-letter corridor with a median of 3 moves left. Record paths climb 13–16, so this file does not help with
  hump rows.

### 3. "AC_idle_wheels_housings_light_v3"
- **Wrong file id:** 1zlpzFaS4qv1iwdxEl4aoxmDD8Q_iYn06 is actually **ACWindow_note.md**. That is the AK(3)
  proof-track note, the same one as in acwindow-lean (fold AK(n) to AK(−n−1), C_p*C_p resonance, spectral gap
  (2−√3)/28, loop detector, genus target).
- I read the v3 PDF (1ji3AdtipA7Gy5WIVebL6o5JsQzKHyRHA) instead: "Idle Wheels, Housings and Light", Beasley,
  Sep 2026. It is an operator-study paper.
  - Resonance theorem; C5*C5 AK(3) distance 9; C7*C7 AK(3) distance ≥ 16.
  - Product-move lower bound |log(E_S/E_R)|/(2 log φ) from unitary evaluations.
  - Housing (Neuwirth/Lackenby) genus test, with the AK(3) class walk to total length 24: 197,870 members,
    no genus 0.
  - Memory kernel of order d−2.
- A newer **v4** exists: PDF 1B04t0tD9erb9r-mFnIOQ6h-jkT6VERKj (20 Sep), plus a 26.7 MB zip.
- **For the leaderboard: nothing new.** Quotient and evaluation lower bounds grow only logarithmically, like the
  SL(2,p) shadow bounds that are already dead, and the genus test is on the failed-controls list. Its value is
  for the proof track only.

### 4. Name searches
- **ACC_BASIN_PORT_ATLAS_FIRST_PASS_20260922.md:**
  - ac-02842: 16 cheapest exits fall into 4 port classes at cap 15; 680 fall into 23. Descent from each
    class representative took 13–17 moves. But ac-02842 is **in the AK3 class**, so skip it.
  - Its table of 8 R_n roots led me to the 118-row family file behind lead 1.
  - Port-class search is already in the Codex audit and IDEAS, so it is not new.
- **ACC_WHITEHEAD_EYE_RETURN_20260917.md:**
  - Corrected rule: "connected and no cut vertex" does not certify minimality. Use the finite rank-2 Type-II
    shear sweep.
  - Hard-port contraction for ac-02923: 12.7M → 137,368 → 82. Every finish check came back 0 (the cap facts are
    in lead 3).
  - 229 of 993 unsolved starts with length ≤ 21 are Whitehead-shortenable, with 0 new matches to solved roots.
  - ac-01083 and ac-03525 are shortened into the ac-02842 class, which agrees with our AK3 list.
  - Whitehead as a beam key is already dead (BEAM_WH).
- **LEAN_ATLAS_RELEASE_INDEX_v1.md:** an index of 483 unique Lean theorems (495 instances) over 14 PRs, with
  no ACC content. It matters for citing the Lean atlas, not for competition work.
- **ACC_PRIOR_ART_CORRIDOR_HANDOFF_2026-09-13:** not in Drive. It is local at
  `/home/user/mad-hatters-acc-private/results/`.
  - It covers prior art: Carreras 2607.23611, Shehper et al., Two-Hump/ACSolverX and Myasnikov–Myasnikov–Shpilrain.
  - It reports an exact corridor-tail finish: 424 official training paths, 950 moves saved, largest saving 8,
    with the rule "shorten every accepted path's corridor tail".
  - This is probably covered by the T9 finish plus the window-14 pass. Check that P2-lane output goes through
    `acc_window`.
