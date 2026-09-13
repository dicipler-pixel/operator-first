# Sealed hand-offs — format v2

v2 exists because review found three ways v1 could report a pass that meant
less than it looked like it meant.

## Transport and claim are different questions

v1 returned one `result`. For a hand-off with `artifact: null` that result was
reached by checking only that the claim string had not been rewritten — which
reads as verification and is not. v2 answers the two questions separately and
never merges them.

**Transport** — did exactly what was sealed arrive?

    transport_verified   true only if ALL of:
      * every artifact matches its sealed byte count and SHA-256
      * the artifact list matches the sealed manifest digest
        (so adding, dropping or swapping a file is caught, not just corrupting one)
      * any inline payload matches its canonical digest
      * the claim still hashes to the digest sealed with it
      * the checker is not the producer

**Claim** — is the sentence true? Never established by inspecting an envelope.

    claim_status   withheld   the default, and the only status `verify` can produce
                   open       attested, with no result either way
                   supports   requires an independently supplied result artifact
                   refutes    same

`attest` refuses a `supports` or `refutes` outcome unless a result artifact is
named, refuses a result produced by the same party that sealed the claim, and
refuses the producer as its own attester.

## Inline payloads are hashed

v1 stored `payload` and never hashed it, so a payload could be edited after
sealing and still verify. v2 hashes the **canonical** form — sorted keys, no
incidental whitespace — so the digest tracks the value rather than one
particular serialization. Two hand-offs with the same payload in different key
order produce the same digest; a single changed number does not.

## Exact integers, everywhere

v1 swept an eye's `output`. A number past 2^53 sitting in `x`, `values`, or any
other field went through unchecked and silently lost digits. v2 walks the entire
record and names the exact path it found:

    handoff: numbers past 2^53 lose digits in JSON; quote them as strings
             — payload.rows[0].D = -217541503961543485618350976479

## Fields

    schema           acc-handoff-v2
    handoff_id       sha256(producer|claim|manifest|payload digest|sealed time)[:12]
    producer         gpt | claude | jeromie | sage | pari | magma | ci
    claim            the falsifiable sentence, written BEFORE the work
    claim_sha256     fixes that sentence
    artifacts[]      {name, path, bytes, sha256} — a package, not one file
    manifest_sha256  over the sorted artifact list
    payload          inline row, for hand-offs that move no file
    payload_sha256   canonical digest of that payload
    evidence         exact-replay | computation | repo-provenance | external-source | none

## Use

    python3 tools/acc/handoff_v2.py seal <file>... --producer P --claim C --evidence E
    python3 tools/acc/handoff_v2.py row --producer P --claim C --evidence E --data '{...}'
    python3 tools/acc/handoff_v2.py verify <id> --checker Q [--file NAME=PATH]
    python3 tools/acc/handoff_v2.py verify-all --checker ci
    python3 tools/acc/handoff_v2.py attest <id> --checker Q --outcome O --evidence E --result <id>
    python3 tools/acc/handoff_v2.py list [--open] [--failed] [--withheld]

## Standing record

`765fad6d0206` seals the rank-9 computation package: seven files, manifest
`5b72c5ef…`. Those files are the instruments and the recorded observations.
They do **not** contain a rank-9 witness. No attestation is offered, so the
claim reads WITHHELD. Until exact class-group coordinates and the 3^9 = 19,683
independence sweep exist, the claim stays open and obstructed.
