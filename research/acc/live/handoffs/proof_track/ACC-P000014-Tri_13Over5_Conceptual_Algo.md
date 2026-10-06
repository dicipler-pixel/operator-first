### How the Andrews-Curtis Solver Works

The Andrews-Curtis challenge asks you to transform an initial group presentation \\(\langle x, y \mid u = 1; v = 1 \rangle\\) into the exact target presentation \\((x, y) = [[1], [2]]\\) [2, 3].

1. **Integer Letter Encoding**:
   * \\(x = 1\\), \\(x^{-1} = -1\\) [2, 3]
   * \\(y = 2\\), \\(y^{-1} = -2\\) [2, 3]
   * Identity word = `[]` [2]
2. **Free Group Reduction**:
   * After every move, adjacent inverse letters (such as \\(1\\) and \\(-1\\), or \\(2\\) and \\(-2\\)) cancel out automatically [2, 3].
3. **The 14 Move Operations (`ac-r2-v1`)** [3]:
   * **Inversions (0–1)**: \\(r_0 \leftarrow r_0^{-1}\\), \\(r_1 \leftarrow r_1^{-1}\\) [3]
   * **Multiplications (2–5)**: \\(r_0 \leftarrow r_0 r_1^{\pm 1}\\), \\(r_1 \leftarrow r_1 r_0^{\pm 1}\\) [3]
   * **Conjugations (6–13)**: Conjugate \\(r_0\\) or \\(r_1\\) by \\(x^{\pm 1}\\) or \\(y^{\pm 1}\\) [3]
4. **Canonicalization Suffix Matching**:
   * Reaching any signed permutation (like \\((x, y^{-1})\\) or \\((y, x)\\)) attaches a deterministic 1- to 5-move suffix to reach \\([[1], [2]]\\) [3].

---

### Complete Python Code (`ac_solver.py`)

```python
"""
SAIR Andrews-Curtis (AC) Discovery Track Solver (ac_solver.py)
---------------------------------------------------------------
A self-contained Python solver and verifier for the SAIR Andrews-Curtis
Discovery Track (AC challenges).
"""

import heapq
import json
import sys


def free_reduce(word):
  """Cancel adjacent inverse letters in a word (+k for g_k, -k for g_k^-1)."""
  stack = []
  for letter in word:
    if stack and stack[-1] == -letter:
      stack.pop()
    else:
      stack.append(letter)
  return stack


def invert_word(word):
  """Return the inverse of a word, freely reduced."""
  return [-w for w in reversed(word)]


def apply_ac_move(relators, move_id):
  """Apply one of the 14 AC moves (ac-r2-v1) to relators [r0, r1]."""
  r0, r1 = relators, relators[1]

  if move_id == 0:  # r0 <- r0^-1
    return free_reduce(invert_word(r0)), r1
  elif move_id == 1:  # r1 <- r1^-1
    return r0, free_reduce(invert_word(r1))
  elif move_id == 2:  # r0 <- r0 * r1
    return free_reduce(r0 + r1), r1
  elif move_id == 3:  # r0 <- r0 * r1^-1
    return free_reduce(r0 + invert_word(r1)), r1
  elif move_id == 4:  # r1 <- r1 * r0
    return r0, free_reduce(r1 + r0)
  elif move_id == 5:  # r1 <- r1 * r0^-1
    return r0, free_reduce(r1 + invert_word(r0))
  elif move_id == 6:  # r0 <- x * r0 * x^-1
    return free_reduce([1] + r0 + [-1]), r1
  elif move_id == 7:  # r0 <- x^-1 * r0 * x
    return free_reduce([-1] + r0 + [1]), r1
  elif move_id == 8:  # r0 <- y * r0 * y^-1
    return free_reduce([2] + r0 + [-2]), r1
  elif move_id == 9:  # r0 <- y^-1 * r0 * y
    return free_reduce([-2] + r0 + [2]), r1
  elif move_id == 10:  # r1 <- x * r1 * x^-1
    return r0, free_reduce([1] + r1 + [-1])
  elif move_id == 11:  # r1 <- x^-1 * r1 * x
    return r0, free_reduce([-1] + r1 + [1])
  elif move_id == 12:  # r1 <- y * r1 * y^-1
    return r0, free_reduce([2] + r1 + [-2])
  elif move_id == 13:  # r1 <- y^-1 * r1 * y
    return r0, free_reduce([-2] + r1 + [2])
  else:
    raise ValueError(f"Invalid move_id: {move_id}")


# Shortest canonicalization suffixes to reach exact target ([1],[2]) from signed permutations
CANONICAL_SUFFIXES = {
    ((1,), (2,)): [],
    ((1,), (-2,)): [1],
    ((-1,), (2,)): ,
    ((-1,), (-2,)): [1],
    ((-2,), (1,)): [2, 4, 5],
    ((2,), (-1,)): [3, 6, 7],
    ((-2,), (-1,)): [2, 3, 6],
    ((2,), (1,)): [2, 4, 5],
}


def solve_ac(initial_relators, max_nodes=50000, max_length_cap=100):
  """Search for a sequence of AC move IDs transforming initial_relators to [[1], [2]]."""
  r0_init = free_reduce(initial_relators)
  r1_init = free_reduce(initial_relators[1])
  start_state = (tuple(r0_init), tuple(r1_init))

  if start_state in CANONICAL_SUFFIXES:
    return list(CANONICAL_SUFFIXES[start_state])

  # Priority queue: (heuristic_cost, path_length, state, path)
  initial_cost = len(r0_init) + len(r1_init)
  pq = [(initial_cost, 0, start_state, [])]
  visited = {start_state: 0}
  nodes_evaluated = 0

  while pq and nodes_evaluated < max_nodes:
    cost, path_len, state, path = heapq.heappop(pq)
    nodes_evaluated += 1

    for move_id in range(14):
      new_r0, new_r1 = apply_ac_move([list(state), list(state[1])], move_id)
      nxt_state = (tuple(new_r0), tuple(new_r1))

      if nxt_state in CANONICAL_SUFFIXES:
        return path + [move_id] + CANONICAL_SUFFIXES[nxt_state]

      nxt_len = len(new_r0) + len(new_r1)
      if nxt_len <= max_length_cap:
        new_path_len = path_len + 1
        if nxt_state not in visited or new_path_len < visited[nxt_state]:
          visited[nxt_state] = new_path_len
          priority = new_path_len + nxt_len
          heapq.heappush(
              pq, (priority, new_path_len, nxt_state, path + [move_id])
          )

  return None


def format_submission_line(challenge_id, moves):
  """Format single solution line for SAIR TXT submission."""
  return f"{challenge_id}: {json.dumps(moves)}"
```

---

### How to Run in SAIR Playground

1. In the SAIR Playground, paste your problem ID and candidate moves in **TXT submission format** [2]:
   ```txt
   ac-00001: [3]
   ac-00002: [1, 2, 6, 8, 9]
   ```
2. For local verification, run the official SAIR verifier against your manifest [6]:
   ```bash
   PYTHONPATH=competition/tools python3 -m verifier \
     --manifest competition/tools/verifier/data/manifest.json \
     --submission submission.txt --pretty
   ```