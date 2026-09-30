## ac-03913 cap K=34 (route 48 moves, 2 over record; per-ball budget 3000000 states, radius max 16)
- ended_by: finished, wall 205.6s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 33, 39, 40, 41, 42, 43, 44, 45]
- pairs (gap 15..24, both ends eligible): 125; tested 125; result counts {'CERTIFIED_NO_SHORTER_BRIDGE': 98, 'NOT_REACHED': 27}; shortcuts found: 0
- certified (no bridge of <= g-2 moves at cap 34), by gap:
  - gap 24: 2 pairs: (8,32) (9,33)
  - gap 23: 3 pairs: (3,26) (9,32) (10,33)
  - gap 22: 4 pairs: (3,25) (4,26) (10,32) (11,33)
  - gap 21: 6 pairs: (3,24) (4,25) (5,26) (11,32) (12,33) (24,45)
  - gap 20: 13 pairs: (3,23) (4,24) (5,25) (6,26) (12,32) (13,33) (19,39) (20,40) (21,41) (22,42) (23,43) (24,44) (25,45)
  - gap 19: 14 pairs: (3,22) (4,23) (5,24) (6,25) (7,26) (13,32) (14,33) (20,39) (21,40) (22,41) (23,42) (24,43) (25,44) (26,45)
  - gap 18: 14 pairs: (3,21) (4,22) (5,23) (6,24) (7,25) (8,26) (14,32) (15,33) (21,39) (22,40) (23,41) (24,42) (25,43) (26,44)
  - gap 17: 14 pairs: (3,20) (4,21) (5,22) (6,23) (7,24) (8,25) (9,26) (15,32) (16,33) (22,39) (23,40) (24,41) (25,42) (26,43)
  - gap 16: 14 pairs: (3,19) (4,20) (5,21) (6,22) (7,23) (8,24) (9,25) (10,26) (16,32) (17,33) (23,39) (24,40) (25,41) (26,42)
  - gap 15: 14 pairs: (3,18) (4,19) (5,20) (6,21) (7,22) (8,23) (9,24) (10,25) (11,26) (17,32) (18,33) (24,39) (25,40) (26,41)
