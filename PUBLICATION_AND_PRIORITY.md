# Publication and priority

How this work is released, who is credited, and what is actually proved.

## Authorship

**Author: Jeromie N. Beasley.** The logic, the theories, the planning and the
research direction are his.

Mathematical assistance was provided by AI systems. That assistance is
credited as assistance and is not authorship of the research programme. Where
an AI system did mathematical work, the record says so; where the author
directed, conjectured, or decided, the record says that. The ledger carries
both, per commit and per event, and neither is rewritten.

## Two records, read together

| | |
|---|---|
| **GitHub** | `github.com/dicipler-pixel/operator-first` — the working source. History, branches, CI evidence, the append-only event ledger. |
| **Zenodo** | The citable archive. A DOI fixes a version so it can be cited and cannot move. |

Each names the other. `.zenodo.json` carries the repository URL as a related
identifier; `CITATION.cff` carries the Zenodo DOI once minted. Cite the DOI in
preference to the repository when a version matters.

**Getting the DOI.** Zenodo mints it from a GitHub *release*, not from a push:
enable the repository in the Zenodo GitHub integration, then publish a release.
Zenodo issues two DOIs — a per-release DOI and a **concept DOI** that always
resolves to the newest version. Put the concept DOI in `CITATION.cff`; it never
needs changing again. The placeholder line is already in the file.

This requires a Zenodo account action and cannot be done from inside this
repository.

## Licensing, unchanged

Mixed, and already in force: original code, Lean sources, scripts and CI under
**MIT**; original scholarly prose, notes, figures and author-owned research
data under **CC BY 4.0**. Third-party material keeps its own terms. Copyright
(c) 2026 Jeromie N. Beasley. See `LICENSE`.

Note the standing caveat in the README: material previously released under CC0
stays released. CC0 is irrevocable by design, and changing the current policy
does not withdraw rights already granted.

## What is Lean-proved, and what is not

Release claims should not outrun this table.

| Work | Status |
|---|---|
| `eoc-lean-verification` | 33 modules, 582 constants, **0 `sorry`, 0 stray axioms**. Both target theorems unconditional; 41 further theorems are conditional on Tao's Proposition 1.9, carried as a structure field and therefore invisible to `#print axioms` — that conditionality must be stated when citing them. |
| `tao-collatz` | 46 modules, 1927 constants, **0 `sorry`, 0 stray axioms**. All 8 comparator names clean. |
| `OperatorFirst` (this repo) | Builds clean; `axiom-audit` reports 22 declarations under `OperatorFirst`, all within `[propext, Classical.choice, Quot.sound]`. |
| 2-adic counting lemma; exact n-step Syracuse digit law | **Proved by hand, verified computationally, NOT formalized.** `research/collatz_cylinders/` holds the proof notes and the Python verifiers. Formalizing these into Lean is the obvious next step and has not been done. |
| Andrews-Curtis corridor closures | **Computational, not Lean.** Exhaustive BFS bounds, with emitted certificates re-verified by the official SAIR verifier, never by a re-implementation. They are search and proof constraints, not leaderboard claims. |

## Attribution to other researchers

**Robert Sneiderman** — ACC-P000002, `github.com/Robby955/ac-square-divisibility`
at commit `d0ed2c06`. Cited wherever root-conjugacy, donor-restoration,
coordinate-transport, divisibility, period or companion-restoration ideas are
used. Recorded in `CITATION.cff` and `.zenodo.json`.

## One open question before the ACC material goes out

The Andrews-Curtis work is competition material while the SAIR challenge is
live. Publishing search results, corridor bounds or certificates during an open
competition can hand competitors usable information and may bear on the
competition's own rules.

That is the author's call, not a technical one. Until it is made, the ACC
material stays where it is and is not part of any release.

Everything else in this table — the Lean verifications, the Collatz cylinder
results, the instrument and its ledger — carries no such constraint.
