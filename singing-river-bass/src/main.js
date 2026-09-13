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
  KREBS_LIGHT, setHeat,
} from './maps/krebs.js';
import { createNana, animateNana } from './game/nana.js';
import { createFish, animateFish, lengthForWeight } from './game/fish.js';
import { Trip, STATE } from './game/trip.js';
import { Hud } from './ui/hud.js';
import { CatchScreen } from './ui/catchscreen.js';
import * as sfx from './audio/sfx.js';
import mapData from './data/04_species_and_maps.json';

const canvas = document.getElementById('game');
const ui = document.getElementById('ui');
const startScreen = document.getElementById('start');

const pipeline = new RetroPipeline(canvas);
const hud = new Hud(ui);
const catchScreen = new CatchScreen(ui);

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
const SEAT = new THREE.Vector3(0, 0, 2.05);

const chair = createChair();
chair.position.copy(SEAT);
chair.rotation.y = Math.PI + 0.10;
scene.add(chair);

const nana = createNana();
nana.position.copy(SEAT);
nana.position.y = 0.02;
nana.rotation.y = Math.PI + 0.10;
scene.add(nana);

// Cooler on her off-hand side. A tappable object in the world.
const cooler = createCooler();
cooler.position.set(SEAT.x - 0.66, 0.06, SEAT.z + 0.10);
cooler.rotation.y = -0.22;
scene.add(cooler);

const rodHolder = createRodHolder();
rodHolder.position.set(SEAT.x + 0.62, 0.04, SEAT.z - 0.45);
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

// ---- camera: just behind and above her shoulder ---------------------------
const camera = new THREE.PerspectiveCamera(52, RENDER_WIDTH / RENDER_HEIGHT, 0.1, 200);
// Just behind and above her shoulder. She sits low-left of centre with the
// rod running up and out to the right, the water filling the middle, and the
// LaPointe-Krebs House on the horizon the whole time.
const CAM_HOME = new THREE.Vector3(SEAT.x - 0.44, 1.92, SEAT.z + 3.05);
const CAM_LOOK = new THREE.Vector3(SEAT.x + 0.16, 0.62, SEAT.z - 16.0);
camera.position.copy(CAM_HOME);
camera.lookAt(CAM_LOOK);

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
});

hud.setName('NANA');
hud.setCooler(trip.coolerLeft);
refreshBest();
hud.setPrompt('TAP THE WATER TO CAST');

function refreshBest() {
  const best = trip.records.best;
  let name = null, lb = 0;
  for (const [k, v] of Object.entries(best)) if (v > lb) { lb = v; name = k; }
  hud.setBest(lb || null);
}

function onStateChange(s) {
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
      hud.setPrompt('TAP! SET THE HOOK!');
      hud.flash('strike');
      break;
    case STATE.FIGHT:
      hud.setPrompt('HOLD TO REEL — LET GO TO GIVE LINE');
      hud.showTension(true);
      hud.setReelEnabled(true);
      spawnHookedFish();
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

  if (tappedCooler(ray)) { trip.tapCooler(); hud.setCooler(trip.coolerLeft); return; }

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
});
addEventListener('keyup', (e) => { if (e.code === 'Space') hold(false); });
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
const can = createCan();
let canPlaced = false;

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

    nextOutboard -= dt;
    if (nextOutboard <= 0) { sfx.distantOutboard(); nextOutboard = 70 + Math.random() * 90; }

    // ---- pick the animation from the state ----------------------------
    const want =
      trip.state === STATE.CASTING ? 'cast' :
      trip.state === STATE.FIGHT ? 'fight' :
      trip.state === STATE.COOLER ? 'cooler' :
      trip.state === STATE.LANDED ? 'lift' :
      (trip.state === STATE.FIGHT && trip.reeling) ? 'reel' : 'idle';
    const resolved = (trip.state === STATE.FIGHT && trip.reeling) ? 'reel' : want;
    if (resolved !== animState) { animState = resolved; animTime = 0; }
    animTime += dt;
    animateNana(nana, animState, animTime, elapsed, Math.min(1, trip.tension));

    // Cooler lid opens while she is reaching in.
    const lidOpen = trip.state === STATE.COOLER ? Math.min(1, trip.stateTime / 0.5) : 0;
    cooler.userData.lid.rotation.x = -lidOpen * 1.25;
    if (trip.hasDrink && !canPlaced) {
      canPlaced = true;
      can.position.copy(chair.userData.cupHolder).applyMatrix4(chair.matrixWorld);
      scene.add(can);
    }

    // ---- tension bar --------------------------------------------------
    if (trip.state === STATE.FIGHT) {
      hud.setTension(trip.tension);
      if (trip.tension >= 1.0) hud.flash('over');
    }

    // ---- the hooked fish, out in the water ----------------------------
    if (hookedFish && trip.pending) {
      const reach = 3.5 + trip.distance * 13.0;
      const wobble = Math.sin(elapsed * 1.6) * (0.6 + trip.distance);
      hookedFish.position.set(SEAT.x + wobble, -0.10 - trip.distance * 0.25, SEAT.z - reach);
      hookedFish.lookAt(SEAT.x, 0, SEAT.z);
      animateFish(hookedFish, elapsed, 0.5 + trip.tension);
      bobber.position.set(hookedFish.position.x, 0.02, hookedFish.position.z + 0.3);
      bobber.visible = true;
    } else if (bobber.visible) {
      bobber.position.y = 0.02 + Math.sin(elapsed * 1.7) * 0.02;
    }
  }

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
  pipeline, water, trip, hud, catchScreen, nana, scene, camera,
  stats: pipeline.stats,
  presets: ['krebs'],
  setPreset: () => {},
  setAutoCycle: () => {},
};
