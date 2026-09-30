#!/usr/bin/env python3
"""Pinned adapter to the unchanged official ac-r2-v1 verifier. Offline only."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
# This file is itself pinned by config.json; this pin binds all dependencies.
PINS_SHA256 = 'c1e6fdb694d57f876aa8ef1b73be63820b08a7dd1aa1f2651a5f40c7700bcbdd'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
        ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def load_kernel():
    pinfile = ROOT/'integration/adapter_pins.json'
    if sha(pinfile) != PINS_SHA256:
        raise ValueError('Checker dependency pin manifest changed.')
    for relative, expected in json.loads(pinfile.read_text()).items():
        path = (ROOT/relative).resolve()
        if not path.is_relative_to(ROOT) or sha(path) != expected:
            raise ValueError('Checker dependency changed: '+relative)
    sys.path.insert(0, str(ROOT/'vendor'))
    from verifier import core, canon, specs
    doc = json.loads((ROOT/'integration/official_selected.json').read_text())
    if specs.check_move_specs(doc['move_specs']):
        raise ValueError('Official move specification mismatch.')
    challenges = {c['challenge_id']: c for c in doc['challenges']}
    for c in challenges.values():
        actual = canon.instance_hash(c['challenge_id'], c['generators'], c['initial_relators'],
            c['target_relators'], c['move_spec_version'], specs.get(c['move_spec_version']).move_spec_hash)
        if actual != c['instance_hash']:
            raise ValueError('Official instance hash mismatch.')
    return core, specs, doc, challenges


def render(relators):
    alphabet = {1:'x', -1:'X', 2:'y', -2:'Y'}
    return [''.join(alphabet[n] for n in word) for word in relators]


def check(candidate):
    core, specs, doc, challenges = load_kernel()
    challenge = challenges[candidate['row_id']]
    rule_hash = specs.get(challenge['move_spec_version']).move_spec_hash.removeprefix('sha256:')
    if candidate.get('track') != 'AC' or candidate.get('ruleset_sha256') != rule_hash:
        raise ValueError('Track or move specification mismatch.')
    if candidate.get('start') != render(challenge['initial_relators']):
        raise ValueError('Exact starting presentation mismatch.')
    verdict = core.verify(challenge, candidate['moves'], challenge['move_spec_version'], doc['limits'])
    # The official successful verdict proves equality to this exact endpoint.
    receipt = {'candidate_sha256':canonical_hash(candidate), 'checker_sha256':sha(__file__),
        'ruleset_sha256':rule_hash, 'valid':verdict['ok'],
        'exact_endpoint':render(challenge['target_relators']) if verdict['ok'] else None,
        'cost':verdict.get('length'), 'peak_length':verdict.get('peak_total_relator_length'),
        'official_verdict':verdict, 'instance_hash':challenge['instance_hash'],
        'official_commit':doc['source_commit']}
    # Detect dependency changes during verification too.
    load_kernel()
    return receipt


def main():
    candidate_path, receipt_path = map(Path, sys.argv[1:3])
    receipt = check(json.loads(candidate_path.read_text()))
    receipt_path.write_text(json.dumps(receipt, indent=2)+'\n')


if __name__ == '__main__':
    main()
