import Certificates
import Mathlib.Data.Rat.Sqrt

/-!
# Integrality of the explicit ±3/2 rational section

This module formalizes the two-point integer image of the explicit rational
section reconstructed in the Diophantine audit.  It does not formalize the
separate Nagell--Lutz specialization/non-torsion argument and does not claim a
solution of any of the six unresolved surfaces.
-/

namespace DiophantineEye

/-- Rational x-coordinate of the reconstructed section. -/
def sectionX (u : ℚ) : ℚ :=
  (u^4 - 34*u^2 + 1) / (4 * (1+u^2)^2)

/-- Rational y-coordinate of the reconstructed section. -/
def sectionY (u : ℚ) : ℚ :=
  3 * (1-u^2) / (2 * (1+u^2))

/-- Auxiliary discriminant coordinate `w = 2z + y^2`. -/
def sectionW (u : ℚ) : ℚ :=
  3*u*(u^4 - 34*u^2 + 1) / (2 * (1+u^2)^3)

/-- z-coordinate recovered from `w = 2z + y^2`. -/
def sectionZ (u : ℚ) : ℚ :=
  (sectionW u - (sectionY u)^2) / 2

/-- The section y-coordinate always lies in the closed interval [-3/2,3/2]. -/
theorem sectionY_lower (u : ℚ) : (-3/2 : ℚ) ≤ sectionY u := by
  have hden : 0 < (2 : ℚ) * (1+u^2) := by
    have h := circle_denominator_positive u
    positivity
  unfold sectionY
  apply (le_div_iff₀ hden).2
  nlinarith [sq_nonneg u]

theorem sectionY_upper (u : ℚ) : sectionY u ≤ (3/2 : ℚ) := by
  have hden : 0 < (2 : ℚ) * (1+u^2) := by
    have h := circle_denominator_positive u
    positivity
  unfold sectionY
  apply (div_le_iff₀ hden).2
  nlinarith [sq_nonneg u]

/-- If the y-coordinate is an integer, the interval bound reduces it to
`-1, 0, 1`. -/
theorem sectionY_integer_range (u : ℚ) (y : ℤ)
    (hy : sectionY u = (y : ℚ)) :
    y = -1 ∨ y = 0 ∨ y = 1 := by
  have hloq : (-2 : ℚ) < (y : ℚ) := by
    rw [← hy]
    have h := sectionY_lower u
    linarith
  have hhiq : (y : ℚ) < (2 : ℚ) := by
    rw [← hy]
    have h := sectionY_upper u
    linarith
  have hlo : (-2 : ℤ) < y := by exact_mod_cast hloq
  have hhi : y < (2 : ℤ) := by exact_mod_cast hhiq
  omega

/-- Solving the y-coordinate equation gives the exact parameter-square
relation used in the written integrality proof. -/
theorem sectionY_parameter_relation (u y : ℚ)
    (hy : sectionY u = y) :
    (3 + 2*y) * u^2 = 3 - 2*y := by
  have hq : (1+u^2 : ℚ) ≠ 0 := ne_of_gt (circle_denominator_positive u)
  unfold sectionY at hy
  field_simp [hq] at hy
  nlinarith [hy]

/-- Five is not a square in the rationals.  This is evaluated through
Mathlib's exact rational square-root criterion, not floating point. -/
theorem five_not_rational_square : ¬ ∃ q : ℚ, q*q = 5 := by
  rw [Rat.exists_mul_self]
  norm_num

/-- An integral y-coordinate forces y=0 and u=±1. -/
theorem sectionY_integer_parameter (u : ℚ) (y : ℤ)
    (hy : sectionY u = (y : ℚ)) :
    y = 0 ∧ (u = 1 ∨ u = -1) := by
  rcases sectionY_integer_range u y hy with hneg | hzero | hpos
  · subst y
    have hrel := sectionY_parameter_relation u (-1) (by simpa using hy)
    have hu : u*u = 5 := by nlinarith
    exact (five_not_rational_square ⟨u, hu⟩).elim
  · refine ⟨hzero, ?_⟩
    subst y
    have hrel := sectionY_parameter_relation u 0 (by simpa using hy)
    have hprod : (u-1)*(u+1)=0 := by nlinarith
    rcases mul_eq_zero.mp hprod with h | h
    · left; linarith
    · right; linarith
  · subst y
    have hrel := sectionY_parameter_relation u 1 (by simpa using hy)
    have hu : u*u = (1/5 : ℚ) := by nlinarith
    have hfive : ∃ q : ℚ, q*q = 5 := by
      refine ⟨5*u, ?_⟩
      nlinarith
    exact (five_not_rational_square hfive).elim

/-- The two parameter values give exactly the two integer triples stated in the
audit. -/
theorem section_values_one :
    sectionX 1 = -2 ∧ sectionY 1 = 0 ∧ sectionZ 1 = -3 := by
  norm_num [sectionX, sectionY, sectionW, sectionZ]

theorem section_values_neg_one :
    sectionX (-1) = -2 ∧ sectionY (-1) = 0 ∧ sectionZ (-1) = 3 := by
  norm_num [sectionX, sectionY, sectionW, sectionZ]

/-- Complete integer image of this particular rational section: it is enough
that the y-coordinate be integral. -/
theorem section_integer_image (u : ℚ) (y : ℤ)
    (hy : sectionY u = (y : ℚ)) :
    (sectionX u = -2 ∧ sectionY u = 0 ∧ sectionZ u = -3) ∨
    (sectionX u = -2 ∧ sectionY u = 0 ∧ sectionZ u = 3) := by
  rcases sectionY_integer_parameter u y hy with ⟨hy0, hu | hu⟩
  · subst u
    exact Or.inl section_values_one
  · subst u
    exact Or.inr section_values_neg_one

end DiophantineEye

#print axioms DiophantineEye.sectionY_lower
#print axioms DiophantineEye.sectionY_upper
#print axioms DiophantineEye.sectionY_integer_range
#print axioms DiophantineEye.sectionY_parameter_relation
#print axioms DiophantineEye.five_not_rational_square
#print axioms DiophantineEye.sectionY_integer_parameter
#print axioms DiophantineEye.section_values_one
#print axioms DiophantineEye.section_values_neg_one
#print axioms DiophantineEye.section_integer_image
