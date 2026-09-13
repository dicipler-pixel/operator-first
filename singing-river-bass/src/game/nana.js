// src/game/nana.js
//
// NANA. The one and only playable character — no roster, no select screen.
// Built to 09_CHARACTER_NANA_v2.md. Stance is B, seated on the bank, settled
// by 11_BANK_WALTER_v2.md, so §7 of 09 is closed.
//
// SEGMENTED RIGID BODY. No skinned mesh, no rig, no Blender. Solid parts
// parented into a hierarchy and animated by rotating the joints, exactly as
// PS1-era characters were built. The visible shoulder seam is period-correct
// and is not a bug to hide.
//
// Budget is about 410 triangles, and the hair gets the largest single
// allocation of any part of her, because you see her from behind for ~95% of
// the game and the back of her head is the entire recognition budget.

import * as THREE from 'three';
import { createRetroMaterial, paint, paintShaded } from '../render/retro.js';

// Wardrobe, translated from the reference into something she'd wear on the
// water with every silhouette cue intact.
const SKIN     = 0xc9a288;
const HAIR_1   = 0xb9b7b2;   // silver-grey, flat bands, not a gradient
const HAIR_2   = 0xa3a19d;
const HAIR_3   = 0xcac8c4;
const SHIRT    = 0xeae4d6;   // cream/white overshirt, worn open
const UNDER    = 0x1c1c1e;   // black-and-white patterned top
const UNDER_HI = 0xe8e8e8;
const TROUSER  = 0x232326;
const BAG      = 0x4a4036;
const GOLD     = 0xc8a53c;   // a few pixels at the throat for the chain

function box(w, h, d, color, shaded = true) {
  const g = new THREE.BoxGeometry(w, h, d);
  return shaded ? paintShaded(g, color) : paint(g, color);
}

/** A box narrower at one end. Everything on her is one of these. */
function taperedBox(w, h, d, color, topScale = 0.8, shaded = true) {
  const g = new THREE.BoxGeometry(w, h, d);
  const pos = g.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    if (pos.getY(i) > 0) {
      pos.setX(i, pos.getX(i) * topScale);
      pos.setZ(i, pos.getZ(i) * topScale);
    }
  }
  pos.needsUpdate = true;
  g.computeVertexNormals();
  return shaded ? paintShaded(g, color) : paint(g, color);
}

function part(geo, mat, x = 0, y = 0, z = 0) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  return m;
}

/**
 * Build Nana.
 *
 * Returns the root Object3D with a `joints` map. Animation is rotating those
 * joints — there are no animation files anywhere in this project.
 */
