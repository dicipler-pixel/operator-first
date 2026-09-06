# Finite gravity projector results

Draft follow-up to the proof infrastructure in PR #7. No merges authorized.

`Gravity.lean` contains 23 accepted theorems. The successful build, per-theorem
axiom audit, independent leanchecker pass, and four rejected false controls are:
https://github.com/dicipler-pixel/operator-first/actions/runs/34034999150
Verified source commit: 39bb1ffccdd54d48244da206f7b5fa2e574604ec.

Run `python3 scripts/verify_gravity.py` after installing the pinned Lean/mathlib
and obtaining its cache. The module covers tangent block algebra, signed-square
coordinates, reciprocal determinant constraints, a bounded-remainder cap step,
complex projector chart identities, metric signs, and exact counterexamples.
It does not formalize the full C² Taylor argument, tangent manifold dimension,
contour functional calculus, or a gravitational field equation.

Install `scripts/gravity_requirements.txt`, then run
`python3 scripts/check_gravity.py`. Its 31 exact/numerical checks write
`evidence/new_checks.json`. The fifteen supplied reproducible gates are under
`gravity/gates/`; run each from that directory with one BLAS thread. They are
numerical programs, not Lean proofs. GEOWALL-ROT-01 retains a failed sign-change
prediction; GEOWALL-LEDGER-02 changes tangent probes at a fixed base operator.
The v4 manuscript gives the corrected interpretation.

The paper and its seven preserved images are delivered separately as dark HTML
and PDF. The publication supplement contains current proof sources and code,
not prior manuscript versions. Formal verification is evidence of the stated
finite algebra, not a novelty or physical-validity certificate.
