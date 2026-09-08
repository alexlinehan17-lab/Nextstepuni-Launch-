/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The ink bleed. A WebGL2 canvas the size of the viewport holds the scene
 * of the chapter being read and the scene of the next one as textures; a
 * fragment shader shows the next wherever a paper-fibre field falls under a
 * threshold the scroll position moves, so the new scene soaks up the sheet
 * as the reader goes — a 1-bit edge, fingers and islands, a tide line where
 * the ink gathered — never a crossfade. The scenes are attached to the
 * page (they scroll with the copy); the front is fixed to the window.
 *
 * Renders only when asked (scroll, resize), one triangle, three texture
 * reads a pixel. The scene tiles are rasterised from their SVGs at CSS
 * resolution once per width, one per idle callback, so a scroll never waits
 * on a rasterise.
 */

import { NOISE_SIZE, noisePixels } from './noise';
import { SCENE_IDS, TILE, sceneUrl } from './layout';

const VERT = `#version 300 es
out vec2 vUv;
void main() {
  vec2 p = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));
  vUv = p;
  gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0);
}`;

const FRAG = `#version 300 es
precision highp float;
in vec2 vUv;
uniform sampler2D uA;
uniform sampler2D uB;
uniform sampler2D uNoise;
uniform vec4 uMap;
uniform vec2 uRes;
uniform float uP;
uniform float uK;
uniform vec2 uSeed;
out vec4 outColor;
void main() {
  vec2 suv = vUv * uMap.xy + uMap.zw;
  vec3 a = texture(uA, suv).rgb;
  vec3 b = texture(uB, suv).rgb;
  // The fibre, in CSS px so it is the same paper on every screen.
  vec2 px = vUv * uRes;
  float n1 = texture(uNoise, px / 1500.0 + uSeed).r;
  float n2 = texture(uNoise, px / 520.0 + uSeed.yx * 1.7).g;
  float n3 = texture(uNoise, px / 380.0 + uSeed * 3.1).b;
  float n4 = texture(uNoise, px / 128.0 + uSeed * 5.3).a;
  float n = 0.52 * n1 + 0.27 * n2 + 0.17 * n3 + 0.04 * n4;
  // The front rises from the foot of the window; the fibre decides how far it has got at each point.
  float f = mix(vUv.y, n, uK);
  // A fixed width in field units, about a pixel and a half at the front: the edge is a line, not a fade.
  float w = 0.0012;
  float m = 1.0 - smoothstep(uP - w, uP + w, f);
  // The tide line: ink gathers along the edge of a bleed.
  float rim = 1.0 - smoothstep(0.0, w * 2.5, abs(f - uP));
  vec3 col = mix(a, b, m) * (1.0 - 0.07 * rim);
  outColor = vec4(col, 1.0);
}`;

/** How much of the front is fibre rather than a flat rising line. */
const FIBRE = 0.32;

export interface BleedFrame {
  /** Page px of the canvas's top edge. */
  pageTop: number;
  /** Scene indices; −1 is blank paper. */
  a: number;
  b: number;
  /** 0–1: how far `b` has soaked in. */
  p: number;
  seed: number;
}

export class Bleed {
  readonly ok: boolean;
  /** Called whenever a scene tile becomes ready, so the owner can redraw. */
  onReady: () => void = () => undefined;

  private gl: WebGL2RenderingContext | null = null;
  private prog: WebGLProgram | null = null;
  private loc: Record<string, WebGLUniformLocation | null> = {};
  private tex: (WebGLTexture | null)[] = SCENE_IDS.map(() => null);
  private imgs: (HTMLImageElement | null)[] = SCENE_IDS.map(() => null);
  private white: WebGLTexture | null = null;
  private noise: WebGLTexture | null = null;
  private scratch: HTMLCanvasElement | null = null;
  private w = 0;
  private h = 0;
  private dpr = 1;
  /** The tile's size in CSS px: design scale, or scaled up to span a wider window. */
  private tileW: number = TILE.w;
  private tileH: number = TILE.h;
  private queue: number[] = [];
  private idle = 0;
  private last: BleedFrame | null = null;
  private lastSize = '';

  constructor(private canvas: HTMLCanvasElement) {
    const gl = ((): WebGL2RenderingContext | null => {
      try {
        return canvas.getContext('webgl2', { alpha: false, antialias: false, depth: false, stencil: false, premultipliedAlpha: false, powerPreference: 'low-power' });
      } catch {
        return null;
      }
    })();
    this.ok = !!gl && this.setup(gl);
    if (this.ok) {
      this.gl = gl;
      SCENE_IDS.forEach((_, i) => {
        const img = new Image();
        img.decoding = 'async';
        img.onload = () => { this.imgs[i] = img; this.enqueue(i); };
        img.src = sceneUrl(i);
      });
    }
  }

