# Kernel priority run, 1 Oct 10:28Z–13:00Z (from Drive `kernel_priority_run_20261001.xlsx`, luna and bob folder; transcribed by UPG-H)

- **Scope:** the UPG-H priority list: 112 entries on 78 AC rows, plus 429 UPG-H routes (all replayed correctly on the official checker).
- **Searches:**
  - on all 78 rows: the radius-4 route-joining web to a fixpoint, plus a radius-7 goal ball at both finishes;
  - on gap-1 rows: radius-5 spine joins up to 10 moves (15 rows finished before 13:00Z).
- **Ties / beats: 0.** Kernel never submits.
- **Scope of the miss:** a tying route must leave every held route by 5+ moves somewhere in the middle. It has to be a new route, not a recombination.

## Shorter routes (official checker 5/5; none at record)

| Row | Team | New | Record | Still over |
|---|---|---|---|---|
| sac-04882 | 56 | 55 | 53 | 2 |
| ac-04882 | 54 | 53 | 51 | 2 |
| ac-04581 | 50 | 49 | 47 | 2 |
| sac-02962 | 40 | 39 | 37 | 2 |
| sac-04018 | 54 | 53 | 50 | 3 |

**Gap to record** after the rerun, over 112 entries: 1 move over → 32, 2 → 23, 3 → 33, 4 → 23, 6 → 1.

## Radius-5 gap-1 rows (every one = the radius-4 result)

| Row | AC rec | Stable rec | Best to (x,y) | Best to (y,x) |
|---|---|---|---|---|
| ac-00145 | 39 | – | 40 | 41 |
| ac-00678 | 41 | – | 42 | 43 |
| ac-00753 | 39 | 41 | 40 | 42 |
| ac-00975 | 34 | 36 | 35 | 35 |
| ac-02288 | – | 38 | 37 | 37 |
| ac-02528 | – | 36 | 35 | 35 |
| ac-03714 | 50 | 52 | 51 | 52 |
| ac-03871 | 30 | 32 | 31 | 31 |
| ac-04493 | – | 53 | 52 | 53 |
| ac-04699 | 37 | – | 38 | 38 |
| ac-05598 | 39 | – | 40 | 39 |
| ac-06045 | 36 | 38 | 37 | 38 |
| ac-06262 | – | 37 | 36 | 37 |
| ac-06768 | – | 34 | 34 | 33 |
| ac-06969 | 38 | 40 | 39 | 39 |

A Stable line = route + 2. Rows after ac-06969 were not reached before the 13:00Z cap.

**Songs:** song 9 missed (74,220 states, wall certified). Song 10: 2,482 rules and 20 shorter routes, none below the row's best. The SONG_IDEAS file has all 10.

**Corrections Kernel recorded himself:**
- The 09:40Z note: sac-01962 and sac-06225 were not new.
- The song-10 word count is 33,320.
- The first radius-5 version ran out of memory and was rebuilt (KERNEL-PRIO5-02).

**Next (UPG-H order, 13:27Z):** plateau search (length-neutral moves only) on the gap-1 rows after 06969 and on 13 near-record Stable rows, until 14:30Z.
