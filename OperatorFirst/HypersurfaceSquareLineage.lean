import Mathlib

/-!
# OperatorFirst.HypersurfaceSquareLineage

Formal reconstruction of the recovered chain:
spacing -> inverse-gap-square response -> metric coefficient -> Snell/Clairaut
-> squared refraction -> fold/Gram squaring -> three-body fourth-power rigidity
-> four-body normal suppression -> fixed-spacing angle-dependent response.

The physical identifications are not axioms here; model-specific inputs appear
only as explicit hypotheses.
-/

namespace OperatorFirst.HypersurfaceSquareLineage

/-! ## I. Spacing and inverse-gap-square response -/

theorem response_square_is_gap_square (a Δ : ℝ) (hΔ : Δ ≠ 0) :
    (a / Δ) ^ 2 = a ^ 2 / Δ ^ 2 := by
  field_simp [hΔ]

theorem gap_square_weight_nonneg (a Δ : ℝ) :
    0 ≤ a ^ 2 / Δ ^ 2 := by
  positivity

theorem inverse_gap_square_antitone
    (Δ₁ Δ₂ : ℝ) (h1 : 0 < Δ₁) (h12 : Δ₁ ≤ Δ₂) :
    1 / Δ₂ ^ 2 ≤ 1 / Δ₁ ^ 2 := by
  have hs : Δ₁ ^ 2 ≤ Δ₂ ^ 2 := by nlinarith
  exact one_div_le_one_div_of_le (sq_pos_of_pos h1) hs

theorem inverse_gap_square_scaling
    (Δ c : ℝ) (hΔ : Δ ≠ 0) (hc : c ≠ 0) :
    1 / (c * Δ) ^ 2 = (1 / c ^ 2) * (1 / Δ ^ 2) := by
  field_simp [hΔ, hc]

/-! ## II. Snell / Clairaut -/

theorem snell_implies_squared_snell
    (n₁ n₂ θ₁ θ₂ : ℝ)
    (h : n₁ * Real.sin θ₁ = n₂ * Real.sin θ₂) :
    n₁ ^ 2 * Real.sin θ₁ ^ 2 = n₂ ^ 2 * Real.sin θ₂ ^ 2 := by
  have hs := congrArg (fun x : ℝ => x ^ 2) h
  simpa [mul_pow] using hs

theorem metric_snell_squared
    (n₁ n₂ g₁ g₂ θ₁ θ₂ : ℝ)
    (hg1 : g₁ = n₁ ^ 2) (hg2 : g₂ = n₂ ^ 2)
    (hSnell : n₁ * Real.sin θ₁ = n₂ * Real.sin θ₂) :
    g₁ * Real.sin θ₁ ^ 2 = g₂ * Real.sin θ₂ ^ 2 := by
  subst g₁
  subst g₂
  exact snell_implies_squared_snell n₁ n₂ θ₁ θ₂ hSnell

theorem squared_snell_from_metric_index
    (n₁ n₂ g₁ g₂ s₁ s₂ : ℝ)
    (hn1 : 0 ≤ n₁) (hn2 : 0 ≤ n₂)
    (hg1 : g₁ = n₁ ^ 2) (hg2 : g₂ = n₂ ^ 2)
    (hs1 : 0 ≤ s₁) (hs2 : 0 ≤ s₂)
    (h : g₁ * s₁ ^ 2 = g₂ * s₂ ^ 2) :
    n₁ * s₁ = n₂ * s₂ := by
  subst g₁
  subst g₂
  have hsq : (n₁ * s₁) ^ 2 = (n₂ * s₂) ^ 2 := by
    simpa [mul_pow] using h
  have hleft : 0 ≤ n₁ * s₁ := mul_nonneg hn1 hs1
  have hright : 0 ≤ n₂ * s₂ := mul_nonneg hn2 hs2
  nlinarith

/-! ## III. Principal-angle reading -/

noncomputable def rankOneChordalSq (θ : ℝ) : ℝ := 2 * Real.sin θ ^ 2

theorem rankOneChordalSq_nonneg (θ : ℝ) :
    0 ≤ rankOneChordalSq θ := by
  unfold rankOneChordalSq
  positivity

theorem sqrt_sin_sq (θ : ℝ) :
    Real.sqrt (Real.sin θ ^ 2) = |Real.sin θ| := by
  simpa using Real.sqrt_sq_eq_abs (Real.sin θ)

/-! ## IV. Fold -> Gram square -> fourth-power rigidity -/

