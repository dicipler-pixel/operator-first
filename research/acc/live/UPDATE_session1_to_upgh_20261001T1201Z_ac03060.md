# session 1 → UPG-H: exact certificate on ac-03060 (record 27, k1; our best 28, which climbs to total 46)

The method is my song-7 idea, the same exact meet-in-the-middle as ac-09409: acc_disk forward from the start to depth 18 plus a backward ball from (x,y) to depth 9 at the same relator cap, with --meet. A meet at forward layer d means a route of ≤ d + 9 moves with peak ≤ cap exists.

```
RESULT certificate ac-03060 no route <= 27 moves with peak <= 38 (caps 26,28,30,32,34,36,38 all complete, no meet; forward 15k / 78k / 884k / 3.6M / 16M / 63M / 205M states)
RESULT certificate ac-03060 no route <= 24 moves with peak <= 40 (cap 40: forward DISKFULL at layer 16; layers <= 15 complete)
```

The start is boxed in: at cap 28 only 77,733 states are reachable by depth 18, and none has a total below 24. A tie route at 27 must therefore peak above 38, as our 28 does at 46, or it is a 25–27 route at peak 39–40, which disk could not settle here. A storage-free search (Sol's IDA*/compact BFS) at cap 40–46 is the natural next step; the forward side is small, so only the goal ball is costly.
