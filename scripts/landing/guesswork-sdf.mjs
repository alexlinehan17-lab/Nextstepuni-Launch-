/**
 * "Less guesswork." — a signed-distance-field texture of the word
 * "guesswork", set in the page's own Source Serif 4 at the display weight, for
 * the erosion effect in components/landing/fx-i/Guesswork*.
 *
 * No SDF/MSDF generator in node_modules works offline on a CFF2 variable
 * font, so the word is rasterised by headless Chromium (with the page's own
 * woff2, so the glyphs match the DOM text exactly) at 2× the texture size,
 * an exact Euclidean distance transform (Felzenszwalb–Huttenlocher) is taken
 * inside and out, and the signed result is box-filtered down to the texture.
 * One word, one texture: an atlas of nine glyphs would only add kerning to
 * reproduce. Output (committed):
 *   public/assets/landing/guesswork/guesswork-sdf.png   8-bit grey, 0.5 = edge
 *   public/assets/landing/guesswork/guesswork.json      metrics in texture px
 *
 *   PW_DIR=<dir with node_modules/playwright> node scripts/landing/guesswork-sdf.mjs
 */

import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../..');
const outDir = path.join(repo, 'public/assets/landing/guesswork');
const fontFile = path.join(repo, 'components/landing/fx-foundation/fonts/SourceSerif4Variable-Roman.otf.woff2');

const WORD = 'guesswork';
const WEIGHT = 600;
const EM = 160;            // texture px per em
const SPREAD = 16;         // texture px of distance encoded either side of the edge
const PAD = 24;            // texture px of margin round the ink (> SPREAD so distances saturate before the border)
const OVER = 2;            // rasterise at this multiple, then box-filter down

const pwDir = process.env.PW_DIR;
if (!pwDir) { console.error('Set PW_DIR to a directory whose node_modules has playwright (it is not a repo dependency).'); process.exit(1); }
const { chromium } = createRequire(path.join(pwDir, 'package.json'))('playwright');

/** Felzenszwalb–Huttenlocher 1-D squared distance transform, in place on f (length n), with scratch arrays. */
const edt1d = (f, n, d, v, z) => {
  let k = 0; v[0] = 0; z[0] = -Infinity; z[1] = Infinity;
  for (let q = 1; q < n; q++) {
    let s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    while (s <= z[k]) { k--; s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]); }
    k++; v[k] = q; z[k] = s; z[k + 1] = Infinity;
  }
  k = 0;
  for (let q = 0; q < n; q++) { while (z[k + 1] < q) k++; d[q] = (q - v[k]) * (q - v[k]) + f[v[k]]; }
};

/** Exact Euclidean distance (px) from every pixel to the nearest pixel where inside[i] is true. */
const edt2d = (inside, w, h) => {
  const INF = 1e12;
  const g = new Float64Array(w * h);
  for (let i = 0; i < w * h; i++) g[i] = inside[i] ? 0 : INF;
  const n = Math.max(w, h);
  const f = new Float64Array(n), d = new Float64Array(n), v = new Int32Array(n), z = new Float64Array(n + 1);
  for (let x = 0; x < w; x++) {
    for (let y = 0; y < h; y++) f[y] = g[y * w + x];
    edt1d(f, h, d, v, z);
    for (let y = 0; y < h; y++) g[y * w + x] = d[y];
  }
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) f[x] = g[y * w + x];
    edt1d(f, w, d, v, z);
    for (let x = 0; x < w; x++) g[y * w + x] = Math.sqrt(d[x]);
  }
  return g;
};

const CRC = new Int32Array(256);
for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; CRC[n] = c; }
const crc32 = (buf) => { let c = -1; for (let i = 0; i < buf.length; i++) c = CRC[(c ^ buf[i]) & 0xff] ^ (c >>> 8); return (c ^ -1) >>> 0; };
const chunk = (type, data) => {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length, 0);
  const body = Buffer.concat([Buffer.from(type, 'ascii'), data]);
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(body), 0);
  return Buffer.concat([len, body, crc]);
};
/** 8-bit greyscale PNG (colour type 0) with the Paeth-free "up" filter, which suits a smooth field. */
const encodeGreyPNG = (width, height, grey) => {
  const raw = Buffer.alloc((width + 1) * height);
  for (let y = 0; y < height; y++) {
    raw[y * (width + 1)] = 2; // Up
    for (let x = 0; x < width; x++) raw[y * (width + 1) + 1 + x] = (grey[y * width + x] - (y ? grey[(y - 1) * width + x] : 0)) & 255;
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0); ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; ihdr[9] = 0; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  return Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0))]);
};

