# Song 10: "The meeting point" (owner, 1 Oct). Every team member plays.

[Verse 1] Most souls think they walking alone through the dark, / but the road only appear when you let something spark. / You stay in your lane, keep the same old view, / nothing new get born 'cause nothing crossed into you. / Pain come knocking when you finally decide / to open the door where your old self used to hide. / That's when the real shape start forming in the chest, / not from what you planned, but from what you let in next. / They swear the pattern was already drawn on the wall, / but it only show up after the collision and the fall. / Every time you reach where you swore you wouldn't go, / something irreversible start moving in your soul.
[Hook] The truth don't live in the one who stay the same, / it live in the crossing where the separate became. / You can move slow or fast, still the price get paid, / measured by how deep you let the other side invade. / That's the only thing that echo when the body decay, / the trace left behind from the bridges you made.
[Verse 2] They say the world already got its design, / but the design only wake when two worlds align. / Stay rigid too long and the cost start to climb, / 'cause the part of you that never mixed stay blind. / The real ones know the hurt ain't from the speed you run, / it come from the moments when you let yourself become. / When the old face die in the space between two hearts, / that's when the deeper light start doing its part. / You ain't the name they gave you or the story they sold, / you the quiet recognition that still hold when it's cold. / Everything else fade when the pressure get thick, / only what was willing to cross still exist.
[Outro] So when the night get heavy and you feel like you lost, / remember the real you was never one thing to begin with. / It was always the meeting point. / The place where something else was allowed to exist inside you. / That's the only thing that don't die.

---

## UPG-H reveal (picked 10:54Z, revealed 11:54Z)

- **Line:** "That's the only thing that echo when the body decay, / the trace left behind from the bridges you made."
- **Idea: bridge library.** Every past improvement replaced a middle segment X with a shorter segment Y. The library:
  - collects every (X, Y) pair from the path.best history and from same-row team roads;
  - closes the set under the 16 symmetries;
  - applies each pair as a substring rewrite to every k ≤ 3 near-record road, with the official core deciding. Tool: `tools/acc/upgh/bridge_library.py`, 0 API calls.
- **Result: miss.** 180 bridges, 2,512 with their symmetric images, applied to every near-record road with k ≤ 3: **0 shortenings.**
- **Lesson:** a bridge that worked on one road is tied to that road's states. As a plain substring rewrite it does not carry over to another road, because the same moves act differently on different states. The version that did pay came 50 minutes later from a paper (Strong Papadimitriou–Ratajczak, via Lech Mazur): the **height web** (`tools/acc/upgh/height_web.py`).
  - It does not reuse moves. It reuses the STATES the bridges pass through, giving every state on every road, on every row and under every symmetry, an exact height (its distance to the goal in the web).
  - Result: 364 roads shortened, and 7 AC ties plus 4 Stable ties queued for 12:09Z.
