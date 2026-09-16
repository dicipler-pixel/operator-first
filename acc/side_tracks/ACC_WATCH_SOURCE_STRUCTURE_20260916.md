# ACC Side-Track WATCH Source-Structure Freeze — 2026-09-16

This is a second WATCH freeze. It was recorded **before the controlled mix**.

Pipeline fence: RAW RECORD -> WATCH -> FREEZE -> MIX -> SEARCH/DECIDE -> OFFICIAL CERTIFICATION.

Parent WATCH commit: `f1420c19d2ae0e421039933d95190e3f2bb0ad0c`.

## Official source provenance

Official repository: `SAIRcompetition/Andrews-Curtis`.
Official problem file: `competition/problems/ac.jsonl`.
Pinned competition commit: `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`.
Git blob SHA at the pin: `09434a6e46090e6c086afa1104b49a4f890a4855`.
The current `main` fetch reports the same blob SHA, so the official problem file is byte-identical to the pinned file.

## Correction / quarantine note

The first three pair rows below pass the independent initial-total-length check against the T1 ledger (`ini=17`). The earlier transcription for the fourth pair `ac-00764/ac-06570` produced length 18 and is therefore quarantined as a bad source transcription rather than used in the mix. It remains in Git history for provenance; it is not evidence.

## Verified source-structure eye

### ac-05616 / ac-05894
- ac-05616 r1: `y^-1 x^-1 x^-1 y^-1 x x y^-1 x`
- ac-05894 r1: `y^-1 x^-1 y^-1 x^-1 x^-1 y^-1 x x`
- shared r2: `y^-1 y^-1 y^-1 y^-1 x^-1 y y y x`

### ac-06835 / ac-07247
- ac-06835 r1: `y^-1 y^-1 x^-1 x^-1 x^-1 y x x`
- ac-07247 r1: `y^-1 y^-1 x^-1 x^-1 y x^-1 x^-1 x^-1`
- shared r2: `y^-1 y^-1 y^-1 y^-1 x^-1 y y y x`

### ac-02024 / ac-06036
- ac-02024 r1: `y^-1 y^-1 x x x y x^-1 x^-1`
- ac-06036 r1: `y^-1 y^-1 x x y x^-1 x^-1 x^-1`
- shared r2: `y^-1 y^-1 y^-1 y^-1 x^-1 y y y x`

## Frozen observations

1. The six verified presentations above share the same second relator exactly.
2. Within each verified pair, source variation is confined to the first relator.
3. A direct free/cyclic word check found that no paired r1 words are related merely by cyclic rotation, nor by cyclic rotation after inversion.
4. The fourth pair is excluded from source-structure mixing until its official rows are cleanly re-extracted.
5. None of this proves or disproves ordinary AC equivalence.

No pair is merged and no equivalence is claimed in this WATCH file.
