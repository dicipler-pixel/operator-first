import Mathlib

/-!
# Canonical rank-two Coxeter-to-dihedral bridge

This file works with mathlib's actual `CoxeterMatrix.I` presentation and
concrete `DihedralGroup`.  The first target is the canonical homomorphism

  (CoxeterMatrix.I m).Group →* DihedralGroup (m + 2)

sending the two simple Coxeter generators to adjacent reflections, together
with a proof that this map is surjective.

The eventual target is a group equivalence.  We keep the stages separate so
that a surjection is not silently promoted to an isomorphism.
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
      simp [DihedralGroup.r_one_pow, ZMod.natCast_zmod_val]
  | sr i =>
      refine ⟨((CoxeterMatrix.I m).simple (0 : Fin 2) *
        (((CoxeterMatrix.I m).simple (0 : Fin 2) *
          (CoxeterMatrix.I m).simple (1 : Fin 2)) ^ i.val)), ?_⟩
      simp [DihedralGroup.r_one_pow, ZMod.natCast_zmod_val]

#print axioms OperatorFirst.CoxeterRankTwo.dihedralSimple_isLiftable
#print axioms OperatorFirst.CoxeterRankTwo.toDihedral_surjective

end OperatorFirst.CoxeterRankTwo
