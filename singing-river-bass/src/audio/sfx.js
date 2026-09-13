// src/audio/sfx.js
//
// Every sound in the game, synthesised in WebAudio.
//
// THIS IS A SUBSTITUTION AND IT IS FLAGGED, NOT SILENT. 01_ASSET_MANIFEST.md
// specifies CC0 clips from Freesound (water lapping, cicadas, outboard motor,
// reel drag whine, rod-tip splash) and Kenney's Interface Sounds for UI.
// freesound.org and kenney.nl are both blocked by this environment's egress
// policy, so nothing could be downloaded. Rather than ship silence, these are
// oscillator-and-noise stand-ins with the same shape and timing, so the loop
// can be judged now. Replace them with the real clips when the packs land —
// `registerSample()` exists for exactly that.
//
// The cooler's three sounds in particular are placeholders that do not yet earn
// their keep. 11_BANK_WALTER_v2.md §5 says the crack, the hiss and the small
// "ahh" should be the best-recorded three in the game, and a synthesised "ahh"
// is not a human voice. That one needs a real recording.
//
// ACCESSIBILITY, from 00_DESIGN_BIBLE.md §4: the important cues — the strike
// alert, the drag whine — sit in the 500 Hz to 2 kHz band, where age-related
// hearing loss is least severe. Nothing relies on a high-frequency ping, and
// every audio cue is mirrored by a visual one in the HUD.

let ctx = null;
let master = null;
let ambienceGain = null;
let started = false;

const samples = new Map();   // name -> AudioBuffer, for real clips later

export function isStarted() { return started; }

/**
 * iOS will not play audio until the user taps. Nothing done during load works.
 * Call this from the TAP TO START handler — which is period-correct anyway,
 * since arcade cabinets sat in attract mode until you pressed start.
 */
export async function startAudio() {
  if (started) return;
  const AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;
  ctx = new AC();
  master = ctx.createGain();
  master.gain.value = 0.8;
  master.connect(ctx.destination);
  ambienceGain = ctx.createGain();
  ambienceGain.gain.value = 0.0;
  ambienceGain.connect(master);
  await ctx.resume();
  started = true;
  buildAmbience();
}

/** Drop a decoded real clip in over a synthesised one, by name. */
export function registerSample(name, audioBuffer) { samples.set(name, audioBuffer); }

function playSample(name, gain = 1) {
  const buf = samples.get(name);
  if (!buf || !ctx) return false;
  const src = ctx.createBufferSource();
  const g = ctx.createGain();
  g.gain.value = gain;
  src.buffer = buf;
  src.connect(g).connect(master);
  src.start();
  return true;
}

// --- primitives ------------------------------------------------------------

function noiseBuffer(seconds = 2) {
  const n = Math.floor(ctx.sampleRate * seconds);
  const buf = ctx.createBuffer(1, n, ctx.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
  return buf;
}

function noiseSource(loop = true) {
  const src = ctx.createBufferSource();
  src.buffer = noiseBuffer(loop ? 2 : 0.6);
  src.loop = loop;
  return src;
}

function env(gain, t0, peak, attack, decay) {
  gain.gain.setValueAtTime(0.0001, t0);
  gain.gain.exponentialRampToValueAtTime(Math.max(0.0002, peak), t0 + attack);
  gain.gain.exponentialRampToValueAtTime(0.0001, t0 + attack + decay);
}

function tone(freq, { t = 0, dur = 0.2, peak = 0.2, type = 'triangle', slideTo = null } = {}) {
  if (!ctx) return;
  const t0 = ctx.currentTime + t;
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, t0);
  if (slideTo) osc.frequency.exponentialRampToValueAtTime(slideTo, t0 + dur);
  env(g, t0, peak, 0.012, dur);
  osc.connect(g).connect(master);
  osc.start(t0);
  osc.stop(t0 + dur + 0.05);
}

function burst({ t = 0, dur = 0.12, peak = 0.3, freq = 1400, q = 1.0, type = 'bandpass' } = {}) {
  if (!ctx) return;
  const t0 = ctx.currentTime + t;
  const src = noiseSource(false);
  const f = ctx.createBiquadFilter();
  const g = ctx.createGain();
  f.type = type; f.frequency.value = freq; f.Q.value = q;
  env(g, t0, peak, 0.004, dur);
  src.connect(f).connect(g).connect(master);
  src.start(t0);
  src.stop(t0 + dur + 0.1);
}

// --- ambience: cicadas, water lapping, a far-off outboard ------------------

let cicadaGain = null;
let lapGain = null;

