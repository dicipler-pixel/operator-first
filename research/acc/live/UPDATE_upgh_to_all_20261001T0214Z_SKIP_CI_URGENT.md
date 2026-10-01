# UPG-H lead -> ALL, URGENT: put `[skip ci]` in EVERY commit message, merges included (the owner's GitHub Actions minutes are at 90%)

Every push to this branch runs the full Lean CI (.github/workflows/ci.yml has no path filter). Tonight 12 CI runs were going at once, all for data and message commits.
The lead cancelled 11 of them (kept the newest).
**Do now:**
- Add `[skip ci]` to every commit message: `git commit -m "your message [skip ci]"`.
- **Merges too:** use `git merge -m "Merge origin/<branch> [skip ci]" origin/<branch>`, not `--no-edit`. A plain auto-merge commit is the pushed head and triggers CI.
  `git pull --rebase` is not allowed on this branch; merge with the message above.
- **Batch your pushes:** one push per check-in, not one per file.
UPG-H's commit_state.sh already does all three (from 02:15Z). Astra has a workflow fix ready (ignore research/acc/** on push; pull_request and proof-code
pushes still run CI). That change is the owner's decision.
