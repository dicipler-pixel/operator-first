// src/watertest.js — STAGE 1 WATER TEST (kept, not deleted)
//
// Served at /watertest.html. The game itself is src/main.js.
//
// Not the game. This stands up the render pipeline and cycles the four water
// presets so the look can be judged before anything else is built.
//
// Stage 2 replaces this with the Krebs Lake bank scene.

import * as THREE from 'three';
import { RetroPipeline, RENDER_WIDTH, RENDER_HEIGHT } from './render/pipeline.js';
import {
  createWater,
  updateWater,
  setWaterPreset,
  WATER_PRESETS,
} from './water/06_water_lowfi_threejs.js';
import mapData from './data/04_species_and_maps.json';

// Preset key -> the map it belongs to in 04_species_and_maps.json.
const PRESETS = [
  { key: 'krebs', map: 'krebs_lake' },
  { key: 'pascagoula', map: 'pascagoula_river' },
  { key: 'escatawpa', map: 'escatawpa_river' },
  { key: 'lanier', map: 'lake_lanier' },
];

const CYCLE_SECONDS = 6;

const canvas = document.getElementById('game');
const label = document.getElementById('label');
const readout = document.getElementById('readout');

const pipeline = new RetroPipeline(canvas);

// --- scene -----------------------------------------------------------------
const scene = new THREE.Scene();

// Camera sits about where a seated angler's eye is: low, looking slightly down
// the water. The glancing angle is what makes the fresnel banding read.
const camera = new THREE.PerspectiveCamera(
  55,
  RENDER_WIDTH / RENDER_HEIGHT,
  0.1,
  260,
);
camera.position.set(0, 1.35, 6);
camera.lookAt(0, 0.2, -26);

const water = createWater('krebs', 300, 128);
scene.add(water);

// Distance fog tinted to the sky colour, per the design bible. Short draw
// distance hidden behind it.
scene.fog = new THREE.Fog(0x000000, 18, 150);

// --- preset cycling --------------------------------------------------------
let index = 0;
let sinceSwitch = 0;
let autoCycle = true;

function applyPreset(i) {
  index = ((i % PRESETS.length) + PRESETS.length) % PRESETS.length;
  const { key, map } = PRESETS[index];
  setWaterPreset(water, key);

  const sky = new THREE.Color(...WATER_PRESETS[key].sky);
  scene.background = sky;
  scene.fog.color.copy(sky);

  const info = mapData.maps[map];
  label.textContent = `${index + 1}/4  ${info.display}`;
  label.title = info.water;
  sinceSwitch = 0;
}

function advance(step = 1) {
  autoCycle = false;   // a deliberate tap takes over from the timer
  applyPreset(index + step);
}

addEventListener('pointerdown', (e) => {
  advance(e.clientX < innerWidth / 2 ? -1 : 1);
});
addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') advance(1);
  else if (e.key === 'ArrowLeft') advance(-1);
  else if (e.key === 'a' || e.key === 'A') autoCycle = !autoCycle;
  else if (e.key === 'd' || e.key === 'D') {
    const u = pipeline.quadMaterial.uniforms.uDither;
    u.value = u.value > 0.5 ? 0 : 1;
  } else if (e.key === 's' || e.key === 'S') {
    const u = water.material.uniforms.uVertexSnap;
    u.value = u.value > 0.5 ? 0 : 1;
  }
});

addEventListener('resize', () => pipeline.resize());

applyPreset(0);

// --- loop ------------------------------------------------------------------
let readoutAccum = 0;

pipeline.start((dt, elapsed) => {
  sinceSwitch += dt;
  if (autoCycle && sinceSwitch >= CYCLE_SECONDS) applyPreset(index + 1);

  updateWater(water, elapsed);
  pipeline.render(scene, camera);

  readoutAccum += dt;
  if (readoutAccum >= 0.5) {
    readoutAccum = 0;
    const info = pipeline.renderer.info;
    readout.textContent =
      `${pipeline.stats.fps.toFixed(1)} FPS  ·  ${RENDER_WIDTH}x${RENDER_HEIGHT}  ·  ` +
      `${info.render.triangles} TRIS  ·  ${info.render.calls} CALLS  ·  ` +
      `DITHER ${pipeline.quadMaterial.uniforms.uDither.value > 0.5 ? 'ON' : 'OFF'}  ·  ` +
      `SNAP ${water.material.uniforms.uVertexSnap.value > 0.5 ? 'ON' : 'OFF'}`;
  }
});

// Hooks for the headless benchmark in tools/bench.mjs.
pipeline.__benchScene = scene;
pipeline.__benchCamera = camera;

window.__srb = {
  // Only the one constructor tools/bench.mjs needs for its subdivision sweep.
  // Assigning the whole THREE namespace to a global defeats tree-shaking and
  // pulls the entire library into the bundle (+215 KB measured).
  PlaneGeometry: THREE.PlaneGeometry,
  pipeline,
  water,
  stats: pipeline.stats,
  presets: PRESETS.map((p) => p.key),
  setPreset: (k) => { autoCycle = false; applyPreset(PRESETS.findIndex((p) => p.key === k)); },
  setAutoCycle: (on) => { autoCycle = !!on; },
  get current() { return PRESETS[index].key; },
};
