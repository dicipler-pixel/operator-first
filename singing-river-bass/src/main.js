// src/main.js — SINGING RIVER BASS
//
// Krebs Lake, Pascagoula, Mississippi. Nana sits in a folding chair on the
// bank, the LaPointe-Krebs House across the water behind her, and fishes.
//
// Stage 2 + Stage 3 of 14_HANDOFF.md. Walter is Stage 4 and is deliberately
// not here yet.
//
// The Stage 1 water test still exists, at /watertest.html.

import * as THREE from 'three';
import { RetroPipeline, RENDER_WIDTH, RENDER_HEIGHT } from './render/pipeline.js';
import { syncRetroLighting, createRetroMaterial, paint } from './render/retro.js';
import { updateWater } from './water/06_water_lowfi_threejs.js';
import {
  createKrebsLake, createChair, createCooler, createRodHolder, createCan,
  KREBS_LIGHT, setHeat, SHELF_Y,
} from './maps/krebs.js';
import { createNana, animateNana } from './game/nana.js';
import { createFish, animateFish, lengthForWeight } from './game/fish.js';
import { Trip, STATE } from './game/trip.js';
import { createWalter, createWalterShadow, WALTER_FORMS } from './game/walter.js';
import { Hud } from './ui/hud.js';
import { CatchScreen } from './ui/catchscreen.js';
import { RecordBoard } from './ui/board.js';
import * as sfx from './audio/sfx.js';
import mapData from './data/04_species_and_maps.json';

const canvas = document.getElementById('game');
const ui = document.getElementById('ui');
const startScreen = document.getElementById('start');

const pipeline = new RetroPipeline(canvas);
const hud = new Hud(ui);
const catchScreen = new CatchScreen(ui);
const board = new RecordBoard(ui);

// ---------------------------------------------------------------------------
// Scene

const scene = new THREE.Scene();
const lake = createKrebsLake();
scene.add(lake);
const water = lake.userData.water;

scene.background = KREBS_LIGHT.sky.clone();
scene.fog = new THREE.Fog(KREBS_LIGHT.sky.clone(), KREBS_LIGHT.fogNear, KREBS_LIGHT.fogFar);

// Where she sits: right at the water's edge, angled a few degrees so the
// composition is not dead-on.
// On the bank, not in it: everything sits on the shelf.
const SEAT = new THREE.Vector3(0, SHELF_Y, 2.05);

const chair = createChair();
chair.position.copy(SEAT);
chair.rotation.y = Math.PI + 0.10;
scene.add(chair);

const nana = createNana();
nana.position.copy(SEAT);
nana.rotation.y = Math.PI + 0.10;
scene.add(nana);

// Cooler on her off-hand side. A tappable object in the world.
//
// Pulled forward of the chair rather than level with it. Level with the chair
// it sat exactly on the BOTTOM EDGE of the 4:3 picture, so half of its touch
// target fell into the letterbox bar — where taps are not picked at all,
// because clientToRenderPixel correctly rejects anything outside the rendered
// image. Measured: only two taps in seven landed. Forward of the chair it sits
// clear of the edge and is still, plainly, beside her.
const cooler = createCooler();
cooler.position.set(SEAT.x - 0.74, SHELF_Y + 0.03, SEAT.z - 0.46);
cooler.rotation.y = -0.30;
scene.add(cooler);

const rodHolder = createRodHolder();
rodHolder.position.set(SEAT.x + 0.62, SHELF_Y + 0.02, SEAT.z - 0.45);
scene.add(rodHolder);

