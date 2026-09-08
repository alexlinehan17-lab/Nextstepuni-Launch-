/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper fibre for the ink bleed: one tileable 256 × 256 RGBA texture, a
 * different noise in each channel — R the large blots that decide where the
 * front has reached, G a middle octave, B fibres laid along the sheet, A
 * grain. Gradient noise on a periodic lattice, so the texture wraps without
 * a seam and the shader can sample it at any scale. Deterministic.
 */

export const NOISE_SIZE = 256;

/** mulberry32. */
const prng = (seed: number): (() => number) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/** 2-D gradient noise on a lattice that repeats every px × py cells. */
const periodic = (rand: () => number, px: number, py: number): ((x: number, y: number) => number) => {
  const g = new Float32Array(px * py * 2);
  for (let i = 0; i < px * py; i++) { const a = rand() * Math.PI * 2; g[i * 2] = Math.cos(a); g[i * 2 + 1] = Math.sin(a); }
  const fade = (t: number): number => t * t * t * (t * (t * 6 - 15) + 10);
  const dot = (ix: number, iy: number, x: number, y: number): number => {
    const i = (((iy % py) + py) % py) * px + (((ix % px) + px) % px);
    return g[i * 2] * x + g[i * 2 + 1] * y;
  };
  return (x, y) => {
    const ix = Math.floor(x), iy = Math.floor(y), fx = x - ix, fy = y - iy;
    const u = fade(fx), v = fade(fy);
    const a = dot(ix, iy, fx, fy), b = dot(ix + 1, iy, fx - 1, fy);
    const c = dot(ix, iy + 1, fx, fy - 1), d = dot(ix + 1, iy + 1, fx - 1, fy - 1);
    const top = a + (b - a) * u, bottom = c + (d - c) * u;
    return top + (bottom - top) * v;
  };
};

type Octave = [px: number, py: number, amplitude: number];

/** The four channels' octaves: cells across the tile in x and y, and weight. */
const CHANNELS: Octave[][] = [
  [[4, 4, 1], [8, 8, 0.5], [16, 16, 0.25]],
  [[10, 10, 1], [20, 20, 0.5], [40, 40, 0.25]],
  // Long in x, short in y: fibres laid along the sheet.
  [[5, 40, 1], [10, 80, 0.45]],
  [[64, 64, 1]],
];

/** RGBA8 pixels, each channel stretched to the full 0–255. */
export function noisePixels(): Uint8Array {
  const rand = prng(1131);
  const N = NOISE_SIZE;
  const out = new Uint8Array(N * N * 4);
  const vals = new Float32Array(N * N);
  CHANNELS.forEach((octaves, c) => {
    const fns = octaves.map(([px, py, a]) => ({ n: periodic(rand, px, py), px, py, a }));
    let lo = Infinity, hi = -Infinity;
    for (let y = 0; y < N; y++) {
      for (let x = 0; x < N; x++) {
        let v = 0;
        for (const o of fns) v += o.a * o.n((x / N) * o.px, (y / N) * o.py);
        vals[y * N + x] = v;
        if (v < lo) lo = v;
        if (v > hi) hi = v;
      }
    }
    const scale = 255 / (hi - lo || 1);
    for (let i = 0; i < N * N; i++) out[i * 4 + c] = Math.round((vals[i] - lo) * scale);
  });
  return out;
}
