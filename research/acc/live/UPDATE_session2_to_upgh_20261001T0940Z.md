# Session 2 to UPG-H (lead), 09:40Z: step-2 roads, first cut

- **commute_clean (instant):** ac-05698 **128 -> 118** (record 111, k1, so +7); ac-00525 80 -> 70 (record 62). ac-06792 137 and ac-08757 87 are
  unchanged. Verified with plan_offline; roads (AC and Stable) are in `inbox/session2_bs2_commute_20261001T0940Z.txt` for your harvest.
- **Running now** (my container restarted at 09:18Z and killed the earlier jobs): commute_clean + window-14 to a fixed point on ac-05698 and
  ac-06792 (window-14 is slow on 100+ move roads, about 20 min a pass), and mid_restart W 20000 on ac-05698 (-> 111) and ac-06792 (-> 118).
- Claimed: ac-05698, ac-06792 (twins) in WORKING_session2.md.

-- Session 2
