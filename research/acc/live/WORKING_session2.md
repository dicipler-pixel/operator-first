# Session 2 (lead, sender): live lanes (updated 2026-09-28 21:20Z, after a container restart)

**Running now (one beam per core):** mir (mirror twin, 120 rows), rk1 and rk2 (two eyes, ranked top 300; Astra runs rk2
from the bottom), yxl ((y,x) lane, one worker), esc2 (twins on near misses: gap 1-2 over, k <= 3, helpers' sweeps
included; replaces esc). **Stopped at the restart, not resumed:** p2v (299-row older ranking, 85 done), yxl2, solo
(1 path in 26 rows), k1p probe (0/12), ac-07790 mid-restart (session 3 owns the MS families). Their rows are free.

Current (skip these rows):
- **rk1 / rk2**: two-eyes beam on the top 300 dual+yx rows of TARGETS_RANKED (`$S/work/rk1_targets.json`, `rk2_targets.json`, 150 each).
- **p2v**: two-eyes beam, 299 rows.
- **(y,x) lane**: yxl (178 rows) + yxl2; long rows (SAC > 90) parked. Fable holds `targets_yx_fable_20260928.json`.
- **near_escalate**: every row 1 over a record with k <= 2 gets mirror twin (AC) and yx/yx2 twins (SAC).
- **ac-07790** (MCSC family, record 40): iterative mid-restart from our 45 path.
- **mir** (20:25Z): mirror twin (AC), 120 rows we are above, not in Codex's 80: ac-07601 ac-09141 ac-08221 ac-06540 ac-08923 ac-01304 ac-02404 ac-04067 ac-04735 ac-06016 ac-07521 ac-08210 ac-09400 ac-09464 ac-02893 ac-07404 ac-01521 ac-02561 ac-04094 ac-06457 ac-07789 ac-00348 ac-00712 ac-04469 ac-06239 ac-09317 ac-10040 ac-05134 ac-04428 ac-01626 ac-02026 ac-02491 ac-04316 ac-06790 ac-07287 ac-08141 ac-08793 ac-03364 ac-05545 ac-06207 ac-02353 ac-01562 ac-01971 ac-02514 ac-03186 ac-03977 ac-05125 ac-05467 ac-06058 ac-06552 ac-07439 ac-07674 ac-07792 ac-09067 ac-09254 ac-09631 ac-01850 ac-00587 ac-02827 ac-03975 ac-06095 ac-07233 ac-08274 ac-06695 ac-06872 ac-05441 ac-09365 ac-00126 ac-02381 ac-03564 ac-04081 ac-06208 ac-06768 ac-07046 ac-07137 ac-07467 ac-09116 ac-09562 ac-09628 ac-01472 ac-05526 ac-00989 ac-01056 ac-01106 ac-01349 ac-03310 ac-03925 ac-06814 ac-09944 ac-01847 ac-04198 ac-04981 ac-06250 ac-07486 ac-07667 ac-08586 ac-09873 ac-04431 ac-00317 ac-01430 ac-05124 ac-00261 ac-04404 ac-02453 ac-02456 ac-02518 ac-02685 ac-03172 ac-03885 ac-03923 ac-04389 ac-05321 ac-05348 ac-05964 ac-06087 ac-06189 ac-06306 ac-06578 ac-08903 ac-08956
- **solo** (20:35Z): two-eyes screen W=4000 on 42 solo-held (k=1) rows, record 42-49, never tried anywhere: ac-02072 ac-03913 ac-03967 ac-02603 ac-05146 ac-07481 ac-09608 ac-09609 ac-02171 ac-06793 ac-07675 ac-08601 ac-00087 ac-00334 ac-00831 ac-01533 ac-01591 ac-01686 ac-02195 ac-02908 ac-03038 ac-03556 ac-03664 ac-03848 ac-03966 ac-04365 ac-04871 ac-05206 ac-05310 ac-06227 ac-06268 ac-06424 ac-06543 ac-06553 ac-06765 ac-07380 ac-08012 ac-08591 ac-08599 ac-09047 ac-09561 ac-10080
- **k1p** (20:30Z): probe, 12 solo-held rows record 55-85 (W=2000): ac-01262 ac-08381 ac-06740 ac-03150 ac-05194 ac-02380 ac-04267 ac-08422 ac-05782 ac-03026 ac-01326 ac-07464
- Helpers' new slices (20:15Z): `ORDERS_helpers_20260928T2015Z.md` (Codex mirror, Luna yx2, Bob fresh dual).

---

# Rows the API session (session 2) is working on (updated 2026-09-27 23:58Z)

Exact capped sweeps (`run_capped_sweep.py`), AC and Stable AC together; every AC hit also yields AC + [16,15].
Session 1: skip these rows. Rows in `WORKING_session1.md` were removed from these lists.

## Sweep A: easy rows (1–2 teams, record ≤ 36), budget 180M states (46 rows)

