// src/maps/krebs.js
//
// KREBS LAKE, Pascagoula, Mississippi. Home water, and the map the game opens
// on. Built to 11_BANK_WALTER_v2.md §1 and 00_DESIGN_BIBLE.md §2.
//
// Brackish oxbow of the Pascagoula, historically Lake Catahoula. Sea level —
// the USGS quad puts it at three feet. Small, intimate, ringed with houses and
// docks. Late afternoon going to evening, warm light.
//
// THE LANDMARK: the LaPointe-Krebs House on the far shore. Built around 1757,
// the oldest standing building in Mississippi. Low white tabby walls, steep
// roof, oaks. It is in view the entire game, and one building of about 300
// triangles is what stops this being a generic lake.
//
// Everything here is procedural. The Kenney Nature Kit and Watercraft Kit that
// would normally supply the trees and the docks are unreachable from this
// environment, so the scene is generated instead. See the Stage 2 report.

import * as THREE from 'three';
import { createRetroMaterial, paint, paintShaded } from '../render/retro.js';
import { createWater, WATER_PRESETS } from '../water/06_water_lowfi_threejs.js';

// Evening on the Gulf coast in August.
// Late afternoon going to evening, but a NICE one.
//
// The first pass was genuinely dreary: ambient at 0.34, fog closing in at 96
// units, and near-black olive water. Read together that is an overcast
// November afternoon, not August on the Gulf coast. Everything below is lifted
// — more ambient, a warmer and brighter sun, the fog pushed well back so the
// far bank is not swimming in haze, and a higher, warmer sky.
export const KREBS_LIGHT = {
  sun: new THREE.Vector3(-0.30, 0.48, -0.82).normalize(),
  sunColor: new THREE.Color(1.00, 0.84, 0.60),
  ambient: new THREE.Color(0.56, 0.53, 0.52),
  sky: new THREE.Color(0.91, 0.78, 0.58),
  fogNear: 42,
  fogFar: 190,
};

/**
 * Water colour lift, applied to the uniforms AFTER the mesh is built.
 *
 * 06_water_lowfi_threejs.js is a delivered file and constraint 13 says never
 * overwrite one, so its krebs preset is untouched on disk. Its deep colour is
 * [0.06, 0.10, 0.06] — near-black olive — which is accurate for brackish
 * oxbow water and reads as a mud puddle on a phone at dusk. These override the
 * live uniforms only.
 */
const KREBS_WATER_LIFT = {
  deep: [0.14, 0.22, 0.17],
  shallow: [0.42, 0.50, 0.33],
  sky: [0.91, 0.78, 0.58],
  glint: [1.00, 0.96, 0.80],
};

// Hotter palette for when the heat has built and she has not touched the cooler.
const HOT_SUN = new THREE.Color(1.00, 0.62, 0.30);
const HOT_SKY = new THREE.Color(0.82, 0.56, 0.32);

/**
 * How high the bank sits above the water. Everything she sits on — the chair,
 * the cooler, the rod holder, Nana herself — is placed at this height, so it
 * is exported rather than repeated.
 */
export const SHELF_Y = 0.46;

const BANK_SAND  = 0xcdb98c;   // pale Gulf-coast sand, not mud
const BANK_WET   = 0xb9a678;   // damp strip at the waterline, only a shade darker
const BANK_GRASS = 0x7f8a4e;
const OAK_BARK   = 0x6b5c4a;
const OAK_LEAF   = 0x5a7343;
const MOSS       = 0xa7ab86;
const TABBY      = 0xd9d5c6;   // low white tabby walls
const ROOF       = 0x6b5344;

function mesh(geo, mat) { return new THREE.Mesh(geo, mat); }

