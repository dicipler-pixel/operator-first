# Compound Eye run ledger — format v1

This is how work in this repository is logged, tracked and traced. One run,
one line, append-only, in `run_ledger_v1.jsonl`.

The point is that a row here is backed by an instrument. Every run is written
by `tools/acc/mixer_log_v1.js`, which validates it through
`tools/compound-eye/projects/eye_mixer/mixer_core.js`. That file is **frozen and
never modified**. The recorder only reads it. So the record cannot drift away
from the mixer that produces it, and a row that claims to replay has been
replayed.

## Why the mixer and not a log file

Three properties are doing real work here, and none of them are decoration.

**The unit guard.** The mixer refuses to add channels that carry different
units under source normalization. When that refusal fires it is recorded as
`units_commensurable: false` with the refusal message. That is a finding about
the run, not an error to suppress. The ACC post-run mix trips it because steps
and letters are not the same quantity, and the correct reading is that they
should not be summed.

**The recipe round trip.** Every mixable run emits a
`compound-eye-mixer-recipe-v1`, and the recorder immediately reads it back and
re-mixes. `roundtrip_ok: false` means the run does not replay, and
`--check` fails the whole ledger on it.

**Declared context.** The frozen dataset schema already demands `object_id`,
`model_id`, `coordinate`, `x_unit` and `source_stage`. Nothing enters the
ledger without saying what it is a measurement *of*.

## Evidence and status

Same vocabulary as `research/acc/dag/schema.md`, so one claim language covers
the repository. `source_stage` in the mixer context carries the evidence class.

| evidence | meaning |
| --- | --- |
| `exact-replay` | replayed under the official SAIR `ac-r2-v1` kernel |
| `computation` | produced by our own code; reproducible via `reproduce` |
| `repo-provenance` | a git object, hash or file at a named commit |
| `external-source` | asserted by a source outside this project |
| `none` | assertion with no attached evidence |

`status` is orthogonal: `verified`, `refuted`, `open`, `blocked`.

## The honest boundary

**Not every piece of work is numeric channels on a common coordinate.** A run
with no channels is recorded with `mixable: false`, no traces file and no
fabricated coordinate. Inventing a coordinate so that something becomes
mixable would be the same error as fitting a pairing after seeing the outcome:
it manufactures a signal rather than measuring one. Four of the seven backfilled
runs are claim-only, and they are no less part of the record for it.

## Fields

    schema            compound-eye-run-ledger-v1
    recorded_utc      ISO-8601
    lane              acc | lean | frontiermath | ...
    run_id            stable slug, unique within the lane
    claim             one falsifiable sentence
    status            verified | refuted | open | blocked
    evidence          class from the table above
    reproduce         exact command that regenerates the run
    caveat            what this run explicitly does NOT establish
    depends_on        list of "lane/run_id" this rests on
    supersedes        the run this replaces, required to re-record an id
    source            {repo, commit, path}
    observed          structured payload
    mixable           whether numeric channels exist

Mixable runs additionally carry `traces_path`, `recipe_path`, `channel_count`,
`coordinate`, `x_unit`, `points`, `units_commensurable`, `unit_guard_message`,
`normalization`, `active_channels`, `rms_combined`, `rms_residual`, `missing`
and `roundtrip_ok`.

## Invariants enforced by `--check`

1. a run id is recorded once per lane unless it carries `supersedes`;
2. `status` and `evidence` are from the vocabularies above;
3. `status: verified` requires evidence stronger than `none`;
4. every `depends_on` target exists in the ledger;
5. a mixable run has a traces file, and it exists on disk;
6. a mixable run's recipe replays to the same combined array.

## Use

    node tools/acc/mixer_log_v1.js record <run.json>
    python3 tools/acc/mixer_trace_v1.py --check
    python3 tools/acc/mixer_trace_v1.py --summary
    python3 tools/acc/mixer_trace_v1.py --blocked
    python3 tools/acc/mixer_trace_v1.py --trace <run_id>
    python3 tools/acc/mixer_trace_v1.py --weak
