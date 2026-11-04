/**
 * Hand-lettered notes that write themselves (components/landing/fx/Note.tsx).
 *
 * A small single-stroke lowercase — strokes, not outlined glyphs — lettered on
 * a 10 × 14 grid (x-height 5, baseline 10), then set with an 8 % lean, a
 * seeded wobble on every control point and a small tilt per letter, and
 * smoothed Catmull-Rom → cubic so it reads as a pen, not a plotter. Every
 * note is ONE path of many subpaths in writing order with pathLength="1", so
 * a single stroke-dashoffset animation writes it stroke by stroke and the pen
 * lifts between letters for free. The one orange star dots an i.
 *
 *   node scripts/landing/lettering.mjs
 *
 * Writes components/landing/fx/notes/{here,join,end}.svg.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { prng, simplex } from './lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT = path.join(ROOT, 'components', 'landing', 'fx', 'notes');

/** Glyphs: advance width in grid units, strokes as point lists (x right, y down; baseline y = 10). */
const GLYPHS = {
  a: { w: 8, s: [[[6.2, 5.4], [3.6, 4.9], [1.4, 6.8], [1.6, 9.2], [3.6, 10.2], [6, 8.6], [6.3, 5.2], [6.5, 10], [7.6, 9.4]]] },
  c: { w: 7.5, s: [[[7, 6], [5, 4.9], [2.2, 5.6], [1.4, 7.6], [2.2, 9.6], [4.8, 10.3], [7, 9.2]]] },
  d: { w: 8.5, s: [[[6.3, 6], [4, 4.9], [1.6, 6.4], [1.5, 8.8], [3.6, 10.3], [6.3, 8.4], [6.5, 1], [6.6, 10], [7.8, 9.5]]] },
  e: { w: 7.5, s: [[[1.6, 7.6], [6.4, 7.3], [6, 5.3], [3.4, 4.9], [1.4, 7.2], [2, 9.6], [4.6, 10.3], [7, 9.2]]] },
  h: { w: 8, s: [[[1.8, 0.8], [1.7, 10.2], [1.8, 7.2], [3.8, 5], [6.2, 5.6], [6.5, 7.8], [6.4, 10.2]]] },
  i: { w: 4, s: [[[2, 5.2], [2, 10.2]]], dot: [2, 2.6] },
  j: { w: 5, s: [[[2.4, 5.2], [2.5, 11.5], [1.6, 13.2], [0.2, 12.4]]], dot: [2.4, 2.6] },
  l: { w: 5, s: [[[2, 0.8], [1.9, 9.6], [3.2, 10.3], [4.4, 9.6]]] },
  n: { w: 8, s: [[[1.8, 5.2], [1.7, 10.2], [1.9, 7.2], [3.8, 5.1], [6.2, 5.6], [6.5, 7.8], [6.4, 10.2]]] },
  o: { w: 7.5, s: [[[6.2, 7.4], [5, 5.1], [2.4, 5.3], [1.4, 7.6], [2.4, 9.9], [5, 10.2], [6.3, 8], [5.9, 5.9]]] },
  r: { w: 7, s: [[[1.8, 5.2], [1.7, 10.2], [1.9, 7.4], [3.6, 5.3], [5.8, 5.3], [6.4, 6.2]]] },
  s: { w: 7.5, s: [[[6.2, 5.8], [4.2, 4.9], [2, 5.7], [2.2, 7.2], [5.2, 8], [6.2, 9.4], [4.4, 10.3], [1.6, 9.6]]] },
  t: { w: 6, s: [[[2.8, 1.8], [2.6, 9.4], [3.8, 10.3], [5.2, 9.6]], [[0.8, 5.2], [5.4, 5]]] },
  u: { w: 8, s: [[[1.6, 5.2], [1.5, 9], [2.8, 10.3], [5.4, 9.4], [6.2, 5.2], [6.3, 10.2], [7.4, 9.6]]] },
  w: { w: 8.5, s: [[[0.8, 5.2], [2.4, 10.3], [4, 6.4], [5.6, 10.3], [7.4, 5.2]]] },
  y: { w: 8, s: [[[1.6, 5.2], [1.6, 8.8], [3, 10.2], [5.6, 9], [6.4, 5.2], [6, 11.4], [4.6, 13.2], [2.6, 12.6]]] },
  "'": { w: 2.5, s: [[[1, 1.6], [0.6, 3.4]]] },
  ' ': { w: 4, s: [] },
};

const SLANT = 0.08;      // x shifts by SLANT per unit above the baseline
const UNIT = 2.1;        // px per grid unit: x-height ≈ 10.5 px
const SPACING = 0.9;     // units between letters
const STAR = 'M0 -3.2l.95 1.95 2.15.3-1.55 1.5.37 2.15L0 3.7l-1.92 1 .37-2.15-1.55-1.5 2.15-.3z';

const fmt = (v) => (Math.round(v * 10) / 10).toString();

