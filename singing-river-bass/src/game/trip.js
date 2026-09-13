// src/game/trip.js
//
// The loop. Stage 3 of 14_HANDOFF.md, and build steps 1-5 of
// 11_BANK_WALTER_v2.md §7.
//
// THREE CONTROLS, ONE THUMB:
//   TAP the water to cast. Direction is where you tapped.
//   TAP to set the hook when the rod bends and the alert sounds.
//   HOLD the reel bar to reel. Let go to give line.
// The cooler is a tappable object in the world, not a fourth button.
//
// NOTHING PUNISHES. No timer, no fail state, no way to lose. A fish that
// throws the hook is `HE GOT OFF!` with a rueful sound, never a failure screen.
//
// WALTER rolls ONCE PER TRIP, at sit-down, and the result is held secretly
// until the game decides to spend it. Per-cast rolling turns him up every
// ninety seconds and he stops being Walter.

import * as THREE from 'three';
import { rollWeight, lengthForWeight } from './fish.js';
import { WALTER_FORMS, walterFightProfile, walterFightSeconds, walterPace } from './walter.js';
import { LINES, makeCycler } from './lines.js';
import * as sfx from '../audio/sfx.js';

export const STATE = {
  IDLE: 'idle',            // rod in the holder, nothing out
  CASTING: 'casting',      // the cast animation is playing
  WAITING: 'waiting',      // lure in the water, bite timer running
  BITE: 'bite',            // rod bent, alert sounding, hook window open
  FIGHT: 'fight',          // hooked, hold to reel
  LANDED: 'landed',        // celebration owns the screen
  COOLER: 'cooler',        // reaching down, two seconds

  // ---- Walter. A ceremony, not a jump scare. ------------------------
  WALTER_TAKE: 'walterTake',     // the rod loads slowly and heavily
  WALTER_REVEAL: 'walterReveal', // he turns near the top and the flank catches
  RELEASE: 'release',            // she eases him back into the shallows
  BOARD: 'board',                // cut to the record board
};

// A forgiving hook window. Sega Bass gives you a fraction of a second; this
// gives a full second and a half. Older reflexes, capacitive touch latency,
// and nobody is trying to eat quarters here.
const HOOK_WINDOW = 1.5;

// A bite roughly every 30 to 60 seconds.
const BITE_MIN = 30;
const BITE_MAX = 60;

const CAST_TIME = 0.85;
const BIG_FISH_LB = 2.0;      // above this, the full turntable celebration

// Walter gets a longer, calmer window. He is a ceremony; rushing her here
// would be the one place in the game that punishes.
const WALTER_HOOK_WINDOW = 2.6;

// He is not available in the first minutes of a trip. Small fish first, so the
// afternoon has a shape before he turns up.
const WALTER_EARLIEST = 100;

const COOLER_CAPACITY = 6;    // six in the cooler

