# Timeline — format v1

The per-claim report says what the eyes see now. This layer says what keeps
coming back, and what happens either side of it.

## The honesty gate comes first

Every ledger here is append-only and timestamped, but that is not the same as
having a time series. Most of these records were written by one command, so
their internal timestamps span milliseconds. Counting repeats inside a single
write would manufacture a trend out of one act.

So `--window` reports, per source, how many **write batches** the records fall
into (a batch is anything closer together than 2 seconds), and every recurring
signal carries a strength:

| strength | meaning |
| --- | --- |
| `sustained` | occurrences spread over days |
| `one-day` | spread over hours |
| `one-session` | spread over minutes, inside one sitting |
| `one-batch` | **all occurrences written by one command — not evidence of recurrence over time** |
| `single` | seen once |

`one-batch` signals are still printed, last and labelled. They are real
structure, just not temporal structure. The four eyes blocked on the same
class-group bridge are a *fan-in* — one bridge that four instruments wait on —
and that is worth knowing. It is not four events over time, and the tool says
so rather than letting the count imply it.

Records with no timestamp at all (the 848-row post-run mix ledger) are ordered
by file position only. They are counted and declared, and excluded from any
before/after claim.

## What counts as a signal

Extracted from every record, never hand-entered:

    blocker         what an eye is waiting for
    failure-mode    how an eye could be wrong
    assumption      what an eye rests on
    verdict         eye:verdict
    evidence        evidence class
    status          lane:status
    unit-guard      a refusal to add unlike channels
    replay-failure  a recipe that did not reproduce
    transport       a hand-off transport outcome
    weight-zero     an eye kept at weight zero
    commit-area     the prefix of a commit subject — which part of the work reopened
    set / seal / attest / roster / snapshot

## Before and after

`--context <signal>` shows, for each occurrence, the N events immediately
before and after it, then aggregates which kinds of event most often precede
and follow it. That is the "what is going on around this" question.

`--around <anchor>` takes a commit, a hand-off id, a run id or a timestamp and
prints the board either side of it: runs verified and blocked, eyes filed and
silent, distinct blockers, hand-offs checked and attested. It names blockers
that appeared, blockers that cleared, and any eye whose verdict flipped across
the anchor.

## Making the record longer

    python3 tools/acc/timeline_v1.py snapshot

appends the current board to `snapshots_v1.jsonl`. One snapshot is a point; the
tool says so until there are at least two. `.github/workflows/acc-timeline.yml`
runs daily and takes a snapshot as CI evidence.

**Known limitation.** That scheduled run has `contents: read`, so its snapshot
is uploaded as a run artifact and does not land in the repository. The durable
series is the committed `snapshots_v1.jsonl`; the CI runs are independent
samples alongside it. Making CI commit its snapshots would need write access to
the branch, which is a decision for the repository owner, not a default.

## Use

    python3 tools/acc/timeline_v1.py --window
    python3 tools/acc/timeline_v1.py --recurring [--min N]
    python3 tools/acc/timeline_v1.py --context "blocker=exact class-group" [--span 3]
    python3 tools/acc/timeline_v1.py --around <commit|handoff_id|run_id|ISO>
    python3 tools/acc/timeline_v1.py --stream [--source S] [--since ISO]
    python3 tools/acc/timeline_v1.py snapshot
