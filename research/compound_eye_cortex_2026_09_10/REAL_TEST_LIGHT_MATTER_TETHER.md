# REAL TEST — Light/matter tether, delay and directional control

**Test ID:** `LIGHT-MATTER-TETHER-01`  
**Date:** 10 September 2026  
**Status:** PASS for the finite/symbolic model; physical identification remains scoped.

## Question

Can the older two-rail idea be sharpened so that the faster light rail is dynamically loaded by a slower matter rail, with the rate mismatch producing the delay/memory that controls the optical motion? Does this connect cleanly to the Electron–Photon Loop and the Kakeya/directional-capacity work?

## Source roles

The current source corpus already contains three separate ingredients:

1. **Light Keeps the Ledger**: two information registers; cross-boundary projector identity; optical response shares transition data with projector geometry; assignment of the two registers to light/matter is a hypothesis, not a finite-algebra theorem.
2. **Elemental Peeling**: eliminating the electronic response produces an explicit causal velocity-memory kernel, with `zeta(0)=2 Delta g_qq` in the declared model.
3. **Electron–Photon Loop**: explicitly proposes two coupled reservoirs, optical and electronic, and repeated photon -> electronic excitation -> photon cycling.
4. **Kakeya / Price of a Direction**: simultaneous directional distinctions consume independent channel capacity; this is used here only as a source of the control-capacity question, not as a theorem about light-matter hybridization.

## Minimal coherent model

Use one fast optical mode and one slower neutral matter excitation:

```text
H(k) = [[omega_f(k), g],
        [g,          omega_s(k)]]
```

with constant real coupling `g`.  Write

```text
Delta = omega_f - omega_s
Omega = sqrt(Delta^2 + 4 g^2)
```

and bare rates

```text
v_f = d omega_f/dk,
v_s = d omega_s/dk.
```

The two eigenvalues are

```text
lambda_+/- = (omega_f+omega_s)/2 +/- Omega/2.
```

Differentiating gives the exact identity

```text
v_+/- = w_f,+/- v_f + w_s,+/- v_s,
```

where the weights are the photonic/matter components of the eigenprojector,

```text
w_f,+ = (1 + Delta/Omega)/2,
w_f,- = (1 - Delta/Omega)/2,
w_s = 1-w_f.
```

Therefore

```text
v_f - v_+/- = w_s,+/- (v_f-v_s).
```

### First result

If `v_f > v_s`, adding matter fraction slows the hybrid branch relative to the bare fast rail.  In the Hermitian constant-coupling model the hybrid rate stays between the two bare rates.

At exact resonance (`Delta=0`), both branches have

```text
v_+ = v_- = (v_f+v_s)/2.
```

Concrete controls:

- `v_f=1`, `v_s=0.2` -> resonance rate `0.6`;
- `v_f=1`, flat matter `v_s=0` -> resonance rate `0.5`.

The most important negative control is exact:

```text
v_f = v_s  =>  v_+ = v_- = v_f
```

for any nonzero `g`.  Coupling by itself does **not** produce a slowdown.  The different bare rates are load-bearing.

## Projector eye

For either rank-one eigenprojector, if `C` is the photonic diagonal weight and `X` the light/matter cross block,

```text
C(1-C) = |X|^2 = g^2/(Delta^2+4g^2).
```

This is the two-mode version of the older projector identity `C-C^2 = X X^dagger`.  At resonance the mixing is maximal: `C=1/2`, `|X|^2=1/4`.

Thus the same projector that records how much matter is in the hybrid mode also records how much the fast bare rate is loaded:

```text
slowdown = matter weight * bare-rate difference.
```

## Memory / self-energy eye

For a general block model

```text
H = [[A, V],
     [V^dagger, D]],
```

eliminating the matter sector gives the fast sector a self-energy

```text
Sigma(z) = V (D-z I)^(-1) V^dagger
```

and a time-domain memory object

```text
K(t) = V exp(-i D t) V^dagger.
```

For `Im z>0`,

```text
Sigma(z) = i integral_0^infinity exp(i z t) K(t) dt.
```

So the frequency-domain loading and the delayed time-domain feedback are two transforms of the same coupling `V,D`.  This is a rigorous candidate for the old phrase “the gap between the rails is the supply”: not an undefined force, but cross-rail coupling plus the slower sector's spectral labels.

## Kakeya / capacity eye

The coupling does not grab every photonic direction automatically.

If a fast-sector vector `x` obeys

```text
V^dagger x = 0,
```

then

```text
Sigma(z) x = 0,
K(t) x = 0
```

for every admissible `z,t`.  It has no matter tether in this model.