export function createKrebsLake() {
  const mat = createRetroMaterial({ affine: false });
  const matDouble = createRetroMaterial({ affine: false, doubleSide: true });
  const scene = new THREE.Object3D();
  scene.name = 'krebs_lake';

  // ---- water ----------------------------------------------------------
  // 96 segments, not the file's default 128. Measured: 96 costs the same per
  // frame as 64 (8.4 ms vs 7.8 ms on software rendering) while 128 more than
  // doubles it to 18.7 ms. See the Stage 1 report — the whole-scene triangle
  // budget in 00_DESIGN_BIBLE.md is the open question here, not this number.
  const water = createWater('krebs', 260, 96);
  water.position.y = 0;
  {
    const u = water.material.uniforms;
    u.uDeep.value.setRGB(...KREBS_WATER_LIFT.deep);
    u.uShallow.value.setRGB(...KREBS_WATER_LIFT.shallow);
    u.uSky.value.setRGB(...KREBS_WATER_LIFT.sky);
    u.uGlint.value.setRGB(...KREBS_WATER_LIFT.glint);
  }
  scene.add(water);

  // ---- near bank: the ground she is sitting on ------------------------
  const bank = new THREE.Object3D();
  scene.add(bank);

  // SHE IS ON LAND, AND IT HAS TO LOOK LIKE IT.
  //
  // Two things went wrong before. The bank sat about 0.12 units above a
  // waterline that itself moves, so no ground ever appeared under the chair
  // and she read as sitting in the lake. Then, raising it as a long ramp made
  // it worse: the slope faces the camera, the evening sun comes from behind
  // the far bank, and a camera-facing slope catches almost no light — it
  // rendered as a dark brown wall.
  //
  // So the shelf is FLAT where she sits, with only a short lip down to the
  // water at the very edge. A flat surface has an up-facing normal, which is
  // what actually catches this light, and she is plainly half a metre above
  // the lake.
  const shoreGeo = new THREE.PlaneGeometry(110, 46, 22, 14);
  shoreGeo.rotateX(-Math.PI / 2);
  {
    const pos = shoreGeo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i), z = pos.getZ(i);
      // Local z runs -23 (waterline) to +23 (well behind the camera).
      const t = THREE.MathUtils.clamp((z + 23) / 1.6, 0, 1);   // short lip
      const rise = SHELF_Y * t * t * (3 - 2 * t);
      const lumps = Math.sin(x * 0.42) * 0.06 + Math.cos(x * 0.19 + z * 0.3) * 0.04;
      pos.setY(i, rise + lumps * t + Math.max(0, z) * 0.02);
    }
    pos.needsUpdate = true;
    shoreGeo.computeVertexNormals();
  }
  const shore = mesh(paintShaded(shoreGeo, BANK_SAND, { top: 1.04, bottom: 0.94 }), mat);
  // Waterline just in front of the chair; the shelf runs back past the camera.
  shore.position.set(0, 0.0, 23.4);
  bank.add(shore);

  // The damp strip right at the water's edge, so there is a waterline to read
  // instead of two planes quietly intersecting.
  const wetGeo = new THREE.PlaneGeometry(110, 1.5, 22, 1);
  wetGeo.rotateX(-Math.PI / 2);
  {
    const pos = wetGeo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i), z = pos.getZ(i);
      pos.setY(i, 0.02 + (z + 0.75) / 1.5 * 0.10 + Math.sin(x * 0.55) * 0.02);
    }
    pos.needsUpdate = true;
    wetGeo.computeVertexNormals();
  }
  const wet = mesh(paintShaded(wetGeo, BANK_WET, { top: 1.0, bottom: 0.95 }), mat);
  wet.position.set(0, 0.01, 0.15);
  bank.add(wet);

  // grass further back, so the bank reads water, sand, then grass
  const grassGeo = new THREE.PlaneGeometry(110, 30, 10, 4);
  grassGeo.rotateX(-Math.PI / 2);
  const grass = mesh(paintShaded(grassGeo, BANK_GRASS, { top: 1.05, bottom: 0.85 }), mat);
  grass.position.set(0, SHELF_Y + 0.34, 42.0);
  bank.add(grass);

  // Reed clumps along the water's edge. Cheap, and they sell the waterline.
  for (let i = 0; i < 26; i++) {
    const rx = (i - 13) * 3.1 + Math.sin(i * 2.7) * 1.4;
    if (Math.abs(rx) < 2.6) continue;          // keep her seat and view clear
    const h = 0.55 + (i % 4) * 0.18;
    const reed = mesh(paint(new THREE.PlaneGeometry(0.55, h), 0x93a15c), matDouble);
    reed.position.set(rx, SHELF_Y + h / 2 - 0.06, 0.9 + Math.sin(i * 1.7) * 0.45);
    reed.rotation.y = i * 0.9;
    bank.add(reed);
  }

  // ---- live oaks behind and to the sides, moss hanging ----------------
  function liveOak(x, z, scale, seed) {
    const t = new THREE.Object3D();
    t.position.set(x, 0.2, z);
    t.scale.setScalar(scale);

    const trunk = mesh(paintShaded(new THREE.CylinderGeometry(0.40, 0.62, 3.0, 5), OAK_BARK), mat);
    trunk.position.y = 1.5;
    t.add(trunk);

    // Live oaks sprawl sideways rather than up. Three or four heavy limbs and
    // flattened canopy blobs read as one from twelve feet away.
    for (let i = 0; i < 4; i++) {
      const a = (i / 4) * Math.PI * 2 + seed;
      const limb = mesh(paintShaded(new THREE.CylinderGeometry(0.16, 0.30, 2.6, 4), OAK_BARK), mat);
      limb.position.set(Math.cos(a) * 1.1, 3.0, Math.sin(a) * 1.1);
      limb.rotation.z = Math.cos(a) * 0.9;
      limb.rotation.x = -Math.sin(a) * 0.9;
      t.add(limb);

      const canopy = mesh(paintShaded(new THREE.SphereGeometry(1.9, 5, 4), OAK_LEAF), mat);
      canopy.position.set(Math.cos(a) * 2.4, 4.0 + Math.sin(seed + i) * 0.3, Math.sin(a) * 2.4);
      canopy.scale.set(1.25, 0.62, 1.25);
      t.add(canopy);

      // Spanish moss: thin hanging strips. Double-sided, alpha off, just geometry.
      for (let m = 0; m < 3; m++) {
        const len = 1.1 + ((i + m + seed) % 1.4);
        const strip = mesh(paint(new THREE.PlaneGeometry(0.20, len), MOSS), matDouble);
        strip.position.set(
          Math.cos(a) * (2.0 + m * 0.45),
          3.5 - len / 2,
          Math.sin(a) * (2.0 + m * 0.45) + (m - 1) * 0.3,
        );
        strip.rotation.y = a + m;
        t.add(strip);
      }
    }
    return t;
  }

  bank.add(liveOak(-9.5, 21, 1.25, 0.3));
  bank.add(liveOak(11.0, 24, 1.45, 1.7));
  bank.add(liveOak(-19.0, 30, 1.1, 2.9));
  bank.add(liveOak(21.0, 33, 1.3, 0.9));

  // ---- the far bank and the LaPointe-Krebs House ----------------------
  const far = new THREE.Object3D();
  far.position.z = -62;
  scene.add(far);

  const farShore = new THREE.PlaneGeometry(200, 30, 10, 2);
  farShore.rotateX(-Math.PI / 2);
  far.add(mesh(paintShaded(farShore, 0x6a6b4c, { top: 1.0, bottom: 0.85 }), mat));

  // The house. About 300 triangles, and the map is instantly not a generic lake.
  const house = new THREE.Object3D();
  house.position.set(-4, 0, 2);
  house.scale.setScalar(1.15);
  far.add(house);

  const walls = mesh(paintShaded(new THREE.BoxGeometry(9.0, 2.5, 5.0), TABBY, { top: 1.0, bottom: 0.88 }), mat);
  walls.position.y = 1.25;
  house.add(walls);

  // Steep roof: a four-sided pyramid stretched along the ridge.
  const roofGeo = new THREE.ConeGeometry(6.6, 3.4, 4);
  roofGeo.rotateY(Math.PI / 4);
  roofGeo.scale(1.0, 1.0, 0.62);
  const roof = mesh(paintShaded(roofGeo, ROOF, { top: 1.0, bottom: 0.7 }), mat);
  roof.position.y = 4.1;
  house.add(roof);

  // Porch running the front, which is the thing you actually recognise.
  const porchRoof = mesh(paint(new THREE.BoxGeometry(9.4, 0.2, 2.2), ROOF), mat);
  porchRoof.position.set(0, 2.45, 3.4);
  house.add(porchRoof);
  for (let i = -3; i <= 3; i++) {
    const post = mesh(paint(new THREE.BoxGeometry(0.16, 2.4, 0.16), TABBY), mat);
    post.position.set(i * 1.45, 1.2, 4.3);
    house.add(post);
  }
  for (const dx of [-2.6, 0, 2.6]) {
    const win = mesh(paint(new THREE.BoxGeometry(0.9, 1.1, 0.08), 0x2b3138), mat);
    win.position.set(dx, 1.5, 2.54);
    house.add(win);
  }

  // oaks around the house, smaller with distance
  for (const [ox, oz, os] of [[-11, 4, 1.5], [7, 5, 1.7], [14, 2, 1.3]]) {
    const t = liveOak(ox, oz, os, ox);
    far.add(t);
  }

  // a couple of docks along the far shore — it is ringed with houses and docks
  for (const dx of [-34, 28]) {
    const dock = new THREE.Object3D();
    dock.position.set(dx, 0, -2);
    far.add(dock);
    const deck = mesh(paintShaded(new THREE.BoxGeometry(2.0, 0.16, 11), 0x6d5f4c), mat);
    deck.position.set(0, 0.55, 5.5);
    dock.add(deck);
    for (let i = 0; i < 5; i++) {
      const pile = mesh(paint(new THREE.BoxGeometry(0.2, 1.3, 0.2), 0x4e4436), mat);
      pile.position.set(0.8, 0.0, 1.5 + i * 2.3);
      dock.add(pile);
    }
  }

  scene.userData.water = water;
  scene.userData.materials = [mat, matDouble];
  return scene;
}

