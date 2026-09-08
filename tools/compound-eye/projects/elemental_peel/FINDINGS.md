# Elemental peel: spacing, channels, and the surface

Research and computations completed 8 September 2026. Au, Ag, Cu, Pt.

The strongest result is a concrete connection between the recovered hypersurface electronic model, the color work, and electrical transport: changing orbital orientation can change both optical transition strength and conductance while leaving the energy spacing fixed. Actual elemental data add a recognizable shell-removal pattern and different visible responses. Together they support an elemental programme that follows **spacing, coupling, occupation, and the boundary at every step**. They do not yet constitute an observed atom-by-atom cascade or a universal removal law.

## 1. An elemental spacing pattern, with its actual meaning

We transcribed the first twelve successive ionization energies from NIST ASD, retaining its uncertainties and estimate brackets. Nuclear charge remains fixed through each sequence: ionizing gold does not turn it into platinum. The following large later increments occur within that twelve-removal window:

| Element | Neutral outer configuration | First ionization, eV | Later jump in the tested window | Increment, eV |
|---|---|---:|---|---:|
| Cu | 3d¹⁰4s¹ | 7.726380 | removal 11 → 12 | 101.67 |
| Ag | 4d¹⁰5s¹ | 7.576234 | removal 11 → 12 | 83.46 |
| Au | 5d¹⁰6s¹ | 9.225554 | removal 11 → 12 | 79.8 |
| Pt | 5d⁹6s¹ | 8.95883 | removal 10 → 11 | 75.5 |

