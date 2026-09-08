/**
 * The chapter scenes: one full-bleed background per chapter of the landing
 * page (components/landing/fx-h), drawn in the page's own materials — ink
 * hairlines on white, and the two SEC cover tints where the subject is the
 * papers themselves. Each is a 1440 × 900 tile that repeats vertically, so
 * one asset serves both the WebGL bleed textures and the static CSS
 * fallback (background-repeat: repeat-y).
 *
 *   node scripts/landing/scenes-svg.mjs
 *
 * Writes public/assets/landing/scenes/<chapter id>.svg, each well under
 * 20 kB. Everything is deterministic.
 *
 *   markbank      ruled answer-book lines with the red margin rule
 *   papertrail    the SEC cover tints, banded like a stack of papers, with
 *                 the cover's white oval bitten out of them
 *   atlas         contour lines like an Ordnance Survey sheet
 *   planner       a week grid, seven columns, Sunday hatched off
 *   launchpad     CAO-form choice boxes and arrows
 *   lab           graph paper with a faint sine and its dashed cosine
 *   futurefinder  a compass rose and a road
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { prng } from './lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT = path.join(ROOT, 'public', 'assets', 'landing', 'scenes');
const W = 1440, H = 900;

const INK = '#1A1A1A';
const ORANGE = '#F26B1F';
/** Sampled from public/assets/landing/papers/*.webp: Higher Level pink, Ordinary Level blue. */
const PINK = '#E2A7C2';
const BLUE = '#A7D0EF';

