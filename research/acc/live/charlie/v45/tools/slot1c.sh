# SCRIPT: CHARLIE_SLOT1C -- easy-row cap ladders resumed after the restore, then surgery lines 57-98
cd /home/claude/acc/charlie
TO=16 STOPST=300000000 MEM=2500 python3 easy_exact.py ac-01770:31::10 ac-09507:30::4 ac-08221:32:33:4 ac-06913:33::4 ac-07977:33::4
echo "== LADDER DONE $(date -u +%H:%MZ)"
MEM=2000 SURG_WORK=surgB python3 surgery.py CHARLIE_surgery_bundle_20260928T2335Z.txt 57 98
echo "== SLOT1C DONE $(date -u +%H:%MZ)"