const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  const font64 = fs.readFileSync(fontFile).toString('base64');
  await page.setContent(`<style>@font-face{font-family:'SS4';src:url(data:font/woff2;base64,${font64}) format('woff2');font-weight:400 700}</style>`);
  const raster = await page.evaluate(async ({ word, weight, size, padHi }) => {
    const font = `${weight} ${size}px 'SS4'`;
    await document.fonts.load(font, word);
    const probe = document.createElement('canvas').getContext('2d');
    probe.font = font;
    const m = probe.measureText(word);
    const left = Math.ceil(m.actualBoundingBoxLeft), right = Math.ceil(m.actualBoundingBoxRight);
    const asc = Math.ceil(m.actualBoundingBoxAscent), desc = Math.ceil(m.actualBoundingBoxDescent);
    const w = left + right + 2 * padHi, h = asc + desc + 2 * padHi;
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const ctx = c.getContext('2d');
    ctx.font = font; ctx.fillStyle = '#000'; ctx.textBaseline = 'alphabetic';
    const ox = padHi + left, oy = padHi + asc;
    ctx.fillText(word, ox, oy);
    const a = ctx.getImageData(0, 0, w, h).data;
    const alpha = new Array(w * h);
    for (let i = 0; i < w * h; i++) alpha[i] = a[i * 4 + 3];
    return { w, h, ox, oy, advance: m.width, left, right, asc, desc, alpha, loaded: document.fonts.check(font) };
  }, { word: WORD, weight: WEIGHT, size: EM * OVER, padHi: PAD * OVER });
  if (!raster.loaded) throw new Error('Source Serif 4 did not load in the rasteriser');

  const { w, h, alpha } = raster;
  const inside = new Uint8Array(w * h), outside = new Uint8Array(w * h);
  for (let i = 0; i < w * h; i++) { inside[i] = alpha[i] >= 128 ? 1 : 0; outside[i] = 1 - inside[i]; }
  const dOut = edt2d(inside, w, h);   // distance to ink, for pixels outside it
  const dIn = edt2d(outside, w, h);   // distance to paper, for pixels inside the ink
  const signed = new Float64Array(w * h);
  for (let i = 0; i < w * h; i++) {
    // Positive inside. The coverage at the edge pixel refines the half-pixel the binary transform loses.
    const cov = alpha[i] / 255;
    signed[i] = inside[i] ? Math.max(0, dIn[i] - 1 + cov) : -Math.max(0, dOut[i] - cov);
  }

  const tw = Math.floor(w / OVER), th = Math.floor(h / OVER);
  const grey = new Uint8Array(tw * th);
  for (let y = 0; y < th; y++) for (let x = 0; x < tw; x++) {
    let s = 0;
    for (let dy = 0; dy < OVER; dy++) for (let dx = 0; dx < OVER; dx++) s += signed[(y * OVER + dy) * w + x * OVER + dx];
    const d = s / (OVER * OVER) / OVER; // hi-res px → texture px
    grey[y * tw + x] = Math.round(Math.min(1, Math.max(0, 0.5 + d / (2 * SPREAD))) * 255);
  }

  fs.mkdirSync(outDir, { recursive: true });
  const png = encodeGreyPNG(tw, th, grey);
  fs.writeFileSync(path.join(outDir, 'guesswork-sdf.png'), png);
  const metrics = {
    word: WORD,
    font: `Source Serif 4 ${WEIGHT}`,
    emPx: EM,
    spread: SPREAD,
    width: tw,
    height: th,
    /** Pen origin (x) and baseline (y) inside the texture, texture px. */
    originX: raster.ox / OVER,
    originY: raster.oy / OVER,
    /** Advance width of the word, texture px (so DOM width / advance = px per texture px). */
    advance: raster.advance / OVER,
    /** Ink bounds relative to the origin, texture px. */
    ink: { left: raster.left / OVER, right: raster.right / OVER, ascent: raster.asc / OVER, descent: raster.desc / OVER },
    generated: new Date().toISOString().slice(0, 10),
  };
  fs.writeFileSync(path.join(outDir, 'guesswork.json'), JSON.stringify(metrics, null, 2) + '\n');
  console.log(`${tw}×${th} sdf, ${(png.length / 1024).toFixed(1)} kB; advance ${metrics.advance.toFixed(1)} px at ${EM} px/em`);
} finally {
  await browser.close();
}