/** Catmull-Rom through the points → one cubic-Bézier subpath. */
const smooth = (pts) => {
  if (pts.length < 2) return '';
  let d = `M${fmt(pts[0][0])} ${fmt(pts[0][1])}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] ?? pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] ?? pts[i + 1];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += `C${fmt(c1[0])} ${fmt(c1[1])} ${fmt(c2[0])} ${fmt(c2[1])} ${fmt(p2[0])} ${fmt(p2[1])}`;
  }
  return d;
};

/**
 * Letter `lines` (an array of strings) starting at (ox, oy) px, returning the
 * subpaths in writing order plus the star's position if an i was dotted.
 * `starOn` names which glyph index (over the whole note) gets the star dot.
 */
const letter = (lines, { ox, oy, seed, starOn = -1, leading = 17 }) => {
  const rand = prng(seed);
  const wobble = simplex(rand);
  const subpaths = [];
  let star = null;
  let glyphIndex = 0;
  let width = 0;
  lines.forEach((text, li) => {
    let pen = ox;
    const base = oy + li * leading;
    for (const ch of text) {
      const g = GLYPHS[ch];
      if (!g) throw new Error(`no glyph for "${ch}"`);
      const tilt = (rand() - 0.5) * 0.09;          // radians, per letter
      const lift = (rand() - 0.5) * 0.35;          // units, per letter
      const place = ([x, y]) => {
        // Wobble in grid units, slant, tilt about the letter's baseline centre, then to px.
        const wx = x + 0.16 * wobble(x * 0.9 + glyphIndex * 3.1, y * 0.9 + seed);
        const wy = y + 0.16 * wobble(x * 0.9 + 7.7, y * 0.9 + glyphIndex * 2.3 + seed);
        const sx = wx + (10 - wy) * SLANT - g.w / 2;
        const sy = wy - 10 + lift;
        const rx = sx * Math.cos(tilt) - sy * Math.sin(tilt) + g.w / 2;
        const ry = sx * Math.sin(tilt) + sy * Math.cos(tilt) + 10;
        return [pen + rx * UNIT, base + (ry - 10) * UNIT];
      };
      for (const stroke of g.s) subpaths.push(smooth(stroke.map(place)));
      if (g.dot) {
        const [dx, dy] = place(g.dot);
        if (glyphIndex === starOn) star = [dx, dy];
        else subpaths.push(`M${fmt(dx)} ${fmt(dy)}l.4 .3`);
      }
      pen += (g.w + SPACING) * UNIT;
      glyphIndex++;
    }
    width = Math.max(width, pen - ox);
  });
  return { subpaths, star, width, height: lines.length * leading };
};

/** A curved arrow from `from` to `to` (px) with an open head, as subpaths. */
const arrow = (from, to, bulge, seed) => {
  const rand = prng(seed);
  const mid = [(from[0] + to[0]) / 2 + bulge[0], (from[1] + to[1]) / 2 + bulge[1]];
  const shaft = [from, [from[0] * 0.6 + mid[0] * 0.4 + (rand() - 0.5), from[1] * 0.6 + mid[1] * 0.4], mid, [to[0] * 0.55 + mid[0] * 0.45, to[1] * 0.55 + mid[1] * 0.45 + (rand() - 0.5)], to];
  const ang = Math.atan2(to[1] - shaft[3][1], to[0] - shaft[3][0]);
  const head = (side) => {
    const a = ang + Math.PI + side * 0.55;
    return [[to[0] + Math.cos(a) * 7.5, to[1] + Math.sin(a) * 7.5], to];
  };
  return [smooth(shaft), smooth(head(1)), smooth(head(-1))];
};

const write = (name, { subpaths, star, w, h }) => {
  const d = subpaths.filter(Boolean).join('');
  const starEl = star ? `<path class="fx-note-star" d="${STAR}" transform="translate(${fmt(star[0])} ${fmt(star[1] - 1)})"/>` : '';
  // No role or label here: Note.tsx supplies them from copy.ts and hides the SVG itself.
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" aria-hidden="true" focusable="false"><path class="fx-note-ink" pathLength="1" d="${d}"/>${starEl}</svg>`;
  const file = path.join(OUT, `${name}.svg`);
  fs.writeFileSync(file, svg);
  console.log(`${path.relative(ROOT, file)}  ${w}×${h}  ${(svg.length / 1024).toFixed(1)} kB`);
};

fs.mkdirSync(OUT, { recursive: true });

// 'you are here' — beside the sticky rail; the arrow points up-left at the contents column.
{
  const t = letter(['you are here'], { ox: 30, oy: 34, seed: 11 });
  const a = arrow([24, 30], [8, 8], [-6, 6], 12);
  write('here', { subpaths: [...t.subpaths, ...a], star: null, w: Math.ceil(t.width + 36), h: 50 });
}

// "join with your school's code" — beside the sign-up link in Schools; the arrow points right.
{
  const t = letter(['join with your', "school's code"], { ox: 4, oy: 26, seed: 23, starOn: 2, leading: 24 });
  const w = Math.ceil(t.width + 44);
  const a = arrow([t.width + 8, 30], [w - 4, 14], [8, 10], 24);
  write('join', { subpaths: [...t.subpaths, ...a], star: t.star, w, h: 62 });
}

// 'the end' — on the footer line, where the character lands.
{
  const t = letter(['the end'], { ox: 4, oy: 30, seed: 37 });
  write('end', { subpaths: t.subpaths, star: null, w: Math.ceil(t.width + 8), h: 42 });
}
