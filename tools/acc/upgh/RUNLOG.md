# UPG-H v2 run log

Short human notes on each working batch. The ledger (`research/acc/upgh/ledger.jsonl`) is the record; this file only points into it.

## 2026-09-30, first session

- `setup` → pins ok at `a0fd6e6`, T9 SHA-256 verified.
- `harvest` → 1,513 unique paths replayed twice, 554 best rows, 0 invalid, 0 disagreements.
- `board` → live AC and SAC boards, 152 submissions / 1,363 held rows.
- `plan` → 0 scoring lines (403 held, 151 behind; 51 of them within 3 moves).
- `run` → t00001 (code choice: sac-03272 and ac-04086, both k=1, 1 move behind; beam W=200000, seed 101, noise 2). In progress at this commit.
