# Step-2 donor junction audit

- Source: `research/acc/live/inbox/upgh_bs_doubling2_20261001T0646Z.txt`, Git blob `c7702f14dcf3334a1706c5c78714c7da2c027106` at reviewed head `8ee0173c8925124c509e98a19038b4cd64638f96`.
- Method: `exact-saved-route-to-fresh-donor-junction-v1` (read-only). This is not the interrupted full-graph BFS.
- Bounds: 180 seconds, 1024 MiB, 600,000 primitive records, zero model workers, zero row searches.
- Result: all four AC donor roads pass the pinned official verifier. They add 369 vertices and 748 directed edges relative to the saved road graph.
- Exact junctions: 13 nontrivial saved-selected-prefix/fresh-donor-suffix state matches (1 on `ac-00022`, 12 on `ac-00028`), but none shortens a saved selected-row baseline.
- Interpretation: retain the roads as fresh verified donor data, but do not rerun this exact junction family until a new selected route or donor road changes the inputs.
- No challenge API call, submission, board claim, pool mutation, or public publication occurred.

`receipt.json` contains the four certificate hashes, graph delta, row summaries, pins, and resource accounting. `candidates.json` is empty because no shorter candidate was produced.
