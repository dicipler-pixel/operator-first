# Offset moduli transfer

The complete all-size argument is in
[ALL_SIZE_TRANSFER.md](ALL_SIZE_TRANSFER.md).

The odd-block determinant is exactly affine in the onsite imbalance v when
the two bulk invariants are fixed. Consequently the determinant asymmetry
and the sign-corrected endpoint remainder both scale by v/e relative to the
equal-hopping reference.

This directory contains a mathematical proof, a runnable verifier, and a
saved local verification report. It does not contain old manuscript versions.
No new Lean certification is claimed.

## Reproduce

~~~sh
python3 -m pip install sympy==1.14.0 mpmath==1.3.0
python3 moduli_transfer/verify_moduli_transfer.py
~~~

Run from the repository root. An alternative report location can be passed
with the --out argument. The script needs no source editing.

The checks cover:

- The explicit transformed matrix and its column degree bounds.
- Fully symbolic characteristic polynomials through five sites.
- Exact rational determinant pencils through eleven sites.
- Failure of the claimed extension to even blocks and asymmetric boundaries.
- Direct Fourier-covariance determinant checks at 12 angles and four odd
  block lengths, with 200-digit arithmetic.

The saved local report records PASS, including a maximum physical relative
determinant discrepancy of approximately 4.365e-182. Numerical precision is
not an interval certificate. The proof for arbitrary size is the argument
in the note, not an extrapolation from these finite checks.

The dedicated GitHub workflow repeats these checks and uploads its report.
Existing Lean workflows continue checking the unchanged formal statements.
The new all-size proof still needs Lean formalization. The sharp remainder
law and cosmological calibration also remain open.
