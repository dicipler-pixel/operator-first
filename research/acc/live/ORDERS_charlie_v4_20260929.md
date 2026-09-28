# Orders for Charlie, v4 (00:15Z): route surgery (replaces the high-cap gap lane). Relayed; no repo needed.

Charlie's 23:59Z report: from-scratch Stable gap runs at start+4 stop at 190-480M states (disk), proving only
"no route of 23-29" when 32-41 is needed: lane dropped. Surgery on held routes produced every gain today
(05378 43 -> 42, 03719 tie, 02528 35). New lane: exact tail + window surgery on every held near miss.

Input: `charlie/charlie_surgery_bundle_20260929.json` (relayed as a file): 119 routes the team holds 1-2 moves over
the record (71 AC, 48 Stable AC), all official-verifier accepted, not already tied by us, records from the 20:50Z AC /
20:23Z Stable boards. Each: side (ac / sac), id, record, teams, ours, gap, value (2^-(k-1)), start relators, moves.
Sorted by value then gap: 24 one-team rows first (ac-00145 40/39, ac-06045 37/36, ac-08995 46/45, ac-00975 35/34 ...).
Stable moves use sac-r8-v1 (stable_core); AC moves ac-r2-v1.

Method (yours): tails (last 20-25 moves) and all windows up to what fits; exact, provably shortest per stretch.
Skip ac-08578 / ac-08078 (already locally optimal by your check). A hit (length <= record): send the line.
Report per route: best length and "locally optimal to window W, tail T" if no gain (that is a useful negative).
Kernel sweep (rows 101-213) keeps running alongside at start+2.