// ---- the rod, held in her right hand --------------------------------------
const rodMat = createRetroMaterial({ affine: false, ambientBoost: 1.45, fillFromCamera: 0.30 });
const rod = new THREE.Object3D();
{
  const shaft = new THREE.Mesh(paint(new THREE.CylinderGeometry(0.010, 0.019, 2.05, 5), 0x2b2f33), rodMat);
  shaft.position.y = 1.02;
  rod.add(shaft);
  const grip = new THREE.Mesh(paint(new THREE.CylinderGeometry(0.028, 0.026, 0.26, 6), 0x4a3a2c), rodMat);
  grip.position.y = 0.12;
  rod.add(grip);
  const reel = new THREE.Mesh(paint(new THREE.CylinderGeometry(0.052, 0.052, 0.055, 6), 0x8d9298), rodMat);
  reel.position.set(0, 0.30, -0.055);
  reel.rotation.x = Math.PI / 2;
  rod.add(reel);
}
nana.userData.joints.rHand.add(rod);
rod.position.set(0, -0.07, 0.02);
// Tip up and OUT over the water, not across her body. A seated angler rests
// the butt on her thigh and the rod runs out past her casting shoulder.
rod.rotation.set(0.34, 0, 0.42);

// The rod tip, tracked in world space so the line can be drawn from it.
const rodTip = new THREE.Object3D();
rodTip.position.y = 2.05;
rod.add(rodTip);

// ---- line and lure ---------------------------------------------------------
const lineMat = new THREE.LineBasicMaterial({ color: 0xd8dde2, transparent: true, opacity: 0.55 });
const lineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
const fishingLine = new THREE.Line(lineGeo, lineMat);
fishingLine.frustumCulled = false;
scene.add(fishingLine);

const bobber = new THREE.Object3D();
{
  const m = createRetroMaterial({ affine: false });
  const top = new THREE.Mesh(paint(new THREE.SphereGeometry(0.055, 5, 4), 0xcf3b32), m);
  const bot = new THREE.Mesh(paint(new THREE.SphereGeometry(0.055, 5, 4), 0xe8e8e8), m);
  top.scale.y = 0.7; top.position.y = 0.03;
  bot.scale.y = 0.7; bot.position.y = -0.03;
  bobber.add(top); bobber.add(bot);
}
bobber.visible = false;
scene.add(bobber);

// The hooked fish, swimming out there during the fight.
let hookedFish = null;

// Walter. For most of the fight she sees the shadow, not the fish: a heavy
// shape, a boil, a swirl, no colour. The coloured fish only exists from the
// reveal onward.
const walterShadow = createWalterShadow();
walterShadow.visible = false;
scene.add(walterShadow);
let walterFish = null;
let walterHush = 0;          // 0..1, how far into the hush we are
let releaseFish = null;

// ---- camera: just behind and above her shoulder ---------------------------
const camera = new THREE.PerspectiveCamera(52, RENDER_WIDTH / RENDER_HEIGHT, 0.1, 200);
// Just behind and above her shoulder. She sits low-left of centre with the
// rod running up and out to the right, the water filling the middle, and the
// LaPointe-Krebs House on the horizon the whole time.
const CAM_HOME = new THREE.Vector3(SEAT.x - 0.44, SHELF_Y + 1.62, SEAT.z + 3.05);
const CAM_LOOK = new THREE.Vector3(SEAT.x + 0.16, SHELF_Y + 0.18, SEAT.z - 16.0);
camera.position.copy(CAM_HOME);
camera.lookAt(CAM_LOOK);

// The camera only ever moves for Walter. Everything else in the game is played
// from the one seated over-the-shoulder shot, so when it does move it means
// something. The reveal and the release both push in close — at the home
// framing a 34.80 lb bull red is a small orange shape beside her, which is not
// what that moment is for.
const camPos = CAM_HOME.clone();
const camLook = CAM_LOOK.clone();
const _wantPos = new THREE.Vector3();
const _wantLook = new THREE.Vector3();