export function createNana() {
  const mat = createRetroMaterial({ affine: false, ambientBoost: 1.55, fillFromCamera: 0.34 });

  const root = new THREE.Object3D();
  root.name = 'nana';

  const joints = {};

  // ---- hips: the anchor everything hangs from -------------------------
  const hips = new THREE.Object3D();
  hips.position.y = 0.46;              // seat height of a folding camp chair
  root.add(hips);
  joints.hips = hips;

  // ---- torso ----------------------------------------------------------
  const torso = new THREE.Object3D();
  hips.add(torso);
  joints.torso = torso;

  // Cream overshirt is the second-biggest recognition cue after the hair —
  // a pale torso against dark water.
  torso.add(part(taperedBox(0.40, 0.52, 0.24, SHIRT, 0.86), mat, 0, 0.26, 0));
  // Patterned top showing at the collar and the front opening. At this size
  // that is a handful of pixels of alternating black and white; bold irregular
  // blocks read, a literal zebra turns to mush.
  torso.add(part(box(0.13, 0.34, 0.03, UNDER), mat, 0, 0.30, 0.115));
  torso.add(part(box(0.05, 0.07, 0.02, UNDER_HI), mat, 0.0, 0.40, 0.126));
  torso.add(part(box(0.04, 0.05, 0.02, UNDER_HI), mat, -0.01, 0.27, 0.126));
  // Two or three pixels of gold at the throat. Registers without ever being legible.
  torso.add(part(box(0.06, 0.02, 0.02, GOLD), mat, 0, 0.47, 0.115));

  // Small tackle bag on a shoulder strap, worn across. Stands in for the
  // handbag in the reference.
  const bag = part(box(0.16, 0.13, 0.08, BAG), mat, -0.21, 0.20, 0.02);
  bag.rotation.z = 0.2;
  torso.add(bag);
  torso.add(part(box(0.04, 0.42, 0.02, BAG), mat, -0.12, 0.34, 0.09));

  // ---- head -----------------------------------------------------------
  const neck = new THREE.Object3D();
  neck.position.y = 0.54;
  torso.add(neck);
  joints.neck = neck;

  neck.add(part(box(0.09, 0.07, 0.09, SKIN), mat, 0, 0.03, 0));
  const head = part(taperedBox(0.20, 0.22, 0.21, SKIN, 1.06), mat, 0, 0.17, 0);
  neck.add(head);

  // Face. Two dark dots, one curved mouth, two short brow strokes. That is the
  // whole face and it should be. Do not chase likeness — at this triangle count
  // a realistic attempt reads as a corpse. Chase recognition instead.
  const face = new THREE.Object3D();
  face.position.set(0, 0.18, 0.107);
  neck.add(face);
  const dark = createRetroMaterial({ affine: false, ambientBoost: 1.55, fillFromCamera: 0.34 });
  face.add(part(box(0.022, 0.022, 0.01, 0x241c18), dark, -0.045, 0.01, 0));
  face.add(part(box(0.022, 0.022, 0.01, 0x241c18), dark,  0.045, 0.01, 0));
  face.add(part(box(0.030, 0.008, 0.01, 0x3b2f28), dark, -0.045, 0.055, 0));
  face.add(part(box(0.030, 0.008, 0.01, 0x3b2f28), dark,  0.048, 0.058, 0));
  // The slightly amused half-smile from the reference, not a neutral line.
  // One pixel of asymmetry does an enormous amount of work.
  const mouth = part(box(0.055, 0.010, 0.01, 0x8d5a52), dark, 0.002, -0.048, 0);
  mouth.rotation.z = 0.09;
  face.add(mouth);
  face.add(part(box(0.014, 0.010, 0.01, 0x8d5a52), dark, 0.034, -0.040, 0));

  // ---- hair: the largest single allocation ----------------------------
  // Long, full, wavy silver-grey, shoulder length and past it. Loose and
  // voluminous, not tidy. Three or four overlapping soft-edged shapes rather
  // than one solid helmet, so the silhouette breaks up and reads as volume
  // instead of a bicycle helmet. NO HAT — a brim would cover the one feature
  // that makes her recognisable.
  const hair = new THREE.Object3D();
  neck.add(hair);
  joints.hair = hair;

  // crown — kept narrow so the mass below it reads as separate
  hair.add(part(taperedBox(0.225, 0.15, 0.235, HAIR_1, 0.78), mat, 0, 0.235, -0.006));

  // Back mass, the piece that actually carries her from behind. Tapered WIDER
  // at the bottom so the outline flares out instead of hanging square, and
  // split into two overlapping tiers at different greys so there is a visible
  // seam across it. A single solid block here is the bicycle-helmet failure.
  hair.add(part(taperedBox(0.225, 0.26, 0.165, HAIR_2, 1.22), mat, 0, 0.105, -0.100));
  hair.add(part(taperedBox(0.265, 0.24, 0.150, HAIR_1, 1.10), mat, 0.008, -0.115, -0.108));
  hair.add(part(taperedBox(0.215, 0.17, 0.115, HAIR_3, 0.80), mat, -0.020, -0.270, -0.098));

  // Two side falls, deliberately uneven and hanging well past the jaw so the
  // silhouette is not symmetrical and not a closed curve.
  const fallL = part(taperedBox(0.105, 0.46, 0.150, HAIR_3, 1.10), mat, -0.128, -0.030, -0.030);
  fallL.rotation.z = 0.12;
  hair.add(fallL);
  const fallR = part(taperedBox(0.090, 0.39, 0.145, HAIR_2, 1.18), mat, 0.132, 0.020, -0.026);
  fallR.rotation.z = -0.09;
  hair.add(fallR);

  // A loose piece over one shoulder. One asymmetric flyaway does most of the
  // work of making it read as loose and voluminous rather than tidy.
  const loose = part(taperedBox(0.075, 0.26, 0.085, HAIR_3, 1.15), mat, -0.148, -0.255, 0.020);
  loose.rotation.z = 0.26;
  hair.add(loose);
  const loose2 = part(taperedBox(0.060, 0.18, 0.070, HAIR_1, 1.1), mat, 0.152, -0.215, 0.010);
  loose2.rotation.z = -0.22;
  hair.add(loose2);

  // ---- arms: rod arm is RIGHT, reel hand is LEFT ----------------------
  function arm(side) {
    const shoulder = new THREE.Object3D();
    shoulder.position.set(0.21 * side, 0.50, 0);
    torso.add(shoulder);
    shoulder.add(part(taperedBox(0.105, 0.26, 0.115, SHIRT, 0.92), mat, 0, -0.13, 0));

    const elbow = new THREE.Object3D();
    elbow.position.y = -0.25;
    shoulder.add(elbow);
    elbow.add(part(taperedBox(0.09, 0.24, 0.095, SHIRT, 0.9), mat, 0, -0.12, 0));

    const wrist = new THREE.Object3D();
    wrist.position.y = -0.235;
    elbow.add(wrist);
    // Mitten block. No fingers — nobody had fingers in 1997.
    wrist.add(part(box(0.085, 0.10, 0.075, SKIN), mat, 0, -0.05, 0));
    return { shoulder, elbow, wrist };
  }

  // She is BUILT facing +Z (the face is at +z) and then turned to face away
  // from the camera, which mirrors left and right. Her anatomical right is
  // therefore local -X. Get this backwards and the rod ends up in the wrong
  // hand and the cooler sits on her casting side.
  const right = arm(-1);
  const left = arm(1);
  joints.rShoulder = right.shoulder; joints.rElbow = right.elbow; joints.rHand = right.wrist;
  joints.lShoulder = left.shoulder;  joints.lElbow = left.elbow;  joints.lHand = left.wrist;

  // ---- legs: seated, so thighs run forward and shins drop -------------
  function leg(side) {
    const hip = new THREE.Object3D();
    hip.position.set(0.115 * side, 0.02, 0.02);
    hips.add(hip);
    hip.rotation.x = -Math.PI / 2 + 0.12;      // thigh forward: she is sitting
    hip.add(part(taperedBox(0.145, 0.36, 0.165, TROUSER, 0.92), mat, 0, -0.18, 0));

    const knee = new THREE.Object3D();
    knee.position.y = -0.36;
    hip.add(knee);
    knee.rotation.x = Math.PI / 2 - 0.06;      // shin down
    knee.add(part(taperedBox(0.115, 0.36, 0.125, TROUSER, 0.88), mat, 0, -0.18, 0));

    const ankle = new THREE.Object3D();
    ankle.position.y = -0.37;
    knee.add(ankle);
    ankle.add(part(box(0.115, 0.07, 0.20, 0x2e2a26), mat, 0, -0.035, 0.045));
    return { hip, knee, ankle };
  }
  const legR = leg(1), legL = leg(-1);
  joints.rHip = legR.hip; joints.rKnee = legR.knee; joints.rAnkle = legR.ankle;
  joints.lHip = legL.hip; joints.lKnee = legL.knee; joints.lAnkle = legL.ankle;

  // Seated rest pose. Rod arm forward and up, reel hand in at the reel.
  joints.rShoulder.rotation.set(-0.55, 0, -0.30);
  joints.rElbow.rotation.set(-0.55, 0, 0);
  joints.lShoulder.rotation.set(-0.42, 0, 0.36);
  joints.lElbow.rotation.set(-0.95, 0, 0);
  joints.torso.rotation.x = -0.06;

  root.userData.joints = joints;
  root.userData.material = mat;
  return root;
}

