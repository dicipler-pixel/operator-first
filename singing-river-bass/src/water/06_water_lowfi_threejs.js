// SCRIPT: 06_water_lowfi_threejs.js
// SINGING RIVER BASS - late-90s water for Three.js
//
// Port of 03_water_lowfi.gdshader. Same technique, same look, WebGL instead of Godot.
// Period-correct on purpose: no screen-space reflection, no refraction, no depth
// buffer read, no normal map, no textures at all. A 1997 console could not do any of
// those, and faking them is what makes retro water look wrong.
//
// Tested: GLSL parsed clean. Not run against a live GL context here - if the console
// throws on first frame, paste the error and I will fix it rather than guess.
//
// Pinned against three 0.186.0.

import * as THREE from 'three';

// ---------------------------------------------------------------------------
// PER-MAP PRESETS
// ---------------------------------------------------------------------------
export const WATER_PRESETS = {
  // Brackish oxbow of the Pascagoula. Near-still. Warm evening light.
  krebs: {
    deep: [0.06, 0.10, 0.06], shallow: [0.26, 0.30, 0.18],
    sky:  [0.72, 0.56, 0.38], glint:   [1.00, 0.92, 0.70],
    waveHeight: 0.025, waveScale: 1.1, waveSpeed: 0.35,
    rippleScale: 6.0, rippleSpeed: 0.35, bands: 6.0, opacity: 0.94,
  },
  // Green-brown, actually moving. Visible current.
  pascagoula: {
    deep: [0.06, 0.14, 0.10], shallow: [0.30, 0.38, 0.22],
    sky:  [0.60, 0.68, 0.70], glint:   [1.00, 0.96, 0.82],
    waveHeight: 0.07, waveScale: 1.6, waveSpeed: 0.85,
    rippleScale: 11.0, rippleSpeed: 0.70, bands: 6.0, opacity: 0.92,
  },
  // Blackwater. Tannin-stained, the colour of strong iced tea, amber where it
  // shallows over white sand. Keep bands LOW - this is a two-colour picture and
  // banding makes it look better, not worse.
  escatawpa: {
    deep: [0.03, 0.03, 0.02], shallow: [0.34, 0.22, 0.07],
    sky:  [0.62, 0.66, 0.62], glint:   [0.95, 0.88, 0.68],
    waveHeight: 0.02, waveScale: 0.9, waveSpeed: 0.25,
    rippleScale: 5.0, rippleSpeed: 0.30, bands: 4.0, opacity: 0.97,
  },
  // Deep, clear, blue-green. Open-water chop.
  lanier: {
    deep: [0.02, 0.10, 0.16], shallow: [0.16, 0.44, 0.46],
    sky:  [0.58, 0.74, 0.88], glint:   [1.00, 0.98, 0.90],
    waveHeight: 0.11, waveScale: 2.1, waveSpeed: 1.10,
    rippleScale: 14.0, rippleSpeed: 0.85, bands: 7.0, opacity: 0.88,
  },
};

// ---------------------------------------------------------------------------
const vertexShader = /* glsl */ `
uniform float uTime;
uniform float uWaveHeight;
uniform float uWaveScale;
uniform float uWaveSpeed;
uniform float uVertexSnap;
uniform vec2  uSnapRes;

varying vec3 vWorldPos;
varying vec3 vWorldNormal;

// Three sines at angles whose periods do not line up. Cheap, and it reads as water.
float waveSum(vec2 p, float t, float s) {
  float w = 0.0;
  w += sin(p.x * 1.00 * s + t * 1.00) * 0.50;
  w += sin(p.y * 1.37 * s - t * 0.83) * 0.30;
  w += sin((p.x + p.y) * 0.71 * s + t * 1.31) * 0.20;
  return w;
}

void main() {
  float t = uTime * uWaveSpeed;
  vec3 p = position;
  vec2 q = (modelMatrix * vec4(position, 1.0)).xz;

  p.y += waveSum(q, t, uWaveScale) * uWaveHeight;
  vWorldPos = (modelMatrix * vec4(p, 1.0)).xyz;

  // Rebuild the normal from the wave slope by sampling four nearby points.
  // Done in world space so it does not care how the geometry is oriented.
  float e = 0.15;
  float hL = waveSum(q - vec2(e, 0.0), t, uWaveScale) * uWaveHeight;
  float hR = waveSum(q + vec2(e, 0.0), t, uWaveScale) * uWaveHeight;
  float hD = waveSum(q - vec2(0.0, e), t, uWaveScale) * uWaveHeight;
  float hU = waveSum(q + vec2(0.0, e), t, uWaveScale) * uWaveHeight;
  vWorldNormal = normalize(vec3(hL - hR, 2.0 * e, hD - hU));

  vec4 clip = projectionMatrix * modelViewMatrix * vec4(p, 1.0);

  // PS1 vertex snapping - quantise clip space to the low-res grid. This is the
  // wobble. Without it the water looks modern no matter what colour it is.
  if (uVertexSnap > 0.5) {
    vec3 ndc = clip.xyz / clip.w;
    ndc.xy = floor(ndc.xy * uSnapRes) / uSnapRes;
    clip = vec4(ndc * clip.w, clip.w);
  }

  gl_Position = clip;
}
`;

