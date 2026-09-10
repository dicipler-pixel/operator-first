import Mathlib

/-!
# A fixed-mode / unbounded-resolvent audit lemma

This is a deliberately finite-dimensional theorem for proof auditing and
linearized-flow diagnostics.  It does **not** prove Navier--Stokes blowup or
regularity.

For the two-component family

    H_k(x,y) = (k y, y),

the vectors `(1,0)` and `(k,1)` are fixed eigenmodes with eigenvalues `0` and
`1`, respectively, for every shear parameter `k`.  Nevertheless the exact
inverse of `(1/2)I - H_k` has arbitrarily large response as `k` grows.

The point is scoped but useful: fixed modal eigenvalue information alone does
not bound resolvent amplification for a non-normal family.
-/

set_option autoImplicit false

namespace SabineNSAudit

/-- Upper-triangular two-mode operator `H_k(x,y) = (k y, y)`. -/
def H (k : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  (k * v.2, v.2)

/-- The shifted operator `(1/2)I - H_k`, written componentwise. -/
def shiftedHalf (k : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  (v.1 / 2 - k * v.2, -v.2 / 2)

/-- The explicit inverse of `(1/2)I - H_k`. -/
def resolventHalf (k : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  (2 * v.1 - 4 * k * v.2, -2 * v.2)

/--
For every requested amplification threshold `M ≥ 0`, there is a member of the
same fixed-mode family whose resolvent response at `z = 1/2` exceeds `M` in
squared Euclidean size.

The theorem simultaneously certifies:
* a `0`-mode `(1,0)`;
* a `1`-mode `(k,1)`;
* an exact two-sided inverse for `(1/2)I - H_k`;
* arbitrarily large resolvent response on the test vector `(0,1)`.
-/
theorem fixed_modes_do_not_bound_resolvent (M : ℝ) (hM : 0 ≤ M) :
    ∃ k : ℝ,
      H k (1, 0) = (0, 0) ∧
      H k (k, 1) = (k, 1) ∧
      (∀ v : ℝ × ℝ,
        shiftedHalf k (resolventHalf k v) = v ∧
        resolventHalf k (shiftedHalf k v) = v) ∧
      M < (resolventHalf k (0, 1)).1 ^ 2 +
          (resolventHalf k (0, 1)).2 ^ 2 := by
  refine ⟨M + 1, ?_, ?_, ?_, ?_⟩
  · simp [H]
  · simp [H]
  · intro v
    constructor <;> ext <;> simp [shiftedHalf, resolventHalf] <;> ring
  · simp [resolventHalf]
    nlinarith [sq_nonneg M]

#print axioms SabineNSAudit.fixed_modes_do_not_bound_resolvent

end SabineNSAudit
