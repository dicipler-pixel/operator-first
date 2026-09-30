UPGH — fresh independently verified improvement, 20260930T2235Z

[V] ac-00009: 81 → 79 moves. Peak total relator length 22; exact endpoint (x,y). Pinned checker independently replayed the new route. Saved board target 34 is stale: this is a local route improvement, not a live scoring claim. No submission or send queue.

Result commit: 5c542e9f3cc6817e6094c4d20ad6ca7583376796
Artifacts: research/acc/harness/acc_synthesis/runs/code_c6e47bb49472b548/ (candidate.json, receipt.json, coverage.json, saved_union.json, executed_bridge_search.py, worker_result.json).
Job key: c6e47bb49472b548a7c93b42fa762746e39087316b2b0fedaacf2e9590856663
Official certificate: sha256:1e6ab245413554fdbb754c350a063766fa4187d0ea105fc67edc046523ee641e

Mechanism: fresh route-local bridge collisions; union shortest 81.
Coverage: {"admitted":600000,"collision_pairs":210664,"fresh_seconds":3.356079260003753,"rss_mib":388.515625,"partial_layer":{"side":0,"depth":3},"improvements":[{"length":79,"fresh_depths":[2,1],"meeting_state":[[1,2,1,-2,-1,-1,-2,-1,2,-1,-2,-1,-1],[-1,-2,1,2,-1,-2,-1,-1]],"elapsed_seconds":0.043843089006259106}]}
No global lower bound; caps 180s/1024MiB/600000 unchanged, zero model workers.

Review route only:
ac-00009: [1,4,7,11,8,6,4,3,7,9,3,1,5,1,9,12,10,7,7,8,3,7,13,11,9,2,7,7,9,3,6,8,6,3,6,4,3,6,12,8,10,2,5,13,5,13,11,12,4,7,5,10,13,5,7,12,2,5,6,2,6,1,6,4,13,4,1,7,9,5,6,8,2,6,8,5,3,3,5]
