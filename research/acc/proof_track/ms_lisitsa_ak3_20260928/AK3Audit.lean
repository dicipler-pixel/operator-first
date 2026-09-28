import Init

/-!
# AK(3) ordinary Andrews–Curtis certificate

This self-contained Lean 4 file checks the P ↔ AK(3) leg of the 2024/2025
argument. It uses the paper's 53 hᵢ actions expanded into standard inversions,
relator multiplications, and conjugations. `P` is the 25-letter presentation
from Myasnikov–Myasnikov–Shpilrain. Uppercase letters in the papers mean inverse.

This file proves no stable trivialization of P. The cited 2002 Theorem 1.4
states that the presented group is trivial; it supplies no stable AC path.
-/

namespace AK3Audit

abbrev Word := List Int
abbrev Pair := Word × Word

-- Free reduction, computed after every elementary operation.
def invWord (w : Word) : Word := w.reverse.map (fun x => -x)

def reduceWord (w : Word) : Word :=
  (w.foldl (fun (stack : Word) (x : Int) =>
    match stack with
    | [] => [x]
    | y :: rest => if x == -y then rest else x :: stack) []).reverse

inductive Letter where
  | a | A | b | B
  deriving Repr, DecidableEq

def signed : Letter → Int
  | .a => 1
  | .A => -1
  | .b => 2
  | .B => -2

def inverseLetter : Letter → Letter
  | .a => .A
  | .A => .a
  | .b => .B
  | .B => .b

inductive Move where
  | invL | invR | mulL | mulR
  | conjL (letter : Letter) | conjR (letter : Letter)
  deriving Repr, DecidableEq

-- These are ordinary AC operations. Multiplication is rᵢ ← rᵢrⱼ.
def applyMove : Move → Pair → Pair
  | .invL, (u, v) => (reduceWord (invWord u), v)
  | .invR, (u, v) => (u, reduceWord (invWord v))
  | .mulL, (u, v) => (reduceWord (u ++ v), v)
  | .mulR, (u, v) => (u, reduceWord (v ++ u))
  | .conjL c, (u, v) => (reduceWord ([signed c] ++ u ++ [-signed c]), v)
  | .conjR c, (u, v) => (u, reduceWord ([signed c] ++ v ++ [-signed c]))

def run (p : Pair) : List Move → Pair
  | [] => p
  | m :: ms => run (applyMove m p) ms

-- A witness carries an explicit finite sequence of the permitted operations.
inductive Reach : Pair → Pair → Prop where
  | refl (p : Pair) : Reach p p
  | step (p : Pair) (m : Move) {q : Pair} : Reach (applyMove m p) q → Reach p q

theorem run_reachable : (ms : List Move) → (p : Pair) → Reach p (run p ms)
  | [], p => Reach.refl p
  | m :: ms, p => Reach.step p m (run_reachable ms (applyMove m p))

-- Relators in order, a=1, b=2, A=-1, B=-2.
def P : Pair := ([-1, -2, 1, -2, -1, 2, 1, -2, -2, 1, 2, -1, 2], [-2, -1, 2, 2, -1, -2, 1, 2, 1, -2, -2, 1])
def AK3 : Pair := ([1, 1, 1, -2, -2, -2, -2], [1, 2, 1, -2, -1, -2])

-- h₂ and h₃ are expanded into invert-other, multiply, invert-other.
-- Hence 53 hᵢ instructions become 67 elementary AC moves.
def certificate : List Move := [
  .conjR .a, .conjR .B, .mulL, .conjL .a, .conjR .b, .conjR .A, .conjR .b, .conjR .a,
  .invL, .mulR, .invL, .conjL .b, .conjL .A, .conjR .B, .conjR .B, .conjR .a,
  .conjR .b, .conjR .A, .invL, .mulR, .invL, .conjR .A, .mulL, .invL,
  .mulR, .invL, .conjL .A, .conjR .A, .conjR .B, .conjR .B, .mulR, .conjR .a,
  .conjR .b, .conjL .a, .invL, .mulR, .invL, .conjR .A, .conjL .b, .invR,
  .mulL, .invR, .conjL .B, .conjL .A, .conjR .a, .conjR .B, .conjR .A, .conjR .b,
  .conjL .b, .invL, .mulR, .invL, .conjL .a, .conjR .b, .conjR .a, .invR,
  .mulL, .invR, .conjL .b, .conjL .A, .conjR .A, .conjR .B, .conjR .a, .conjR .b,
  .mulR, .conjR .a, .conjL .a
 ]

set_option maxRecDepth 4096 in
set_option maxHeartbeats 1000000 in
theorem certificate_end : run P certificate = AK3 := by decide

theorem p_to_ak3 : Reach P AK3 := by
  rw [← certificate_end]
  exact run_reachable certificate P

