import Mathlib

/-!
# Stable fixed modes do not bound resolvent amplification

This is a deliberately finite-dimensional theorem for proof auditing and
linearized-flow diagnostics. It does **not** prove Navier--Stokes blowup or
regularity.

For the two-component upper-triangular family

    H_k(x,y) = (-x + k y, -2 y),

the modal eigenvalues remain fixed at `-1` and `-2` for every shear parameter
`k`. Nevertheless the exact resolvent at `z = 0`, namely `(-H_k)^{-1}`, has
arbitrarily large response as `k` grows.

The scoped lesson is useful for fluid stability: strictly stable modal
eigenvalues alone do not bound forced/resolvent amplification for a non-normal
family.
-/

set_option autoImplicit false
noncomputable section

namespace SabineNSAudit

/-- Stable upper-triangular two-mode operator `H_k(x,y) = (-x + k y, -2y)`. -/
def H (k : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  (-v.1 + k * v.2, -2 * v.2)

/-- The zero-frequency resolvent denominator `0 I - H_k = -H_k`. -/
def shiftedZero (k : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  (v.1 - k * v.2, 2 * v.2)

/-- The explicit inverse `(-H_k)^{-1}`. -/
def resolventZero (k : ℝ) (v : ℝ × ℝ) : ℝ × ℝ :=
  (v.1 + (k / 2) * v.2, v.2 / 2)

/--
For every requested amplification threshold `M ≥ 0`, there is a member of one
fixed stable modal family whose zero-frequency resolvent response exceeds `M`
in squared Euclidean size.

The theorem simultaneously certifies:
* the fixed eigenmode `(1,0)` with eigenvalue `-1`;
* the fixed second eigenvalue `-2`, witnessed by eigenvector `(-k,1)`;
* an exact two-sided inverse for `-H_k`;
* arbitrarily large resolvent response on the test vector `(0,1)`.
-/
theorem stable_modes_do_not_bound_resolvent (M : ℝ) (hM : 0 ≤ M) :
    ∃ k : ℝ,
      H k (1, 0) = (-1, 0) ∧
      H k (-k, 1) = (2 * k, -2) ∧
      (∀ v : ℝ × ℝ,
        shiftedZero k (resolventZero k v) = v ∧
        resolventZero k (shiftedZero k v) = v) ∧
      M < (resolventZero k (0, 1)).1 ^ 2 +
          (resolventZero k (0, 1)).2 ^ 2 := by
  refine ⟨2 * (M + 1), ?_, ?_, ?_, ?_⟩
  · simp [H]
  · simp [H]
    ring
  · intro v
    constructor <;> ext <;> simp [shiftedZero, resolventZero] <;> ring
  · simp [resolventZero]
    nlinarith [sq_nonneg M]

#print axioms SabineNSAudit.stable_modes_do_not_bound_resolvent

end SabineNSAudit