ac/sac-03305 ac/sac-03060 ac/sac-03871 ac/sac-09312 ac/sac-00441 ac/sac-05343 ac/sac-07085 ac/sac-07476 ac/sac-08305 ac/sac-08428 ac/sac-09767 ac/sac-00126
ac/sac-04286 ac/sac-05149 ac/sac-05423 ac/sac-06768 ac/sac-08904 ac/sac-01104 ac/sac-02275 ac/sac-02386 ac/sac-02452 ac/sac-02925 ac/sac-03310 ac/sac-05818
ac/sac-06016 ac/sac-01349 ac/sac-01472 ac/sac-02962 ac/sac-04735 ac/sac-05726 ac/sac-06262 ac/sac-06737 ac/sac-07137 ac/sac-07492 ac/sac-08031 ac/sac-09390
ac/sac-09944 ac/sac-00989 ac/sac-02381 ac/sac-02404 ac/sac-04499 ac/sac-05526 ac/sac-06045 ac/sac-06814 ac/sac-07521 ac/sac-08210

## Sweep B: ac-00145 first, then records 33–40 held by 1–6 teams, budget 70M (309 rows)

ac/sac-00145 ac/sac-01304 ac/sac-08328 ac/sac-09464 ac/sac-06717 ac/sac-09400 ac/sac-05659 ac/sac-04699 ac/sac-01056 ac/sac-06019 ac/sac-07046 ac/sac-08649
ac/sac-01106 ac/sac-03925 ac/sac-05064 ac/sac-06888 ac/sac-08923 ac/sac-01638 ac/sac-02827 ac/sac-05598 ac/sac-08069 ac/sac-00171 ac/sac-00587 ac/sac-03834
ac/sac-03975 ac/sac-04939 ac/sac-07233 ac/sac-08274 ac/sac-08575 ac/sac-09883 ac/sac-10098 ac/sac-09562 ac/sac-03564 ac/sac-06969 ac/sac-07467 ac/sac-03774
ac/sac-06118 ac/sac-04460 ac/sac-06583 ac/sac-07165 ac/sac-04520 ac/sac-04921 ac/sac-05062 ac/sac-09776 ac/sac-00345 ac/sac-01198 ac/sac-01371 ac/sac-05273
ac/sac-01879 ac/sac-04101 ac/sac-06066 ac/sac-07709 ac/sac-01460 ac/sac-02988 ac/sac-06238 ac/sac-06921 ac/sac-09038 ac/sac-00822 ac/sac-05046 ac/sac-06908
ac/sac-07107 ac/sac-07155 ac/sac-00753 ac/sac-01729 ac/sac-03208 ac/sac-03762 ac/sac-04331 ac/sac-04922 ac/sac-05137 ac/sac-05467 ac/sac-05909 ac/sac-07439
ac/sac-07674 ac/sac-07792 ac/sac-09254 ac/sac-09910 ac/sac-00261 ac/sac-01562 ac/sac-01971 ac/sac-02514 ac/sac-03186 ac/sac-03696 ac/sac-03977 ac/sac-04404
ac/sac-05125 ac/sac-05452 ac/sac-06058 ac/sac-06552 ac/sac-09067 ac/sac-09631 ac/sac-09825 ac/sac-01655 ac/sac-02424 ac/sac-08634 ac/sac-07215 ac/sac-07879
ac/sac-04909 ac/sac-00232 ac/sac-00667 ac/sac-04133 ac/sac-09607 ac/sac-04382 ac/sac-05540 ac/sac-09423 ac/sac-02749 ac/sac-08900 ac/sac-09344 ac/sac-00009
ac/sac-06898 ac/sac-08377 ac/sac-01359 ac/sac-04282 ac/sac-00250 ac/sac-00980 ac/sac-01343 ac/sac-04535 ac/sac-05531 ac/sac-06299 ac/sac-09586 ac/sac-03064
ac/sac-05458 ac/sac-05955 ac/sac-08255 ac/sac-01880 ac/sac-05373 ac/sac-06069 ac/sac-07649 ac/sac-08402 ac/sac-09758 ac/sac-00576 ac/sac-01754 ac/sac-02368
ac/sac-02420 ac/sac-07985 ac/sac-08811 ac/sac-09323 ac/sac-00003 ac/sac-02022 ac/sac-02343 ac/sac-04755 ac/sac-05141 ac/sac-05709 ac/sac-06032 ac/sac-06597
ac/sac-07596 ac/sac-08158 ac/sac-09211 ac/sac-03057 ac/sac-09963 ac/sac-01247 ac/sac-05701 ac/sac-06168 ac/sac-08366 ac/sac-02079 ac/sac-03875 ac/sac-04963
ac/sac-09691 ac/sac-00242 ac/sac-01819 ac/sac-07269 ac/sac-07346 ac/sac-08150 ac/sac-04692 ac/sac-05759 ac/sac-01333 ac/sac-02445 ac/sac-03257 ac/sac-05255
ac/sac-00147 ac/sac-01561 ac/sac-02406 ac/sac-03534 ac/sac-04225 ac/sac-05438 ac/sac-08206 ac/sac-00252 ac/sac-01233 ac/sac-04251 ac/sac-04327 ac/sac-05031
ac/sac-06722 ac/sac-07348 ac/sac-02215 ac/sac-03704 ac/sac-07433 ac/sac-09905 ac/sac-00428 ac/sac-01136 ac/sac-03217 ac/sac-03517 ac/sac-04780 ac/sac-05869
ac/sac-06296 ac/sac-07564 ac/sac-07992 ac/sac-08136 ac/sac-08262 ac/sac-08858 ac/sac-00594 ac/sac-00820 ac/sac-01544 ac/sac-01570 ac/sac-02357 ac/sac-02969
ac/sac-04817 ac/sac-05078 ac/sac-05658 ac/sac-06147 ac/sac-07007 ac/sac-07373 ac/sac-07718 ac/sac-08106 ac/sac-07977 ac/sac-01239 ac/sac-05407 ac/sac-09100
ac/sac-07108 ac/sac-07088 ac/sac-08901 ac/sac-10101 ac/sac-04673 ac/sac-04842 ac/sac-06024 ac/sac-06913 ac/sac-08252 ac/sac-01285 ac/sac-02467 ac/sac-04749
ac/sac-05549 ac/sac-06895 ac/sac-07372 ac/sac-08519 ac/sac-00658 ac/sac-03700 ac/sac-06212 ac/sac-07083 ac/sac-09874 ac/sac-02483 ac/sac-03419 ac/sac-06762
ac/sac-06329 ac/sac-07306 ac/sac-07310 ac/sac-08696 ac/sac-00818 ac/sac-02240 ac/sac-03313 ac/sac-04417 ac/sac-04628 ac/sac-06732 ac/sac-07057 ac/sac-07710
ac/sac-07876 ac/sac-08542 ac/sac-08840 ac/sac-00582 ac/sac-00669 ac/sac-00986 ac/sac-01260 ac/sac-01914 ac/sac-02943 ac/sac-04435 ac/sac-04603 ac/sac-04674
ac/sac-05573 ac/sac-05600 ac/sac-05840 ac/sac-06230 ac/sac-07504 ac/sac-07980 ac/sac-00826 ac/sac-03040 ac/sac-07469 ac/sac-08350 ac/sac-08510 ac/sac-09089
ac/sac-01089 ac/sac-03895 ac/sac-07065 ac/sac-08883 ac/sac-09835 ac/sac-09909 ac/sac-01823 ac/sac-04483 ac/sac-08051 ac/sac-08624 ac/sac-09727 ac/sac-08311
ac/sac-09125 ac/sac-03167 ac/sac-04789 ac/sac-07794 ac/sac-07900 ac/sac-01611 ac/sac-02294 ac/sac-04015 ac/sac-04050 ac/sac-04256 ac/sac-04542 ac/sac-05702
ac/sac-06091 ac/sac-07136 ac/sac-00575 ac/sac-01376 ac/sac-01843 ac/sac-03371 ac/sac-05418 ac/sac-08737 ac/sac-08803

