# ACWindow Lean

`ACWindow.lean` is the frozen core-Lean word-level kernel for the fourteen
ordinary SAIR Andrews–Curtis moves (`ac-r2-v1`).

It currently proves:

- the fold `AK(n) -> AK(-n-1)` for every integer `n`;
- a finite kernel-evaluated resonance control in `C_p * C_p` for
  `p = 2..29`, `n = -10..40`;
- the 9-move `C_5 * C_5` image certificate
  `[1,13,5,11,4,6,3,5,0]`;
- the single-letter conjugation fixed-point lemma;
- a finite literal-word fold control.

It does **not** import the official `AC.lean` and makes no claim about
`AC.Reachable`.

Frozen file SHA-256:

`a5d61103cfe60a249d1673fa170d36b2bb08f87908c35700fdaae0495fb7d5d4`

Do not bulk-copy ACC research into this directory. The gate for theorem-level
material, exact source SHAs, recheck candidates, and rejected heuristic imports
is:

- [CURATED_ACC_INTAKE.md](CURATED_ACC_INTAKE.md)
