/-
ACWindow.lean — core Lean 4 (v4.29.1), no imports, no mathlib.

Self-contained word model of the fourteen ordinary Andrews–Curtis moves of the
SAIR verifier (move_spec ac-r2-v1, commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e):
  0,1   invert relator 0 / 1
  2,3   r0 <- r0 r1 / r0 r1^-1        4,5   r1 <- r1 r0 / r1 r0^-1
  6..9  r0 <- g r0 g^-1, g = x, x^-1, y, y^-1
  10..13 r1 <- g r1 g^-1, same order
Free reduction is the verifier's single left-fold stack cancellation.

What is proved here:
  * fold_r1, fold_r2 : the swap x <-> y, one rotation of the first relator and
    one inversion of the second carry AK(n) to AK(-n-1), for EVERY integer n.
  * cp_resonance_check : in the free product C_p * C_p (runs reduced mod p)
    the normal form of the first relator of AK(n) equals that of AK(n mod p),
    for every p in 2..29 and every n in -10..40.  Kernel-evaluated finite
    control of the resonance identity; the general statement for all n, p is
    NOT formalized here.  (The second relators coincide literally.)
  * cp5_nine_moves : the official moves [1,13,5,11,4,6,3,5,0] carry the image
    of AK(3) in C_5 * C_5 to the image of (x, y).  Kernel-evaluated.
  * letter_fixed_by_conj : a relator equal to a single letter g is fixed by
    conjugation with g (the easy direction of the loop statement).
  * fold_window_check : the fold identity on literal words for -12 <= n <= 12,
    kernel-evaluated (a finite control for fold_r1/fold_r2).

Not formalized here: the AC-triviality of AK(m) for m in {-3,...,2} (which uses
the length-12 theorem of Myasnikov–Myasnikov / Havas–Ramsay and a primitive-
relator argument), the spectral gap, and the embeddability test.  This file is
a word-level kernel; it does not import the official AC.lean (mathlib) and makes
no claim about AC.Reachable.
-/

namespace ACWindow

inductive Gen where
  | x | y
  deriving DecidableEq, Repr

structure Letter where
  g   : Gen
  pos : Bool
  deriving DecidableEq, Repr

abbrev Word := List Letter

def Letter.inv (a : Letter) : Letter := ⟨a.g, !a.pos⟩

@[simp] theorem Letter.inv_inv (a : Letter) : a.inv.inv = a := by
  cases a with
  | mk g p => cases p <;> rfl

/-- Verifier's left-fold stack reduction: push, cancelling against the top. -/
def push (out : Word) (a : Letter) : Word :=
  match out with
  | [] => [a]
  | b :: r => if b = a.inv then r else a :: b :: r

/-- Reduce, keeping the stack reversed; `reduce` returns it in reading order. -/
def reduceRev (w : Word) : Word := w.foldl push []
def reduce (w : Word) : Word := (reduceRev w).reverse

def winv (w : Word) : Word := (w.map Letter.inv).reverse

def swapL (a : Letter) : Letter :=
  match a.g with
  | Gen.x => ⟨Gen.y, a.pos⟩
  | Gen.y => ⟨Gen.x, a.pos⟩

def swap (w : Word) : Word := w.map swapL

def rotate (w : Word) (k : Nat) : Word := w.drop k ++ w.take k

/-- g^k as a literal word, for an integer k. -/
def pow (g : Gen) (k : Int) : Word :=
  if 0 ≤ k then List.replicate k.toNat ⟨g, true⟩
  else List.replicate (-k).toNat ⟨g, false⟩

def X : Letter := ⟨Gen.x, true⟩
def Xi : Letter := ⟨Gen.x, false⟩
def Y : Letter := ⟨Gen.y, true⟩
def Yi : Letter := ⟨Gen.y, false⟩

/-- AK(n) = (x^n y^{-(n+1)},  x y x y^-1 x^-1 y^-1). -/
def AK1 (n : Int) : Word := pow Gen.x n ++ pow Gen.y (-(n + 1))
def R2 : Word := [X, Y, X, Yi, Xi, Yi]
def AK (n : Int) : Word × Word := (AK1 n, R2)

/-! ### The fourteen official moves on freely reduced pairs -/

def conjL (g : Letter) (w : Word) : Word := reduce ([g] ++ w ++ [g.inv])

def gens : List Letter := [X, Xi, Y, Yi]

def move (m : Nat) (s : Word × Word) : Word × Word :=
  let (r0, r1) := s
  match m with
  | 0 => (winv r0, r1)
  | 1 => (r0, winv r1)
  | 2 => (reduce (r0 ++ r1), r1)
  | 3 => (reduce (r0 ++ winv r1), r1)
  | 4 => (r0, reduce (r1 ++ r0))
  | 5 => (r0, reduce (r1 ++ winv r0))
  | 6 => (conjL X r0, r1)
  | 7 => (conjL Xi r0, r1)
  | 8 => (conjL Y r0, r1)
  | 9 => (conjL Yi r0, r1)
  | 10 => (r0, conjL X r1)
  | 11 => (r0, conjL Xi r1)
  | 12 => (r0, conjL Y r1)
  | 13 => (r0, conjL Yi r1)
  | _ => s

def run (ms : List Nat) (s : Word × Word) : Word × Word := ms.foldl (fun t m => move m t) s

/-! ### Lemma B (the fold), for every integer n -/

theorem swap_pow (g : Gen) (k : Int) :
    swap (pow g k) = pow (match g with | Gen.x => Gen.y | Gen.y => Gen.x) k := by
  unfold swap pow
  cases g <;> split <;> simp [List.map_replicate, swapL]

