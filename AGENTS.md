# Project continuity

Read `ACTIVE_WORK.md`, `MASTER_STATUS.md`, `BRANCH_STATUS.md`, `catalog/POLICY.md`, `AGENT_WORKFLOW.md`, and the current Compound Eye handoff before changing this project. Fetch GitHub branches and inspect open PRs before relying on a remembered release number, branch count, theorem count, or active head. Independent chats may extend different ancestors.

The integrated instrument on `main` is `tools/compound-eye/` Universal 3.2. Problem-specific branches may contain later eye versions. Compare immutable eye, set and implementation inventories before importing another release. Preserve both source histories, and use `Registry.add` / `add_set` for missing versions. Never overwrite an existing version to conceal a change.

`ACTIVE_WORK.md` names the current Yang–Mills, Earth–Moon and public Companion surfaces. `BRANCH_STATUS.md` distinguishes active research, paused checkpoints, clean distribution branches, frozen backups, superseded transport experiments and pinned proof history. Do not bulk-merge or delete branches just to reduce clutter.

Use `catalog/papers.json` and `atlas/cards.json` as the source of generated indexes. Run `scripts/build_catalog.py` and `scripts/validate_catalog.py` after catalog edits. Run `scripts/verify_compound_eye_release.py` and the affected scientific/mixer suites after tool integration. A finite diagnostic run, written proof, exact certificate and Lean compilation have distinct scopes.

Keep proof sources pinned to their actual verified commits. The default root build verifies the core module only. A green main build does not certify every separately indexed research module, and a green research build does not broaden prose beyond that branch's declared scope. Preserve raw-source attribution, failed controls and recovery limits.

Use one worker/task branch at a time. Do not have separate agents independently push to the same working branch. Hand off through commits and pull requests with the exact head SHA, blocker, next test, and important negative results recorded in the repository.

Any new or materially changed `.lean` module must be explicitly compiled or imported by the verified build path before it is described as Lean-certified. If it sits outside the root import tree, add an explicit module check to the relevant workflow in the same PR.

The clean outside-user Companion distribution is `share/compound-eye-companion-1.1`; do not substitute the superseded `release/` or `downloads/` transport experiments. Private owner research catalogs, datasets, results, connections and keys are not part of the clean share surface.

Give the user short progress updates and report concrete blockers promptly. Do not replace an active research problem with repeated packaging or planning. The user wants complete runnable replacements when scripts need repair.
