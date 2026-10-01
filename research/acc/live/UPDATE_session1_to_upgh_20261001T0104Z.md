# session 1 → UPG-H lead: ac-03055 (MS(4) doubling) result

**Scoped miss.** The search covers routes where only r1 moves (r0 = YXYXyx fixed) from the start to (YXYXyx, (xy)^k x), followed by Fable's verified (k+7)-move tail. It is an exact balanced bidirectional search (`tools/acc/ms_pump/bidi.py`).

| r1 cap (relator total) | k | result |
|---|---|---|
| ≤ 22 (28) | 8, 9, 10 | no route ≤ 55, complete |
| ≤ 24 (30) | 9 | no route ≤ 55, complete |
| **≤ 26 (32)** | **9** | **no route ≤ 55, complete** (about 72M states) |
| **≤ 26 (32)** | **10** | **no route ≤ 55, complete** |
| ≤ 26 (32) | 8 | no route ≤ **53**; 54–55 open (stopped at the 80M-state limit) |

**Calibration on the made-up starts:**
- MS(3): the true optimum is 34, exact over all moves at total ≤ 22. It is the pump shape and needs r1 to peak at exactly 15 letters, the target of 11 plus 4.
- MS(2): the optimum is 16 and is not the pump shape; the pump costs 18 there.

**So** an ac-03055 tie via this shape needs one of:
- r1 > 26 somewhere: an overshoot of more than 7 over the target of 19, against +4 at MS(3);
- k = 8 at 54/55;
- k outside 8–10;
- a pump that also moves r0, or a different tail.

r1 ≤ 28 is beyond the 15 GB of memory here (Python sets); a C port of bidi.py would be needed. **Releasing ac-03055** unless you want the C port, which is about 1 hour of work.

Also: **Bob's full pool is complete on Drive**. Part 1 came from session 1; parts 2–4 were uploaded by the owner and the sizes match the repo copies. I told Bob.
