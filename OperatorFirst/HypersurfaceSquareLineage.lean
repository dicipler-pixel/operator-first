import Mathlib

/-!
# OperatorFirst.HypersurfaceSquareLineage

Formal reconstruction of the recovered lineage

  spacing
    -> inverse-gap-square response
    -> projector / metric coefficient
    -> Snell-Clairaut refraction
    -> squared refraction law
    -> fold / Gram squaring
    -> three-body fourth-power rigidity
    -> four-body normal suppression
    -> fixed-spacing angle-dependent response

The purpose of this file is to formalize the *logical skeleton* of the recovered
three-body / four-body / hypersurface / spacing programme.

Important scope:
* It does not assert that ionization energies, band gaps, transport gaps, and
  geometric principal angles are numerically identical.
* It does not identify a rigidity functional with a refractive index unless
  that identification is explicitly assumed.
* It does not derive a physical Hamiltonian for Cu/Ag/Au/Pt.
* It does not prove a continuum gravity law.
* Model-specific analytic facts (for example a simple fold zero) are exposed as
  hypotheses and their consequences are proved exactly.

This is intended for the repository's pinned Lean/mathlib toolchain.
-/

open scoped BigOperators

namespace OperatorFirst.HypersurfaceSquareLineage

/-! -------------------------------------------------------------------------
    I. SPACING -> INVERSE-SQUARE GEOMETRIC RESPONSE
    ------------------------------------------------------------------------- -/

/-- The elementary algebra behind inverse-gap-square weights:
if the first-order response is `a / Δ`, its quadratic metric contribution is
`a² / Δ²`. -/
theorem response_square_is_gap_square
    (a Δ : ℝ) (hΔ : Δ ≠ 0) :
    (a / Δ) ^ 2 = a ^ 2 / Δ ^ 2 := by
  field_simp [hΔ]
  ring

/-- Positive gap-squared weights are nonnegative. -/
theorem gap_square_weight_nonneg
    (a Δ : ℝ) :
    0 ≤ a ^ 2 / Δ ^ 2 := by
  positivity

/-- For fixed nonzero coupling, increasing the positive gap decreases the
inverse-gap-square factor. -/
theorem inverse_gap_square_antitone
    (Δ₁ Δ₂ : ℝ) (h1 : 0 < Δ₁) (h12 : Δ₁ ≤ Δ₂) :
    1 / Δ₂ ^ 2 ≤ 1 / Δ₁ ^ 2 := by
  have h2 : 0 < Δ₂ := lt_of_lt_of_le h1 h12
  have hs : Δ₁ ^ 2 ≤ Δ₂ ^ 2 := by nlinarith
  exact one_div_le_one_div_of_le (sq_pos_of_pos h1) hs

/-- Scaling a gap by a positive factor rescales the inverse-gap-square
susceptibility by the inverse square of that factor. -/
theorem inverse_gap_square_scaling
    (Δ c : ℝ) (hΔ : Δ ≠ 0) (hc : c ≠ 0) :
    1 / (c * Δ) ^ 2 = (1 / c ^ 2) * (1 / Δ ^ 2) := by
  field_simp [hΔ, hc]
  ring

/-! -------------------------------------------------------------------------
    II. GEOMETRIC INDEX -> SNELL / CLAIRAUT
    ------------------------------------------------------------------------- -/

/-- A squared Snell law is exactly the square of the ordinary Snell law. -/
theorem snell_implies_squared_snell
    (n₁ n₂ θ₁ θ₂ : ℝ)
    (h : n₁ * Real.sin θ₁ = n₂ * Real.sin θ₂) :
    n₁ ^ 2 * Real.sin θ₁ ^ 2 = n₂ ^ 2 * Real.sin θ₂ ^ 2 := by
  nlinarith [sq_nonneg (n₁ * Real.sin θ₁ - n₂ * Real.sin θ₂)]

/-- Writing `g = n²`, ordinary Snell is equivalent to the commonly used
`g sin² θ` invariant after squaring. -/
theorem metric_snell_squared
    (n₁ n₂ g₁ g₂ θ₁ θ₂ : ℝ)
    (hg1 : g₁ = n₁ ^ 2)
    (hg2 : g₂ = n₂ ^ 2)
    (hSnell : n₁ * Real.sin θ₁ = n₂ * Real.sin θ₂) :
    g₁ * Real.sin θ₁ ^ 2 = g₂ * Real.sin θ₂ ^ 2 := by
  subst g₁
  subst g₂
  exact snell_implies_squared_snell n₁ n₂ θ₁ θ₂ hSnell

/-- If the squared metric index is conserved and both indices are positive,
then the unsquared Snell quantities agree up to the positive square root
choice encoded by the supplied equality `n² = g`. -/
theorem squared_snell_from_metric_index
    (n₁ n₂ g₁ g₂ s₁ s₂ : ℝ)
    (hn1 : 0 ≤ n₁) (hn2 : 0 ≤ n₂)
    (hg1 : g₁ = n₁ ^ 2) (hg2 : g₂ = n₂ ^ 2)
    (hs1 : 0 ≤ s₁) (hs2 : 0 ≤ s₂)
    (h : g₁ * s₁ ^ 2 = g₂ * s₂ ^ 2) :
    n₁ * s₁ = n₂ * s₂ := by
  subst g₁
  subst g₂
  have hsq : (n₁ * s₁)^2 = (n₂ * s₂)^2 := by
    simpa [mul_pow] using h
  have hleft : 0 ≤ n₁ * s₁ := mul_nonneg hn1 hs1
  have hright : 0 ≤ n₂ * s₂ := mul_nonneg hn2 hs2
  nlinarith