## Sweep C: records 25–32 held by 1–6 teams, cheapest first, budget 25M (77 rows)

ac/sac-01629 ac/sac-07186 ac/sac-04346 ac/sac-05558 ac/sac-07188 ac/sac-01443 ac/sac-03799 ac/sac-07435 ac/sac-09763 ac/sac-02153 ac/sac-02583 ac/sac-05506
ac/sac-06590 ac/sac-09212 ac/sac-05612 ac/sac-02016 ac/sac-07789 ac/sac-01850 ac/sac-07141 ac/sac-09365 ac/sac-09091 ac/sac-00697 ac/sac-03339 ac/sac-03514
ac/sac-04612 ac/sac-04633 ac/sac-01521 ac/sac-02561 ac/sac-02612 ac/sac-04094 ac/sac-06457 ac/sac-00513 ac/sac-00828 ac/sac-05456 ac/sac-01079 ac/sac-02076
ac/sac-06690 ac/sac-07693 ac/sac-04195 ac/sac-09189 ac/sac-09507 ac/sac-00135 ac/sac-05521 ac/sac-00367 ac/sac-04235 ac/sac-08886 ac/sac-01770 ac/sac-08201
ac/sac-01637 ac/sac-02302 ac/sac-00037 ac/sac-01762 ac/sac-04547 ac/sac-02902 ac/sac-07548 ac/sac-07893 ac/sac-02574 ac/sac-05461 ac/sac-00581 ac/sac-02882
ac/sac-03100 ac/sac-04211 ac/sac-09243 ac/sac-02756 ac/sac-07681 ac/sac-09328 ac/sac-00217 ac/sac-01461 ac/sac-04276 ac/sac-05542 ac/sac-07569 ac/sac-08221
ac/sac-07450 ac/sac-07267 ac/sac-00797 ac/sac-02007 ac/sac-09576
