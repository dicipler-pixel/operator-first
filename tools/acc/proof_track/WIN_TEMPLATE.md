# WIN: <row> — <our length> beats <old record> (<date> UTC)

Copy to `WIN_<row>_<YYYYMMDD>.md` for every 1-point result (beat, or a row we hold alone).
Fill every field; a win without reproduction steps doesn't count as documented.

## Result
- Row: `<ac-/sac-XXXXX>`. Start relators: `r0 = [...]`, `r1 = [...]` (manifest, commit a0fd6e6).
- Live record before: <length>, k = <teams> (board `generatedAt` <time>).
- Ours: <length> moves. Submission id <id>, accepted <time>. Board after: <length>, k = <teams>.
- Line: `<row>: [<moves>]`
- Official verifier: accepted, length <n> (command and output below).

## How we got it
- Method: <H-beam / seeded restart / capped BFS / window / splice / helper AI / other>.
- Exact parameters: <W, DMAX, BEAM_* env, seed, noise, caps, budget>.
- Wall time and machine: <minutes, cores, RAM>.
- Why it worked here (one or two sentences): <e.g. the record path climbs to total length N;
  cap N+1 found it>.
- Helper credit: <which helper / human idea, if any>.

## Reproduce
```
<exact commands from a fresh clone, including T9 build and the search command>
```
- Tool commit: `<git hash of the search code used>`. Result commit: `<git hash of the line>`.

## What we learned
- <what to try on similar rows; add a line to METHODS_PLAYBOOK.md>
