import Mathlib

/-!
# Canonical rank-two Coxeter-to-dihedral bridge

This file works with mathlib's actual `CoxeterMatrix.I` presentation and
concrete `DihedralGroup`.

We construct the canonical homomorphism

  (CoxeterMatrix.I m).Group →* DihedralGroup (m + 2)

sending the two simple Coxeter generators to adjacent reflections.  We then
prove a two-coset normal form inside the presented Coxeter group, use it to
show that the canonical map has trivial kernel, and obtain the multiplicative
group equivalence.
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
  change (((CoxeterMatrix.I m).toCoxeterSystem.simple (0 : Fin 2) *
    (CoxeterMatrix.I m).toCoxeterSystem.simple (1 : Fin 2)) ^ (m + 2) = 1)
  simpa [CoxeterMatrix.I] using
    (CoxeterMatrix.I m).toCoxeterSystem.simple_mul_simple_pow
      (0 : Fin 2) (1 : Fin 2)

/-- The second reflection is the first reflection followed by the rotation. -/
theorem c1_eq_c0_mul_coxRot (m : ℕ) : c1 m = c0 m * coxRot m := by
  calc
    c1 m = 1 * c1 m := by simp
    _ = (c0 m * c0 m) * c1 m := by rw [c0_sq]
    _ = c0 m * (c0 m * c1 m) := by simp only [mul_assoc]
    _ = c0 m * coxRot m := by rfl

/-- Conjugation by the first reflection reverses the rotation. -/
@[simp] theorem c0_mul_coxRot_mul_c0 (m : ℕ) :
    c0 m * coxRot m * c0 m = (coxRot m)⁻¹ := by
  rw [coxRot]
  calc
    c0 m * (c0 m * c1 m) * c0 m
        = (c0 m * c0 m) * c1 m * c0 m := by simp only [mul_assoc]
    _ = c1 m * c0 m := by simp
    _ = (c0 m * c1 m)⁻¹ := by simp [mul_inv_rev]

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
        = 1 * ((coxRot m) ^ k * c0 m) := by simp
    _ = (c0 m * c0 m) * ((coxRot m) ^ k * c0 m) := by rw [c0_sq]
    _ = c0 m * (c0 m * (coxRot m) ^ k * c0 m) := by simp only [mul_assoc]
    _ = c0 m * (coxRot m) ^ (-k) := by rw [c0_mul_coxRot_zpow_mul_c0]

/-- Rotate then multiply by the second reflection. -/
theorem coxRot_zpow_mul_c1 (m : ℕ) (k : ℤ) :
    (coxRot m) ^ k * c1 m = c0 m * (coxRot m) ^ (-k + 1) := by
  rw [c1_eq_c0_mul_coxRot, ← mul_assoc, coxRot_zpow_mul_c0]
  group

/-- A reflected normal form times the first reflection becomes a rotation. -/
theorem c0_mul_coxRot_zpow_mul_c0_nf (m : ℕ) (k : ℤ) :
    c0 m * (coxRot m) ^ k * c0 m = (coxRot m) ^ (-k) :=
  c0_mul_coxRot_zpow_mul_c0 m k

/-- A reflected normal form times the second reflection becomes a rotation. -/
theorem c0_mul_coxRot_zpow_mul_c1 (m : ℕ) (k : ℤ) :
    c0 m * (coxRot m) ^ k * c1 m = (coxRot m) ^ (-k + 1) := by
  rw [c1_eq_c0_mul_coxRot, ← mul_assoc, c0_mul_coxRot_zpow_mul_c0]
  group

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
    simp
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

/-! ## Kernel closure and the actual equivalence -/

@[simp] theorem toDihedral_c0 (m : ℕ) : toDihedral m (c0 m) = sr 0 := by
  simpa [c0] using toDihedral_simple_zero m

@[simp] theorem toDihedral_coxRot (m : ℕ) : toDihedral m (coxRot m) = r 1 := by
  simpa [coxRot, c0, c1] using toDihedral_rotation m

/-- The canonical map has trivial kernel. In the rotation normal form, the
concrete target detects divisibility of the exponent by `m+2`; the Coxeter
period relation then kills the source rotation. The reflected normal form
cannot map to the identity because `r` and `sr` are distinct constructors. -/
theorem toDihedral_eq_one_imp (m : ℕ) {w : IGroup m}
    (hw : toDihedral m w = 1) : w = 1 := by
  obtain ⟨k, hk | hk⟩ := hasDihedralNormalForm m w
  · subst w
    have hr : (r 1 : DihedralGroup (m + 2)) ^ k = 1 := by
      simpa using hw
    have hkdiv : ((m + 2 : ℕ) : ℤ) ∣ k := by
      simpa using (orderOf_dvd_iff_zpow_eq_one.mpr hr)
    have horderNat : orderOf (coxRot m) ∣ m + 2 :=
      orderOf_dvd_of_pow_eq_one (coxRot_pow_order m)
    have horderInt : (orderOf (coxRot m) : ℤ) ∣ ((m + 2 : ℕ) : ℤ) := by
      exact Int.natCast_dvd_natCast.mpr horderNat
    exact orderOf_dvd_iff_zpow_eq_one.mp (horderInt.trans hkdiv)
  · subst w
    exfalso
    have hbad :
        (sr (k : ZMod (m + 2)) : DihedralGroup (m + 2)) = r 0 := by
      simpa [DihedralGroup.r_one_zpow] using hw
    cases hbad

/-- The canonical map is injective. -/
theorem toDihedral_injective (m : ℕ) : Function.Injective (toDihedral m) := by
  rw [injective_iff_map_eq_one]
  intro w hw
  exact toDihedral_eq_one_imp m hw

/-- Mathlib's presented rank-two Coxeter group is canonically equivalent to
the concrete dihedral group. -/
noncomputable def IGroupEquivDihedral (m : ℕ) :
    IGroup m ≃* DihedralGroup (m + 2) :=
  MulEquiv.ofBijective (toDihedral m)
    ⟨toDihedral_injective m, toDihedral_surjective m⟩

#print axioms OperatorFirst.CoxeterRankTwo.dihedralSimple_isLiftable
#print axioms OperatorFirst.CoxeterRankTwo.toDihedral_surjective
#print axioms OperatorFirst.CoxeterRankTwo.hasDihedralNormalForm
#print axioms OperatorFirst.CoxeterRankTwo.toDihedral_injective
#print axioms OperatorFirst.CoxeterRankTwo.IGroupEquivDihedral

end OperatorFirst.CoxeterRankTwo
