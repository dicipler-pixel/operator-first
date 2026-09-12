# ACC knowledge DAG — node schema

A node records **one claim and the evidence class that backs it**. Nodes are
append-only; a superseded node is not edited or deleted, it gains a successor
that `supersedes` it. This is the shared state agents read before working and
write after working, replacing linear handoff prose.

The point of the `evidence` field is that a reader can tell, without rerunning
anything, how much weight a claim carries. Evidence classes, strongest first:

| class | meaning |
| --- | --- |
| `exact-replay` | replayed under the official SAIR `ac-r2-v1` kernel |
| `computation` | produced by our own code; reproducible via `reproduce` |
| `repo-provenance` | a git object, hash, or file that exists at a named commit |
| `external-source` | asserted by a source outside this project |
| `none` | assertion with no attached evidence — a hypothesis, not a result |

`status` is orthogonal to evidence: `verified`, `refuted`, `open`, `blocked`.
A `blocked` node names a missing artifact and must NOT be worked around by
reconstructing a substitute (AGENTS.md; ACC brief section 6).

## Required fields

    id             stable slug, unique
    kind           fact | question | experiment | blocker | method
    claim          one sentence, falsifiable
    status         verified | refuted | open | blocked
    evidence       one of the classes above
    recorded_utc   ISO-8601

## Optional fields

    depends_on     list of node ids this claim rests on (must exist; acyclic)
    supersedes     node id this replaces
    source         {repo, commit, path} provenance
    reproduce      exact command that regenerates `observed`
    observed       structured result payload
    caveat         what this node explicitly does NOT establish
    visibility     public | private  (private => summary only in this repo)

## Invariants enforced by `dag.py --check`

1. ids unique;
2. every `depends_on` / `supersedes` target exists;
3. the `depends_on` relation is acyclic;
4. `status: verified` requires `evidence` stronger than `none`;
5. `visibility: private` nodes carry no `observed` payload in this repo.

Invariant 5 is the public/private competition boundary: aggregate statistics
are public, per-challenge competitive intelligence is not.