// ---------------------------------------------------------------------------
// The furniture she is actually sitting in.
// ---------------------------------------------------------------------------

const CHAIR_FRAME = 0x8d9298;   // aluminium
const CHAIR_NYLON = 0x2f4d64;   // woven nylon
const COOLER_BODY = 0xcfd3d6;
const COOLER_LID  = 0xbb2d2a;

/** Folding camp chair: aluminium frame, woven nylon, cup holder in the arm. */
const NEAR_FILL = { ambientBoost: 1.45, fillFromCamera: 0.30 };

export function createChair() {
  const mat = createRetroMaterial({ affine: false, ...NEAR_FILL });
  const matD = createRetroMaterial({ affine: false, doubleSide: true, ...NEAR_FILL });
  const chair = new THREE.Object3D();
  chair.name = 'chair';

  const tube = (w, h, d, x, y, z, rx = 0, rz = 0) => {
    const m = mesh(paintShaded(new THREE.BoxGeometry(w, h, d), CHAIR_FRAME), mat);
    m.position.set(x, y, z); m.rotation.x = rx; m.rotation.z = rz;
    return m;
  };

  // legs: the classic crossed folding frame
  for (const side of [-1, 1]) {
    chair.add(tube(0.045, 0.62, 0.045, 0.29 * side, 0.30, -0.22, 0.42));
    chair.add(tube(0.045, 0.62, 0.045, 0.29 * side, 0.30, 0.22, -0.42));
    chair.add(tube(0.04, 0.50, 0.04, 0.29 * side, 0.70, -0.16, 0.16));   // back uprights
    chair.add(tube(0.05, 0.05, 0.50, 0.29 * side, 0.47, 0.0));           // arm rail
    chair.add(tube(0.04, 0.20, 0.04, 0.29 * side, 0.37, 0.24));          // arm post
  }
  chair.add(tube(0.62, 0.05, 0.05, 0, 0.47, 0.24));

  // woven nylon seat and back
  const seat = mesh(paint(new THREE.PlaneGeometry(0.58, 0.50), CHAIR_NYLON), matD);
  seat.rotation.x = -Math.PI / 2 + 0.10;
  seat.position.set(0, 0.44, 0.0);
  chair.add(seat);
  const back = mesh(paint(new THREE.PlaneGeometry(0.58, 0.52), CHAIR_NYLON), matD);
  back.position.set(0, 0.70, -0.20);
  back.rotation.x = 0.26;
  chair.add(back);

  // cup holder in the arm — this is where the beer ends up
  const holder = mesh(paint(new THREE.CylinderGeometry(0.055, 0.05, 0.09, 6, 1, true), CHAIR_FRAME), matD);
  holder.position.set(0.29, 0.52, 0.16);
  chair.add(holder);
  chair.userData.cupHolder = new THREE.Vector3(0.29, 0.55, 0.16);

  return chair;
}

