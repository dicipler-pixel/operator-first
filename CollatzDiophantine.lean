import Mathlib

/-!
# Exact Collatz Diophantine gap certificates

This module isolates the denominator-free arithmetic that turns a survival
inequality into a bound controlled by the integer power gap `P - Q`.

For the saturated Collatz barrier the intended specialization is
`P = 2^p`, `Q = 3^m`, and `C` equal to the saturated envelope correction.
No statement here asserts the Collatz conjecture.
-/

namespace CollatzDiophantine

/-- If `Q ≤ P` and survival gives `P*n ≤ Q*n + C`, then the entire seed is
controlled by the exact integer gap: `(P-Q)*n ≤ C`. -/
theorem gap_mul_le_of_survival {P Q n C : ℕ}
    (hQP : Q ≤ P)
    (hsurvival : P * n ≤ Q * n + C) :
    (P - Q) * n ≤ C := by
  have hsum : (P - Q) * n + Q * n ≤ C + Q * n := by
    calc
      (P - Q) * n + Q * n = P * n := by
        rw [← Nat.add_mul, Nat.sub_add_cancel hQP]
      _ ≤ Q * n + C := hsurvival
      _ = C + Q * n := Nat.add_comm _ _
  exact Nat.le_of_add_le_add_right hsum

/-- A finite exclusion certificate.  If the envelope is already smaller than
`(P-Q)*N`, then no surviving seed can be as large as `N`. -/
theorem seed_lt_of_gap_certificate {P Q n C N : ℕ}
    (hQP : Q ≤ P)
    (hgap : 0 < P - Q)
    (hsurvival : P * n ≤ Q * n + C)
    (hcertificate : C < (P - Q) * N) :
    n < N := by
  have hmul : (P - Q) * n ≤ C :=
    gap_mul_le_of_survival hQP hsurvival
  have hstrict : (P - Q) * n < (P - Q) * N :=
    lt_of_le_of_lt hmul hcertificate
  exact (Nat.mul_lt_mul_left hgap).mp hstrict

/-- Exact cross-multiplication test for comparing two positive rational
barriers `C₁/g₁` and `C₂/g₂`, stated without division. -/
theorem barrier_lt_iff_cross {C₁ C₂ g₁ g₂ : ℕ}
    (hg₁ : 0 < g₁) (hg₂ : 0 < g₂) :
    (C₁ : ℚ) / g₁ < (C₂ : ℚ) / g₂ ↔ C₁ * g₂ < C₂ * g₁ := by
  norm_num [div_lt_div_iff₀, hg₁, hg₂]

end CollatzDiophantine

#print axioms CollatzDiophantine.gap_mul_le_of_survival
#print axioms CollatzDiophantine.seed_lt_of_gap_certificate
#print axioms CollatzDiophantine.barrier_lt_iff_cross