function updateCamera(dt) {
  _wantPos.copy(CAM_HOME);
  _wantLook.copy(CAM_LOOK);
  let ease = 1.4;

  const subject = walterFish ?? releaseFish;
  if (subject) {
    // Frame him from slightly off his shoulder, close enough that the flank
    // fills the shot and the markings read.
    //
    // Pull the distance in for the smaller form. At a fixed distance the
    // 8.40 lb trout reads as a minnow next to the 34.80 lb red, which loses
    // the reveal for one of the two forms. Scaling by sqrt keeps the trout
    // visibly the smaller fish while still filling the frame.
    const len = WALTER_FORMS[subject.userData.walterForm]?.length ?? 1.2;
    const k = Math.sqrt(len / 1.35);
    _wantPos.set(
      subject.position.x + 1.45 * k,
      subject.position.y + 0.76 * k,
      subject.position.z + 2.35 * k,
    );
    _wantLook.copy(subject.position);
    ease = 1.1;
  }

  camPos.lerp(_wantPos, Math.min(1, dt * ease));
  camLook.lerp(_wantLook, Math.min(1, dt * ease));
  camera.position.copy(camPos);
  camera.lookAt(camLook);
}

syncRetroLighting(scene, {
  sun: KREBS_LIGHT.sun,
  sunColor: KREBS_LIGHT.sunColor,
  ambient: KREBS_LIGHT.ambient,
  fogColor: KREBS_LIGHT.sky,
  fogNear: KREBS_LIGHT.fogNear,
  fogFar: KREBS_LIGHT.fogFar,
});

// ---------------------------------------------------------------------------
// Game

const trip = new Trip(mapData, {
  onCatch: (fish) => {
    if (hookedFish) { scene.remove(hookedFish); hookedFish = null; }
    bobber.visible = false;
    hud.showTension(false);
    hud.flash('catch');
    catchScreen.show(fish, () => trip.celebrationDone());
    refreshBest();
  },
  onLost: () => {
    if (hookedFish) { scene.remove(hookedFish); hookedFish = null; }
    bobber.visible = false;
    hud.showTension(false);
    hud.setPrompt('HE GOT OFF!');
    setTimeout(() => { if (trip.state === STATE.IDLE) hud.setPrompt('TAP THE WATER TO CAST'); }, 2200);
  },
  onSay: (line) => hud.say(line),
  onState: (s) => onStateChange(s),

  // The water goes still. The cicadas stop. The light shifts a little.
  onWalterStart: () => {
    walterShadow.visible = true;
    bobber.visible = true;
  },

  // He turns near the top and the flank catches the light. Copper with a black
  // dot, or silver with speckles. This is the beat the two forms exist for,
  // and at 128px and 15-bit colour the two are still instantly different.
  onWalterReveal: (form) => {
    walterShadow.visible = false;
    hud.setReelEnabled(false);
    walterFish = createWalter(form);
    scene.add(walterFish);
    hud.setPrompt(form === 'red' ? 'COPPER. THAT BLACK SPOT.' : 'SILVER. THOSE SPECKLES.');
    hud.showTension(false);
    hud.flash('catch');
  },

  // She saw him long enough to know which form it was. Never `YOU LOST HIM`.
  onAlmostWalter: (form) => {
    if (walterFish) { scene.remove(walterFish); walterFish = null; }
    walterShadow.visible = false;
    bobber.visible = false;
    hud.showTension(false);
    hud.setPrompt('HE WAS RIGHT THERE.');
    showBoard('He was right there.');
  },

  onRelease: () => {
    if (walterFish) { scene.remove(walterFish); walterFish = null; }
    releaseFish = createWalter(trip.walterForm);
    scene.add(releaseFish);
    hud.setPrompt('');
  },

  onWalterEnd: () => {
    walterShadow.visible = false;
    if (walterFish) { scene.remove(walterFish); walterFish = null; }
    if (releaseFish) { scene.remove(releaseFish); releaseFish = null; }
  },
});

hud.setName('NANA');
hud.setCooler(trip.coolerLeft);
refreshBest();
hud.setPrompt('TAP THE WATER TO CAST');

