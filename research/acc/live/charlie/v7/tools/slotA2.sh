# SCRIPT: CHARLIE_SLOTA2 -- resume after the 13:58Z restart: batch 3 value rows from ac-02404 cap 31, surgery 43-56, kernel sweep
cd /home/claude/acc/charlie
TO=16 STOPST=300000000 MEM=2500 python3 easy_exact.py ac-02404:36:38:10 ac-04566:33:34:8 ac-05726:35:37:8 ac-03310:34:36:8 ac-05526:36:38:8 ac-06737:35:37:8 ac-08094:35:36:8 ac-03868:36:37:8
echo "== BATCH3 VALUE DONE $(date -u +%H:%MZ)"
MEM=2000 SURG_WORK=surgA python3 surgery.py CHARLIE_surgery_bundle_20260928T2335Z.txt 43 56
echo "== SURGERY 43-56 DONE $(date -u +%H:%MZ)"
MEM=2500 python3 kernel/kernel_sweep.py 0 4 >> kernel/sweep.out 2>&1
echo "== SLOTA2 DONE $(date -u +%H:%MZ)"