/**
 * The cooler. A tappable object in the world, not a HUD button — the game
 * still has three controls. Six in it.
 */
export function createCooler() {
  const mat = createRetroMaterial({ affine: false, ...NEAR_FILL });
  const cooler = new THREE.Object3D();
  cooler.name = 'cooler';

  const body = mesh(paintShaded(new THREE.BoxGeometry(0.60, 0.36, 0.38), COOLER_BODY), mat);
  body.position.y = 0.18;
  cooler.add(body);

  const lid = new THREE.Object3D();
  lid.position.set(0, 0.36, -0.19);
  cooler.add(lid);
  const lidMesh = mesh(paintShaded(new THREE.BoxGeometry(0.62, 0.07, 0.40), COOLER_LID), mat);
  lidMesh.position.z = 0.19;
  lid.add(lidMesh);
  cooler.userData.lid = lid;

  // A GENEROUS INVISIBLE HIT PROXY.
  //
  // The cooler is the only interactive object in the world, and measured on a
  // 390px phone the visible box is 71x64 CSS pixels with no forgiveness at all
  // — a dead-centre tap worked and 22 pixels off missed. That is nominally at
  // the 64pt floor and useless in practice with a thumb, which is why the beer
  // was undiscoverable. 00_DESIGN_BIBLE.md §4 sets 64pt as a MINIMUM, not a
  // target, so this proxy is about two and a half times the visible cooler.
  //
  // It stays a world object rather than becoming a fourth button: the proxy
  // moves with the cooler, is occluded by nothing, and draws nothing.
  const proxy = new THREE.Mesh(
    new THREE.BoxGeometry(1.45, 1.05, 1.15),
    new THREE.MeshBasicMaterial({ visible: false }),
  );
  proxy.position.set(0, 0.34, 0);
  proxy.name = 'cooler_hit';
  cooler.add(proxy);
  cooler.userData.hitProxy = proxy;

  // handle + latch, so it reads as a cooler and not a box
  const handle = mesh(paint(new THREE.BoxGeometry(0.06, 0.10, 0.03), 0x3a3f44), mat);
  handle.position.set(0, 0.30, 0.20);
  cooler.add(handle);
  for (const dx of [-0.26, 0.26]) {
    const grip = mesh(paint(new THREE.BoxGeometry(0.05, 0.12, 0.05), 0x3a3f44), mat);
    grip.position.set(dx, 0.22, 0);
    cooler.add(grip);
  }

  return cooler;
}

