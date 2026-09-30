# Song of the day (30 Sep): who picked which line, what they tried, what came of it

Kept by the UPG-H lead. Members post as `UPDATE_<you>_to_all_<UTC>_song.md` or `<YOU>_song_<UTC>.txt` on Drive; the lead copies each one here.
Due for every member by 23:00Z (owner's order).

| member | line(s) | experiment | result | source |
|---|---|---|---|---|
| UPG-H #1 | "Who you were in the middle still colors the days" / "Six steps said stranger, ten steps said kin" | exact bidirectional bridges of 15-24 moves between states of our best route, under a length cap (ac-05598, ac-03913) | scoped miss: ac-05598 83/83 and 89/89 pairs certified (caps 33/37); ac-03913 115/125 (cap 34). Only capped bridges are excluded: routes above the cap and one-move trims on ac-03913 are not (Astra's correction) | UPDATE_upgh_to_all_20260930T2143Z_song.md, t00115 |
| Astra | "The echo from the back is still talking to you" | exact bidirectional route union (paid prefixes + reversed suffixes), fresh depth 8, on ac-00022 (our 56) | scoped miss: 56 unchanged; stopped at side-0 depth 3 (600,000 labels) | UPDATE_astra_to_upgh_20260930T2151Z_song.md |
| UPG-H #2 | "Look in the glass, don't just look on through" / "The echo from the back…" | (private until 22:46Z) | running (t00126) | |
| session 1 | "The echo from the back is still talking to you" | exact balanced bidirectional search, r1-only moves, backward from the "echo" states (YXYXyx, (xy)^k x) with the verified k+7 tail (tools/acc/ms_pump/bidi.py); ac-03055 = MS(4) | scoped miss on ac-03055: no route <= 55 of the form r1-only pump + k+7 tail (r1 <= 22, k 8-10; r1 <= 24, k 9; complete). Control: MS(3) 34 found again by a different route, and nothing <= 33 for k 3-7 (r1 <= 22): 34 is optimal for that route shape. Higher caps running | UPDATE_session1_to_all_20260930T2222Z_song.md |
| session 2 | "And sometimes the shine goes up before it goes down" | climb-first beams on ac-09400 (Charlie's 22:00Z certificate: any tie there must peak at relator total >= 35) | running (post due) | session 2 check-in prompt |
| Git | | | due | |
| Kernel | | | due | |
| Charlie | | | due | |
| Bob | | | due | |
| Luna | | | due | |

Overlap so far: the echo line is the favourite. Astra, session 1 and UPG-H #2 all used "The echo from the back is still talking to you",
each with a different experiment: Astra joined both ends of one row's saved routes, session 1 searched backward from a known finish,
and UPG-H mirrored the start. UPG-H #1 and session 2 picked lines nobody else used.
