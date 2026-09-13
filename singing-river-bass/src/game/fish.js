// src/game/fish.js
//
// Fish, built procedurally. 01_ASSET_MANIFEST.md's "Fish gap" note says there
// is no CC0 pack of Southeast freshwater species and recommends four base
// meshes retextured fourteen ways. With the CC0 hosts unreachable there is no
// Quaternius mesh to retexture, so the same four body plans are generated from
// a profile curve instead. Same conclusion, one less dependency:
//
//   lean   long and lean          speckled trout, striped bass
//   deep   deep and round         bluegill, longear sunfish
//   heavy  deep-bodied and heavy  red drum, black drum
//   cat    flat-headed, barbels   channel catfish, flathead
//
// About 300 triangles each, per the polygon budget. At this size the
// silhouette does nearly all the work and colour does the rest.

import * as THREE from 'three';
import { createRetroMaterial, paint } from '../render/retro.js';

// Body profile: half-height of the fish at 0..1 along its length.
const PLANS = {
  lean:  { rings: [0.02, 0.09, 0.14, 0.165, 0.17, 0.16, 0.14, 0.11, 0.08, 0.05, 0.03], widthK: 0.30, tail: 0.30 },
  deep:  { rings: [0.03, 0.14, 0.23, 0.28, 0.30, 0.29, 0.25, 0.19, 0.12, 0.07, 0.04], widthK: 0.20, tail: 0.26 },
  heavy: { rings: [0.03, 0.13, 0.21, 0.25, 0.27, 0.26, 0.23, 0.18, 0.12, 0.07, 0.04], widthK: 0.32, tail: 0.30 },
  cat:   { rings: [0.05, 0.12, 0.16, 0.175, 0.17, 0.15, 0.12, 0.09, 0.06, 0.04, 0.02], widthK: 0.46, tail: 0.28 },
};

// Eight-sided cross-section. Six read as a hexagonal lump at celebration
// scale; eight is still cheap and still visibly faceted, which is the point.
const SIDES = 8;