/** Rod holder stuck in the bank, so the rod can sit while she isn't working it. */
export function createRodHolder() {
  const mat = createRetroMaterial({ affine: false, ...NEAR_FILL });
  const o = new THREE.Object3D();
  const tubeG = new THREE.CylinderGeometry(0.045, 0.03, 0.70, 6);
  const tube = mesh(paintShaded(tubeG, 0x3c4a3a), mat);
  tube.position.y = 0.24;
  tube.rotation.x = -0.28;
  o.add(tube);
  return o;
}

/** A can of beer, for the cup holder. */
export function createCan() {
  const mat = createRetroMaterial({ affine: false, ...NEAR_FILL });
  const can = mesh(paintShaded(new THREE.CylinderGeometry(0.033, 0.033, 0.12, 6), 0xb8c0c6), mat);
  const band = mesh(paint(new THREE.CylinderGeometry(0.034, 0.034, 0.04, 6), 0x9a2f2c), mat);
  band.position.y = 0.005;
  can.add(band);
  return can;
}

export function setHeat(scene, heat) {
  // Heat pushes the light hotter and the sky with it. Purely atmospheric —
  // 11_BANK_WALTER_v2.md §5 is explicit that the cooler grants no mechanical
  // bonus and that ignoring it must cost nothing.
  const sunColor = KREBS_LIGHT.sunColor.clone().lerp(HOT_SUN, heat);
  const sky = KREBS_LIGHT.sky.clone().lerp(HOT_SKY, heat);
  return { sunColor, sky };
}
