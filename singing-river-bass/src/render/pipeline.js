// src/render/pipeline.js
//
// The whole trick, per 05_WEB_STACK.md: render SMALL and blow it up. Never
// render at screen resolution and filter down.
//
//   scene -> WebGLRenderTarget(320x240, NearestFilter, no mipmaps)
//         -> fullscreen quad on an ortho camera, letterboxed, NEAREST again
//         -> dither/posterise runs on the QUAD, not on the scene
//
// Two constraints from the handoff are enforced here and must not be "fixed":
//   - renderer.setPixelRatio(1). Never window.devicePixelRatio. A phone at DPR 3
//     otherwise renders nine times the pixels for a game that wants 320x240.
//   - 30fps via a delta accumulator. Not raw requestAnimationFrame. 60fps breaks
//     the spell and doubles battery drain.

import * as THREE from 'three';
import { UPSCALE_VERTEX, UPSCALE_FRAGMENT } from './dither.js';

export const RENDER_WIDTH = 320;
export const RENDER_HEIGHT = 240;
export const TARGET_FPS = 30;

const FRAME_STEP = 1 / TARGET_FPS;

export class RetroPipeline {
  /**
   * @param {HTMLCanvasElement} canvas
   * @param {object} [opts]
   * @param {boolean} [opts.dither=true]
   * @param {number}  [opts.levels=32]  colour levels per channel; 32 = 15-bit
   */
  constructor(canvas, opts = {}) {
    this.canvas = canvas;
    this.width = RENDER_WIDTH;
    this.height = RENDER_HEIGHT;

    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: false,          // 1997 had no AA and we do not want any
      alpha: false,
      powerPreference: 'low-power',
    });
    this.renderer.setPixelRatio(1);   // NOT window.devicePixelRatio. See above.
    this.renderer.autoClear = true;

    // Two render() calls per frame. Left on auto, info.render would reset at
    // the start of each and only ever report the upscale quad's 2 triangles,
    // which makes the 8,000-triangle scene budget unmeasurable. Reset by hand,
    // once, so the counts cover scene + quad together.
    this.renderer.info.autoReset = false;

    // --- the 320x240 framebuffer -----------------------------------------
    this.target = new THREE.WebGLRenderTarget(this.width, this.height, {
      minFilter: THREE.NearestFilter,
      magFilter: THREE.NearestFilter,
      generateMipmaps: false,
      depthBuffer: true,
      stencilBuffer: false,
      type: THREE.UnsignedByteType,
    });
    this.target.texture.generateMipmaps = false;
    this.target.texture.wrapS = THREE.ClampToEdgeWrapping;
    this.target.texture.wrapT = THREE.ClampToEdgeWrapping;

    // --- the upscale quad -------------------------------------------------
    // Clip-space triangle pair; the vertex shader passes position straight
    // through, so the quad is scaled by adjusting geometry, not the camera.
    this.quadScene = new THREE.Scene();
    this.quadCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    this.quadMaterial = new THREE.ShaderMaterial({
      vertexShader: UPSCALE_VERTEX,
      fragmentShader: UPSCALE_FRAGMENT,
      depthTest: false,
      depthWrite: false,
      uniforms: {
        tDiffuse: { value: this.target.texture },
        uRes: { value: new THREE.Vector2(this.width, this.height) },
        uLevels: { value: opts.levels ?? 32 },
        uDither: { value: opts.dither === false ? 0 : 1 },
      },
    });
    this.quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), this.quadMaterial);
    this.quad.frustumCulled = false;
    this.quadScene.add(this.quad);

    // --- frame clock ------------------------------------------------------
    this.accumulator = 0;
    this.elapsed = 0;
    this.lastTime = 0;
    this.running = false;
    this._rafId = 0;

    // Measured, not assumed. Counts real presented frames per second.
    this.stats = { fps: 0, frames: 0, rafPerSecond: 0, longestFrameMs: 0 };
    this._fpsWindowStart = 0;
    this._framesInWindow = 0;
    this._rafInWindow = 0;

    this.resize();
  }

  /** Fit 4:3 inside the viewport, letterboxed, with the canvas at CSS size. */
  resize() {
    const vw = Math.max(1, Math.floor(this.canvas.clientWidth || window.innerWidth));
    const vh = Math.max(1, Math.floor(this.canvas.clientHeight || window.innerHeight));

    this.renderer.setSize(vw, vh, false);

    const scale = Math.min(vw / this.width, vh / this.height);
    const drawW = this.width * scale;
    const drawH = this.height * scale;

    this.quad.scale.set(drawW / vw, drawH / vh, 1);
    this.viewport = { vw, vh, drawW, drawH, scale };
  }

  /**
   * Map a client-space point (a tap) onto the 320x240 framebuffer.
   * Returns null when the tap lands in the letterbox bars.
   */
  clientToRenderPixel(clientX, clientY) {
    const rect = this.canvas.getBoundingClientRect();
    const { drawW, drawH } = this.viewport;
    const ox = (rect.width - drawW) / 2;
    const oy = (rect.height - drawH) / 2;
    const x = (clientX - rect.left - ox) / drawW;
    const y = (clientY - rect.top - oy) / drawH;
    if (x < 0 || x > 1 || y < 0 || y > 1) return null;
    return { x: x * this.width, y: y * this.height, u: x, v: 1 - y };
  }

  /** One composite: scene into the small target, then the target onto the screen. */
  render(scene, camera) {
    this.renderer.info.reset();

    this.renderer.setRenderTarget(this.target);
    this.renderer.clear();
    this.renderer.render(scene, camera);

    this.renderer.setRenderTarget(null);
    this.renderer.clear();
    this.renderer.render(this.quadScene, this.quadCamera);
  }

  /**
   * Start the 30fps loop.
   * @param {(dt:number, elapsed:number)=>void} onFrame called once per LOCKED
   *        frame with a fixed dt of exactly 1/30. Draw inside it.
   */
  start(onFrame) {
    this.running = true;
    this.lastTime = performance.now() / 1000;
    this._fpsWindowStart = this.lastTime;

    const tick = () => {
      if (!this.running) return;
      this._rafId = requestAnimationFrame(tick);

      const now = performance.now() / 1000;
      let dt = now - this.lastTime;
      this.lastTime = now;
      this._rafInWindow++;

      // A backgrounded tab returns a huge dt. Clamp it or the accumulator
      // tries to catch up with a burst of frames and the water jumps.
      if (dt > 0.25) dt = 0.25;
      this.accumulator += dt;

      if (this.accumulator >= FRAME_STEP) {
        // Drop surplus rather than spiral. We are locking a ceiling, not
        // guaranteeing a fixed-step simulation.
        this.accumulator = this.accumulator % FRAME_STEP;

        const t0 = performance.now();
        this.elapsed += FRAME_STEP;
        onFrame(FRAME_STEP, this.elapsed);
        const frameMs = performance.now() - t0;

        this.stats.frames++;
        this._framesInWindow++;
        if (frameMs > this.stats.longestFrameMs) this.stats.longestFrameMs = frameMs;
      }

      const windowLen = now - this._fpsWindowStart;
      if (windowLen >= 1) {
        this.stats.fps = this._framesInWindow / windowLen;
        this.stats.rafPerSecond = this._rafInWindow / windowLen;
        this._framesInWindow = 0;
        this._rafInWindow = 0;
        this._fpsWindowStart = now;
      }
    };

    this._rafId = requestAnimationFrame(tick);
  }

  stop() {
    this.running = false;
    cancelAnimationFrame(this._rafId);
  }

  dispose() {
    this.stop();
    this.target.dispose();
    this.quad.geometry.dispose();
    this.quadMaterial.dispose();
    this.renderer.dispose();
  }
}