const r1 = (v) => Math.round(v * 10) / 10;
const svg = (body) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${body}</svg>`;
/** A hairline group: 1 px ink at the given alpha. */
const ink = (d, alpha, extra = '') => `<path d="${d}" fill="none" stroke="${INK}" stroke-opacity="${alpha}" stroke-width="1"${extra}/>`;
const hlines = (ys, x0 = 0, x1 = W) => ys.map(y => `M${x0} ${r1(y)}H${x1}`).join('');
const vlines = (xs, y0 = 0, y1 = H) => xs.map(x => `M${r1(x)} ${y0}V${y1}`).join('');
const range = (n, f) => Array.from({ length: n }, (_, i) => f(i));

/* ── Periodic gradient noise, so a field can tile ─────────────────────────── */

/** 2-D Perlin noise on a lattice that repeats every px × py cells. */
const periodicNoise = (rand, px, py) => {
  const g = range(px * py, () => { const a = rand() * Math.PI * 2; return [Math.cos(a), Math.sin(a)]; });
  const fade = (t) => t * t * t * (t * (t * 6 - 15) + 10);
  const dot = (ix, iy, x, y) => { const v = g[((iy % py + py) % py) * px + ((ix % px + px) % px)]; return v[0] * x + v[1] * y; };
  return (x, y) => {
    const ix = Math.floor(x), iy = Math.floor(y), fx = x - ix, fy = y - iy;
    const u = fade(fx), v = fade(fy);
    const a = dot(ix, iy, fx, fy), b = dot(ix + 1, iy, fx - 1, fy);
    const c = dot(ix, iy + 1, fx, fy - 1), d = dot(ix + 1, iy + 1, fx - 1, fy - 1);
    return (a + (b - a) * u) + ((c + (d - c) * u) - (a + (b - a) * u)) * v;
  };
};

/* ── I · Mark Bank: the answer book ───────────────────────────────────────── */

const markbank = () => {
  const rules = hlines(range(H / 30, i => 15 + i * 30));
  return svg(
    ink(rules, 0.085, ' shape-rendering="crispEdges"') +
    // The red margin rule, in the page's one accent, doubled the way the answer book rules it.
    `<path d="M118 0V${H}M124 0V${H}" fill="none" stroke="${ORANGE}" stroke-opacity="0.3" stroke-width="1" shape-rendering="crispEdges"/>`,
  );
};

/* ── II · Paper Trail: a stack of covers ──────────────────────────────────── */

const papertrail = () => {
  const pitch = 36, band = 13, n = H / pitch;
  const rand = prng(202);
  // Mostly Higher Level; every so often an Ordinary Level paper in the pile.
  const blue = new Set();
  while (blue.size < 5) blue.add(Math.floor(rand() * n));
  const bands = range(n, i =>
    `<rect x="0" y="${i * pitch + 9}" width="${W}" height="${band}" fill="${blue.has(i) ? BLUE : PINK}"/>`).join('');
  // The SEC cover's white oval, bitten out of the pile; a smaller one off the right edge.
  const ovals = `<ellipse cx="470" cy="450" rx="560" ry="392" fill="#FFFFFF"/><ellipse cx="1420" cy="700" rx="300" ry="160" fill="#FFFFFF"/>`;
  // Every sheet's edge, run through the ovals too, so the pile still reads as paper.
  const edges = hlines(range(n, i => i * pitch + 9 + 0.5));
  return svg(`<g opacity="0.46">${bands}</g>${ovals}` + ink(edges, 0.07, ' shape-rendering="crispEdges"'));
};

/* ── III · Topic Atlas: contours ──────────────────────────────────────────── */

const atlas = () => {
  const cell = 18, nx = W / cell, ny = H / cell;
  const rand = prng(303);
  // Three octaves on lattices that all repeat in 900, so the field tiles vertically.
  const base = 225;
  const amp = [1, 0.42, 0.14];
  // Only the vertical period must divide the tile exactly; nothing tiles sideways.
  const oct = [1, 2, 4].map((f, i) => ({ f, n: periodicNoise(rand, Math.ceil((W / base) * f), (H / base) * f), a: amp[i] }));
  const field = (x, y) => oct.reduce((s, o) => s + o.a * o.n((x / base) * o.f, (y / base) * o.f), 0);
  const h = range(ny + 1, j => range(nx + 1, i => field(i * cell, j * cell)));
  let lo = Infinity, hi = -Infinity;
  for (const row of h) for (const v of row) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
  const levels = 10;
  const paths = { index: [], plain: [] };
  for (let l = 1; l < levels; l++) {
    const iso = lo + (hi - lo) * (l / levels);
    const segs = [];
    const lerp = (a, b, pa, pb) => { const t = (iso - a) / (b - a); return [pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t]; };
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const tl = h[j][i], tr = h[j][i + 1], br = h[j + 1][i + 1], bl = h[j + 1][i];
      const idx = (tl > iso ? 8 : 0) | (tr > iso ? 4 : 0) | (br > iso ? 2 : 0) | (bl > iso ? 1 : 0);
      if (idx === 0 || idx === 15) continue;
      const x = i * cell, y = j * cell;
      const top = () => lerp(tl, tr, [x, y], [x + cell, y]);
      const right = () => lerp(tr, br, [x + cell, y], [x + cell, y + cell]);
      const bottom = () => lerp(bl, br, [x, y + cell], [x + cell, y + cell]);
      const left = () => lerp(tl, bl, [x, y], [x, y + cell]);
      const add = (a, b) => segs.push([a, b]);
      switch (idx) {
        case 1: case 14: add(left(), bottom()); break;
        case 2: case 13: add(bottom(), right()); break;
        case 3: case 12: add(left(), right()); break;
        case 4: case 11: add(top(), right()); break;
        case 5: add(left(), top()); add(bottom(), right()); break;
        case 6: case 9: add(top(), bottom()); break;
        case 7: case 8: add(left(), top()); break;
        case 10: add(top(), right()); add(left(), bottom()); break;
      }
    }
    // Chain segments into polylines so the path data is short.
    const key = (p) => `${Math.round(p[0] * 2)},${Math.round(p[1] * 2)}`;
    const ends = new Map();
    segs.forEach((s, n) => { for (const p of s) { const k = key(p); (ends.get(k) ?? ends.set(k, []).get(k)).push(n); } });
    const used = new Uint8Array(segs.length);
    const walk = (n, p) => {
      const line = [p];
      let cur = n, at = p;
      for (;;) {
        used[cur] = 1;
        const s = segs[cur];
        at = key(s[0]) === key(at) ? s[1] : s[0];
        line.push(at);
        const next = (ends.get(key(at)) ?? []).find(m => !used[m]);
        if (next === undefined) break;
        cur = next;
      }
      return line;
    };
    let d = '';
    for (let n = 0; n < segs.length; n++) {
      if (used[n]) continue;
      // Start from an open end where there is one, so a line is walked once, not twice.
      const openEnd = segs[n].find(p => (ends.get(key(p)) ?? []).filter(m => !used[m]).length === 1) ?? segs[n][0];
      const line = walk(n, openEnd);
      let px = Math.round(line[0][0]), py = Math.round(line[0][1]);
      d += `M${px} ${py}`;
      for (let k = 1; k < line.length; k++) {
        const qx = Math.round(line[k][0]), qy = Math.round(line[k][1]);
        d += `l${qx - px} ${qy - py}`; px = qx; py = qy;
      }
    }
    (l % 4 === 0 ? paths.index : paths.plain).push(d);
  }
  // The sheet's kilometre grid under the contours.
  const grid = vlines(range(W / 100 - 1, i => (i + 1) * 100)) + hlines(range(H / 100 - 1, i => (i + 1) * 100));
  return svg(
    ink(grid, 0.045, ' shape-rendering="crispEdges"') +
    ink(paths.plain.join(''), 0.075, ' stroke-linejoin="round"') +
    ink(paths.index.join(''), 0.12, ' stroke-linejoin="round"'),
  );
};

/* ── IV · Planner & Study: the week ───────────────────────────────────────── */

const planner = () => {
  const col = W / 7;
  const columns = vlines(range(6, i => (i + 1) * col));
  const hours = hlines(range(H / 60, i => i * 60 + 30));
  // Sunday, hatched off: rest days stay rest days.
  let hatch = '';
  for (let s = -H; s < col; s += 22) hatch += `M${r1(6 * col + s)} 0l${H} ${H}`;
  // A few study blocks on the week, outlined the way the planner draws them.
  const rand = prng(404);
  let blocks = '';
  const slots = [[0, 2], [1, 5], [2, 1], [2, 9], [3, 6], [4, 3], [4, 11], [5, 7], [0, 12], [3, 13]];
  for (const [c, row] of slots) {
    const hgt = 60 * (1 + Math.floor(rand() * 2));
    blocks += `<rect x="${r1(c * col + 8)}" y="${row * 60 + 34}" width="${r1(col - 16)}" height="${hgt - 8}" rx="3" fill="none" stroke="${INK}" stroke-opacity="0.11" stroke-width="1"/>`;
  }
  return svg(
    ink(hours, 0.065, ' shape-rendering="crispEdges"') +
    ink(columns, 0.1, ' shape-rendering="crispEdges"') +
    `<g clip-path="url(#sun)">${ink(hatch, 0.05)}</g><clipPath id="sun"><rect x="${r1(6 * col)}" y="0" width="${r1(col)}" height="${H}"/></clipPath>` +
    blocks,
  );
};

/* ── V · Launchpad: the CAO form ──────────────────────────────────────────── */

const launchpad = () => {
  const box = 30, gap = 5, rowPitch = 54, rows = 10, cols = 6;
  const list = (x0, y0) => {
    let d = '';
    for (let r = 0; r < rows; r++) {
      const y = y0 + r * rowPitch;
      // The choice number's ring, then six code boxes.
      d += `<circle cx="${x0 - 30}" cy="${y + 18}" r="8" fill="none" stroke="${INK}" stroke-opacity="0.09" stroke-width="1"/>`;
      for (let c = 0; c < cols; c++) d += `<rect x="${x0 + c * (box + gap)}" y="${y}" width="${box}" height="36" fill="none" stroke="${INK}" stroke-opacity="0.1" stroke-width="1"/>`;
    }
    return d;
  };
  const top = 150;
  const heads = hlines([top - 40, top + rows * rowPitch + 4], 140, W - 140);
  // Arrows out of a few choices: a course, a route, a deadline met.
  const arrow = (x, y, dx, dy, bend) =>
    `<path d="M${x} ${y}q${bend[0]} ${bend[1]} ${dx} ${dy}" fill="none" stroke="${INK}" stroke-opacity="0.12" stroke-width="1"/>` +
    `<path d="M${x + dx} ${y + dy}m-9 -5l9 5l-9 5" fill="none" stroke="${INK}" stroke-opacity="0.12" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>`;
  const arrows =
    arrow(410, top + 18, 300, -60, [140, -70]) +
    arrow(410, top + 18 + rowPitch * 3, 300, 22, [150, 40]) +
    arrow(410, top + 18 + rowPitch * 6, 300, -28, [180, -10]) +
    arrow(1050, top + 18 + rowPitch, 280, -40, [120, -50]) +
    arrow(1050, top + 18 + rowPitch * 5, 280, 40, [120, 60]);
  return svg(ink(heads, 0.12, ' shape-rendering="crispEdges"') + list(200, top) + list(840, top) + arrows);
};

/* ── VI · Learning Lab: graph paper ───────────────────────────────────────── */

const lab = () => {
  const minor = vlines(range(W / 15 - 1, i => (i + 1) * 15).filter(x => x % 75)) + hlines(range(H / 15 - 1, i => (i + 1) * 15).filter(y => y % 75));
  const major = vlines(range(Math.floor(W / 75), i => (i + 1) * 75)) + hlines(range(H / 75 - 1, i => (i + 1) * 75));
  const wave = (amp, phase, step = 6) => {
    let d = '';
    for (let x = 0; x <= W; x += step) {
      const y = 450 - amp * Math.sin((x / 480) * Math.PI * 2 + phase);
      d += (x === 0 ? 'M' : 'L') + `${x} ${r1(y)}`;
    }
    return d;
  };
  return svg(
    ink(minor, 0.045, ' shape-rendering="crispEdges"') +
    ink(major, 0.09, ' shape-rendering="crispEdges"') +
    `<path d="${wave(120, Math.PI / 2, 8)}" fill="none" stroke="${INK}" stroke-opacity="0.09" stroke-width="1" stroke-dasharray="6 8"/>` +
    `<path d="${wave(150, 0)}" fill="none" stroke="${INK}" stroke-opacity="0.16" stroke-width="1.25"/>`,
  );
};

/* ── VII · Future Finder: a compass rose and a road ───────────────────────── */

const futurefinder = () => {
  const cx = 1090, cy = 320, R = 180;
  const P = (a, r) => [r1(cx + Math.sin(a) * r), r1(cy - Math.cos(a) * r)];
  let rose = `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${INK}" stroke-opacity="0.1" stroke-width="1"/>`;
  rose += `<circle cx="${cx}" cy="${cy}" r="${R - 16}" fill="none" stroke="${INK}" stroke-opacity="0.1" stroke-width="1"/>`;
  rose += `<circle cx="${cx}" cy="${cy}" r="7" fill="none" stroke="${INK}" stroke-opacity="0.12" stroke-width="1"/>`;
  // Degree ticks between the rings, every fifth longer.
  let ticks = '';
  for (let i = 0; i < 72; i++) {
    const a = (i / 72) * Math.PI * 2, len = i % 9 === 0 ? 16 : i % 3 === 0 ? 10 : 5;
    const [x1, y1] = P(a, R), [x2, y2] = P(a, R - len);
    ticks += `M${x1} ${y1}L${x2} ${y2}`;
  }
  rose += ink(ticks, 0.1);
  // Eight points, each a diamond with its dark half filled.
  let points = '';
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2, long = i % 2 === 0;
    const len = long ? R - 26 : R - 78, half = long ? 15 : 10;
    const tip = P(a, len), l = P(a - Math.PI / 2, half), r = P(a + Math.PI / 2, half);
    points += `<path d="M${tip[0]} ${tip[1]}L${l[0]} ${l[1]}L${cx} ${cy}L${r[0]} ${r[1]}Z" fill="none" stroke="${INK}" stroke-opacity="0.12" stroke-width="1" stroke-linejoin="round"/>`;
    points += `<path d="M${tip[0]} ${tip[1]}L${r[0]} ${r[1]}L${cx} ${cy}Z" fill="${INK}" fill-opacity="0.07"/>`;
  }
  rose += points;
  // North's mark.
  const [nx, ny] = P(0, R + 22);
  rose += `<path d="M${nx} ${ny}l-7 16h14z" fill="none" stroke="${INK}" stroke-opacity="0.14" stroke-width="1" stroke-linejoin="round"/>`;

  // The road: a periodic centre line so the tile joins, with the verges drawn beside it.
  const centre = (y) => 430 + 150 * Math.sin((y / H) * Math.PI * 2) + 55 * Math.sin((y / H) * Math.PI * 4 + 1.2);
  const road = (offset, step = 10) => {
    let d = '';
    for (let y = 0; y <= H; y += step) {
      // Offset along the local normal so the width holds through the bends.
      const dx = (centre(y + 1) - centre(y - 1)) / 2;
      const nrm = 1 / Math.hypot(1, dx);
      const x = centre(y) + offset * nrm, yy = y - offset * dx * nrm;
      d += (y === 0 ? 'M' : 'L') + `${r1(x)} ${r1(yy)}`;
    }
    return d;
  };
  const verges = `<path d="${road(-28)}${road(28)}" fill="none" stroke="${INK}" stroke-opacity="0.11" stroke-width="1"/>`;
  const dashes = `<path d="${road(0)}" fill="none" stroke="${INK}" stroke-opacity="0.1" stroke-width="1" stroke-dasharray="20 16"/>`;
  return svg(verges + dashes + rose);
};

const SCENES = { markbank, papertrail, atlas, planner, launchpad, lab, futurefinder };

fs.mkdirSync(OUT, { recursive: true });
for (const [id, draw] of Object.entries(SCENES)) {
  const file = path.join(OUT, `${id}.svg`);
  const body = draw();
  fs.writeFileSync(file, body);
  console.log(`${path.relative(ROOT, file)}  ${(body.length / 1024).toFixed(1)} kB`);
}
