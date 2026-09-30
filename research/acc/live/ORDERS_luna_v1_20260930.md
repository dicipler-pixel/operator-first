# Luna v1 (2026-09-30): welcome to Mad Hatters, where to go, what to get, first job

Welcome, Luna. This page is everything you need to start. Read it top to bottom once, set up, pass the control, then take the first job.

## 1. What we are doing

**Mad Hatters** (team ACC01-T00051) competes in the **SAIR Andrews–Curtis Challenge** (Discovery Track). There are two boards,
**AC** and **Stable AC**, each with 10,115 rows (`ac-00001`…`ac-10115` and `sac-00001`…`sac-10115`). Each row is a balanced
presentation `<x, y | r0, r1>` of the trivial group. A solution is a list of move IDs that turns it into exactly `(x, y)` for AC
(IDs 0–13), or into the empty presentation for Stable AC (IDs 0–256; our Stable lines are usually the AC path + `[16, 15]`, or a
path to `(y, x)` + `[15, 15]`).

**Scoring:** on each row, the k teams tied at the shortest length each get 2^(1−k) points.
- A **beat** (shorter than the record): 1.0 point, whatever k was.
- A **tie**: 0.5 when k = 1, 0.25 at k = 2, 0.125 at k = 3, below 0.01 once k ≥ 8.

So we hunt beats, and ties on rows held by **few** teams (small k). A tie on a row with 12 teams is almost worthless.

## 2. Hard rules (no exceptions)

1. **Never submit and never call the SAIR API.** You never upload, and you never run `sair_api.py` send/boards/mine/check or
   anything that talks to `api.sair.foundation`. The team has 40 uploads a day in total and 360 API calls; session 2 sends
   once an hour.
2. **Never ask for, paste or store keys or tokens.**
3. **Never copy or use another team's solution paths.** Methods from papers are fine; paths from rivals are not.
4. **Never work on or send these rows** (the owner handles them): ac-09839, sac-02257, ac-09311, ac-06403, ac-04718, ac-05378.
5. **Every line you hand over must pass the official verifier** (SAIR repo at commit `a0fd6e6`, see §4).
6. Keep failed runs and negatives. A certificate like "no path ≤ N through cap C" saves the team from re-searching.

## 3. Where to go

| What | Where |
|---|---|
| **Team hub (Drive)**: orders, relays, your reports | **Mad Hatters ACC Shared Hub**: https://drive.google.com/drive/folders/1FKL3CsdhkxC6iSiV3YA7Hj5Cgk7eMP89 |
| **Team repo** (code, target lists, logs) | https://github.com/dicipler-pixel/operator-first, branch **`claude/gallant-bardeen-0pgpae`** |
| **Official SAIR repo** (rules, problems, verifier) | https://github.com/SAIRcompetition/Andrews-Curtis at commit **`a0fd6e6`** |

If you cannot read the team repo directly, ask Jeromie for a branch snapshot on the Drive hub (Kernel works this way).

**Read first (in the team repo, `research/acc/live/` unless noted):**
- `ORDERS_lowk_20260929T2345Z.md`: why the team only works rows with small k.
- `UPDATE_session2_to_kernel_git_20260930T0150Z.md`: **your first job's background** (the doubling family).
- `tools/acc/METHODS_PLAYBOOK.md`: what methods exist and what they found.
- `IDEAS.md` (newest entries at the bottom): what was tried last night, including the negatives.
- `SENT_ROWS.txt`: every row and length we have already sent. Don't redo these.
- Official rules: `SAIR/competition/rules/discovery.md`.

## 4. What to get (setup, once; fits in 8 GB RAM and about 2 GB disk)

```
git clone https://github.com/dicipler-pixel/operator-first && cd operator-first
git checkout claude/gallant-bardeen-0pgpae
git clone https://github.com/SAIRcompetition/Andrews-Curtis SAIR && (cd SAIR && git checkout a0fd6e6)
mkdir -p work bin
gcc -O3 -march=native -o bin/acc_beam   research/acc/optimality/acc_beam.c -lm
gcc -O3 -march=native -o bin/acc_window research/acc/optimality/acc_window.c
gcc -O3 -march=native -o work/acc_opt   research/acc/optimality/acc_opt.c -lm
work/acc_opt tball 8 40000000 work/T8.tab work/abc_t8   # 640 MB finishing table
sha256sum work/T8.tab   # must be 38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8
```
You need Python 3.10+ and gcc.

**Verifier check** (must print `accepted: true` and `ok: true` twice):
```
cd SAIR && PYTHONPATH=competition/tools python3 -m verifier \
  --manifest competition/examples/training_manifest.json \
  --submission competition/examples/sample_submission.txt --pretty; cd ..
```

## 5. Control run (do this before any real row)

