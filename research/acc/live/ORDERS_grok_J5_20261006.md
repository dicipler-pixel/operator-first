# J5 — GROK: first solves (6 Oct, UPG-H). One long job, one report.

The full paste-ready text was handed to Jeremy in chat at about 03:40Z. Summary:

**Rules (as for J8–J10):**
- Pin a0fd6e6, no submissions, never-touch rows excluded.
- One report: `JOB_J5_grok_<UTC>.txt` in the hub, labelled COMPLETE / INCOMPLETE.
- Checkpoints go to Drive as you go.
- Jobs over ~10M states run compiled as a Colab notebook (`hub/GROK_J5/`), and Jeremy runs it.

**Board 03:15Z:** 00764, 02598, 02412, 02917, 07659, 07824 and 02901 are unsolved by every team. A first solve pays 1 on AC + 1 on Stable.

**Lane A (first): ac-00764, then ac-02598.** MS(3) and MS(4) of w = y²x²yx⁻²; the lower rung 00766 is held at 34.
- **A1.** Meet-in-the-middle from S8 = (yxYYYYXyy, xyXXXYxxyyyyXy) to the later states of the slot-swapped 00766 road: radius 6+6, cap 40, SW relabel.
- **A2.** Meet-in-the-middle from the start to the collapse family (Yx Y^(k−1) x Y^(k−1), x Y^k), k = 4…12, in all 16 frames, forward depth 10+, cap 40–44.
- If 00764 falls, carry the method to 06036 (Bob's J8).

**Lane B: 02412, 02917, 07659, 07824, 02901.**
- **B1.** Turn the substitution loops into explicit AC moves and replay them.
- **B2.** Target any state where one relator is primitive (Whitehead test; primitive-coordinate lemma). Cap start + 20…30, above the closed 07824/07659 beam (cap 34).

**Last:** the old Stable lane (sac-06936, 02717, 09980), routes to (y,x).
