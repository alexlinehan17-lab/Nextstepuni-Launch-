/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ask the papers — build the search index the landing page lights up.
 *
 * For eight subjects, every English-language Leaving Certificate paper the
 * local corpus holds for 2010–2025 (Higher and Ordinary) is read with pdf.js,
 * split into questions by the paper's own numbering, stripped of the SEC's
 * page furniture and instructions, and written as one compact JSON per
 * subject in public/assets/landing/ask/. Only question text is kept: a
 * SECTION / PART / TEXT heading ends a question, and nothing between that
 * heading and the next numbered question survives — which is what keeps the
 * comprehension extracts and unseen poems of the English papers (third-party
 * text) out of the index. Each question keeps whole sentences up to a cap so
 * the eight files fit a ~1 MB budget uncompressed.
 *
 * Usage: node scripts/landing/ask-index.mjs [subject ...]   (default: all eight)
 * Reads:  paperTrailData.ts for the file ids, then
 *         /Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/exampapers/<year>/<fileid>
 * Writes: public/assets/landing/ask/<subject>.json and index.json, and prints
 *         a report of every paper that failed to open or yielded no questions.
 */

import fs from 'node:fs';
import path from 'node:path';
import * as pdfjs from 'pdfjs-dist/legacy/build/pdf.mjs';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const CORPUS = process.env.CORPUS || '/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/exampapers';
const OUT_DIR = path.join(ROOT, 'public', 'assets', 'landing', 'ask');
const YEARS = { from: 2010, to: 2025 };
const arg = (name, fallback) => { const a = process.argv.find(x => x.startsWith(`--${name}=`)); return a ? a.slice(name.length + 3) : fallback; };
/** Whole sentences are kept until a question's text passes this many characters. */
const TEXT_CAP = +arg('cap', 600);
/** Which levels to index; the size budget decides. */
const LEVELS = arg('levels', 'higher,ordinary').split(',');

/** Subject id in paperTrailData.ts → the name printed on the page and in the attribution. */
const SUBJECTS = [
  ['biology', 'Biology'],
  ['chemistry', 'Chemistry'],
  ['physics', 'Physics'],
  ['mathematics', 'Maths'],
  ['english', 'English'],
  ['geography', 'Geography'],
  ['economics', 'Economics'],
  ['business', 'Business'],
];
const ATTRIBUTION_NAME = { mathematics: 'Mathematics' };
const LEVEL_CODE = { higher: 'H', ordinary: 'O' };
const LEVEL = Object.fromEntries(LEVELS.filter(l => LEVEL_CODE[l]).map(l => [l, LEVEL_CODE[l]]));

/** The shipped index: which PDF is which paper. */
const loadIndex = () => {
  const t = fs.readFileSync(path.join(ROOT, 'paperTrailData.ts'), 'utf8');
  const s = t.indexOf('export const PAPER_TRAIL_INDEX');
  const b = t.indexOf('{', s);
  const e = t.indexOf('\n};', b);
  return JSON.parse(t.slice(b, e + 2).replace(/,\s*([\]}])/g, '$1'));
};

/** "Paper One / Higher Level (EV)" → "Paper 1"; "Exam Paper" → "". */
const paperLabel = (label) => {
  const l = label.replace(/\s*\/.*$/, '').replace(/:.*$/, '').trim();
  if (/^Exam Paper$/i.test(l)) return '';
  return l.replace(/\bOne\b/, '1').replace(/\bTwo\b/, '2').replace(/\s*&\s*/g, ' & ');
};

/** Mathematical italic/bold letters (U+1D400–U+1D7FF) back to plain letters; the
 *  maths papers emit each such glyph twice, so an evenly doubled run is halved. */
