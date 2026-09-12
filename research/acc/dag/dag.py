"""Minimal append-only knowledge DAG for the ACC effort.

Deliberately small: a file format, a validator, and a query. Agents read
`open` / `blocked` nodes before starting work and append result nodes after.
No framework, no scheduler -- those can grow once the format earns its keep.
"""

import json
import sys
from pathlib import Path

NODES = Path(__file__).with_name("nodes.jsonl")

REQUIRED = ("id", "kind", "claim", "status", "evidence", "recorded_utc")
KINDS = {"fact", "question", "experiment", "blocker", "method"}
STATUSES = {"verified", "refuted", "open", "blocked"}
EVIDENCE = {"exact-replay", "computation", "repo-provenance", "external-source", "none"}


def load(path=NODES):
    nodes = []
    for lineno, line in enumerate(Path(path).read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            nodes.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{lineno}: {exc}") from exc
    return nodes


def check(nodes):
    """Return a list of invariant violations, empty when the DAG is sound."""
    errors = []
    by_id = {}
    for n in nodes:
        missing = [f for f in REQUIRED if f not in n]
        if missing:
            errors.append(f"{n.get('id', '<no id>')}: missing {', '.join(missing)}")
            continue
        if n["id"] in by_id:
            errors.append(f"{n['id']}: duplicate id")
        by_id[n["id"]] = n
        if n["kind"] not in KINDS:
            errors.append(f"{n['id']}: unknown kind {n['kind']!r}")
        if n["status"] not in STATUSES:
            errors.append(f"{n['id']}: unknown status {n['status']!r}")
        if n["evidence"] not in EVIDENCE:
            errors.append(f"{n['id']}: unknown evidence {n['evidence']!r}")
        if n["status"] == "verified" and n.get("evidence") == "none":
            errors.append(f"{n['id']}: verified but evidence is 'none'")
        if n.get("visibility") == "private" and "observed" in n:
            errors.append(f"{n['id']}: private node carries an observed payload")

    for n in nodes:
        for field in ("depends_on", "supersedes"):
            targets = n.get(field, [])
            if isinstance(targets, str):
                targets = [targets]
            for t in targets:
                if t not in by_id:
                    errors.append(f"{n.get('id')}: {field} -> unknown node {t!r}")

    # cycle detection over depends_on (iterative, so a deep chain cannot blow the stack)
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {i: WHITE for i in by_id}
    for root in by_id:
        if colour[root] != WHITE:
            continue
        stack = [(root, iter(by_id[root].get("depends_on", [])))]
        colour[root] = GREY
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                colour[node] = BLACK
                stack.pop()
            elif nxt in colour and colour[nxt] == GREY:
                errors.append(f"cycle in depends_on at {nxt!r}")
                colour[nxt] = BLACK
            elif nxt in colour and colour[nxt] == WHITE:
                colour[nxt] = GREY
                stack.append((nxt, iter(by_id[nxt].get("depends_on", []))))
    return errors


def query(nodes, status=None, kind=None, evidence=None):
    out = nodes
    if status:
        out = [n for n in out if n.get("status") == status]
    if kind:
        out = [n for n in out if n.get("kind") == kind]
    if evidence:
        out = [n for n in out if n.get("evidence") == evidence]
    return out


def append(node, path=NODES):
    nodes = load(path) + [node]
    errors = check(nodes)
    if errors:
        raise ValueError("refusing to append; DAG would be invalid:\n  " + "\n  ".join(errors))
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(node, sort_keys=True) + "\n")


def main(argv):
    nodes = load()
    if "--check" in argv:
        errors = check(nodes)
        for e in errors:
            print("FAIL", e)
        print(f"{len(nodes)} nodes, {len(errors)} violations")
        return 1 if errors else 0

    status = None
    for flag in ("open", "blocked", "verified", "refuted"):
        if f"--{flag}" in argv:
            status = flag
    for n in query(nodes, status=status):
        print(f"[{n['status']:<8}] [{n['evidence']:<16}] {n['id']}")
        print(f"             {n['claim']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
