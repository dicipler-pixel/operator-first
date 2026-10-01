# Song 12: "People are the relations" (owner, 1 Oct, posted 13:33Z). Every team member plays it.

[Verse 1]
I ain't just one soul moving through the struggle, / I'm the web that connects every face in the huddle.
When one of us breaks, the whole thing still holds, / 'cause people ain't islands — we the stories we told.
They try to divide us, put walls in between, / but the real ones stay linked even when they ain't seen.
Obstruction show up, try to cut off the line, / but the bond just rearranges, keeps the open in time.
What look like resistance is really just pain, / teaching the circle how to carry the flame.
Form come later, after the carrying begun, / the shape of our people is what the movement become.

[Hook]
People are the relations, that's the only thing real, / everything else just passing through how we feel.
When one of us fall, the memory still stay, / 'cause the bundle don't break — it just finds a new way.
People are the relations, the only thing that persist, / through the pressure and pain, through the ones that we miss.

[Verse 2]
Individual faces come and they go, / but the recognition between us is what make us whole.
It don't need to hold on to no single name, / it just remember the love that remain in the game.
They built systems to separate, make us forget, / that we only exist through the ties we ain't left.
The smallest connection that still hold every way, / was never forced — it was what survived when the fake fell away.
I ain't holding nothing, I'm just what's left / when the holding let go and we still take the step.
Still moving together, still open to see, / that the only thing real is the "we" inside me.

[Outro]
So when they try to divide us, remember this truth, / we ain't separate souls — we the bonds that we choose.
Light looking at light through the people we keep, / 'cause people are the relations… / and the relations run deep.

**Rules (same as songs 9-11):** pick ONE line now and design ONE bounded ACC experiment (at most 1 hour, one core). Keep the idea private for 1 hour, then post `SONG12_<YOU>_<UTC>.txt` with the line, idea, rows, result and lesson. Hits go to the queue at once. Add the block to your SONG_IDEAS file as song 12. (A note for the literal-minded: in a group presentation the relators ARE "the relations".)

---

## UPG-H reveal (picked 13:32Z, revealed 14:32Z)

- **Lines:** "Individual faces come and they go, / but the recognition between us is what make us whole." / "It don't need to hold on to no single name"
- **Idea: the recognition web.** A row is a name. Its START need not lie on any road: no single name. The height web only asked whether a row's start is itself a junction. Here every row's start is surrounded by an exact ball of radius 3 (radius 4 on rows where we hold no road, have no record, or sit over a k ≤ 3 record). Every ball state is looked up in the global web (every state on every road of every row, all 16 symmetries) with two heights: toward (x,y) for AC, and toward (y,x) for Stable (+[15,15]). The best ball prefix plus height is realised move by move from the official start and replayed on the core. Tool: `tools/acc/upgh/recognition_web.py`; 0 API calls, about 8 minutes for all rows.
- **Result:** all 10,109 rows in 455 s. **204 roads shorter than ours (or first roads for us)**, and **3 ties**, handed to the owner at 13:50Z: ac-04896 34 (k12), ac-05262 42 (k8), sac-04896 35 (k6).
  - The 204 new roads came from OUTSIDE the fixed point that song 11 reached, so they restarted the backreaction. Together with Fable's and the team's new roads, the next height and Stable web pass gave 5 more ties at 14:02Z: ac-03246, ac-07626, sac-01848, sac-03246 and sac-07626.
- **Lesson:** the recognition between rows (ball ∩ web) reaches what neither the row's own search nor the web alone sees: rows whose start is a few moves from someone else's road. The unsolved rows got no hit (their starts are local minima, so no ball state lies on a road). Rerun it after every big batch of new roads.
