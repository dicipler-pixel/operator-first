# Exact capped exhaustion table for six hard Andrews-Curtis rows

Stable ID: `ACC-CAPPED-EXHAUSTION-TABLE`

## Statement

For six official rows no record-length path stays within the stated total-length cap: ac-06969 (start 27, record 38) empty through cap 32; ac-00145 (15, 39) through 22; ac-06936 (25, 26/27) through 33; ac-03305 (24, 23/24) through 36, with the Stable path first at cap 37 and the AC path at cap 40 with 133M states; ac-03871 (23, 30/32) through 32; ac-05818 (25, 34/36) through 26.

## Assumptions

Official move set and verifier; exhaustive capped search with the recorded state budgets.

## Failure mode

Each row excludes only paths inside its cap; the state budget (about 180M states in 15 GB) is the binding wall at the next cap, not a mathematical limit. Short rows held by few teams need humps of 10 or more letters above the start.

## Evidence status

Exact finite computations recorded in tools/acc/METHODS_PLAYBOOK.md (section 'Exact capped proofs so far'), rerunnable with run_capped_sweep.py; probe-and-predict validated on ac-05818 (cap 26 predicted 80M, actual 87M).

## Verification scope

This branch (claude/gallant-bardeen-0pgpae), 27-28 September 2026 war-room files tools/acc/WARROOM_2026-09-25_capped_proofs.md and the playbook table. Not Lean-certified.

## Credit

Mad Hatters ACC team sessions 1 and 2.

## Next step

Pin the commit, save per-row certificates (inputs, cap, state count, seed) with the table.

## Sources

- [METHODS_PLAYBOOK.md (this branch)](https://github.com/dicipler-pixel/operator-first/blob/claude/gallant-bardeen-0pgpae/tools/acc/METHODS_PLAYBOOK.md)
- [WARROOM_2026-09-25_capped_proofs.md (this branch)](https://github.com/dicipler-pixel/operator-first/blob/claude/gallant-bardeen-0pgpae/tools/acc/WARROOM_2026-09-25_capped_proofs.md)

## Paper applications

- [andrews-curtis](../papers/andrews-curtis/README.md)
