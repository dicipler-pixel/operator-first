// src/render/retro.js
//
// The material every solid object in the scene uses. Ports the techniques from
// the Godot shaders in shaders/retro/ into three.js, per the "What to port"
// table in 05_WEB_STACK.md:
//
//   Vertex snapping     quantise clip space to the 320x240 grid. The wobble.
//   Affine mapping      GLSL ES has no `noperspective`, so multiply UV by
//                       view-space depth in the vertex shader and divide it
//                       back out in the fragment shader. That is the PS1 swim.
//   Vertex lighting     Gouraud, computed per-vertex, passed as a varying.
//                       Never per-fragment.
//   Distance fog        tinted to the sky colour, set tight.
//
// One directional light plus ambient, both passed as uniforms rather than read
// from three's light system — a ShaderMaterial does not participate in that,
// and hand-rolling it keeps the whole lighting model visible in one file.

import * as THREE from 'three';

export const SNAP_RES = new THREE.Vector2(320, 240);

const vertexShader = /* glsl */ `
uniform float uVertexSnap;
uniform vec2  uSnapRes;
uniform vec3  uSunDir;
uniform vec3  uSunColor;
uniform vec3  uAmbient;
uniform float uFill;
uniform float uAffine;
uniform vec3  uTint;

attribute vec3 color;

varying vec3  vLit;
varying vec2  vUvAffine;
varying float vDepth;
varying float vFogDepth;

void main() {
  vec4 mv = modelViewMatrix * vec4(position, 1.0);

  // Gouraud. Half-lambert so the shadowed side stays readable instead of
  // going flat black, which is what the era actually shipped.
  vec3 n = normalize(normalMatrix * normal);
  vec3 l = normalize((viewMatrix * vec4(uSunDir, 0.0)).xyz);
  float ndl = dot(n, l) * 0.5 + 0.5;
  // Camera-side fill. A flat cheat, and exactly the kind of cheat the era used
  // to stop backlit characters going to solid black.
  float fill = uFill * max(0.0, dot(n, vec3(0.0, 0.25, 1.0)));
  vLit = (uAmbient + uSunColor * ndl + vec3(fill)) * color * uTint;

  vFogDepth = -mv.z;

  // Affine texture mapping: carry UV scaled by depth, undo it per fragment.
  vDepth = uAffine > 0.5 ? -mv.z : 1.0;
  vUvAffine = uv * vDepth;

  vec4 clip = projectionMatrix * mv;

  if (uVertexSnap > 0.5) {
    vec3 ndc = clip.xyz / clip.w;
    ndc.xy = floor(ndc.xy * uSnapRes) / uSnapRes;
    clip = vec4(ndc * clip.w, clip.w);
  }

  gl_Position = clip;
}
`;

const fragmentShader = /* glsl */ `
uniform sampler2D uMap;
uniform float uHasMap;
uniform vec3  uFogColor;
uniform float uFogNear;
uniform float uFogFar;
uniform float uAlpha;
uniform float uAlphaTest;

varying vec3  vLit;
varying vec2  vUvAffine;
varying float vDepth;
varying float vFogDepth;

void main() {
  vec4 tex = vec4(1.0);
  if (uHasMap > 0.5) {
    tex = texture2D(uMap, vUvAffine / vDepth);
    if (tex.a < uAlphaTest) discard;
  }

  vec3 col = vLit * tex.rgb;

  float f = clamp((vFogDepth - uFogNear) / (uFogFar - uFogNear), 0.0, 1.0);
  col = mix(col, uFogColor, f);

  gl_FragColor = vec4(col, uAlpha * tex.a);
}
`;

/**
 * @param {object} [opts]
 * @param {THREE.Color|number} [opts.tint=0xffffff]  flat multiply over vertex colour
 * @param {THREE.Texture} [opts.map]
 * @param {boolean} [opts.affine=true]
 * @param {boolean} [opts.snap=true]
 * @param {number}  [opts.alpha=1]
 * @param {boolean} [opts.transparent=false]
 * @param {boolean} [opts.doubleSide=false]
 */
