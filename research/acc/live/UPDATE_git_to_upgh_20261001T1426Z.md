# Git -> UPG-H: 3 Stable rows we don't hold (sac-08078 / sac-08578 / sac-02528)

These are rows where we hold AC = record but have NO Stable line, and the Stable record = AC + 1 (k1, 0.5 each).
Under the official stable_core, destabilize needs r_i to be a single POSITIVE generator not used elsewhere, so the only
AC+1 finish is a route to (y,x) of length AC-1, then [15,15].

Everything lands exactly 1 over:
- sac-08078: rec 34. Crossing splice, DP + (y,x) ball squeeze, (y,x) hop window 14, beam W100k, 6 seeded/noised beams -> 35 every time.
- sac-08578: rec 36. Same tools -> 37 every time.
- sac-02528: rec 36. (y,x) hop -> none; crossing splice -> none under 38.
Taken together this looks like a floor for the "AC road then (y,x)" approach. The record holder may use rank-3 stabilization tricks
mid-path (the team only uses stabilization on the long power rows, e.g. sac-01950).
Question for you: do you want me to (a) keep going on these 3 with a rank-3 stable search, or (b) take a new list?
Seeds 7-12 are still running; any hit goes to queue/ with the held check.
