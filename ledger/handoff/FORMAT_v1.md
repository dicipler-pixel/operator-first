# Sealed hand-offs — format v1

Four files were damaged crossing a boundary this session and the receiving side
had no way to know: an HTML file arrived 3,143 characters short, an image
arrived with a corrupted band, another arrived at 300x200, a zip was truncated.
None of those was a mathematical error. Each was a file moved without a
fingerprint.

A hand-off carries what was sent and what was claimed, and the receiver
recomputes both.

    handoff_id      sha256(producer|claim|artifact digest|sealed time)[:12]
    sealed_utc      when the envelope was made
    producer        gpt | claude | jeromie | sage | pari | magma | ci
    claim           the falsifiable sentence, written BEFORE the work
    claim_sha256    fixes that sentence; editing it afterwards is detectable
    artifact        {name, path, bytes, sha256}   — null for a row hand-off
    payload         the inline row, for hand-offs that move no file
    evidence        exact-replay | computation | repo-provenance | external-source | none
    verification    filled in by a second party, never by the producer

## Three mechanical refusals

| status | when |
| --- | --- |
| `damaged-in-transit` | byte count or digest differs; the message says how short |
| `claim-rewritten` | the claim no longer hashes to the digest sealed with it |
| `refused` | the checker is the producer — self-verification is not verification |

Any of them sets `result: fail` and a non-zero exit code.

## Rows, not files

Most hand-offs should move a row, not a payload. `row` seals a small inline
record with the same envelope around it; files move only when a row points at
one. That removes most of the transport surface and most of the manual relay.

## Use

    python3 tools/acc/handoff_v1.py row    --producer claude --claim "..." --evidence computation --data '{...}'
    python3 tools/acc/handoff_v1.py seal   path/to/file --producer claude --claim "..." --evidence computation
    python3 tools/acc/handoff_v1.py verify <handoff_id> --checker gpt [--file PATH]
    python3 tools/acc/handoff_v1.py list --open      # sealed, never independently checked
    python3 tools/acc/handoff_v1.py list --failed