function buildAmbience() {
  // Cicadas. FAR back in the mix, and deliberately so.
  //
  // The first version of this was band-passed noise amplitude-modulated at
  // 11 Hz around 4.2 kHz. That is close to the real insect and it was
  // genuinely unpleasant to sit under — a hard buzz right in the most
  // fatiguing part of the spectrum, running continuously for a whole session.
  // A real cicada wall works outdoors because it is diffuse and you can look
  // away from it; through phone speakers it is just an irritant.
  //
  // So: down around 2.2 kHz where it reads as distant rather than adjacent,
  // a slow shallow pulse instead of a fast deep one, and a level low enough
  // that you notice it when it stops rather than while it plays. Walter's
  // hush still works — arguably better, because the silence lands against
  // something restful instead of a relief from noise.
  const cic = noiseSource(true);
  const cf = ctx.createBiquadFilter();
  cf.type = 'bandpass'; cf.frequency.value = 2200; cf.Q.value = 0.9;
  const cfHi = ctx.createBiquadFilter();
  cfHi.type = 'lowpass'; cfHi.frequency.value = 3200;   // shave the hard top
  cicadaGain = ctx.createGain();
  cicadaGain.gain.value = 0.0001;   // starts silent; the scheduler brings them in
  cic.connect(cf).connect(cfHi).connect(cicadaGain).connect(ambienceGain);
  cic.start();
  scheduleCicadas();

  // Water lapping: low-passed noise, slowly swelling.
  const lap = noiseSource(true);
  const lf = ctx.createBiquadFilter();
  lf.type = 'lowpass'; lf.frequency.value = 420; lf.Q.value = 0.7;
  lapGain = ctx.createGain();
  lapGain.gain.value = 0.055;
  const swell = ctx.createOscillator();
  const swellGain = ctx.createGain();
  swell.frequency.value = 0.28;
  swellGain.gain.value = 0.028;
  swell.connect(swellGain).connect(lapGain.gain);
  lap.connect(lf).connect(lapGain).connect(ambienceGain);
  lap.start(); swell.start();

  ambienceGain.gain.linearRampToValueAtTime(1.0, ctx.currentTime + 2.5);
}

// Cicadas COME AND GO. They are audible maybe fifteen percent of the time.
//
// A continuous bed is what makes insect noise grating — once it never stops,
// there is nothing to stop noticing, and it just sits on top of everything for
// the whole session. Real cicadas on that bank swell up, run for a while, and
// drop away again for a minute or two, and that intermittency is most of why
// it reads as somewhere pleasant rather than as noise.
//
// It also costs nothing and buys the Walter hush: he cannot silence something
// that is already silent most of the time, so the hush is scheduled to land on
// a live stretch when it can.
let cicadaHeat = 0;
let cicadaHushed = false;
let cicadaTimer = null;

// 15% of the original level. The first pass ran at 0.030 continuously; this
// peaks at 0.0045 and only during a stretch, so it sits under the water rather
// than over it.
const CICADA_FULL = 0.030;        // what the first, unpleasant version ran at
const CICADA_LEVEL = 0.15;        // fifteen percent of it

function cicadaPeak() {
  // Heat nudges it, but never past a fifth of the original.
  return CICADA_FULL * CICADA_LEVEL * (1 + cicadaHeat * 0.35);
}

function scheduleCicadas() {
  if (!ctx || !cicadaGain) return;
  clearTimeout(cicadaTimer);
  if (cicadaHushed) return;

  // Audible roughly fifteen percent of the time: a short stretch, then a long
  // quiet one. Slow ramps at both ends so a stretch arrives and leaves without
  // ever being an event.
  const gap = 52 + Math.random() * 38;      // a minute or so of nothing
  const rise = 3.5;
  const hold = 4 + Math.random() * 4;
  const fall = 4.5;

  cicadaTimer = setTimeout(() => {
    if (!ctx || cicadaHushed) return;
    const t = ctx.currentTime;
    const g = cicadaGain.gain;
    g.cancelScheduledValues(t);
    g.setValueAtTime(Math.max(0.0001, g.value), t);
    g.linearRampToValueAtTime(cicadaPeak(), t + rise);
    g.setValueAtTime(cicadaPeak(), t + rise + hold);
    g.linearRampToValueAtTime(0.0001, t + rise + hold + fall);
    scheduleCicadas();
  }, gap * 1000);
}

/** True while a cicada stretch is actually audible. */
export function cicadasAudible() {
  return !!cicadaGain && cicadaGain.gain.value > 0.0008;
}

/**
 * Heat nudges how loud a cicada stretch gets when one comes. Walter stops them
 * dead — and if they happen to be in a quiet gap when he takes it, the lapping
 * dropping away carries the hush instead.
 */
