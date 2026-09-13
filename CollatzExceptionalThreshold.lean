import CollatzNoFixedWindow

/-!
# Exact exceptional-cylinder resolution threshold

This file formalizes the counting threshold behind the moving-anchor warning.
At a residue resolution with `M` exact cylinders, one bad cylinder already has
relative mass at least `1 / M`.  Therefore an aggregate exceptional fraction
strictly below `1 / M` forces the exceptional cylinder count to be zero.

For the odd-to-odd Collatz realization layer the exact depth resolution is
`M = 2^(S+1)`, where `S` is the cumulative valuation exponent.  Thus a bound
of the form `epsilon < 2^(-(S+1))` is strong enough to exclude every bad
cylinder at that fixed depth.  Mere `epsilon -> 0` is not such a pointwise
statement unless it outruns this moving arithmetic resolution.

This is a finite counting interface only.  It does not prove a Tao-style
exceptional estimate with this strength, does not prove moving-anchor escape,
and does not prove the Collatz conjecture.
-/

namespace CollatzExceptionalThreshold

/-- If the bad-cylinder fraction is strictly below the mass of one cylinder,
then there are no bad cylinders. -/
theorem exceptional_count_zero_of_fraction_lt_singleton
    (M bad : ℕ) (hM : 0 < M)
    (hsmall : (bad : ℚ) / (M : ℚ) < (1 : ℚ) / (M : ℚ)) :
    bad = 0 := by
  have hMq : (0 : ℚ) < (M : ℚ) := by
    exact_mod_cast hM
  have hltq : (bad : ℚ) < (1 : ℚ) :=
    (div_lt_div_iff_of_pos_right hMq).mp hsmall
  have hlt : bad < 1 := by
    exact_mod_cast hltq
  omega

/-- Conversely, one or more bad cylinders force exceptional fraction at least
the mass of one cylinder. -/
theorem nonzero_exceptional_count_forces_singleton_fraction_le
    (M bad : ℕ) (hM : 0 < M) (hbad : bad ≠ 0) :
    (1 : ℚ) / (M : ℚ) ≤ (bad : ℚ) / (M : ℚ) := by
  have hMq : (0 : ℚ) < (M : ℚ) := by
    exact_mod_cast hM
  have hbad1 : 1 ≤ bad := Nat.one_le_iff_ne_zero.mpr hbad
  have hcast : (1 : ℚ) ≤ (bad : ℚ) := by
    exact_mod_cast hbad1
  exact (div_le_div_iff_of_pos_right hMq).mpr hcast

/-- Exact number of binary phase cylinders at cumulative valuation depth `S`
for the corrected odd-to-odd modulus `2^(S+1)`. -/
def phaseResolution (S : ℕ) : ℕ := 2 ^ (S + 1)

/-- The corrected phase resolution is always positive. -/
theorem phaseResolution_pos (S : ℕ) : 0 < phaseResolution S := by
  dsimp [phaseResolution]
  positivity

/-- **Moving-resolution threshold.**  At the corrected Collatz phase modulus
`2^(S+1)`, an exceptional fraction strictly below one cylinder's mass forces
zero exceptional cylinders at that depth. -/
theorem phase_exceptional_fraction_below_one_cylinder_forces_zero
    (S bad : ℕ)
    (hsmall :
      (bad : ℚ) / (phaseResolution S : ℚ) <
        (1 : ℚ) / (phaseResolution S : ℚ)) :
    bad = 0 := by
  exact exceptional_count_zero_of_fraction_lt_singleton
    (phaseResolution S) bad (phaseResolution_pos S) hsmall

/-- Equivalent lower-bound direction at the moving Collatz resolution: if a
bad phase cylinder exists, aggregate exceptional mass cannot be smaller than
one exact cylinder. -/
theorem nonzero_phase_exceptional_count_forces_resolution_floor
    (S bad : ℕ) (hbad : bad ≠ 0) :
    (1 : ℚ) / (phaseResolution S : ℚ) ≤
      (bad : ℚ) / (phaseResolution S : ℚ) := by
  exact nonzero_exceptional_count_forces_singleton_fraction_le
    (phaseResolution S) bad (phaseResolution_pos S) hbad

end CollatzExceptionalThreshold

#print axioms CollatzExceptionalThreshold.exceptional_count_zero_of_fraction_lt_singleton
#print axioms CollatzExceptionalThreshold.nonzero_exceptional_count_forces_singleton_fraction_le
#print axioms CollatzExceptionalThreshold.phaseResolution_pos
#print axioms CollatzExceptionalThreshold.phase_exceptional_fraction_below_one_cylinder_forces_zero
#print axioms CollatzExceptionalThreshold.nonzero_phase_exceptional_count_forces_resolution_floor
