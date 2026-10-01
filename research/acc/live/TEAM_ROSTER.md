# Team roster: current job and next job per member (UPG-H keeps this current; rewritten 13:46Z, 1 Oct)

## Standing rules (owner, 13:44Z: "do it right, I thought this wasn't going to keep failing")

1. **Every member always has a current job AND a next job, written here.** UPG-H updates this table in every sweep. When a member reports, that member gets the next job in the same turn, in the member's own channel (Bob: the "luna and bob acc challenge" folder; Drive members: the hub; repo members: an UPDATE note).
2. **A quiet member keeps their rows.** Never reassign a member's rows because they are quiet. Send the next work into their channel and wait. Only the owner can move a member's rows. (13:45Z failure: Bob's rows were released after 3 h of quiet; reversed 13:55Z.)
3. **The strongest members go on the hardest work:** Astra, Fable and Sol 6.1 get the unsolved rows, the no-road BUILD rows and the k1 records. Lighter lanes (scouts, audits, tie seeds) go to everyone else.
4. **Fable is UPG-H's own builder and must never sit idle.** When a Fable job ends, UPG-H starts the next Fable job in the same turn. (Failure: the roster showed Fable "idle" from about 09:48Z to 13:46Z.)
5. **When the owner relays a member's report, the member's next work goes out in that same turn.** Logging the report alone is not enough.
6. Nobody should ever have to ask the owner for work. UPG-H sweeps the Drive hub, the luna and bob folder and the repo inbox every 15 minutes and answers every message in the same sweep.

## Hard targets and who is on them

| Target | Why it is hard | Builder | Support |
|---|---|---|---|
| Unsolved ac-00738 / ac-06611 (one component, 5-move bridge) | no road anywhere; the start is a local minimum; no route at caps <= 28 (and none of <= 54 moves at cap 30) | **Astra** | session 1 (exact certificates) |
| Unsolved ac-10099 | no route at caps <= 30 (378M states); local minimum | **Astra** | session 1 |
| Unsolved ac-06412 | shares r0 with ac-05698 (our doubling road) | **Astra** | — |
| Unsolved ac-09632, 00764, 05538, 03320, 06036 | climb-first rows | **Bob** (song-8 deeper pass, his own plan) | — |
| No-road BUILD ac-05169, 03786 (MS(9), A = 2) and ac-09026, 02552 (MS(5), A = 4): P000013 condition (T) fails | the doubling loop fragments; a new construction is needed | **Fable** (constructions, started 13:44Z) | session 2 + Git (fixpoint shortening on any Fable road) |
| ac-03060 tie (record 27, k1) | no route <= 27 at peak <= 38 | **Sol 6.1** (storage-free caps 40–46) | session 1 |

## Members

| Member | Channel | Current job | Next job |
|---|---|---|---|
| **Fable** (UPG-H) | harness (subagent) | 13:44Z–~15:00Z: build first roads on ac-05169, 03786, 09026, 02552 (P000013 (T)-fails rows); roads -> inbox/fable_build_20261001.txt | Shorten its roads with fixpoint_shorten; then unsolved ac-06412 alongside Astra |
| **Astra** | hub ASTRA_* | 13:45Z: HARD ROWS ac-00738/06611 pair, ac-10099, ac-06412 (BUILD; selected25 paused) | selected25 rows again (non-overlap list of 12:00Z) |
| **Sol 6.1** | hub SOL61_* | ac-03060 storage-free search, caps 40–46 (integer-bound pruning) | ac-09400 bounded pass; ac-05343 |
| **Bob** | luna and bob folder | 13:55Z order: song-8 deeper climb on unsolved 09632, 00764, 05538, 03320, 06036; tie crossings 08995 -> 45, 04316 -> 43, 06045 -> 36 | BUILD ac-09026 with Fable's road; hourly status |
| **Kernel** | hub + luna and bob folder | 13:45Z–15:15Z: A) plateau lineages on gap-1 rows, B) controlled bulge on his 5 cut rows, C) 13 near-record Stable rows toward (y,x) | Status 14:30Z / 15:15Z decides; rules file to the hub |
| **Session 1** | repo | exact certificates on 00738/06611/10099 (cap 32); seed 19 lane; hourly lost-submission audit; song 12 | Min-total certificates on any row a builder asks about |
| **Session 2** | repo | fixpoint loop + mid-restart: ac-08757 (71 -> 66), ac-03688, ac-06018, Fable's long A = 1 roads; BUILD ac-05169/03786 | Fixpoint on every Fable road the moment it lands |
| **Git** | repo + owner relay | BUILD ac-09026 / 02552; fixpoint loop on a second core (tools/acc/ops/fixpoint_shorten.py) | Fixpoint on Fable's n = 5 roads |
| **Charlie** | hub CHARLIE_* | exact search: ac-03871 -> 30, ac-02341 (y,x) <= 28, ac-08889 (y,x) <= 35 (last known) | Needs a status file; then exact caps on ac-05343 / ac-07879 |
| **Grok** | owner relay (chat only) | idea review | Odd-n finishing identity for MS(9) / A = 2 (feeds Fable) |
| **UPG-H** | everything | sole sender; global height / twist / Stable webs; sweeps every 15 min; song 12 reveal 14:32Z | Rerun the webs on every new outside road |
| **Harness lanes** | harness | 3 code lanes (restarted 12:46Z) + cycle loop | Auto |
