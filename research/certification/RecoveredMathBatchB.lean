import Mathlib

/-!
# Recovered math batch B

Hamiltonian/variational algebra and the first geometry negative control.
These are exact kernels only; no physical dictionary is certified by this file.
-/

namespace RecoveredMathBatchB

/-! ## B1. Real oscillator Lagrangian and Legendre algebra -/

/-- Real one-degree-of-freedom oscillator Lagrangian with an external scalar
potential value `V`. -/
noncomputable def oscillatorL (m omega q qdot V : ℝ) : ℝ :=
  (1 / 2 : ℝ) * m * qdot ^ 2 -
  (1 / 2 : ℝ) * m * omega ^ 2 * q ^ 2 - V

/-- For the quadratic kinetic term, the canonical momentum is `m*qdot`.
This theorem records the algebraic target used by the calculus derivation. -/
def canonicalP (m qdot : ℝ) : ℝ := m * qdot

/-- Substituting `p=m*qdot` into `H=p*qdot-L` gives kinetic plus potential
energy for the real oscillator model. -/
theorem legendre_transform_oscillator
    (m omega q qdot V : ℝ) :
    canonicalP m qdot * qdot - oscillatorL m omega q qdot V =
      (1 / 2 : ℝ) * m * qdot ^ 2 +
      (1 / 2 : ℝ) * m * omega ^ 2 * q ^ 2 + V := by
  unfold canonicalP oscillatorL
  ring

/-- If `m >= 0` and the external potential contribution is nonnegative, the
standard oscillator Hamiltonian is nonnegative. -/
theorem oscillator_hamiltonian_nonnegative
    (m omega q qdot V : ℝ) (hm : 0 ≤ m) (hV : 0 ≤ V) :
    0 ≤ (1 / 2 : ℝ) * m * qdot ^ 2 +
      (1 / 2 : ℝ) * m * omega ^ 2 * q ^ 2 + V := by
  positivity

/-! ## B2. Euler-Lagrange algebraic normal form -/

/-- Algebraic normalization of the real oscillator equation. This does not by
itself prove the Euler-Lagrange theorem; it proves the division-by-mass step
once the variational equation has been obtained. -/
theorem oscillator_equation_divide_mass
    (m qddot omega q dV : ℝ) (hm : m ≠ 0)
    (hEq : m * qddot + m * omega ^ 2 * q + dV = 0) :
    qddot + omega ^ 2 * q + dV / m = 0 := by
  field_simp [hm]
  nlinarith

/-! ## D2. Geometry negative control -/

/-- The determinant of a two-dimensional outer-product matrix
`[[a^2,ab],[ab,b^2]]` is zero. This is the exact 2D kernel behind the warning
that `g_{μν}=∂_μ Psi ∂_ν Psi` is degenerate when built from a single scalar
gradient. -/
theorem outer_product_two_by_two_det_zero (a b : ℝ) :
    (a * a) * (b * b) - (a * b) * (a * b) = 0 := by
  ring

/-- More generally, every 2x2 minor of a rank-one outer product vanishes. -/
theorem outer_product_minor_zero (a b c d : ℝ) :
    (a * c) * (b * d) - (a * d) * (b * c) = 0 := by
  ring

/-! ## First Lyapunov algebra kernels -/

/-- Squared distance is nonnegative. -/
theorem lyapunov_distance_nonnegative (x x0 : ℝ) :
    0 ≤ (x - x0) ^ 2 := by
  positivity

/-- Strict positivity away from the equilibrium point. -/
theorem lyapunov_distance_pos_of_ne (x x0 : ℝ) (h : x ≠ x0) :
    0 < (x - x0) ^ 2 := by
  have hsub : x - x0 ≠ 0 := sub_ne_zero.mpr h
  exact sq_pos_of_ne_zero hsub

/-- The distance-square term vanishes exactly at equilibrium. -/
theorem lyapunov_distance_eq_zero_iff (x x0 : ℝ) :
    (x - x0) ^ 2 = 0 ↔ x = x0 := by
  constructor
  · intro h
    have hx : x - x0 = 0 := by nlinarith
    exact sub_eq_zero.mp hx
  · intro h
    simp [h]

#print axioms RecoveredMathBatchB.legendre_transform_oscillator
#print axioms RecoveredMathBatchB.oscillator_hamiltonian_nonnegative
#print axioms RecoveredMathBatchB.oscillator_equation_divide_mass
#print axioms RecoveredMathBatchB.outer_product_two_by_two_det_zero
#print axioms RecoveredMathBatchB.outer_product_minor_zero
#print axioms RecoveredMathBatchB.lyapunov_distance_nonnegative
#print axioms RecoveredMathBatchB.lyapunov_distance_pos_of_ne
#print axioms RecoveredMathBatchB.lyapunov_distance_eq_zero_iff

end RecoveredMathBatchB
