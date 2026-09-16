# ACC Controlled Mix — 2026-09-16

This file is the **first mix**. Its inputs were frozen beforehand; later corrections to source transcription are preserved as later commits.

Parents / corrections:
- raw ledger: `f202ac7c2ce17543b942279c4e6281667cba2bbb`
- T1 WATCH original freeze: `f1420c19d2ae0e421039933d95190e3f2bb0ad0c`
- T1 WATCH corrected directly from pinned JSONL: `f6b72c6c06d07d3ee61c7f6fe1ef6ec41d1044f6`
- source-structure WATCH original: `1fdafc82c867bad14d6a3f8b7fa32dfbd9750b81`
- fourth-pair source transcription quarantine: `bf7a2793f0253f78dcd141f8d610376f2c4c0f0c`

## Inputs

Eye A — corrected capped T1 fingerprints:
- exact full size+depth ladder twins: `05616/05894`, `06835/07247`;
- exact four-cap component-size twins with one cap19 depth discrepancy: `02024/06036`, `00764/06570`.

Eye B — verified official presentation structure:
- verified for the first three pairs only;
- each verified pair shares exactly the same r2 and differs in r1;
- simple cyclic/inverse-cyclic equivalence of paired r1 words was excluded.
- the fourth pair is excluded from structural mixing pending clean re-extraction.

Independent growth eye contributes zero because the pinned growth file does not jointly cover these pairs.

## Mixed output: exact bounded-membership search queue

Tier A:
1. `ac-05616 <-> ac-05894`
2. `ac-06835 <-> ac-07247`
3. `ac-02024 <-> ac-06036`

Quarantined from current mixed structural search:
4. `ac-00764 <-> ac-06570`

## Required success condition

A pair may be promoted only by an explicit ordinary-AC path replayed under pinned SAIR semantics. Conversely, exhaustive closure at a fixed total-relator-length cap can certify only the bounded statement that no path staying inside that cap connects the pair.

No unbounded equivalence/non-equivalence, solve, nontriviality, or leaderboard claim follows from this mix.
