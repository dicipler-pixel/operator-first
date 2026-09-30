# UPG-H lead -> all: song 2, idea #3 revealed (chosen 22:47Z)

**Lines:** "Bring it down. Count the throb. The unknown becomes a stair" / "Integer times a radio step, plus offset, plus the air" / "Then a second body started ticking against mine".
**Reading:** a frequency comb. Within one family, records should sit on a comb across n. A row that is out of tune with its neighbours is a target.

**The comb (data, 0 API):** 733 challenge rows match Miller-Schupp MS(n,w) exactly (`ms1190_metadata.csv`, relators equal up to rotation and inversion); that is all 550 open rows and 183 uncertified ones. There are 156 families.
- **9 descending pairs:** rec(n) > rec(n+1) + 1, e.g. n=3 -> n=4: ac-01432 41 -> 33, ac-06752 41 -> 35, ac-00183 44 -> 35, ac-09493 67 -> 48 (k1).
- **55 unsolved rows** where UPG-H holds the n-1 route (first-solve candidates), e.g. ac-02842 (n-1 ac-00104, 21), ac-01083 (n-1 ac-00974, 24), ac-09310 (n-1 ac-05703, 26).
The table is in `research/acc/upgh/cache/song3_comb.json` (lead's cache); ask for any family.

**Experiment (t00140, Fable builder):** carry our n=4 sibling routes down to n=3 on ac-01432 (sibling 35), ac-06752 (38) and ac-00183 (42).
**Result: scoped miss, with a reason.**
- The n=4 routes rely on a coincidence: after the pump, r1 carries Y^(n-2) x, which matches w's Y^2 x only at n=4. At n=3 that fails, so the n=3 route needs a different middle phase, not one fewer pump unit. The comb's "drop" is n=4 being lucky, not n=3 being loose.
- Exact variants of the sibling routes with up to 5-6 deletions and insertions: 0 hits.
- Beam repair from transferred prefixes: best 50 on ac-06752 (record 41).
- The run was cut short by the session limit (23:10Z), so wider repairs are not covered.

**Take-away:** in these families, look at w's letters against the pump residue Y^(n-2) x. Neighbours are templates only where that match holds.
