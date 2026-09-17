# Earth–Moon continuation — 9 September 2026

Research programme of Jeromie N. Beasley. Dedicated workstream based on main `401f6b4b255504ef4465140a15b6cfd6daa9c887`; separate from Yang–Mills PR #18. No merge or modification of earlier manuscripts is authorized by this checkpoint.

## Exact target

Find a simple graph G on 19 labelled vertices, supplied as the union of two planar layers, with no independent triple. This certifies chi(G)>=10; the zero-triple branch additionally computes exact chromatic number as 19 minus maximum matching size in its triangle-free complement. This is a sufficient route to the broader Epoch target, not an equivalence with every possible Earth–Moon construction.

## Verified starting state

The recovered `EM19_QUADFLIP_03.py` has closed spherical triangulations, 51 edges and 34 faces per layer. The best saved pair has five independent triples, 101 distinct union edges, one overlap, and a checked nine-coloring. The roof control has six triples at 102 edges. Earlier radius-three search covered 77,046 embedded states and 216,587 transitions without reducing five. Do not count a rerun of that radius as new progress.

Checkpoint file SHA256: `05e3629415ed1b7102c1db881d1df78776813d5951d9e9ca2cd82f1f6149ae76`.
Original search engine SHA256: `023d0fd19be4bd526c5e43c0f035f0af823262e91089c493471ae635e419a526`.
Resume ZIP SHA256: `ceba0d7cbbe68c539b5582513fdeb5e4a8cb13d51e895b7647cf159b91b8bce1`.

The previous one-flip diagnostic has 75 legal moves, no improving move, five neutral moves. Only two immediately destroy old bad triples, but they create six or seven new triples and raise the total to ten or eleven. A target-edge-only objective ignores the removal cost.

## Active experiments

1. Coordinated multi-flip and plateau repair, recording complete move sequences and both gain and damage.
2. Planarity-preserving relative vertex permutations and other larger moves, kept separate from diagonal-flip radius claims.
3. Exact fixed-layer completion via Boolean constraints and independently checked nonplanarity cuts, with a bounded domain and an explicit unknown status on time limits.
4. Current primary literature on these representations and on strong small-order obstructions; separate known results, new derivations, experiments, and conjectures.

Necessary successful-endpoint conditions already proved in the source audit are 96<=edges<=102, minimum degree>=10, overlap<=6, and an induced C5 in the complement. They do not prohibit temporary overlap during unrestricted setup moves or justify a universal ban on symmetry/blow-ups.

## Evidence policy

Persist inputs, actual best states, exact moves, check results, source notes, failed runs and limits. No unplaced edges or add-then-random-repair deletions. Every candidate keeps two planar layers by construction or is passed to an exact feasibility checker; provisional SAT assignments are not called planar. No search failure is a global nonexistence proof. No formal acceptance is claimed without a successful matching compiler run. This is active-session work, not an autonomous after-session promise.
