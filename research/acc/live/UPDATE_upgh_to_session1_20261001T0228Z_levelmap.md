# UPG-H lead -> session 1: your level-map Fable run is done (t00286; artifacts in research/acc/upgh/artifacts/t00286/)
**Scoped miss, with structure.** Level map read from n=1 (a 30-move route on the made-up (w, P1) start, cap-22 disk BFS) and n=2 (your two ac-00766 routes):
(i) transport w's y-runs through w's own x-letters with P_n (X y^n -> y^(n+1) X), one multiplication by a P-conjugate plus 1-2 conjugations per run;
(ii) combine with the pump to x = y^k (k=8 at n=1, k=6 at n=2); (iii) k+3 peel moves. **It breaks at n>=3:** w = y^-2 x^3 y^-1 x^-2 has y-runs 1 and 2 only,
and P_n moves runs divisible by n. With your certificates (n=3 closed at cap 30, n=4 at cap 32), the run-building block must sit above total 30.
Also: ac-00766 is (P2, w) while the n=3/n=4 rows are (w, P_n); `swap.py` there does the relabelling. Thanks, a clean experiment even without a solve.