-- Check the reverse route as another finite certificate. A multiplication
-- is undone with three ordinary AC operations.
def undo : Move → List Move
  | .invL => [.invL]
  | .invR => [.invR]
  | .mulL => [.invR, .mulL, .invR]
  | .mulR => [.invL, .mulR, .invL]
  | .conjL c => [.conjL (inverseLetter c)]
  | .conjR c => [.conjR (inverseLetter c)]

def reverseCertificate : List Move := certificate.reverse.flatMap undo

set_option maxRecDepth 4096 in
set_option maxHeartbeats 1000000 in
theorem reverse_end : run AK3 reverseCertificate = P := by decide

theorem ak3_to_p : Reach AK3 P := by
  rw [← reverse_end]
  exact run_reachable reverseCertificate AK3

/-!
The stable system below permits the same three AC operations at every rank,
plus introduction/removal of a fresh generator with its singleton relator.
It records the precise missing premise without assuming that premise.
-/

structure Pres where
  rank : Nat
  rels : List Word
  deriving Repr, DecidableEq

def asPres (p : Pair) : Pres := ⟨2, [p.1, p.2]⟩
def standard : Pres := ⟨2, [[1], [2]]⟩

inductive GMove where
  | invert (i : Nat)
  | multiply (i j : Nat)
  | conjugate (i : Nat) (w : Word)
  deriving Repr, DecidableEq

def validWord (n : Nat) (w : Word) : Bool :=
  w.all (fun x => x != 0 && x.natAbs <= n)

def applyGeneral : GMove → Pres → Option Pres
  | .invert i, p => do
      let r ← p.rels[i]?
      some { p with rels := p.rels.set i (reduceWord (invWord r)) }
  | .multiply i j, p => do
      if i == j then none else
        let r ← p.rels[i]?
        let s ← p.rels[j]?
        some { p with rels := p.rels.set i (reduceWord (r ++ s)) }
  | .conjugate i w, p => do
      if !validWord p.rank w then none else
        let r ← p.rels[i]?
        some { p with rels := p.rels.set i (reduceWord (w ++ r ++ invWord w)) }

def stabilize (p : Pres) : Pres :=
  ⟨p.rank + 1, p.rels ++ [[Int.ofNat (p.rank + 1)]]⟩

inductive StableStep : Pres → Pres → Prop where
  | ac (p q : Pres) (m : GMove) (h : applyGeneral m p = some q) : StableStep p q
  | add (p : Pres) : StableStep p (stabilize p)
  | remove (p : Pres) : StableStep (stabilize p) p

inductive StableReach : Pres → Pres → Prop where
  | refl (p : Pres) : StableReach p p
  | step {p q r : Pres} (h : StableStep p q) (tail : StableReach q r) : StableReach p r

theorem StableReach.trans {p q r : Pres}
    (h₁ : StableReach p q) (h₂ : StableReach q r) : StableReach p r := by
  induction h₁ with
  | refl _ => exact h₂
  | step h _ ih => exact StableReach.step h (ih h₂)

def runGeneral (p : Pres) : List GMove → Option Pres
  | [] => some p
  | m :: ms => (applyGeneral m p).bind (fun q => runGeneral q ms)

theorem checkedRun {p q : Pres} (ms : List GMove)
    (h : runGeneral p ms = some q) : StableReach p q := by
  induction ms generalizing p with
  | nil =>
      have hp : p = q := by simpa [runGeneral] using h
      subst q
      exact StableReach.refl p
  | cons m ms ih =>
      cases hm : applyGeneral m p with
      | none => simp [runGeneral, hm] at h
      | some mid =>
          have ht : runGeneral mid ms = some q := by simpa [runGeneral, hm] using h
          exact StableReach.step (StableStep.ac p mid m hm) (ih ht)

def toGeneral : Move → GMove
  | .invL => .invert 0
  | .invR => .invert 1
  | .mulL => .multiply 0 1
  | .mulR => .multiply 1 0
  | .conjL c => .conjugate 0 [signed c]
  | .conjR c => .conjugate 1 [signed c]

set_option maxRecDepth 8192 in
set_option maxHeartbeats 1500000 in
theorem forward_stable_check :
    runGeneral (asPres P) (certificate.map toGeneral) = some (asPres AK3) := by decide

set_option maxRecDepth 8192 in
set_option maxHeartbeats 1500000 in
theorem reverse_stable_check :
    runGeneral (asPres AK3) (reverseCertificate.map toGeneral) = some (asPres P) := by decide

theorem ak3_to_p_in_stable : StableReach (asPres AK3) (asPres P) :=
  checkedRun _ reverse_stable_check

-- This is the exact dependency that the early paper silently supplied.
theorem ak3_stable_if_p_stable
    (missing : StableReach (asPres P) standard) :
    StableReach (asPres AK3) standard :=
  StableReach.trans ak3_to_p_in_stable missing

end AK3Audit
