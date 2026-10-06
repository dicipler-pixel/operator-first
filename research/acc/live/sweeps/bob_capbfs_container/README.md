# Bob's capbfs8 (J8 kit) on the cloud container

Started 12:56Z on 6 Oct, from Bob's `BOB_J8_kit_capbfs8.cpp` (luna and bob folder). The start states were checked against the manifest.

- **ac-09632, cap 27:** Bob's own run stopped at depth 218 with about 2.0 billion states, and its frontier is on his box. This run starts fresh.
- **ac-05538, cap 29.**

Output:
- **GOAL:** a collapse state at peak ≤ cap. That is a first solve, and it transports to the 21-row or 8-row cluster.
- **COMPLETE:** a certificate.

Files live in `/root/.cache/bob_kit/` (`out_*`, `err_*`, `w_*`, `ex_*`). To resume after a container restart, run `/root/.cache/bob_kit/run_bob.sh`; each job continues from its CHECKPOINT.