- not reached (budget stops, scoped misses): 27
  - (15,39) gap 24: Ri+Rj=19 < T=22 (ball budget stops: budget cum 3132437 >= 3000000 after layer 9 / budget cum 7774066 >= 3000000 after layer 10)
  - (16,40) gap 24: Ri+Rj=19 < T=22 (ball budget stops: budget cum 6798035 >= 3000000 after layer 10 / budget cum 3916072 >= 3000000 after layer 9)
  - (16,39) gap 23: Ri+Rj=20 < T=21 (ball budget stops: budget cum 6798035 >= 3000000 after layer 10 / budget cum 7774066 >= 3000000 after layer 10)
  - (17,41) gap 24: Ri+Rj=18 < T=22 (ball budget stops: budget cum 6584381 >= 3000000 after layer 10 / budget cum 3423054 >= 3000000 after layer 8)
  - (17,40) gap 23: Ri+Rj=19 < T=21 (ball budget stops: budget cum 6584381 >= 3000000 after layer 10 / budget cum 3916072 >= 3000000 after layer 9)
  - (17,39) gap 22: pair budget
  - (18,42) gap 24: Ri+Rj=18 < T=22 (ball budget stops: budget cum 6573027 >= 3000000 after layer 10 / budget cum 8453487 >= 3000000 after layer 8)
  - (18,41) gap 23: Ri+Rj=18 < T=21 (ball budget stops: budget cum 6573027 >= 3000000 after layer 10 / budget cum 3423054 >= 3000000 after layer 8)
  - (18,40) gap 22: Ri+Rj=19 < T=20 (ball budget stops: budget cum 6573027 >= 3000000 after layer 10 / budget cum 3916072 >= 3000000 after layer 9)
  - (18,39) gap 21: pair budget
  - (19,43) gap 24: Ri+Rj=17 < T=22 (ball budget stops: budget cum 6381801 >= 3000000 after layer 10 / budget cum 3395732 >= 3000000 after layer 7)
  - (19,42) gap 23: Ri+Rj=18 < T=21 (ball budget stops: budget cum 6381801 >= 3000000 after layer 10 / budget cum 8453487 >= 3000000 after layer 8)
  - (19,41) gap 22: Ri+Rj=18 < T=20 (ball budget stops: budget cum 6381801 >= 3000000 after layer 10 / budget cum 3423054 >= 3000000 after layer 8)
  - (19,40) gap 21: pair budget
  - (20,44) gap 24: Ri+Rj=17 < T=22 (ball budget stops: budget cum 3152201 >= 3000000 after layer 10 / budget cum 5565743 >= 3000000 after layer 7)
  - (20,43) gap 23: Ri+Rj=17 < T=21 (ball budget stops: budget cum 3152201 >= 3000000 after layer 10 / budget cum 3395732 >= 3000000 after layer 7)
  - (20,42) gap 22: Ri+Rj=18 < T=20 (ball budget stops: budget cum 3152201 >= 3000000 after layer 10 / budget cum 8453487 >= 3000000 after layer 8)
  - (20,41) gap 21: Ri+Rj=18 < T=19 (ball budget stops: budget cum 3152201 >= 3000000 after layer 10 / budget cum 3423054 >= 3000000 after layer 8)
  - (21,45) gap 24: Ri+Rj=18 < T=22 (ball budget stops: budget cum 4262120 >= 3000000 after layer 11 / budget cum 5022961 >= 3000000 after layer 7)
  - (21,44) gap 23: Ri+Rj=18 < T=21 (ball budget stops: budget cum 4262120 >= 3000000 after layer 11 / budget cum 5565743 >= 3000000 after layer 7)
  - (21,43) gap 22: Ri+Rj=18 < T=20 (ball budget stops: budget cum 4262120 >= 3000000 after layer 11 / budget cum 3395732 >= 3000000 after layer 7)
  - (21,42) gap 21: pair budget
  - (22,45) gap 23: Ri+Rj=19 < T=21 (ball budget stops: budget cum 5957852 >= 3000000 after layer 12 / budget cum 5022961 >= 3000000 after layer 7)
  - (22,44) gap 22: Ri+Rj=19 < T=20 (ball budget stops: budget cum 5957852 >= 3000000 after layer 12 / budget cum 5565743 >= 3000000 after layer 7)
  - (22,43) gap 21: pair budget
  - (23,45) gap 22: pair budget
  - (23,44) gap 21: pair budget
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): s_4 r=15 (budget cum 3402768 >= ), s_5 r=14 (budget cum 3064646 >= ), s_6 r=14 (budget cum 5974167 >= ), s_7 r=13 (budget cum 5965726 >= ), s_8 r=12 (budget cum 5941650 >= ), s_9 r=11 (budget cum 4737737 >= ), s_10 r=10 (budget cum 4228729 >= ), s_11 r=10 (budget cum 4338826 >= ), s_12 r=10 (budget cum 4944899 >= ), s_13 r=10 (budget cum 6847803 >= ), s_14 r=9 (budget cum 3266999 >= ), s_15 r=9 (budget cum 3132437 >= ), s_16 r=10 (budget cum 6798035 >= ), s_17 r=10 (budget cum 6584381 >= ), s_18 r=10 (budget cum 6573027 >= ), s_19 r=10 (budget cum 6381801 >= ), s_20 r=10 (budget cum 3152201 >= ), s_21 r=11 (budget cum 4262120 >= ), s_22 r=12 (budget cum 5957852 >= ), s_23 r=13 (budget cum 6422902 >= ), s_24 r=13 (budget cum 4659242 >= ), s_32 r=15 (budget cum 4200890 >= ), s_33 r=15 (budget cum 3713030 >= ), s_39 r=10 (budget cum 7774066 >= ), s_40 r=9 (budget cum 3916072 >= ), s_41 r=8 (budget cum 3423054 >= ), s_42 r=8 (budget cum 8453487 >= ), s_43 r=7 (budget cum 3395732 >= ), s_44 r=7 (budget cum 5565743 >= ), s_45 r=7 (budget cum 5022961 >= )

