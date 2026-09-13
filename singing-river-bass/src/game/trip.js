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
// WALTER IS NOT HERE YET. He is Stage 4, and 11_BANK_WALTER_v2.md §7 puts him
// last on purpose: everything before him has to feel good enough that a trip
// with no big one is still worth taking, because that is a quarter of them.
// The trip roll is stubbed below so that when he lands, the roll happens once
// at sit-down and not once per cast.

import * as THREE from 'three';
import { rollWeight, lengthForWeight } from './fish.js';
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
    };

    // ---- the trip roll, rolled ONCE, right now, at sit-down -----------
    // Held secretly until the game decides to spend it. Per-cast rolling
    // destroys the game. Walter does not fire yet (Stage 4) but the roll is
    // made here so the structure is right when he lands.
    const r = Math.random();
    this.walterRoll = r < 0.50 ? 'walter' : r < 0.75 ? 'almost' : 'none';
    this.walterForm = Math.random() < 0.5 ? 'trout' : 'red';
    this.walterSpent = false;

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
    if (this.state === STATE.BITE) return this.setHook();
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
    if (this.state === STATE.BITE) return this.setHook();
    return null;
  }

  setHook() {
    if (this.state !== STATE.BITE) return null;
    sfx.sfxHookSet();
    sfx.dragStart();
    this.setState(STATE.FIGHT);
    this.tension = 0.25;
    this.distance = 1;
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
    if (this.state === STATE.LANDED) this.setState(STATE.IDLE);
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
