import Mathlib

/-!
# Rank-two finite-to-affine reflection certificate

A small, exact formal slice motivated by the open problem of making Coxeter's
finite/affine classification computer-verifiable.

This file does NOT claim the full classification. It isolates the rank-two
crystallographic boundary in a concrete integral reflection model.

For nonnegative Cartan off-diagonal magnitudes `a,b`, use the two involutions

  s₁(x,y) = (-x + a y, y)
  s₂(x,y) = (x, b x - y).

Their product has the familiar rank-two behavior controlled by `a*b`.
The canonical crystallographic finite products `0,1,2,3` give periods
`2,3,4,6`; the product-4 affine representative `(a,b)=(2,2)` has no positive
period and instead has linear unipotent drift.

We also record the golden product `(3+√5)/2` between `2` and `3`, hence it is
not an integer. This is the arithmetic obstruction seen at the 36-degree
`I₂(5)=H₂` case.
-/

set_option autoImplicit false

namespace OperatorFirst.CoxeterRankTwo

abbrev V := ℤ × ℤ

/-- First simple reflection for a rank-two Cartan pair. -/
def s1 (a : ℤ) (v : V) : V :=
  (-v.1 + a * v.2, v.2)

/-- Second simple reflection for a rank-two Cartan pair. -/
def s2 (b : ℤ) (v : V) : V :=
  (v.1, b * v.1 - v.2)

/-- Coxeter step `s₁ s₂`. -/
def step (a b : ℤ) (v : V) : V :=
  s1 a (s2 b v)

/-- A deliberately transparent iterate, used only for this finite certificate. -/
def iter {α : Type*} (f : α → α) : ℕ → α → α
  | 0 => fun x => x
  | n + 1 => fun x => f (iter f n x)

/-- Exact period means a universal period and no smaller positive universal period. -/
def HasExactPeriod {α : Type*} (f : α → α) (n : ℕ) : Prop :=
  (∀ x, iter f n x = x) ∧
    ∀ m, 0 < m → m < n → ∃ x, iter f m x ≠ x

@[simp] theorem s1_involution (a : ℤ) (v : V) : s1 a (s1 a v) = v := by
  rcases v with ⟨x, y⟩
  ext <;> simp [s1]

@[simp] theorem s2_involution (b : ℤ) (v : V) : s2 b (s2 b v) = v := by
  rcases v with ⟨x, y⟩
  ext <;> simp [s2]

/-- Product `0`: type `A₁ × A₁`. -/
def U2 : V → V := step 0 0

/-- Product `1`: type `A₂`. -/
def U3 : V → V := step 1 1

/-- Product `2`: type `B₂/C₂`. -/
def U4 : V → V := step 1 2

/-- Product `3`: type `G₂`. -/
def U6 : V → V := step 1 3

/-- Product `4`: the symmetric affine rank-two representative. -/
def Uaff : V → V := step 2 2

@[simp] theorem U2_formula (x y : ℤ) : U2 (x, y) = (-x, -y) := by
  ext <;> simp [U2, step, s1, s2]

@[simp] theorem U3_formula (x y : ℤ) : U3 (x, y) = (-y, x - y) := by
  ext <;> simp [U3, step, s1, s2] <;> ring_nf

@[simp] theorem U4_formula (x y : ℤ) : U4 (x, y) = (x - y, 2 * x - y) := by
  ext <;> simp [U4, step, s1, s2] <;> ring_nf

@[simp] theorem U6_formula (x y : ℤ) : U6 (x, y) = (2 * x - y, 3 * x - y) := by
  ext <;> simp [U6, step, s1, s2] <;> ring_nf

@[simp] theorem Uaff_formula (x y : ℤ) : Uaff (x, y) = (3 * x - 2 * y, 2 * x - y) := by
  ext <;> simp [Uaff, step, s1, s2] <;> ring_nf

theorem U2_period : ∀ v : V, iter U2 2 v = v := by
  rintro ⟨x, y⟩
  ext <;> simp [iter, U2, step, s1, s2]

theorem U3_period : ∀ v : V, iter U3 3 v = v := by
  rintro ⟨x, y⟩
  ext <;> simp [iter, U3, step, s1, s2] <;> ring_nf

theorem U4_period : ∀ v : V, iter U4 4 v = v := by
  rintro ⟨x, y⟩
  ext <;> simp [iter, U4, step, s1, s2] <;> ring_nf

