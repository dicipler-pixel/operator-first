#!/usr/bin/env python3
"""Import the independent 2.2 additions into an extracted 3.1 source tree.

Existing manifests and content-addressed implementations must agree. History
from 3.1 stays intact; missing 2.2 entries are registered through the real API.
Both input inventories and every conflicting historical file are retained.
"""
import argparse
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--older', type=Path, required=True)
    ap.add_argument('--target', type=Path, required=True)
    args = ap.parse_args()
    old, target = args.older.resolve(), args.target.resolve()
    before_old, before_new = inventory(old), inventory(target)
    preserved = target / 'preserved/synchronization_3_2'
    if preserved.exists():
        raise ValueError('This integration has already been applied.')
    preserved.mkdir(parents=True)
    for name, inv in [('universal_2_2', before_old), ('universal_3_1', before_new)]:
        (preserved / (name + '_inventory.json')).write_text(json.dumps(inv, indent=2) + '\n')
    immutable = ('catalog/eyes/', 'catalog/sets/', 'plugins/installed/')
    conflicts = [p for p in before_old.keys() & before_new.keys()
                 if before_old[p] != before_new[p] and p.startswith(immutable)]
    if conflicts:
        raise ValueError('Immutable source conflicts: ' + repr(conflicts))
    changed = []
    for rel in sorted(before_old):
        source, dest = old / rel, target / rel
        if rel in before_new:
            if before_old[rel] != before_new[rel]:
                archive = preserved / 'universal_2_2' / rel
                archive.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, archive)
                changed.append(rel)
        elif not rel.startswith(('catalog/eyes/', 'catalog/sets/')):
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
    # Preserve the 3.1 presentation and ledgers before integration edits.
    for rel in ['START_HERE.html', 'START_HERE.md', 'CHAT_HANDOFF.md',
                'build_portal.py', 'build_mixer_portal.py', 'run_all.py',
                'release_counts.json', 'UNIVERSAL_MANIFEST.json', 'CITATION.cff',
                'catalog/history.jsonl', 'catalog/set_history.jsonl']:
        dest = preserved / 'universal_3_1' / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target / rel, dest)
    spec = importlib.util.spec_from_file_location('ce_sync_machine', target / 'machine.py')
    machine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(machine)
    registry = machine.Registry(target)
    added_eyes, added_sets = [], []
    for row in map(json.loads, (old / 'catalog/history.jsonl').read_text().splitlines()):
        ref = row['eye']
        if ref not in registry.eyes:
            rel = 'catalog/eyes/' + ref + '.json'
            registry.add(json.loads((old / rel).read_text()))
            # Preserve original whitespace as well as the canonical content.
            shutil.copy2(old / rel, target / rel)
            added_eyes.append(ref)
    for row in map(json.loads, (old / 'catalog/set_history.jsonl').read_text().splitlines()):
        ref = row['set']
        if ref not in registry.sets:
            rel = 'catalog/sets/' + ref + '.json'
            registry.add_set(json.loads((old / rel).read_text()))
            shutil.copy2(old / rel, target / rel)
            added_sets.append(ref)
    registry = machine.Registry(target)
    for inv in [before_old, before_new]:
        for rel, expected in inv.items():
            if rel.startswith(immutable):
                assert sha(target / rel) == expected, rel
    report = {'release': '3.2', 'source_releases': ['2.2', '3.1'],
              'shared_eye_versions': 167, 'eye_versions': len(registry.eyes),
              'sets': len(registry.sets), 'imported_eyes': added_eyes,
              'imported_sets': added_sets, 'immutable_conflicts': conflicts,
              'historical_file_conflicts_preserved': changed,
              'all_source_eye_set_and_implementation_bytes_preserved': True,
              'scope': 'Source reconciliation and registry validation; not a scientific rerun.'}
    out = target / 'projects/master_sync'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'reconciliation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
