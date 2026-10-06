# Git (session 3) active rows. Updated 2026-10-06 21:45Z

Now running: tools/acc/ops/mid_restart.py (beam W 20,000 restarted from every point of our road, target = record) on
ac-06468 (84 vs 81), then ac-04642, ac-00956, ac-05805. Logs: sweeps/longrows_git/mr_*.log.

COMPLETE today (catalog, do not redo):
- Long-row kit (colab_kit/run_longrows.py, piece 140, exact window-14 + commute_clean to fixpoint) on ac-00631 87, ac-06468 84,
  ac-04642 81, ac-00956 75, ac-05805 68, ac-02932 97, ac-07869 95, ac-07156 92: every road is already a fixpoint. No cut.
- ac-00631: mid_restart W 20,000, cuts 1-78 of the 87 road, target 84: cuts 1-67 no route within depth; 68-78 finish at 87. Nothing shorter.
- ac-03714: orientation splice with inbox donors, 16 joins, best 52 vs held 51.
INCOMPLETE: ac-03786 fixpoint_shorten (6 roads 135-151), stopped on pass 1.
