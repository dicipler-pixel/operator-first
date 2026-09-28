# Codex ACC route-map handoff — 2026-09-27

Verifier: SAIR Andrews–Curtis commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`. Board comparison: committed AC/SAC snapshots generated 2026-09-27 22:45 UTC; team history snapshot 22:39 UTC. Recheck fresh boards before any submission.

## Highest-value near miss

`ac-05818`: 35 moves versus AC record 34 (k=2). Our history at the snapshot held 52. The stable companion `+[16,15]` is 37 versus Stable AC record 36 (k=2); our history held 54. The official CLI accepts the AC line, work 646, certificate `sha256:ff11001a0bc55e9769d0832d4f3f62a8c12d54d03fe272b57e53aacd0a648912`.

```text
ac-05818: [10,10,13,4,10,12,5,12,5,6,4,1,11,13,3,7,4,1,6,3,7,8,5,10,2,13,10,3,8,10,4,2,2,2,4]
```

Method: exact ordered-state root BFS into 183,810 validated suffix states gave 35. Enlarging the root BFS from depth 4 to 6 found no shorter join. Generator sign symmetries of the short suffix atlas (102,512 transformed states) plus depth-6 root BFS found 35 again. Exact bidirectional replacement search found no shorter section of length 2–14 in the displayed route. These are local and atlas-limited misses, not a shortestness proof. Try the queued capped search or a different hump-sensitive route.

## Other checked routes

- `ac-06045`: 40 versus record 36 (k=1). Official CLI work 658, certificate `sha256:3a634624e653ed70e4c1545e6d7cb765fb5dfd1a0eed050084a97ec60d37e96a`. No exact shorter section of length 2–13.
- `ac-09230`: atlas join 36 shortened repeatedly to 27, versus record 26. Official CLI work 435, certificate `sha256:e85c900b72af99471f2bad6cf1ce02bbdbaba5280415f8c0dc7a087a8774b1bf`. No further exact shorter section through length 14. Team history already held AC 26 and SAC 28.
- `ac-09292`: atlas join 19 shortened to 17; an exact forward radius-7 BFS joined the radius-9 goal filter to produce an AC 16. Official CLI accepted AC 16 (work 235, `sha256:2ac991d73c2ce4dd3c552124ca353f3f7e45ec3d7f063287fc5184f565d73f8f`) and SAC 18 (work 236, `sha256:cdb38606bd2a4b900e9a1ce2e000a88241f15cc3b2b5466d7905c44094a19435`). Team history already held both lengths, so these are alternate verified routes, not new scoring submissions.

```text
ac-06045: [5,12,12,12,12,0,2,6,6,8,1,5,10,10,8,2,9,9,2,7,1,4,11,8,3,8,8,6,2,6,8,5,11,8,2,4,4,4,2,0]
ac-09230: [0,11,4,8,6,12,3,7,9,7,8,2,6,5,6,4,6,5,6,6,2,4,4,4,4,4,4]
ac-09292: [1,4,10,12,12,12,12,5,6,2,2,2,2,2,2,2]
sac-09292: [1,4,10,12,12,12,12,5,6,2,2,2,2,2,2,2,16,15]
```

## Coverage and method

- Exact root BFS to depth 4 over all 270 `ac-09071`–`ac-09340` starts found 22 full AC suffix joins. Their AC and simple Stable AC companions (44 lines) all passed the official CLI, but none reached the saved board records.
- The same atlas pass on the 66 targets in `tools/acc/targets_easy_lowk_20260927.json` found seven joins; the closest was `ac-05818` at 35 versus 34.
- A sign-flipped suffix atlas (109,534 short transformed states) and depth-4 root BFS over those 66 found no tie or beat.
- Radius-9 filter was built by streaming 304,332,182 neighbor inserts from the 21,738,013 states at exact radius 8; every positive hit is confirmed by an exact radius-8 neighbor. This avoids the 4.5 GB T9 disk file for exploratory searches. The team's full T9 remains the preferred faster tool when available.
- No SAIR POST was made from this session. No WIN proof-track file is appropriate because no new point was established.

## Global tube check on ac-05818

An exact shortest-path BFS was restricted to the union of radius-R neighborhoods around all 36 ordered states of the 35-move route. It allows switching lanes repeatedly, including detours that cannot be represented by one contiguous window replacement. Results:

| Radius | Allowed states | BFS states visited through 34 moves | Route ≤ 34 |
|---:|---:|---:|---|
| 3 | 42,655 | 39,759 | none |
| 4 | 391,687 | 359,007 | none |
| 5 | 3,555,823 | 3,183,477 | none |
| 6 | 32,087,950 | 27,911,371 | none |

The radius-6 run used packed states and 123-bit fingerprints, with a 6.5 GB virtual-memory cap; it completed without OOM. A competitive path must leave this radius-6 union at some point, subject to the fingerprint collision caveat. This supports an outbound excursion search that deliberately preserves states beyond the known route's local neighborhood. No team record or SAIR submission changed.

## Two-interstate search on ac-05818

A depth-6 exact root search into the validated suffix atlas found three full routes: the 35-move route above and two 36-move alternatives. The first 36-move route and the 35-move route share **only start and goal** as exact ordered states. An additional 35-move route was recovered from the joint radius-3 graph; it adds 11 states to the graph. All four routes have official core verification receipts and exact state sequences in [the mergeable graph map](ac-05818_two_interstates_map.json), now 83 nodes and 87 labeled edges.

The exact shortest-path search allowed any number of switches inside the union of the two distinct routes' radius-R neighborhoods. It looked for a path of at most 34 moves:

| Joint radius | Allowed states | Reached within 34 moves | Tie or beat |
|---:|---:|---:|---|
| 3 | 83,551 | 77,480 | none |
| 4 | 767,892 | 698,448 | none |
| 5 | 6,975,226 | 6,177,667 | none |
| 6 | 62,967,597 | 54,138,001 | none |

The radius-6 traversal used disk frontier layers and 123-bit fingerprints. A separate positive control, with the 36-move route as primary, reconstructed another 35-move route through the same graph and passed official core verification (certificate `sha256:5df43220b2a5997c5ba5e9fdea3959514818e4900852bd2bcf1b6c5e3c59f31a`). Exact contiguous-window replacement on the alternate 36-move route checked 377 windows of lengths 2–14 and found no shorter replacement. These are corridor-restricted results, not a global shortestness proof; any competitive route must leave both tested radius-6 neighborhoods at some point, apart from the negligible fingerprint-collision caveat.

A depth-5 suffix-atlas search also found `ac-07119` at 35 moves versus the snapshot AC record 33 and Stable AC record 34. Its exact window search found no shorter section. No new scoring submission was produced by these checks.

### Additional long corridors and exact checks (2026-09-28 UTC)

Three independent beam settings supplied further official-core-verified AC routes of length 36, including one beginning with move `7` that shares only start and goal with route 0. The [graph map](ac-05818_two_interstates_map.json) now contains **seven verified routes, 141 exact states, and 149 labeled edges**. The two long routes beginning `10` and `7` formed another radius-6 union of 62,272,133 states; exact layered BFS reached 53,893,187 states within 34 moves and found no competitive path. The union of **all seven** radius-5 corridors had 13,399,301 states; 12,302,285 were reached within 34 moves, with no path. The alternate 36-move route resisted all 377 contiguous windows of lengths 2–14; the 35-move route also resisted all 21 exact windows of length 15 (balanced radius-7 meet).

A separate ac-07119 root-depth-6 atlas pass found a distinct 37-move route sharing only endpoints with the 35-move route. Its two-route radius-4 and radius-5 searches found no path at most 34. Diversified beams found alternative AC 35/36 routes for ac-07119/ac-05818, all above the saved record. No new score was established.

## 01734 verifier replay — already sent

[Archived, already-sent lines](codex_01734_candidate_ties.txt): the user's AC path at 36 and its Stable AC companion at 38 (append `[16,15]`). The official CLI accepts **both lines together** at verifier commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`: AC work 647, certificate `sha256:bb37c26f8fec919b55a02bd5d39bc694d2668ab546f8ab68dfe07214a1228a1f`; SAC work 648, certificate `sha256:c3e44dc4b6a61a51db12bf42919a98b0496de098355ff26b2a9255abf68723ba`. The saved 2026-09-27 22:45 UTC board listed AC 36 (k=5) and SAC 38 (k=4); a 22:51 UTC team snapshot listed SAC k=5. The team confirmed ac-01734 at 36 and sac-01734 at 38 were previously accepted by SAIR (SAC submission 2558). **Do not resend these lines.** No SAIR POST occurred here. The SAC line is a valid shorter alternative to the earlier 39-move example, but it is not a new team result.

An exact balanced radius-7 meet tested all 22 contiguous windows of length 15 on the 36-move AC path and found no shortcut to 35. A root-depth-5 suffix atlas supplied only one route of length at most 42 for this challenge.

**Mandatory duplicate gate for helpers:** read [`research/acc/live/SENT_ROWS.txt`](../live/SENT_ROWS.txt) before preparing or claiming any scoring line. It is regenerated by the dashboard and lists our best accepted length, live record, and teams on record. The 01734 lines in this handoff are already sent.
