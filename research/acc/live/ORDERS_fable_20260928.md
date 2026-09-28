# Orders for the new helper (Fable), 2026-09-28

## Read only these (in order), nothing else first
1. This file.
2. `research/acc/live/ORDERS_luna_ms.md` (the doubling-chain problem, all updates).
3. `research/acc/live/IDEAS.md`: only the sections from "2026-09-28 05:" onward that mention MS, height, or Smith.

Do **not** re-verify anything already in the ledger. Every path, negative result and scope there was checked by the
official verifier or by complete exact search, with the settings written next to it. Treat them as facts. Only verify
**your own new** paths (one command, below).

## Your job: the construction for the YXXyx chain (reasoning, not brute force)
Board rows ac-01950 (n=5, record 80), ac-02033 (n=6, 145), ac-06796 (n=7, 275), ac-03079 (n=8, 532),
ac-06727 (n=9, 1046), ac-00106 (n=10, 2071). Each is held by **one** team on both AC and Stable AC: 12 full points.
Start is (YXXyx, Y^(n+1) X y^n x). Records fit 2^(n+1) + n + ~11.

Known facts (do not recompute):
- Exact optima on made-up small cases: n=1: 8, n=2: 15, n=3: **28** =
  `5 1 12 2 5 8 3 6 3 6 3 0 12 2 6 8 2 7 5 6 6 2 4 4 4 4 4 4`.
- n=3 mechanism: moves 6-11 build X^6 in r0 at one move per x (pairs 3, 6); then y = x^7 and y = x^6 collapse to x in
  one move; peel 6.
- n=4: our best is 55 (x^7 then pairs (5,11) to x^15, then peel). Target <= 47. Exact: no route stays below length 20;
  shortest by ceiling 20: 69, 21: 65, 22: 62; none <= 47 under ceiling 25 with moves {0-8,12}, {+10}, {+11}.
- The n=3 recipe on n=4 stalls after 11 moves (leading X's run out). Exact continuations from moves 5/7 find nothing
  short.
- Lisitsa's published routes are valid but far too long (n=5: 1,332 scored moves).

Goal: a **rule** that produces path(n) for n = 4..10 at or near the records. Reason about the words (Baumslag-Solitar
relation y^-1 x^2 y = x; the record grows by about 2x per level, so think recursion: level n reuses level n-1).
Use small experiments to test ideas; do not launch broad searches (those lanes are already running elsewhere).

## Tools (already built; do not rebuild tables)
- Move semantics and verification: SAIR repo at commit a0fd6e6, `competition/tools/verifier/core.py` (`apply_move`).
  Moves 0-13 = ac-r2-v1. Check your path with `tools/acc/plan_offline.py` or `core.verify`.
- `tools/acc/mstrace.py N <moves>`: prints a path on MS(N, YXXyx) with x^k runs shortened.
- `tools/acc/ms_hop.py`: exact shortest route between two given states (small only).

## Output
- A path at or below a record: write `ac-NNNNN: [..]` to `research/acc/live/inbox/<UTC>_fable_<row>.txt`, commit,
  push. Session 2 verifies against the live board and sends. Never submit yourself.
- Ideas and negatives: append a short dated entry to `research/acc/live/IDEAS.md` (what you tried, exact scope, result).
- Branch: `claude/gallant-bardeen-0pgpae`. Pull before you push; never rewrite history.