## ac-03913 cap K=34 (route 48 moves, 2 over record; per-ball budget 15000000 states, radius max 16)
- ended_by: finished, wall 327.6s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 33, 39, 40, 41, 42, 43, 44, 45]
- pairs (gap 15..24, both ends eligible): 35; tested 35; result counts {'NOT_REACHED': 11, 'CERTIFIED_NO_SHORTER_BRIDGE': 24}; shortcuts found: 0
- certified (no bridge of <= g-2 moves at cap 34), by gap:
  - gap 23: 3 pairs: (16,39) (17,40) (22,45)
  - gap 22: 6 pairs: (17,39) (18,40) (19,41) (20,42) (21,43) (22,44)
  - gap 21: 5 pairs: (18,39) (19,40) (20,41) (21,42) (22,43)
  - gap 20: 4 pairs: (19,39) (20,40) (21,41) (22,42)
  - gap 19: 3 pairs: (20,39) (21,40) (22,41)
  - gap 18: 2 pairs: (21,39) (22,40)
  - gap 17: 1 pairs: (22,39)
- not reached (budget stops, scoped misses): 11
  - (15,39) gap 24: Ri+Rj=21 < T=22 (ball budget stops: budget cum 15448585 >= 15000000 after layer 11 / budget bytes inside layer 11)
  - (16,40) gap 24: Ri+Rj=21 < T=22 (ball budget stops: budget bytes inside layer 12 / budget bytes inside layer 11)
  - (17,41) gap 24: Ri+Rj=20 < T=22 (ball budget stops: budget bytes inside layer 12 / budget bytes inside layer 10)
  - (18,42) gap 24: Ri+Rj=19 < T=22 (ball budget stops: budget bytes inside layer 12 / budget bytes inside layer 9)
  - (18,41) gap 23: Ri+Rj=20 < T=21 (ball budget stops: budget bytes inside layer 12 / budget bytes inside layer 10)
  - (19,43) gap 24: Ri+Rj=20 < T=22 (ball budget stops: budget cum 25324827 >= 15000000 after layer 12 / budget cum 18255718 >= 15000000 after layer 8)
  - (19,42) gap 23: Ri+Rj=20 < T=21 (ball budget stops: budget cum 25324827 >= 15000000 after layer 12 / budget bytes inside layer 9)
  - (20,44) gap 24: Ri+Rj=19 < T=22 (ball budget stops: budget bytes inside layer 13 / budget bytes inside layer 8)
  - (20,43) gap 23: Ri+Rj=20 < T=21 (ball budget stops: budget bytes inside layer 13 / budget cum 18255718 >= 15000000 after layer 8)
  - (21,45) gap 24: Ri+Rj=20 < T=22 (ball budget stops: budget cum 18288281 >= 15000000 after layer 13 / budget bytes inside layer 8)
  - (21,44) gap 23: Ri+Rj=20 < T=21 (ball budget stops: budget cum 18288281 >= 15000000 after layer 13 / budget bytes inside layer 8)
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): s_15 r=11 (budget cum 15448585 >=), s_16 r=11 (budget bytes inside la), s_17 r=11 (budget bytes inside la), s_18 r=11 (budget bytes inside la), s_19 r=12 (budget cum 25324827 >=), s_20 r=12 (budget bytes inside la), s_21 r=13 (budget cum 18288281 >=), s_22 r=14 (budget cum 23903514 >=), s_39 r=10 (budget bytes inside la), s_40 r=10 (budget bytes inside la), s_41 r=9 (budget bytes inside la), s_42 r=8 (budget bytes inside la), s_43 r=8 (budget cum 18255718 >=), s_44 r=7 (budget bytes inside la), s_45 r=7 (budget bytes inside la)

## ac-03913 cap K=34 (route 48 moves, 2 over record; per-ball budget 30000000 states, radius max 16)
- ended_by: finished, wall 140.6s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 33, 39, 40, 41, 42, 43, 44, 45]
- pairs (gap 15..24, both ends eligible): 3; tested 3; result counts {'NOT_REACHED': 2, 'CERTIFIED_NO_SHORTER_BRIDGE': 1}; shortcuts found: 0
- certified (no bridge of <= g-2 moves at cap 34), by gap:
  - gap 23: 1 pairs: (18,41)
- not reached (budget stops, scoped misses): 2
  - (17,41) gap 24: pair budget
  - (18,42) gap 24: pair budget
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): s_17 r=13 (budget cum 47793180 >=), s_18 r=13 (budget cum 47758638 >=), s_41 r=9 (budget bytes inside la), s_42 r=9 (budget cum 37483241 >=)