A finite matter sector with `r` independent channels can load at most `rank(V)<=r` independent fast combinations.  In the executed control, eight photonic channels coupled to three generic matter channels left an exact five-dimensional blind subspace; memory and self-energy on that subspace were below `8e-15` numerical residual.

This gives a clean bridge to the directional-capacity language:

> to control `mu` independent optical directions through this mechanism, the matter coupling must have rank at least `mu` on those directions.

This is linear algebra in the present model.  It is not a transfer of the Arithmetic Kakeya conjecture into optics.

## The Electron–Photon Loop splits into two mechanisms

The older loop should now distinguish two physically different regimes.

### A. Coherent hybrid / “kite on a reel”

Light and a neutral electronic excitation form one propagating hybrid state.  The photonic fraction carries motion; the matter fraction stores part of the excitation and lowers the group rate.  Coupling/detuning controls the mixing.

This is close to established polariton and dark-state-polariton physics.  In EIT, the light/matter mixing angle can be changed so that the group velocity is reduced and the optical state is reversibly mapped into a long-lived collective matter state.

### B. Absorb / dwell / re-emit recycling

A photon is absorbed, the energy dwells in matter for a finite time, and a photon is later re-emitted.  This is not the same object as a coherent group-velocity reduction.  If a path of length `L` contains `N` material dwell events of mean duration `tau`, then schematically

```text
v_eff/c = L/(L + c N tau) < 1.
```

The delay is real, but it is residence time rather than a single hybrid dispersion relation.

## Car brakes or kite?

**Kite/reel is the better analogy, with a correction.**  The string is not a literal electron behind a photon.  It is the light-matter coupling, and the reel is the slower material degree of freedom / coherence.

The “brake” analogy corresponds to adding damping `Gamma` to the matter sector.  Then the coherent memory is multiplied by

```text
exp(-Gamma t/2).
```

More damping therefore shortens coherent memory and spends energy.  It can attenuate and rephase a field, but it is not the clean origin of the sub-fast hybrid rate.  For useful reversible control, changing coupling, detuning, or using a long-lived matter coherence is a better knob than frictional loss.

## Executed controls

`light_matter_tether_check.py` ran 13 symbolic/finite checks.

- 20,000 random Hermitian hybrid controls;
- zero velocity-bound violations;
- maximum weighted-velocity identity residual `3.33e-16`;
- 8 fast channels / 3 matter channels -> 5-dimensional coupling blind subspace;
- maximum memory action on that blind subspace `6.00e-15`;
- maximum self-energy action on that blind subspace `7.92e-15`;
- memory rank never exceeded 3.

See `light_matter_tether_check_results.json`.

## External reality check

This model is not inventing the existence of slow light-matter hybrids.  Established dark-state polariton work identifies coupled light/matter excitations whose group velocity is set by their mixing and can be reduced to zero under EIT control (Fleischhauer & Lukin, PRL 84, 5094 (2000); PRA 65, 022314 (2002)).  Recent polariton-transport work likewise relates group velocity to photonic/matter Hopfield fractions and studies further renormalization of that velocity.

What is specific to this programme is the attempt to place the same phenomenon inside one operator-first ledger:

```text
fast rail -> coupling V -> slower matter rail
          -> projector mixing
          -> self-energy / memory
          -> finite directional-control rank
```

## Current verdict

### Established within the declared model

- a slower matter component slows a coherent hybrid mode in proportion to its matter weight;
- equal bare rates kill the effect exactly;
- the cross-rail coupling generates both self-energy and time memory;
- coupling rank limits how many independent photonic directions can be loaded;
- damping is a lossy memory-shortener, not the fundamental slowdown mechanism.

### Physical hypothesis worth carrying forward

The strongest version of the old two-rail idea is now:

> **Light supplies the fast propagation component; a slower neutral electronic/material sector supplies stored weight and delayed response; their coupling determines how much of a propagating mode is free to run and how much is temporarily held.**

This is a good finite operator model for light in matter.  It is **not** yet a statement about a free photon being tethered by a single electron in vacuum.

### Next discriminator

Use one spatially extended model with a real photonic dispersion and a calibrated electronic/excitonic band, then measure from the same Hamiltonian:

1. hybrid group velocity;
2. photonic/matter projector weights;
3. self-energy and time memory;
4. optical susceptibility / phase delay;
5. directional coupling rank;
6. loss when damping is turned on.

The key falsifier is simple: if the measured hybrid slowdown does not track the matter projector weight and bare-rate mismatch in the constant-coupling regime, this minimal tether model is wrong for that system.
