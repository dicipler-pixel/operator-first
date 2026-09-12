import Mathlib

/-!
# Exact Collatz prefix barrier

Machine-checkable algebra extracted from the accelerated odd Collatz map.
This module proves only exact finite-prefix identities and envelope inequalities.
It does **not** claim the Collatz conjecture.
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

/-- Envelope correction with prescribed exponent caps `u_j`. -/
def envelopeCorrection (u : ℕ → ℕ) : ℕ → ℕ
  | 0 => 0
  | j + 1 => 3 * envelopeCorrection u j + 2 ^ u j

@[simp] theorem prefixSum_zero (a : ℕ → ℕ) : prefixSum a 0 = 0 := rfl
@[simp] theorem prefixSum_succ (a : ℕ → ℕ) (j : ℕ) :
    prefixSum a (j + 1) = prefixSum a j + a j := rfl

@[simp] theorem correction_zero (a : ℕ → ℕ) : correction a 0 = 0 := rfl
@[simp] theorem correction_succ (a : ℕ → ℕ) (j : ℕ) :
    correction a (j + 1) = 3 * correction a j + 2 ^ prefixSum a j := rfl

@[simp] theorem envelopeCorrection_zero (u : ℕ → ℕ) : envelopeCorrection u 0 = 0 := rfl
@[simp] theorem envelopeCorrection_succ (u : ℕ → ℕ) (j : ℕ) :
    envelopeCorrection u (j + 1) = 3 * envelopeCorrection u j + 2 ^ u j := rfl

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

/-- Finite-prefix version of `affine_prefix_identity`.
Only the step equations before the requested endpoint are needed. -/
theorem affine_prefix_identity_finite (a x : ℕ → ℕ) :
    ∀ j, (∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1) →
      2 ^ prefixSum a j * x j = 3 ^ j * x 0 + correction a j := by
  intro j
  induction j with
  | zero => simp
  | succ j ih =>
      intro hstep
      have hprev : 2 ^ prefixSum a j * x j = 3 ^ j * x 0 + correction a j :=
        ih (fun i hi => hstep i (Nat.lt_trans hi (Nat.lt_succ_self j)))
      rw [prefixSum_succ, correction_succ, pow_add]
      calc
        (2 ^ prefixSum a j * 2 ^ a j) * x (j + 1)
            = 2 ^ prefixSum a j * (2 ^ a j * x (j + 1)) := by ring
        _ = 2 ^ prefixSum a j * (3 * x j + 1) := by
          rw [hstep j (Nat.lt_succ_self j)]
        _ = 3 * (2 ^ prefixSum a j * x j) + 2 ^ prefixSum a j := by ring
        _ = 3 * (3 ^ j * x 0 + correction a j) + 2 ^ prefixSum a j := by rw [hprev]
        _ = 3 ^ (j + 1) * x 0 + (3 * correction a j + 2 ^ prefixSum a j) := by
          rw [pow_succ]
          ring

/-- Cross-multiplied descent criterion. This is the denominator-free form of
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

/-- Exact survival criterion at a multiplicatively contractive endpoint.
When `q ≤ p`, survival `n ≤ x` is equivalent to the denominator-free barrier
condition `(p-q)n ≤ B`. -/
theorem survival_iff_gap {p q x n B : ℕ} (hp : 0 < p) (hqp : q ≤ p)
    (h : p * x = q * n + B) :
    n ≤ x ↔ (p - q) * n ≤ B := by
  constructor
  · intro hstay
    have hsurvival : p * n ≤ q * n + B := by
      calc
        p * n ≤ p * x := Nat.mul_le_mul_left p hstay
        _ = q * n + B := h
    have hsum : (p - q) * n + q * n ≤ B + q * n := by
      calc
        (p - q) * n + q * n = p * n := by
          rw [← Nat.add_mul, Nat.sub_add_cancel hqp]
        _ ≤ q * n + B := hsurvival
        _ = B + q * n := Nat.add_comm _ _
    exact Nat.le_of_add_le_add_right hsum
  · intro hgap
    have hsurvival : p * n ≤ q * n + B := by
      calc
        p * n = (p - q) * n + q * n := by
          rw [← Nat.add_mul, Nat.sub_add_cancel hqp]
        _ ≤ B + q * n := Nat.add_le_add_right hgap _
        _ = q * n + B := Nat.add_comm _ _
    rw [← h] at hsurvival
    exact Nat.le_of_mul_le_mul_left hsurvival hp

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

/-- At any prefix for which `3^j ≤ 2^A_j`, survival above the initial seed is
exactly the integer power-gap barrier `(2^A_j-3^j)x₀ ≤ B_j`. -/
theorem collatz_prefix_survival_iff_gap (a x : ℕ → ℕ)
    (hstep : ∀ j, 2 ^ a j * x (j + 1) = 3 * x j + 1) (j : ℕ)
    (hpow : 3 ^ j ≤ 2 ^ prefixSum a j) :
    x 0 ≤ x j ↔
      (2 ^ prefixSum a j - 3 ^ j) * x 0 ≤ correction a j := by
  apply survival_iff_gap (p := 2 ^ prefixSum a j) (q := 3 ^ j)
      (B := correction a j)
  · positivity
  · exact hpow
  · exact affine_prefix_identity a x hstep j

/-- Monotonicity of the ordered correction under pointwise prefix-power caps.
This is the algebraic core of the saturated first-contraction envelope. -/
theorem correction_le_envelope (a u : ℕ → ℕ) :
    ∀ m, (∀ i < m, 2 ^ prefixSum a i ≤ 2 ^ u i) →
      correction a m ≤ envelopeCorrection u m := by
  intro m
  induction m with
  | zero => simp
  | succ m ih =>
      intro hcap
      have hprev : correction a m ≤ envelopeCorrection u m :=
        ih (fun i hi => hcap i (Nat.lt_trans hi (Nat.lt_succ_self m)))
      have hlast : 2 ^ prefixSum a m ≤ 2 ^ u m := hcap m (Nat.lt_succ_self m)
      rw [correction_succ, envelopeCorrection_succ]
      exact Nat.add_le_add (Nat.mul_le_mul_left 3 hprev) hlast