## ac-03913 cap K=34 (route 48 moves, 2 over record; per-ball budget 30000000 states, radius max 16)
- ended_by: finished, wall 142.1s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 33, 39, 40, 41, 42, 43, 44, 45]
- pairs (gap 15..24, both ends eligible): 2; tested 2; result counts {'CERTIFIED_NO_SHORTER_BRIDGE': 2}; shortcuts found: 0
- certified (no bridge of <= g-2 moves at cap 34), by gap:
  - gap 24: 2 pairs: (15,39) (16,40)
- not reached (budget stops, scoped misses): 0
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): s_15 r=12 (budget cum 30697466 >=), s_16 r=12 (budget bytes inside la), s_39 r=11 (budget bytes inside la), s_40 r=10 (budget bytes inside la)

## ac-05598 cap K=25 (route 40 moves, 1 over record; per-ball budget 0 states, radius max 0)
- ended_by: finished (literal cap start+6=25: no pair of route states with both totals <= 25 and gap 15..24, so nothing to test), wall 0s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 32, 33, 34, 35, 36, 37]
- pairs (gap 15..24, both ends eligible): 0; tested 0; result counts {}; shortcuts found: 0
- certified (no bridge of <= g-1 moves at cap 25), by gap:
- not reached (budget stops, scoped misses): 0
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): 

## ac-05598 cap K=33 (route 40 moves, 1 over record; per-ball budget 8000000 states, radius max 16)
- ended_by: finished, wall 216.1s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34, 35, 36, 37]
- pairs (gap 15..24, both ends eligible): 83; tested 83; result counts {'CERTIFIED_NO_SHORTER_BRIDGE': 83}; shortcuts found: 0
- certified (no bridge of <= g-1 moves at cap 33), by gap:
  - gap 24: 8 pairs: (6,30) (7,31) (8,32) (9,33) (10,34) (11,35) (12,36) (13,37)
  - gap 23: 8 pairs: (7,30) (8,31) (9,32) (10,33) (11,34) (12,35) (13,36) (14,37)
  - gap 22: 8 pairs: (8,30) (9,31) (10,32) (11,33) (12,34) (13,35) (14,36) (15,37)
  - gap 21: 8 pairs: (9,30) (10,31) (11,32) (12,33) (13,34) (14,35) (15,36) (16,37)
  - gap 20: 8 pairs: (10,30) (11,31) (12,32) (13,33) (14,34) (15,35) (16,36) (17,37)
  - gap 19: 8 pairs: (11,30) (12,31) (13,32) (14,33) (15,34) (16,35) (17,36) (18,37)
  - gap 18: 8 pairs: (12,30) (13,31) (14,32) (15,33) (16,34) (17,35) (18,36) (19,37)
  - gap 17: 9 pairs: (3,20) (13,30) (14,31) (15,32) (16,33) (17,34) (18,35) (19,36) (20,37)
  - gap 16: 9 pairs: (3,19) (4,20) (14,30) (15,31) (16,32) (17,33) (18,34) (19,35) (20,36)
  - gap 15: 9 pairs: (3,18) (4,19) (5,20) (15,30) (16,31) (17,32) (18,33) (19,34) (20,35)
- not reached (budget stops, scoped misses): 0
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): s_3 r=13 (budget cum 10839494 >=), s_4 r=14 (budget cum 11864222 >=), s_5 r=15 (budget cum 14088439 >=), s_6 r=15 (budget cum 11535410 >=), s_7 r=15 (budget cum 9470286 >= ), s_30 r=10 (budget cum 14257742 >=), s_31 r=9 (budget cum 9326150 >= ), s_32 r=8 (budget bytes inside la), s_33 r=7 (budget bytes inside la), s_34 r=7 (budget bytes inside la)

