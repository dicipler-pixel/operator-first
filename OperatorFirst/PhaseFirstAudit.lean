/-!
# Phase-first and quantum-information audit

This file formalizes only the exact algebraic core recovered from the user's
17--18 September 2026 notes. Empirical physics claims are deliberately not
encoded as theorems merely to make them compile.

The formalized content is:

* Bell-pair normalization as an algebraic condition.
* The four Pauli correction identities underlying the standard teleportation
  correction table.
* Frequency doubling ("octaves") as ordinary powers of two.
* The distinction between a phase wavenumber and a dimensionless calibrated
  quantity.
* The vacuum-photon sanity check: if k = omega / c with nonzero omega and c,
  then k is not zero.
* Snell rescaling: tangential phase continuity survives division by a common
  reference wavenumber.
* A finite arithmetic counterexample to the proposed width-only
  fragmentation threshold for the rho(770) numbers used in the research note.
* A Lipschitz window bound showing that observable variation depends on both
  spectral width and response sensitivity.
* A minimal countermodel showing that equality of one coarse scalar label does
  not identify the underlying state.

No theorem below proves a zeta zero, the no-communication theorem,
spin-statistics, hyperbolicity of a knot, QGP phenomenology, or a physical
phase-class observable.
-/

import Mathlib

namespace OperatorFirst.PhaseFirstAudit

/-! ## Bell normalization and teleportation correction algebra -/

section Teleportation

variable {R : Type*} [Ring R]

/-- A two-component amplitude register. This is only the algebra needed for
the Pauli correction table; it is not a Hilbert-space teleportation theorem. -/
abbrev Qubit := R × R

/-- Pauli-X action on amplitudes. -/
def X (q : Qubit) : Qubit := (q.2, q.1)

/-- Pauli-Z action on amplitudes. -/
def Z (q : Qubit) : Qubit := (q.1, -q.2)

/-- First Z, then X. -/
def XZ (q : Qubit) : Qubit := X (Z q)

/-- First X, then Z. -/
def ZX (q : Qubit) : Qubit := Z (X q)

theorem X_involutive (q : Qubit) : X (X q) = q := by
  rcases q with ⟨a, b⟩
  rfl

theorem Z_involutive (q : Qubit) : Z (Z q) = q := by
  rcases q with ⟨a, b⟩
  simp [Z]

/-- Bell-result 00: no correction is required. -/
theorem teleport_correction_00 (q : Qubit) : q = q := rfl

/-- Bell-result 01: an X error is corrected by X. -/
theorem teleport_correction_01 (q : Qubit) : X (X q) = q :=
  X_involutive q

/-- Bell-result 10: a Z error is corrected by Z. -/
theorem teleport_correction_10 (q : Qubit) : Z (Z q) = q :=
  Z_involutive q

/-- Bell-result 11 in the convention XZ q: correction ZX recovers q. -/
theorem teleport_correction_11 (q : Qubit) : ZX (XZ q) = q := by
  rcases q with ⟨a, b⟩
  simp [ZX, XZ, X, Z]

end Teleportation

section BellNormalization

variable {R : Type*} [Ring R]

/-- If each of the two nonzero Bell amplitudes has square s^2 and
2*s^2 = 1, their total algebraic square-weight is one. The analytic choice
s = 1/sqrt(2) is intentionally kept outside this ring-level lemma. -/
theorem bell_phi_plus_square_weight (s : R) (h : (2 : R) * s ^ 2 = 1) :
    s ^ 2 + s ^ 2 = 1 := by
  simpa [two_mul] using h

end BellNormalization

/-! ## Ordinary octave scaling -/

section Octaves

variable {R : Type*} [CommSemiring R]

/-- Frequency doubling is just the recursion for powers of two. -/
theorem octave_step (F0 : R) (k : ℕ) :
    F0 * (2 : R) ^ (k + 1) = 2 * (F0 * (2 : R) ^ k) := by
  rw [pow_succ]
  ring

end Octaves

/-! ## Phase wavenumber versus dimensionless calibration -/

/-- Quantity with dimensions of inverse velocity. Keeping a separate type
prevents silently adding it to a dimensionless loop phase. -/
structure InvVelocity where
  val : ℝ

/-- Dimensionless scalar. -/
structure Dimensionless where
  val : ℝ

/-- A reference velocity is required before an inverse-velocity quantity is
turned into a dimensionless scalar. -/
def normalizeDispersion (vRef : ℝ) (d : InvVelocity) : Dimensionless :=
  ⟨vRef * d.val⟩

