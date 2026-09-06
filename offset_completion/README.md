# Offset completion proof evidence

This is the actual successful verification of the 28 new named theorems.

- [Endpoint workflow](https://github.com/dicipler-pixel/operator-first/actions/runs/34013213809)
- [Core workflow](https://github.com/dicipler-pixel/operator-first/actions/runs/34013213849)
- Source head: `7f714341843e65e6b42744bc0e86501bbe52c40f`
- Tested PR merge: `88fc1f350cd460384e162605f8725bc17af63e9b`

GitHub tests a temporary merge of the draft into its base. This is a check; it does not merge the PR into the branch. `report.json` records that temporary merge commit and the SHA-256 of each checked Lean source. `provenance.json` maps it to the draft head. The later evidence-only commit retains these source hashes.

`lean_verification.log` preserves the completion verifier's actual output with timestamps. Every module built, every named theorem's axiom list passed the standard whitelist, all three `leanchecker` runs passed, and all four deliberately false statements failed mathematically.

Run `python3 scripts/verify_offset_completion.py` to produce a new report for a checkout. Read [the scope](../OFFSET_COMPLETION_SCOPE.md) and [work register](../LEAN_WORK_STATUS.md) before treating a passing conditional theorem as a physical result.
