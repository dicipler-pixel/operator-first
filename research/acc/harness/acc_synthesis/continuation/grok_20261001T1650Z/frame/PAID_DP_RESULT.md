# n=10 paid-frame DP, first rewrite ordering

Completed under reservation 9ad348cbbe861127764bfced9562f67a0bbebceb.
The exact minimum inside this specified 15-rewrite necklace chain and its
cyclic/inverse r0/r1 frames is **58 moves**, exceeding the requested entry
budget 48. This is not a lower bound on all 15-rewrite orders or on the full
AC graph. In fact a separate direct level-order derivation gives a 56-move
upper bound, demonstrating that ordering is material.

The chain applies YYx -> xxYY fifteen times. At each step it selects the first
cyclic cut whose resulting cyclic word retains at least three positive y's.
The primitive frame graph includes moves 0,1,6..13, and transitions to the next
necklace use moves 2 or 3. Conjugating tails and other normal-closure rewrite
orders are excluded. Every cost is counted; every recovered move was replayed
by the pinned official core.

Start: (XyyyyyyyyyyxYYYYYYYYYYY, xxYYXyy).
End: (YYxxxxxxxxxxxxxxxxyyyX, xxYYXyy).

The complete 58-move entry, trace, reproducible script hash, layer counts and
all chosen necklace words are in `paid_frame_dp_receipt.json`, produced by
`paid_frame_dp.py`. No finish is appended and no scored-row certificate is
claimed.

Elapsed 0.174 seconds; peak RSS 14.61 MiB; 111,664 primitive transition records.
Bounds: 20 seconds, 192 MiB, 600,000 records, 15 rewrite layers.

Setup originally assumed the rewrite necklace was unique; an assertion caught
branching at layer 2 before the DP began. The corrected, explicit first-cut
ordering was then searched once. This setup correction is not a second search.

The next justified experiment is another registered rewrite ordering that
completes each doubling level before beginning the next (prefer the substitution
that consolidates the x-run), or a bounded all-order graph. It is distinct from
the completed first-cut chain and cannot be reported as already tested.
