# Lisitsa's Miller–Schupp sequences: independent replay

28 September 2026

## Sources and scope

- Alexei Lisitsa, [*New Andrews–Curtis trivializations for Miller–Schupp group presentations*](https://doi.org/10.1016/j.exco.2024.100168), *Examples and Counterexamples* 6 (2024), and the [author's 2024 preprint](https://easychair.org/publications/preprint/M5tc/open). The published paper covers the fixed-word examples through MS(8); the preprint gives the explicit structural conjectures.
- Lisitsa, [*Automated theorem proving reveals a lengthy Andrews–Curtis trivialization for a Miller–Schupp trivial group presentation*](https://www.sciencedirect.com/science/article/pii/S2666657X2500028X), on MS(9).
- [Supplementary data, version 2](https://doi.org/10.5281/zenodo.14647749), containing `MS-3-LAB.txt` through `MS-9-LAB.txt`, retrieved here as `MS_supplement_v2.zip`. The ZIP's MD5 is `345a7a0d3ddfffe395a52f8b0474c4f2`, matching Zenodo.

The examples are the **fixed-word** subfamily

\[
MS_n(w_*)=\langle a,b\mid a^{-1}b^n a b^{-(n+1)},\;a^{-1}b^{-1}aba^{-1}\rangle,
\qquad 3\le n\le9.
\]

They are not arbitrary Miller–Schupp presentations \(MS_n(w)\). In the data, capitals `A,B` mean \(a^{-1},b^{-1}\).

## Replay result

`python ms_lisitsa_replay.py MS_supplement_v2.zip` verifies the source checksum and all consecutive relators. It checks `INV` as inversion, `MULT` as first relator multiplied on the right by the unchanged second relator, and `CONJ` by extracting an explicit conjugator \(z\) and checking free reduction of \(zuz^{-1}=v\). It also checks both endpoints for every file.

| File | Archive moves | `INV` | `MULT` | `CONJ` | Longest first relator | Moves with common finish |
|---|---:|---:|---:|---:|---:|---:|
| MS(3) | 55 | 18 | 14 | 23 | 11 | 66 |
| MS(4) | 160 | 46 | 42 | 72 | 14 | 171 |
| MS(5) | 401 | 106 | 102 | 193 | 17 | 412 |
| MS(6) | 906 | 230 | 226 | 450 | 18 | 917 |
| MS(7) | 1,942 | 486 | 482 | 974 | 21 | 1,953 |
| MS(8) | 4,145 | 1,024 | 1,020 | 2,101 | 24 | 4,156 |
| MS(9) | 8,623 | 2,088 | 2,084 | 4,451 | 28 | 8,634 |

All **16,232 labeled archive moves pass**. Every file begins with \(a^{-1}b^n a b^{-(n+1)}\), keeps \(a^{-1}b^{-1}aba^{-1}\) fixed, and ends with the first relator \(ab^{-1}a^{-3}\). The archive stops there. The final column adds the independent 11-step finish below; the MS(9) total agrees with Lisitsa's 8,634.

### Explicit common finish

This is an independent construction from the common endpoint. A `CONJ z` step replaces the indicated relator \(r\) by \(zrz^{-1}\); `MULT` replaces it by \(r\) times the other relator. All words below have been checked by free reduction. The last pair \((b,a)\) presents the trivial group; its relators are written in reverse order from \((a,b)\).

| Step | Relator changed | Operation | First relator | Second relator |
|---:|---:|---|---|---|
| 0 | — | start | `aBAAA` | `ABabA` |
| 1 | 1 | `CONJ A` | `BAA` | `ABabA` |
| 2 | 2 | `CONJ A` | `BAA` | `AABab` |
| 3 | 2 | `MULT` | `BAA` | `AABA` |
| 4 | 2 | `CONJ aa` | `BAA` | `BAAA` |
| 5 | 2 | `CONJ aab` | `BAA` | `ABAA` |
| 6 | 1 | `INV` | `aab` | `ABAA` |
| 7 | 2 | `MULT` | `aab` | `A` |
| 8 | 1 | `CONJ b` | `baa` | `A` |
| 9 | 1 | `MULT` | `ba` | `A` |
| 10 | 1 | `MULT` | `b` | `A` |
| 11 | 2 | `INV` | `b` | `a` |

If an implementation requires the **ordered tuple** \((a,b)\), it must also account for swapping the two relators; this finish itself ends at \((b,a)\). The supplied Zenodo sequences contain no finish beyond `aBAAA`.

### Shared suffixes

The archive trajectories of neighboring \(n\) agree exactly on these *final states and operation labels* (before the common 11-step finish). Indices are zero-based state indices in the larger and smaller files, respectively.

| Pair | Shared archive moves | First common state at indices |
|---|---:|---|
| MS(4) / MS(3) | 35 | 125 / 20 |
| MS(5) / MS(4) | 134 | 267 / 26 |
| MS(6) / MS(5) | 369 | 537 / 32 |
| MS(7) / MS(6) | 893 | 1,049 / 13 |
| MS(8) / MS(7) | 1,590 | 2,555 / 352 |
| MS(9) / MS(8) | 4,063 | 4,560 / 82 |

These shared tails make a finite **merge pattern** visible. None of MS(4)..MS(9) goes through the exact MS(\(n-1\)) starting relator, nor even a conjugate of it, while keeping the second relator fixed. The varying join states do not themselves give an induction \(n+1\to n\).

## What is proved, and what remains open

The replay independently certifies ordinary AC trivializations for these seven fixed-word instances, conditional only on the standard interpretation of the three operations and the usual identification of relator order. It does **not** prove the conjectured pattern for all \(n\), nor classify unrelated \(w\), nor resolve AK(3). Lisitsa's preprint calls the fixed-second-relator pattern Conjecture 3 and proposes a one-relator search with the second component omitted; the v2 archive extends its finite evidence through \(n=9\). A universal Lean theorem would need a parameterized bridge or other induction argument in addition to importing these finite witnesses.

The replay is a Python free-group audit, not a Lean compilation. It constructs actual conjugating words for each `CONJ`, so they can be emitted into a later Lean certificate rather than trusting an unlabeled conjugacy oracle.
