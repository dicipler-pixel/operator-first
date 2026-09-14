# Compound Eye — build lineage and regression matrix

**GENERATED — do not hand-edit.** Regenerate with
`python3 tools/acc/lineage_v1.py --write`; CI may assert freshness with `--check`.

A hand-typed lineage launders an assertion into a fact. Every row below names
where it came from. Where two eyes disagree about a build, both are printed and
the contradiction is named; this table never silently picks a winner.

## 1. Chronological lineage

Frozen instrument manifest reports release **3.2**, built from source releases **2.2, 3.1**.
Manifest scope, in its own words: *File identity, not scientific certification.*

| build | evidence it exists |
|---|---|
| `Eye Mixer 1.0` | string present in the frozen instrument tree |
| `Eye Mixer 1.0.0` | string present in the frozen instrument tree |
| `Universal 2.0` | string present in the frozen instrument tree |
| `Universal 2.1` | string present in the frozen instrument tree |
| `Universal 2.2` | string present in the frozen instrument tree |
| `Universal 3.0` | string present in the frozen instrument tree |
| `Universal 3.1` | string present in the frozen instrument tree |
| `Universal 3.2` | string present in the frozen instrument tree |

Content hashes recorded at import validation (the package itself is a private
working instrument and is deliberately not committed):

| artifact | sha256 |
|---|---|
| `Compound_Eye_Matrix_Mixer_Canonical_5_1.html` | `1084ded507fc76f161fbc78b63b03f5597c8b0cfbf8718a68b80bafdf2744250` |
| `Compound_Eye_Matrix_Mixer_Canonical_5_1.zip` | `961d6bae24a54638b16a70e8c41a38676d9ab9513e7cc99ed286ad35c84af7a5` |

## 2. Capability regression matrix

Rows are capability claims about the pre-ledger builds, taken verbatim from the
event stream. `state` is the eye's own recorded state — a contradicted eye keeps
its observation, it is not deleted.

| seq | eye | state | claim | basis |
|---|---|---|---|---|
| 2272 | `claude-build-assessment` | observed | lacked relationship mixing, prediction comparison, replay, failure preservation and what-next logic; these were gaps the | inferred from a version table and from Universal 3.2 having no durable browser event history |
| 2273 | `jeromie-reaudit` | observed | already contained relationship mixing, prediction, replay, failure preservation and what-next logic; what they lacked wa | independently reran the distinct builds; Canonical 5.1 validated all ten studies, recipe-round-tripped, all-off gave exa |

### Open contradictions

- **contradiction:claude-build-assessment-vs-jeromie-reaudit** (seq 2274) — disagreement on *capabilities of the pre-ledger Compound Eye builds*; resolved: **False**
  - `claude-build-assessment` (seq 2272): lacked relationship mixing, prediction, replay, failure preservation, what-next
  - `jeromie-reaudit` (seq 2273): already had all of those; lacked only permanent automatic memory
  - note: Jeromie's side carries the stronger evidence: he reran the builds and produced replay hashes, while my side was an inference from a version table. The filing records both, unedited. What survives from my side is narrower and still true: Canonical 5.1 keeps trials in RAM, does not record disabled eye

## 3. Recorder property matrix

Each property is paired with the test that tries to break it. A property with no
test is worth nothing, so the count of matching test references is shown.

| property | how it is enforced | test file | references |
|---|---|---|---|
| tamper-evident | hash chain; editing any event breaks every later link | `test_event_log_v1.py` | 1 |
| torn-write safe | one fsynced line under flock; a kill mid-append leaves a short line | `test_event_log_v1.py` | 8 |
| concurrent safe | appends take flock(LOCK_EX); writers interleave records not bytes | `test_event_log_v1.py` | 3 |
| exactly typed | unsafe integers rejected recursively over the whole event | `test_event_log_v1.py` | 4 |

## 4. Provenance of this file

- repository HEAD at generation: `cfcc9a9`
- event stream length: 2394 events
- sources read: `tools/compound-eye/UNIVERSAL_MANIFEST.json`, the frozen instrument tree,
  `tools/acc/MIXER_5_1_IMPORT_VALIDATION.md`, `ledger/events/stream_v1.jsonl`
- the frozen instrument is READ ONLY here; nothing under `tools/compound-eye/` is written
