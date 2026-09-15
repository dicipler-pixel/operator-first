# MS-1190 status is an exact predictor of board status

Derived entirely from the official public competition package
(`github.com/SAIRcompetition/andrews-curtis`, commit `a0fd6e6`) plus the
2026-09-12 Discovery board snapshot. No platform API was called.

## What the official package publishes

`competition/tools/verifier/data/README.md` publishes the frozen encoding
for the Miller–Schupp family:

    r0 = x^-1 y^n x y^-(n+1)        r1 = x w^-1        (both freely reduced)

and ships `ms1190_metadata.csv`, which gives `n`, `w_vector` and a
`status_at_freeze` for all 1190 MS instances:

| status | count | meaning |
|---|---|---|
| `open` | 550 | no known trivialization |
| `uncertified` | 216 | literature reports solved, no public replayable certificate |
| `certified` | 424 | public replayable path exists (training data) |

The README also states the pool composition: *"all 550 open MS-1190
instances are scored, no certified one is."*

## Recovering the challenge IDs

`ms_match_v1.py` rebuilds each MS presentation from `n` and `w_vector`,
then matches it against `manifest.json` under the pool's own uniqueness
relation — relator order, cyclic rotation, and inversion.

    exact 0   canon 733   unmatched 457   (of 1190)

      certified    unmatched  424
      open         matched    550
      uncertified  matched    183
      uncertified  unmatched   33

Zero ambiguous matches, zero duplicate challenge IDs. The match is
self-validating: **all 424 certified rows fall outside the pool and all
550 open rows fall inside it**, exactly as the official README states.
Exact match is 0 because the manifest stores each presentation in its own
rotation; the canonical relation is the correct one and its counts
reproduce the documented composition.

Output: `ms1190_to_challenge_v1.jsonl`, 733 rows.

## The result

Against the 2,730 challenges the 2026-09-12 board lists as unsolved:

| set | size | unsolved on board |
|---|---|---|
| MS `open` | 550 | **550 (100.0%)** |
| MS `uncertified` | 183 | **0 (0.0%)** |
| everything else | 9,382 | 2,180 (23.2%) |

The label separates the pool perfectly. Under independence at the 27.0%
base rate the two tails are about `10^-313` and `10^-25`.

This is empirical, not tautological. `open` means no trivialization was
known at freeze; it does not forbid a competitor from finding one. In the
first day of the Discovery window nobody did — not one of the 550. And
every one of the 183 `uncertified` rows, where the literature says a
solution exists, was already taken.

## What it changes

**The 550 MS-open rows are the hard core.** They are 20.1% of the
unsolved set and the only part of it with a published reason to be hard.
They are also worth the most: scoring is `2^(1-k)` for the `k` teams tied
at the shortest verified solution, so a first solve on a row nobody has
touched pays the full **1 point**, the maximum any challenge can pay.

**The 183 MS-uncertified rows are worthless to search.** All are solved;
a tie only splits the point further.

**Component structure tracks the MS label.** Of the 24 multi-member
components found by the bounded-transport sweep, 14 contain an MS-open
challenge and **13 of those 14 are entirely MS-open**. This is an
independent confirmation of the component-homogeneity result — a
component's members share board status, and here they share provenance
too. Transport between members uses the coordinate-transport and
donor-restoration ideas of Robert Sneiderman (ACC-P000002,
`github.com/Robby955/ac-square-divisibility` @ `d0ed2c06`).

### Ranked n-for-one targets

15 all-unsolved components, 37 challenges. `minlen` is the shortest
initial total relator length in the component — the cheapest member to
attack, since a solve transports to the rest.

| rep | size | minlen | shortest | all MS-open |
|---|---|---|---|---|
| ac-00413 | 4 | 14 | ac-00413 | no (2 open, 2 draw) |
| ac-01657 | 3 | 15 | ac-01657 | yes |
| ac-02422 | 3 | 15 | ac-02422 | yes |
| ac-04967 | 3 | 15 | ac-04967 | yes |
| ac-06349 | 3 | 15 | ac-06349 | yes |
| ac-06576 | 3 | 15 | ac-06576 | yes |
| ac-00399 | 2 | 13 | ac-00399 | no (draw) |
| ac-01083 | 2 | 15 | ac-01083 | yes |
| ac-01558 | 2 | 15 | ac-01558 | yes |
| ac-01571 | 2 | 15 | ac-01571 | yes |
| ac-01956 | 2 | 15 | ac-01956 | yes |
| ac-02216 | 2 | 15 | ac-02216 | yes |
| ac-02563 | 2 | 15 | ac-02563 | yes |
| ac-02828 | 2 | 15 | ac-02828 | yes |
| ac-04619 | 2 | 15 | ac-04619 | yes |

### Shortest ungrouped MS-open rows

517 MS-open challenges are not yet in any known component. The shortest
are the natural next sweep:

    ac-02842  len 14  n=3  w = x^-1 y^-1 x y^-1
    ac-03467  len 14  n=2  w = y x^2 y x^-2
    ac-06556  len 14  n=3  w = y x y x^-1
    ac-08126  len 14  n=2  w = x^-2 y^-1 x^2 y^-1
    ac-04300  len 15  n=3  w = x^-1 y^-2 x y
    ac-08892  len 15  n=2  w = x^-1 y^-1 x^-1 y^-1 x^2 y^-1
    ac-09350  len 15  n=3  w = y^2 x y^-1 x^-1

## What is still missing

Per-challenge best lengths. The board snapshot gives solved/unsolved
only. The lengths live behind an authenticated endpoint,
`GET /competitions/acc/discoveries/snapshot?problem=ac`, whose items carry
`currentBestLength` and `kTeams`. Nothing in any public repository
mirrors it. For the 550 MS-open rows it does not matter — `k` is 0, so
any verified path scores 1 — but for every other row it is what turns a
search result into a priced candidate.
