// src/game/walter.js
//
// WALTER. Built to 11_BANK_WALTER_v2.md and 13_VOICE_v2.md §1.
//
// WALTER IS NOT A SPECIES. Walter is what you call the big one. He shows up as
// either a speckled trout or a redfish, and which one it is on any given day is
// part of the fish.
//
// That is the right answer for this water and it is not a compromise. Krebs
// Lake is brackish, and brackish Mississippi water has exactly two trophies in
// it: a gator speckled trout and a bull redfish. There is no third candidate.
//
// EACH FORM ALWAYS WEIGHS EXACTLY THE SAME, EVERY SINGLE TIME. Not a random big
// specimen. The number never moves. That is what makes him Walter.
//
// Both weights sit deliberately ABOVE the normal maximum for their species in
// 04_species_and_maps.json — 6.00 lb for speckled trout, 30.00 lb for red drum.
// Walter is off the table. Nothing else in the game can reach him.

import * as THREE from 'three';
import { createFish } from './fish.js';
import { createRetroMaterial, paint } from '../render/retro.js';

export const WALTER_FORMS = {
  trout: {
    key: 'trout',
    label: 'WALTER — TROUT',
    species: 'Speckled Trout',
    scientific: 'Cynoscion nebulosus',
    lb: 8.40,                 // never moves
    length: 0.95,
    // Long and lean. Silver-green flank, hard black speckles, yellow inside
    // the mouth.
    fight: 'shallow',
  },
  red: {
    key: 'red',
    label: 'WALTER — RED',
    species: 'Red Drum',
    scientific: 'Sciaenops ocellatus',
    lb: 34.80,                // never moves
    length: 1.35,
    // Deep-bodied and heavy. Copper-bronze, one black spot at the tail.
    fight: 'deep',
  },
};

/**
 * The fish himself, in colour. Only ever shown at the reveal and afterwards —
 * for most of the fight he is the shadow below.
 */
export function createWalter(formKey) {
  const form = WALTER_FORMS[formKey];
  const fish = createFish(form.species, form.length);

  // He reads bigger than a normal one of his species, which is the whole point.
  const mat = fish.userData.material;
  mat.userData.ambientBoost = 1.35;
  mat.userData.fillFromCamera = 0.22;

  if (formKey === 'trout') {
    // Yellow inside the mouth. Three or four pixels at this size, and it is
    // the detail that separates a gator trout from a big one.
    const mouth = new THREE.Mesh(
      paint(new THREE.BoxGeometry(0.085, 0.055, 0.05), 0xd9a52c),
      mat,
    );
    mouth.position.set(0, -0.02, 0.46);
    fish.add(mouth);
  }

  fish.userData.walterForm = formKey;
  return fish;
}

/**
 * What she actually sees for most of the fight: a heavy shape under the
 * surface, a boil, a swirl. NO COLOUR.
 *
 * 11_BANK_WALTER_v2.md is explicit that the reveal is the best beat in the
 * game, and it only works if there is nothing to read beforehand. A coloured
 * fish visible at twenty seconds throws the whole thing away.
 */
export function createWalterShadow() {
  const mat = createRetroMaterial({ affine: false, ambientBoost: 0.30, doubleSide: true });
  const o = new THREE.Object3D();
  o.name = 'walter_shadow';

  // The mass. Dark, indistinct, deliberately not fish-shaped enough to read as
  // one form or the other.
  const body = new THREE.Mesh(paint(new THREE.SphereGeometry(0.55, 7, 5), 0x0d1410), mat);
  body.scale.set(0.42, 0.55, 1.55);
  o.add(body);

  // The boil: a flat disc on the surface above him, slightly bigger than he is.
  const boilMat = createRetroMaterial({ affine: false, ambientBoost: 1.4, transparent: true, alpha: 0.45, doubleSide: true });
  const boil = new THREE.Mesh(paint(new THREE.CircleGeometry(0.95, 10), 0x7d8f76), boilMat);
  boil.rotation.x = -Math.PI / 2;
  o.add(boil);
  o.userData.boil = boil;
  o.userData.boilMat = boilMat;

  // A swirl trailing off it, so the surface says something is down there
  // moving without ever saying what.
  const swirl = new THREE.Mesh(paint(new THREE.RingGeometry(0.9, 1.35, 12), 0x94a68b), boilMat);
  swirl.rotation.x = -Math.PI / 2;
  swirl.position.y = 0.01;
  o.add(swirl);
  o.userData.swirl = swirl;

  return o;
}

/**
 * Fight profiles. A big red fights deep and slow and dogged. A gator trout runs
 * shallow and headshakes and jumps.
 *
 * These have to FEEL different, so that by about twenty seconds in she starts
 * to suspect which one she's got — and is sometimes wrong. The overlap is the
 * point: the red's occasional hard surge and the trout's occasional long sullen
 * hold are what make a confident guess wrong often enough to matter.
 *
 * @returns {{pull:number, headshake:number, jump:boolean, depth:number}}
 */
export function walterFightProfile(formKey, t, seed = 0) {
  if (formKey === 'red') {
    // Deep, slow, dogged. Long sustained pressure, rare but heavy surges.
    const base = 0.62 + Math.sin(t * 0.55 + seed) * 0.16;
    const surge = Math.pow(Math.max(0, Math.sin(t * 0.31 + seed * 2)), 6) * 0.55;
    return {
      pull: base + surge,
      headshake: 0.04,
      jump: false,
      depth: 0.85 + Math.sin(t * 0.4) * 0.10,     // stays down
    };
  }
  // Shallow, fast, headshakes and jumps.
  const base = 0.44 + Math.sin(t * 1.35 + seed) * 0.20;
  const shake = Math.pow(Math.max(0, Math.sin(t * 4.2 + seed)), 3);
  const sullen = Math.pow(Math.max(0, Math.sin(t * 0.24 + seed * 3)), 8) * 0.34;
  return {
    pull: base + shake * 0.30 + sullen,
    headshake: 0.22 + shake * 0.35,
    jump: Math.sin(t * 0.9 + seed) > 0.93,
    depth: 0.30 + Math.sin(t * 1.1) * 0.22,       // runs shallow
  };
}

/**
 * How long he takes to bring in, holding the bar. Seven seconds.
 *
 * DELIBERATE DEVIATION FROM 11_BANK_WALTER_v2.md §3, which asks for thirty to
 * sixty seconds against five for everything else. That was far too much fuss
 * on a phone for the player this is built for, and it is what made him feel
 * uncatchable rather than hard.
 *
 * Seven is the settled number: about half again as long as an ordinary fish,
 * so he registers as heavier and there is room for the shape under the surface
 * to move before the reveal — but everything that made him a test is gone. The
 * bite and the hook window are the ordinary ones; this is the only thing about
 * catching him that differs at all.
 *
 * Reeling is continuous, so this is the real duration, not a target that a
 * tension mechanic then stretches.
 */
export const WALTER_FIGHT_SECONDS = 7;

export function walterFightSeconds() {
  return WALTER_FIGHT_SECONDS;
}
