# Active work — 10 September 2026

This is the short operational map. Read `MASTER_STATUS.md` for the broader project record and `BRANCH_STATUS.md` before creating, merging, or replacing branches.

## 1. Yang–Mills — ACTIVE

- Draft PR: [#18](https://github.com/dicipler-pixel/operator-first/pull/18)
- Branch: `research/yang-mills-2026-09-09`
- Current research head at this audit: `4c90eaa499cde0c178ac3378a2138aa8aa9c5c34`
- Latest root CI on that head: success, run `34413639743`.
- Focused native reproduction and the separately scoped Lean runs are recorded in the PR body and research reports.
- Current mathematical boundary: no quantitative moderate-coupling volume-uniform gap and no nontrivial four-dimensional continuum construction. The next useful work is spatial scaling / failure diagnosis, not relabelling finite-cell certificates as Clay Yang–Mills.
- Keep Earth–Moon statistics, Elemental declaration counts, and finite Compound Eye observations separate from gauge-theory theorem counts.

## 2. Earth–Moon — PAUSED, FULLY CHECKPOINTED

- Draft PR: [#19](https://github.com/dicipler-pixel/operator-first/pull/19)
- Branch: `research/earth-moon-2026-09-09`
- Current research head at this audit: `3c3a8b2845ef0d57c5d406739ca485397381192e`
- Latest root CI on that head: success, run `34398791804`.
- Frozen hard-backup branch: `backup/earth-moon-2026-09-09-1918utc` at `582a70c3069b606b042d26303f1e27ff7f599f95`.
- Resume from the hard-backup checkpoint and side-scanner reports, not stale PID/RUNNING files.
- Current status remains no winning Earth–Moon graph; the 100-edge ten-chromatic survivor still has planar thickness UNKNOWN.

## 3. Compound Eye clean public share — READY

- Share branch: `share/compound-eye-companion-1.1`
- Current share head at this audit: `12a6eef9f3380e8b8821e6ec375f3fcb2171a704`.
- GitHub smoke-test workflow: success, run `34461867296`.
- Direct GitHub ZIP: https://github.com/dicipler-pixel/operator-first/archive/refs/heads/share/compound-eye-companion-1.1.zip
- This is the clean friend/share edition. It is deliberately separate from private owner research catalogs, datasets, results, account connections, and API keys.
- `release/compound-eye-companion-1.1` and `downloads/compound-eye-companion-1.1` are superseded transport experiments; do not give them out as the current share build.

## 4. Main — STABLE INTEGRATED BASELINE

Before this bookkeeping update, `main` was `401f6b4b255504ef4465140a15b6cfd6daa9c887`, the verified Universal 3.2 synchronization merge. Its CI passed. This September 10 update changes project-navigation documents only; it does not merge PR #18 or #19 or broaden any scientific claim.

The unified instrument on main remains `tools/compound-eye/` Universal 3.2. New research-specific Compound Eye developments live on their dated research branches until deliberately reconciled.

## 5. Other proof/research branches — PINNED HISTORY OR SEPARATE WORK

Light, Offset, peeling, projector/gravity, Kakeya, Diophantine, catalog and older Compound Eye branches remain useful pinned evidence. They are not automatically superseded mathematically merely because they are older, and they are not to be bulk-merged. Use the exact verified branch/commit named by the relevant paper or report.

## Operating rule

For any new session:

1. Read this file, `MASTER_STATUS.md`, `BRANCH_STATUS.md`, and `catalog/POLICY.md`.
2. Fetch current branches and open PRs before relying on remembered counts.
3. Work on the branch belonging to the active problem.
4. Preserve failed controls and source hashes.
5. Do not merge a research PR into main merely to make the repository look tidy.