/-! -------------------------------------------------------------------------
    III. PRINCIPAL-ANGLE / SUBSPACE ROTATION READING
    ------------------------------------------------------------------------- -/

/-- The rank-one chordal quantity used throughout the programme. -/
noncomputable def rankOneChordalSq (θ : ℝ) : ℝ :=
  2 * Real.sin θ ^ 2

theorem rankOneChordalSq_nonneg (θ : ℝ) :
    0 ≤ rankOneChordalSq θ := by
  unfold rankOneChordalSq
  positivity

/-- The metric coefficient `g = sin² θ` produces the index
`n = sqrt g = |sin θ|`. -/
theorem sqrt_sin_sq (θ : ℝ) :
    Real.sqrt (Real.sin θ ^ 2) = |Real.sin θ| := by
  simpa [sq_abs] using Real.sqrt_sq_eq_abs (Real.sin θ)

/-! -------------------------------------------------------------------------
    IV. FOLD -> GRAM SQUARE -> FOURTH-POWER RIGIDITY
    ------------------------------------------------------------------------- -/

/-- First squaring: a simple soft scale `s` becomes a Gram eigenvalue `s²`. -/
def gramSoft (s : ℝ) : ℝ := s ^ 2

/-- Second squaring/inversion: the historical rigidity used in the three-body
work is the inverse square of the soft Gram eigenvalue. -/
def rigidityFromGram (λ : ℝ) : ℝ := 1 / λ ^ 2

/-- Combining the two definitions gives the fourth power exactly. -/
theorem fold_gram_rigidity_fourth_power
    (s : ℝ) (hs : s ≠ 0) :
    rigidityFromGram (gramSoft s) = 1 / s ^ 4 := by
  unfold rigidityFromGram gramSoft
  field_simp [hs]
  ring

/-- The specific `cos` form used on the three-body shape sphere. -/
theorem three_body_sec_four
    (θ : ℝ) (hc : Real.cos θ ≠ 0) :
    rigidityFromGram (Real.cos θ ^ 2) = 1 / Real.cos θ ^ 4 := by
  unfold rigidityFromGram
  field_simp [hc]
  ring

/-- If a local coordinate has a simple zero `s(ε)=c ε`, then the same
construction gives an exact `ε⁻⁴` law. -/
theorem simple_zero_gives_inverse_fourth
    (c ε : ℝ) (hc : c ≠ 0) (hε : ε ≠ 0) :
    rigidityFromGram ((c * ε) ^ 2)
      = (1 / c ^ 4) * (1 / ε ^ 4) := by
  unfold rigidityFromGram
  field_simp [hc, hε]
  ring

/-! -------------------------------------------------------------------------
    V. THREE-BODY REFRACTION CHAIN
    ------------------------------------------------------------------------- -/

/-- Once a three-body model supplies a positive rigidity `R` and the
variational interface law is assumed, squaring the ordinary Snell relation is
not an independent physical law. -/
theorem three_body_refraction_is_squared_snell
    (R₁ R₂ θ₁ θ₂ : ℝ)
    (hSnell : Real.sqrt R₁ * Real.sin θ₁
            = Real.sqrt R₂ * Real.sin θ₂)
    (hR1 : 0 ≤ R₁) (hR2 : 0 ≤ R₂) :
    R₁ * Real.sin θ₁ ^ 2 = R₂ * Real.sin θ₂ ^ 2 := by
  have hs := congrArg (fun x : ℝ => x^2) hSnell
  rw [mul_pow, mul_pow,
      Real.sq_sqrt hR1, Real.sq_sqrt hR2] at hs
  exact hs

/-! -------------------------------------------------------------------------
    VI. FOUR-BODY HYPERSURFACE: NORMAL SUPPRESSION
    ------------------------------------------------------------------------- -/

/-- Minimal scalar abstraction of the four-body binary-wall block:
parallel motion evolves through `A`, normal motion through the squeeze `2λ`.
The lower-left block is zero, so purely parallel input cannot generate a normal
component. -/
def fourBodyWallMap
    (A shear λ parallel normal : ℝ) : ℝ × ℝ :=
  (A * parallel + shear * normal, (2 * λ) * normal)

theorem four_body_parallel_stays_tangent
    (A shear λ parallel : ℝ) :
    (fourBodyWallMap A shear λ parallel 0).2 = 0 := by
  simp [fourBodyWallMap]

/-- The normal component is scaled exactly by `2λ`. -/
theorem four_body_normal_squeeze
    (A shear λ parallel normal : ℝ) :
    (fourBodyWallMap A shear λ parallel normal).2 = 2 * λ * normal := by
  simp [fourBodyWallMap, mul_assoc]

