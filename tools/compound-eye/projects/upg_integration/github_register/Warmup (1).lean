-- SCRIPT: WARMUP-CORE-01
-- Two warm-up theorems from "Light Keeps the Ledger", stated and proved in
-- core Lean 4 with NO mathlib dependency. Everything used is defined below.
--
--   T1  commutator identity   [S+K, S-K] = -2[S,K]
--       corollary             C = S+K is normal  <->  [S,K] = 0   (needs 2-torsion-free)
--   T2  reciprocity           star B = B  ->  star V * B = B * V  ->  star (B*V) = B*V
--
-- Both are proved for an arbitrary ring, which is strictly more general than
-- the real matrices the paper states them for.

namespace OperatorFirst

class MyRing (R : Type u) extends Add R, Mul R, Neg R, Zero R where
  add_assoc      : forall a b c : R, a + b + c = a + (b + c)
  add_comm       : forall a b : R, a + b = b + a
  zero_add       : forall a : R, 0 + a = a
  neg_add_cancel : forall a : R, -a + a = 0
  mul_assoc      : forall a b c : R, a * b * c = a * (b * c)
  left_distrib   : forall a b c : R, a * (b + c) = a * b + a * c
  right_distrib  : forall a b c : R, (a + b) * c = a * c + b * c

namespace MyRing

variable {R : Type u} [MyRing R]

def sub (a b : R) : R := a + -b
instance : Sub R := ⟨sub⟩
theorem sub_eq (a b : R) : a - b = a + -b := rfl

attribute [simp] add_assoc

theorem add_zero (a : R) : a + 0 = a := by
  rw [add_comm, zero_add]

theorem add_neg_cancel (a : R) : a + -a = 0 := by
  rw [add_comm, neg_add_cancel]

theorem add_left_cancel {a b c : R} (h : a + b = a + c) : b = c := by
  have h2 : -a + (a + b) = -a + (a + c) := by rw [h]
  rw [← add_assoc, ← add_assoc, neg_add_cancel, zero_add, zero_add] at h2
  exact h2

theorem add_left_comm (a b c : R) : a + (b + c) = b + (a + c) := by
  rw [← add_assoc, ← add_assoc, add_comm a b]

theorem mul_zero (a : R) : a * 0 = 0 := by
  have h : a * 0 + a * 0 = a * 0 + 0 := by
    rw [← left_distrib, zero_add, add_zero]
  exact add_left_cancel h

theorem zero_mul (a : R) : (0 : R) * a = 0 := by
  have h : 0 * a + 0 * a = 0 * a + 0 := by
    rw [← right_distrib, zero_add, add_zero]
  exact add_left_cancel h

theorem neg_zero : -(0 : R) = 0 := by
  have h : (0 : R) + -0 = (0 : R) + 0 := by rw [add_neg_cancel, add_zero]
  exact add_left_cancel h

theorem mul_neg (a b : R) : a * -b = -(a * b) := by
  have h : a * b + a * -b = a * b + -(a * b) := by
    rw [← left_distrib, add_neg_cancel, mul_zero, add_neg_cancel]
  exact add_left_cancel h

theorem neg_mul (a b : R) : -a * b = -(a * b) := by
  have h : a * b + -a * b = a * b + -(a * b) := by
    rw [← right_distrib, add_neg_cancel, zero_mul, add_neg_cancel]
  exact add_left_cancel h

theorem neg_add (a b : R) : -(a + b) = -a + -b := by
  have h : (a + b) + -(a + b) = (a + b) + (-a + -b) := by
    rw [add_neg_cancel, add_assoc, add_left_comm b (-a) (-b), ← add_assoc,
        add_neg_cancel, zero_add, add_neg_cancel]
  exact add_left_cancel h

theorem neg_neg (a : R) : - -a = a := by
  have h : -a + - -a = -a + a := by rw [add_neg_cancel, neg_add_cancel]
  exact add_left_cancel h

/-- The commutator `a*b - b*a`. -/
def comm (a b : R) : R := a * b - b * a

theorem comm_def (a b : R) : comm a b = a * b + -(b * a) := rfl