export class Trip {
  /**
   * @param {object} mapData   04_species_and_maps.json
   * @param {object} hooks     { onCatch, onLost, onSay, onState }
   */
  constructor(mapData, hooks = {}) {
    this.map = mapData.maps.krebs_lake;
    this.hooks = hooks;

    this.state = STATE.IDLE;
    this.stateTime = 0;
    this.elapsed = 0;

    this.biteTimer = 0;
    this.hookTimer = 0;
    this.pending = null;      // the fish currently on, or about to be

    // Fight state
    this.tension = 0;         // 0..1 — the bar that fills AND changes width
    this.distance = 1;        // 1 = far out, 0 = landed
    this.reeling = false;

    // Cooler. No mechanical effect whatsoever, per 11 §5.
    this.coolerLeft = COOLER_CAPACITY;
    this.heat = 0;            // 0..1, purely atmospheric
    this.hasDrink = false;

    this.caught = [];
    this.lastCatch = null;

    this.say = {
      crackBeer: makeCycler(LINES.crackBeer),
      hot: makeCycler(LINES.hot),
      water: makeCycler(LINES.water),
      smallCatch: makeCycler(LINES.smallCatch),
      goodCatch: makeCycler(LINES.goodCatch),
      gotOff: makeCycler(LINES.gotOff),
      idle: makeCycler(LINES.idle),
      walterTake: makeCycler(LINES.walterTake),
      walterFight: makeCycler(LINES.walterFight),
      walterLanded: makeCycler(LINES.walterLanded),
      walterRelease: makeCycler(LINES.walterRelease),
      walterAlmost: makeCycler(LINES.walterAlmost),
    };

    // ---- the trip roll, rolled ONCE, right now, at sit-down -----------
    // Held secretly until the game decides to spend it. Per-cast rolling
    // destroys the game. Walter does not fire yet (Stage 4) but the roll is
    // made here so the structure is right when he lands.
    //   0.00 - 0.50  WALTER        he shows, he fights, she lands him   50%
    //   0.50 - 0.75  ALMOST WALTER he shows, he fights, he goes         25%
    //   0.75 - 1.00  NO BIG ONE    a good day of small fish             25%
    //
    // Fifty percent is very high for a legendary fish and that is deliberate.
    // Do not "fix" it. This is not a game about scarcity. He cannot be a
    // surprise at that rate, so the drama lives somewhere else instead.
    const r = Math.random();
    this.walterRoll = r < 0.50 ? 'walter' : r < 0.75 ? 'almost' : 'none';
    this.walterForm = Math.random() < 0.5 ? 'trout' : 'red';
    this.walterSpent = false;
    this.walterOn = false;
    this.walterSeed = Math.random() * 100;
    this.walterToasted = false;

    // Nothing announces a no-big-one trip. There is no "no Walter today"
    // message — that turns a pleasant afternoon into a notification about
    // absence. The trip is just bream and a channel cat and the light going
    // orange, and that is a complete thing on its own.

    this._records = loadRecords();
  }

  get records() { return this._records; }

  setState(s) {
    if (this.state === s) return;
    this.state = s;
    this.stateTime = 0;
    this.hooks.onState?.(s);
  }

  // ---- input ---------------------------------------------------------

  /** TAP on the water. Casts, or sets the hook if a fish is on. */
  tapWater(point) {
    if (this.state === STATE.BITE || this.state === STATE.WALTER_TAKE) return this.setHook();
    if (this.state === STATE.IDLE || this.state === STATE.WAITING) {
      this.castTarget = point;
      this.setState(STATE.CASTING);
      sfx.sfxCast();
      return 'cast';
    }
    return null;
  }

  /** TAP anywhere while the rod is bent also sets the hook — forgiving. */
  tapAnywhere() {
    if (this.state === STATE.BITE || this.state === STATE.WALTER_TAKE) return this.setHook();
    return null;
  }

  setHook() {
    if (this.state !== STATE.BITE && this.state !== STATE.WALTER_TAKE) return null;
    sfx.sfxHookSet();
    sfx.dragStart();
    this.setState(STATE.FIGHT);
    this.tension = this.walterOn ? 0.40 : 0.25;
    this.distance = 1;
    this.fightTime = 0;
    this.revealed = false;
    if (this.walterOn) this.hooks.onSay?.(this.say.walterFight());
    return 'hooked';
  }

  /** HOLD to reel. Let go to give line. */
  setReeling(on) { this.reeling = !!on && this.state === STATE.FIGHT; }

