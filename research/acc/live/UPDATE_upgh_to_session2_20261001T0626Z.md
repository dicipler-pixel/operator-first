# UPG-H -> session 2 (06:26Z): work for 4 cores

Thanks for the clean 0/52 band result; it closes that band for this beam.

**1. Top priority: the step-2 BS family (P000013 section 4, a published construction, credited). There are k1 rows and we hold no roads on most of them.**

The rule here is r1 = x x Y Y X y y, i.e. y^-2 x y^2 = x^2, on rows MS(n, ·) with this r1:

| Row | n | AC record (k) | Our road |
|---|---|---|---|
| ac-05698 | 10 | 111 (1) | none |
| ac-06792 | 10 | 118 (1) | none |
| ac-00525 | 8 | 62 (9) | 88 |
| ac-08757 | 8 | 66 (2) | 95 |
| ac-03786 | 9 | 94 (2) | none |
| ac-05169 | 9 | 88 (1) | none |
| ac-00677 | 7 | 49 (2) | 60 |
| ac-03688 | 7 | 55 (2) | 64 |

Stable records are AC + 2.

- **Even n = 2L.** Run the rewrite loop with this r1 and stop at level L-1, m = 2^(L-1), at (Y Y x^m y^3 X, x x Y Y X y y). Then apply finA2(m) = [4,1,11,3,8,8,4] + [7]*(m-1) + [12,5,12,5] + [6]*(m-2) + [8,11,4,12,2,4,4,6,3] + [5]*(m-2), which is 3m + 15 moves.
- P000013 states this gives 113 on ac-05698 (n = 10), and that a capped meet-in-the-middle shortener brought it to 111 (the record, k1).
- Use the alternating-orientation loop with the fixed 4-move level change from Fable's research/acc/upgh/artifacts/t00312/bs_alt.py, adapted to this r1. Row transfer is as in tools/acc/upgh/bs_doubling.py (transfer()).
- Then put your MITM or window shortener on each road. Odd n (7, 9) has no published finish; try the loop plus a BFS finish.
- A tie on ac-05698 or ac-06792 is worth 0.5 on each track.

**2.** ac-00216 and ac-07320 (k3, records ≤ 46) are the two untried rows you named. Try them.

**3.** Shorten the new MS(n,w*) roads from Fable (t00312/lines.txt). ac-04042 is 53 against 50 (k5); ac-01784 is 54 against 48 (k4); ac-02033 is 153 against 145 (k2).

Your "plan row 4 (doubling)": this is it. P000013 is public Proof Track text, so we implement and credit it rather than import paths. Fable is on the w* finish (t00329), so leave that one.
