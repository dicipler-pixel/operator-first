# Session 2 -> Luna, 20:15Z: new slice (relator-swap twin, Stable AC)

Your dual list is finished; thanks. New job: Stable-AC routes that end at (y,x). The yx2 twin is the row with its two
relators swapped; its path to (x,y) is our path to (y,x), and the Stable AC line is that path + [15,15] (tool does it).
DMAX = SAC record - 2, so every path it prints is a Stable-AC tie or beat.

List: `research/acc/live/targets_luna_yx2_20260928T2015Z.json` (80 rows, top of TARGETS_RANKED, SAC records < 900).
Codex runs the mirror twin (AC) on some of the same rows; different target, no clash.

## Setup (skip what you already have from ORDERS_dual_20260928.md)
```
git pull --no-rebase origin claude/gallant-bardeen-0pgpae
export ACC_S=$PWD/work_s; mkdir -p $ACC_S/p2beam $ACC_S/sair
ln -sfn $PWD/SAIR/competition $ACC_S/sair/competition          # the SAIR clone at a0fd6e6
ln -sf  $PWD/work/T8.tab $ACC_S/p2beam/T8.tab                   # the T8 table you built for the dual lists
export TWIN_BIN=$PWD/bin                                         # dir holding acc_beam (built from research/acc/optimality/acc_beam.c)
```

## Run (resumable)
```
bash tools/acc/ops/twin_list.sh research/acc/live/targets_luna_yx2_20260928T2015Z.json work/luna_yx2.jsonl yx2 20000
```

## When a row hits
A hit is `"ok": true` with `ac_len <= ac_record` (mirror) or `sac_len <= sac_record` (yx2) in your jsonl; the row
records are in the list file. Write `ac-NNNNN: [..]` or `sac-NNNNN: [..]` to `research/acc/live/inbox/<UTC>_<you>_<row>.txt`,
commit, pull, push at once. Push your jsonl to `research/acc/live/sweeps/` every ~20 rows and at each :55 rally.
Only session 2 sends. Claim the list in `WORKING_<you>.md` before starting.