// ---------------------------------------------------------------------------
// Five animations, all procedural. Rotate the joint nodes in code.
// ---------------------------------------------------------------------------

const REST = {
  rShoulder: [-0.55, 0, -0.30], rElbow: [-0.55, 0, 0],
  lShoulder: [-0.42, 0, 0.36],  lElbow: [-0.95, 0, 0],
  torso: [-0.06, 0, 0], neck: [0, 0, 0],
};

function lerpTo(node, target, k) {
  node.rotation.x += (target[0] - node.rotation.x) * k;
  node.rotation.y += (target[1] - node.rotation.y) * k;
  node.rotation.z += (target[2] - node.rotation.z) * k;
}

/**
 * @param {THREE.Object3D} nana
 * @param {string} state  idle | cast | reel | fight | lift
 * @param {number} t      seconds elapsed in this state
 * @param {number} elapsed global clock, for the idle sway
 * @param {number} [intensity=0] 0..1, how hard the fish is pulling
 */
export function animateNana(nana, state, t, elapsed, intensity = 0) {
  const j = nana.userData.joints;
  const k = 0.22;

  // Seated idle: a slow settle rather than a boat rock. She is on solid
  // ground in a camp chair, so it is breath and the occasional weight shift.
  const breathe = Math.sin(elapsed * 1.1) * 0.012;
  const shift = Math.sin(elapsed * 0.23) * 0.03;

  switch (state) {
    case 'cast': {
      // Wind back over the shoulder, torso twists, then snap forward.
      const p = Math.min(1, t / 0.85);
      const wind = p < 0.45 ? p / 0.45 : 1 - (p - 0.45) / 0.55;
      const snap = p < 0.45 ? 0 : (p - 0.45) / 0.55;
      lerpTo(j.rShoulder, [-0.55 - wind * 1.5 + snap * 1.1, 0, -0.30 - wind * 0.35], 0.45);
      lerpTo(j.rElbow, [-0.55 - wind * 1.2 + snap * 0.9, 0, 0], 0.45);
      lerpTo(j.torso, [-0.06, -wind * 0.34 + snap * 0.22, 0], 0.35);
      lerpTo(j.lShoulder, REST.lShoulder, k);
      lerpTo(j.lElbow, REST.lElbow, k);
      break;
    }
    case 'reel': {
      // Left hand cranks a circle. Rod arm stays fairly still. Slight lean.
      const a = t * 7.5;
      j.lElbow.rotation.x = -0.95 + Math.sin(a) * 0.34;
      j.lShoulder.rotation.z = 0.36 + Math.cos(a) * 0.16;
      j.lShoulder.rotation.x = -0.42 + Math.sin(a) * 0.07;
      lerpTo(j.rShoulder, [-0.72, 0, -0.30], k);
      lerpTo(j.rElbow, [-0.60, 0, 0], k);
      lerpTo(j.torso, [-0.12, 0, 0], k);
      break;
    }
    case 'fight': {
      // Lean back, rod arm high and bent, torso strains against the pull.
      const strain = Math.sin(elapsed * 5.5) * 0.05 * intensity;
      lerpTo(j.rShoulder, [-1.28 - intensity * 0.3 + strain, 0, -0.26], k);
      lerpTo(j.rElbow, [-1.05 - intensity * 0.2, 0, 0], k);
      lerpTo(j.torso, [0.16 + intensity * 0.16 + strain, 0, 0], k);
      lerpTo(j.neck, [-0.10, 0, 0], k);
      // reel hand still cranks, but harder work
      const a = t * 5.0;
      j.lElbow.rotation.x = -0.95 + Math.sin(a) * 0.26;
      j.lShoulder.rotation.z = 0.36 + Math.cos(a) * 0.12;
      break;
    }
    case 'lift': {
      // The one that matters. Both arms up, fish held out at chest height,
      // head tilts toward it. This plays on the catch celebration.
      const p = Math.min(1, t / 0.6);
      lerpTo(j.rShoulder, [-1.45 * p, 0, -0.55 * p], 0.30);
      lerpTo(j.rElbow, [-1.15 * p, 0, 0], 0.30);
      lerpTo(j.lShoulder, [-1.45 * p, 0, 0.55 * p], 0.30);
      lerpTo(j.lElbow, [-1.15 * p, 0, 0], 0.30);
      lerpTo(j.torso, [-0.14, 0, 0], 0.25);
      lerpTo(j.neck, [0.20 * p, 0, 0.06 * p], 0.25);
      break;
    }
    case 'release': {
      // She leans over the arm of the chair and eases him into the shallows.
      // Slow, and she stays leaning while he sits there — that pause is the
      // whole beat, and rushing back upright throws it away.
      const p = Math.min(1, t / 1.6);
      const back = t > 3.6 ? Math.min(1, (t - 3.6) / 1.0) : 0;
      const lean = p * (1 - back);
      lerpTo(j.torso, [0.52 * lean - 0.06, -0.20 * lean, 0.10 * lean], 0.14);
      lerpTo(j.rShoulder, [-0.30 - 0.85 * lean, 0, -0.30 + 0.18 * lean], 0.14);
      lerpTo(j.rElbow, [-0.55 + 0.30 * lean, 0, 0], 0.14);
      lerpTo(j.lShoulder, [-0.42 - 0.80 * lean, 0, 0.36 - 0.14 * lean], 0.14);
      lerpTo(j.lElbow, [-0.95 + 0.42 * lean, 0, 0], 0.14);
      lerpTo(j.neck, [0.40 * lean, 0, 0], 0.14);
      break;
    }
    case 'cooler': {
      // Reaches down to her off-hand side, cracks one, sets it in the holder.
      const p = Math.min(1, t / 2.0);
      const down = p < 0.45 ? p / 0.45 : Math.max(0, 1 - (p - 0.45) / 0.35);
      lerpTo(j.lShoulder, [0.30 * down - 0.42 * (1 - down), 0, 0.36 + 0.42 * down], 0.30);
      lerpTo(j.lElbow, [-0.95 + 0.55 * down, 0, 0], 0.30);
      lerpTo(j.torso, [-0.06 + 0.30 * down, 0, -0.18 * down], 0.25);
      lerpTo(j.neck, [0.22 * down, 0, 0], 0.25);
      lerpTo(j.rShoulder, REST.rShoulder, k);
      lerpTo(j.rElbow, REST.rElbow, k);
      break;
    }
    default: {
      lerpTo(j.rShoulder, REST.rShoulder, k);
      lerpTo(j.rElbow, REST.rElbow, k);
      lerpTo(j.lShoulder, REST.lShoulder, k);
      lerpTo(j.lElbow, REST.lElbow, k);
      lerpTo(j.torso, [REST.torso[0] + breathe, shift * 0.5, 0], k);
      lerpTo(j.neck, [breathe * 0.5, shift, 0], k);
    }
  }

  // Hair lags the head very slightly. One extra line, and it stops the whole
  // mass reading as welded on.
  j.hair.rotation.x += (-j.neck.rotation.x * 0.25 - j.hair.rotation.x) * 0.10;
  j.hair.rotation.z += (-j.neck.rotation.z * 0.30 - j.hair.rotation.z) * 0.10;
}
