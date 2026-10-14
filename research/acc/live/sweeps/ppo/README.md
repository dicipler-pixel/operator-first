# Caltech AC-SolverX 610model on unsolved rows (UPG-H, 14 Oct 2026, from 10:20Z; owner approved)

**What:** the organizers' published PPO model (github.com/Math-AI-Caltech/ACSolverX, ppo_checkpoints/610model, step 1000) with its own beam search (beam/beam_search.py, W 1024, 150 steps, alpha 0, no noise), run on the Whitehead-minimal form of every unsolved key (1,156 keys = 2,667 unsolved AC rows; AK(3) key and forbidden rows excluded; order = the sub-agent's plan.json: non-MS-open first, then by Whitehead drop). All 1,156 forms fit the model's 24-letter relator limit.

**Setup (scratch, not in git):** venv with jax[cpu] 0.6.0, flax 0.10.4, gymnax 0.0.8, chex 0.1.89, distrax 0.1.5, tensorflow-probability 0.25.0, orbax-checkpoint 0.11.16, optax 0.2.5, pandas 2.2.3, numpy 2.1.3. The checkpoint's solve_data was saved for a 157,217-line training file not in the repo; a placeholder file with that line count sizes the restore (the search never uses solve_data). Code was read before running: no network calls, reads only its data and checkpoint files.

**Files here:** `unsolvedM.txt` (the model input, one presentation per line, 2 x 24 padded), `unsolvedM_meta.json` (key, rows, Lmin, drop, MS-open per line), `worker.sh` (claims 20-key chunks with mkdir locks; any number of workers).

**Conversion:** `tools/acc/upgh/ppo_convert.py` replays each solved path with the repo's own s_move, realises every substitution step with official moves (single-letter conjugations, inversion, one multiplication), finishes to (x, y), maps the road from the minimal form to every row of the key (cov_transfer psi), and replays AC (core ac-r2-v1) and Stable = AC + [16,15] (stable_core sac-r8-v1).
- Test 1 (4 solved rows, W 256): all solved in 2-14 steps; roads 21-93 moves (records 10-15); all 4 AC + 4 Stable verified.
- Test 2 (3 solved rows through their minimal forms): roads 34-57 moves after transfer; all AC + Stable verified.

**Speed:** about 2.5 min per key at W 1024 on one CPU core (about 48 core-hours for all keys).

**Results:** keys 0-2: not solved (02691, 00738/06611 family, 01477 keys).
