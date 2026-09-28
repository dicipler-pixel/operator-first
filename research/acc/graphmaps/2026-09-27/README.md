# ACC route-state graph maps — 2026-09-27

This folder exports an exact witnessed subgraph of verified AC and Stable AC solution routes. It is not the full reachable state graph and missing nodes or edges imply no reachability conclusion.

## Files

- `route_maps.jsonl.gz`: 117 per-route records. Each record stores the move list, every exact ordered state from start through target, its move-spec version, provenance, and verifier receipt.
- `nodes.jsonl.gz`: 3039 distinct exact states, separated by move-spec namespace. Node IDs are SHA-256 of the spec plus a canonical encoding of the exact signed-integer relator tuple; the full relators are stored, so hashes can be checked.
- `edges.jsonl.gz`: 3038 unique directed, move-labeled transitions occurring on those routes, with route references.
- `candidate_lines.txt`: three newly found record-length AC paths from the 2026-09-27 tuned-score beam pass.
- `manifest.json`: source checksum, counts, node-ID scheme, and the three new-path verifier receipts.

## Provenance and limits

The base route records come from the supplied `ACC-graphmaps-delta-20260927.tar.zst` archive (archive SHA-256 `c704ff2d3f6067d25ae92e44cd72e96b5036853a536a089f3b74347a578d21b2`). That archive contains 114 route-map receipts under pinned verifier commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`: 57 `ac-r2-v1` and 57 `sac-r8-v1` records. One challenge ID has an alternate route record. The three appended AC records were independently replayed with the pinned official core and accepted by its official TXT submission parser.

The new lines match the task's captured 2026-09-27 records at 31 moves; captured `k` values are not live prices. The exact lines are in `candidate_lines.txt`.

Each route is a path in its own exact move graph. AC and Stable AC use separate namespaces and move specs; do not combine their vertices. The graph contains only observed route corridors, not all legal neighbors or a complete connected component. Fingerprint-based candidate generation is probabilistic in principle, but all three appended paths were independently checked from official starts.

Verifier commit: `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`.


## 2026-09-28 graph splice audit

The exact state-join audit for the two archived `sac-09365` routes found nine intersections. Joining the 31-move route's first 24 moves to the 32-move alternate route's suffix after move 25 reproduces the existing 31-move route exactly. The 31-move route passes the pinned official Stable AC verifier and TXT parser (work 553, peak total relator length 25). This shortens the supplied 32-move path, but it was already present in the source graph archive and is not a new certificate. The exact intersection and verifier receipt are in [graph_splice_audit_2026-09-28.json](graph_splice_audit_2026-09-28.json). The route/node/edge counts are unchanged.