/-- Generic survival-envelope inequality.

If a prefix has not descended, its terminal divisor power is at least `2^L`,
and every earlier correction term is bounded by an envelope, then the seed
must satisfy the corresponding cross-multiplied survival inequality. -/
theorem survival_le_envelope (a u x : ℕ → ℕ)
    (hstep : ∀ j, 2 ^ a j * x (j + 1) = 3 * x j + 1)
    (m L : ℕ)
    (hstay : x 0 ≤ x m)
    (hterminal : 2 ^ L ≤ 2 ^ prefixSum a m)
    (hcap : ∀ i < m, 2 ^ prefixSum a i ≤ 2 ^ u i) :
    2 ^ L * x 0 ≤ 3 ^ m * x 0 + envelopeCorrection u m := by
  have hcorr : correction a m ≤ envelopeCorrection u m :=
    correction_le_envelope a u m hcap
  calc
    2 ^ L * x 0 ≤ 2 ^ prefixSum a m * x 0 := Nat.mul_le_mul_right _ hterminal
    _ ≤ 2 ^ prefixSum a m * x m := Nat.mul_le_mul_left _ hstay
    _ = 3 ^ m * x 0 + correction a m := affine_prefix_identity a x hstep m
    _ ≤ 3 ^ m * x 0 + envelopeCorrection u m := Nat.add_le_add_left hcorr _

/-- Direct power-gap form of the survival envelope.

Once `3^m ≤ 2^L`, a prefix that has not descended must satisfy
`(2^L - 3^m) * x_0 ≤ envelopeCorrection u m`. This is the exact integer
Diophantine obstruction behind the saturated barrier denominator. -/
theorem survival_gap_bound (a u x : ℕ → ℕ)
    (hstep : ∀ j, 2 ^ a j * x (j + 1) = 3 * x j + 1)
    (m L : ℕ)
    (hpow : 3 ^ m ≤ 2 ^ L)
    (hstay : x 0 ≤ x m)
    (hterminal : 2 ^ L ≤ 2 ^ prefixSum a m)
    (hcap : ∀ i < m, 2 ^ prefixSum a i ≤ 2 ^ u i) :
    (2 ^ L - 3 ^ m) * x 0 ≤ envelopeCorrection u m := by
  have hsurvival :
      2 ^ L * x 0 ≤ 3 ^ m * x 0 + envelopeCorrection u m :=
    survival_le_envelope a u x hstep m L hstay hterminal hcap
  have hsum :
      (2 ^ L - 3 ^ m) * x 0 + 3 ^ m * x 0 ≤
        envelopeCorrection u m + 3 ^ m * x 0 := by
    calc
      (2 ^ L - 3 ^ m) * x 0 + 3 ^ m * x 0 = 2 ^ L * x 0 := by
        rw [← Nat.add_mul, Nat.sub_add_cancel hpow]
      _ ≤ 3 ^ m * x 0 + envelopeCorrection u m := hsurvival
      _ = envelopeCorrection u m + 3 ^ m * x 0 := Nat.add_comm _ _
  exact Nat.le_of_add_le_add_right hsum

/-- Finite exclusion certificate obtained from the exact power gap.

If the envelope is strictly smaller than `(2^L-3^m)N`, then no seed `x_0`
that survives the prefix can be at least `N`. -/
theorem seed_lt_of_survival_gap_certificate (a u x : ℕ → ℕ)
    (hstep : ∀ j, 2 ^ a j * x (j + 1) = 3 * x j + 1)
    (m L N : ℕ)
    (hpow : 3 ^ m ≤ 2 ^ L)
    (hgap : 0 < 2 ^ L - 3 ^ m)
    (hstay : x 0 ≤ x m)
    (hterminal : 2 ^ L ≤ 2 ^ prefixSum a m)
    (hcap : ∀ i < m, 2 ^ prefixSum a i ≤ 2 ^ u i)
    (hcertificate : envelopeCorrection u m < (2 ^ L - 3 ^ m) * N) :
    x 0 < N := by
  have hmul : (2 ^ L - 3 ^ m) * x 0 ≤ envelopeCorrection u m :=
    survival_gap_bound a u x hstep m L hpow hstay hterminal hcap
  have hstrict :
      (2 ^ L - 3 ^ m) * x 0 < (2 ^ L - 3 ^ m) * N :=
    lt_of_le_of_lt hmul hcertificate
  exact (Nat.mul_lt_mul_left hgap).mp hstrict

end CollatzBarrier

#print axioms CollatzBarrier.affine_prefix_identity
#print axioms CollatzBarrier.affine_prefix_identity_finite
#print axioms CollatzBarrier.descent_iff_cross
#print axioms CollatzBarrier.return_iff_cross
#print axioms CollatzBarrier.growth_iff_cross
#print axioms CollatzBarrier.survival_iff_gap
#print axioms CollatzBarrier.collatz_prefix_descent_iff
#print axioms CollatzBarrier.collatz_prefix_return_iff
#print axioms CollatzBarrier.collatz_prefix_survival_iff_gap
#print axioms CollatzBarrier.correction_le_envelope
#print axioms CollatzBarrier.survival_le_envelope
#print axioms CollatzBarrier.survival_gap_bound
#print axioms CollatzBarrier.seed_lt_of_survival_gap_certificate