export function setAmbience({ heat = 0, hushed = false } = {}) {
  if (!ctx || !cicadaGain) return;
  cicadaHeat = heat;

  if (hushed !== cicadaHushed) {
    cicadaHushed = hushed;
    const t = ctx.currentTime;
    if (hushed) {
      clearTimeout(cicadaTimer);
      cicadaGain.gain.cancelScheduledValues(t);
      cicadaGain.gain.setValueAtTime(Math.max(0.0001, cicadaGain.gain.value), t);
      cicadaGain.gain.linearRampToValueAtTime(0.0001, t + 1.1);
    } else {
      scheduleCicadas();
    }
  }

  if (lapGain) {
    const t = ctx.currentTime;
    lapGain.gain.cancelScheduledValues(t);
    lapGain.gain.linearRampToValueAtTime(hushed ? 0.016 : 0.050, t + 1.2);
  }
}

/** A boat motor somewhere far off, occasionally. */
export function distantOutboard() {
  if (!ctx) return;
  if (playSample('outboard', 0.25)) return;
  const t0 = ctx.currentTime;
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(74, t0);
  osc.frequency.linearRampToValueAtTime(88, t0 + 6);
  f.type = 'lowpass'; f.frequency.value = 260;
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.linearRampToValueAtTime(0.022, t0 + 2.5);
  g.gain.linearRampToValueAtTime(0.0001, t0 + 8);
  osc.connect(f).connect(g).connect(master);
  osc.start(t0); osc.stop(t0 + 8.5);
}

// --- game cues -------------------------------------------------------------

export function sfxCast() {
  if (playSample('cast')) return;
  burst({ dur: 0.22, peak: 0.16, freq: 2600, q: 0.6 });        // line hissing out
  burst({ t: 0.34, dur: 0.16, peak: 0.22, freq: 900, q: 1.4 }); // rod-tip splash
}

/**
 * The strike alert. The single most important sound in the game, and it sits
 * at 900 Hz on purpose. Mirrored by the rod bending AND the screen edge
 * flashing — never rely on the sound alone.
 */
export function sfxStrike() {
  if (playSample('strike')) return;
  tone(900, { dur: 0.10, peak: 0.34, type: 'square' });
  tone(1350, { t: 0.11, dur: 0.13, peak: 0.30, type: 'square' });
}

export function sfxHookSet() {
  if (playSample('hookset')) return;
  tone(620, { dur: 0.09, peak: 0.28, type: 'sawtooth', slideTo: 1100 });
  burst({ dur: 0.10, peak: 0.18, freq: 1200, q: 1.0 });
}

/** Reel drag whine. Held while the fish is running, pitch follows the strain. */
let dragOsc = null, dragGain = null;
export function dragStart() {
  if (!ctx || dragOsc) return;
  dragOsc = ctx.createOscillator();
  dragGain = ctx.createGain();
  const f = ctx.createBiquadFilter();
  f.type = 'bandpass'; f.frequency.value = 1400; f.Q.value = 3.5;
  dragOsc.type = 'sawtooth';
  dragOsc.frequency.value = 700;
  dragGain.gain.value = 0.0001;
  dragOsc.connect(f).connect(dragGain).connect(master);
  dragOsc.start();
}
export function dragSet(strain) {
  if (!ctx || !dragOsc) return;
  const t = ctx.currentTime;
  dragOsc.frequency.setTargetAtTime(620 + strain * 900, t, 0.08);
  dragGain.gain.setTargetAtTime(0.0001 + strain * 0.10, t, 0.08);
}
export function dragStop() {
  if (!dragOsc) return;
  const t = ctx.currentTime;
  dragGain.gain.setTargetAtTime(0.0001, t, 0.10);
  dragOsc.stop(t + 0.5);
  dragOsc = null; dragGain = null;
}

/** Small fish: a chime, a second and a half, back to fishing. */
export function sfxChime() {
  if (playSample('chime')) return;
  tone(784, { dur: 0.22, peak: 0.24 });
  tone(1175, { t: 0.10, dur: 0.30, peak: 0.20 });
}

/** Anything over about two pounds gets the fanfare. */
export function sfxFanfare() {
  if (playSample('fanfare')) return;
  const notes = [523, 659, 784, 1047];
  notes.forEach((f, i) => tone(f, { t: i * 0.13, dur: 0.34, peak: 0.26, type: 'square' }));
  tone(1568, { t: 0.56, dur: 0.7, peak: 0.22, type: 'triangle' });
}

/** The tick per tenth as the weight counts up. */
export function sfxTick() {
  if (playSample('tick')) return;
  tone(1500, { dur: 0.03, peak: 0.10, type: 'square' });
}

/**
 * A fish that throws the hook. A rueful note, NOT a failure sound — there is
 * no failure in this game.
 */
