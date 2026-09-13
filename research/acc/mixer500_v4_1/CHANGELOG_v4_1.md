# Compound Eye 500 — v4.1 repair (2026-09-13)

Base: `Compound_Matrix_Mixer_500I_v4.zip` (Drive hub, sha256 `d6398c66…`), `compound_eye_500.py`.

## Defect in v4 (DAG `compound-eye-500-v4-target-leak`)
Every generic eye averaged all numeric columns of a row, including the target column, so `target_abs_correlation` was leakage: 0.998 reported on a two-column table whose true Pearson is 0.743; all identity eyes reported 0.708 on the 42-column table. The diverse panel also admitted exact duplicates.

## Changes
1. One eye instance per `(view, feature column)`, id `<view>@<column>`; the target column is never eye input; `source_column` and `source_column_index` are carried on every trace for provenance.
2. Diverse panel rejects a candidate whose |r| to an already selected eye exceeds 0.999, even at high utility.
3. Redundancy/novelty computed with numpy over all instances (pairwise-complete, NaN-aware); pure-Python fallback kept.
4. `--resume`-style behaviour: if `EYES_ALL_RAW.jsonl` and `INDIVIDUAL_EYE_SUMMARY.json` already exist in the output directory, traces are reused and only the mixing stage reruns.
5. Report fields: `generic_eye_instances_per_column`, `new_generic_executable_views`, `feature_columns`.

## Validation
- Two-column control `(floor, remaining)`: identity eye now reports 0.7426 = true Pearson.
- 3,000-row random subsample of the ACC calibration table (19 features, target `remaining`): 5,871 instances, 52 kernel groups; best |Pearson| per column: len_r1 0.808, floor 0.702, cyc_tot 0.663, tot 0.659, Smith mul-r0-by-r1 radius 0.510, foxA 0.493, hab 0.168, conjugation Smith layers ≤ 0.18. 4,900 of 5,871 instances are exact duplicates of another instance (identity/center/zscore views of the same window agree up to affine maps), which is why the panel dedupe matters; the panel now spans six columns.
- Caveat: rolling-window views assume consecutive rows form a sequence. The subsample was shuffled, so only the window-1 views are meaningful there; feed per-path sequences (sorted by challenge, step) to use the rolling views.
- Standing rule: no eye is removed. Uninformative instances stay in the ledger at routing weight zero.

Run: `python3 compound_eye_500.py <table.csv> <outdir> --target-column <name>` (needs `catalog/eyes_500.json` beside the script; numpy optional but strongly recommended).