def gramSoft (s : ℝ) : ℝ := s ^ 2

noncomputable def rigidityFromGram (lam : ℝ) : ℝ := 1 / lam ^ 2

theorem fold_gram_rigidity_fourth_power (s : ℝ) (hs : s ≠ 0) :
    rigidityFromGram (gramSoft s) = 1 / s ^ 4 := by
  unfold rigidityFromGram gramSoft
  field_simp [hs]

theorem three_body_sec_four (θ : ℝ) (hc : Real.cos θ ≠ 0) :
    rigidityFromGram (Real.cos θ ^ 2) = 1 / Real.cos θ ^ 4 := by
  unfold rigidityFromGram
  field_simp [hc]

theorem simple_zero_gives_inverse_fourth
    (c ε : ℝ) (hc : c ≠ 0) (hε : ε ≠ 0) :
    rigidityFromGram ((c * ε) ^ 2) = (1 / c ^ 4) * (1 / ε ^ 4) := by
  unfold rigidityFromGram
  field_simp [hc, hε]

/-! ## V. Three-body refraction -/

theorem three_body_refraction_is_squared_snell
    (R₁ R₂ θ₁ θ₂ : ℝ)
    (hSnell : Real.sqrt R₁ * Real.sin θ₁ = Real.sqrt R₂ * Real.sin θ₂)
    (hR1 : 0 ≤ R₁) (hR2 : 0 ≤ R₂) :
    R₁ * Real.sin θ₁ ^ 2 = R₂ * Real.sin θ₂ ^ 2 := by
  have hs := congrArg (fun x : ℝ => x ^ 2) hSnell
  rw [mul_pow, mul_pow, Real.sq_sqrt hR1, Real.sq_sqrt hR2] at hs
  exact hs

/-! ## VI. Four-body hypersurface block -/

def fourBodyWallMap (A shear lam parallel normal : ℝ) : ℝ × ℝ :=
  (A * parallel + shear * normal, (2 * lam) * normal)

theorem four_body_parallel_stays_tangent (A shear lam parallel : ℝ) :
    (fourBodyWallMap A shear lam parallel 0).2 = 0 := by
  simp [fourBodyWallMap]

theorem four_body_normal_squeeze (A shear lam parallel normal : ℝ) :
    (fourBodyWallMap A shear lam parallel normal).2 = 2 * lam * normal := by
  simp [fourBodyWallMap, mul_assoc]

theorem four_body_zero_squeeze_kills_normal (A shear parallel normal : ℝ) :
    (fourBodyWallMap A shear 0 parallel normal).2 = 0 := by
  simp [fourBodyWallMap]

/-! ## VII. Fixed spacing, changing orientation -/

def twoLevelGapSq (Δ : ℝ) : ℝ := Δ ^ 2

noncomputable def orientationWeight (θ : ℝ) : ℝ := Real.sin θ ^ 2

theorem orientationWeight_nonneg (θ : ℝ) :
    0 ≤ orientationWeight θ := by
  unfold orientationWeight
  positivity

theorem fixed_gap_does_not_fix_orientation_weight :
    orientationWeight 0 = 0 ∧ orientationWeight (Real.pi / 2) = 1 := by
  constructor <;> simp [orientationWeight]

noncomputable def conductanceFactor (Δ γ θ : ℝ) : ℝ :=
  (γ ^ 2 * (Δ / 2) ^ 2 * Real.sin θ ^ 2) /
    (((Δ / 2) ^ 2 + γ ^ 2 / 4) ^ 2)

theorem conductance_zero_at_zero_angle (Δ γ : ℝ) :
    conductanceFactor Δ γ 0 = 0 := by
  simp [conductanceFactor]

theorem conductance_numerator_factor (Δ γ θ : ℝ) :
    γ ^ 2 * (Δ / 2) ^ 2 * Real.sin θ ^ 2 =
      (γ ^ 2 * (Δ / 2) ^ 2) * orientationWeight θ := by
  simp [orientationWeight]

/-! ## VIII. Keep spacing notions distinct -/

inductive SpacingKind
  | ionization | bandGap | principalAngle | spatial | channel
deriving DecidableEq, Repr

structure SpacingMeasurement where
  kind : SpacingKind
  value : ℝ

theorem different_kind_measurements_ne (x : ℝ) :
    ({ kind := SpacingKind.ionization, value := x } : SpacingMeasurement) ≠
    ({ kind := SpacingKind.bandGap, value := x } : SpacingMeasurement) := by
  intro h
  have hk := congrArg SpacingMeasurement.kind h
  cases hk

