#!/usr/bin/env bash
# Exercise every refusal path of commit_snapshot_v1.sh in throwaway repos.
# A scheduled job with write access has to be tested before it is trusted, and
# a scheduled event cannot be fired by hand.
set -uo pipefail

SCRIPT="$(cd "$(dirname "$0")" && pwd)/commit_snapshot_v1.sh"
SNAP="ledger/timeline/snapshots_v1.jsonl"
pass=0; fail=0

check() { # name expected_exit expected_substring actual_exit actual_output
  if [ "$4" = "$2" ] && printf '%s' "$5" | grep -qF -- "$3"; then
    echo "  ok    $1"; pass=$((pass+1))
  else
    echo "  FAIL  $1"; echo "        exit $4 (want $2)"; echo "        $5"
    fail=$((fail+1))
  fi
}

fixture() { # -> prints repo dir, on branch $1
  d=$(mktemp -d)
  git -C "$d" init -q -b "$1"
  mkdir -p "$d/$(dirname "$SNAP")"
  printf '{"row":0}\n' > "$d/$SNAP"
  git -C "$d" add -A >/dev/null
  git -C "$d" -c user.email=t@t -c user.name=t commit -qm base
  printf '%s' "$d"
}

run() { ( cd "$1" && shift && PUSH=0 env "$@" "$SCRIPT" 2>&1 ); }

echo "commit_snapshot_v1.sh"

d=$(fixture main)
out=$(run "$d" SNAPSHOT_PATH="$SNAP" ALLOWED_BRANCHES="main" GITHUB_REF_NAME=main); rc=$?
check "no change is a normal no-op" 0 "no new snapshot to commit" "$rc" "$out"

d=$(fixture main)
printf '{"row":1}\n' >> "$d/$SNAP"
out=$(run "$d" SNAPSHOT_PATH="$SNAP" ALLOWED_BRANCHES="main" GITHUB_REF_NAME=main); rc=$?
check "one appended row commits" 0 "committed locally" "$rc" "$out"
n=$(git -C "$d" rev-list --count HEAD)
check "history advanced by exactly one commit" 0 "2" 0 "$n"

d=$(fixture main)
printf '{"row":1}\n' >> "$d/$SNAP"
out=$(run "$d" SNAPSHOT_PATH="$SNAP" ALLOWED_BRANCHES="main other" GITHUB_REF_NAME=nope); rc=$?
check "a branch outside the allowlist is refused" 0 "not in ALLOWED_BRANCHES" "$rc" "$out"
n=$(git -C "$d" rev-list --count HEAD)
check "and nothing was committed there" 0 "1" 0 "$n"

d=$(fixture main)
printf '{"row":1}\n{"row":2}\n' >> "$d/$SNAP"
out=$(run "$d" SNAPSHOT_PATH="$SNAP" ALLOWED_BRANCHES="main" GITHUB_REF_NAME=main); rc=$?
check "two appended rows are refused" 1 "expected exactly one appended line" "$rc" "$out"

d=$(fixture main)
printf '{"row":9}\n' > "$d/$SNAP"          # rewrite rather than append
out=$(run "$d" SNAPSHOT_PATH="$SNAP" ALLOWED_BRANCHES="main" GITHUB_REF_NAME=main); rc=$?
check "rewriting an existing row is refused" 1 "got +1 -1" "$rc" "$out"

d=$(fixture main)
printf '{"row":1}\n' >> "$d/$SNAP"
echo "secret" > "$d/other.txt"
git -C "$d" add other.txt >/dev/null              # something else pre-staged
out=$(run "$d" SNAPSHOT_PATH="$SNAP" ALLOWED_BRANCHES="main" GITHUB_REF_NAME=main); rc=$?
check "an unrelated staged file is refused" 1 "staged more than the snapshot ledger" "$rc" "$out"

d=$(fixture claude/confident-fermi-09rd02)
printf '{"row":1}\n' >> "$d/$SNAP"
out=$(run "$d" SNAPSHOT_PATH="$SNAP" ALLOWED_BRANCHES="main claude/confident-fermi-09rd02" \
      GITHUB_REF_NAME=claude/confident-fermi-09rd02); rc=$?
check "the working branch is allowed" 0 "committed locally" "$rc" "$out"

echo "  $pass passed, $fail failed"
[ "$fail" = 0 ]
