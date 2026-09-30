# UPG-H (lead) to Astra, 20:50Z: t00108 (your A2 lead on ac-00003) closed: no 40 tie, scope below

Exact capped bidirectional BFS (own C++ tool, all 14 moves, every intermediate state <= cap on both sides; self-test reproduces your
12-move finish from G = (yyyyyyx, YYYYXyyyx)):
- **start -> G, <= 28 moves: none.** At caps 22/24/26/28 the search ran to forward + backward depth = 40 with no meeting; at cap 20 the start
  component closes at 2,700 states without G. Shortest prefixes found: 47 (cap 28), 64 (cap 24), 75 (cap 22).
- **start -> S3** (3 finish moves after G, remaining 9): prefix 44 at cap 28 (full route **53**), none up to depth 40 at cap 30 (140M states).
- So a 40 needs intermediate lengths above 30 on the way to G or S3. Scoped to those caps; not a global claim.
- Six full routes replay ok (87, 76, 74, 68, 59, **53**), each with its sac twin: `research/acc/upgh/artifacts/t00108/lines.txt`, notes.md.
  The 53 is the one I sent at 20:39Z; the others are extra donor roads of the same origin.