  /**
   * Tap the cooler. An optional world interaction, the way you'd reach down
   * without thinking about it. Allowed mid-fight — she should be able to.
   */
  tapCooler() {
    if (this.state === STATE.LANDED || this.state === STATE.COOLER) return null;
    if (this.state === STATE.FIGHT) {
      this.hooks.onSay?.(Math.random() < 0.5 ? "Not now, Walter." : "Hold on. Hold on.");
      return 'busy';
    }
    if (this.coolerLeft <= 0) {
      // The only empty-cooler line there is. No alternates, no cycling.
      this.hooks.onSay?.(LINES.coolerEmpty);
      sfx.sfxCoolerOpen();
      return 'empty';
    }
    this._resumeState = this.state;
    this.setState(STATE.COOLER);
    this.coolerLeft--;
    sfx.sfxCoolerOpen();
    setTimeout(() => sfx.sfxCrack(), 550);
    setTimeout(() => sfx.sfxHiss(), 620);
    setTimeout(() => sfx.sfxAhh(), 1250);
    // A drink resets the heat. Ignoring the cooler entirely costs nothing at
    // all; the afternoon just looks hotter than it needs to.
    const wasHot = this.heat > 0.55;
    this.heat = 0;
    this.hasDrink = true;
    setTimeout(() => {
      this.hooks.onSay?.(wasHot ? this.say.hot() : this.say.crackBeer());
    }, 1300);
    return 'drink';
  }

  // ---- update --------------------------------------------------------

  update(dt) {
    this.elapsed += dt;
    this.stateTime += dt;

    // Heat builds slowly over a trip. Atmosphere only.
    this.heat = Math.min(1, this.heat + dt / 420);

    switch (this.state) {
      case STATE.CASTING:
        if (this.stateTime >= CAST_TIME) {
          this.setState(STATE.WAITING);
          this.biteTimer = BITE_MIN + Math.random() * (BITE_MAX - BITE_MIN);
        }
        break;

      case STATE.WAITING:
        this.biteTimer -= dt;
        if (this.biteTimer <= 0) this.startBite();
        break;

      case STATE.WALTER_TAKE:
        // The rod loads slowly and heavily rather than snapping. She has a
        // long, calm window; this beat is not a reflex test.
        this.hookTimer -= dt;
        if (this.hookTimer <= 0) {
          // Even Walter slipping the hook before she sets it is not a failure.
          this.walterOn = false;
          this.pending = null;
          this.setState(STATE.WAITING);
          this.biteTimer = BITE_MIN + Math.random() * (BITE_MAX - BITE_MIN);
          this.hooks.onSay?.(this.say.walterAlmost());
          this.hooks.onWalterEnd?.();
          sfx.sfxGotOff();
        }
        break;

      case STATE.WALTER_REVEAL:
        if (this.stateTime >= 2.2) {
          if (this.walterRoll === 'almost') this.almostWalter();
          else this.landFish();
        }
        break;

      case STATE.RELEASE:
        // He sits there a second — they do — then he's gone with one push of
        // the tail. Then the record board.
        if (this.stateTime >= 5.2) {
          this.hooks.onWalterEnd?.();
          this.setState(STATE.BOARD);
        }
        break;

      case STATE.BITE:
        this.hookTimer -= dt;
        if (this.hookTimer <= 0) {
          // A missed bite. Normal, not a punishment.
          this.pending = null;
          this.setState(STATE.WAITING);
          this.biteTimer = BITE_MIN + Math.random() * (BITE_MAX - BITE_MIN);
          this.hooks.onSay?.(this.say.gotOff());
          sfx.sfxGotOff();
        }
        break;

      case STATE.FIGHT:
        this.updateFight(dt);
        break;

      case STATE.COOLER:
        if (this.stateTime >= 2.0) this.setState(this._resumeState ?? STATE.IDLE);
        break;
    }
  }

  startBite() {
    if (this.shouldSpendWalter()) return this.startWalter();

    const species = this.pickSpecies();
    const lb = rollWeight(species);
    this.pending = {
      species: species.name,
      scientific: species.scientific,
      lb,
      length: lengthForWeight(lb),
      // Heavier fish pull harder and take longer.
      strength: THREE.MathUtils.clamp(0.30 + lb / 14, 0.30, 0.95),
    };
    this.hookTimer = HOOK_WINDOW;
    this.setState(STATE.BITE);
    sfx.sfxStrike();
  }

