/-!
# JB certification — finite transport kernels (Mathlib, no analysis)

Source pack: `CLAUDE_CERTIFICATION_HANDOFF_2026-09-12.md` (Drive, Mad Hatters ACC Shared Hub);
*What Transport Keeps*, research edition 3, Theorems 3 and 4 (grade [T]+[C]);
*The Companion-Matrix Projector Diagnostic* (conserved Casoratian pairing, Kronecker factorization).

Tags: `JB-PROJ-001` / `JB-WTK3-001` conserved pairing (Theorem 3, first display and the
moving-coordinate statement); `JB-WTK3-002` coboundary transport (Theorem 4, first display).

Every statement is finite algebra in an abstract monoid or group, so it specialises to
invertible matrices over any field (`JBCertMatrix.lean`). No recessive-mode selection, no
readout-error bound, no asymptotics, no spectral or physical statement is made here; those
are fenced in `CERTIFICATION_REGISTRY_JB.md`.
-/
import Mathlib.Algebra.Group.Basic
import Mathlib.Algebra.Group.Defs

namespace JBCert

section ConservedPairing

variable {G : Type*} [Monoid G]

/-- `JB-PROJ-001` (one step, monoid form). If `M * Minv = 1`, the pairing of a row `ℓ`
transported as `ℓ ↦ ℓ * M` with a column `z` transported as `z ↦ Minv * z` is unchanged.
Theorem 3 of *What Transport Keeps* is the case `M = Aₙ⁻¹`, `Minv = Aₙ`, i.e.
`ℓₙ₊₁ᵀ = ℓₙᵀ Aₙ⁻¹` (equivalently `ℓₙ₊₁ = Aₙ⁻ᵀ ℓₙ`) and `xₙ₊₁ = Aₙ xₙ`. -/
theorem pairing_conserved_step (ℓ z M Minv : G) (h : M * Minv = 1) :
    (ℓ * M) * (Minv * z) = ℓ * z := by
  calc (ℓ * M) * (Minv * z) = ℓ * (M * Minv) * z := by simp only [mul_assoc]
    _ = ℓ * z := by rw [h, mul_one]

/-- Row after transporting through the listed steps in order. -/
def rowAfter (ℓ : G) : List (G × G) → G
  | [] => ℓ
  | p :: ps => rowAfter (ℓ * p.1) ps

/-- Column after transporting through the same steps; each inverse acts on the left. -/
def colAfter (z : G) : List (G × G) → G
  | [] => z
  | p :: ps => colAfter (p.2 * z) ps

/-- `JB-PROJ-001` (finite iteration). Along any finite list of steps `(Mₖ, Minvₖ)` with
`Mₖ * Minvₖ = 1`, the pairing is invariant at every index. -/
theorem pairing_conserved_iter (ℓ z : G) (Ms : List (G × G))
    (h : ∀ p ∈ Ms, p.1 * p.2 = 1) :
    rowAfter ℓ Ms * colAfter z Ms = ℓ * z := by
  induction Ms generalizing ℓ z with
  | nil => rfl
  | cons p ps ih =>
    have hp : p.1 * p.2 = 1 := h p (by simp)
    have hps : ∀ q ∈ ps, q.1 * q.2 = 1 := fun q hq => h q (by simp [hq])
    simp only [rowAfter, colAfter]
    rw [ih (ℓ * p.1) (p.2 * z) hps]
    exact pairing_conserved_step ℓ z p.1 p.2 hp

/-- Theorem 3, moving coordinate change: with `x' = S⁻¹ x` and `ℓ'ᵀ = ℓᵀ S`
(i.e. `ℓ' = Sᵀ ℓ`), the pairing is unchanged. Same algebra as the transport step. -/
theorem pairing_gauge_invariant (ℓ x S Sinv : G) (h : S * Sinv = 1) :
    (ℓ * S) * (Sinv * x) = ℓ * x :=
  pairing_conserved_step ℓ x S Sinv h

end ConservedPairing

section Coboundary

variable {G : Type*} [Group G]

/-- Right-ordered product `f 0 * f 1 * ⋯ * f (N-1)`. -/
def prodUpTo (f : ℕ → G) : ℕ → G
  | 0 => 1
  | N + 1 => prodUpTo f N * f N

/-- `JB-WTK3-002` (Theorem 4 of *What Transport Keeps*, first display). For right-ordered
transports with `T n * U (n+1) = U n * C n`, successive cancellation gives
`T 0 ⋯ T (N-1) = U 0 * (C 0 ⋯ C (N-1)) * (U N)⁻¹`. Both endpoint frames appear. -/
theorem coboundary_transport (T U C : ℕ → G)
    (h : ∀ n, T n * U (n + 1) = U n * C n) (N : ℕ) :
    prodUpTo T N = U 0 * prodUpTo C N * (U N)⁻¹ := by
  induction N with
  | zero => simp [prodUpTo]
  | succ N ih =>
    have key : (U N)⁻¹ * T N = C N * (U (N + 1))⁻¹ := by
      have h1 : T N = U N * C N * (U (N + 1))⁻¹ := by
        rw [← h N, mul_assoc, mul_inv_cancel, mul_one]
      rw [h1, ← mul_assoc, ← mul_assoc, inv_mul_cancel, one_mul]
    calc prodUpTo T (N + 1) = prodUpTo T N * T N := rfl
      _ = U 0 * prodUpTo C N * (U N)⁻¹ * T N := by rw [ih]
      _ = U 0 * prodUpTo C N * ((U N)⁻¹ * T N) := by simp only [mul_assoc]
      _ = U 0 * prodUpTo C N * (C N * (U (N + 1))⁻¹) := by rw [key]
      _ = U 0 * (prodUpTo C N * C N) * (U (N + 1))⁻¹ := by simp only [mul_assoc]
      _ = U 0 * prodUpTo C (N + 1) * (U (N + 1))⁻¹ := rfl

/-- Consequence stated in Theorem 4: omitting the terminal frame `U N` changes the
comparison unless `U N = 1`; precisely, the transport product equals the conjugated
coboundary product `U 0 * prodUpTo C N * (U 0)⁻¹` exactly when `U N = U 0`. -/
theorem coboundary_endpoint_matters (T U C : ℕ → G)
    (h : ∀ n, T n * U (n + 1) = U n * C n) (N : ℕ) (hUN : U N = U 0) :
    prodUpTo T N = U 0 * prodUpTo C N * (U 0)⁻¹ := by
  rw [coboundary_transport T U C h N, hUN]

end Coboundary

end JBCert
