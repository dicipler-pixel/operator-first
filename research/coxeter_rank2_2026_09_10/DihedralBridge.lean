import Mathlib

/-!
# Canonical rank-two Coxeter-to-dihedral bridge

This file works with mathlib's actual `CoxeterMatrix.I` presentation and
concrete `DihedralGroup`.

Stage 1 constructs the canonical homomorphism

  (CoxeterMatrix.I m).Group →* DihedralGroup (m + 2)

sending the two simple Coxeter generators to adjacent reflections and proves
that it is surjective.

Stage 2 proves an internal dihedral normal form in the presented Coxeter group:
every element is either a rotation power or the first reflection times a
rotation power.  This is the load-bearing input for injectivity; we keep the
stages explicit so a surjection is never silently promoted to an isomorphism.
-/

set_option autoImplicit false

namespace OperatorFirst.CoxeterRankTwo

open CoxeterMatrix
open DihedralGroup

/-- The two adjacent reflections in the concrete dihedral group. -/
def dihedralSimple (m : ℕ) : Fin 2 → DihedralGroup (m + 2) := fun i =>
  if i = 0 then sr 0 else sr 1

/-- The adjacent dihedral reflections satisfy the `I₂(m+2)` Coxeter relations. -/
theorem dihedralSimple_isLiftable (m : ℕ) :
    CoxeterMatrix.IsLiftable (CoxeterMatrix.I m) (dihedralSimple m) := by
  intro i j
  fin_cases i <;> fin_cases j <;>
    simp [dihedralSimple, CoxeterMatrix.I, DihedralGroup.r_pow]

/-- Canonical map from mathlib's presented rank-two Coxeter group to the
concrete dihedral group. -/
def toDihedral (m : ℕ) :
    (CoxeterMatrix.I m).Group →* DihedralGroup (m + 2) :=
  (CoxeterMatrix.I m).toCoxeterSystem.lift
    ⟨dihedralSimple m, dihedralSimple_isLiftable m⟩

@[simp] theorem toDihedral_simple_zero (m : ℕ) :
    toDihedral m ((CoxeterMatrix.I m).simple (0 : Fin 2)) = sr 0 := by
  simpa [toDihedral, dihedralSimple] using
    (CoxeterMatrix.I m).toCoxeterSystem.lift_apply_simple
      (dihedralSimple_isLiftable m) (0 : Fin 2)

@[simp] theorem toDihedral_simple_one (m : ℕ) :
    toDihedral m ((CoxeterMatrix.I m).simple (1 : Fin 2)) = sr 1 := by
  simpa [toDihedral, dihedralSimple] using
    (CoxeterMatrix.I m).toCoxeterSystem.lift_apply_simple
      (dihedralSimple_isLiftable m) (1 : Fin 2)

/-- The Coxeter rotation maps to the basic dihedral rotation. -/
@[simp] theorem toDihedral_rotation (m : ℕ) :
    toDihedral m
      ((CoxeterMatrix.I m).simple (0 : Fin 2) *
       (CoxeterMatrix.I m).simple (1 : Fin 2)) = r 1 := by
  simp [toDihedral_simple_zero, toDihedral_simple_one]

/-- The canonical map already reaches every concrete dihedral element. -/
theorem toDihedral_surjective (m : ℕ) : Function.Surjective (toDihedral m) := by
  intro d
  cases d with
  | r i =>
      refine ⟨(((CoxeterMatrix.I m).simple (0 : Fin 2) *
        (CoxeterMatrix.I m).simple (1 : Fin 2)) ^ i.val), ?_⟩
      simp
  | sr i =>
      refine ⟨((CoxeterMatrix.I m).simple (0 : Fin 2) *
        (((CoxeterMatrix.I m).simple (0 : Fin 2) *
          (CoxeterMatrix.I m).simple (1 : Fin 2)) ^ i.val)), ?_⟩
      simp

/-! ## Internal normal form in the presented Coxeter group -/

abbrev IGroup (m : ℕ) := (CoxeterMatrix.I m).Group

/-- First canonical Coxeter generator. -/
def c0 (m : ℕ) : IGroup m := (CoxeterMatrix.I m).simple (0 : Fin 2)

/-- Second canonical Coxeter generator. -/
def c1 (m : ℕ) : IGroup m := (CoxeterMatrix.I m).simple (1 : Fin 2)

/-- Canonical rotation word. -/
def coxRot (m : ℕ) : IGroup m := c0 m * c1 m

@[simp] theorem c0_sq (m : ℕ) : c0 m * c0 m = 1 := by
  simpa [c0] using
    (CoxeterMatrix.I m).toCoxeterSystem.simple_mul_simple_self (0 : Fin 2)

@[simp] theorem c1_sq (m : ℕ) : c1 m * c1 m = 1 := by
  simpa [c1] using
    (CoxeterMatrix.I m).toCoxeterSystem.simple_mul_simple_self (1 : Fin 2)

@[simp] theorem c0_inv (m : ℕ) : (c0 m)⁻¹ = c0 m := by
  exact (eq_inv_of_mul_eq_one_right (c0_sq m)).symm

