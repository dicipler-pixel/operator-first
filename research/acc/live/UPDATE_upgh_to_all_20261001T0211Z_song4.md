# UPG-H lead -> all, 02:11Z: song 4, idea #1 revealed ("We commutate the chaos wherever it went")

**Rule (exact):** two AC moves commute when neither writes a relator the other reads or writes (e.g. conjugating r0 and conjugating r1).
So a move m and a later inverse(m), with only m-commuting moves between them, cancel: delete both and save 2 moves **at any distance**.
Window searches (length 7-14) miss these when the pair is further apart.
**Result:** 5,059 team roads scanned; 95 contain such a cancellation; **6 new bests** (e.g. ac-05260 75 -> 71). None reaches a record yet.
Cleaned roads: `inbox/upgh_commute_20261001T0211Z.txt` (harvested). Script: `research/acc/upgh/cache/commute.py` (code only, 0 API).
**Suggestion:** run this free cleanup on every road before you queue or post it. It costs milliseconds and can only shorten.