// Packing up and sitting back down re-rolls the trip. Without it, a trip that
// rolled NO BIG ONE could never produce Walter for as long as the page stayed
// open — which is exactly what it felt like in play.
function startNewTrip() {
  if (walterFish) { scene.remove(walterFish); walterFish = null; }
  if (releaseFish) { scene.remove(releaseFish); releaseFish = null; }
  if (hookedFish) { scene.remove(hookedFish); hookedFish = null; }
  if (canPlaced) { scene.remove(can); canPlaced = false; }
  walterShadow.visible = false;
  bobber.visible = false;
  trip.newTrip();
  hud.setCooler(trip.coolerLeft);
  hud.setPrompt('TAP THE WATER TO CAST');
  hud.say('Right. Again.');
  refreshBest();
}

function showBoard(headline) {
  board.show(trip.records, headline ?? null, () => trip.boardDone(), startNewTrip);
}

function refreshBest() {
  const best = trip.records.best;
  let name = null, lb = 0;
  for (const [k, v] of Object.entries(best)) if (v > lb) { lb = v; name = k; }
  hud.setBest(lb || null);
}

function onStateChange(s) {
  // A fish is on: hide anything that is not part of landing it.
  const busy = s === STATE.FIGHT || s === STATE.BITE ||
               s === STATE.WALTER_REVEAL || s === STATE.RELEASE;
  ui.classList.toggle('busy', busy);

  switch (s) {
    case STATE.CASTING:
      hud.setPrompt('');
      bobber.visible = false;
      break;
    case STATE.WAITING:
      hud.setPrompt('WAITING ON A BITE');
      bobber.visible = true;
      break;
    case STATE.BITE:
      // Mirrored three ways: the rod bends, the screen edge flashes, it beeps.
      // Walter's bite is the same bite — only the wording and the colour of the
      // flash say something heavier is on.
      hud.setPrompt(trip.walterOn ? 'SOMETHING HEAVY. TAP!' : 'TAP! SET THE HOOK!');
      hud.flash(trip.walterOn ? 'walter' : 'strike');
      break;
    case STATE.WALTER_REVEAL:
    case STATE.RELEASE:
      // The ceremony owns the screen. A live reel bar under it says there is
      // still something to do, and there is not.
      hud.showTension(false);
      hud.setReelEnabled(false);
      break;
    case STATE.BOARD:
      hud.setPrompt('');
      if (!board.active) showBoard(null);
      break;
    case STATE.FIGHT:
      hud.setPrompt('HOLD THE BAR. HE COMES IN.');
      hud.showTension(true);
      hud.setReelEnabled(true);
      if (!trip.walterOn) spawnHookedFish();
      break;
    case STATE.IDLE:
      hud.setPrompt('TAP THE WATER TO CAST');
      hud.showTension(false);
      hud.setReelEnabled(false);
      bobber.visible = false;
      break;
  }
}

function spawnHookedFish() {
  const f = trip.pending;
  if (!f) return;
  hookedFish = createFish(f.species, f.length);
  scene.add(hookedFish);
}

// ---------------------------------------------------------------------------
// Three controls, one thumb. No swipes, no pinch, no drag, no tilt.

const can = createCan();
let canPlaced = false;

const raycaster = new THREE.Raycaster();
const waterPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
const ndc = new THREE.Vector2();
const hitPoint = new THREE.Vector3();

function pickWorld(clientX, clientY) {
  const px = pipeline.clientToRenderPixel(clientX, clientY);
  if (!px) return null;
  ndc.set(px.u * 2 - 1, px.v * 2 - 1);
  raycaster.setFromCamera(ndc, camera);
  return raycaster;
}

/** Did the tap land on the cooler? It is a world object, not a fourth button. */
function tappedCooler(ray) {
  const hits = ray.intersectObject(cooler, true);
  return hits.length > 0;
}

