---
name: upgh
description: Drive the UPG-H v2 harness (Claude edition) for the SAIR Andrews-Curtis Challenge. It checks health, pulls the live board read-only, harvests every path into the ledger, writes a send plan of the lines that score now, and runs bounded search, advisor and checker tasks. Code decides dispatch; subagents do the model work; the pinned official verifier certifies.
when_to_use: The user types /upgh, or asks to run, continue, check or stop the ACC harness, asks what scores right now, or asks to keep the ACC searches going.
argument-hint: "[status | plan | loop N | stop REASON]"
---

# UPG-H loop

The ledger `research/acc/upgh/ledger.jsonl` is the record. Every command below reads it or appends to it. Run commands from the repository root.

```
U="python3 tools/acc/upgh/upgh.py"
```

## 0. Health

`$U doctor`. Fix before anything else:
- `[licence] FAIL` or missing tools/T9: `$U setup --t9` (clones and pins the official verifier; building T9 takes about 3 minutes and 4.5 GB).
- `[Z] ledger unreadable`: stop and tell the user. Never hand-edit the ledger. `$U doctor --repair-tail` only moves a torn last line aside.

## 1. Present state

- If any board or history clock is stale (`$U status`): `$U board`. This is read-only.
- `$U harvest`. Always safe; it writes the ledger line for any path found in files (S4).
- `$U plan`. Show the user its lines, the points and the file path.

**Sending.** The user's standing rule (2026-09-30): send the team queue about every 40 minutes when it has lines. That is at most about 36 of the 40 daily submissions; never send more often than every 30 minutes. Use only `python3 tools/acc/sair_api.py send-queue --yes --force --lean`. It re-pulls the live board within 5 minutes, drops lines already sent (API history plus the local send log), and keeps only ties, beats and first solves. Never use `submit --yes` directly. With an empty queue, send nothing. Report every send: rows, lengths, live record and k.

## 2. Work loop (for `loop N`, or until the user's budget)

Repeat up to N times:

1. `$U --json next` returns `{task, role, token, contract, runner, agent}`, or `{"task": null}`. On null, stop and report.
2. If `runner` is `code`: `$U execute TASK TOKEN`. It heartbeats itself. For runs over two minutes, use `run_in_background`.
3. Otherwise dispatch the subagent named in `agent` (`upgh-builder`, `upgh-checker`, `upgh-advisor`, `upgh-memory`) with the Agent tool. Use this prompt: "Task contract: `<contract>`. Task id `<task>`. Lease token for heartbeats: `<token>`. Follow your role file. Return only the result JSON." Save its reply verbatim to `research/acc/upgh/tasks/<task>.result.json`, then run `$U accept TASK TOKEN research/acc/upgh/tasks/<task>.result.json`.
   If that agent type is not available (agent files added during a session load only in the next session), use `general-purpose` with the model from `tools/acc/upgh/config.json` `roles`, and tell it to read `.claude/agents/<agent>.md` and its role file first.
4. If `accept` rejects the result, show the error. Send the subagent one correction with the error text, then accept again. If it fails a second time, let the lease expire (`$U recover` marks it interrupted) and report it.

Independent tasks can run in parallel: several `execute` runs in the background, or several subagents in one message. Each task has its own lease.

## 3. After each batch

1. `$U doctor`, then `$U plan` if anything improved.
2. Commit `research/acc/upgh/` (ledger, plans, artifacts, harvest reports) and push to the working branch. The container is ephemeral, and an unpushed ledger is an unwritten Z.
3. Tell the user, in short plain words: what ran, each outcome (hit, improved, miss, refused), scoring lines, what is parked and what reopens it, and any advisor proposal with its discriminating test.

## Stop

When the user says stop, run `$U stop "<their words>"`. The stop persists: `next`, `run`, wakes and new tasks are refused, and the stop hook blocks search and submit commands. Recording results is still allowed. Only run `$U resume` when the user asks.

## Refusals are answers

A refusal (`[S2]` cosmetic switch or exact repeat, `[S3]` stale or disagreeing clocks, `[licence]`, `[stop]`) is written to the ledger and printed. Report it, and do the step it names (`upgh board`, ask the advisor, etc.). Never work around it.