/-- Vanishing normal squeeze produces a rank-drop in this reduced block. -/
theorem four_body_zero_squeeze_kills_normal
    (A shear parallel normal : ℝ) :
    (fourBodyWallMap A shear 0 parallel normal).2 = 0 := by
  simp [fourBodyWallMap]

/-! -------------------------------------------------------------------------
    VII. FIXED SPACING, CHANGING ORIENTATION
    ------------------------------------------------------------------------- -/

/-- Two-level eigenvalues stay fixed at `±Δ/2` in the recovered rotating
two-level model; this helper records the squared spacing. -/
def twoLevelGapSq (Δ : ℝ) : ℝ := Δ ^ 2

/-- Dipole/orientation strength used in the electronic-sheet control. -/
noncomputable def orientationWeight (θ : ℝ) : ℝ :=
  Real.sin θ ^ 2

theorem orientationWeight_nonneg (θ : ℝ) :
    0 ≤ orientationWeight θ := by
  unfold orientationWeight
  positivity

/-- At fixed gap, orientation can still change the response weight. -/
theorem fixed_gap_does_not_fix_orientation_weight :
    orientationWeight 0 = 0 ∧
    orientationWeight (Real.pi / 2) = 1 := by
  constructor
  · simp [orientationWeight]
  · simp [orientationWeight]

/-- Recovered model conductance factor, stripped to its exact scalar content. -/
noncomputable def conductanceFactor
    (Δ γ θ : ℝ) : ℝ :=
  (γ ^ 2 * (Δ / 2) ^ 2 * Real.sin θ ^ 2) /
    (((Δ / 2) ^ 2 + γ ^ 2 / 4) ^ 2)

/-- In the recovered electronic-sheet model, conductance vanishes when the
orbital orientation is aligned so that `sin θ = 0`. -/
theorem conductance_zero_at_zero_angle
    (Δ γ : ℝ) :
    conductanceFactor Δ γ 0 = 0 := by
  simp [conductanceFactor]

/-- For fixed `Δ` and `γ`, the only angular dependence of the numerator is
`sin² θ`. -/
theorem conductance_numerator_factor
    (Δ γ θ : ℝ) :
    γ ^ 2 * (Δ / 2) ^ 2 * Real.sin θ ^ 2
      = (γ ^ 2 * (Δ / 2) ^ 2) * orientationWeight θ := by
  simp [orientationWeight]
  ring

/-! -------------------------------------------------------------------------
    VIII. KEEP THE SPACING NOTIONS DISTINCT
    ------------------------------------------------------------------------- -/

/-- A tiny type-level guardrail: different spacing notions are represented by
different constructors, preventing accidental numerical identification without
an explicit map. -/
inductive SpacingKind
  | ionization
  | bandGap
  | principalAngle
  | spatial
  | channel
deriving DecidableEq, Repr

structure SpacingMeasurement where
  kind : SpacingKind
  value : ℝ

/-- Two measurements of different kinds are not definitionally the same
measurement even when the stored real number happens to agree. -/
theorem different_kind_measurements_ne
    (x : ℝ) :
    ({ kind := SpacingKind.ionization, value := x } : SpacingMeasurement)
      ≠
    ({ kind := SpacingKind.bandGap, value := x } : SpacingMeasurement) := by
  intro h
  have hk := congrArg SpacingMeasurement.kind h
  cases hk

/-! -------------------------------------------------------------------------
    IX. MASTER CONDITIONAL LINEAGE
    ------------------------------------------------------------------------- -/

/-- Compact theorem expressing the recovered logical spine.

Hypotheses:
* `q = a/Δ` is the first-order cross-subspace response.
* `g = q²` is the quadratic metric coefficient.
* `n² = g` defines the positive refractive index.
* `n sin θ` is conserved across an interface.

Conclusion:
* the metric Snell quantity `g sin² θ` is conserved.

This does not identify `a`, `Δ`, `g`, or `n` with any specific physical model;
that identification belongs in the relevant realization theorem.
-/
theorem spacing_to_hypersurface_refraction
    (a₁ a₂ Δ₁ Δ₂ q₁ q₂ g₁ g₂ n₁ n₂ θ₁ θ₂ : ℝ)
    (hΔ1 : Δ₁ ≠ 0) (hΔ2 : Δ₂ ≠ 0)
    (hq1 : q₁ = a₁ / Δ₁)
    (hq2 : q₂ = a₂ / Δ₂)
    (hg1 : g₁ = q₁ ^ 2)
    (hg2 : g₂ = q₂ ^ 2)
    (hn1 : g₁ = n₁ ^ 2)
    (hn2 : g₂ = n₂ ^ 2)
    (hSnell : n₁ * Real.sin θ₁ = n₂ * Real.sin θ₂) :
    g₁ * Real.sin θ₁ ^ 2 = g₂ * Real.sin θ₂ ^ 2 := by
  exact metric_snell_squared n₁ n₂ g₁ g₂ θ₁ θ₂ hn1 hn2 hSnell

end OperatorFirst.HypersurfaceSquareLineage