const fragmentShader = /* glsl */ `
uniform float uTime;
uniform vec3  uDeep;
uniform vec3  uShallow;
uniform vec3  uSky;
uniform vec3  uGlint;
uniform float uOpacity;
uniform float uRippleScale;
uniform float uRippleSpeed;
uniform float uRippleDepth;
uniform float uBands;
uniform vec3  uSunDir;
uniform float uGlintSize;
uniform float uGlintPower;
uniform float uFresnelBias;

varying vec3 vWorldPos;
varying vec3 vWorldNormal;

float rippleLayer(vec2 p, float t) {
  float a = sin(p.x * 3.10 + t * 1.10) * cos(p.y * 2.30 - t * 0.80);
  float b = sin((p.x - p.y) * 4.10 - t * 1.60);
  return (a * 0.6 + b * 0.4) * 0.5 + 0.5;
}

void main() {
  float t = uTime * uRippleSpeed;
  vec2 uvw = vWorldPos.xz * (uRippleScale * 0.1);

  // Two layers drifting at different speeds and angles.
  float r = rippleLayer(uvw, t) * 0.6
          + rippleLayer(uvw * 1.9 + vec2(4.2, 1.7), -t * 0.7) * 0.4;

  // Crush to hard bands. This is the step that sells the era - real 15-bit water
  // had visible flat plateaus of colour, not a smooth gradient.
  r = floor(r * uBands) / uBands;

  // View angle. Looking down shows the water body, glancing shows sky.
  vec3 n = normalize(vWorldNormal);
  vec3 v = normalize(cameraPosition - vWorldPos);
  float facing = clamp(dot(n, v), 0.0, 1.0);
  float fres = pow(1.0 - facing, 3.0);
  fres = clamp(fres + uFresnelBias * (1.0 - facing), 0.0, 1.0);
  fres = floor(fres * uBands) / uBands;

  vec3 body = mix(uDeep, uShallow, r * uRippleDepth + (1.0 - uRippleDepth) * 0.5);
  vec3 col  = mix(body, uSky, fres);

  // Sun glint: a specular blob, hard-clipped so it has a visible edge rather
  // than a soft modern falloff.
  vec3 h = normalize(normalize(uSunDir) + v);
  float spec = pow(max(dot(n, h), 0.0), uGlintSize) * uGlintPower;
  spec = step(0.25, spec) * spec;
  col += uGlint * spec;

  gl_FragColor = vec4(col, uOpacity);
}
`;

// ---------------------------------------------------------------------------
/**
 * Build a water plane.
 *
 * IMPORTANT: the geometry is rotated at build time, not the mesh. That puts local
 * space in the same frame as world space (XZ flat, +Y up) so the shader maths is
 * unambiguous. Do not rotate the returned mesh.
 *
 * @param {string} presetName  one of: krebs, pascagoula, escatawpa, lanier
 * @param {number} size        plane size in world units
 * @param {number} segments    subdivisions per side. Below ~64 the waves have
 *                             nothing to move and the water goes flat.
 */
export function createWater(presetName = 'krebs', size = 300, segments = 128) {
  const cfg = WATER_PRESETS[presetName];
  if (!cfg) throw new Error(`Unknown water preset: ${presetName}`);

  const geometry = new THREE.PlaneGeometry(size, size, segments, segments);
  geometry.rotateX(-Math.PI / 2);

  const material = new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    transparent: true,
    depthWrite: true,
    side: THREE.DoubleSide,
    uniforms: {
      uTime:        { value: 0 },
      uWaveHeight:  { value: cfg.waveHeight },
      uWaveScale:   { value: cfg.waveScale },
      uWaveSpeed:   { value: cfg.waveSpeed },
      uVertexSnap:  { value: 1.0 },
      uSnapRes:     { value: new THREE.Vector2(320, 240) },
      uDeep:        { value: new THREE.Color(...cfg.deep) },
      uShallow:     { value: new THREE.Color(...cfg.shallow) },
      uSky:         { value: new THREE.Color(...cfg.sky) },
      uGlint:       { value: new THREE.Color(...cfg.glint) },
      uOpacity:     { value: cfg.opacity },
      uRippleScale: { value: cfg.rippleScale },
      uRippleSpeed: { value: cfg.rippleSpeed },
      uRippleDepth: { value: 0.30 },
      uBands:       { value: cfg.bands },
      uSunDir:      { value: new THREE.Vector3(0.45, 0.75, 0.35) },
      uGlintSize:   { value: 48.0 },
      uGlintPower:  { value: 0.85 },
      uFresnelBias: { value: 0.35 },
    },
  });

  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = `water_${presetName}`;
  return mesh;
}

/** Call once per frame. `elapsed` is seconds since start (THREE.Clock). */
export function updateWater(mesh, elapsed) {
  mesh.material.uniforms.uTime.value = elapsed;
}

/** Swap maps without rebuilding the mesh. */
export function setWaterPreset(mesh, presetName) {
  const cfg = WATER_PRESETS[presetName];
  if (!cfg) throw new Error(`Unknown water preset: ${presetName}`);
  const u = mesh.material.uniforms;
  u.uDeep.value.setRGB(...cfg.deep);
  u.uShallow.value.setRGB(...cfg.shallow);
  u.uSky.value.setRGB(...cfg.sky);
  u.uGlint.value.setRGB(...cfg.glint);
  u.uWaveHeight.value  = cfg.waveHeight;
  u.uWaveScale.value   = cfg.waveScale;
  u.uWaveSpeed.value   = cfg.waveSpeed;
  u.uRippleScale.value = cfg.rippleScale;
  u.uRippleSpeed.value = cfg.rippleSpeed;
  u.uBands.value       = cfg.bands;
  u.uOpacity.value     = cfg.opacity;
  mesh.name = `water_${presetName}`;
}