function buildBody(plan) {
  const p = PLANS[plan];
  const rings = p.rings;
  const segs = rings.length;
  const positions = [], normals = [], uvs = [], indices = [];

  for (let i = 0; i < segs; i++) {
    const t = i / (segs - 1);
    const z = 0.5 - t;                      // nose at +z, tail at -z
    const h = rings[i];
    for (let s = 0; s < SIDES; s++) {
      const a = (s / SIDES) * Math.PI * 2;
      positions.push(Math.cos(a) * h * p.widthK * 2.0, Math.sin(a) * h, z);
      normals.push(Math.cos(a), Math.sin(a), 0);
      uvs.push(t, s / SIDES);
    }
  }
  for (let i = 0; i < segs - 1; i++) {
    for (let s = 0; s < SIDES; s++) {
      const a = i * SIDES + s;
      const b = i * SIDES + ((s + 1) % SIDES);
      const c = (i + 1) * SIDES + s;
      const d = (i + 1) * SIDES + ((s + 1) % SIDES);
      indices.push(a, c, b, b, c, d);
    }
  }

  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(normals, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  g.setIndex(indices);
  g.computeVertexNormals();
  return g;
}

/**
 * Build a fin from explicit vertices in the plane it actually lives in, rather
 * than a generic triangle that then gets rotated. Rotating a generic triangle
 * is how you end up with a sail where a dorsal ridge should be.
 *
 * @param {number[][]} pts  triangle-fan points, already in fish-local space
 */
function finFromPoints(pts, color) {
  const g = new THREE.BufferGeometry();
  const flat = [];
  for (const p of pts) flat.push(p[0], p[1], p[2]);
  g.setAttribute('position', new THREE.Float32BufferAttribute(flat, 3));
  const idx = [];
  for (let i = 1; i < pts.length - 1; i++) idx.push(0, i, i + 1);
  g.setIndex(idx);
  g.computeVertexNormals();
  return paint(g, color);
}

/** Forked caudal fin, in the YZ plane at the tail. */
function tailFin(h, color) {
  return finFromPoints([
    [0,  0.00, -0.46],
    [0,  h,    -0.72],
    [0,  h * 0.30, -0.56],
    [0, -h * 0.30, -0.56],
    [0, -h,    -0.72],
  ], color);
}

/** Dorsal ridge: long and low along the back, not a sail. */
function dorsalFin(top, h, color) {
  return finFromPoints([
    [0, top,            0.18],
    [0, top + h,       -0.02],
    [0, top + h * 0.9, -0.18],
    [0, top,           -0.30],
  ], color);
}

/** Anal fin, underneath, small. */
function analFin(bot, h, color) {
  return finFromPoints([
    [0, bot,       -0.10],
    [0, bot - h,   -0.24],
    [0, bot,       -0.34],
  ], color);
}

/** Pectoral, in the XZ-ish plane at the shoulder. */
function pectoralFin(side, len, color) {
  return finFromPoints([
    [0, 0, 0.10],
    [len * side, -0.05, -0.06],
    [len * side * 0.55, 0.02, -0.14],
  ], color);
}

/**
 * The species table. Names, colours and body plans keyed to the Krebs Lake
 * entries in 04_species_and_maps.json.
 */
export const SPECIES_LOOK = {
  'Bluegill':        { plan: 'deep',  body: 0x4f6a46, belly: 0xc98a3e, fin: 0x37452f, marks: 'bars' },
  'Channel Catfish': { plan: 'cat',   body: 0x6a6257, belly: 0xd6cdb8, fin: 0x4c463d, marks: 'none' },
  'Speckled Trout':  { plan: 'lean',  body: 0x8d99a0, belly: 0xdfe3e6, fin: 0x6c777e, marks: 'speckles' },
  'Red Drum':        { plan: 'heavy', body: 0xb57038, belly: 0xe3cba6, fin: 0x8d552a, marks: 'spot' },
  'Black Drum':      { plan: 'heavy', body: 0x5b5a58, belly: 0xb4b0a8, fin: 0x434240, marks: 'bars' },
};

const DEFAULT_LOOK = SPECIES_LOOK['Bluegill'];

/**
 * @param {string} speciesName  a name from 04_species_and_maps.json
 * @param {number} lengthUnits  world length, scaled from weight by the caller
 */
export function createFish(speciesName, lengthUnits = 0.30) {
  const look = SPECIES_LOOK[speciesName] ?? DEFAULT_LOOK;
  const mat = createRetroMaterial({ affine: false, doubleSide: true });

  const root = new THREE.Object3D();
  root.name = `fish_${speciesName}`;

  const body = new THREE.Mesh(paint(buildBody(look.plan), look.body), mat);
  root.add(body);

  // Belly: a second, slightly smaller body squashed downward. Two-tone at a
  // hard seam is exactly how the era did counter-shading.
  const bellyGeo = paint(buildBody(look.plan), look.belly);
  const belly = new THREE.Mesh(bellyGeo, mat);
  belly.scale.set(0.96, 0.52, 0.97);
  belly.position.y = -0.055;
  root.add(belly);

  // Fins, all sized off the body's own depth so they stay in proportion
  // whichever body plan this is.
  const depth = PLANS[look.plan].rings[3];
  root.add(new THREE.Mesh(tailFin(depth * 0.95, look.fin), mat));
  root.add(new THREE.Mesh(dorsalFin(depth * 0.88, depth * 0.42, look.fin), mat));
  root.add(new THREE.Mesh(analFin(-depth * 0.80, depth * 0.34, look.fin), mat));
  for (const side of [-1, 1]) {
    const pec = new THREE.Mesh(pectoralFin(side, depth * 0.85, look.fin), mat);
    pec.position.set(depth * 0.45 * side, -depth * 0.25, 0.12);
    root.add(pec);
  }

  // Markings. These are what make the render style help rather than hurt:
  // crushed to 128px and 15-bit colour, "one black spot at the tail" and
  // "silver with speckles" stay instantly different.
  if (look.marks === 'spot') {
    // The one black spot at the tail. On a red drum this is THE identifying
    // mark, and 11_BANK_WALTER_v2.md leans on it surviving 128px and 15-bit
    // colour — so it has to be big enough to survive them.
    const spot = new THREE.Mesh(paint(new THREE.SphereGeometry(0.085, 6, 5), 0x16130f), mat);
    spot.position.set(0, 0.045, -0.40);
    spot.scale.set(1.25, 1.0, 0.30);
    root.add(spot);
  } else if (look.marks === 'speckles') {
    for (let i = 0; i < 9; i++) {
      const s = new THREE.Mesh(paint(new THREE.BoxGeometry(0.026, 0.026, 0.012), 0x14161a), mat);
      s.position.set(
        (i % 2 ? 1 : -1) * 0.075,
        0.10 - (i % 3) * 0.055,
        0.30 - i * 0.075,
      );
      root.add(s);
    }
  } else if (look.marks === 'bars') {
    for (let i = 0; i < 4; i++) {
      const b = new THREE.Mesh(paint(new THREE.BoxGeometry(0.16, 0.22, 0.022), 0x2c3a28), mat);
      b.position.set(0, 0.02, 0.20 - i * 0.15);
      root.add(b);
    }
  }

  if (look.plan === 'cat') {
    for (const side of [-1, 1]) {
      const barbel = new THREE.Mesh(paint(new THREE.BoxGeometry(0.012, 0.012, 0.18), 0x5a5248), mat);
      barbel.position.set(0.05 * side, 0.02, 0.54);
      barbel.rotation.y = 0.5 * side;
      root.add(barbel);
    }
  }

  root.scale.setScalar(lengthUnits / 1.0);
  root.userData.species = speciesName;
  root.userData.material = mat;
  return root;
}

/** Swim wobble. `swim` 0..1 scales how hard it is thrashing. */
export function animateFish(fish, elapsed, swim = 1) {
  fish.rotation.z = Math.sin(elapsed * 7.0) * 0.12 * swim;
  fish.rotation.y += (Math.sin(elapsed * 5.0) * 0.10 * swim - fish.rotation.y) * 0.2;
}

// ---------------------------------------------------------------------------
// Weight

/**
 * Pick a weight inside the species' range, biased low so a big one stays an
 * event. `04_species_and_maps.json` ranges are typical rod-and-reel catches.
 */
export function rollWeight(species, rng = Math.random) {
  const { min, max } = species.weight_lb;
  const skew = Math.pow(rng(), 2.1);        // most fish are small ones
  return +(min + (max - min) * skew).toFixed(2);
}

/** World length for a weight. Rough, and only has to look right. */
export function lengthForWeight(lb) {
  return THREE.MathUtils.clamp(0.16 + Math.cbrt(lb) * 0.20, 0.16, 1.10);
}
