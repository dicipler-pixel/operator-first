# n=10 entry and finish audit

All endpoint checks use the pinned official 14-move core, SHA256
`d2972711dc7008679127a987a8965d41ea1606b0fc50bf67e2e06c71c456b3b5`.
No challenge API, submission, external solver, or model API was used.

## Verified constructions

Grok's 14-move block is exact for n=6. With the supplied finA2(4), the
synthetic family start reaches `(x,y)` in 41 moves. The same 14 moves at
n=10 produce `(YYxxxxyyyyyyyXYYYY, xxYYXyy)`, not the m=16 finish state.

The supplied finA2 formula independently replays in 27, 39, and 63 moves
for m=4, 8, and 16, respectively. The m=16 finish peak total length is 87.

A new explicit cyclic-substitution scaffold reaches the exact n=10
m=16 entry state in 56 moves and then `(x,y)` in 119. It temporarily
rotates r1 to `XyyxxYY`, then restores it to `xxYYXyy`. This verifies that
temporary r1 changes are usable. It does not meet the 48-move entry
budget and is not a competitive submission candidate.

The full inputs, move lists, traces, and peaks are in `replay_receipt.json`.
The independently written implementation is `replay.py`.

## Bounded tests and retained misses

1. Frozen-r1 heuristic beam from the 14-move n=10 endpoint toward the
   exact m=16 entry: depth 34, beam 600, total-length cap 80, at most
   100,000 unique states, 20 seconds, 192 MiB. It checked 96,905 unique
   states in 1.34 seconds and ended at the depth cap without a hit.
   This is a heuristic miss, not an exhaustive exclusion.
2. Exact replacement of finish-route windows of length 3–8 by at most
   two primitives for m=4,8,16: 25,830 generated endpoints in 0.052
   seconds. No shortcut in that finite scope; lengths remain 27,39,63.
3. Exact trace splicing using the canonical 119 scaffold, all eight
   signed generator maps and both relator orders, and the earlier
   verified ac-05698/ac-06792 routes. Cyclic/inverse joins were paid in
   actual primitives and replayed. There were 1,625 join comparisons
   in 0.14 seconds. Best resulting routes were 118 and 134, respectively.
   These are worse than the team's reported 110 and 117; no new
   improvement or current leaderboard claim is made. The 0750Z
   candidate file was empty.

Each computation has a matching source and JSON receipt. Repeating the
same input, caps, and methods would duplicate these recorded probes.

## Recovered Bob data overlay

The new canonical 119-move trace was compared, at exact ordered states,
with Bob's recovered 946-row cross-class bundle. Forbidden IDs and their
signed-generator/relator-order/cyclic-inverse classes were filtered using
the official manifest before any donor replay. Known named twin groups
were also checked. Five forbidden rows were present and skipped:
ac-04718, ac-05378, ac-06403, ac-09311, ac-09839; ac-02257 was absent.

All 941 remaining donor routes independently reached `(x,y)` under the
pinned core. The comparison found 1,648 exact state intersections but
no shorter canonical route. The 119-move scaffold remains unchanged.
This used 83,239 combined primitive replay/comparison records and 0.31
seconds, within 100,000 records, 15 seconds, and 192 MiB. No archived
solver code was imported. `bob_exact_overlay.py` and
`bob_exact_overlay_receipt.json` preserve the input hashes, skip list,
per-donor checks, bounds, and final verifier receipt. There is no new
row candidate to transfer against the team's reported 110/117 routes.

## Remaining question

No 48-move n=10 entry was found. The fixed-r1 block cannot simply be
repeated; it ends in a different cyclic frame. Shorter entries require
a better schedule, a different rewrite lineage, or relator changes
beyond the tested frozen-r1 beam. This is an open construction task,
not a proof that entry 48 is impossible.
