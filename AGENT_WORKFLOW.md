# Shared agent workflow

GitHub is the project record. Use a separate branch for each worker and each task. Do not have multiple workers independently modify the same working branch.

Before changing research state, read AGENTS.md, ACTIVE_WORK.md, MASTER_STATUS.md, BRANCH_STATUS.md, catalog/POLICY.md, and the active pull request.

Research changes go through pull requests into main. Each pull request must state what changed, what was tested, what failed, and what remains unproved.

Lean modules are certified only when the exact module is compiled or imported by a verified build. A green root build does not certify unrelated Lean files.

Keep raw data, numerical checks, exact certificates, written arguments, Lean theorems, and interpretation separate.

Handoffs belong in the repository or pull request with the exact commit SHA, blocker, next test, and important negative results.

Preserve competing branches until they have been compared. Do not overwrite history to make versions agree.
