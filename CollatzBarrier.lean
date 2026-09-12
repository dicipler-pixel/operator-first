import Mathlib

/-!
# Exact Collatz prefix barrier

Machine-checkable algebra extracted from the accelerated odd Collatz map.
This module proves only the exact finite-prefix identities and cross-multiplied
barrier statements. It does **not** claim the Collatz conjecture.
-/

namespace CollatzBarrier

/-- Prefix sum `A_j = a_0 + ... + a_{j-1}` of valuation exponents. -/
def prefixSum (a : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | j + 1 => prefixSum a j + a j

/-- Ordered affine correction
`B_j = Σ_{i<j} 3^(j-1-i) 2^(A_i)`, encoded by its exact recurrence. -/
def correction (a : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | j + 1 => 3 * correction a j + 2 ^ prefixSum a j

@[simp] theorem prefixSum_zero (a : ℕ → ℕ) : prefixSum a 0 = 0 := rfl
@[simp] theorem prefixSum_succ (a : ℕ → ℕ) (j : ℕ) :
    prefixSum a (j + 1) = prefixSum a j + a j := rfl

@[simp] theorem correction_zero (a : ℕ → ℕ) : correction a 0 = 0 := rfl
@[simp] theorem correction_succ (a : ℕ → ℕ) (j : ℕ) :
    correction a (j + 1) = 3 * correction a j + 2 ^ prefixSum a j := rfl

/-- Exact affine-prefix identity.

If the odd-step sequence satisfies
`2^(a_j) x_{j+1} = 3 x_j + 1`, then after `j` odd steps
`2^(A_j) x_j = 3^j x_0 + B_j` exactly. -/
theorem affine_prefix_identity (a x : ℕ → ℕ)
    (hstep : ∀ j, 2 ^ a j * x (j + 1) = 3 * x j + 1) :
    ∀ j, 2 ^ prefixSum a j * x j = 3 ^ j * x 0 + correction a j := by
  intro j
  induction j with
  | zero => simp
  | succ j ih =>
      rw [prefixSum_succ, correction_succ, pow_add]
      calc
        (2 ^ prefixSum a j * 2 ^ a j) * x (j + 1)
            = 2 ^ prefixSum a j * (2 ^ a j * x (j + 1)) := by ring
        _ = 2 ^ prefixSum a j * (3 * x j + 1) := by rw [hstep j]
        _ = 3 * (2 ^ prefixSum a j * x j) + 2 ^ prefixSum a j := by ring
        _ = 3 * (3 ^ j * x 0 + correction a j) + 2 ^ prefixSum a j := by rw [ih]
        _ = 3 ^ (j + 1) * x 0 + (3 * correction a j + 2 ^ prefixSum a j) := by
          rw [pow_succ]
          ring

/-- Cross-multiplied descent criterion.  This is the denominator-free form of
`n > B/(p-q)` and is preferable for formal arithmetic. -/
theorem descent_iff_cross {p q x n B : ℕ} (hp : 0 < p)
    (h : p * x = q * n + B) :
    x < n ↔ q * n + B < p * n := by
  rw [← h]
  exact (Nat.mul_lt_mul_left hp).symm

/-- Cross-multiplied return criterion. -/
theorem return_iff_cross {p q x n B : ℕ} (hp : 0 < p)
    (h : p * x = q * n + B) :
    x = n ↔ q * n + B = p * n := by
  rw [← h]
  constructor
  · intro hxn
    rw [hxn]
  · intro hmul
    exact Nat.eq_of_mul_eq_mul_left hp hmul

/-- Cross-multiplied growth criterion. -/
theorem growth_iff_cross {p q x n B : ℕ} (hp : 0 < p)
    (h : p * x = q * n + B) :
    n < x ↔ p * n < q * n + B := by
  rw [← h]
  exact (Nat.mul_lt_mul_left hp).symm

/-- Collatz prefix descent written with the exact ordered correction. -/
theorem collatz_prefix_descent_iff (a x : ℕ → ℕ)
    (hstep : ∀ j, 2 ^ a j * x (j + 1) = 3 * x j + 1) (j : ℕ) :
    x j < x 0 ↔
      3 ^ j * x 0 + correction a j < 2 ^ prefixSum a j * x 0 := by
  apply descent_iff_cross (p := 2 ^ prefixSum a j) (q := 3 ^ j)
      (B := correction a j)
  · positivity
  · exact affine_prefix_identity a x hstep j

/-- Collatz prefix return written with the exact ordered correction. -/
theorem collatz_prefix_return_iff (a x : ℕ → ℕ)
    (hstep : ∀ j, 2 ^ a j * x (j + 1) = 3 * x j + 1) (j : ℕ) :
    x j = x 0 ↔
      3 ^ j * x 0 + correction a j = 2 ^ prefixSum a j * x 0 := by
  apply return_iff_cross (p := 2 ^ prefixSum a j) (q := 3 ^ j)
      (B := correction a j)
  · positivity
  · exact affine_prefix_identity a x hstep j

end CollatzBarrier

#print axioms CollatzBarrier.affine_prefix_identity
#print axioms CollatzBarrier.descent_iff_cross
#print axioms CollatzBarrier.return_iff_cross
#print axioms CollatzBarrier.growth_iff_cross
#print axioms CollatzBarrier.collatz_prefix_descent_iff
#print axioms CollatzBarrier.collatz_prefix_return_iff
