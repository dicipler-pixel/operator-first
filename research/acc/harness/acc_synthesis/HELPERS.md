# Recovered Charlie, Bob and Kernel methods

Recovered from private branch head `3981da39a41834acf982336318cad2dde8d4b8a0` on September 30, 2026. The source inventory covers 185 matching paths / 161 unique blobs / 2,615,417 original bytes. Original Git blob hashes were verified. Their private repository paths and SHA256 values are in `helpers/recovered_source_inventory.json`; required copies and runtime inputs are committed under `helpers/*_sources/`.

| Lane | Latest useful protocol | New executable adaptation | First bounded result |
| --- | --- | --- | --- |
| Charlie | v11 cap ladders; exact ordered freely reduced states and disk layers | Small-memory two-sided exact-cap BFS; radius-5 goal ball, explicit partial layers | ac-00037: 32 remains, target 31; cap 39 incomplete, 600,000 admitted records, 9.10s, 249.2 MiB RSS |
| Bob | Job3 cross-class generator transfer; closed reach2/3 splice stays closed | 456 short Nielsen maps against 946 saved donor paths; all conjugations/alignment/finishing charged as official moves; exact own-route union | ac-00012: 52 remains, target 47; 945 foreign donors, 430,920 comparisons, zero class matches, 14.77s |
| Kernel | Sep30 06:00 road-compressor handoff, distinct from the Astra relay | Verify foreign roads, build directed unit-cost exact-state graph with explicit inverses, join bounded fresh prefixes to saved suffixes | ac-00034: 44 remains, target 41; 2,781 verified roads, 69,116 graph states, 600,000 graph-plus-fresh records, 26.62s, 397.6 MiB RSS |

These are bounded misses, not proofs that shorter routes do not exist. Kernel's graph had 144,184 directed edges and 344 exact collisions but no improvement. Charlie completed the radius-5 goal ball and start expansions through depth 10, then stopped partway through depth 11. Caps 41 and 43 were not started. Bob exhausted only the declared donor/automorphism family.

Charlie's first attempt accidentally spent essentially the whole record budget on an incomplete radius-7 goal ball. It is preserved as an implementation allocation failure at `runs/charlie_revival/`; it is not research coverage. The repaired result lives under `repaired_run/`. No ac-00028 search was run: source-fit review reassigned the same worker to ac-00037 before search. Start length 31 is one beyond Charlie v11's original <=30 slice; this adaptation is explicit.

Large historical T16/B36 disk components were not recovered. The standalone Kernel write-up closing the doubling lead was absent from the pinned tree; its contents are not invented. The doubling lead and Bob's closed block-splice lead are not reopened. Kernel's foreign-road overlay is a new adaptation of the compressor handoff, not a claimed reproduction of a historical win.

Three successful implementation workers completed under the owner's direct helper request: Sol for Charlie and Bob, Sol 6.1 for Kernel. Two capacity failures and one same-worker row reassignment are preserved separately in `continuation/helper_handoffs.json`. They are not counted as successful searches. Scheduled dispatch stays zero. There is no external provider client or submission transport.

Executed source/test snapshots, input hashes and result artifacts are retained per probe. Later boundary repairs (OS memory limits, absent saved baselines, immutable output directories, startup pin checks and stop polling) do not create permission to repeat unchanged mathematical work. Bob's initial probe observed RSS without the later hard address-space limit; the reusable lane now enforces it. Charlie's repaired probe had a 178-second deadline and hit the unchanged record cap in 9.10 seconds; its memory key also blocks a redundant 180-second scheduling slot.

Run continuation through `helper_batch.py`, following `CONTINUATION.md`. No current scoring claim is supported by the stale board snapshot. No challenge API request or submission was made.

The new controller subsequently reserved ac-00037 in private commit `04926247e8cf4d17d3f6430c23bc6076e288beb6` and ran Bob entirely as code. It examined 945 foreign donors / 430,920 transformations in 16.25 seconds with no class matches or improvement (32 vs target 31). This different method is now recorded under its own stable negative-memory key. No model worker was launched.
