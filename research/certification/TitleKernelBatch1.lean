import Mathlib

/-!
# Jeromie Beasley title certification — batch 1

These are deliberately small source-faithful kernels. A green theorem certifies
only the exact statement written here, not the surrounding physical or research
interpretation.
-/

namespace JBTitleCert

/-- `JB-SPACING-001`.
A common additive offset does not change a difference. This is the algebraic
kernel of the statement that an identity shift moves every level together while
leaving level spacings unchanged. -/
theorem spacing_invariant_under_common_shift {R : Type*} [AddCommGroup R]
    (a b c : R) :
    (a + c) - (b + c) = a - b := by
  abel

/-- `JB-FOFT24-001`.
If the two baseline shifts commute with the opposite dynamical factors and with
one another, then adding those baseline pieces does not change the commutator.
For scalar multiples of the identity these hypotheses are automatic. -/
theorem commutator_invariant_under_central_shifts {R : Type*} [Ring R]
    (A B z w : R)
    (hzB : z * B = B * z)
    (hwA : w * A = A * w)
    (hzw : z * w = w * z) :
    (A + z) * (B + w) - (B + w) * (A + z) = A * B - B * A := by
  calc
    (A + z) * (B + w) - (B + w) * (A + z)
        = A * B + A * w + z * B + z * w -
          (B * A + B * z + w * A + w * z) := by
            noncomm_ring
    _ = A * B - B * A := by
      rw [hzB, hwA, hzw]
      noncomm_ring

/-- `JB-CONE7-001`.
At a Hermitian point the round-trip scalar contribution has the form
`|M|^2 / Delta^2`; this scalar kernel is nonnegative. -/
theorem hermitian_round_trip_weight_nonneg (M : ℂ) (Delta : ℝ) :
    0 ≤ ‖M‖ ^ 2 / Delta ^ 2 := by
  positivity

#print axioms JBTitleCert.spacing_invariant_under_common_shift
#print axioms JBTitleCert.commutator_invariant_under_central_shifts
#print axioms JBTitleCert.hermitian_round_trip_weight_nonneg

end JBTitleCert
