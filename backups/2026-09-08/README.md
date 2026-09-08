# Complete accessible-work backup

This backup preserves **2,009 files / 769,334,120 original bytes**: 52 supplied attachments, 13 delivered artifacts (including complete releases 2.0, 2.1 and 2.2), and all 1,944 files of the current Compound Eye 2.2 instrument. The repository itself retains the paper register, Atlas, proof sources and history.

This covers the work available in this workspace. It cannot include unseen chats, inaccessible Windows Downloads, or remote files not supplied here. Installed dependencies and transient analysis caches are excluded. Research papers downloaded separately for reading are cited by URL and hash rather than redistributed.

## Restore

Download this branch as a ZIP, or clone it. Then run, from the repository root:

```sh
python backups/2026-09-08/restore_work.py --output restored-work
```

Choose an empty destination. Python 3.9 or newer is required; no third-party packages are needed for restoration. The script verifies every part, the complete archive, and every restored file. Restored paths are organized as `attachments/`, `deliverables/`, and `compound_eye_universal_2_2/`. Open `START_HERE.html` in the restored instrument, or install its requirements and run `run_all.py`.

`FILES.json` preserves exact original paths, sizes and SHA-256 values. `PARTS.json` specifies the ordered binary pieces and complete archive hash. The pieces contain the full bytes; restoration needs no external storage service, expiring link, or authentication beyond access to this repository.

Scientific scope, reconstruction and corrected claims are in [the audit](../../research/diophantine/Findings.md). Seven algebraic Lean certificates passed in the [isolated build](https://github.com/dicipler-pixel/operator-first/actions/runs/34171724494). The unrelated inherited root build remains broken; nothing has been merged.

Attribution and third-party data licenses remain in the archived sources. Backup is preservation, not endorsement of historical scientific claims.