theorem add_neg_cancel_left (a b : R) : a + (-a + b) = b := by
  rw [← add_assoc, add_neg_cancel, zero_add]

/-- The one piece of abelian-group bookkeeping the main identity needs:
`p` cancels `-p`, `u` cancels `-u`, and two copies of `X` survive. -/
theorem abel4 (p u X : R) :
    (p + (X + -u)) + (-p + (X + u)) = X + X := by
  calc (p + (X + -u)) + (-p + (X + u))
      = p + ((X + -u) + (-p + (X + u))) := by rw [add_assoc]
    _ = p + (-p + ((X + -u) + (X + u)))  := by rw [add_left_comm (X + -u) (-p) (X + u)]
    _ = (X + -u) + (X + u)               := by rw [add_neg_cancel_left]
    _ = X + (-u + (X + u))               := by rw [add_assoc]
    _ = X + (X + (-u + u))               := by rw [add_left_comm (-u) X u]
    _ = X + (X + 0)                      := by rw [neg_add_cancel]
    _ = X + X                            := by rw [add_zero]

theorem expand_left (S K : R) :
    (S + K) * (S - K) = S * S + (-(S * K) + (K * S + -(K * K))) := by
  rw [sub_eq, right_distrib, left_distrib, left_distrib, mul_neg, mul_neg,
      add_assoc]

theorem expand_right (S K : R) :
    (S - K) * (S + K) = S * S + (S * K + (-(K * S) + -(K * K))) := by
  rw [sub_eq, right_distrib, left_distrib, left_distrib, neg_mul, neg_mul,
      add_assoc]

/-- T1. `[S+K, S-K] = -2 [S,K]`, with `-2 x` written `-(x + x)` so that the
statement needs no multiplicative identity. -/
theorem comm_add_sub (S K : R) :
    comm (S + K) (S - K) = -(comm S K + comm S K) := by
  show (S + K) * (S - K) + -((S - K) * (S + K)) = -(comm S K + comm S K)
  rw [expand_left, expand_right, comm_def]
  rw [neg_add, neg_add, neg_add, neg_neg, neg_neg]
  rw [neg_add, neg_add, neg_neg]
  rw [← add_assoc (-(S * K)) (K * S) (-(K * K)),
      ← add_assoc (-(S * K)) (K * S) (K * K)]
  exact abel4 (S * S) (K * K) (-(S * K) + K * S)

end MyRing

/-- A ring in which `x + x = 0` forces `x = 0`. Real and complex matrices
qualify; characteristic-two rings do not. -/
class TwoTorsionFree (R : Type u) [MyRing R] where
  eq_zero_of_add_self : forall a : R, a + a = 0 -> a = 0

namespace MyRing

variable {R : Type u} [MyRing R]

/-- Corollary. `C = S + K` is normal exactly when `S` and `K` commute.
The forward direction is where the 2-torsion hypothesis is spent. -/
theorem normal_iff_comm_zero [TwoTorsionFree R] (S K : R) :
    comm (S + K) (S - K) = 0 ↔ comm S K = 0 := by
  rw [comm_add_sub]
  constructor
  · intro h
    have h2 : comm S K + comm S K = 0 := by
      have h3 : - -(comm S K + comm S K) = -(0 : R) := congrArg Neg.neg h
      rw [neg_neg, neg_zero] at h3
      exact h3
    exact TwoTorsionFree.eq_zero_of_add_self _ h2
  · intro h
    rw [h, add_zero, neg_zero]

end MyRing

class MyStarRing (R : Type u) extends MyRing R where
  star      : R -> R
  star_star : forall a : R, star (star a) = a
  star_mul  : forall a b : R, star (a * b) = star b * star a

namespace MyStarRing

variable {R : Type u} [MyStarRing R]

/-- T2. Reciprocity. If `B` is symmetric and `V` is `B`-symmetric then `B*V`
is symmetric. Nothing here uses positivity, definiteness or invertibility of
`B` -- only `star B = B`. -/
theorem star_mul_of_symm {B V : R} (hB : star B = B) (hV : star V * B = B * V) :
    star (B * V) = B * V := by
  rw [star_mul, hB, hV]

end MyStarRing

end OperatorFirst
