# Astra unsolved target scout — 2026-09-29

This is a catalogue audit and proposed search allocation, not a new solution or search-speedup claim.

## Result
Using session 2's saved AC board pulled at 11:18Z (generated 11:15Z), all 2,605 rows in the existing 1,621-class shortlist remain unsolved. The entire saved board has 2,672 unsolved AC rows; the curated shortlist excludes known hard classes. Do not infer that rows outside the shortlist are safe new targets.

The 231 Miller–Schupp entries have solved family neighbours at varying parameter distances. Matching the exact word-pair canonical form against the pinned manifest finds 86 classes with a solved adjacent-n representative. **45 of those classes (75 rows) have an adjacent-n route in the 946-route team bundle.** All 946 source routes were freshly verified using official SAIR core a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e. All 231 catalogue family hints match their declared starts under the catalogue symmetries.

The saved hints mark 84 entries as distance 1; this fresh lookup finds 86. It uses the newer saved board and all official starts under cyclic rotation, inversion, signed generator permutations and relator exchange. The source of the two-entry discrepancy has not been isolated; the output supplies explicit source IDs for review. No new bridge search was performed.

## Concrete sources
| Unsolved representative | Rows in target class | Verified adjacent source | Source route length |
|---|---:|---|---:|
| ac-02412 | 5 | ac-01784 | 56 |
| ac-09310 | 2 | ac-05703 | 26 |
| ac-03390 | 2 | ac-05653 | 28 |
| ac-07430 | 2 | ac-00101 | 30 |
| ac-09194 | 2 | ac-08646 | 31 |
| ac-04413 | 2 | ac-08646 | 31 |

The unsolved neighbour may still be very hard. Adjacency in n is not a short AC-distance certificate. Canonical equality does not supply a ready-to-execute move sequence. Any use of a source route requires explicit orientation/basis alignment and official replay of the completed target path.

## Proposed team allocation
- Session 1 owns unsolved MS firstsolve; Git also owns the YYXXYx family. These rows have **not** been claimed by Astra. Cross-check their complete private target files before assigning a pilot.
- Bob's 11:05Z job already expands generator-change transfer on all 946 source routes. Do not duplicate that pass.
- Complement their work with explicit bridges from an unsolved state to an intermediate state with a verified suffix. The existing firstsolve script keeps only the shortest replayed prefix. A useful bounded comparison would retain several structurally distinct prefixes, including ones before a temporary length increase, under the same total compute budget.
- Start with at most 10 owner-cleared classes. Save all prefixes, searched bounds and verified suffixes. Expand only after a new verified connection or first solve; if none appears within the pilot budget, record the bounded negative and change the method.
- For first solves, prioritize a legal verified route before optimizing its length. Then explicitly transport and verify it across the target symmetry class and check Stable variants separately.
- Snell/Smith/ordered-chain scores remain exploratory. Session 2 is already running the matched chain A/B; this scout changes no production key.
- Only session 2 submits. No SAIR API reads or submissions were made by this script.

## Reproduction
Run from the repo root with the pinned official SAIR checkout:
```sh
python3 research/acc/optimality/experiments/astra_unsolved_scout/scout.py \
  --board research/acc/live/boards/ac_20260929T1118Z.json.gz \
  --unsolved research/acc/live/UNSOLVED_TARGETS_20260928.json \
  --roads research/acc/live/bob/bob_crossclass_bundle2_20260929.json \
  --exclusions research/acc/live/AK3_CLASS_ROWS.json \
  --output work/astra_unsolved_scout.json
```
The JSON includes each source row, route length and official certificate hash; full source routes stay in the existing team bundle. The recorded input hashes refer to the local replay copies; source Git blob SHAs are in source_blobs.json.