const MATH = /[\u{1D400}-\u{1D7FF}]+/gu;
const plainMath = (run) => {
  const chars = Array.from(run).map(ch => {
    const cp = ch.codePointAt(0);
    if (cp >= 0x1D400 && cp <= 0x1D6A3) { const i = (cp - 0x1D400) % 52; return String.fromCharCode(i < 26 ? 65 + i : 97 + i - 26); }
    if (cp >= 0x1D6A8 && cp <= 0x1D7CB) return ch; // greek: leave
    if (cp >= 0x1D7CE && cp <= 0x1D7FF) return String((cp - 0x1D7CE) % 10);
    return ch;
  });
  const even = chars.length % 2 === 0 && chars.every((c, i) => i % 2 === 1 ? c === chars[i - 1] : true);
  return (even ? chars.filter((_, i) => i % 2 === 0) : chars).join('');
};
/** Answer lines, inline marks tags and doubled maths glyphs out of a line of text. */
const clean = (t) => t
  .replace(MATH, plainMath)
  .replace(/_{3,}|\.{4,}|…{2,}/g, ' ')
  .replace(/\s\(\d{1,2}\)(?=\s|$)/g, ' ')
  .replace(/\s\[\d{1,2}\](?=\s|$)/g, ' ')
  .replace(/\s+/g, ' ')
  .trim();

const apply = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];

/** Text lines of one page with their position as fractions of the page. */
async function pageLines(pg) {
  const vp = pg.getViewport({ scale: 1 });
  const H = vp.height || 1, W = vp.width || 1;
  const c = await pg.getTextContent();
  const sp = c.items
    .filter(it => it.str && it.transform)
    .map(it => { const tr = it.transform; const [dx, dy] = apply(vp.transform, tr[4], tr[5]); return { s: it.str, x: dx, y: dy, w: it.width || 0, h: Math.hypot(tr[1], tr[3]) || 10 }; });
  sp.sort((a, b) => a.y - b.y || a.x - b.x);
  const lines = [];
  let cur = [], ly = sp[0]?.y ?? 0;
  const push = (L) => {
    L.sort((a, b) => a.x - b.x);
    let tx = '', pr = null;
    for (const s of L) {
      if (pr !== null && !tx.endsWith(' ') && !s.s.startsWith(' ') && s.x - pr > s.h * 0.28) tx += ' ';
      tx += s.s;
      pr = s.x + s.w;
    }
    const text = clean(tx);
    if (text) lines.push({ y: L[0].y / H, x: L[0].x / W, h: L[0].h, text });
  };
  for (const s of sp) {
    const tol = Math.max(3, s.h * 0.6);
    if (!cur.length || Math.abs(s.y - ly) <= tol) { cur.push(s); ly = (ly * (cur.length - 1) + s.y) / cur.length; }
    else { push(cur); cur = [s]; ly = s.y; }
  }
  if (cur.length) push(cur);
  return lines;
}

/* ── What starts, ends and never enters a question ─────────────────────── */