  private setup(gl: WebGL2RenderingContext): boolean {
    const compile = (type: number, src: string): WebGLShader | null => {
      const s = gl.createShader(type);
      if (!s) return null;
      gl.shaderSource(s, src);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { console.error('[scenes] shader', gl.getShaderInfoLog(s)); return null; }
      return s;
    };
    const vs = compile(gl.VERTEX_SHADER, VERT), fs = compile(gl.FRAGMENT_SHADER, FRAG);
    const prog = gl.createProgram();
    if (!vs || !fs || !prog) return false;
    gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { console.error('[scenes] link', gl.getProgramInfoLog(prog)); return false; }
    gl.useProgram(prog);
    for (const name of ['uA', 'uB', 'uNoise', 'uMap', 'uRes', 'uP', 'uK', 'uSeed']) this.loc[name] = gl.getUniformLocation(prog, name);
    gl.uniform1i(this.loc.uA, 0); gl.uniform1i(this.loc.uB, 1); gl.uniform1i(this.loc.uNoise, 2);
    gl.uniform1f(this.loc.uK, FIBRE);
    // A vertex array must be bound to draw in WebGL2, even with no attributes.
    gl.bindVertexArray(gl.createVertexArray());
    this.prog = prog;

    this.white = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, this.white);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([255, 255, 255, 255]));
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);

    this.noise = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, this.noise);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, NOISE_SIZE, NOISE_SIZE, 0, gl.RGBA, gl.UNSIGNED_BYTE, noisePixels());
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    return true;
  }

  /** The canvas's CSS size and pixel ratio. Re-rasterises the tiles when the width changes. */
  resize(w: number, h: number, dpr: number): void {
    if (!this.gl || w === 0 || h === 0) return;
    this.w = w; this.h = h; this.dpr = dpr;
    this.canvas.width = Math.round(w * dpr);
    this.canvas.height = Math.round(h * dpr);
    this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    // Never below design scale: a narrower window sees the middle of the tile, not a shrunken one.
    const s = Math.max(1, w / TILE.w);
    const tileW = Math.round(TILE.w * s), tileH = Math.round(TILE.h * s);
    if (tileW !== this.tileW || this.lastSize === '') {
      this.tileW = tileW; this.tileH = tileH;
      this.queue = [];
      this.imgs.forEach((img, i) => { if (img) this.enqueue(i); });
    }
    this.lastSize = `${w}x${h}`;
    this.last = null;
  }

  private enqueue(i: number): void {
    if (!this.queue.includes(i)) this.queue.push(i);
    if (this.idle) return;
    const run = (): void => {
      this.idle = 0;
      const next = this.queue.shift();
      if (next === undefined) return;
      this.rasterise(next);
      this.onReady();
      if (this.queue.length) this.idle = schedule(run);
    };
    const schedule = (fn: () => void): number =>
      typeof requestIdleCallback === 'function' ? requestIdleCallback(fn, { timeout: 400 }) : window.setTimeout(fn, 16);
    this.idle = schedule(run);
  }

  /** Draw one scene's SVG into a tile at the current width and upload it. */
  private rasterise(i: number): void {
    const gl = this.gl, img = this.imgs[i];
    if (!gl || !img) return;
    const scratch = this.scratch ?? (this.scratch = document.createElement('canvas'));
    scratch.width = this.tileW; scratch.height = this.tileH;
    const ctx = scratch.getContext('2d');
    if (!ctx) return;
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, this.tileW, this.tileH);
    ctx.drawImage(img, 0, 0, this.tileW, this.tileH);
    const tex = this.tex[i] ?? (this.tex[i] = gl.createTexture());
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.pixelStorei(gl.UNPACK_COLORSPACE_CONVERSION_WEBGL, gl.NONE);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, scratch);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    // Down the page the tile repeats.
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    this.last = null;
  }

  /** True once the scene tiles needed for this frame have been rasterised. */
  ready(frame: BleedFrame): boolean {
    return (frame.a < 0 || !!this.tex[frame.a]) && (frame.b < 0 || !!this.tex[frame.b]);
  }

  render(frame: BleedFrame): void {
    const gl = this.gl;
    if (!gl || !this.prog || this.w === 0) return;
    const l = this.last;
    if (l && l.pageTop === frame.pageTop && l.a === frame.a && l.b === frame.b && l.p === frame.p && l.seed === frame.seed) return;
    this.last = { ...frame };
    const at = frame.a < 0 ? this.white : this.tex[frame.a] ?? this.white;
    const bt = frame.b < 0 ? this.white : this.tex[frame.b] ?? this.white;
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, at);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, bt);
    gl.activeTexture(gl.TEXTURE2); gl.bindTexture(gl.TEXTURE_2D, this.noise);
    // Scene uv from canvas uv: the middle of the tile across, the page's own y down (v grows downwards; uv.y grows upwards).
    const { w, h, tileW, tileH } = this;
    gl.uniform4f(this.loc.uMap, w / tileW, -h / tileH, 0.5 - w / (2 * tileW), (frame.pageTop + h) / tileH);
    gl.uniform2f(this.loc.uRes, w, h);
    // A little past both ends, so the front starts below the window and finishes above it.
    const p = frame.a === frame.b ? -0.2 : frame.p * 1.06 - 0.03;
    gl.uniform1f(this.loc.uP, p);
    gl.uniform2f(this.loc.uSeed, (frame.seed * 0.37) % 1, (frame.seed * 0.61) % 1);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }

  destroy(): void {
    if (this.idle) {
      if (typeof cancelIdleCallback === 'function') cancelIdleCallback(this.idle); else window.clearTimeout(this.idle);
    }
    const gl = this.gl;
    if (gl) {
      this.tex.forEach(t => { if (t) gl.deleteTexture(t); });
      if (this.white) gl.deleteTexture(this.white);
      if (this.noise) gl.deleteTexture(this.noise);
      if (this.prog) gl.deleteProgram(this.prog);
      gl.getExtension('WEBGL_lose_context')?.loseContext();
    }
    this.gl = null;
  }
}
