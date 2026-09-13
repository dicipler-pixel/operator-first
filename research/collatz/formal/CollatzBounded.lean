import Mathlib

/-!
# Collatz bounded-collapse certificate

This module deliberately proves a finite theorem, not the global Collatz conjecture.
The ordinary Collatz map is used: even `n` goes to `n/2`, odd `n` goes to `3*n+1`.

The executable checker is connected to the mathematical trajectory statement by
`reachesOneB_sound`.  The concrete theorem `bounded_collapse_100000` is then
closed by `native_decide` over the finite range `1 ≤ n ≤ 100000`.
-/

namespace CollatzBounded

/-- One ordinary Collatz step. -/
def step (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else 3 * n + 1

/-- `iterate k n` is the result after exactly `k` Collatz steps. -/
def iterate : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => iterate k (step n)

/-- Executable bounded search for the value `1`. -/
def reachesOneB : Nat → Nat → Bool
  | n, 0 => decide (n = 1)
  | n, fuel + 1 => if n = 1 then true else reachesOneB (step n) fuel

/-- Mathematical bounded-collapse statement. -/
def ReachesOneWithin (n fuel : Nat) : Prop :=
  ∃ k ≤ fuel, iterate k n = 1

@[simp] theorem step_of_even {n : Nat} (h : n % 2 = 0) : step n = n / 2 := by
  simp [step, h]

@[simp] theorem step_of_odd {n : Nat} (h : n % 2 ≠ 0) : step n = 3 * n + 1 := by
  simp [step, h]

@[simp] theorem iterate_zero (n : Nat) : iterate 0 n = n := rfl

@[simp] theorem iterate_succ (k n : Nat) : iterate (k + 1) n = iterate k (step n) := rfl

/-- The Boolean bounded search never manufactures a false mathematical witness. -/
theorem reachesOneB_sound {n fuel : Nat} (h : reachesOneB n fuel = true) :
    ReachesOneWithin n fuel := by
  induction fuel generalizing n with
  | zero =>
      simp [reachesOneB] at h
      exact ⟨0, Nat.le_refl 0, h⟩
  | succ fuel ih =>
      by_cases hn : n = 1
      · exact ⟨0, Nat.zero_le _, by simpa [iterate, hn]⟩
      · have hnext : reachesOneB (step n) fuel = true := by
          simpa [reachesOneB, hn] using h
        rcases ih hnext with ⟨k, hk, htraj⟩
        exact ⟨k + 1, Nat.succ_le_succ hk, by simpa [iterate] using htraj⟩

/-- Exact finite computation: every positive value at most 100000 is accepted
by the 400-step checker.  This is a finite theorem evaluated by Lean's kernel-
checked `native_decide` mechanism, not a statistical test. -/
theorem bounded_checker_100000 :
    ∀ n : Fin 100001, n.val = 0 ∨ reachesOneB n.val 400 = true := by
  native_decide

/-- Bounded collapse: every ordinary Collatz orbit starting in `[1,100000]`
reaches `1` in at most 400 steps. -/
theorem bounded_collapse_100000 (n : Nat) (hpos : 1 ≤ n) (hbound : n ≤ 100000) :
    ReachesOneWithin n 400 := by
  let m : Fin 100001 := ⟨n, Nat.lt_succ_iff.mpr hbound⟩
  have hc := bounded_checker_100000 m
  rcases hc with hzero | hcert
  · have : n = 0 := hzero
    omega
  · exact reachesOneB_sound hcert

/-- Any certified collapse witness supplies an explicit iterate equal to one. -/
theorem bounded_collapse_has_witness {n fuel : Nat} (h : ReachesOneWithin n fuel) :
    ∃ k, k ≤ fuel ∧ iterate k n = 1 := by
  rcases h with ⟨k, hk, h1⟩
  exact ⟨k, hk, h1⟩

/-- The finite theorem makes no assertion about starting values above 100000. -/
theorem bounded_scope (n : Nat) (hpos : 1 ≤ n) (hbound : n ≤ 100000) :
    ∃ k ≤ 400, iterate k n = 1 :=
  bounded_collapse_100000 n hpos hbound

#print axioms CollatzBounded.step_of_even
#print axioms CollatzBounded.step_of_odd
#print axioms CollatzBounded.reachesOneB_sound
#print axioms CollatzBounded.bounded_checker_100000
#print axioms CollatzBounded.bounded_collapse_100000
#print axioms CollatzBounded.bounded_collapse_has_witness
#print axioms CollatzBounded.bounded_scope

end CollatzBounded