const NUMBERED = /^(\d{1,2})\.\s+(?=\S)/;
const QUESTION_N = /^Question\s+(\d{1,2})\b/;
const QUESTION_LETTER = /^QUESTION\s+([A-C])\b/;
/** English Paper 2's single-text heads: "C HAMLET – William Shakespeare". */
const TEXT_HEAD = /^([A-F])\s+[A-Z][A-Z'’.,:!?-]+(\s+[A-Z][A-Z'’.,:!?-]*)*\s+[–-]\s+\S/;
/** Headings that end a question. Nothing after one survives until the next question starts. */
const CUT = /^(SECTION|Section|PART|Part|TEXT|Text)\s+([A-Z0-9IVX]+)\b|^([A-C]\s+)?(UNSEEN|PRESCRIBED)\s+POE(M|TRY)|^(Acknowledgements?|ACKNOWLEDGEMENTS?|Blank Page|BLANK PAGE|Instructions|INSTRUCTIONS|Copyright notice|Texts$)/;
/** Lines that are furniture, never content. */
const DROP = [
  /^Leaving Certificate Examination/i,
  /^(Coimisiún na Scrúduithe Stáit|State Examinations Commission)/i,
  /^Page \d+/i,
  /^\d+$/,
  /^(Higher|Ordinary|Foundation) Level\b/i,
  /^\(?\d+\s*marks?\)?\.?$/i,
  /^(OR|or)$/,
  /^Turn over/i,
  /^Do not (write|hand)/i,
  /^Write your (answers?|examination|name)/i,
  /^Answer (any|all|either|both) /i,
  /^(Examination Number|Centre Stamp|Date of Birth|Candidate Number)/i,
  /^(Space|Page|Room|Extra space|Additional space) for (rough |extra |additional )?(work|writing|answers?)/i,
  /^\d{4}[LM.]\S*$/,
  /^This page is/i,
  /^There (are|is) .* (section|question|page)s? /i,
  /^It is recommended that/i,
  /^Each question carries/i,
  /^Marks will be/i,
  /^Marks for each/i,
  /^Calculators may be used/i,
  /^Relevant data are/i,
  /^Take (the )?(value of )?g\b/i,
  /^Take the acceleration/i,
  /^Assume the acceleration/i,
  /^You must answer/i,
  /^Candidates (must|should|may)/i,
  /^Use the (spaces|answerbook)/i,
  /^Total marks/i,
  /^Maximum marks/i,
  /^Marks$/i,
  /^Q\.\s?\d+\s*\(/,
  /^Question$/,
  /^(Question\s+)?Start each question on a new page/i,
  /^Answer Book/i,
  /^Rough work/i,
];

const isDrop = (l) => {
  if (l.y > 0.905 || l.y < 0.045) return true;
  if (!/[A-Za-z]{2}/.test(l.text)) return true;          // axis ticks, mark tables, "1 2 3 4 5", "H H H H"
  if (l.text.length <= 4) return true;                     // "(a)", "A", "i"
  const t = l.text;
  if (/:$/.test(t) && t.split(' ').length <= 3) return true; // answer-box labels: "Function:", "Tube A:"
  return DROP.some(re => re.test(t));
};

/** Split a block of text into sentences for the cap. */
const sentences = (s) => s.split(/(?<=[.?!])\s+(?=[A-Z“"‘(\d])/).map(x => x.trim()).filter(Boolean);
const capText = (s) => {
  const out = [];
  let n = 0;
  for (const sent of sentences(s)) {
    if (n >= TEXT_CAP) break;
    out.push(sent);
    n += sent.length + 1;
  }
  return out.join(' ');
};

/**
 * Walk a paper's lines and return its questions. The left margin is the
 * paper's own: the smallest x at which a numbered or "Question N" line
 * appears; a start must sit within 0.02 of it, which is what keeps a
 * question's internal "1. … 2. …" sub-list (indented) from splitting it.
 */
function splitQuestions(pages, subjectId) {
  const all = [];
  for (const [pg, lines] of pages) for (const l of lines) all.push({ ...l, pg });
  const heads = all.filter(l => l.y < 0.905 && (NUMBERED.test(l.text) || QUESTION_N.test(l.text)));
  const margin = heads.length ? Math.min(...heads.map(l => l.x)) : 0.05;
  const pageMargin = new Map();
  for (const l of heads) pageMargin.set(l.pg, Math.min(pageMargin.get(l.pg) ?? 1, l.x));
  // Booklets mirror their margins on facing pages, so a start may sit up to
  // 0.05 right of the paper's leftmost head — but never right of its own
  // page's leftmost head by more than 0.02, which is what rejects a
  // question's indented "1. … 2. …" sub-list.
  const atMargin = (l) => l.x <= margin + 0.05 && l.x <= (pageMargin.get(l.pg) ?? margin) + 0.02;
  const english = subjectId === 'english';
  const debug = process.env.ASK_DEBUG ? [] : null;

  const qs = [];
  let cur = null;
  let last = null;
  let cut = 'section';   // what ended the last block: 'section' (a heading), 'text' (an English TEXT — nothing numbered inside it is a question), or null
  let prevNumbered = null; // the previous numbered line, for the list-spacing test
  const close = () => { if (cur && cur.lines.length) qs.push(cur); cur = null; };
  /** A numbered line within three text lines of the previous numbered line on the same page, and no further left, is a list item. */
  const listSpaced = (l) => prevNumbered && prevNumbered.pg === l.pg && l.y - prevNumbered.y < 0.045 && l.x >= prevNumbered.x - 0.005;

  for (const l of all) {
    const t = l.text;
    let m;
    if ((m = CUT.exec(t))) { close(); cut = english && /^TEXT\b/i.test(t) ? 'text' : 'section'; continue; }
    let start = null;
    const numbered = NUMBERED.exec(t);
    if (numbered && l.y < 0.905) {
      const n = +numbered[1];
      const seq = last !== null && (n === last + 1 || n === last + 2);
      const restart = n === 1 && (last === null || cut === 'section');
      if (n <= 30 && (last === null || seq || restart) && l.x <= margin + 0.08 && !listSpaced(l) && cut !== 'text') start = { n: `Q${n}`, num: n };
      prevNumbered = l;
    } else if ((m = QUESTION_N.exec(t)) && !/\bis on the next page/i.test(t)) {
      const n = +m[1];
      const seq = last !== null && (n === last + 1 || n === last + 2);
      const restart = n === 1 && (last === null || cut === 'section');
      if (n <= 30 && (last === null || seq || restart)) start = { n: `Q${n}`, num: n };
    } else if (english && (m = QUESTION_LETTER.exec(t))) {
      start = { n: `Question ${m[1]}`, num: last };
    } else if (english && (m = TEXT_HEAD.exec(t)) && l.x < 0.16) {
      start = { n: m[1], num: last };
    }
    if (debug && (numbered || QUESTION_N.test(t) || QUESTION_LETTER.test(t) || TEXT_HEAD.test(t))) debug.push(`  ${start ? 'START' : '     '} p${l.pg} x${l.x.toFixed(3)} y${l.y.toFixed(2)} last=${last} cut=${cut} | ${t.slice(0, 70)}`);
    if (start) {
      close();
      cur = { n: start.n, pg: l.pg, lines: [] };
      last = start.num;
      cut = null;
      // the heading line's own words are question text ("3. The diagram shows the human alimentary canal.")
      const rest = t.replace(NUMBERED, '').replace(QUESTION_N, '').replace(QUESTION_LETTER, '').replace(/^\s*[–-]\s*\d+\s*Marks?/i, '').replace(/^\s*\(\d+\s*marks\)/i, '').trim();
      if (start.n.length === 1) { /* single-text head: the title is not a question */ }
      else if (rest && !isDrop({ ...l, text: rest })) cur.lines.push(rest);
      continue;
    }
    if (cut || !cur) continue;
    if (isDrop(l)) continue;
    cur.lines.push(t);
  }
  close();
  if (debug) console.log(`margin ${margin.toFixed(3)}\n` + debug.join('\n'));
  return qs.map(q => ({ n: q.n, pg: q.pg, text: capText(q.lines.join(' ').replace(/\s+/g, ' ').trim()) })).filter(q => q.text.length >= 20);
}

async function readPaper(file) {
  const task = pdfjs.getDocument({ data: new Uint8Array(fs.readFileSync(file)), verbosity: 0 });
  try {
    const doc = await task.promise;
    const pages = [];
    for (let n = 1; n <= doc.numPages; n++) {
      const pg = await doc.getPage(n);
      pages.push([n, await pageLines(pg)]);
      pg.cleanup();
    }
    return pages;
  } finally {
    await task.destroy();
  }
}

async function buildSubject(subjectId, name, INDEX, report) {
  const papers = [];
  const q = [];
  const entries = (INDEX[subjectId] || [])
    .filter(en => en.lang === 'ev' && en.year >= YEARS.from && en.year <= YEARS.to && LEVEL[en.level])
    .sort((a, b) => a.year - b.year || a.level.localeCompare(b.level));
  for (const en of entries) {
    for (const p of en.papers) {
      if (p.modified) continue;
      const file = path.join(CORPUS, String(en.year), p.doc.f);
      const label = paperLabel(p.label);
      if (!fs.existsSync(file)) { report.push({ subject: subjectId, year: en.year, level: en.level, paper: label, file: p.doc.f, problem: 'missing from corpus' }); continue; }
      let pages;
      try { pages = await readPaper(file); }
      catch (e) { report.push({ subject: subjectId, year: en.year, level: en.level, paper: label, file: p.doc.f, problem: `failed to parse: ${e.message}` }); continue; }
      if (process.env.ASK_DEBUG && process.env.ASK_DEBUG !== `${en.year}:${en.level}:${label}` && process.env.ASK_DEBUG !== `${en.year}:${en.level}`) continue;
      if (process.env.ASK_DEBUG) console.log(`\n### ${subjectId} ${en.year} ${en.level} ${label} ${p.doc.f}`);
      const qs = splitQuestions(pages, subjectId);
      if (!qs.length) { report.push({ subject: subjectId, year: en.year, level: en.level, paper: label, file: p.doc.f, problem: 'no questions found' }); continue; }
      const pi = papers.push({ y: en.year, l: LEVEL[en.level], p: label, f: p.doc.f }) - 1;
      for (const x of qs) q.push([pi, x.n, x.pg, x.text]);
    }
  }
  const years = Array.from(new Set(papers.map(p => p.y))).sort();
  return { id: subjectId, name, attributionName: ATTRIBUTION_NAME[subjectId] || name, years, papers, q };
}

const main = async () => {
  const only = process.argv.slice(2).filter(a => !a.startsWith('--'));
  const INDEX = loadIndex();
  const report = [];
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const index = fs.existsSync(path.join(OUT_DIR, 'index.json')) ? JSON.parse(fs.readFileSync(path.join(OUT_DIR, 'index.json'), 'utf8')) : { subjects: [] };
  let total = 0;
  for (const [id, name] of SUBJECTS) {
    if (only.length && !only.includes(id)) continue;
    const t0 = Date.now();
    const data = await buildSubject(id, name, INDEX, report);
    const out = path.join(OUT_DIR, `${id}.json`);
    fs.writeFileSync(out, JSON.stringify(data));
    const bytes = fs.statSync(out).size;
    total += bytes;
    const row = { id, name, file: `${id}.json`, questions: data.q.length, papers: data.papers.length, years: data.years, bytes };
    const i = index.subjects.findIndex(s => s.id === id);
    if (i >= 0) index.subjects[i] = row; else index.subjects.push(row);
    console.log(`${name.padEnd(10)} papers ${String(data.papers.length).padStart(3)}  questions ${String(data.q.length).padStart(5)}  years ${data.years[0]}–${data.years[data.years.length - 1]} (${data.years.length})  ${(bytes / 1024).toFixed(0)} KB  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  index.subjects.sort((a, b) => SUBJECTS.findIndex(s => s[0] === a.id) - SUBJECTS.findIndex(s => s[0] === b.id));
  index.years = Array.from(new Set(index.subjects.flatMap(s => s.years))).sort();
  index.built = new Date().toISOString().slice(0, 10);
  index.levels = LEVELS;
  index.cap = TEXT_CAP;
  fs.writeFileSync(path.join(OUT_DIR, 'index.json'), JSON.stringify(index));
  console.log(`total ${(index.subjects.reduce((n, s) => n + s.bytes, 0) / 1024).toFixed(0)} KB across ${index.subjects.length} subjects (this run wrote ${(total / 1024).toFixed(0)} KB)`);
  if (report.length) {
    console.log(`\n${report.length} paper(s) not indexed:`);
    for (const r of report) console.log(`  ${r.subject} ${r.year} ${r.level} ${r.paper || 'Exam Paper'} ${r.file}: ${r.problem}`);
  } else console.log('\nevery paper indexed');
};

main().catch(e => { console.error(e); process.exit(1); });
