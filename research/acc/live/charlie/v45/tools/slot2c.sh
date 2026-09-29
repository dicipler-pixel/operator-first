# SCRIPT: CHARLIE_SLOT2C -- ac-06737 push at cap 31, then surgery line 16, then lines 21-56
cd /home/claude/acc/charlie
MEM=1500 MAXST=200000000 python3 push06737.py
MEM=2000 SURG_WORK=surgA python3 surgery.py CHARLIE_surgery_bundle_20260928T2335Z.txt 16 16
MEM=2000 SURG_WORK=surgA python3 surgery.py CHARLIE_surgery_bundle_20260928T2335Z.txt 21 56
echo "== SLOT2C DONE $(date -u +%H:%MZ)"