canvas.addEventListener('pointerdown', (e) => {
  if (!sfx.isStarted()) return;
  const ray = pickWorld(e.clientX, e.clientY);
  if (!ray) return;

  // The hook window is forgiving on purpose: a tap anywhere sets it.
  if (trip.state === STATE.BITE) { trip.setHook(); return; }

  if (tappedCooler(ray)) {
    // After the release, the cooler is the Walter beer. A ritual rather than a
    // mechanic, and the only line in the game with music under it.
    if (trip.lastCatch?.walter && !trip.walterToasted) trip.toastWalter();
    else trip.tapCooler();
    hud.setCooler(trip.coolerLeft);
    return;
  }

  if (ray.ray.intersectPlane(waterPlane, hitPoint)) {
    // Only water in front of her counts as a cast target.
    if (hitPoint.z < SEAT.z - 1.2) {
      const r = trip.tapWater(hitPoint.clone());
      if (r === 'cast') {
        const d = hitPoint.clone().sub(SEAT);
        nana.rotation.y = Math.PI + Math.atan2(d.x, -d.z) * 0.35 + 0.10;
        bobber.position.copy(hitPoint);
      }
    }
  }
});

// HOLD to reel. A permanent bar across the bottom third, thumb-reachable
// one-handed on a large phone, 64pt minimum.
const reelBtn = document.getElementById('reel');
const hold = (on) => { trip.setReeling(on); hud.setReelActive(on); };
reelBtn.addEventListener('pointerdown', (e) => { e.preventDefault(); if (trip.state === STATE.BITE) trip.setHook(); else hold(true); });
reelBtn.addEventListener('pointerup', () => hold(false));
reelBtn.addEventListener('pointercancel', () => hold(false));
reelBtn.addEventListener('pointerleave', () => hold(false));
reelBtn.addEventListener('contextmenu', (e) => e.preventDefault());

addEventListener('keydown', (e) => {
  if (e.repeat) return;
  if (e.code === 'Space') { e.preventDefault(); if (trip.state === STATE.BITE) trip.setHook(); else hold(true); }
  if (e.key === 'c' || e.key === 'C') { trip.tapCooler(); hud.setCooler(trip.coolerLeft); }
  // Debug: skip the 30-60s wait. Bites are meant to be slow; this is for testing.
  if (e.key === 'b' || e.key === 'B') trip.forceBite();
  // Debug: force this trip's Walter. T = trout form, R = red form.
  if (e.key === 't' || e.key === 'T') trip.forceWalter('trout');
  if (e.key === 'r' || e.key === 'R') trip.forceWalter('red');
  // Debug: show the record board.
  if (e.key === 'v' || e.key === 'V') showBoard(null);
});
addEventListener('keyup', (e) => { if (e.code === 'Space') hold(false); });
document.getElementById('records-btn').addEventListener('pointerdown', (e) => {
  e.preventDefault(); e.stopPropagation();
  showBoard(null);
});

addEventListener('resize', () => pipeline.resize());

// ---------------------------------------------------------------------------
// TAP TO START. iOS will not play audio until the user taps, and nothing done
// during load works. Period-correct anyway — cabinets sat in attract mode.

let running = false;
startScreen.addEventListener('pointerdown', async () => {
  await sfx.startAudio();
  startScreen.classList.add('gone');
  ui.classList.add('on');
  running = true;
});

// ---------------------------------------------------------------------------
// Loop, locked to 30fps by the pipeline's delta accumulator.

let animState = 'idle';
let animTime = 0;
let nextOutboard = 40 + Math.random() * 60;

const tmpTip = new THREE.Vector3();
const linePositions = fishingLine.geometry.attributes.position;

