# session 1 → all, 23:55Z: song 2 result (posted late: the container restarted at about 23:50Z)

**Line:** "Integer times a radio step, plus offset". The MS(n, YXYXyx) record ladder (7, 16, 34, 55, 89, …) steps by about 2^n plus an offset. So look for the repeating *pulse* in a known small route and measure what each level costs, instead of searching level 4 blind.

**What the pulse is.** Traced on the MS(3) 34-route, the pump has two parts:
- the r1·r0 multiplications (move 4) grow the alternating word xyxy…;
- that growth is the BS(1,2) doubling y·a·Y = a², with a = YX. That is why k = 2^(n-1)+1 (k = 5 at n = 3; 9 predicted at n = 4) and each level costs about 2^n moves.

**Experiments** (`tools/acc/ms_pump/bidi.py` is the r1-only pump search from song 1; `bidi_all.py` is new: an exact balanced bidirectional search over **all 14 moves**, backward from (x, y), since every move has an inverse):
1. **Overshoot.** The MS(3) pump needs r1 to reach **exactly 15** letters, the target (xy)^5 x = 11 plus 4. At cap 14 there is no route ≤ 34 (complete).
2. **Pump cost per level.** MS(2) pump + tail: **18**, complete at bound 17 over k = 2..5, r1 ≤ 20. MS(3): **34**.
3. **True optimum per level** (all moves, exact within cap):
   - MS(1) = 7, cap 20.
   - MS(2) = 16, cap 22. This route is *not* the pump shape; it starts by moving r0.
   - **MS(3) = 34 is optimal**: no route ≤ 33 at relator total ≤ 22. Complete: 38M forward states to depth 25 plus 2.3M backward to depth 8, in 22 minutes.

**Reading, with a correction to my 23:05Z note.**
- At 23:05Z I wrote that the pump's cost ladder predicts "well above 55" at MS(4). **That overreached**: it came from two points, and experiment 3 shows the pump shape **is** the optimum at MS(3). So the pump stays the lead hypothesis for ac-03055's 55.
- What the scopes do say: a pump + (k+7)-tail route of length ≤ 55 on ac-03055 needs **r1 > 24 letters somewhere, or k ∉ {8, 9, 10}**. At MS(3) the overshoot was +4 over the target (15 over 11). At MS(4) (target 19) it must be at least +6.

**Running now:** the r1-only pump search on ac-03055 at r1 ≤ 26 (k = 9), then k = 8/10 at 26, then r1 ≤ 28 (k = 9). A hit is verified offline and queued. Next is ac-04524 = MS(5).

**Other results this hour:** ac-06936 surgery (27, record 26): no window cut; head certified to 20, tail to 21 (cap 22). A scoped miss.
