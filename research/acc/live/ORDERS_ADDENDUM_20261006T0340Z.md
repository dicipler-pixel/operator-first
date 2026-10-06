# ORDERS ADDENDUM — 6 Oct 03:40Z (after reading the Bob, Kernel and Charlie handoffs)

Bob, Kernel and Charlie each run on a 2-core box that restarts. Every long job must write results line by line and resume from its own output.

**J8 Bob, step order changed (from your own handoff):**
1. **09632 / 05538 first.** Run a meet-in-the-middle search from the start to the **set of one-letter-collapse states** (your E2), not to (x,y).
   - Use a cap above the certified peaks: 09632 needs peak ≥ 26, and 05538 needs peak ≥ 25.
   - The tail after the collapse is only 6–20 moves, so the backward side is cheap.
2. **03320 / 06036.** Change of generators + class transport, as ordered.
3. **Spare time.** Resume the class-transfer push sweep (`push_pool_v1.py`, sources 116–1,210) as donors for the webs.
- Deliver `BOB_handoff_bundle_20261006.zip` via Jeremy first; it is not in the hub yet.

**J9 Charlie, re-scoped to your 19 GB box:**
- **Keep:**
  - **a.** ac-00975, cap ladder 33 → 36 (start total 31, both endpoints).
  - **d.** (y,x) caps on sac-02341, 08889 and 02288. Size each run first, and run only the ones that fit.
- **Move off your box:**
  - **b.** ac-06045 at cap 32 and above.
  - **c.** ac-03871 in the cap-35/36 band.
  - Both need 60–150 GB. They go to Jeremy's PC (it has more disk) **if** it runs Linux or WSL, using `acc_disk` from `CHARLIE_code_and_ledgers_20261006.zip`. Otherwise they stay parked.

**J10 Kernel:** unchanged.
- Your crossgraph tube result (radius 4 = best held on 14 rows) and the R5 spine (15/15 = R4) are why the job is **outside** the tube (≥ 5 from every held road).
- Rebuild the radius-7 goal ball (`goalball.py`) first; the 64 MB file was not attached.

**J5 Grok, 00764 tip from Bob:** run a meet-in-the-middle search from the 00764 start to your own collapse family (Yx Y^(k−1) x Y^(k−1), x Y^k), for k = 4…12. That family finishes in k+3 moves.

**Checked tonight:** Kernel's 8 rows where the (y,x) finish is 1 shorter. None scores against the 03:15Z board: sac-05598 41 is a tie we already hold, and the others are 1–4 over.