Thus the later shell jump occurs **after eleven removals in Cu/Ag/Au and after ten in Pt**, consistent with these outer-electron counts. This is a family resemblance, not an evenly spaced universal ladder. Highly ionized states reorganize; several high-charge thresholds are estimates. The conservative sum-of-uncertainties bounds on these four increments are respectively 1.15, 2.52, 2.4, and 2.0 eV. These bounds preserve the reported input uncertainty convention; they are not newly estimated confidence intervals. [NIST ASD](https://physics.nist.gov/asd)

These isolated-ion thresholds are distinct from occupied-to-empty band transitions and from the energies of states carrying current near the Fermi level. Their numerical identification would be a false bridge. Exact source URLs, flags and values are in `data/nist_first12.json`; the automated CSV endpoint returned HTTP 403, so this input is an explicitly recorded transcription of the accessible NIST tables.

## 2. The actual elemental color comparison

We replayed Johnson–Christy's measured optical constants for Au, Ag and Cu through Maxwell reflection, and used Rakić's published optical fit for Pt. The table is calculated normal-incidence reflectance of a semi-infinite surface, rather than new reflectance measurements:

| Element / optical input | R at 450 nm | R at 550 nm | R at 650 nm |
|---|---:|---:|---:|
| Au / measured constants | 0.408 | 0.792 | 0.957 |
| Ag / measured constants | 0.980 | 0.983 | 0.990 |
| Cu / measured constants | 0.538 | 0.624 | 0.935 |
| Pt / fitted constants | 0.588 | 0.641 | 0.678 |

Gold and copper strongly change their visible reflection across this range; silver stays highly reflective. Platinum's fitted response is lower and less strongly tilted. The measured constants come from finite metal films; treating them as fixed bulk inputs during further thinning is a stated continuum approximation. [Johnson & Christy (1972)](https://doi.org/10.1103/PhysRevB.6.4370), [Rakić et al. (1998)](https://doi.org/10.1364/AO.37.005271)

The live viewer recomputes 10–200 nm films on substrates with refractive index 1–2, including both interfaces, reflection phase, transmission, absorption and D65 color. It can vary interband weight and scattering width in the fitted model. Color uses official CIE tables with both published MD5 checks matched. A swatch describes reflected daylight under a specified observer; it is not a photograph of a metal object. [CIE observer](https://cie.co.at/datatable/cie-1931-colour-matching-functions-2-degree-observer), [CIE daylight](https://cie.co.at/datatable/cie-standard-illuminant-d65)

Changing thickness or substrate changes the computed color even when the material optical constants stay fixed. This is exactly where the hypersurface work matters: the observable depends on electronic response **and on the boundary problem**. At 10 nm, continuity, roughness and unchanged material constants are particularly consequential assumptions. Atomic layers require new material data, not continuation of this slider to zero thickness.

We also compared Rakić fits against the measured constants: visible reflectance RMS differences are 0.043 for Au, 0.048 for Ag and 0.063 for Cu. These are model/source discrepancies, not measurement error bars. Optical-fit extrapolations to zero frequency are labelled as such and are **not supplied as measured DC conductivities or a reliable bulk conductivity ranking**.

## 3. The recovered hypersurface/color bridge now carries current too

The original color-model script and the recovered hypersurface verifier ran successfully; the latter passed all **328 named checks**. Those source packages are preserved with this study.

We attached explicit electrical contacts to the hypersurface two-level electronic-sheet Hamiltonian. Across 65 orientations, its levels stayed at −1 and +1 eV, its optical strength varied from zero to one, and conductance varied from zero to 0.147929 conductance quanta. The projector metric stayed at 1/4. Two inherited UPG eyes independently followed the same Hamiltonian's projector sensitivity and feedback coupling at seventeen orientations.

This supplies a common object for the different observations; it does not identify this two-level model with an ab initio description of any of the four metals. The recovered color script is likewise an ideal band-model control. Its literature connection is the optical role of quantum geometry at a quadratic band touching, not an elemental conductivity fit. [Oh et al., 2026 journal article; preprint revised 29 August 2026](https://arxiv.org/abs/2503.18372)

## 4. What a conductive peel can do

Removing a fixed nonnegative channel contribution obeys the earlier monotonicity result. Changing a coupled orbital generally changes the remaining scattering problem as well. A side-coupled orbital supplies a checked counterexample to treating these operations as equivalent: reducing its coupling from 0.8 to zero raises conductance from **0.180144 to 1 G₀** by releasing destructive interference. Exact elimination, with its energy-dependent self-energy retained, agrees with the full model; bare deletion loses that information.

Conductance alone also cannot count open channels. One perfectly open channel and two half-open channels both give G₀, but their shot-noise factors differ. Even conductance plus noise need not determine three channels: two different triples tested here both give 1.5 G₀ and F = 0.38. The instrument records these ambiguities explicitly.

Atomic-contact experiments already provide a relevant element comparison: published Au/Ag results show channels opening approximately one by one, while Pt exhibits a more complex set of partially transmitting channels. This is evidence for an orbital-sensitive experiment, rather than an inference from the ionization ladder alone. We read the published analysis; we did not obtain and replay its raw shot-noise records. [Vardimon, Klionsky & Tal](https://arxiv.org/abs/1308.3425)

## 5. Latest research and what it changes

* **2026 gold contacts:** simultaneous conductance and thermopower measurements show that a conductance plateau can conceal changing energy-sensitive transport. The authors find that an electronic-only explanation of the temperature dependence conflicts with measured current–voltage behaviour and argue for a phonon contribution. For the next experiment, track temperature, thermopower and I–V alongside conductance. [Möller et al., June 2026 preprint](https://arxiv.org/html/2606.12734v1)
* **January 2026 goldene calculations:** DFT plus transport modelling directly tests strain and structural defects in a one-layer gold structure. This is the right kind of material-specific bridge for a physical peel. The article's abstract and detailed vacancy discussion give differing percentage reductions, so this report does not adopt one universal robustness number. It is a theoretical calculation, not a measured cascade. [Berdiyorov & Aissa](https://www.nature.com/articles/s41699-025-00657-y)
* **2 September 2026 Au–Ag–Cu monolayer preprint:** an enumeration of ordered alloys finds that atomic arrangement matters at fixed composition. This makes geometry an essential control when comparing conductance during removal. It does not establish an experimental elemental law. [Pereira Junior](https://arxiv.org/abs/2609.02709)
* **Physical material removal exists:** goldene was synthesized through a chemical exfoliation route. This provides a real one-layer material target, but exfoliation, isolated-atom ionization, and an artificial oscillator reduction remain different interventions. [Kashiwaya et al.](https://www.nature.com/articles/s44160-024-00518-4)

No newly retrieved raw atomic-contact trajectory, goldene transport dataset, or four-element matched experiment was fitted in this pass. Latest literature informs the test design; bundled optical tables and NIST values supply the actual element-specific replay.

## 6. What is ready, and the next decisive test

Seven new immutable eyes bring the registry to **198 versions**, preserving the previous 191. The new main and extension runs contain **714 requests, 1,253 eye evaluations, four intended domain refusals, and 846 assertions**. Ten distinct registered methods are used, including the inherited positive-channel, redistribution and projector-sensitivity eyes. These counts describe checks and evaluations, not independent experiments or new theorems. The recovered 328-check hypersurface run is separate. No new Lean compilation is claimed.

The next decisive dataset is an element-labelled, temperature-controlled sequence with a known physical intervention and measured geometry. For an atomic contact, use elongation/displacement, G, low-bias shot noise, full I–V and thermopower. For film thinning, use calibrated thickness, structure/roughness, DC sheet resistance and spectroscopic reflection/transmission or ellipsometry. Relate both through a validated electronic Hamiltonian before identifying their channels. Track forward and reverse paths: any hysteresis must survive heating, geometry and calibration controls before it is called memory.

The elemental hypothesis is now sharper: **changes in level/band spacing, orbital coupling and boundary loading should predict changes in several readouts of the same evolving material.** The useful discovery test is whether these coordinated observations expose a transition that one spectrum, one color, or one conductance trace misses.