  /**
   * Decide whether THIS bite is the one the trip roll gets spent on. The roll
   * itself was made at sit-down and never changes; this only picks the moment.
   */
  shouldSpendWalter() {
    if (this.walterSpent) return false;
    if (this.walterRoll === 'none') return false;
    if (this.elapsed < WALTER_EARLIEST) return false;
    // Rising chance per bite once he is eligible, so he always turns up
    // eventually but never at a predictable count.
    this.walterChance = (this.walterChance ?? 0.22) + 0.16;
    return Math.random() < this.walterChance;
  }

  /**
   * He is a ceremony, not a jump scare. The water goes still, the cicadas
   * stop, the light shifts a little, and the rod loads slowly.
   */
  startWalter() {
    this.walterSpent = true;
    this.walterOn = true;
    const form = WALTER_FORMS[this.walterForm];
    this.pending = {
      species: form.species,
      scientific: form.scientific,
      label: form.label,
      lb: form.lb,                  // never moves
      length: form.length,
      walter: true,
      form: this.walterForm,
      strength: 1,
    };
    this.fightLength = walterFightSeconds(this.walterForm);
    this.hookTimer = WALTER_HOOK_WINDOW;
    this.setState(STATE.WALTER_TAKE);
    sfx.setAmbience({ hushed: true });
    sfx.sfxWalterTake();
    this.hooks.onWalterStart?.(this.walterForm);
    this.hooks.onSay?.(this.say.walterTake());
  }

  /**
   * Mostly bluegill, with channel cat, ordinary speckled trout, and the
   * occasional drum — per 11_BANK_WALTER_v2.md §6.
   */
  pickSpecies() {
    const weights = {
      'Bluegill': 52,
      'Channel Catfish': 18,
      'Speckled Trout': 16,
      'Red Drum': 8,
      'Black Drum': 6,
    };
    const pool = this.map.species.filter((s) => weights[s.name]);
    let total = 0;
    for (const s of pool) total += weights[s.name];
    let r = Math.random() * total;
    for (const s of pool) {
      r -= weights[s.name];
      if (r <= 0) return s;
    }
    return pool[0];
  }

  updateFight(dt) {
    const f = this.pending;
    if (!f) return this.setState(STATE.IDLE);
    this.fightTime = (this.fightTime ?? 0) + dt;

    if (f.walter) return this.updateWalterFight(dt);

    // The fish surges on its own rhythm. Reeling closes distance but loads the
    // line; giving line bleeds tension off.
    const surge = (Math.sin(this.stateTime * 2.1) * 0.5 + 0.5) * f.strength;

    if (this.reeling) {
      this.distance -= dt * (0.34 - f.strength * 0.16);
      this.tension += dt * (0.34 + surge * 0.72);
    } else {
      this.tension -= dt * 0.62;
      this.distance += dt * surge * 0.045;
    }

    this.tension = THREE.MathUtils.clamp(this.tension, 0, 1.25);
    this.distance = THREE.MathUtils.clamp(this.distance, 0, 1);
    sfx.dragSet(Math.min(1, this.tension));

    if (this.tension >= 1.0) {
      // Over-tension for long enough and he throws the hook. Never a failure.
      this.overTime = (this.overTime ?? 0) + dt;
      if (this.overTime > 1.3) return this.loseFish();
    } else {
      this.overTime = 0;
    }

    if (this.distance <= 0) this.landFish();
  }

