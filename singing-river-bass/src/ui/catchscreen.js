// src/ui/catchscreen.js
//
// The catch celebration. 00_DESIGN_BIBLE.md calls this non-negotiable and it
// is the whole reward loop, so it is built early and it should feel slightly
// excessive.
//
//   Everything stops. The fish rotates on a turntable against a colour-banded
//   backdrop. Species name in big letters. Weight counts UP to its final value
//   with a tick per tenth. Fanfare. NEW PERSONAL BEST! in stretched italic if
//   it beats the stored record. Hold four full seconds before letting them back.
//
// Three lengths, per 11_BANK_WALTER_v2.md §6:
//   small fish        1.5 s, a chime
//   over about 2 lb   4 s, turntable, fanfare
//   Walter            longer still, and his own music  <- Stage 4
//
// The turntable is a real 3D pass: the fish is re-rendered through the same
// 320x240 pipeline, so it dithers and wobbles like everything else.

import * as THREE from 'three';
import { createFish, animateFish } from '../game/fish.js';
import { createWalter } from '../game/walter.js';
import { createRetroMaterial, paint, syncRetroLighting } from '../render/retro.js';
import * as sfx from '../audio/sfx.js';

const SMALL_SECONDS = 1.5;
const BIG_SECONDS = 4.0;
// Longer still, and he gets his own music. The longest ceremony in the game —
// and it still is not the end of his beat, because the release follows it.
const WALTER_SECONDS = 6.5;

export class CatchScreen {
  constructor(uiRoot) {
    this.el = {
      root: uiRoot.querySelector('#catch'),
      species: uiRoot.querySelector('#catch-species'),
      weight: uiRoot.querySelector('#catch-weight'),
      best: uiRoot.querySelector('#catch-best'),
      sub: uiRoot.querySelector('#catch-sub'),
    };

    // Its own little scene, rendered through the same pipeline.
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(42, 320 / 240, 0.05, 20);
    this.camera.position.set(0, 0.05, 1.5);
    this.camera.lookAt(0, 0, 0);

    // Colour-banded backdrop. Flat horizontal bands, because that is what the
    // era did and it stops the fish floating in a void.
    // Bright enough that a dark fish still reads against it. Unlit — the bands
    // are a backdrop, not part of the world, so they take the full ambient.
    const bandMat = createRetroMaterial({ affine: false, snap: false, ambientBoost: 2.6 });
    const bands = new THREE.Object3D();
    const palette = [0x2d5d7e, 0x3d7d92, 0x54a08f, 0x79b978, 0xa8c86a];
    palette.forEach((c, i) => {
      const q = new THREE.Mesh(paint(new THREE.PlaneGeometry(8, 0.6), c), bandMat);
      q.position.set(0, 1.2 - i * 0.6, -2.2);
      bands.add(q);
    });
    this.scene.add(bands);
    this.bandMat = bandMat;

    this.turntable = new THREE.Object3D();
    this.scene.add(this.turntable);

    this.active = false;
    this.fish = null;
    this.t = 0;
    this.duration = 0;
    this.onDone = null;
  }

  /** @param {{species:string, lb:number, length:number, big:boolean, isPersonalBest:boolean}} fish */
  show(fish, onDone) {
    this.onDone = onDone;
    this.active = true;
    this.t = 0;
    this.tickedTenths = 0;
    this.data = fish;
    this.duration = fish.walter ? WALTER_SECONDS : fish.big ? BIG_SECONDS : SMALL_SECONDS;

    // Start broadside. The profile is what identifies a fish; nose-on it is a
    // blob whatever you do to the geometry.
    this.turntable.rotation.y = Math.PI / 2;
    if (this.fish) this.turntable.remove(this.fish);
    // Scale up for the presentation — a bluegill at true scale is a speck.
    this.fish = fish.walter
      ? createWalter(fish.form)
      : createFish(fish.species, Math.max(0.55, fish.length * 1.9));
    if (fish.walter) this.fish.scale.multiplyScalar(0.95);
    this.turntable.add(this.fish);
    // The turntable is a presentation, not the bank. Light it from the front
    // so the markings that distinguish one species from another actually show.
    this.fish.userData.material.userData.ambientBoost = 1.9;
    this.fish.userData.material.userData.fillFromCamera = 0.45;
    syncRetroLighting(this.scene, {
      sun: new THREE.Vector3(0.30, 0.65, 0.70).normalize(),
      sunColor: new THREE.Color(1.0, 0.94, 0.84),
      ambient: new THREE.Color(0.36, 0.35, 0.34),
      fogColor: new THREE.Color(0x0b1218),
      fogNear: 6, fogFar: 18,
    });

    // `WALTER — TROUT`, not `SPECKLED TROUT`. Naming the size rather than the
    // species is how people who actually fish it talk.
    this.el.species.textContent = (fish.label ?? fish.species).toUpperCase();
    this.el.weight.textContent = '0.00 LBS';
    this.el.best.classList.toggle('on', !!fish.isPersonalBest);
    this.el.sub.textContent = fish.scientific ?? '';
    this.el.root.classList.add('on');
    this.el.root.classList.toggle('big', !!(fish.big || fish.walter));
    this.el.root.classList.toggle('walter', !!fish.walter);
    // Everything stops. The rest of the HUD gets out of the way — a reel bar
    // and a bite prompt underneath the ceremony ruins it.
    this.el.root.parentElement.classList.add('celebrating');

    if (fish.walter) sfx.sfxWalterFanfare();
    else if (fish.big) sfx.sfxFanfare();
    else sfx.sfxChime();
  }

  update(dt, elapsed) {
    if (!this.active) return;
    this.t += dt;

    // Weight counts UP with a tick per tenth. This is most of the drama.
    const countFor = Math.min(this.duration * 0.55, 1.8);
    const p = Math.min(1, this.t / countFor);
    const shown = this.data.lb * p;
    this.el.weight.textContent = `${shown.toFixed(2)} LBS`;
    const tenths = Math.floor(shown * 10);
    if (tenths > this.tickedTenths) {
      this.tickedTenths = tenths;
      if (tenths % 2 === 0) sfx.sfxTick();
    }

    this.turntable.rotation.y += dt * (this.data.walter ? 0.72 : this.data.big ? 0.95 : 1.8);
    if (this.fish) animateFish(this.fish, elapsed, 0.35);

    if (this.t >= this.duration) this.hide();
  }

  hide() {
    this.active = false;
    this.el.root.classList.remove('on');
    this.el.root.parentElement.classList.remove('celebrating');
    this.onDone?.();
  }
}
