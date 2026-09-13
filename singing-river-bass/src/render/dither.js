// src/render/dither.js
//
// The fullscreen upscale pass. Two jobs, one draw call:
//   1. Blow the 320x240 render target up to the screen, NEAREST, letterboxed.
//   2. Ordered (Bayer) dither and quantise to 15-bit colour.
//
// The dither matrix is indexed off the LOW-RES pixel grid, not gl_FragCoord.
// That matters: index it off the screen grid and you get a fine 1-screen-pixel
// crosshatch that nobody in 1997 ever saw. Indexed off the 320x240 grid it
// upscales along with the image, which is what a real framebuffer did.

// The quad is a PlaneGeometry(2,2) on an ortho camera spanning -1..1, so its
// mesh scale is what letterboxes the picture. Go through the matrices rather
// than writing position straight into clip space, or the scale is ignored and
// the image stretches to fill the screen at the wrong aspect.
export const UPSCALE_VERTEX = /* glsl */ `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

export const UPSCALE_FRAGMENT = /* glsl */ `
uniform sampler2D tDiffuse;
uniform vec2  uRes;      // 320x240
uniform float uLevels;   // 32 -> 5 bits per channel -> 15-bit colour
uniform float uDither;   // 0 = off, 1 = on

varying vec2 vUv;

// 4x4 ordered Bayer, values 0..15 scaled to 0..1.
float bayer4(vec2 p) {
  int x = int(mod(p.x, 4.0));
  int y = int(mod(p.y, 4.0));
  int i = y * 4 + x;
  float v = 0.0;
  if      (i ==  0) v =  0.0; else if (i ==  1) v =  8.0;
  else if (i ==  2) v =  2.0; else if (i ==  3) v = 10.0;
  else if (i ==  4) v = 12.0; else if (i ==  5) v =  4.0;
  else if (i ==  6) v = 14.0; else if (i ==  7) v =  6.0;
  else if (i ==  8) v =  3.0; else if (i ==  9) v = 11.0;
  else if (i == 10) v =  1.0; else if (i == 11) v =  9.0;
  else if (i == 12) v = 15.0; else if (i == 13) v =  7.0;
  else if (i == 14) v = 13.0; else v =  5.0;
  return v / 16.0;
}

void main() {
  vec3 c = texture2D(tDiffuse, vUv).rgb;

  float b = uDither > 0.5 ? bayer4(floor(vUv * uRes)) : 0.5;
  float n = uLevels - 1.0;
  vec3 q = floor(c * n + b) / n;

  gl_FragColor = vec4(clamp(q, 0.0, 1.0), 1.0);
}
`;