  /**
   * The long fight. Thirty to sixty seconds, against five for everything else.
   *
   * A big red fights deep and slow and dogged. A gator trout runs shallow and
   * headshakes and jumps. The two have to FEEL different, so that by about
   * twenty seconds in she starts to suspect which one she's got — and is
   * sometimes wrong.
   *
   * He stays UNDER THE SURFACE for the whole of this. A heavy shape, a boil, a
   * swirl, no colour. The reveal is worth nothing if he can be read early.
   */
  updateWalterFight(dt) {
    this.walterProfile = walterFightProfile(this.pending.form, this.fightTime, this.walterSeed);
    const pull = this.walterProfile.pull;

    // Distance is paced to the form's fight length rather than to raw reeling,
    // so the ceremony runs as long as it should whatever she does with the bar.
    //
    // The 0.55 is the point. Sizing this for CONTINUOUS reeling is wrong: the
    // tension bar means she can only hold the bar down roughly half to two
    // thirds of the time, so a rate tuned to continuous reeling stretches a
    // 52-second fight past two minutes and the ceremony turns into a chore.
    // Tuned instead, per form, so that the share of the fight the bar actually
    // lets her spend reeling lands inside the thirty-to-sixty-second window.
    // See walterPace() — the red needed a different number from the trout.
    const gain = 1 / (this.fightLength * walterPace(this.pending.form));

    if (this.reeling) {
      this.distance -= dt * gain * (1.25 - pull * 0.30);
      this.tension += dt * (0.30 + pull * 0.80);
    } else {
      this.tension -= dt * 0.58;
      // He takes a little back when she gives line, but nowhere near enough to
      // stall her — there is no way to lose Walter to bad play.
      this.distance += dt * gain * pull * 0.20;
    }

    this.tension = THREE.MathUtils.clamp(this.tension, 0, 1.25);
    this.distance = THREE.MathUtils.clamp(this.distance, 0, 1);
    sfx.dragSet(Math.min(1, this.tension));

    if (this.walterProfile.jump) sfx.sfxSplash(0.8);

    // He does not throw the hook on over-tension. There is no way to lose
    // Walter to a mistake — whether he goes was decided at sit-down, and
    // dressing that up as her error would be a lie about the trip table.
    // Over-tension just stalls her.
    if (this.tension >= 1.0) {
      this.distance = Math.min(1, this.distance + dt * 0.05);
    }

    if (this.distance <= 0.02 && !this.revealed) {
      this.revealed = true;
      this.setState(STATE.WALTER_REVEAL);
      sfx.dragStop();
      sfx.sfxWalterReveal();
      this.hooks.onWalterReveal?.(this.pending.form);
    }
  }

  /**
   * ALMOST WALTER — 25%.
   *
   * She hooks him, fights him, gets him to the surface where she SEES him —
   * and then he's gone. Line goes slack.
   *
   * She sees him long enough to know WHICH FORM it was, and that matters,
   * because it feeds the counter. This must never read as failure. The near
   * miss becomes something she collects rather than something she loses.
   * Thirty years of almost is the whole story of a fish like this.
   */
  almostWalter() {
    sfx.dragStop();
    sfx.sfxSplash(1.2);
    sfx.sfxGotOff();

    this._records.sightings[this.walterForm] = (this._records.sightings[this.walterForm] ?? 0) + 1;
    saveRecords(this._records);

    this.walterOn = false;
    this.pending = null;
    this.hooks.onAlmostWalter?.(this.walterForm);
    this.hooks.onSay?.(this.say.walterAlmost());
    sfx.setAmbience({ hushed: false });   // the cicadas come back
    this.setState(STATE.BOARD);
  }

  /**
   * She lets him go. The most important thing in the design.
   *
   * The celebration does not end on the weight. It ends with her putting him
   * back. Without a release he is USED UP — caught, logged, done — and the
   * point of him evaporates by the third session. Releasing him means he is
   * never finished: the record board is a log of encounters, not a kill count.
   *
   * It is also just true. Nobody keeps a thirty-five pound bull red.
   */
  releaseWalter() {
    this.setState(STATE.RELEASE);
    this.hooks.onSay?.(this.say.walterRelease());
    this.hooks.onRelease?.(this.walterForm);
    setTimeout(() => sfx.sfxSplash(1.0), 2600);
    // Cicadas come back up as he goes.
    setTimeout(() => sfx.setAmbience({ hushed: false }), 3000);
  }

  loseFish() {
    sfx.dragStop();
    sfx.sfxGotOff();
    sfx.sfxSplash(0.7);
    this.overTime = 0;
    this.pending = null;
    this.hooks.onLost?.();
    this.hooks.onSay?.(this.say.gotOff());
    this.setState(STATE.IDLE);
  }

