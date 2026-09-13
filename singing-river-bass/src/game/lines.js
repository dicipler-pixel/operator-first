// src/game/lines.js
//
// Every line she says. Verbatim from 13_VOICE_v2.md — original writing, none
// of it lifted from a film.
//
// Dry, unfiltered, warm underneath. Not a cartoon southern grandmother — no
// biscuits, no "bless your heart." A woman who says what she thinks and is
// comfortable where she is.
//
// TWO LINES ARE HIS AND ARE MARKED. Do not rewrite them, do not add
// alternates, do not "correct" them.

export const LINES = {
  // "Don't tell my sister." is HIS, and leads. MY, not YOUR — that one word
  // decides who the player is. `Your sister` makes her a parent scolding you;
  // `my sister` makes the player her accomplice, someone she is letting in on
  // something. Do not "correct" it.
  crackBeer: [
    "Don't tell my sister.",
    "That's the good stuff.",
    "Somebody's got to drink 'em.",
    "Well, I earned it.",
    "I'm not sharing.",
    "This is the good part right here.",
  ],

  // Fires only once the heat has built a while.
  hot: [
    "Hoo. It's a hot one.",
    "Lord, it's close out here.",
    "That helped.",
  ],

  water: [
    "Fine. Water.",
    "I'm being good.",
    "Don't look at me like that.",
  ],

  // HIS, and the only empty-cooler line there is. `always` is the whole joke —
  // it makes this a standing grievance she has clearly voiced before rather
  // than a moment of discovery, so it works the first time the cooler runs dry
  // and every time after. NO ALTERNATES. NO CYCLING. A catchphrase that varies
  // is not a catchphrase.
  coolerEmpty: "Why is the beer always gone?",

  // Small fish. Not in 13_VOICE_v2.md, which covers Walter and the cooler —
  // these are the placeholder slots that still need her real voice.
  smallCatch: [
    "There we go.",
    "Well, hello.",
    "Little one.",
    "That's a start.",
  ],
  goodCatch: [
    "Now that's a fish.",
    "Look at you.",
    "Oh, that's a good one.",
  ],
  // A fish that throws the hook. Rueful, never a failure.
  gotOff: [
    "He got off.",
    "Ah, shoot.",
    "Slippery devil.",
  ],
  idle: [
    "Nice out here.",
    "Walter's out there somewhere.",
    "Take your time.",
  ],

  // ---- Walter, verbatim from 13_VOICE_v2.md §2 ------------------------
  // Short. She isn't making a speech, she's talking to a fish.

  // When he takes it — rod loads heavy, water goes still.
  walterTake: [
    "...well now.",
    "That's him.",
    "Oh, you're kidding me.",
  ],

  // Mid-fight, once she's fairly sure which form.
  walterFight: [
    "You're the big one.",
    "Don't you dare.",
    "Not this time, buddy.",
  ],

  walterLanded: [
    "Walter. You old devil.",
    "Hello, handsome.",
    "I knew you were down there.",
  ],

  // At the release — ONE line, then nothing.
  //
  // 13_VOICE_v2.md §4 flags this as the one slot still worth replacing: it is
  // the emotional end of the entire game, three words and then nothing but a
  // splash. If she has something she actually says to a fish she's putting
  // back, it goes here.
  walterRelease: [
    "Go on. Get.",
    "See you next time.",
    "Stay out of trouble.",
  ],

  // Almost Walter, as the line goes slack. Never `YOU LOST HIM`, never a
  // failure sound. A rueful note and the cicadas come back.
  walterAlmost: [
    "He was right there.",
    "...Every time.",
    "Well. That's Walter.",
  ],

  // The Walter beer. A ritual rather than a mechanic. Last line of a good
  // trip, and the only one with music under it.
  walterToast: "To Walter.",
};

/** Cycle a list without immediate repeats. */
export function makeCycler(list) {
  let last = -1;
  return () => {
    if (list.length === 1) return list[0];
    let i = last;
    while (i === last) i = Math.floor(Math.random() * list.length);
    last = i;
    return list[i];
  };
}
