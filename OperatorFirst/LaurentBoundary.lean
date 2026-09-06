import Mathlib

/-!
# The arbitrary-size boundary-column degree bound

Formal support bounds for Laurent polynomials and determinants. No size cutoff,
positivity assumption, or covariance interpretation is used. This module proves
the determinant-degree step of ALL_SIZE_TRANSFER.md; it does not assume the
physical sine law as an axiom.
-/

noncomputable section
open scoped BigOperators
open LaurentPolynomial

namespace OperatorFirst.LaurentBoundary

variable {R : Type*} [CommRing R]

/-- Every coefficient strictly above the integer bound is zero. -/
def Bounded (f : LaurentPolynomial R) (d : ℤ) : Prop :=
  ∀ k : ℤ, d < k → f.coeff k = 0

theorem bounded_zero (d : ℤ) : Bounded (0 : LaurentPolynomial R) d := by
  intro k hk
  simp

theorem bounded_mono {f : LaurentPolynomial R} {a b : ℤ}
    (hf : Bounded f a) (hab : a ≤ b) : Bounded f b := by
  intro k hk
  exact hf k (lt_of_le_of_lt hab hk)

theorem bounded_C (a : R) : Bounded (C a) 0 := by
  intro k hk
  simp [C_apply, ne_of_gt hk]

theorem bounded_monomial (a : R) (d : ℤ) : Bounded (C a * T d) d := by
  intro k hk
  rw [← single_eq_C_mul_T]
  simp [AddMonoidAlgebra.coeff_single, ne_of_gt hk]

theorem bounded_add {f g : LaurentPolynomial R} {d : ℤ}
    (hf : Bounded f d) (hg : Bounded g d) : Bounded (f + g) d := by
  intro k hk
  simp [AddMonoidAlgebra.coeff_add, hf k hk, hg k hk]

theorem bounded_neg {f : LaurentPolynomial R} {d : ℤ}
    (hf : Bounded f d) : Bounded (-f) d := by
  intro k hk
  simp [AddMonoidAlgebra.coeff_neg, hf k hk]

theorem bounded_mul {f g : LaurentPolynomial R} {a b : ℤ}
    (hf : Bounded f a) (hg : Bounded g b) : Bounded (f * g) (a + b) := by
  classical
  intro k hk
  rw [AddMonoidAlgebra.coeff_mul_apply_left]
  apply Finset.sum_eq_zero
  intro i hi
  have hi' : f.coeff i ≠ 0 := Finsupp.mem_support_iff.mp hi
  have hia : i ≤ a := by
    by_contra hn
    exact hi' (hf i (lt_of_not_ge hn))
  rw [hg (-i + k) (by omega), mul_zero]

theorem bounded_sum {ι : Type*} (s : Finset ι)
    (f : ι → LaurentPolynomial R) (d : ℤ)
    (hf : ∀ i ∈ s, Bounded (f i) d) : Bounded (∑ i ∈ s, f i) d := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using bounded_zero (R := R) d
  | @insert i s hi ih =>
    rw [Finset.sum_insert hi]
    exact bounded_add (hf i (Finset.mem_insert_self i s))
      (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))

theorem bounded_prod {ι : Type*} (s : Finset ι)
    (f : ι → LaurentPolynomial R) (d : ι → ℤ)
    (hf : ∀ i ∈ s, Bounded (f i) (d i)) :
    Bounded (∏ i ∈ s, f i) (∑ i ∈ s, d i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using bounded_C (1 : R)
  | @insert i s hi ih =>
    rw [Finset.prod_insert hi, Finset.sum_insert hi]
    exact bounded_mul (hf i (Finset.mem_insert_self i s))
      (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))

/-- Each determinant term spends the degree budget of each column exactly once. -/
theorem determinant_column_bound {ι : Type*} [Fintype ι] [DecidableEq ι]
    (M : Matrix ι ι (LaurentPolynomial R)) (d : ι → ℤ)
    (hM : ∀ i j, Bounded (M i j) (d j)) :
    Bounded M.det (∑ j, d j) := by
  classical
  rw [Matrix.det_apply']
  apply bounded_sum
  intro σ hσ
  have hp := bounded_prod Finset.univ (fun j => M (σ j) j) d
    (fun j _ => hM (σ j) j)
  have hs : Bounded ((Equiv.Perm.sign σ : ℤ) : LaurentPolynomial R) 0 := by
    simpa using bounded_C ((Equiv.Perm.sign σ : ℤ) : R)
  simpa using bounded_mul hs hp

/-- One distinguished column allows at most degree one, in every finite size. -/
theorem determinant_one_boundary_column {ι : Type*} [Fintype ι] [DecidableEq ι]
    (M : Matrix ι ι (LaurentPolynomial R)) (b : ι)
    (hbulk : ∀ i j, j ≠ b → Bounded (M i j) 0)
    (hboundary : ∀ i, Bounded (M i b) 1) : Bounded M.det 1 := by
  classical
  have h := determinant_column_bound M (fun j => if j = b then 1 else 0)
    (by intro i j; by_cases hj : j = b <;> simp [hj, hbulk, hboundary])
  simpa using h

/-- The same argument bounds growth by the number of degree-one boundary columns. -/
theorem determinant_boundary_set {ι : Type*} [Fintype ι] [DecidableEq ι]
    (M : Matrix ι ι (LaurentPolynomial R)) (B : Finset ι)
    (hbulk : ∀ i j, j ∉ B → Bounded (M i j) 0)
    (hboundary : ∀ i j, j ∈ B → Bounded (M i j) 1) :
    Bounded M.det (B.card : ℤ) := by
  classical
  have h := determinant_column_bound M (fun j => if j ∈ B then 1 else 0)
    (by intro i j; by_cases hj : j ∈ B <;> simp [hj, hbulk, hboundary])
  simpa using h

/-- At the top possible exponent only the two top coefficients can contribute. -/
theorem coeff_mul_top {f g : LaurentPolynomial R} {a b : ℤ}
    (hf : Bounded f a) (hg : Bounded g b) :
    (f * g).coeff (a + b) = f.coeff a * g.coeff b := by
  classical
  rw [AddMonoidAlgebra.coeff_mul_apply_left]
  rw [Finset.sum_eq_single a]
  · simp
  · intro i hi hia
    by_cases hle : i ≤ a
    · have hlt : i < a := lt_of_le_of_ne hle hia
      rw [hg (-i + (a + b)) (by omega), mul_zero]
    · rw [hf i (lt_of_not_ge hle), zero_mul]
  · intro ha
    rw [Finsupp.notMem_support_iff.mp ha, zero_mul]

end OperatorFirst.LaurentBoundary

#print axioms OperatorFirst.LaurentBoundary.bounded_zero
#print axioms OperatorFirst.LaurentBoundary.bounded_mono
#print axioms OperatorFirst.LaurentBoundary.bounded_C
#print axioms OperatorFirst.LaurentBoundary.bounded_monomial
#print axioms OperatorFirst.LaurentBoundary.bounded_add
#print axioms OperatorFirst.LaurentBoundary.bounded_neg
#print axioms OperatorFirst.LaurentBoundary.bounded_mul
#print axioms OperatorFirst.LaurentBoundary.bounded_sum
#print axioms OperatorFirst.LaurentBoundary.bounded_prod
#print axioms OperatorFirst.LaurentBoundary.determinant_column_bound
#print axioms OperatorFirst.LaurentBoundary.determinant_one_boundary_column
#print axioms OperatorFirst.LaurentBoundary.determinant_boundary_set
#print axioms OperatorFirst.LaurentBoundary.coeff_mul_top