pipeline.start((dt, elapsed) => {
  updateWater(water, elapsed);

  if (running) {
    trip.update(dt);
    hud.update(dt);
    catchScreen.update(dt, elapsed);

    // ---- heat: atmosphere only, no mechanical effect ------------------
    const { sunColor, sky } = setHeat(lake, trip.heat);
    scene.background = sky;
    scene.fog.color.copy(sky);
    syncRetroLighting(scene, { sunColor, fogColor: sky });
    sfx.setAmbience({ heat: trip.heat });

    const hint = trip.maybeHintCooler();
    if (hint) hud.say(hint);

    nextOutboard -= dt;
    if (nextOutboard <= 0) { sfx.distantOutboard(); nextOutboard = 70 + Math.random() * 90; }

    // ---- pick the animation from the state ----------------------------
    const want =
      trip.state === STATE.CASTING ? 'cast' :
      trip.state === STATE.FIGHT ? 'fight' :
      trip.state === STATE.COOLER ? 'cooler' :
      trip.state === STATE.RELEASE ? 'release' :
      trip.state === STATE.LANDED ? 'lift' : 'idle';
    const resolved = (trip.state === STATE.FIGHT && trip.reeling) ? 'reel' : want;
    if (resolved !== animState) { animState = resolved; animTime = 0; }
    animTime += dt;
    animateNana(nana, animState, animTime, elapsed, trip.strain);

    // Cooler lid opens while she is reaching in.
    const lidOpen = trip.state === STATE.COOLER ? Math.min(1, trip.stateTime / 0.5) : 0;
    cooler.userData.lid.rotation.x = -lidOpen * 1.25;
    if (trip.hasDrink && !canPlaced) {
      canPlaced = true;
      can.position.copy(chair.userData.cupHolder).applyMatrix4(chair.matrixWorld);
      scene.add(can);
    }

    // ---- tension bar --------------------------------------------------
    // Progress, not tension. Nothing here can go wrong, so nothing here flashes.
    if (trip.state === STATE.FIGHT) hud.setProgress(1 - trip.distance);

    // ---- Walter: the hush, the shadow, the reveal ---------------------
    // The water goes still and the light shifts a little. Both are slow enough
    // that you feel them rather than see them happen.
    const wantHush = trip.walterOn || trip.state === STATE.RELEASE;
    walterHush += ((wantHush ? 1 : 0) - walterHush) * dt * 0.9;
    const wu = water.material.uniforms;
    wu.uWaveHeight.value = 0.025 * (1 - walterHush * 0.86);
    wu.uWaveSpeed.value = 0.35 * (1 - walterHush * 0.55);

    if (walterShadow.visible) {
      const prof = trip.walterProfile ?? { depth: 0.7, headshake: 0 };
      const reach = 2.6 + trip.distance * 12.0;
      const drift = Math.sin(elapsed * 0.8 + trip.walterSeed) * (0.5 + trip.distance * 1.4);
      walterShadow.position.set(SEAT.x + drift, -0.32 - prof.depth * 0.55, SEAT.z - reach);
      walterShadow.lookAt(SEAT.x, walterShadow.position.y, SEAT.z);
      walterShadow.rotation.z = Math.sin(elapsed * 6) * prof.headshake * 0.25;
      // The boil sits on the surface above him and grows as he comes up.
      const boil = walterShadow.userData.boil;
      const swirl = walterShadow.userData.swirl;
      const up = -walterShadow.position.y;
      boil.position.y = up; swirl.position.y = up + 0.01;
      const size = 0.55 + (1 - trip.distance) * 0.65;
      boil.scale.setScalar(size); swirl.scale.setScalar(size * (1 + Math.sin(elapsed * 1.4) * 0.12));
      walterShadow.userData.boilMat.uniforms.uAlpha.value = 0.18 + (1 - trip.distance) * 0.34;
      bobber.position.set(walterShadow.position.x, 0.02, walterShadow.position.z + 0.5);
    }

    if (walterFish) {
      // THE REVEAL. He turns near the top and the flank catches the light.
      //
      // He has to actually BREACH the surface, not hover just under it: the
      // water plane writes depth, so anything at or below y=0 is simply hidden
      // and all the player gets is the caption. The first version of this sat
      // him at y=-0.16 and he was invisible for the whole beat — which threw
      // away the one moment the two forms exist for.
      //
      // So: up out of the water, close enough to read, held broadside.
      const p = Math.min(1, trip.stateTime / 2.2);
      const rise = Math.sin(Math.min(1, p * 1.4) * Math.PI * 0.5);   // eases up, holds
      walterFish.position.set(
        SEAT.x + 0.30,
        0.10 + rise * 0.30,
        SEAT.z - 2.55 + p * 0.35,
      );
      // Broadside from the start, rolling slowly so the flank turns into the
      // light rather than spinning.
      walterFish.rotation.set(
        -0.10 - rise * 0.16,
        Math.PI * 0.5 + p * 0.28,
        Math.sin(elapsed * 2.2) * 0.16 - rise * 0.22,
      );
      bobber.position.set(walterFish.position.x, 0.02, walterFish.position.z + 0.45);
    }

    if (releaseFish) {
      // She eases him into the shallows. He sits there a second — they do —
      // then he's gone with one push of the tail.
      const t = trip.stateTime;
      const easeIn = Math.min(1, t / 2.4);
      const gone = t > 4.0 ? Math.min(1, (t - 4.0) / 1.2) : 0;
      // Same trap as the reveal: keep him just proud of the surface while she
      // holds him, so the moment before he goes is actually visible.
      releaseFish.position.set(
        SEAT.x - 0.5 + easeIn * 0.1,
        0.46 - easeIn * 0.36 - gone * 0.22,
        SEAT.z - 1.1 - easeIn * 0.7 - gone * 9.0,
      );
      releaseFish.rotation.set(0.1 - gone * 0.25, Math.PI * 0.5 - gone * 0.35, 0);
      animateFish(releaseFish, elapsed, gone > 0 ? 1.6 : 0.12);
      releaseFish.visible = gone < 0.98;
    }

    // ---- the hooked fish, out in the water ----------------------------
    if (hookedFish && trip.pending) {
      const reach = 3.5 + trip.distance * 13.0;
      const wobble = Math.sin(elapsed * 1.6) * (0.6 + trip.distance);
      hookedFish.position.set(SEAT.x + wobble, -0.10 - trip.distance * 0.25, SEAT.z - reach);
      hookedFish.lookAt(SEAT.x, 0, SEAT.z);
      animateFish(hookedFish, elapsed, 0.5 + trip.strain);
      bobber.position.set(hookedFish.position.x, 0.02, hookedFish.position.z + 0.3);
      bobber.visible = true;
    } else if (bobber.visible) {
      bobber.position.y = 0.02 + Math.sin(elapsed * 1.7) * 0.02;
    }
  }

  if (running) updateCamera(dt);

  // ---- line from rod tip to bobber ------------------------------------
  rod.updateWorldMatrix(true, false);
  rodTip.getWorldPosition(tmpTip);
  linePositions.setXYZ(0, tmpTip.x, tmpTip.y, tmpTip.z);
  if (bobber.visible) linePositions.setXYZ(1, bobber.position.x, bobber.position.y, bobber.position.z);
  else linePositions.setXYZ(1, tmpTip.x, tmpTip.y - 0.01, tmpTip.z);
  linePositions.needsUpdate = true;
  fishingLine.geometry.computeBoundingSphere();
  fishingLine.visible = bobber.visible;

  // ---- render: the game, or the turntable if a fish is being celebrated
  if (catchScreen.active) pipeline.render(catchScreen.scene, catchScreen.camera);
  else pipeline.render(scene, camera);
});

// Hooks for tools/bench.mjs.
pipeline.__benchScene = scene;
pipeline.__benchCamera = camera;
window.__srb = {
  PlaneGeometry: THREE.PlaneGeometry,
  pipeline, water, trip, hud, catchScreen, board, nana, scene, camera,
  stats: pipeline.stats,
  presets: ['krebs'],
  setPreset: () => {},
  setAutoCycle: () => {},
};
