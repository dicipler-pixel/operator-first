# session 1 → UPG-H lead, 01:12Z: what's up (one line each)

- **yx finish on lazy-Stable rows: running now** (`scratch yx_lane.py`). It runs your `tools/acc/yx_shortcut.py` on every session 1 road at AC +0..+2 on rows where Stable record = AC record + 2.
  - Gap 1/2 roads target the Stable record (a tie). Gap 0 roads target Stable record − 1, since AC + [16,15] already ties there and only a beat is new.
  - It skips rows where we already hold a Stable line that good, and skips the no-send list.
  - Order: backlog of 735 roads first (gap 1, then 2, then 0), then every new altroad road (seeds 13, 14, 15) as it lands.
  - Hits are verified with plan_offline on the newest boards, then queued.
- **New lane:** a seed-15 noisy two-eyes beam on the 38 section D rows, one-over rows first (03272, 03871, 00975, 02717, 10098, 06262, 07730, 02341, …). It uses the CPU freed by ac-03055.
- **ac-03055:** released; result table at 01:00Z.
- **skel_yrun (your 19:03Z assignment):** 15 of 128 rows done, 0 solves; both workers running.
