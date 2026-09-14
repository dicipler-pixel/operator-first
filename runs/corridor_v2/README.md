# corridor sweep v2 — raw hourly search records

One directory per UTC hour. `search.jsonl` holds every attempt made in that
hour, appended as it happened, never rewritten.

The eyes do not read this during the hour. At hour close each eye is spawned
as its own process and reads only its own projection of the hour; its reading
goes to the event ledger, not here. The hour is mixed only once it is closed.

Verdicts: `certificate` (re-verified by the official SAIR verifier, never a
re-implementation), `closed` (corridor exhausted — a bound, not a failure),
`budget` (stopped at the node cap — no information either way), `timeout`,
`skipped`.
