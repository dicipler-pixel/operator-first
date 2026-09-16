# ACC Controlled Mix — 2026-09-16

This file is the **first mix**. Both input eyes were frozen beforehand.

Parents:
- raw ledger: `f202ac7c2ce17543b942279c4e6281667cba2bbb`
- T1 ladder WATCH: `f1420c19d2ae0e421039933d95190e3f2bb0ad0c`
- official source-structure WATCH: `1fdafc82c867bad14d6a3f8b7fa32dfbd9750b81`

No unfrozen signal is used here.

## Inputs

Eye A — capped T1 orbit fingerprint:
- three exact four-cap twins: `05616/05894`, `06835/07247`, `02024/06036`;
- one state-count twin with a cap19 depth mismatch: `00764/06570`.

Eye B — official presentation structure:
- all eight share exactly the same r2;
- paired variation is confined to r1;
- simple cyclic/inverse-cyclic equivalence of paired r1 words was excluded.

The independent growth-curve eye contributes **zero** to this mix because the pinned growth file does not jointly cover the strongest pairs. Missing evidence is not imputed.

## Mixed output: exact-witness search queue

The mix does not infer equivalence. It only chooses where an exact legal transport search has the best evidence-to-cost ratio.

Tier A (exact full-ladder twins + common r2):
1. `ac-05616 <-> ac-05894`
2. `ac-06835 <-> ac-07247`
3. `ac-02024 <-> ac-06036`

Tier B (state-count twin but one depth discrepancy + common r2):
4. `ac-00764 <-> ac-06570`

## Required success condition

A candidate pair may be promoted from fingerprint to exact relation only if we obtain:
1. an explicit ordinary-AC move sequence under the pinned SAIR move semantics;
2. exact replay from one official presentation to the other (allowing only the equivalences actually permitted by the verifier);
3. a persistent certificate containing source IDs, move list, endpoint, and verifier pin.

A bounded miss remains a bounded miss. The mix itself is not a proof, solve, leaderboard claim, or nontriviality result.
