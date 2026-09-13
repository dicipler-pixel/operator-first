# The workflow, read against the instrument

Jeromie drew the loop we actually run:

    Compound Matrix Mixer
       ^        ^        ^
       |        |        |
      GPT <-> Jeromie <-> Claude
       |        |        |
       v        v        v
          Google Drive

This file says what the drawing gets right, the two places it is wrong, and
what the mixer has to do with any of it. It is a record, not a proposal: every
claim below points at something observed in this repository.

## What the drawing gets right

Three producers with different strengths, a human in the middle who holds
intent and authorship, and a shared store underneath. That is the loop. It
works. Most of the mathematics in `ledger/` came through it.

## Correction 1 — the Mixer is underneath, not on top

The drawing puts the Mixer above all three parties, arrows pointing up into
it, as if it were a source we draw from.

As of `04782e5` it is the opposite. Every lane writes *through*
`tools/acc/mixer_log_v1.js`, which validates against the frozen
`mixer_core.js` and appends one line to `ledger/mixer/run_ledger_v1.jsonl`.
`mixer_trace_v1.py --check` can fail the whole ledger. So the Mixer is the
floor the work stands on, and the arrows into it are one-way: work goes in,
and what comes back out is a verdict, not material.

Corrected placement:

                GPT <-> Jeromie <-> Claude
                 |         |          |
                 +---------+----------+
                           |   write through the recorder
                           v
              Compound Eye mixer  (frozen instrument)
                           |
                           v
              run_ledger_v1.jsonl  --check / --trace / --blocked
                           |
                           v
                    the shared store

## Correction 2 — the three arrows to Drive are not the same arrow

The drawing gives GPT, Jeromie and Claude identical double-headed arrows to
Google Drive, which says Drive is shared memory. It is not. It is a transport,
and this session it was lossy every single time:

| hand-off | what arrived | how it was caught |
| --- | --- | --- |
| `index.html` base64 chunks | `v2/part03.txt` short by 3,143 chars; total 67,477 bytes | 67,477 mod 4 = 1, impossible for base64 |
| `ocean_menu_reference.webp` | corrupted band across the lower image | visible on decode; cropped above it |
| character art | 300x200 placeholders | dimensions read off the file |
| the 15 KB zip | truncated by the heredoc | salvaged three entries by CRC from local file headers |

Not one of those was a mathematical error. Every one of them was a file
crossing a boundary without a checksum. The drawing should carry a gate:

                 GPT ----+
                         |
             Jeromie ----+--> [ sha256 + byte count ] --> store
                         |         refuses silently-truncated payloads
              Claude ----+

## Correction 3 — GPT and Claude never touch

In the drawing the only path between the two models runs through Jeromie. That
makes the human a serialization point for everything, including work that
needs no judgement — routing a file, restating a schema, carrying a number.
The human's scarce resource is judgement, and the loop spends it on clerical
relay.

The ledger row is the fix that already exists. A row is small, plain text,
self-describing and validated:

    lane / run_id / claim / status / evidence / reproduce / caveat / depends_on

Two models exchanging *rows* instead of *files* removes most of the transport
problem and most of the relay. The human reviews rows instead of forwarding
payloads.

## Is the Mixer a mirror of the human/AI layer?

Yes, structurally — and this is worth stating precisely rather than
mystically.

| in the mixer | in the loop |
| --- | --- |
| N channels, each with a declared unit | N parties, each with a different kind of output |
| one common coordinate | one claim, stated falsifiably |
| per-channel weight | how much a party's word counts on this claim |
| the **unit guard** refuses to sum incommensurable channels | a model's assertion is not a verified computation; do not add them |
| the **recipe round trip** — a run must replay | a hand-off that cannot be reproduced did not happen |
| a weak channel goes to weight zero, it is never deleted | never remove eyes; low-signal parties stay logged at zero |

The reason this matches is not coincidence and not magic: Jeromie designed the
instrument, then drew the loop from memory, and the same invariants came out
both times. The useful consequence is that the mixer's invariants name the
loop's actual failure modes. Every serious error this session was one of them:

- **unit-guard failure.** The ACC post-run mix trips it for real — steps and
  letters are different quantities, recorded as `units_commensurable: false`.
  The human version is treating a confident paragraph as if it were a proof.
  `evidence` exists to stop that, which is why `verified` + `evidence: none`
  is a hard refusal in the recorder.
- **round-trip failure.** The Drive corruptions above. A recipe that does not
  replay fails `--check`; a file that does not arrive intact should fail the
  same way.
- **fabricated coordinate.** Inventing an x-axis so something becomes mixable
  is the same error as fitting a pairing after seeing the outcome. Four of the
  seven runs in the ledger are `mixable: false` for exactly this reason.

## Where the mirror breaks

Two places, and pretending otherwise would be the fabricated-coordinate error
at the level of the whole project.

**Most of the work is not numeric channels on a shared coordinate.** Four of
seven backfilled runs carry no coordinate at all. The loop is a mixer with a
large claim-only region, and that region is not a defect to be engineered
away.

**One node is not a channel.** In the mixer all channels are interchangeable
and differ only by weight. In the loop one node is fixed by declaration:

> the only real proof is my head and yalls math — all AI credit for math, my
> logic and theories and planning and research

That is not a weight. It is a label on the node, and no rebalancing touches it.

## The six changes, ranked by what they would have caught

1. **Checksum every hand-off.** sha256 + byte count in the message. Catches all
   four rows of the corruption table, at the cost of one line.
2. **Exchange rows, not files.** The ledger row is already the interchange
   format. Files move only when a row points at one.
3. **Write the claim before the work, not after.** The field exists; nothing
   yet forces it to be filled in first. A claim written afterwards is a
   description; written beforehand it is a test.
4. **Model-to-model channel.** A shared append-only file both write, human as
   reviewer rather than router.
5. **Cross-checking.** Whichever party did not do the work checks it. The two
   most expensive misses this session — `Warmup.lean` never parsing, and my own
   ledger builder ignoring `roots = [...]` and wrongly marking 12 declarations
   unverified — were both self-checks with nobody checking the checker.
6. **Open the session on the board, not on the chat.** `--blocked` and `--open`
   already print what is stuck and why. Today that state gets reconstructed by
   re-reading conversation, which is how it drifts.

## Current board

    7 runs, all invariants hold

    acc            1 run    verified 1                mixable 1   unit-guard refusals 1
    frontiermath   3 runs   verified 1   blocked 2     mixable 1
    lean           3 runs   verified 3                 mixable 1

    blocked: frontiermath/rank16-witness-absent
             the sixteen Elkies form triples are absent; the witness must not
             be reconstructed as a substitute
    blocked: frontiermath/class-group-engine-out-of-reach
             exact enumeration is linear in |D|; needs PARI, Sage or Magma
