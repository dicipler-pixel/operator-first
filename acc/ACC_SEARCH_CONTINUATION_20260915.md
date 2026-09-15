# ACC search continuation — 2026-09-15

Scope: ordinary Andrews–Curtis only. This continuation picks up the unfinished September 15 ACC search from the verified package `ACC_VERIFIED_SEARCH_PASS_20260915.zip` and does **not** promote any bounded miss to a nontriviality claim.

## Source package

- Package: `ACC_VERIFIED_SEARCH_PASS_20260915.zip`
- Archived SHA-256: `b4ead3b00e120f595ceb8bb2ae4bbb558104a9ed924d5d8e50fbae53d0a1e33d`
- Official SAIR semantics pinned there to commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`.
- Existing exact reverse dictionary: radius 8 = 24,587,144 states; radius 7 = 2,849,131 states.
- Existing exact trajectory suffix dictionary: 182,639 states.

## Do-not-repeat boundary

The current ACC ledger already closes the cap <= 18 corridor for the AK(3)-equivalent target class represented by `ac-00399`, `ac-06279`, and `ac-06945`. Cap 19 is unresolved. Therefore this continuation did **not** rerun the closed cap <= 18 corridor.

## AK(3)-equivalent representative search

Representative used:

`ac-00399  YXYxyx  YYYYxxx`

The search uses the package's frozen 14 ordinary rank-two AC moves and a loose total-relator cap 37, so this is not another cap-19 forward closure attempt.

### Radius-8 + exact-suffix pass

One completed seed before the local execution budget expired:

```json
{"challenge_id":"ac-00399","algorithm":"atomic-beam-ball8-trajectory-suffix-v3","record":0,"kTeams":0,"time_budget":15,"seconds":15.0438,"width":60000,"depth_limit":120,"levels":18,"seed":0,"cap":37,"seen":6262858,"expanded":751616,"generated":9634652,"exact_suffix_hits":0,"found":false}
```

Interpretation: 6,262,858 forward states were retained/seen, 9,634,652 legal transitions generated, 18 forward levels reached, and there was no collision with either the radius-8 finishing ball or the 182,639 exact trajectory suffix states during this bounded pass.

### Radius-7 multi-seed comparison

```json
{"challenge_id":"ac-00399","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":8,"seconds":8.70973,"width":60000,"depth_limit":100,"levels":14,"seed":0,"cap":37,"seen":4267483,"expanded":525568,"generated":6695246,"found":false}
{"challenge_id":"ac-00399","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":8,"seconds":8.017,"width":60000,"depth_limit":100,"levels":9,"seed":1,"cap":37,"seen":1919473,"expanded":248320,"generated":3078361,"found":false}
{"challenge_id":"ac-00399","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":8,"seconds":8.01112,"width":60000,"depth_limit":100,"levels":15,"seed":2,"cap":37,"seen":4638226,"expanded":569856,"generated":7271099,"found":false}
{"challenge_id":"ac-00399","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":8,"seconds":8.00671,"width":60000,"depth_limit":100,"levels":16,"seed":3,"cap":37,"seen":4993882,"expanded":620288,"generated":7913887,"found":false}
```

All four bounded passes miss. This says only that these four heuristic beams did not hit the radius-7 finishing dictionary under the stated budgets.

## Other unresolved ambiguity classes

To avoid overfitting all compute to the AK(3) collision class, one radius-7 pass was run on each of the current ambiguity representatives:

```json
{"challenge_id":"ac-02089","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":6,"seconds":6.00874,"width":50000,"depth_limit":90,"levels":15,"seed":0,"cap":38,"seen":3830794,"expanded":478464,"generated":6068157,"found":false}
{"challenge_id":"ac-05932","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":6,"seconds":6.00869,"width":50000,"depth_limit":90,"levels":15,"seed":1,"cap":38,"seen":3778713,"expanded":485632,"generated":6138068,"found":false}
{"challenge_id":"ac-03467","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":6,"seconds":6.55267,"width":50000,"depth_limit":90,"levels":16,"seed":2,"cap":38,"seen":4356222,"expanded":541440,"generated":6886078,"found":false}
{"challenge_id":"ac-08126","algorithm":"atomic-beam-ball7-v1","record":0,"kTeams":0,"time_budget":6,"seconds":6.37934,"width":50000,"depth_limit":90,"levels":16,"seed":3,"cap":38,"seen":4356814,"expanded":557824,"generated":7089310,"found":false}
```

Again these are bounded misses only.

## Search consequence

The current four-eye beam rankings are not intersecting the known finishing neighborhoods on these hard representatives even with a loose cap. The next useful implementation change is therefore **not** another identical forward beam or another rerun of cap <= 18. The next experiment should bias toward the representation-rescue signal directly: generate legal signed/Nielsen/cyclic transports, score each representation by distance/collision propensity against the reverse dictionary and exact suffix atlas, then launch bidirectional search from the best representations. Any hit must be compiled back to primitive ordinary AC and independently replayed under the pinned official verifier before promotion.

No new SAIR submission, first solve, score claim, Stable-AC claim, or impossibility claim is made by this continuation.
