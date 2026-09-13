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
  // Cicadas: band-passed noise amplitude-modulated at ~11 Hz. Crude, and from
  // twelve feet away in August it is close enough to sit under everything.
  const cic = noiseSource(true);
  const cf = ctx.createBiquadFilter();
  cf.type = 'bandpass'; cf.frequency.value = 4200; cf.Q.value = 2.2;
  cicadaGain = ctx.createGain();
  cicadaGain.gain.value = 0.030;
  const lfo = ctx.createOscillator();
  const lfoGain = ctx.createGain();
  lfo.frequency.value = 11;
  lfoGain.gain.value = 0.016;
  lfo.connect(lfoGain).connect(cicadaGain.gain);
  cic.connect(cf).connect(cicadaGain).connect(ambienceGain);
  cic.start(); lfo.start();

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

/** Cicadas creep louder as the heat builds, and stop dead when Walter is on. */
export function setAmbience({ heat = 0, hushed = false } = {}) {
  if (!ctx || !cicadaGain) return;
  const t = ctx.currentTime;
  const target = hushed ? 0.0 : 0.030 + heat * 0.030;
  cicadaGain.gain.cancelScheduledValues(t);
  cicadaGain.gain.linearRampToValueAtTime(target, t + (hushed ? 0.9 : 2.0));
  if (lapGain) {
    lapGain.gain.cancelScheduledValues(t);
    lapGain.gain.linearRampToValueAtTime(hushed ? 0.020 : 0.055, t + 1.2);
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
export function sfxCoolerOpen() {
  if (playSample('coolerlid')) return;
  burst({ dur: 0.12, peak: 0.16, freq: 520, q: 1.2 });
}
