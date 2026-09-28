#!/usr/bin/env python3
"""Exact ordered-state reverse AC components under complete total-length ceilings.

No cyclic quotient, heuristic prune, or fingerprint collision. A ceiling is
reported complete only when the BFS queue is empty. The first complete ceiling
that connects a state certifies its minimum *total-length* height barrier;
distances here are shortest only within that ceiling.
"""
import argparse
import json
import sys
import time
from collections import Counter, deque
from pathlib import Path


def length(state):
    return len(state[0]) + len(state[1])


def as_json(state):
    return [list(state[0]), list(state[1])]


def path_to(state, info):
    result = []
    while info[state][1] is not None:
        depth, parent, move = info[state]
        result.append(move)
        state = parent
    return result[::-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verifier-root', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--first', type=int, default=2)
    ap.add_argument('--last', type=int, default=8)
    ap.add_argument('--max-states', type=int, default=500000)
    ap.add_argument('--max-seconds-per-cap', type=float, default=60)
    args = ap.parse_args()
    sys.path.insert(0, str(Path(args.verifier_root) / 'competition' / 'tools'))
    from verifier import core
    manifest = json.loads(Path(args.manifest).read_text())
    challenges = {tuple(tuple(w) for w in c['initial_relators']): c['challenge_id']
                  for c in manifest['challenges'] if c['challenge_id'].startswith('ac-')}
    root = ((1,), (2,))
    prior_depths = {}
    prior_info = {}
    output = []
    for cap in range(args.first, args.last + 1):
        start = time.monotonic()
        # value: (BFS distance within this ceiling, parent state, move from parent)
        info = {root: (0, None, None)}
        queue = deque([root])
        expanded = 0
        attempted = 0
        aborted = None
        while queue:
            state = queue.popleft()
            expanded += 1
            depth = info[state][0]
            for move in range(core.NUM_MOVES):
                attempted += 1
                nxt = core.apply_move(state, move)
                if length(nxt) > cap or nxt in info:
                    continue
                info[nxt] = (depth + 1, state, move)
                queue.append(nxt)
                if len(info) > args.max_states:
                    aborted = 'state_budget'
                    break
            if aborted:
                break
            if expanded % 10000 == 0 and time.monotonic() - start > args.max_seconds_per_cap:
                aborted = 'time_budget'
                break
        rec = {'cap_total_length': cap, 'complete': not aborted,
               'abort_reason': aborted, 'states_seen': len(info),
               'states_expanded': expanded, 'transitions_attempted': attempted,
               'queue_remaining': len(queue), 'wall_s': round(time.monotonic()-start, 3)}
        if aborted:
            output.append(rec)
            print(json.dumps(rec), flush=True)
            break
        depths = {s: entry[0] for s, entry in info.items()}
        rec['diameter_within_cap'] = max(depths.values())
        rec['depth_histogram'] = dict(sorted(Counter(depths.values()).items()))
        rec['new_states_from_prior_cap'] = len(depths.keys() - prior_depths.keys()) if prior_depths else None
        if prior_depths:
            detours = [s for s in depths.keys() - prior_depths.keys() if length(s) < cap]
            rec['new_lower_length_states_requiring_this_height'] = len(detours)
            if detours:
                witness = min(detours, key=lambda s: (depths[s], length(s), s))
                forward = path_to(witness, info)
                back = [core.INVERSE_MOVE[m] for m in forward[::-1]]
                cursor = witness
                for m in back:
                    cursor = core.apply_move(cursor, m)
                assert cursor == root
                rec['height_witness'] = {'state': as_json(witness), 'state_total_length': length(witness),
                                         'distance_within_cap': depths[witness],
                                         'moves_from_root': forward, 'moves_home': back,
                                         'optional_challenge_id': challenges.get(witness)}
            shorter = [s for s in prior_depths if s in depths and depths[s] < prior_depths[s]]
            rec['old_states_with_shorter_path_at_new_cap'] = len(shorter)
            rec['largest_distance_saving_at_new_cap'] = max((prior_depths[s] - depths[s] for s in shorter), default=0)
            if shorter:
                witness = max(shorter, key=lambda s: (prior_depths[s] - depths[s], -length(s), s))
                old_moves = path_to(witness, prior_info)
                new_moves = path_to(witness, info)
                rec['distance_shortcut_witness'] = {
                    'state': as_json(witness), 'state_total_length': length(witness),
                    'prior_cap': cap - 1, 'prior_distance_within_cap': prior_depths[witness],
                    'new_cap': cap, 'new_distance_within_cap': depths[witness],
                    'prior_moves_from_root': old_moves, 'new_moves_from_root': new_moves,
                    'optional_challenge_id': challenges.get(witness)}
        matched = [(cid, depths[s]) for s, cid in challenges.items() if s in depths]
        rec['manifest_ac_rows_connected'] = len(matched)
        rec['manifest_examples'] = sorted(matched, key=lambda x: x[1], reverse=True)[:5]
        output.append(rec)
        print(json.dumps({k:v for k,v in rec.items() if k != 'depth_histogram'}), flush=True)
        prior_depths = depths
        prior_info = info
    print('RESULT_JSON=' + json.dumps(output), flush=True)


if __name__ == '__main__':
    main()
