# Claude Code ACC handoff — 2026-09-12

## What this branch adds

`research/acc/dag/` — an append-only knowledge DAG for the ACC effort, seeded
with this session's verified results. It is a file format, a validator and a
query, not a framework. Agents read `--open` / `--blocked` before starting and
append result nodes after, so findings stop living only in chat transcripts.

    python3 research/acc/dag/dag.py --check      # validate invariants
    python3 research/acc/dag/dag.py --blocked    # what is stuck and why
    python3 -m unittest discover -s research/acc/dag

## Exact provenance

| Object | Commit |
| --- | --- |
| Official pool + verifier | `SAIRcompetition/andrews-curtis` main `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e` |
| ACC well work | `acc-length-well-eye-2026-09-12` `6cbe71cf99df7d6e41dd0ad3f0966d836a4bfe90` |
| ACC observer work | `acc-collab-2026-09-11` `83724f198d11b76fa47aadc964ff6b4b529ede9d` |
| AC datasets | `Math-AI-Caltech/acsolverx` `6a12515fe1d95178a483b76d5553266e61122417` |
| Base of this branch | `main` `436779d` |

## What was executed and passed

1. Official verifier self-test: 63/63 golden vectors; all 20,230 challenge
   hashes recompute; both training paths return `ok: true`.
2. **Kernel equivalence.** The branch's 20-move `ac-00015` descent witness was
   replayed from the official manifest relators through
   `verifier.core.apply_move`. The length profile matched all 21 entries and
   the final state matched `LENGTH_WELL_STATUS.md` exactly. The length-well
   programme rests on genuine `ac-r2-v1` semantics.
3. `ac-00015` start length 21 and `ac-00002` start length 25 confirmed against
   the official manifest.
4. Reverse target basin recomputed: 1, 11, 88, 662, 5115, 40779, **336477**,
   2849131 at radius 0..7 — confirming the Target-2 figure.
5. Pool composition reproduced: 733 Miller-Schupp entries = 550 open + 183
   uncertified + 0 certified, matching the organisers' stated construction.
6. Upstream drift checked: the hub's recorded SAIR head `99a65377` is an
   ancestor of `a0fd6e6f` and the pool/manifest bytes are identical between
   them. No re-freeze; earlier work stays valid.
7. **Independent closure engine** (`research/acc/official_closure.py`, built on
   `verifier.core`, no shared code with the C++/string engines) reproduces
   every published well count exactly: `ac-00015` cap 26 = 105,912;
   `ac-00002` cap 31 = 1,021,696 and cap 32 = 1,303,928; second well cap 29
   = 5,149,128 and cap 30 = 9,096,912 with the full level census matching.
   Every certified well bound now rests on two independent implementations.
8. DAG regression suite 15/15; closure regression 3/3.

## What failed / what is missing

- **Blocker: the Highway checkpoint does not exist in version control.**
  `highway`, `submitted_best`, `ac-03364`, `ac-05613`, `ac-07031` return zero
  hits across all 44 remote branches; the private hub's `ledger/` and
  `results/` are 140-953 byte files. Per the ACC brief section 6 this is
  reported, not reconstructed. Highway work stays interface-only.
- **336,477 appeared in no branch.** The figure was correct but had never been
  persisted. Recomputed and recorded as a node.
- **Network.** `competition.sair.foundation`, `terrytao.wordpress.com`,
  `arxiv.org` and `zulip.sair.foundation` are blocked by egress policy in this
  environment. Submissions cannot be uploaded from here; a `submission.txt` can
  be produced and locally verified only.

## Negative / cautionary results recorded

- `ac-00002` is Miller-Schupp in form (n = 6) but is in **none** of MS-1190,
  AC-19, AC19_extended or AC-1M. It has no prior art to inherit.
- (Resolved this session.) The `ac-00002` cap-31/32 and second-well cap-30
  counts previously had a single engine behind them; see item 7 above.

## Public/private boundary

One node (`pool-known-actrivial-overlap`) is marked `visibility: private` and
carries its aggregate only. The per-challenge id list is competitive
intelligence and belongs in the private hub, not here. `dag.py --check`
enforces that private nodes carry no payload in this repository.

## Next bottleneck

`cap31-neck` is the open question node. Before anyone starts: the cap-30 L30
level alone holds 3,801,440 states, so a full boundary enumeration is roughly
53M edge evaluations. Budget a two-stage funnel — cheap labels on every exit,
expensive labels (Magnus depth, return-channel counts) on a filtered subset —
or the scan will not finish.

## Late correction — 2026-09-12 ~21:00Z

- **T16 is in the start orbit.** `[8,12,10]` takes the official `ac-00008`
  start to T16; both relators keep their conjugacy classes. The 71-move
  Noff-9 -> Noff-18 -> T48 -> T16 excursion is a loop. Do not use ORIG-16 vs
  T16 as evidence that hab/foxA/H3/D detected a better basin.
- **Required regression added.** `research/acc/eyes.py` now has an exact
  start-orbit eye (`orbit_signature`, `in_start_orbit`, `distance_back`,
  `collapse_outcome`). The cancellation eye's collapse floor predicted both
  ac-00008 collapses exactly (48->29, 29->16), but the second one is a
  *return* to the start orbit. Read collapse floor and start-orbit together.
- **Confirmed team routes.** Noff-9 -> T16 in 10 moves (none <= 9 under cap
  60); start -> the length-38 hab-0 state in 12 moves (none <= 11 under cap
  60). Both replayed under the official kernel; both bounds re-derived with
  an independent bidirectional search.
- **Not closed.** The cap-32 component of the post-deletion state D exceeded
  24.4M states and was killed; no bound is claimed.
- **ac-00002 well raised.** Official-kernel closures from the start at cap 33
  (4,658,392 states) and cap 34 (6,312,448 states) are closed with minimum 25.
  Every descent must visit total length >= 35; certified depth is now +10.
- **Shortening is exhausted.** Segment meet-in-the-middle (windows 8-24) left
  the beam routes for ac-00104/00974/04308 unchanged, like the earlier window
  shortener.

## Team hub and retirements — 2026-09-12 ~22:45Z

- **Where the other lanes live.** The team hub is the Google Drive folder
  "Mad Hatters ACC Shared Hub" (Claude chat, ChatGPT, Grok read it; only
  Claude Code reads this repo). Every result here is mirrored there as a
  `CLAUDE_CODE_TO_TEAM_NOW_*.md` note. Read `CLAUDE_AK3_IDENTIFICATION.md`
  and the newest `CHATGPT_TO_CLAUDE_NOW_*.txt` there before running anything.
- **Retired by theorem.** ac-00399, ac-06279 and ac-06945 are AK(3) up to
  signed relabelling (DAG `ak3-disguises-confirmed`). Do not search them.
- **Dead ends closed today** (all in the DAG): three beam shapes and greedy on
  the 58 long k=1 records; the length beam on the 62 shortest unsolved;
  segment and window shorteners on beam routes; the eye-ranked beam control;
  ChatGPT's atlas proximity scan (radius <= 4, zero meets on 2,730 starts).
