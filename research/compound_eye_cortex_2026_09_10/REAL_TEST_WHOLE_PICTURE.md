# REAL TEST — whole-picture light/matter causal mixer

**Test ID:** `LIGHT-MATTER-WHOLE-PICTURE-01`  
**Date:** 10 September 2026  
**Status:** PASS for the declared finite/symbolic controls. Physical identification remains scoped.

## Question

What happens if the currently connected Light Ledger, Elemental Peeling, Electron–Photon Loop, directional/Kakeya-capacity and two-rail Rice–Mele structures are placed in one causal view rather than inspected separately? Which quantities actually control which others, and which scalar readouts fail to identify their cause?

## Whole-picture spine

The declared model keeps these links separate:

```text
fast optical rail --+--> light/matter projector mixing --> hybrid group rate
                    |
                    +--> self-energy <--> time memory --> response / phase

matter coupling rank + directional demand --> loaded and blind optical combinations

photon absorption --> matter dwell time --> re-emission --> residence-time delay

Rice-Mele gap ratio --> max lattice group rate + correlation length + boundary log-odds
```

These are model-level dependencies, not a claim that every arrow is an experimentally established electron/photon mechanism.

## Fresh scaled controls

The new runner executed 200,000 random Hermitian two-mode hybrid cases and independent rank/ambiguity controls.

- hybrid velocity outside the two bare velocities: **0 violations**;
- exact speed/projector identity maximum numerical residual: **1.14e-12**;
- projector mixing bound `C(1-C) <= 1/4`: **0 violations**;
- when `v_fast > v_slow`, increasing coupling on the instantaneous photon-like branch failed to increase slowdown in **0** tested controls;
- increasing absolute detuning failed to return that branch toward the fast bare rate in **0** tested controls;
- equal-bare-rate negative control: maximum velocity residual **machine precision**;
- 300 generic fast/matter rank controls: **0 rank-deficit violations**;
- one scalar target speed `v=0.6` was reproduced by three inequivalent mechanisms with maximum residual **1.11e-16**.

The complete standalone replacement checker is `light_matter_whole_picture_check.py`.

## New exact cross-readout identity

For either constant-coupling two-mode Hermitian branch,

```text
v_h = C v_f + (1-C) v_s
```

where `C` is its fast/light projector weight. Therefore, whenever `v_f != v_s`,

```text
C(1-C)
 = ((v_f-v_h)(v_h-v_s)) / (v_f-v_s)^2.
```

Since the rank-one projector also obeys

```text
C(1-C) = |X|^2 = g^2/(Delta^2+4g^2),
```

the normalized location of the hybrid group rate between the two bare rates determines the projector cross-block magnitude in this minimal model. The identity becomes non-informative at equal bare rates, exactly where coupling can remain nonzero while the velocity readout loses all information about the mixing.

That equal-rate case is a useful blind-spot control, not a defect of the algebra.

## Strongest pattern found: one slowdown, different causes

A scalar speed below a chosen fast reference does not identify its mechanism.

At normalized target speed `0.6`, three distinct model states reproduce the same scalar value:

1. **Coherent hybridization:** `v_f=1`, exact resonance, `v_s=0.2`, giving a 50:50 light/matter hybrid with speed `0.6`.
2. **Absorb/dwell/re-emit:** bare propagation speed `1` plus total residence-time budget `N tau = 2/3`, giving effective transit rate `1/(1+2/3)=0.6`.
3. **Gapped Rice-Mele analogue:** `rho=e/M=(1-0.6^2)/(1+0.6^2)`, giving normalized maximal lattice rate `sqrt((1-rho)/(1+rho))=0.6`.

They agree on the scalar speed and disagree on their internal records: projector matter weight, coherent memory/self-energy, dwell lifetime, correlation length and boundary log-odds.

This is the whole-picture version of the Cortex sufficiency question: **what target-relevant information did the first observation erase?**

## Directional-control rank

If `V^dagger x = 0`, the same optical combination is invisible to both

```text
Sigma(z)=V(D-zI)^(-1)V^dagger
```

and

```text
K(t)=V exp(-iDt)V^dagger.
```

Thus a rank-`r` matter coupling can load at most `r` independent fast combinations. This supplies the finite linear-algebra bridge to the older directional-capacity language. It does **not** transfer the Arithmetic Kakeya conjecture into optics.

## Brake versus reel

The present model separates coherent loading from damping.

- changing coupling/detuning changes projector mixing and therefore the Hermitian hybrid group rate when the bare rates differ;
- increasing damping shortens the coherent memory envelope and spends coherence/energy;
- dwell/re-emission adds residence time even when the coherent equal-rate slowdown vanishes.

So the useful version of the earlier metaphor is a **kite on a controllable reel**, not an electron physically trailing behind a photon and not friction as the fundamental origin of the slower hybrid rate.

## Retina / Cortex status

The live viewer was built from the exact embedded catalog of **191 public eye versions** in Compound Eye Universal 3.2:

- 172 implemented;
- 17 specified/unimplemented;
- 2 archived results.

For this question the transparent routing heuristic marks **56** implemented eyes for direct inspection, leaves **116** visible in standby, records the 17 specified eyes as blocked, and keeps the 2 archived results visible. `routed` means selected for inspection; it is **not** a claim that all 172 Python functions were executed with compatible scientific inputs.

This preserves the Cortex rule: **attention prioritizes; it never erases.**

## Visual app

The generated standalone live viewer contains:

- animated fast, slow and hybrid rails;
- coupling/tether and memory-tail visualization;
- live parameter controls for bare rates, coupling, detuning, damping and probe;
- coherent versus dwell delay decomposition;
- directional demand versus matter coupling rank;
- Rice-Mele gap/rate/correlation/boundary analogue;
- a live coupling-sweep mixer;
- a cause-spine view;
- local intervention sensitivity bars;
- a three-mechanism same-speed discriminator;
- a hypothesis board;
- the full 191-eye public retina with searchable input/scope records;
- a link back to the unchanged Universal 3.2 app.

## Evidence boundary

This run establishes relationships in a declared finite operator model and exact/finite numerical controls. It does not establish that a free photon in vacuum is tethered to a single electron, does not prove a physical electron is the unique origin of optical slowdown in matter, does not transfer Arithmetic Kakeya into optics, and does not establish a theory of everything.

The next empirical discriminator is to use one calibrated spatially extended light-matter Hamiltonian and measure, from the same system, hybrid velocity, projector fractions, self-energy/time memory, phase/susceptibility, directional coupling rank and loss. The minimal coherent model predicts that at fixed bare rates/detuning the group-rate change tracks the matter projector weight; failure of that relation falsifies this minimal tether model for that system.