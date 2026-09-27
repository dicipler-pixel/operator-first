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
