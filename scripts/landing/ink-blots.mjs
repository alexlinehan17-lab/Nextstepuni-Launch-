/**
 * Three ink blots as 512 px alpha PNGs, for the landing page's CSS-mask
 * reveals (components/landing/fx/fx.css, .fx-blot). Drawn procedurally: a
 * metaball body with a few satellite drops, its outline pushed around by two
 * octaves of simplex noise so the edge is irregular, and a feathered,
 * fibrous alpha edge so the ink looks soaked into paper rather than cut out.
 *
 *   node scripts/landing/ink-blots.mjs
 *
 * Writes public/assets/landing/fx/blot-{1,2,3}.png. The core is sized so that
 * at mask-size 280% the opaque body covers a 16:10 frame corner to corner.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { prng, simplex, encodePNG, smoothstep } from './lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT = path.join(ROOT, 'public', 'assets', 'landing', 'fx');
const SIZE = 512;

const blot = (seed) => {
  const rand = prng(seed * 7919 + 17);
  const nA = simplex(rand), nB = simplex(rand), nC = simplex(rand), nD = simplex(rand);
  // Metaballs in a −1…1 square: the body, then drops that ran off it.
  const balls = [{ x: 0, y: 0, r: 0.52 }];
  const drops = 3 + Math.floor(rand() * 3);
  for (let i = 0; i < drops; i++) {
    const a = rand() * Math.PI * 2, d = 0.42 + rand() * 0.24;
    balls.push({ x: Math.cos(a) * d, y: Math.sin(a) * d, r: 0.07 + rand() * 0.09 });
  }
  const specks = 2 + Math.floor(rand() * 3);
  for (let i = 0; i < specks; i++) {
    const a = rand() * Math.PI * 2, d = 0.62 + rand() * 0.2;
    balls.push({ x: Math.cos(a) * d, y: Math.sin(a) * d, r: 0.025 + rand() * 0.025 });
  }
  const px = new Uint8Array(SIZE * SIZE * 4);
  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const u = (x - SIZE / 2) / (SIZE / 2), v = (y - SIZE / 2) / (SIZE / 2);
      // Warp the sample point so the outline wanders.
      const qx = u + 0.11 * nA(u * 2.1, v * 2.1) + 0.035 * nB(u * 6.5, v * 6.5);
      const qy = v + 0.11 * nA(u * 2.1 + 9.3, v * 2.1 + 4.1) + 0.035 * nB(u * 6.5 + 3.7, v * 6.5 + 8.2);
      let field = 0;
      for (const b of balls) {
        const dx = qx - b.x, dy = qy - b.y;
        field += (b.r * b.r) / (dx * dx + dy * dy + 1e-6);
      }
      // Feathered edge whose width breathes with fine noise: ink wicking into fibres.
      const feather = 0.14 + 0.1 * nC(u * 15, v * 15);
      let a = smoothstep(1 - feather, 1 + feather, field);
      // A fibrous fringe just outside the edge.
      const fringe = Math.max(0, nD(u * 34, v * 34) - 0.25) * smoothstep(0.72, 1, field) * (1 - a) * 0.55;
      a = Math.min(1, a + fringe);
      const i = (y * SIZE + x) * 4;
      px[i] = 0; px[i + 1] = 0; px[i + 2] = 0; px[i + 3] = Math.round(a * 255);
    }
  }
  return encodePNG(SIZE, SIZE, px);
};

fs.mkdirSync(OUT, { recursive: true });
for (const n of [1, 2, 3]) {
  const file = path.join(OUT, `blot-${n}.png`);
  const buf = blot(n);
  fs.writeFileSync(file, buf);
  console.log(`${path.relative(ROOT, file)}  ${(buf.length / 1024).toFixed(1)} kB`);
}
