# External result (relayed by the owner, 06:10Z 2026-09-30): ac-02089 and ac-08126 (unsolved, k0)
Source: alejandrozarco/andrews-curtis-ms14 @ 3b646c8. Authors used Claude; it is not a team member's result. Not verified by us.
- **ac-02089 = MS(2, x⁻²y⁻¹x²y)** is AC-equivalent to the residual class C6 = ⟨x,y | x²yx²y⁻², xyx⁻¹y⁻²x⁻¹y⟩ (nahomar list). Their certificate is 1,066 moves (peak total length 41), replayed with the official `apply_move`. So solving C6, or linking C6 to ac-00399 (AK(3)), solves ac-02089.
- **Lower bound (their search model, not independently checked):** exhaustive search up to total length 32 (71.5M states mod symmetry, conjugators ≤ 8) shows no path to trivial or to AK(3) from either row. **Any solution must climb to total length ≥ 33.**
- **For us:** these are first-solve rows (1 pt each if solved), but our exact tool caps near start+14 = 28 on a length-14 start, far below 33. Our beams (DMAX = record + 2) have no record to aim at. **Do not spend exact-search time on them.** Only a high-climb method (Git's pulse/doubling ideas, Kernel's outward growth) has a chance.
- ac-00399 (AK(3)) is unsolved on the board too, as expected.
- Team files that list these rows as targets: UNSOLVED_TARGETS_20260928.json, targets_codex_oddeasyB.json, WORKING_codex_abc.md. Lanes working them should read this first.