The two-eyes beam on a known row must reproduce **AC 20 / Stable 22** on `ac-06015`:
```
echo '[{"id":"ac-06015","record":20,"k":1,"ac_record":20,"sac_record":22}]' > work/control.json
env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 \
  python3 research/acc/optimality/run_beam_raw.py SAIR/competition/tools/verifier/data/manifest.json \
  bin work/T8.tab work/w_control 20000 200 work/control_cap.jsonl work/control.json
```
Then put the returned `ac` path in `f.txt` as `ac-06015: [..]` and check it with the official verifier:
```
cd SAIR && PYTHONPATH=competition/tools python3 -m verifier \
  --manifest competition/tools/verifier/data/manifest.json --submission ../f.txt --pretty; cd ..
```
Report "control passed" (with the lengths) in your first note. If it fails, stop and say exactly what failed.

## 6. First job: the doubling family (36 rows, 23 of them held by one team)

**List:** `research/acc/live/targets_luna_msw_20260930.json`. These are rows `ac-…` in the Miller–Schupp family
MS_n(w\*), with w\* = b⁻¹aba⁻¹, for n = 3, 4, 5 (8 + 14 + 14 rows). Each entry has `n`, the AC and Stable `record` and `k`.

**Why this family:** its records **double with every step in n**: about 32–43 at n=3, 48–78 at n=4, 80–118 at n=5, 145–188 at
n=6, then 290, 550, 1,060 and 2,090 at n=10. That is record(n) ≈ 2·record(n−1) − 30, the signature of a recursive method that
uses the n−1 solution twice. **A method that grows more slowly beats every row from some n on**, at 1.0 point each on both
boards (92 rows per board in the whole family, n = 3..10). Nobody else on the team holds this job. Kernel is looking up the
published Lisitsa (2024) trivializations for the same family; Git has seen a "pulse" pattern in a sister family.

**Step A: routes for n = 3 and n = 4** (22 rows). Run the beam on these rows, one at a time (resumable):
```
python3 -c "import json;T=json.load(open('research/acc/live/targets_luna_msw_20260930.json'));json.dump([t for t in T if t['n']<=4],open('work/luna34.json','w'))"
env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 \
  python3 research/acc/optimality/run_beam_raw.py SAIR/competition/tools/verifier/data/manifest.json \
  bin work/T8.tab work/w_luna 20000 600 work/luna34_cap.jsonl work/luna34.json
```
Each row prints a JSON line. `verdict` TIE or BEAT is a hit. Note every length you get, hit or not.

**Step B: find the structure.** Put your n=3 and n=4 routes for the **same** r0 side by side (for example ac-09243 at n=3 and
ac-04016 at n=4 both start `YXyXyx | Y…Xy…x`). Session 2's n=4 route on ac-04016 (71 moves) has a clear shape:
- a three-move pulse (`r1 ← r1·r0⁻¹`, conjugate r1 by y, conjugate r1 by x⁻¹) repeated about 12 times, growing r1 from 13 to 33 letters;
- one multiplication that collapses it;
- a tail that shrinks r0 by 2 letters per move.

Ask how each phase grows with n. If you can write a route for general n whose length grows slower than doubling, build it for
n = 5 and 6, verify it, and compare it with the records.

**Step C: n = 5.** We hold **no** route on any n = 5 row. Run the same beam on the n = 5 rows (DMAX = record + 2), and try your
Step B construction there. Any verified n=5 route at or under its record scores.

**Report after each step**, even if everything is negative: lengths per row, the per-n growth you see, and any construction.

**Fallback** (if the family stalls): `research/acc/live/targets_luna_midk_20260930.json`, 55 rows held by 4–6 teams where we
already sit 1–4 moves over the record (a tie is worth 0.03–0.06). Same beam command, one row at a time.

## 7. How to hand results over

- **Lines:** one per path, `ac-NNNNN: [m1,m2,...]` (and `sac-NNNNN: [...]` for Stable). Every line official-verified.
- **Where:** a file named `<UTC>_luna_<rows>.txt` in the Drive hub (or `research/acc/live/inbox/` if you have push access; then
  commit, pull and push at once). Put a `#` comment line above each row: row, length, record, k, how you found it.
- **Your log:** keep `research/acc/live/WORKING_luna.md` (or `WORKING_luna.md` on the Drive hub): one dated line per run:
  what ran, settings, result, and any certificate.
- **Timing:** session 2 sends once an hour at **:25**. Get lines in by **:20** to make that hour's send. Session 2 re-verifies,
  checks the live board and drops anything already sent or no longer scoring. You never submit.

## 8. Who does what (don't duplicate)

| Who | Working on |
|---|---|
| Session 2 (lead) | hourly sends and 30-minute pulls; beat hunts on rows we hold with k 2–8; k4–6 road DP; trace-chain A/B; (y,x) Stable restarts |
| Session 1 | loose road-keeping DP on the 67 low-k rows (`targets_lowk_20260929T2345Z.json`) |
| Git (session 3) | "eyes" and pulse patterns; unsolved-row structure |
| Kernel | MS families on its unsolved rows 101–213; Lisitsa lengths for MS_n(w\*) |
| Charlie | exact ladder, batch 6 (15 low-k rows near start) |
| Bob | shortening our best paths (DP / window) |
| **Luna** | **MS_n(w\*) doubling family, n = 3..5 → general n** (this page) |

Questions go through Jeromie, or into a note on the Drive hub named `UPDATE_luna_to_session2_<UTC>.md`.
