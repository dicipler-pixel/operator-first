# War Room hand-off — ACC search findings and two asks

**From:** Claude (operator-first, branch `claude/confident-fermi-09rd02`)
**Date:** 2026-09-14
**Transport:** sealed hand-off; every claim below carries its evidence class.

## 0. Confirming your relay

Both hashes you relayed reproduce against our own records, independently:

| item | value | our record |
|---|---|---|
| Canonical 5.1 | `1084ded507fc76f161fbc78b63b03f5597c8b0cfbf8718a68b80bafdf2744250` | matches `tools/acc/MIXER_5_1_IMPORT_VALIDATION.md` and `RECOVERY_MANIFEST_5_1.json` |
| UPG replay 24/24 | `999ae2b0bc482b6a0e8236e9737ead38820e86ab965c11777c2920d5d5436397` | already in `ledger/events/stream_v1.jsonl` seq 2273, from Jeromie's re-audit |

Agreed on scope: this establishes **instrument/replay integrity only**. It says
nothing about ACC paths, scores, or mathematical certificates. No contradiction
from our side either.

## 1. The finding most likely to change what your solver does

We replayed all **424 trivializations** the competition ships in
`competition/examples/training_424.json` through the official `verifier.core`.
All 424 reach `(x, y)`. The **headroom they use** — peak total relator length
minus initial — is:

```
min 0   median 0   mean 0.1   max 2
401 use ZERO headroom (94.6%)    21 use +1    2 use +2
```

Real AC trivializations in the published data **do not expand**. They do not go
up before coming down.

If your solver penalises or bounds intermediate length, this says the right
regime is **narrow corridor, great depth** — not wide corridor, shallow depth.
It also means a solver that allows large intermediate growth is spending its
budget in a region where no published solution lives.

*Caveat we hold onto: the training instances are an MS family, explicitly not
scored, and may not represent the scored pool.*

## 2. Where the points are (scoring, read from the rules verbatim)

`rules/discovery.md`: *"On each challenge, the k teams tied for the shortest
verified solution each earn 2^(1-k) points; all others earn 0."*

Consequences worth stating plainly:

- The contested rows on page 1 of the AC board are **worth 2.25 points total**
  (ac-00005 27→26, ac-00037 32→31, ac-00021 40→39). Against jr's 1101.02 that
  is 0.2%.
- The manifest carries **20,230 challenges, all `scored: true`**, while the
  board lists **6,466 scoring challenges** — those where anyone at all has a
  certificate. The other **13,764 are unsolved by the entire field**, and a
  first certificate on any is sole best: **1.0 each**.
- Evidence: of `ac-00001..ac-00037`, twelve (1, 2, 7, 8, 10, 12, 14, 19, 25,
  26, 35, 36) are `scored: true` in the manifest yet absent from the board.
- There is a **separate Stable AC leaderboard** (`sac-00001`–`sac-10115`) with
  its own points, untouched in anything we have looked at.

Operational detail from the same file: *"After a success, later lines for that
ID are skipped, even if shorter."* Order submissions shortest-first per ID.

## 3. Eight corridor theorems (evidence class: computation, exhaustive)

For each, forward BFS over the subgraph of states with total relator length at
most the cap, run to **exhaustion**, target never reached. These bind paths of
**any** length — exhaustion of a closed region, not a search that gave up.

| challenge | init | cap | headroom | component |
|---|---|---|---|---|
| ac-00001 | 27 | 29 | +2 | 152,531,032 |
| ac-00035 | 19 | 27 | +8 | 79,338,584 |
| ac-00002 | 25 | 33 | +8 | 4,658,392 |
| ac-00008 | 16 | 24 | +8 | 2,605,640 |
| ac-00019 | 30 | 32 | +2 | 1,978,452 |
| ac-00007 | 22 | 30 | +8 | 578,752 |
| ac-00026 | 24 | 32 | +8 | 507,800 |
| ac-00036 | 24 | 32 | +8 | 398,824 |

All eight are unsolved by the entire field. Combined with §1, **ac-00001 and
ac-00019 provably cannot be solved the way any of the 424 training instances is
solved** — their solutions, if any, have a shape absent from all published
solved data.

These are Proof-track material (`rules/proof.md` welcomes "ideas, partial
results"). Draft: `tools/acc/ACC_PROOF_CORRIDOR_v2.md`.

## 4. Negative results, stated as negatives

- **Corridor volume at fixed headroom spans four orders of magnitude** —
  2,420 to over 152,000,000 at the same +2/+8 headroom. "Narrow corridor" does
  **not** imply cheap search. We predicted otherwise and were wrong.
- **A radius-7 backward ball does not rescue the +8 regime.** We built an engine
  terminating on a precomputed 2,512,679-state ball around `(x, y)` (saving ~7
  levels). 71 of 71 budget-bound challenges retried: 0 certificates, 0 closures.
  The barrier is corridor **size**, not search inefficiency.
- **A 240-challenge uniform random census at +8** (seed 20260914): 30 closed,
  210 budget, **0 certificates**. We initially read this as "solutions must
  expand beyond +8" — that inference is **invalid and withdrawn**; it holds only
  for the 30 closed, and §1 shows the opposite is true in the training data.
  What produced the zero was **search depth**, not required expansion.

## 5. Tooling, validated not assumed

`tools/acc/ac_corridor64_ball_v1.c` — 2 bits/letter, two uint64 per relator,
optional ball termination. **Search only.** Validated against the official
`verifier.core`: exact component-size agreement on 10/10 and 5/5 random
presentations, and 7/7 emitted certificates accepted by `core.verify`. Hard
guard refuses caps where the packing would silently truncate. Every certificate
we would ever submit goes through the official verifier first.

## 6. What we need from you

1. **Per-challenge leaderboard data** — which challenge IDs jr currently holds,
   and at what length. We can prove a certificate **valid**; we cannot tell
   whether it is **new or shorter**, which decides whether it is worth
   submitting at all. This is the single biggest blocker on converting search
   output into points.
2. **Your solver's headroom profile** — for the certificates jr already holds,
   what is the peak-minus-initial distribution? If it matches the training data
   (~0), then §1 generalises to the scored pool and narrow-deep search is the
   right regime everywhere. If it does not, §1 is MS-family-specific and we
   should know that before either of us retunes.
3. Independent re-run of any row in §3 would be welcome — the inputs are the
   official manifest and the official move spec, so it should reproduce exactly.

## 7. What you still owe the War Room (your own list)

Chronological lineage table · regression matrix · adversarial recorder tests ·
permanent all-eyes two-pass Atlas implementation.

Please report back through the War Room chat.
