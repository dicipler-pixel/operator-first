# Bob, job 3 (11:05Z): cross-class transfer on the whole pool
Your cross-class run on 290 paths gave verified paths on 44 new rows (and shorter replacements, e.g. ac-00286 30 vs our
109). Block splice is closed (dead at reach 2 and 3). Same method, bigger input:
`bob/bob_crossclass_bundle2_20260929.json`: the best verified AC path we hold on every row (946 rows).
For each path: carry it through your changes of generators (y->xy, y->Xy, x->xxy, ...), shorten, verify with the official
core. Report:
1. any transferred path at or under that row's record (board 00:03Z is in the bundle: record, teams) -> send the line;
2. any path onto a row that is UNSOLVED on the board (record 0) -> send the line at ANY length (first solve = full point);
3. any path shorter than our `ours` on that row (feeds the team's shorteners).
Hourly one line (rows done, hits, new rows, improvements) to the user or WORKING_bob.md.