export function sfxGotOff() {
  if (playSample('gotoff')) return;
  tone(520, { dur: 0.26, peak: 0.20, type: 'triangle', slideTo: 360 });
  burst({ t: 0.06, dur: 0.20, peak: 0.16, freq: 700, q: 1.0 });
}

export function sfxSplash(size = 1) {
  if (playSample('splash')) return;
  burst({ dur: 0.18 * size, peak: 0.20 * size, freq: 780, q: 0.9 });
  burst({ t: 0.05, dur: 0.26 * size, peak: 0.12 * size, freq: 380, q: 0.7 });
}

// --- the cooler: the three that should be the best in the game ------------

export function sfxCrack() {
  if (playSample('crack')) return;
  burst({ dur: 0.035, peak: 0.40, freq: 2600, q: 0.8, type: 'highpass' });
  tone(1800, { dur: 0.04, peak: 0.16, type: 'square' });
}
export function sfxHiss() {
  if (playSample('hiss')) return;
  if (!ctx) return;
  const t0 = ctx.currentTime + 0.04;
  const src = noiseSource(false);
  const f = ctx.createBiquadFilter();
  const g = ctx.createGain();
  f.type = 'highpass'; f.frequency.value = 3000;
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(0.13, t0 + 0.03);
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.55);
  src.connect(f).connect(g).connect(master);
  src.start(t0); src.stop(t0 + 0.7);
}
export function sfxAhh() {
  // Placeholder, and the weakest sound in the game. This wants a real voice.
  if (playSample('ahh')) return;
  if (!ctx) return;
  const t0 = ctx.currentTime;
  const src = noiseSource(false);
  const f = ctx.createBiquadFilter();
  const g = ctx.createGain();
  f.type = 'bandpass'; f.frequency.setValueAtTime(700, t0);
  f.frequency.linearRampToValueAtTime(480, t0 + 0.5);
  f.Q.value = 4;
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(0.07, t0 + 0.10);
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.6);
  src.connect(f).connect(g).connect(master);
  src.start(t0); src.stop(t0 + 0.7);
}
// --- Walter -------------------------------------------------------------

/**
 * He takes it. The rod loads slowly and heavily rather than snapping, and the
 * sound has to do the same — a low swell, not the sharp two-note strike alert
 * a bream gets. From the way this lands she knows it's a Walter. She does not
 * know which one.
 */
export function sfxWalterTake() {
  if (playSample('waltertake')) return;
  if (!ctx) return;
  const t0 = ctx.currentTime;
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  const f = ctx.createBiquadFilter();
  osc.type = 'triangle';
  osc.frequency.setValueAtTime(150, t0);
  osc.frequency.exponentialRampToValueAtTime(74, t0 + 1.5);
  f.type = 'lowpass'; f.frequency.value = 900;
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(0.30, t0 + 0.55);   // loads slowly
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + 1.9);
  osc.connect(f).connect(g).connect(master);
  osc.start(t0); osc.stop(t0 + 2.0);
  // A single low note under it, in the 500-2k band so it still reads.
  tone(660, { t: 0.12, dur: 0.9, peak: 0.12, type: 'triangle', slideTo: 520 });
}

/** He turns near the top and the flank catches the light. */
export function sfxWalterReveal() {
  if (playSample('walterreveal')) return;
  sfxSplash(1.3);
  tone(392, { dur: 0.5, peak: 0.18, type: 'triangle', slideTo: 587 });
  tone(587, { t: 0.24, dur: 0.7, peak: 0.16 });
}

/**
 * His own music. Longer than the fanfare and warmer — this is the only
 * celebration in the game with a tune rather than a flourish.
 */
export function sfxWalterFanfare() {
  if (playSample('walterfanfare')) return;
  const mel = [[392, 0], [523, 0.26], [659, 0.52], [784, 0.78], [659, 1.10], [784, 1.32], [1047, 1.62]];
  for (const [f, t] of mel) tone(f, { t, dur: 0.46, peak: 0.24, type: 'square' });
  for (const [f, t] of [[196, 0], [262, 0.78], [330, 1.62]]) {
    tone(f, { t, dur: 1.1, peak: 0.13, type: 'triangle' });
  }
}

/** "To Walter." The only line with music under it. */
export function sfxToast() {
  if (playSample('toast')) return;
  for (const [f, t] of [[523, 0], [659, 0.20], [784, 0.40]]) {
    tone(f, { t, dur: 0.9, peak: 0.13, type: 'triangle' });
  }
}

export function sfxCoolerOpen() {
  if (playSample('coolerlid')) return;
  burst({ dur: 0.12, peak: 0.16, freq: 520, q: 1.2 });
}
