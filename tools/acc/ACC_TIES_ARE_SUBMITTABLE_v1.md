# Ties are submittable — and we have eighteen

**Correction to `ACC_METRIC_VS_LEDGER_AUDIT_v1.md` and to
`ACC_PRICED_AUDIT_20260916_v1.md` §1.** Both concluded our ledger lines were
worth zero. Both were applying a test the board does not use.

## The audit's own rule never said a tie was worth zero

    Scoreboard reads LEDGER length only.
    If kTeams already holds a SHORTER ledger, the METRIC improvement is 0.

*Shorter.* A tie is not shorter. The rule zeroes you only when someone holds
something strictly better. I read "zero improvement" as "zero value" and never
checked what the board does with an equal-length submission.

## What the board does with a tie: counts you

Take every row whose `currentBestLength` is **identical** on the 09-12 and
09-16 snapshots, and look at what `kTeams` did:

| rows with an unchanged record | 476 |
|---|---|
| `kTeams` **rose** | **450** |
| `kTeams` unchanged | 26 |
| `kTeams` fell | **0** |

450 rows gained holders while the record did not move by a single unit, and
not one row ever lost a holder. There is only one reading: **teams submit
record-length paths, the board accepts them, and `kTeams` increments.** Tying
is not a consolation — on static rows it is essentially the whole of the
observed activity.

Every one of our eighteen tie rows shows it directly:

    ac-01635  record 8->8    k 17->29      ac-00742  record 10->10  k 14->24
    ac-08491  record 8->8    k 17->28      ac-01411  record 11->11  k 12->23
    ac-07445  record 13->13  k 12->21      ac-04631  record 11->11  k 13->21
    ac-06500  record 15->15  k 12->19      ac-00977  record 17->17  k  9->14
    ac-09594  record 15->15  k 10->17      ac-10029  record 18->18  k  7->12
    ac-04359  record 17->17  k  6->14      ac-06225  record 19->19  k 10->15
    ac-08327  record 17->17  k  4-> 8      ac-04275  record 21->21  k  4->11
    ac-09868  record 25->25  k  2-> 5      ac-06823  record 21->21  k  5->11
                                           ac-10115  record 22->22  k  3-> 6
                                           ac-01059  record 22->22  k  2-> 4

## The eighteen

**Eight** from the existing ledger (already cashed by the frozen verifier):
`ac-01635` 8, `ac-08491` 8, `ac-07445` 13, `ac-06500` 15, `ac-09594` 15,
`ac-04359` 17, `ac-08327` 17, `ac-09868` 25.

**Ten** found and captured this session, each at exactly the board record:
`ac-00742` 10, `ac-01411` 11, `ac-04631` 11, `ac-00977` 17, `ac-10029` 18,
`ac-06225` 19, `ac-04275` 21, `ac-06823` 21, `ac-10115` 22, `ac-01059` 22.

Move sequences are in `PRIVATE_ties_20260916.json` (gitignored per the repo's
"never commit competition certificates" rule).

All ten were **independently verified** by `verify.py` — a Python replay
written from the AC move definitions, sharing no code with the C engine. All
ten land on `(x, y)` exactly, at exactly the stated length.

## What I can and cannot claim

**Established:** ties are accepted and increment `kTeams`; our ten paths
verify; they match the record exactly.

**Not established:** how points divide among `k` co-holders. The snapshot
carries no scoring formula, so I cannot say what an 18th holder on a k=29 row
is worth versus a 5th holder on a k=4 row. If the split is per-capita, the
low-`k` rows (`ac-01059` k=4, `ac-09868` k=5, `ac-10115` k=6) are worth more
than the crowded ones (`ac-01635` k=29, `ac-08491` k=28).

## The lesson

Twice now the zero-value conclusion came from a test I invented rather than
one the board runs — first "the row is solved", then "only strict improvement
counts". Both times the snapshot had the answer sitting in a column I had
already parsed. **Check what the board rewards before deciding what the work
is worth.**
