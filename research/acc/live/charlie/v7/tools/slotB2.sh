# SCRIPT: CHARLIE_SLOTB2 -- resume after the 13:58Z restart: batch 3 easy rows from ac-09857 cap 38, batch 2 rest, surgery 65-98
cd /home/claude/acc/charlie
TO=16 STOPST=300000000 MEM=2500 python3 easy_exact.py ac-09857:27:28:14 ac-05414:26:28:8 ac-09212:28:30:8 ac-08371:25:27:8
echo "== BATCH3 EASY DONE $(date -u +%H:%MZ)"
TO=14 STOPST=300000000 MEM=2500 python3 easy_exact.py ac-04282:35:37:8 ac-00737:34:35 ac-02467:35:37 ac-05821:35:37
echo "== BATCH2 REST DONE $(date -u +%H:%MZ)"
MEM=2000 SURG_WORK=surgB python3 surgery.py CHARLIE_surgery_bundle_20260928T2335Z.txt 65 98
echo "== SLOTB2 DONE $(date -u +%H:%MZ)"
