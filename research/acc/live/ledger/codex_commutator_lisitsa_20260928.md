# Codex probe: Miller–Schupp mapping and commutator phase (2026-09-28)

## Exact family identification

Shehper et al. arXiv:2408.15332v2, Theorem 3 and the cited Lisitsa (2024)
family use (w_\star=b^{-1}ab a^{-1}), giving ordered relators
[
Q_n=(a^{-1}b^n a b^{-(n+1)},\ a^{-1}b^{-1}ab a^{-1}).
]
Set (a=x, b=Y=y^{-1}), and let (X=x^{-1}).  The first word is
(X Y^n x y^{n+1}); **invert** it to obtain our scored second relator
(Y^{n+1}X y^n x).  The second word is (X y x Y X); **cyclically rotate**
it to (Y X X y x), our scored first relator.  Thus the relevant scored
family is the **YXXyx** chain, specifically ac-01950 (n=5), ac-02033
(n=6), ac-06796 (n=7), ac-03079 (n=8), ac-06727 (n=9),
ac-00106 (n=10).  The 11:45Z IDEAS entry's (w_\star) spelling
`y^-1 x^-1 y x^-1 y x` and `YXyXyx` identification are different
words and should not be used to transfer Lisitsa paths to this family.
A formal equivalence of presentations does not price the swap, rotation
or generator change as free scored moves.

Theorem 3 gives existence for every n by a generator swap and rewriting
through MS(1,w).  It does not supply the rival's record-length scored
certificate.  The 2025 n=9 Lisitsa sequence is 8,634 moves by its
abstract, much longer than the competition record.

## Commutator eye: exact algebra and replay

Let (c(r,s)=|\operatorname{cyc}([r,s])|) be cyclically reduced length of
(rsr^{-1}s^{-1}).  **Moves 0–5 preserve c exactly**: replacing
(r\mapsto rs^{\pm1}) or (s\mapsto sr^{\pm1}) changes the commutator
at most by conjugacy/inversion, and inversion also preserves cyclic
length.  Only single-letter conjugations (moves 6–13) can change c.
This proves why c cannot be a standalone move-by-move compass for
multiplications.  It is a diagnostic for the rotation phase.  The
team lead already screened this same `comm_len` as a P2 tie-break
(`SCORE_ZOO.md`, climbing top-3 0.413 -> 0.616 on 59 hump paths);
this probe proposes an **event trigger**, not a duplicate primary score.

Replay of previously verified paths through the pinned SAIR `core.py`
(commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e):

| route | moves | c at start / max / end | first c=4 | moves remaining | conjugation changes (down / flat / up) |
|---|---:|---:|---:|---:|---:|
| YXXyx n=3 | 29 | 22 / 24 / 4 | 21 | 8 | 3 / 6 / 2 |
| YXXyx n=4 | 55 | 26 / 38 / 4 | 37 | 18 | 4 / 8 / 9 |
| YXXyx n=5 (Codex generator) | 125 | 30 / 70 / 4 | 91 | 34 | 5 / 32 / 24 |
| P -> AK(3), 53 h moves | 53 | 46 / 50 / 22 | never | n/a | 18 / 5 / 19 |

In each row every Nielsen move (18, 34, 64, 11 respectively) was
c-flat.  On n=5 the successful path **rises to c=70 before falling to
4**, so pruning states for high c kills this route.  The first c=4
state is
`(xYx^29, xYx^30)`; two rotations plus one multiplication make
`(xYx^29,x)`, then the long peeling tail.  Its trigger at step 91
already exceeds the record 80: **no scoring hit**.  Possible next
experiment: treat c=4 as a camera switch to a Nielsen/endgame solver,
compare early-hit rate and full verified path length against P2 on
n=5/6.  Do not infer optimality from this one generator.

## Local camera-switch attempt on n=5

Searched all scored-move detours of radius at most 4 from every prefix
before the first c=4 event of the 125-move route.  Each detour was
bounded by total relator length 100 and deduplicated by exact ordered
state for each prefix.  **1,216,470 neighboring states** were tested;
none reached c=4 sooner than step 91.  This is only a neighborhood
result, not a lower bound on all n=5 routes.  Reproduce with
`python3 research/acc/optimality/codex_commutator_phase_probe.py --sair-root SAIR-AC --detour-radius 4`.
No record tie or beat resulted.

## AK(3) attachment and scoring convention

The user's independently replayed Shehper 53 h_i moves reach P ->
AK(3), with no subsequent stable trivialization.  For the pinned
`ac-r2-v1` scored 14-move table, their h1..h12 translate to:

`{1:4, 2:3, 3:5, 4:2, 5:11, 6:9, 7:13, 8:6, 9:10, 10:8, 11:12, 12:7}`.

SAIR has inverse-other multiplication directly as moves 3 and 5, so
this is **53 SAIR ordinary moves** even though the paper's stricter
standard move convention expands those to 67.  An exact replay via
the pinned `verifier.core.verify` on a *synthetic* P-to-AK3 endpoint
returns `ok=True, length=53, peak_total_relator_length=25, work=891`.
This is equivalence data only, **not a solution to any SAIR challenge**
and not a proof of AK(3) or stable AK(3).

Sources:
- https://arxiv.org/html/2408.15332v2 (Theorem 3, §3.4)
- https://github.com/SAIRcompetition/Andrews-Curtis/blob/a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e/competition/tools/verifier/core.py
- `tools/acc/ak3_p_to_ak3_replay.py` (same as the user's attachment)
- `research/acc/optimality/yxxyx_chain.py` and `research/acc/live/ledger/codex_yxxyx_trace.py`
