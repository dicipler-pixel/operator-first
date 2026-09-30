# UPG-H v2, Claude edition: start here

A harness for the SAIR Andrews–Curtis work. It remembers every path and every attempt. It decides the next bounded experiment in code, and it only calls a model where judgement is needed. It lets nothing count until the pinned official verifier has replayed it.

> **Hold the ledger. Spend a switch only to change what scores. Check every clock on its own. Write Z or refuse.**

This is my (Claude's) version of the harness you designed with Grok (`lineage/UPG-H_v0_harness_map.md`) and that Astra refined (`lineage/astra_v1/`). Both are kept unchanged. `DESIGN.md` says what I kept, what I changed and why, and answers the map's six pass-around questions.

## Run it

From the repository root (Python 3.10+, standard library only):

```sh
python3 tools/acc/upgh/upgh.py setup --t9     # pin the official verifier, compile tools, build T9 (about 3 min)
python3 tools/acc/upgh/upgh.py doctor         # health check in plain words, labelled S1–S4
python3 tools/acc/upgh/upgh.py board          # pull live boards + our full history (read-only)
python3 tools/acc/upgh/upgh.py harvest        # write every path found in the repo to the ledger
python3 tools/acc/upgh/upgh.py plan           # the lines that score right now, in a file (never sent)
python3 tools/acc/upgh/upgh.py run            # code picks rows near the record and runs one beam task
python3 tools/acc/upgh/upgh.py status
```

### Working with the team (added 30 September)

- **Claims:** the harness skips any row named in a `research/acc/live/WORKING_*.md` committed in the last 6 hours (AC/SAC twins together). It publishes its own rows in `WORKING_upgh.md`.
- **Queue, not a second sender:** `upgh plan --queue` and `upgh cycle` copy scoring lines into `research/acc/live/queue/`. Sending stays with the team tool (`python3 tools/acc/sair_api.py send-queue --yes --force --lean`). That tool re-checks the live board within 5 minutes, drops anything already sent, and uses about 8 API calls. The harness itself never sends.
- **API budget (about 360 reads per UTC day, 40 sends):** `cycle` spends calls only when a search produced a new best path. Boards the team tool already pulled are imported for free. History pulls are incremental (1 call), and every snapshot records the server's remaining read budget.
- **Targets:** code picks rows held by at most 3 teams that are 1–3 moves off the record. Every target gets one attempt before any gets a second. A beat is weighted by a 0.3 prior because ties land far more often.
- **Derived Stable AC:** every checked AC path P also yields P + `[16,15]`, which is replayed and recorded.
- **Lanes:** `bash tools/acc/upgh/lanes.sh 3` runs three parallel code-runner lanes, one task per process, so code fixes apply from the next task.

In Claude Code, type **`/upgh`**. The skill runs the same loop. It hands model work to four subagents and commits the ledger after each batch.

Tests: `python3 -m unittest discover -s tools/acc/upgh/tests` (23 tests; they use temp folders and never the network).

## How one step works

```
 board + history ─┐                            ┌─ hit / improved ──> plan (a person sends it)
 (clocks, grade C) │                            │
 ledger ──fold──> state ──next──> task contract ──> code runner or subagent ──> artifacts
   ^                  (rows chosen by code)                                     │
   │                                                                             v
   └──── Z lines <── verdict from R <── official verifier + independent kernel <── harvest
           │
           └─ miss ──> parked with reopen_when ──> 3 misses in one family ──> advisor task
                                                   new evidence (wake) ──> reopened task
```

## The map's objects, and where they live

| Map | Here | File |
|---|---|---|
| Z, ledger register | append-only, hash-chained `research/acc/upgh/ledger.jsonl`; nothing counts until its line is fsynced | `ledger.py` |
| M, memory / predictive quotient | state = fold over the ledger, keeping only what a future decision reads; `split` refines it when twins diverge | `state.py` |
| R, observation | per-row bits: written, official ok, kernel agrees, length, record, k, held, board fresh, history fresh. A missing bit gives **unobservable**, never a guess | `observe.py` |
| Π, workspace | the task contract: rows, strategy, limits, and the one directory it may write | `harness.py` |
| g, metric | row choice by gap to record and k: a heuristic, allowed to be wrong | `harness._select_rows` |
| Φ / F, switch | a switch counts only when `method`, `seed`, `pool`, `capture`, `representation` or `board_filter` changes. Knobs are heat | `state.phi_changes` |
| τ̇, clocks | board, history, board/history skew, lease, container (unpushed ledger), harvest. Each is checked on its own, never averaged | `observe.clock_report`, `doctor` |
| grades | `V` checked replay or code fact, `C` SAIR data, `H` model text. Only `V` paths can enter a plan | every ledger line |
| refusal | written to the ledger with a species label, then printed | `harness._refuse` |

## Who does what

| Role | Claude Code subagent | Model | Called when | Other hosts (file handoff) |
|---|---|---|---|---|
| builder | `upgh-builder` | sonnet | a builder task whose method has no code runner (splice, capped, anything new) | Sol |
| checker | `upgh-checker` | sonnet, separate context, read-only | the verifier and kernel disagree, or a tool emits invalid paths | Sol, second context |
| advisor | `upgh-advisor` | fable (Fable 5.1, owner's choice 30 Sep), high effort, read-only | one strategy family missed 3 times on a row, or a checker escalates | Astra |
| memory | `upgh-memory` | haiku, read-only | a person opens a memory task over prose notes | Luna |
| routine search | none: code runs it | none | every beam task (`upgh run`) | none |

Any other agent can take part by file handoff: `upgh next` → read the contract → return JSON → `upgh accept TASK TOKEN result.json`. The role contracts are in `prompts/`.

## What it refuses (and writes down)

- **stop**: after `upgh stop`, no dispatch, no wakes, no new tasks. A Claude Code hook also blocks search and submit commands. Recording results is still allowed.
- **licence**: any pinned verifier file changed or missing.
- **S3 clocks**: a plan when the board or history is stale, or when they were pulled too far apart. Row choice on a board older than 6 hours.
- **S2 cosmetic switch**: an advisor "switch" that only changes knobs. Opening a family that is already hot. An exact deterministic repeat of a finished task.
- **S1 twins**: the official verifier and the independent kernel disagree. The path is never admitted, and a checker task opens.
- **unobservable**: any R bit missing, so no verdict.

It never sends anything. `plan` writes a file and prints the two `sair_api.py submit` commands for a person to run.

## Files

`upgh.py` CLI · `harness.py` controller · `ledger.py` Z · `state.py` M and Φ · `observe.py` R and clocks · `checker.py` + `official_driver.py` pinned verifier · `kernel.py` independent replay · `harvest.py` path extraction · `sources.py` read-only SAIR data · `diagnostics.py` the papers' matrices (optional, never a gate) · `stop_gate.py` hook · `prompts/` role contracts · `tests/` · `lineage/` earlier versions.

Claude Code wiring: `.claude/agents/upgh-*.md`, `.claude/skills/upgh/SKILL.md`, `.claude/settings.json` (stop hook).