theorem rotate_append (a b : Word) : rotate (a ++ b) a.length = b ++ a := by
  unfold rotate
  simp

/-- Swapping x and y and rotating by the length of the x-block carries the
first relator of AK(n) to the first relator of AK(-n-1). -/
theorem fold_r1 (n : Int) :
    rotate (swap (AK1 n)) (pow Gen.y n).length = AK1 (-n - 1) := by
  unfold AK1
  have hs : swap (pow Gen.x n ++ pow Gen.y (-(n + 1)))
      = pow Gen.y n ++ pow Gen.x (-(n + 1)) := by
    unfold swap
    rw [List.map_append]
    show swap (pow Gen.x n) ++ swap (pow Gen.y (-(n+1))) = _
    rw [swap_pow, swap_pow]
  rw [hs, rotate_append]
  have h1 : -(n + 1) = -n - 1 := by omega
  have h2 : n = -(-n - 1 + 1) := by omega
  have h3 : -(-n - 1 + 1) = n := by omega
  rw [h1, h3]

/-- Inverting the swapped second relator returns the second relator itself. -/
theorem fold_r2 : winv (swap R2) = R2 := by decide

/-! ### Resonance: the image of the first relator in C_p * C_p depends only on n mod p -/

/-- Run form of a word in the free product C_p * C_p: adjacent letters of the
same generator merge, exponents are taken mod p, zero runs are dropped.
Uses the same stack discipline as free reduction. -/
def cpPush (p : Nat) (out : List (Gen × Nat)) (a : Letter) : List (Gen × Nat) :=
  let e : Nat := if a.pos then 1 else p - 1
  match out with
  | [] => [(a.g, e % p)]
  | (g, k) :: r =>
    if g = a.g then
      let k' := (k + e) % p
      if k' = 0 then r else (g, k') :: r
    else (a.g, e % p) :: (g, k) :: r

def cpNormal (p : Nat) (w : Word) : List (Gen × Nat) := (w.foldl (cpPush p) []).reverse

/-- Finite control for the resonance statement: for every p in 2..29 and every
n in -10..40, the normal form of the first relator of AK(n) in C_p * C_p equals
that of AK(n mod p).  Kernel-evaluated. -/
def resonanceCheck : Bool :=
  (List.range 28).all fun i =>
    let p := i + 2
    (List.range 51).all fun j =>
      let n : Int := (j : Int) - 10
      decide (cpNormal p (AK1 n) = cpNormal p (AK1 (n % p)))

theorem cp_resonance_check : resonanceCheck = true := by decide

/-! ### The nine-move certificate in C_5 * C_5 -/

def cpInv (p : Nat) (r : List (Gen × Nat)) : List (Gen × Nat) :=
  (r.map fun gk => (gk.1, (p - gk.2) % p)).reverse

def cpWord (r : List (Gen × Nat)) : Word :=
  r.foldr (fun gk acc => List.replicate gk.2 ⟨gk.1, true⟩ ++ acc) []

def cpMul (p : Nat) (a b : List (Gen × Nat)) : List (Gen × Nat) := cpNormal p (cpWord a ++ cpWord b)
def cpConj (p : Nat) (g : Letter) (r : List (Gen × Nat)) : List (Gen × Nat) :=
  cpNormal p ([g] ++ cpWord r ++ [g.inv])

abbrev CpState := List (Gen × Nat) × List (Gen × Nat)

def cpMove (p : Nat) (m : Nat) (s : CpState) : CpState :=
  let (r0, r1) := s
  match m with
  | 0 => (cpInv p r0, r1)
  | 1 => (r0, cpInv p r1)
  | 2 => (cpMul p r0 r1, r1)
  | 3 => (cpMul p r0 (cpInv p r1), r1)
  | 4 => (r0, cpMul p r1 r0)
  | 5 => (r0, cpMul p r1 (cpInv p r0))
  | 6 => (cpConj p X r0, r1)
  | 7 => (cpConj p Xi r0, r1)
  | 8 => (cpConj p Y r0, r1)
  | 9 => (cpConj p Yi r0, r1)
  | 10 => (r0, cpConj p X r1)
  | 11 => (r0, cpConj p Xi r1)
  | 12 => (r0, cpConj p Y r1)
  | 13 => (r0, cpConj p Yi r1)
  | _ => s

def cpRun (p : Nat) (ms : List Nat) (s : CpState) : CpState := ms.foldl (fun t m => cpMove p m t) s

def ninePath : List Nat := [1, 13, 5, 11, 4, 6, 3, 5, 0]

/-- In C_5 * C_5 the official moves 1,13,5,11,4,6,3,5,0 carry the image of AK(3)
to the image of the standard pair (x, y). -/
theorem cp5_nine_moves :
    cpRun 5 ninePath (cpNormal 5 (AK1 3), cpNormal 5 R2) = ([(Gen.x, 1)], [(Gen.y, 1)]) := by
  decide

/-! ### A letter relator is fixed by conjugation with that letter -/

theorem letter_ne_inv (g : Letter) : g ≠ g.inv := by
  cases g with
  | mk a p => cases p <;> simp [Letter.inv]

theorem letter_fixed_by_conj (g : Letter) : conjL g [g] = [g] := by
  unfold conjL reduce reduceRev
  simp [List.foldl, push, letter_ne_inv g]

/-! ### Finite control for the fold on literal words, -12 <= n <= 12 -/

def foldCheck : Bool :=
  (List.range 25).all fun j =>
    let n : Int := (j : Int) - 12
    decide (rotate (swap (AK1 n)) (pow Gen.y n).length = AK1 (-n - 1)) &&
    decide (winv (swap R2) = R2)

theorem fold_window_check : foldCheck = true := by decide

end ACWindow
