/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic-tag pipeline, step 1 — extract each anchored question's opening text.
 *
 * For a subject, reads the committed answer-map sidecars (which carry verified
 * per-question anchors: page pP + fractional pY), downloads each paper PDF, and
 * pulls the stem text at each anchor. Output feeds the classifier agents.
 *
 * Usage:  node scripts/paper-trail/topic-tags/extract-stems.mjs <subjectId> [cycle]
 *   e.g.  node scripts/paper-trail/topic-tags/extract-stems.mjs mathematics lc
 * Writes: scripts/paper-trail/topic-tags/out/<subjectId>-stems.json
 */
import fs from 'fs';
import path from 'path';
import * as pdfjs from 'pdfjs-dist/legacy/build/pdf.mjs';

const SUBJECT = process.argv[2];
const CYCLE = process.argv[3] || 'lc';
if (!SUBJECT) {
  console.error('usage: extract-stems.mjs <subjectId> [cycle]');
  process.exit(1);
}
const BUCKET = 'nextstepuni-app.firebasestorage.app';
const url = p => `https://firebasestorage.googleapis.com/v0/b/${BUCKET}/o/${encodeURIComponent(p)}?alt=media`;
const apply = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];

// answered papers for the subject, from the shipped index
const t = fs.readFileSync('paperTrailData.ts', 'utf8');
const s = t.indexOf('export const PAPER_TRAIL_INDEX');
const b = t.indexOf('{', s);
const e = t.indexOf('\n};', b);
const INDEX = JSON.parse(t.slice(b, e + 2).replace(/,\s*([\]}])/g, '$1'));
const rows = [];
for (const en of INDEX[SUBJECT] || [])
  for (const p of en.papers)
    if (p.answers === 1) rows.push({ year: en.year, level: en.level, lang: en.lang, label: p.label, f: p.doc.f });

const sideFor = (year, f) => {
  const p = `scripts/paper-trail/answers/${year}/${f}.json`;
  return fs.existsSync(p) ? p : null;
};

async function pageLines(pg) {
  const vp = pg.getViewport({ scale: 1 }), H = vp.height || 1;
  const c = await pg.getTextContent();
  const sp = c.items
    .filter(it => it.str && it.transform)
    .map(it => {
      const tr = it.transform;
      const [dx, dy] = apply(vp.transform, tr[4], tr[5]);
      return { s: it.str, x: dx, y: dy, w: it.width || 0, h: Math.hypot(tr[1], tr[3]) || 10 };
    });
  sp.sort((a, b) => a.y - b.y || a.x - b.x);
  const lines = [];
  let cur = [], ly = sp[0]?.y ?? 0;
  const push = L => {
    L.sort((a, b) => a.x - b.x);
    let tx = '', pr = null;
    for (const s of L) {
      if (pr !== null) {
        const g = s.x - pr;
        if (!tx.endsWith(' ') && !s.s.startsWith(' ') && g > s.h * 0.28) tx += ' ';
      }
      tx += s.s;
      pr = s.x + s.w;
    }
    if (tx.trim()) lines.push({ y: L[0].y / H, text: tx });
  };
  for (const s of sp) {
    const tol = Math.max(3, s.h * 0.6);
    if (!cur.length || Math.abs(s.y - ly) <= tol) {
      cur.push(s);
      ly = (ly * (cur.length - 1) + s.y) / cur.length;
    } else {
      push(cur);
      cur = [s];
      ly = s.y;
    }
  }
  if (cur.length) push(cur);
  return lines;
}

const out = [];
for (const r of rows) {
  const side = sideFor(r.year, r.f);
  if (!side) {
    console.error('no sidecar', r.year, r.f);
    continue;
  }
  const map = JSON.parse(fs.readFileSync(side, 'utf8'));
  let buf;
  const localPaper = path.join('paper-trail-corpus', 'exampapers', String(r.year), r.f);
  try {
    // The harvested corpus is the reproducible source when it is present.  The
    // old network-only path made an offline taxonomy audit report zero stems
    // even though the exact SEC PDFs were already checked into the workspace.
    if (fs.existsSync(localPaper)) buf = new Uint8Array(fs.readFileSync(localPaper));
    else {
      const res = await fetch(url(`papers/${CYCLE}/${SUBJECT}/${r.year}/paper/${r.f}`));
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      buf = new Uint8Array(await res.arrayBuffer());
    }
  } catch (error) {
    console.error('paper unavailable', r.year, r.f, error instanceof Error ? error.message : error);
    continue;
  }
  const doc = await pdfjs.getDocument({ data: buf }).promise;
  const cache = {};
  const getLines = async n => {
    if (!(n in cache)) {
      if (n < 1 || n > doc.numPages) cache[n] = [];
      else {
        const pg = await doc.getPage(n);
        cache[n] = await pageLines(pg);
        pg.cleanup();
      }
    }
    return cache[n];
  };
  const qs = map.q.slice().sort((a, b) => a.pP - b.pP || a.pY[0] - b.pY[0]);
  for (let i = 0; i < qs.length; i++) {
    const q = qs[i], startY = q.pY[0];
    const next = qs[i + 1];
    const endY = next && next.pP === q.pP ? next.pY[0] : 1.0;
    let lines = (await getLines(q.pP)).filter(l => l.y >= startY - 0.01 && l.y < endY);
    let stem = lines.map(l => l.text).join(' ');
    if (stem.length < 160) stem += ' ' + (await getLines(q.pP + 1)).filter(l => l.y < 0.5).map(l => l.text).join(' ');
    stem = stem.replace(/\s+/g, ' ').trim().slice(0, 700);
    out.push({ key: `${r.level}|${r.label}|${r.year}|${r.lang}|Q${q.n}`, subjectId: SUBJECT, level: r.level, paper: r.label, year: r.year, lang: r.lang, f: r.f, n: q.n, stem });
  }
  console.error('ok', r.year, r.level, r.label, '→', qs.length, 'q');
}
const dir = 'scripts/paper-trail/topic-tags/out';
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(path.join(dir, `${SUBJECT}-stems.json`), JSON.stringify(out, null, 1));
console.error('TOTAL stems', out.length);
