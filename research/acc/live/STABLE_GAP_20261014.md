# Stable-gap rows: the Stable board's own opening (UPG-H, 14 Oct 2026, 07:45Z)

Owner's hint: "look for what has been there this whole time right there". The two live boards themselves (00:13Z).

**Stable record minus AC record, per row (all 7,443 rows solved on both boards):**

| Stable - AC | -1 | 0 | +1 | +2 | +3 | +4 | +5 | > +5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rows | 2 | 70 | 833 | 6,204 | 103 | 59 | 29 | 143 |

- +2 is the plain conversion (AC road + [16,15]); +1 / 0 / -1 means someone used a (y,x) finish or a real stable move.
- **334 rows have Stable record >= AC record + 3.** On these, the AC-record holder (usually k1, a top team) never submitted the conversion, and a longer Stable line holds the record.
- **On those rows an AC road that misses the AC record by up to (Stable - AC - 3) moves still BEATS the Stable record** (AC road + [16,15]). A Stable beat is a new solo record: 1.0 point.
- No row is solved on one board and unsolved on the other.
- We hold a road on only 13 of the 334 rows. The lost-line audit (all repo roads, run 07:30Z on the 00:13Z board) found 0 scoring lines, so none of our existing roads qualifies.

**Slack** = (Stable - 3) / AC record, the factor our AC road may be over the AC record: 1 row >= 1.25 (sac-00590: AC 116 k1, Stable 148 k1 -> any AC road <= 145 beats), 2 rows >= 1.15, 13 rows >= 1.10, 45 rows >= 1.05, 273 rows >= 1.00. Full ranked list: `sweeps/rival3/stable_gap_ranked_20261014.json` (slack, row, AC rec, k, Stable rec, k, AC target, ours).

**Lane (started 07:42Z):** real dual-P2 beam (rival3/rival_beam.py, direct + twin + (y,x), W 20000, depth = Stable record - 3) on the 16 rows with slack >= 1.10 (`sweeps/rival3/jobs_stablegap.json`). A verified Stable line under the record goes to `research/acc/live/inbox/upgh_rival3_<UTC>.txt`. Our long-row test (records ~101) reached 1.21x on one row and no road on five, so the 1.25x and 1.15x rows are the realistic ones.

**Also checked, nothing there:** the official repo has no commits after our pin (a0fd6e6, 11 Sep). `ms1190_metadata.csv` (in the verifier data folder): the 550 "open" MS presentations are 1,440 of the 2,672 unsolved rows; all 366 rows of the 216 "uncertified" (literature-solved) presentations are already solved on the board.

**Results so far**
- 08:00Z ac-00590 (slack 1.25): no road within depth 145 (W 20000, three modes, 1,617 s). The beam cannot finish long rows at all.
- 08:20Z change-of-variables transfer onto Stable-gap rows (`tools/acc/upgh/stablegap_cov.py`): 51 pairs (rows with a key-mate we hold a road on), all verified, **0 under the Stable record**. The mates sit on rows with only 3-5 moves of slack, and the transfers are 1.5-3x long.
- Short Stable-gap rows (AC record <= 80): 60 rows, 25 of them accept an AC road 1-4 over the AC record (sac-01366 AC+4, sac-09799 AC+4, sac-08907 AC+3, sac-07160 AC+3, ...). The owner's other session already works several of these (08451, 09747, 00430, 02264, 05309); list in scratch `stable_gap_small.json`.

**Mirror-copy check (symmetry recognition, all 10,109 rows, radius 1, 08:13Z):** 15,374 roads replayed, 2,003 matched start keys. Exactly 1 scoring line is new to us: **ac-06299 36** (via ac-05659; ties AC 36, k12, worth about 0.0002) and **sac-06299 38** (ties Stable 38, k9, worth about 0.002). Both verified on the official cores. Queued in `inbox/upgh_symrecog_20261014T081341Z_r1_all.txt`; not sent (owner's call). Mirror copies are otherwise fully exploited.
- 09:03Z Stable-gap lane stopped by PID after 2 of 16 rows: sac-00590 (D 145) and sac-02933 (D 253) found no road at all (1,617 s and 3,276 s). Verdict: our beam cannot finish long Stable-gap rows from scratch; the remaining 14 rows were not run.
