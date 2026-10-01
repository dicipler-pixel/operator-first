# AC-1M vs the board (UPG-H, 10:50Z)

- **Source:** ACSolverX (Math-AI-Caltech, the Two-Hump paper), data/AC1M.txt.gz, 1,136,154 AC-trivial presentations of length <= 30, presentations only (no paths).
- **Method:** canonical key up to the 16 symmetries and per-relator rotation/inversion (twin_lookup.key). Every AC-1M line was matched against every board row.
- **Result:** **0 of the 2,672 board-unsolved AC rows are in AC-1M.**
- **Control:** the matcher found 453 already-solved rows (total <= 30) in just the first 300k AC-1M lines, so it works.
- **Reading:** the unsolved pool is disjoint from the public AC-trivial datasets, so AC-1M gives no free first solves. Do not repeat this check.
