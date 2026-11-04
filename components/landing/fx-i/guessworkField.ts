/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The word that erodes. "guesswork" is drawn from a signed-distance field
 * (public/assets/landing/guesswork/, made by scripts/landing/guesswork-sdf.mjs
 * from the page's own Source Serif 4) on a canvas laid exactly over the real
 * word in the DOM. Where the pointer touches, a damage map rises and with it
 * the field's threshold, so the glyphs thin and break up along a fibrous
 * noise edge; every cell of ink that goes leaves as a mote of orange dust,
 * a GPU particle whose whole flight is a function of its birth on the vertex
 * shader — no compute pass, so the WebGPU and WebGL 2 backends draw the same
 * thing. When most of the word is gone there is a beat, then the dust runs
 * back and the word re-forms.
 *
 * three's WebGPURenderer with TSL materials; it picks WebGL 2 by itself where
 * navigator.gpu is missing (forceWebGL makes that explicit for ?gpu=webgl).
 * Loaded lazily by GuessworkWord.tsx once the section nears the viewport.
 */

import {
  Color, DataTexture, InstancedBufferAttribute, InstancedBufferGeometry, LinearFilter, Mesh, MeshBasicNodeMaterial,
  NoColorSpace, OrthographicCamera, PlaneGeometry, RGBAFormat, Scene, Texture, UnsignedByteType, WebGPURenderer,
  type Node,
} from 'three/webgpu';
import {
  attribute, clamp, cos, float, fwidth, max, mix, mx_fractal_noise_float, positionGeometry, sin, smoothstep, step,
  texture, uniform, uv, vec2, vec3,
} from 'three/tsl';

interface Metrics {
  emPx: number; spread: number; width: number; height: number;
  originX: number; originY: number; advance: number;
  ink: { left: number; right: number; ascent: number; descent: number };
}

export interface GuessworkOptions {
  canvas: HTMLCanvasElement;
  /** The inline-block that holds the word; the canvas is positioned inside it. */
  host: HTMLElement;
  /** The real word's span (measured for width and font size). */
  text: HTMLElement;
  /** A zero-size inline-block whose offsetTop is the baseline. */
  probe: HTMLElement;
  /** The element that takes pointer events. */
  hit: HTMLElement;
  forceWebGL?: boolean;
  onReady?: (backend: 'webgpu' | 'webgl') => void;
  onTouch?: () => void;
  onPhase?: (phase: Phase) => void;
}

export type Phase = 'live' | 'beat' | 'reform';

export interface GuessworkField { destroy(): void; readonly backend: 'webgpu' | 'webgl' }

const ASSETS = '/assets/landing/guesswork/';
/** Damage-map cells across the word (the height follows the texture's aspect). */
const GW = 256;
/** Particle ring buffer. Roughly one mote per ink cell, so the whole word can leave. */
const N = 6144;
/** Most gone: the eroded share of the ink that starts the beat. */
const GONE = 0.62;
const BEAT_MS = 650;
const REFORM_MS = 1500;
const INK = '#1A1A1A';
const ORANGE = '#F26B1F';

const easeInOut = (t: number): number => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

const loadImage = (src: string): Promise<HTMLImageElement> => new Promise((resolve, reject) => {
  const img = new Image();
  img.onload = () => resolve(img);
  img.onerror = () => reject(new Error(`could not load ${src}`));
  img.src = src;
});

export async function createGuessworkField(o: GuessworkOptions): Promise<GuessworkField> {
  const [metrics, img] = await Promise.all([
    fetch(`${ASSETS}guesswork.json`).then(r => r.json() as Promise<Metrics>),
    loadImage(`${ASSETS}guesswork-sdf.png`),
  ]);
  const GH = Math.round(GW * metrics.height / metrics.width);

  // ── The field on the CPU, at damage-map resolution, so a stamp knows which ink it just removed.
  const sd = new Float32Array(GW * GH);
  {
    const c = document.createElement('canvas'); c.width = GW; c.height = GH;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    if (!ctx) throw new Error('no 2d context');
    ctx.drawImage(img, 0, 0, GW, GH);
    const px = ctx.getImageData(0, 0, GW, GH).data;
    for (let i = 0; i < GW * GH; i++) sd[i] = px[i * 4] / 255;
  }
  let inkCells = 0;
  for (let i = 0; i < GW * GH; i++) if (sd[i] > 0.5) inkCells++;

  // ── Renderer. Transparent over the white page; the DOM word underneath is painted transparent while we show.
  const renderer = new WebGPURenderer({ canvas: o.canvas, alpha: true, antialias: false, forceWebGL: !!o.forceWebGL });
  await renderer.init();
  const backend: 'webgpu' | 'webgl' = (renderer.backend as { isWebGLBackend?: boolean }).isWebGLBackend ? 'webgl' : 'webgpu';
  renderer.setClearColor(0x000000, 0);
  const scene = new Scene();
  const camera = new OrthographicCamera(0, 1, 1, 0, -10, 10);

  // ── Textures.
  const sdfTex = new Texture(img);
  sdfTex.minFilter = LinearFilter; sdfTex.magFilter = LinearFilter; sdfTex.generateMipmaps = false;
  sdfTex.colorSpace = NoColorSpace; sdfTex.needsUpdate = true;
  const dmg = new Float32Array(GW * GH);
  const dmgPixels = new Uint8Array(GW * GH * 4);
  for (let i = 0; i < GW * GH; i++) dmgPixels[i * 4 + 3] = 255;
  const dmgTex = new DataTexture(dmgPixels, GW, GH, RGBAFormat, UnsignedByteType);
  dmgTex.minFilter = LinearFilter; dmgTex.magFilter = LinearFilter; dmgTex.generateMipmaps = false;
  dmgTex.colorSpace = NoColorSpace; dmgTex.flipY = true; dmgTex.needsUpdate = true;

  const ink = new Color(INK); const orange = new Color(ORANGE);
  const uAA = uniform(0.02);
  const uEm = uniform(90);
  const uTime = uniform(0);
  const uReforming = uniform(0);
  const uReform = uniform(0);
  const uReformAt = uniform(0);

  // ── The word: the field's threshold rises with damage, along a fibrous edge; a hair of orange where it is going.
  const wordMat = new MeshBasicNodeMaterial();
  wordMat.transparent = true; wordMat.depthTest = false; wordMat.depthWrite = false; wordMat.premultipliedAlpha = true;
  {
    const u = uv();
    const s = texture(sdfTex, u).r;
    const d = texture(dmgTex, u).r;
    const fibre = mx_fractal_noise_float(vec3(u.x.mul(110), u.y.mul(26), 1.7), 3, 2.1, 0.55, 1);
    const thr = float(0.5).add(d.mul(float(0.5).add(fibre.mul(0.24))));
    const aa = max(uAA, fwidth(s).mul(0.6));
    const alpha = smoothstep(thr.sub(aa), thr.add(aa), s);
    const rim = smoothstep(thr, thr.add(0.1), s).oneMinus().mul(step(0.03, d));
    wordMat.colorNode = mix(vec3(ink.r, ink.g, ink.b), vec3(orange.r, orange.g, orange.b), rim.mul(0.9));
    wordMat.opacityNode = alpha;
  }
  const word = new Mesh(new PlaneGeometry(1, 1), wordMat);
  word.frustumCulled = false;
  scene.add(word);

  // ── The dust: one quad per mote; its flight is a function of age, so nothing is integrated.
  const origins = new Float32Array(N * 2);
  const vels = new Float32Array(N * 2);
  const borns = new Float32Array(N).fill(-1e6);
  const seeds = new Float32Array(N);
  for (let i = 0; i < N; i++) seeds[i] = Math.random();
  const geo = new InstancedBufferGeometry();
  {
    const quad = new PlaneGeometry(1, 1);
    geo.setIndex(quad.getIndex());
    geo.setAttribute('position', quad.getAttribute('position'));
    geo.setAttribute('uv', quad.getAttribute('uv'));
  }
  const aOrigin = new InstancedBufferAttribute(origins, 2);
  const aVel = new InstancedBufferAttribute(vels, 2);
  const aBorn = new InstancedBufferAttribute(borns, 1);
  const aSeed = new InstancedBufferAttribute(seeds, 1);
  geo.setAttribute('aOrigin', aOrigin); geo.setAttribute('aVel', aVel); geo.setAttribute('aBorn', aBorn); geo.setAttribute('aSeed', aSeed);
  geo.instanceCount = N;
  const dustMat = new MeshBasicNodeMaterial();
  dustMat.transparent = true; dustMat.depthTest = false; dustMat.depthWrite = false; dustMat.premultipliedAlpha = true;
  {
    const origin = attribute<'vec2'>('aOrigin', 'vec2');
    const vel = attribute<'vec2'>('aVel', 'vec2');
    const born = attribute<'float'>('aBorn', 'float');
    const seed = attribute<'float'>('aSeed', 'float');
    const life = float(1.8).add(seed.mul(1.6));
    const flight = (age: Node<'float'>) => {
      const t = clamp(age.div(life), 0, 1);
      const wob = vec2(
        sin(age.mul(2.6).add(seed.mul(37))).mul(uEm.mul(0.05)),
        cos(age.mul(1.9).add(seed.mul(19))).mul(uEm.mul(0.025)).add(age.mul(age).mul(uEm.mul(-0.02))),
      );
      return { pos: origin.add(vel.mul(age).mul(t.mul(0.45).oneMinus())).add(wob.mul(t)), t };
    };
    const live = flight(uTime.sub(born));
    // Clamped so a never-born mote's frozen branch stays finite: both branches are always evaluated (see mix below).
    const frozenAge = clamp(uReformAt.sub(born), 0, 60);
    const frozen = flight(frozenAge);
    const dead = step(life.mul(4), frozenAge); // long dead before the reform began: stays gone
    const back = smoothstep(0, 1, uReform);
    const away = origin.sub(frozen.pos);
    const arc = vec2(away.y.negate(), away.x).mul(sin(back.mul(3.14159)).mul(seed.sub(0.5)).mul(0.5));
    const reformPos = mix(frozen.pos, origin, back).add(arc);
    // mix on a 0/1 flag, not select(): on the WebGL 2 backend a select whose branch carries this much maths blanked every live mote.
    const reforming = step(0.5, uReforming);
    const pos = mix(live.pos, reformPos, reforming);
    const liveAlpha = live.t.oneMinus().mul(smoothstep(0, 0.08, live.t).oneMinus().mul(0.3).oneMinus());
    // smoothstep's edges must be in order (a reversed pair is undefined in GLSL and, through the select, blanked every live mote on the WebGL path).
    const reformAlpha = max(frozen.t.oneMinus(), 0.7).mul(dead.oneMinus()).mul(smoothstep(0.82, 1, uReform).oneMinus());
    const alpha = mix(liveAlpha, reformAlpha, reforming);
    const size = uEm.mul(float(0.03).add(seed.mul(0.028))).mul(float(1).sub(live.t.mul(0.3))).mul(step(0.001, alpha));
    dustMat.positionNode = vec3(pos.x.add(positionGeometry.x.mul(size)), pos.y.add(positionGeometry.y.mul(size)), 0.5);
    dustMat.colorNode = vec3(orange.r, orange.g, orange.b);
    dustMat.opacityNode = alpha;
  }
  const dust = new Mesh(geo, dustMat);
  dust.frustumCulled = false;
  scene.add(dust);

  // ── Layout: the canvas over the word, with room around it for the dust.
  let W = 1, H = 1;           // canvas CSS px
  let rx = 0, ry = 0, rw = 1, rh = 1; // the texture's rectangle in canvas px (y down)
  let em = 90;
  const layout = () => {
    const textRect = o.text.getBoundingClientRect();
    const hostRect = o.host.getBoundingClientRect();
    const fontPx = parseFloat(getComputedStyle(o.text).fontSize) || 90;
    em = fontPx;
    const kx = textRect.width / metrics.advance;        // the DOM word is letter-spaced; the field follows its width
    const ky = fontPx / metrics.emPx;
    const left = textRect.left - hostRect.left;
    const baseline = o.probe.offsetTop;
    const m = fontPx * 0.55;
    rw = metrics.width * kx; rh = metrics.height * ky;
    const x0 = left - metrics.originX * kx, y0 = baseline - metrics.originY * ky;
    W = Math.max(1, Math.round(rw + 2 * m)); H = Math.max(1, Math.round(rh + 2 * m));
    rx = x0 - Math.round(x0 - m); ry = y0 - Math.round(y0 - m);
    o.canvas.style.left = `${Math.round(x0 - m)}px`; o.canvas.style.top = `${Math.round(y0 - m)}px`;
    o.canvas.style.width = `${W}px`; o.canvas.style.height = `${H}px`;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(W, H, false);
    camera.right = W; camera.top = H; camera.updateProjectionMatrix();
    // World is y-up: the texture's top row sits at H - ry.
    word.position.set(rx + rw / 2, H - (ry + rh / 2), 0);
    word.scale.set(rw, rh, 1);
    uEm.value = em;
    uAA.value = 0.55 / (2 * metrics.spread * ky);
  };
  layout();
  const ro = new ResizeObserver(() => layout());
  ro.observe(o.host);

  // ── Erosion.
  const cellToWorld = (i: number, j: number): [number, number] => [
    rx + ((i + 0.5 + (Math.random() - 0.5) * 0.8) / GW) * rw,
    H - (ry + ((j + 0.5 + (Math.random() - 0.5) * 0.8) / GH) * rh),
  ];
  let head = 0;
  let clock = 0;
  const spawn = (i: number, j: number, px: number, py: number) => {
    const [x, y] = cellToWorld(i, j);
    // Away from the finger, with a lift, in em per second.
    let dx = x - px, dy = y - py; const l = Math.hypot(dx, dy) || 1; dx /= l; dy /= l;
    const speed = em * (0.25 + Math.random() * 0.45);
    const k = head; head = (head + 1) % N;
    origins[k * 2] = x; origins[k * 2 + 1] = y;
    vels[k * 2] = dx * speed + (Math.random() - 0.5) * em * 0.3;
    vels[k * 2 + 1] = dy * speed * 0.6 + em * (0.15 + Math.random() * 0.25);
    borns[k] = clock;
    dirtyParticles = true;
  };
  let dirtyParticles = false;
  let hidden = 0; // ink cells currently past the threshold
  let phase: Phase = 'live';
  let dmgAtReform: Float32Array | null = null;
  const visible = (i: number, d: number) => sd[i] > 0.5 + d * 0.5;
  /** Raise the damage under (u, v) — word-rect space — by `strength` inside a brush of radius r em. */
  const stamp = (u: number, v: number, strength: number, r: number) => {
    const cx = u * GW, cy = v * GH;
    const rxc = (r * em / rw) * GW, ryc = (r * em / rh) * GH;
    const i0 = Math.max(0, Math.floor(cx - rxc)), i1 = Math.min(GW - 1, Math.ceil(cx + rxc));
    const j0 = Math.max(0, Math.floor(cy - ryc)), j1 = Math.min(GH - 1, Math.ceil(cy + ryc));
    if (i0 > i1 || j0 > j1) return;
    const px = rx + u * rw, py = H - (ry + v * rh);
    let changed = false;
    for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) {
      const ddx = (i + 0.5 - cx) / rxc, ddy = (j + 0.5 - cy) / ryc;
      const q = ddx * ddx + ddy * ddy;
      if (q >= 1) continue;
      const fall = 1 - q * q;
      const idx = j * GW + i;
      const before = dmg[idx];
      if (before >= 1) continue;
      const after = Math.min(1, before + strength * fall);
      dmg[idx] = after;
      dmgPixels[idx * 4] = Math.round(after * 255);
      changed = true;
      if (sd[idx] > 0.5 && visible(idx, before) && !visible(idx, after)) {
        hidden++;
        spawn(i, j, px, py);
        if (Math.random() < 0.7) spawn(i, j, px, py);
      }
    }
    if (changed) dmgTex.needsUpdate = true;
  };

  // ── Pointer.
  let over = false; let lastX = 0, lastY = 0; let hasLast = false; let touched = false;
  const toUV = (e: PointerEvent): [number, number, number, number] => {
    const r = o.canvas.getBoundingClientRect();
    const x = e.clientX - r.left, y = e.clientY - r.top;
    return [(x - rx) / rw, (y - ry) / rh, x, y];
  };
  const onMove = (e: PointerEvent) => {
    if (phase !== 'live') return;
    const [u, v, x, y] = toUV(e);
    over = true;
    if (!touched) { touched = true; o.onTouch?.(); }
    const moved = hasLast ? Math.hypot(x - lastX, y - lastY) : 0;
    lastX = x; lastY = y; hasLast = true;
    const strength = Math.min(1, 0.3 + moved / (0.2 * em)) * 0.5;
    stamp(u, v, strength, e.pointerType === 'touch' ? 0.32 : 0.26);
  };
  const onLeave = () => { over = false; hasLast = false; };
  const onDown = (e: PointerEvent) => { hasLast = false; onMove(e); };
  o.hit.addEventListener('pointermove', onMove);
  o.hit.addEventListener('pointerdown', onDown);
  o.hit.addEventListener('pointerleave', onLeave);
  o.hit.addEventListener('pointercancel', onLeave);

  // ── The loop. Runs while the word is on screen; the world clock only advances while it runs.
  let raf = 0; let last = 0; let running = false; let phaseAt = 0;
  const setPhase = (p: Phase) => { phase = p; phaseAt = clock; o.host.dataset.phase = p; o.onPhase?.(p); };
  const frame = (now: number) => {
    raf = requestAnimationFrame(frame);
    const dt = Math.min(0.05, last ? (now - last) / 1000 : 0.016); last = now;
    clock += dt; uTime.value = clock;
    const eroded = inkCells ? hidden / inkCells : 0;
    o.host.dataset.eroded = eroded.toFixed(2);
    if (phase === 'live') {
      if (over && hasLast) stamp((lastX - rx) / rw, (lastY - ry) / rh, 1.6 * dt, 0.22);
      if (eroded >= GONE) setPhase('beat');
    } else if (phase === 'beat') {
      if (clock - phaseAt >= BEAT_MS / 1000) {
        dmgAtReform = Float32Array.from(dmg);
        uReformAt.value = clock; uReforming.value = 1; uReform.value = 0;
        setPhase('reform');
      }
    } else if (phase === 'reform' && dmgAtReform) {
      const t = Math.min(1, (clock - phaseAt) / (REFORM_MS / 1000));
      const e = easeInOut(t);
      uReform.value = e;
      const keep = 1 - e;
      for (let i = 0; i < GW * GH; i++) { const d = dmgAtReform[i] * keep; dmg[i] = d; dmgPixels[i * 4] = Math.round(d * 255); }
      dmgTex.needsUpdate = true;
      if (t >= 1) {
        dmg.fill(0); for (let i = 0; i < GW * GH; i++) dmgPixels[i * 4] = 0;
        dmgTex.needsUpdate = true;
        borns.fill(-1e6); dirtyParticles = true;
        hidden = 0; dmgAtReform = null; uReforming.value = 0; uReform.value = 0; hasLast = false;
        setPhase('live');
      }
    }
    if (dirtyParticles) { aOrigin.needsUpdate = true; aVel.needsUpdate = true; aBorn.needsUpdate = true; dirtyParticles = false; }
    renderer.render(scene, camera);
  };
  const start = () => { if (running) return; running = true; last = 0; raf = requestAnimationFrame(frame); };
  const stop = () => { if (!running) return; running = false; cancelAnimationFrame(raf); };
  const io = new IntersectionObserver(entries => { if (entries.some(en => en.isIntersecting)) start(); else stop(); }, { rootMargin: '80px 0px' });
  io.observe(o.host);

  // First frame before we show, so the swap from text to field is seamless.
  renderer.render(scene, camera);
  o.host.dataset.backend = backend;
  o.host.dataset.phase = 'live';
  // A window for the screenshot scripts (scratchpad pw/i-guess*.js): the live state, read-only by convention.
  (o.host as HTMLElement & { __guesswork?: unknown }).__guesswork = { borns, origins, vels, uniforms: { uTime, uEm, uReform, uReforming, uReformAt }, size: () => ({ W, H, rx, ry, rw, rh, em }), counts: () => ({ head, hidden, inkCells }), renderer, dust, word };
  o.onReady?.(backend);

  return {
    backend,
    destroy() {
      stop(); io.disconnect(); ro.disconnect();
      o.hit.removeEventListener('pointermove', onMove);
      o.hit.removeEventListener('pointerdown', onDown);
      o.hit.removeEventListener('pointerleave', onLeave);
      o.hit.removeEventListener('pointercancel', onLeave);
      geo.dispose(); word.geometry.dispose(); wordMat.dispose(); dustMat.dispose(); sdfTex.dispose(); dmgTex.dispose();
      renderer.dispose();
    },
  };
}