section PhaseWavenumber

variable {K : Type*} [Field K]

/-- Algebraic phase wavenumber omega / v. -/
def phaseWavenumber (ω v : K) : K := ω / v

theorem phaseWavenumber_ne_zero {ω v : K} (hω : ω ≠ 0) (hv : v ≠ 0) :
    phaseWavenumber ω v ≠ 0 := by
  exact div_ne_zero hω hv

/-- If phase wavenumber is omega/c, setting it to zero at nonzero c forces
zero frequency. -/
theorem zero_phaseWavenumber_forces_zero_frequency {ω c : K} (hc : c ≠ 0)
    (h : phaseWavenumber ω c = 0) : ω = 0 := by
  by_contra hω
  exact phaseWavenumber_ne_zero hω hc h

/-- Dividing both sides of tangential phase continuity by the same reference
scale preserves the Snell-type relation. -/
theorem snell_rescale (k₁ k₂ s₁ s₂ k0 : K)
    (h : k₁ * s₁ = k₂ * s₂) :
    (k₁ / k0) * s₁ = (k₂ / k0) * s₂ := by
  calc
    (k₁ / k0) * s₁ = (k₁ * s₁) / k0 := by ring
    _ = (k₂ * s₂) / k0 := by rw [h]
    _ = (k₂ / k0) * s₂ := by ring

end PhaseWavenumber

/-! ## Width-only fragmentation fails as an iff criterion -/

/-- Rejected toy threshold: fragmentation is declared when width Gamma is at
least the chosen internal scale E. -/
def widthOnlyFragmentation (Γ E : ℚ) : Prop := E ≤ Γ

/-- With the pasted rho(770) values Gamma = 147.4 MeV and E = 775.26 MeV,
the proposed threshold is false. -/
theorem rho770_not_fragmented_by_width_only :
    ¬ widthOnlyFragmentation (737 / 5 : ℚ) (38763 / 50 : ℚ) := by
  norm_num [widthOnlyFragmentation]

theorem rho770_width_mass_ratio_lt_one :
    (737 / 5 : ℚ) / (38763 / 50 : ℚ) < 1 := by
  norm_num

/-! ## A repair: width times observable sensitivity -/

section CompressionWindow

/-- A local Lipschitz response estimate implies a finite spectral-window
variation bound. Width alone cannot determine response fragmentation. -/
theorem response_window_bound (F : ℝ → ℝ) (E0 E Γ L : ℝ)
    (hL : 0 ≤ L)
    (hLip : ∀ x, |F x - F E0| ≤ L * |x - E0|)
    (hWindow : |E - E0| ≤ Γ / 2) :
    |F E - F E0| ≤ L * (Γ / 2) := by
  calc
    |F E - F E0| ≤ L * |E - E0| := hLip E
    _ ≤ L * (Γ / 2) := mul_le_mul_of_nonneg_left hWindow hL

end CompressionWindow

/-! ## One scalar label does not determine the state -/

/-- A deliberately minimal coarse observable. -/
def coarseLabel (_ : Bool) : Nat := 0

/-- Equality of one scalar descriptor is logically insufficient to identify
the underlying state. This is a countermodel to that inference pattern, not a
quantum exchange theorem. -/
theorem equal_coarse_label_not_equal_state :
    coarseLabel false = coarseLabel true ∧ false ≠ true := by
  constructor
  · rfl
  · decide

/-! ## A harmless oscillation identity -/

theorem cosine_square_nonnegative (x : ℝ) : 0 ≤ Real.cos x ^ 2 :=
  sq_nonneg _

end OperatorFirst.PhaseFirstAudit

#print axioms OperatorFirst.PhaseFirstAudit.teleport_correction_11
#print axioms OperatorFirst.PhaseFirstAudit.bell_phi_plus_square_weight
#print axioms OperatorFirst.PhaseFirstAudit.octave_step
#print axioms OperatorFirst.PhaseFirstAudit.zero_phaseWavenumber_forces_zero_frequency
#print axioms OperatorFirst.PhaseFirstAudit.snell_rescale
#print axioms OperatorFirst.PhaseFirstAudit.rho770_not_fragmented_by_width_only
#print axioms OperatorFirst.PhaseFirstAudit.response_window_bound
#print axioms OperatorFirst.PhaseFirstAudit.equal_coarse_label_not_equal_state