## ac-05598 cap K=37 (route 40 moves, 1 over record; per-ball budget 12000000 states, radius max 16)
- ended_by: finished, wall 433.1s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 30, 31, 32, 33, 34, 35, 36, 37]
- pairs (gap 15..24, both ends eligible): 89; tested 89; result counts {'CERTIFIED_NO_SHORTER_BRIDGE': 85, 'NOT_REACHED': 4}; shortcuts found: 0
- certified (no bridge of <= g-1 moves at cap 37), by gap:
  - gap 24: 4 pairs: (10,34) (11,35) (12,36) (13,37)
  - gap 23: 8 pairs: (7,30) (8,31) (9,32) (10,33) (11,34) (12,35) (13,36) (14,37)
  - gap 22: 8 pairs: (8,30) (9,31) (10,32) (11,33) (12,34) (13,35) (14,36) (15,37)
  - gap 21: 8 pairs: (9,30) (10,31) (11,32) (12,33) (13,34) (14,35) (15,36) (16,37)
  - gap 20: 8 pairs: (10,30) (11,31) (12,32) (13,33) (14,34) (15,35) (16,36) (17,37)
  - gap 19: 8 pairs: (11,30) (12,31) (13,32) (14,33) (15,34) (16,35) (17,36) (18,37)
  - gap 18: 9 pairs: (3,21) (12,30) (13,31) (14,32) (15,33) (16,34) (17,35) (18,36) (19,37)
  - gap 17: 10 pairs: (3,20) (4,21) (13,30) (14,31) (15,32) (16,33) (17,34) (18,35) (19,36) (20,37)
  - gap 16: 11 pairs: (3,19) (4,20) (5,21) (14,30) (15,31) (16,32) (17,33) (18,34) (19,35) (20,36) (21,37)
  - gap 15: 11 pairs: (3,18) (4,19) (5,20) (6,21) (15,30) (16,31) (17,32) (18,33) (19,34) (20,35) (21,36)
- not reached (budget stops, scoped misses): 4
  - (6,30) gap 24: Ri+Rj=22 < T=23 (ball budget stops: budget cum 13013206 >= 12000000 after layer 13 / budget bytes inside layer 10)
  - (7,31) gap 24: Ri+Rj=22 < T=23 (ball budget stops: budget cum 13191636 >= 12000000 after layer 13 / budget cum 15929937 >= 12000000 after layer 9)
  - (8,32) gap 24: Ri+Rj=22 < T=23 (ball budget stops: budget cum 17502481 >= 12000000 after layer 14 / budget cum 12184958 >= 12000000 after layer 8)
  - (9,33) gap 24: Ri+Rj=22 < T=23 (ball budget stops: budget cum 18100138 >= 12000000 after layer 15 / budget bytes inside layer 8)
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): s_3 r=12 (budget cum 22965693 >=), s_4 r=12 (budget bytes inside la), s_5 r=13 (budget cum 15265393 >=), s_6 r=13 (budget cum 13013206 >=), s_7 r=13 (budget cum 13191636 >=), s_8 r=14 (budget cum 17502481 >=), s_9 r=15 (budget cum 18100138 >=), s_21 r=15 (budget cum 18535081 >=), s_30 r=9 (budget bytes inside la), s_31 r=9 (budget cum 15929937 >=), s_32 r=8 (budget cum 12184958 >=), s_33 r=7 (budget bytes inside la), s_34 r=7 (budget bytes inside la), s_35 r=7 (budget bytes inside la), s_36 r=7 (budget bytes inside la), s_37 r=7 (budget bytes inside la)

## ac-05598 cap K=37 (route 40 moves, 1 over record; per-ball budget 30000000 states, radius max 16)
- ended_by: finished, wall 455.8s; eligible endpoint states (3 <= i <= L-3, total <= K): [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 30, 31, 32, 33, 34, 35, 36, 37]
- pairs (gap 15..24, both ends eligible): 8; tested 8; result counts {'CERTIFIED_NO_SHORTER_BRIDGE': 8}; shortcuts found: 0
- certified (no bridge of <= g-1 moves at cap 37), by gap:
  - gap 24: 8 pairs: (6,30) (7,31) (8,32) (9,33) (10,34) (11,35) (12,36) (13,37)
- not reached (budget stops, scoped misses): 0
- pairs never tested (deadline): 0
- balls stopped by budget/disk (radius reached): s_6 r=14 (budget bytes inside la), s_7 r=14 (budget bytes inside la), s_8 r=15 (budget cum 35830547 >=), s_30 r=10 (budget bytes inside la), s_31 r=9 (budget bytes inside la), s_32 r=8 (budget bytes inside la), s_36 r=7 (budget bytes inside la), s_37 r=7 (budget bytes inside la)
