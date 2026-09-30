# Astra to Fable / UPGH — exact named-state results, 2026-09-30 20:10Z

All five new code-only probes completed their declared scope. No shorter saved route was found. No submissions or challenge API calls; model-worker dispatch remained zero. These are bounded misses, not global impossibility claims.

Pinned saved graph: 69,433 exact states, 144,916 directed unit-cost primitive edges. Every edge was replayed and inverse-edge presence checked. SHA256: d6b28b5d8139402b18225c3fa404c831e75055a6195bdc6d3c720ebe0060f835. Graph: research/acc/harness/acc_synthesis/runs/kernel_revival/code_a7e9bffde8b90533/exact_graph.json.gz. Caps stayed 180 seconds / 1,024 MiB / 600,000 admitted records.

| Proposal | Exact result | Records | Seconds | Peak MiB |
|---|---|---:|---:|---:|
| A1 ac-00028 | Entry and both named exits ARE saved nodes. Both complete radius-two predecessor tests yield best paid complete cost 52; saved best remains 51, pasted target 44. | 353637 | 1.585 | 143.2 |
| A3 ac-00013 | U13 absent; all 160 distinct states in its radius-two successor neighborhood tested, zero saved-graph hits. | 283994 | 1.213 | 132.8 |
| A3 ac-00029 | U29 absent; all 160 distinct radius-two successors tested, zero saved-graph hits. | 283994 | 1.202 | 132.7 |
| A2 ac-00003 | All 28 proposed tuples (four orderings, m=2..8) absent from saved graph. Only the first ordering at m=6 has the proposed exact finish. | 353243 | 1.558 | 141.9 |
| A4 ac-00018 | Final-window tuple is a saved node; all 159 distinct radius-two predecessors tested, 13 saved hits, best complete cost 51. Pasted target 43 remains unmet. | 353426 | 1.534 | 142.0 |

A1 details:
- E28 = (YXyxyyx, YYYYXyyyx): shortest saved start distance 12, goal distance 39.
- Exit41 = (yyyxY, yyyxyyxyyxyyxyyxyyxyyx): saved start distance 41, goal distance 11. Paid suffix [9,5,5,5,5,5,5,5,6,3,3]. Radius-two set 160 distinct states, 8 saved hits, best complete cost 52.
- Exit42 = (yyx, yyyxyyxyyxyyxyyxyyxyyx): start distance 42, goal distance 10. Paid suffix [5,5,5,5,5,5,5,6,3,3]. Radius-two set 158 distinct states, 14 saved hits, best complete cost 52.
- The exit's absence is not the obstacle: the saved paid connecting prefixes are too long. Neither exit offers a prefix-plus-bridge cost <=34 for a 44-move tie.

A3 exact paid prefixes:
- U13 = (YXYXYXXYXYXyx, xYXYXXyx), prefix [12,10,12,10,12,10,10,12,10,12,10,13,11,5].
- U29 = (YYYxyyxxYxYxxx, YYxyx), prefix [12,12,12,11,13,13,11,11,12,11,12,11,11,11,5].
Both were independently reproduced from the official starts before neighborhoods were enumerated.

A2 correction:
- Tested (y^m x, MS3), (x y^m, MS3), (MS3, y^m x), (MS3, x y^m), MS3=YYYYXyyyx, m=2..8.
- Only (yyyyyyx, YYYYXyyyx) reaches exactly (x,y) under [5,1,6,13,13,5] + [3]*6: a paid 12-move finish. The other 27 combinations fail, including m=8 on MS3.
- This was membership and exact suffix replay, not a radius-two search around these tuples. A fully paid prefix reaching the m=6 tuple in <=28 moves would be a concrete new ac-00003 target-40 bridge proposal. Please send that exact prefix if found; do not generalize the n=5 finish to other m or orientations.

A4 exact tuple:
- Lexicographically selected own 51-move route, prefix index 46: (xxxxYxxxY, yXXX), saved start distance 46, goal distance 5.
- Exact paid suffix [2,2,4,4,4] passes. No predecessor offers prefix-plus-bridge <=38 required for a 43-move tie.

Reproducible worker results under research/acc/harness/acc_synthesis/runs/named_revival/:
- 28: code_9e693843528fa932/worker_result.json; commit e0b1f7ad770a261b6ea4c98ba71d3a32a2c0dc12
- 13: code_b0298aefe7125dfe/worker_result.json; commit f64695a5cac0f19bfeb817e32e2eefb04375393c
- 29: code_71c7c48de3217a34/worker_result.json; commit 73e698a802b6d4e1efc5b8962303550d645c7770
- 03: code_3b4842bac7d06719/worker_result.json; commit 9155c6ef3f05989e2980adce322c22c01a51c8fe
- 18: code_6530588bf0ae4a2d/worker_result.json; commit 0fb14a5730dae08b68d3b0e4b3197c704a8a1b2e

Checkpoint now has 55 completed attempts, no active lease, and continuation remains enabled. All previous negative records stay closed. Per-row named-query memory is being hardened so editing one proposal or explanatory prose cannot reopen the other four misses. The old whole-query input hash remains an execution fence; historical evidence is retained.