/-! ## IX. Master conditional lineage -/

theorem spacing_to_hypersurface_refraction
    (a₁ a₂ Δ₁ Δ₂ q₁ q₂ g₁ g₂ n₁ n₂ θ₁ θ₂ : ℝ)
    (hΔ1 : Δ₁ ≠ 0) (hΔ2 : Δ₂ ≠ 0)
    (hq1 : q₁ = a₁ / Δ₁) (hq2 : q₂ = a₂ / Δ₂)
    (hg1 : g₁ = q₁ ^ 2) (hg2 : g₂ = q₂ ^ 2)
    (hn1 : g₁ = n₁ ^ 2) (hn2 : g₂ = n₂ ^ 2)
    (hSnell : n₁ * Real.sin θ₁ = n₂ * Real.sin θ₂) :
    g₁ = a₁ ^ 2 / Δ₁ ^ 2 ∧
    g₂ = a₂ ^ 2 / Δ₂ ^ 2 ∧
    g₁ * Real.sin θ₁ ^ 2 = g₂ * Real.sin θ₂ ^ 2 := by
  have hgap1 : g₁ = a₁ ^ 2 / Δ₁ ^ 2 := by
    calc
      g₁ = q₁ ^ 2 := hg1
      _ = (a₁ / Δ₁) ^ 2 := by rw [hq1]
      _ = a₁ ^ 2 / Δ₁ ^ 2 := response_square_is_gap_square a₁ Δ₁ hΔ1
  have hgap2 : g₂ = a₂ ^ 2 / Δ₂ ^ 2 := by
    calc
      g₂ = q₂ ^ 2 := hg2
      _ = (a₂ / Δ₂) ^ 2 := by rw [hq2]
      _ = a₂ ^ 2 / Δ₂ ^ 2 := response_square_is_gap_square a₂ Δ₂ hΔ2
  exact ⟨hgap1, hgap2, metric_snell_squared n₁ n₂ g₁ g₂ θ₁ θ₂ hn1 hn2 hSnell⟩

end OperatorFirst.HypersurfaceSquareLineage

#print axioms OperatorFirst.HypersurfaceSquareLineage.response_square_is_gap_square
#print axioms OperatorFirst.HypersurfaceSquareLineage.gap_square_weight_nonneg
#print axioms OperatorFirst.HypersurfaceSquareLineage.inverse_gap_square_antitone
#print axioms OperatorFirst.HypersurfaceSquareLineage.inverse_gap_square_scaling
#print axioms OperatorFirst.HypersurfaceSquareLineage.snell_implies_squared_snell
#print axioms OperatorFirst.HypersurfaceSquareLineage.metric_snell_squared
#print axioms OperatorFirst.HypersurfaceSquareLineage.squared_snell_from_metric_index
#print axioms OperatorFirst.HypersurfaceSquareLineage.rankOneChordalSq_nonneg
#print axioms OperatorFirst.HypersurfaceSquareLineage.sqrt_sin_sq
#print axioms OperatorFirst.HypersurfaceSquareLineage.fold_gram_rigidity_fourth_power
#print axioms OperatorFirst.HypersurfaceSquareLineage.three_body_sec_four
#print axioms OperatorFirst.HypersurfaceSquareLineage.simple_zero_gives_inverse_fourth
#print axioms OperatorFirst.HypersurfaceSquareLineage.three_body_refraction_is_squared_snell
#print axioms OperatorFirst.HypersurfaceSquareLineage.four_body_parallel_stays_tangent
#print axioms OperatorFirst.HypersurfaceSquareLineage.four_body_normal_squeeze
#print axioms OperatorFirst.HypersurfaceSquareLineage.four_body_zero_squeeze_kills_normal
#print axioms OperatorFirst.HypersurfaceSquareLineage.orientationWeight_nonneg
#print axioms OperatorFirst.HypersurfaceSquareLineage.fixed_gap_does_not_fix_orientation_weight
#print axioms OperatorFirst.HypersurfaceSquareLineage.conductance_zero_at_zero_angle
#print axioms OperatorFirst.HypersurfaceSquareLineage.conductance_numerator_factor
#print axioms OperatorFirst.HypersurfaceSquareLineage.different_kind_measurements_ne
#print axioms OperatorFirst.HypersurfaceSquareLineage.spacing_to_hypersurface_refraction
