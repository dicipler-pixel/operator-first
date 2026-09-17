# Operator-First Atlas: Finite Lean Kernels v0.2

Certified source: `formal/atlas-cards-2026-09-11` at `f4e682ff428b5e941a3da7d2a1b211dc925bdbc6`  
Pull request: https://github.com/dicipler-pixel/operator-first/pull/21  
Verification: https://github.com/dicipler-pixel/operator-first/actions/runs/34684818137

Run `python verify.py`. The verifier builds the pinned project, audits theorem axioms, runs `leanchecker`, and requires the mathematical false controls to fail.

The corrected B56 kernel proves that no linear map from `ℝ²` to `ℝ³` is surjective. Applied to one wall equation plus two coalescence equations, this says that any meeting is nontransverse. It does not assert unconditional disjointness or a genericity theorem.