@[simp] theorem c1_inv (m : ℕ) : (c1 m)⁻¹ = c1 m := by
  exact (eq_inv_of_mul_eq_one_right (c1_sq m)).symm

/-- The canonical rotation has the Coxeter period relation. -/
theorem coxRot_pow_order (m : ℕ) : (coxRot m) ^ (m + 2) = 1 := by
  simpa [coxRot, c0, c1, CoxeterMatrix.I] using
    (CoxeterMatrix.I m).toCoxeterSystem.simple_mul_simple_pow
      (0 : Fin 2) (1 : Fin 2)

/-- The second reflection is the first reflection followed by the rotation. -/
theorem c1_eq_c0_mul_coxRot (m : ℕ) : c1 m = c0 m * coxRot m := by
  simp [coxRot, mul_assoc]

/-- Conjugation by the first reflection reverses the rotation. -/
@[simp] theorem c0_mul_coxRot_mul_c0 (m : ℕ) :
    c0 m * coxRot m * c0 m = (coxRot m)⁻¹ := by
  simp [coxRot, mul_assoc, mul_inv_rev]

/-- The conjugation identity at every integer power. -/
theorem c0_mul_coxRot_zpow_mul_c0 (m : ℕ) (k : ℤ) :
    c0 m * (coxRot m) ^ k * c0 m = (coxRot m) ^ (-k) := by
  calc
    c0 m * (coxRot m) ^ k * c0 m
        = c0 m * (coxRot m) ^ k * (c0 m)⁻¹ := by simp
    _ = (c0 m * coxRot m * (c0 m)⁻¹) ^ k := by
          simpa using (conj_zpow (a := c0 m) (b := coxRot m) (i := k)).symm
    _ = ((coxRot m)⁻¹) ^ k := by simp
    _ = (coxRot m) ^ (-k) := by simp

/-- Move the first reflection through an arbitrary rotation power. -/
theorem coxRot_zpow_mul_c0 (m : ℕ) (k : ℤ) :
    (coxRot m) ^ k * c0 m = c0 m * (coxRot m) ^ (-k) := by
  calc
    (coxRot m) ^ k * c0 m
        = c0 m * (c0 m * (coxRot m) ^ k * c0 m) := by simp [mul_assoc]
    _ = c0 m * (coxRot m) ^ (-k) := by rw [c0_mul_coxRot_zpow_mul_c0]

/-- Rotate then multiply by the second reflection. -/
theorem coxRot_zpow_mul_c1 (m : ℕ) (k : ℤ) :
    (coxRot m) ^ k * c1 m = c0 m * (coxRot m) ^ (-k + 1) := by
  rw [c1_eq_c0_mul_coxRot]
  rw [← mul_assoc, coxRot_zpow_mul_c0]
  rw [mul_assoc, ← zpow_add]
  simp

/-- A reflected normal form times the first reflection becomes a rotation. -/
theorem c0_mul_coxRot_zpow_mul_c0_nf (m : ℕ) (k : ℤ) :
    c0 m * (coxRot m) ^ k * c0 m = (coxRot m) ^ (-k) :=
  c0_mul_coxRot_zpow_mul_c0 m k

/-- A reflected normal form times the second reflection becomes a rotation. -/
theorem c0_mul_coxRot_zpow_mul_c1 (m : ℕ) (k : ℤ) :
    c0 m * (coxRot m) ^ k * c1 m = (coxRot m) ^ (-k + 1) := by
  rw [c1_eq_c0_mul_coxRot]
  rw [← mul_assoc, c0_mul_coxRot_zpow_mul_c0]
  rw [← zpow_add]
  simp

/-- Dihedral two-coset normal-form predicate. -/
def HasDihedralNormalForm (m : ℕ) (w : IGroup m) : Prop :=
  ∃ k : ℤ, w = (coxRot m) ^ k ∨ w = c0 m * (coxRot m) ^ k

/-- Every element of the presented rank-two Coxeter group has a dihedral
normal form. -/
theorem hasDihedralNormalForm (m : ℕ) (w : IGroup m) :
    HasDihedralNormalForm m w := by
  let cs := (CoxeterMatrix.I m).toCoxeterSystem
  apply cs.simple_induction_right w
  · refine ⟨0, Or.inl ?_⟩
    simp [HasDihedralNormalForm]
  · intro w i hw
    rcases hw with ⟨k, hk | hk⟩
    · subst w
      fin_cases i
      · refine ⟨-k, Or.inr ?_⟩
        exact coxRot_zpow_mul_c0 m k
      · refine ⟨-k + 1, Or.inr ?_⟩
        exact coxRot_zpow_mul_c1 m k
    · subst w
      fin_cases i
      · refine ⟨-k, Or.inl ?_⟩
        exact c0_mul_coxRot_zpow_mul_c0_nf m k
      · refine ⟨-k + 1, Or.inl ?_⟩
        exact c0_mul_coxRot_zpow_mul_c1 m k

#print axioms OperatorFirst.CoxeterRankTwo.dihedralSimple_isLiftable
#print axioms OperatorFirst.CoxeterRankTwo.toDihedral_surjective
#print axioms OperatorFirst.CoxeterRankTwo.hasDihedralNormalForm

end OperatorFirst.CoxeterRankTwo