  landFish() {
    sfx.dragStop();
    sfx.sfxSplash(Math.min(1.4, 0.6 + this.pending.lb / 8));
    const fish = this.pending;
    this.pending = null;
    this.overTime = 0;

    if (fish.walter) {
      // Two Walter slots, not one. She can have landed one, both, or neither,
      // and the empty slot is a standing reason to go back.
      //
      // WALTER IS ALWAYS RELEASED. Never kept, never logged as a kill — so he
      // does not touch `best` or the caught count, which are about fish she
      // brought home.
      this._records.walter[fish.form] = fish.lb;
      saveRecords(this._records);
      this.caught.push(fish);
      this.lastCatch = fish;
      this.walterOn = false;
      this.setState(STATE.LANDED);
      this.hooks.onCatch?.(fish);
      this.hooks.onSay?.(this.say.walterLanded());
      return;
    }

    const prev = this._records.best[fish.species];
    fish.isPersonalBest = !prev || fish.lb > prev;
    fish.big = fish.lb >= BIG_FISH_LB;

    if (fish.isPersonalBest) this._records.best[fish.species] = fish.lb;
    this._records.caught = (this._records.caught ?? 0) + 1;
    // Save on every catch, not on quit. Phones kill backgrounded tabs without
    // warning and there is no save button to forget to press.
    saveRecords(this._records);

    this.caught.push(fish);
    this.lastCatch = fish;
    this.setState(STATE.LANDED);
    this.hooks.onCatch?.(fish);
    this.hooks.onSay?.(fish.big ? this.say.goodCatch() : this.say.smallCatch());
  }

  /** Called by the celebration when it is finished with the screen. */
  celebrationDone() {
    if (this.state !== STATE.LANDED) return;
    // Walter's ceremony does not end on the weight. It ends with the release.
    if (this.lastCatch?.walter) return this.releaseWalter();
    this.setState(STATE.IDLE);
  }

  /** Called by the record board when she dismisses it. */
  boardDone() {
    if (this.state === STATE.BOARD) this.setState(STATE.IDLE);
  }

  /**
   * The Walter beer. Optional, and a ritual rather than a mechanic. Last line
   * of a good trip, and the only one with music under it.
   */
  toastWalter() {
    if (this.walterToasted || this.coolerLeft <= 0) return false;
    this.walterToasted = true;
    this.coolerLeft--;
    sfx.sfxCoolerOpen();
    setTimeout(() => sfx.sfxCrack(), 420);
    setTimeout(() => sfx.sfxHiss(), 490);
    setTimeout(() => { this.hooks.onSay?.(LINES.walterToast); sfx.sfxToast(); }, 900);
    return true;
  }

  /** Debug only: force the trip's Walter to be available on the next bite. */
  forceWalter(form) {
    if (form) this.walterForm = form;
    if (this.walterRoll === 'none') this.walterRoll = 'walter';
    this.walterSpent = false;
    this.walterChance = 1;
    this.elapsed = Math.max(this.elapsed, WALTER_EARLIEST + 1);
    this.forceBite();
  }

  /** Debug only: skip the 30-60s wait. Bound to B in main.js. */
  forceBite() {
    if (this.state === STATE.WAITING || this.state === STATE.IDLE) {
      if (this.state === STATE.IDLE) this.setState(STATE.WAITING);
      this.biteTimer = 0;
    }
  }
}

// ---------------------------------------------------------------------------
// localStorage. No account, no login, no password, no network.

const KEY = 'singing-river-bass/records/v1';

export function loadRecords() {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const r = JSON.parse(raw);
      return { best: r.best ?? {}, caught: r.caught ?? 0, walter: r.walter ?? {}, sightings: r.sightings ?? { trout: 0, red: 0 } };
    }
  } catch { /* private mode, cleared storage — carry on with a blank board */ }
  return { best: {}, caught: 0, walter: {}, sightings: { trout: 0, red: 0 } };
}

export function saveRecords(r) {
  try { localStorage.setItem(KEY, JSON.stringify(r)); } catch { /* nothing to do */ }
}
