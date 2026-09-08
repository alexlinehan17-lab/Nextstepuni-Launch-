/**
 * Flow-field pen hatching, one SVG per chapter, for the ornament behind each
 * chapter heading on the landing page (components/landing/fx/Field.tsx).
 *
 * A seeded simplex field (seed = the chapter number) steers 250–400 evenly
 * spaced streamlines of 20–60 short steps; each is a 0.5 px ink stroke at
 * 12–18 % alpha. Runtime is plain SVG: the strokes are inked in by CSS
 * (stroke-dashoffset on a view() timeline), so every path carries
 * pathLength="1". Coordinates are integers with relative moves to keep each
 * file near 10 kB gzipped; the rounding adds a pen's wobble.
 *
 *   node scripts/landing/flow-fields.mjs
 *
 * Writes components/landing/fx/fields/field-{1..6}.svg.
 */

import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { prng, simplex } from './lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT = path.join(ROOT, 'components', 'landing', 'fx', 'fields');

const W = 1200, H = 420;
const CELL = 6;              // occupancy grid: keeps streamlines a pen-width apart
const STEP = 3.2;            // px per integration step
const TARGET = 320;          // streamlines wanted per field
const MIN_STEPS = 20, MAX_STEPS = 60;
const ALPHAS = ['.12', '.15', '.18'];

const field = (n) => {
  const rand = prng(n * 104729 + 3);
  const noise = simplex(rand);
  const fine = simplex(rand);
  // Each chapter flows a little differently: a base heading and how much the field bends.
  const base = (rand() - 0.5) * 0.9;
  const bend = 1.1 + rand() * 0.7;
  const scale = 0.0022 + rand() * 0.0012;
  const angle = (x, y) => base + bend * noise(x * scale, y * scale) + 0.35 * fine(x * scale * 4.3, y * scale * 4.3);

  const cols = Math.ceil(W / CELL) + 1, rows = Math.ceil(H / CELL) + 1;
  const busy = new Uint8Array(cols * rows);
  const cellOf = (x, y) => Math.floor(y / CELL) * cols + Math.floor(x / CELL);
  const inside = (x, y) => x >= 0 && x < W && y >= 0 && y < H;

  const trace = (x0, y0, dir) => {
    const pts = [];
    let x = x0, y = y0;
    for (let i = 0; i < MAX_STEPS / 2; i++) {
      // Midpoint (RK2) step along the field.
      const a1 = angle(x, y);
      const mx = x + dir * Math.cos(a1) * STEP * 0.5, my = y + dir * Math.sin(a1) * STEP * 0.5;
      const a2 = angle(mx, my);
      const nx = x + dir * Math.cos(a2) * STEP, ny = y + dir * Math.sin(a2) * STEP;
      if (!inside(nx, ny)) break;
      const c = cellOf(nx, ny);
      if (busy[c] && c !== cellOf(x, y)) break;
      pts.push([nx, ny]);
      x = nx; y = ny;
    }
    return pts;
  };

  const paths = [[], [], []];
  let made = 0, tries = 0;
  while (made < TARGET && tries < TARGET * 40) {
    tries++;
    const x0 = rand() * W, y0 = rand() * H;
    if (busy[cellOf(x0, y0)]) continue;
    const fwd = trace(x0, y0, 1);
    const back = trace(x0, y0, -1).reverse();
    const pts = [...back, [x0, y0], ...fwd];
    if (pts.length < MIN_STEPS) continue;
    // Claim the cells so the next line keeps its distance.
    for (const [x, y] of pts) busy[cellOf(x, y)] = 1;
    // Integer coordinates with relative moves: small files, and a pen's wobble.
    let px = Math.round(pts[0][0]), py = Math.round(pts[0][1]);
    let d = `M${px} ${py}`;
    for (let i = 1; i < pts.length; i++) {
      const cx = Math.round(pts[i][0]), cy = Math.round(pts[i][1]);
      const dx = cx - px, dy = cy - py;
      if (dx === 0 && dy === 0) continue;
      d += `l${dx} ${dy}`;
      px = cx; py = cy;
    }
    paths[made % 3].push(`<path pathLength="1" d="${d}"/>`);
    made++;
  }
  const groups = paths.map((ps, i) => `<g stroke-opacity="${ALPHAS[i]}">${ps.join('')}</g>`).join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" fill="none" stroke="#1A1A1A" stroke-width=".5" stroke-linecap="round">${groups}</svg>`;
  return { svg, made };
};

fs.mkdirSync(OUT, { recursive: true });
for (let n = 1; n <= 6; n++) {
  const { svg, made } = field(n);
  const file = path.join(OUT, `field-${n}.svg`);
  fs.writeFileSync(file, svg);
  const gz = zlib.gzipSync(svg).length;
  console.log(`${path.relative(ROOT, file)}  ${made} streamlines  ${(svg.length / 1024).toFixed(1)} kB raw  ${(gz / 1024).toFixed(1)} kB gz`);
}