export function createRetroMaterial(opts = {}) {
  const m = new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    transparent: !!opts.transparent,
    side: opts.doubleSide ? THREE.DoubleSide : THREE.FrontSide,
    depthWrite: opts.depthWrite !== false,
    uniforms: {
      uVertexSnap: { value: opts.snap === false ? 0 : 1 },
      uSnapRes: { value: SNAP_RES.clone() },
      uSunDir: { value: new THREE.Vector3(0.45, 0.75, 0.35).normalize() },
      uSunColor: { value: new THREE.Color(0.85, 0.72, 0.52) },
      uAmbient: { value: new THREE.Color(0.34, 0.32, 0.34) },
      uFill: { value: opts.fillFromCamera ?? 0 },
      uAffine: { value: opts.affine === false ? 0 : 1 },
      uTint: { value: new THREE.Color(opts.tint ?? 0xffffff) },
      uMap: { value: opts.map ?? null },
      uHasMap: { value: opts.map ? 1 : 0 },
      uFogColor: { value: new THREE.Color(0x000000) },
      uFogNear: { value: 18 },
      uFogFar: { value: 150 },
      uAlpha: { value: opts.alpha ?? 1 },
      uAlphaTest: { value: opts.alphaTest ?? 0.5 },
    },
  });
  m.userData.isRetro = true;
  // Evening light comes from behind the far bank, which leaves anything near
  // the camera in silhouette. A per-material fill lets Nana read against dark
  // water — her pale overshirt is the second-biggest recognition cue after the
  // hair, and it has to actually be visible to do that job.
  m.userData.ambientBoost = opts.ambientBoost ?? 1;
  m.userData.fillFromCamera = opts.fillFromCamera ?? 0;
  return m;
}

/** Push the scene's light and fog settings into every retro material under root. */
export function syncRetroLighting(root, { sun, sunColor, ambient, fogColor, fogNear, fogFar }) {
  root.traverse((o) => {
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of mats) {
      if (!m?.userData?.isRetro) continue;
      const u = m.uniforms;
      if (sun) u.uSunDir.value.copy(sun);
      if (sunColor) u.uSunColor.value.copy(sunColor);
      if (m.userData.fillFromCamera) u.uFill.value = m.userData.fillFromCamera;
      if (ambient) u.uAmbient.value.copy(ambient).multiplyScalar(m.userData.ambientBoost ?? 1);
      if (fogColor) u.uFogColor.value.copy(fogColor);
      if (fogNear !== undefined) u.uFogNear.value = fogNear;
      if (fogFar !== undefined) u.uFogFar.value = fogFar;
    }
  });
}

/**
 * Paint a geometry with a flat vertex colour. Every retro material reads the
 * `color` attribute, so nothing may reach the shader without one.
 */
export function paint(geometry, color) {
  const c = new THREE.Color(color);
  const n = geometry.attributes.position.count;
  const arr = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { arr[i * 3] = c.r; arr[i * 3 + 1] = c.g; arr[i * 3 + 2] = c.b; }
  geometry.setAttribute('color', new THREE.BufferAttribute(arr, 3));
  return geometry;
}

/** Flat vertex colour, but darker towards -Y. Cheap fake AO for ground clutter. */
export function paintShaded(geometry, color, { top = 1.0, bottom = 0.55 } = {}) {
  const c = new THREE.Color(color);
  const pos = geometry.attributes.position;
  const n = pos.count;
  let lo = Infinity, hi = -Infinity;
  for (let i = 0; i < n; i++) { const y = pos.getY(i); if (y < lo) lo = y; if (y > hi) hi = y; }
  const span = Math.max(1e-5, hi - lo);
  const arr = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const t = (pos.getY(i) - lo) / span;
    const k = bottom + (top - bottom) * t;
    arr[i * 3] = c.r * k; arr[i * 3 + 1] = c.g * k; arr[i * 3 + 2] = c.b * k;
  }
  geometry.setAttribute('color', new THREE.BufferAttribute(arr, 3));
  return geometry;
}