theorem U6_period : ∀ v : V, iter U6 6 v = v := by
  rintro ⟨x, y⟩
  ext <;> simp [iter, U6, step, s1, s2] <;> ring_nf

theorem U2_exact : HasExactPeriod U2 2 := by
  refine ⟨U2_period, ?_⟩
  intro m hm hlt
  refine ⟨(1, 0), ?_⟩
  interval_cases m <;> norm_num [iter, U2, step, s1, s2] at *

theorem U3_exact : HasExactPeriod U3 3 := by
  refine ⟨U3_period, ?_⟩
  intro m hm hlt
  refine ⟨(1, 0), ?_⟩
  interval_cases m <;> norm_num [iter, U3, step, s1, s2] at *

theorem U4_exact : HasExactPeriod U4 4 := by
  refine ⟨U4_period, ?_⟩
  intro m hm hlt
  refine ⟨(1, 0), ?_⟩
  interval_cases m <;> norm_num [iter, U4, step, s1, s2] at *

theorem U6_exact : HasExactPeriod U6 6 := by
  refine ⟨U6_period, ?_⟩
  intro m hm hlt
  refine ⟨(1, 0), ?_⟩
  interval_cases m <;> norm_num [iter, U6, step, s1, s2] at *

/-- The affine product-4 representative is `I + N` with `N²=0`, so its
iterates drift linearly rather than closing. -/
theorem Uaff_iterate (n : ℕ) (x y : ℤ) :
    iter Uaff n (x, y) =
      (x + 2 * (n : ℤ) * (x - y), y + 2 * (n : ℤ) * (x - y)) := by
  induction n with
  | zero => simp [iter]
  | succ n ih =>
      change Uaff (iter Uaff n (x, y)) = _
      rw [ih, Uaff_formula]
      simp only [Nat.cast_succ]
      ext <;> ring

/-- No positive iterate of the affine representative is the identity. -/
theorem Uaff_no_positive_period (n : ℕ) (hn : 0 < n) :
    iter Uaff n (1, 0) ≠ (1, 0) := by
  rw [Uaff_iterate]
  intro h
  have h2 := congrArg Prod.snd h
  simp at h2
  omega

/-- The finite crystallographic rank-two Cartan-product values. -/
theorem product_lt_four_cases (p : ℕ) (hp : p < 4) :
    p = 0 ∨ p = 1 ∨ p = 2 ∨ p = 3 := by
  omega

/-- Rank-two determinant margin `4-p` is positive exactly on this finite side. -/
theorem finite_margin_positive (p : ℕ) (hp : p < 4) :
    0 < (4 : ℤ) - (p : ℤ) := by
  omega

@[simp] theorem affine_margin_zero : (4 : ℤ) - 4 = 0 := by norm_num

/-- The golden Cartan product at the `36°` / `I₂(5)=H₂` case lies strictly
between the crystallographic integer products `2` and `3`. -/
theorem golden_product_between :
    (2 : ℝ) < (3 + Real.sqrt 5) / 2 ∧ (3 + Real.sqrt 5) / 2 < 3 := by
  have hs0 : 0 ≤ Real.sqrt (5 : ℝ) := Real.sqrt_nonneg _
  have hs2 : (Real.sqrt (5 : ℝ)) ^ 2 = 5 := by norm_num
  constructor <;> nlinarith

/-- In particular the golden rank-two product is not integral. -/
theorem golden_product_not_integer :
    ¬ ∃ z : ℤ, (z : ℝ) = (3 + Real.sqrt 5) / 2 := by
  rintro ⟨z, hz⟩
  obtain ⟨hlo, hhi⟩ := golden_product_between
  have hzlo : (2 : ℝ) < (z : ℝ) := by simpa [hz] using hlo
  have hzhi : (z : ℝ) < (3 : ℝ) := by simpa [hz] using hhi
  have hzlo' : (2 : ℤ) < z := by exact_mod_cast hzlo
  have hzhi' : z < (3 : ℤ) := by exact_mod_cast hzhi
  omega

#print axioms OperatorFirst.CoxeterRankTwo.U2_exact
#print axioms OperatorFirst.CoxeterRankTwo.U3_exact
#print axioms OperatorFirst.CoxeterRankTwo.U4_exact
#print axioms OperatorFirst.CoxeterRankTwo.U6_exact
#print axioms OperatorFirst.CoxeterRankTwo.Uaff_no_positive_period
#print axioms OperatorFirst.CoxeterRankTwo.golden_product_not_integer

end OperatorFirst.CoxeterRankTwo
