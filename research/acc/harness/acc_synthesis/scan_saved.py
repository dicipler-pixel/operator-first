#!/usr/bin/env python3
"""Read the saved ACC ledger and pools without network or model calls.

Reports source assertions, not newly replayed solutions or live eligibility.
Missing rows mean absent from these inputs, never absent from the whole repo.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def scan(targets_path, repo_path):
    targets_path, repo_path = Path(targets_path), Path(repo_path)
    manifest = json.loads(targets_path.read_text())
    rows = manifest['rows']
    ids = [r['row_id'] for r in rows]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r'ac-\d{5}', r) for r in ids):
        raise ValueError('Expected unique exact AC row IDs.')
    live = repo_path / 'research/acc/live'
    result = {r['row_id']: {**r, 'accepted_evidence': [], 'pool_paths': []} for r in rows}
    sources = []

    def read(path):
        raw = path.read_bytes()
        sources.append({'path': str(path.relative_to(repo_path)), 'bytes': len(raw),
                        'sha256': hashlib.sha256(raw).hexdigest(),
                        'git_blob_sha1': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()})
        return raw.decode('utf-8')

    for line_no, line in enumerate(read(live/'SENT_ROWS.txt').splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        cols = line.split()
        if cols[0] in result:
            if len(cols) < 5:
                raise ValueError('Malformed SENT_ROWS entry.')
            result[cols[0]]['accepted_evidence'].append({'length': int(cols[1]),
                'source': 'research/acc/live/SENT_ROWS.txt', 'line': line_no,
                'scope': 'saved ledger assertion; not a fresh server check'})

    def accept(items, source, location):
        for item in items:
            key = item.get('challenge_id')
            if key in result and item.get('ok') is True:
                length = item.get('length')
                if type(length) is not int or length < 0:
                    raise ValueError('Invalid accepted length in '+source)
                result[key]['accepted_evidence'].append({'length': length, 'source': source,
                    'location': location, 'scope': 'archived server acceptance; not current eligibility'})

    for line_no, line in enumerate(read(live/'submit_log.jsonl').splitlines(), 1):
        if line.strip():
            entry = json.loads(line)
            accept(entry.get('results', []), 'research/acc/live/submit_log.jsonl', line_no)
    recent = json.loads(read(live/'mine_recent.json'))
    for item in recent['items']:
        accept(item.get('results', []), 'research/acc/live/mine_recent.json', item['submissionId'])

    pool_records = 0
    for path in sorted((live/'pool').glob('*.jsonl')):
        for line_no, line in enumerate(read(path).splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            pool_records += 1
            if record['id'] not in result:
                continue
            moves = record['ac']
            if not isinstance(moves, list) or any(type(m) is not int for m in moves):
                raise ValueError('Malformed move sequence.')
            if record.get('ac_len', len(moves)) != len(moves):
                raise ValueError('Pool length disagrees with moves.')
            result[record['id']]['pool_paths'].append({'length':len(moves), 'moves':moves,
                'source':str(path.relative_to(repo_path)), 'line':line_no,
                'scope':'saved path; not replayed by this import'})

    counts = {}
    for row in result.values():
        best = min((e['length'] for e in row['accepted_evidence']), default=None)
        row['saved_accepted_best'] = best
        row['board_eligibility'] = 'unverified'
        row['search_dispatch'] = 'blocked_pending_exact_start_checker_and_budget'
        if best is not None and best <= row['record']:
            row['next_action'] = 'improvement_only'
            row['desired_max_moves'] = min(best, row['record']) - 1
        elif best is not None:
            row['next_action'] = 'recover_accepted_path_then_shorten'
            row['desired_max_moves'] = row['record']
        elif row['pool_paths']:
            row['next_action'] = 'replay_saved_path'
            row['desired_max_moves'] = row['record']
        else:
            row['next_action'] = 'resolve_start_and_other_saved_paths'
            row['desired_max_moves'] = row['record']
        counts[row['next_action']] = counts.get(row['next_action'], 0) + 1
    return {'schema':'acc-saved-intake/1', 'source_commit':manifest['repo_commit'],
        'targets_sha256':hashlib.sha256(targets_path.read_bytes()).hexdigest(),
        'model_calls':0, 'network_calls':0, 'fresh_replays':0,
        'scope':'Only the listed local sources were scanned. Points are preserved as pasted; no new reward is inferred.',
        'counts':counts, 'pool_records_scanned':pool_records, 'sources':sources, 'rows':list(result.values())}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--targets', required=True)
    p.add_argument('--repo', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    report = scan(args.targets, args.repo)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('counts','pool_records_scanned','model_calls','network_calls','fresh_replays')}))


if __name__ == '__main__':
    main()
