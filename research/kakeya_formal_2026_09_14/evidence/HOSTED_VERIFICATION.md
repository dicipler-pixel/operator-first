# Hosted Kakeya verification — 14 September 2026

**PASS** for proof head `6a2c3bdce1e8d983a132d23887802320b4760ce6`.
GitHub checked merge revision `b2d3db07806e19cf018873ec7617163a4244b500`.

- [Draft PR 62](https://github.com/dicipler-pixel/operator-first/pull/62)
- [Successful dedicated workflow run34834518645](https://github.com/dicipler-pixel/operator-first/actions/runs/34834518645)
- [Proof package and original development archive](https://github.com/dicipler-pixel/operator-first/tree/6a2c3bdce1e8d983a132d23887802320b4760ce6/research/kakeya_formal_2026_09_14)
- [Permanent hosted evidence and mixer events](hosted_replay_and_mixer_records.tar.xz)
- [Archive manifest](HOSTED_ARCHIVE_MANIFEST.json)
- [Hosted verifier report](HOSTED_REPORT.json)

All five modules compiled on the ordinary hosted Lean4.33.0 toolchain and
passed `leanchecker -v`. The audit covered121 declarations by their defining
modules, including generated declarations;33 are top-level source lemmas and
controls. The axiom union is only `propext`, `Classical.choice`, `Quot.sound`.
Both deliberately false claims were mathematically rejected. All gated source
hashes in the hosted receipt match the submitted source files exactly.

The receipt was recovered through the job-log path after the direct artifact
transport failed. All24 receipt members were checked against byte counts and
SHA256. Receipt SHA256:
`b23b528f3bdfc124409a2916cc56155c64f307830e102fc288f5501af9762c8e`.
This is a TAR/XZ receipt, distinct from the temporary GitHub ZIP artifact.

The permanent43-file archive also includes the complete earlier and final
job logs, transport failures, recorder inputs, and the exact two-observation
and one-run deltas appended through the unchanged mixer tools. Recover the
original154-file archive from the proof package, then run the included
`replay_ci_ledgers.py INSTRUMENT_DIRECTORY` to append the CI deltas. It verifies
the base and final hashes and refuses an unfamiliar ledger. Actual replay
matched the working ledgers byte-for-byte; a second replay added no duplicates.

The scientific scope is finite two-coordinate **nonzero-multiple** forcing.
Completion implies the necessary independent-label cut condition. The
literal unit-target PDF rule, sufficiency of cuts, a winning score, new
exponent and transport/geometry connection are not certified by this result.
This is a downstream mathlib-based supplement, with its assumptions exposed
in the definition audit.

This evidence branch records results for the proof head above. Its own
documentation-only archival commit is not a new proof certification or merge
into `main`.
