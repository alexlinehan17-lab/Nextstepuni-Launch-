/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Sit the paper — lift what each hall paper's cover prints off the actual
 * SEC PDF, so the exam hall never types a sitting, a duration or an
 * instruction of its own.
 *
 * For each of the six papers the Subjects stack shows (the same sittings as
 * components/landing/fx-c/papers.ts; the corpus fileids come from
 * paperTrailData.ts) the script reads the PDF from the Paper Trail corpus,
 * takes the cover's text lines, and keeps:
 *   sitting       the printed day-and-time line ("WEDNESDAY, 21 JUNE –
 *                 MORNING, 9:30 TO 12:30"); where the cover splits it over
 *                 two lines (Construction Studies) they are joined by a space
 *   minutes       the length of the sitting, end time minus start time, from
 *                 that line — the only arithmetic in the file
 *   marks         the printed marks line, as printed
 *   instructions  the cover's own instruction lines, wrapped lines rejoined;
 *                 where the cover prints none (Maths, Economics, Irish) the
 *                 paper's printed "Instructions" / "Treoracha" block on the
 *                 next pages, with the page it came from
 * Boilerplate that is not an instruction (the "Do not hand this up" trio and
 * the examination-number box) is dropped by an explicit list. Nothing is
 * rephrased: every string in the output is a run of the PDF's own text.
 *
 * Writes components/landing/fx-j/covers.ts (what the page imports) and
 * public/assets/landing/hall/covers.json (the same lift with every raw cover
 * line kept, for checking against the PDF).
 *
 * Usage: node scripts/landing/hall-cover.mjs [--print]
 *   PAPER_TRAIL_CORPUS overrides the corpus directory.
 */

import fs from 'node:fs';
import path from 'node:path';
import { getDocument } from 'pdfjs-dist/legacy/build/pdf.mjs';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const CORPUS = process.env.PAPER_TRAIL_CORPUS || '/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/exampapers';
const OUT_TS = path.join(ROOT, 'components', 'landing', 'fx-j', 'covers.ts');
const OUT_JSON = path.join(ROOT, 'public', 'assets', 'landing', 'hall', 'covers.json');
const PRINT = process.argv.includes('--print');

/** The six hall papers: the ids of components/landing/fx-c/papers.ts, and their corpus files. */
const PAPERS = [
  { id: 'physics', year: 2023, file: 'LC021ALP000EV.pdf' },
  { id: 'english', year: 2025, file: 'LC002ALP100EV.pdf' },
  { id: 'maths', year: 2025, file: 'LC003ALP100EV.pdf' },
  { id: 'construction-studies', year: 2023, file: 'LC029ALP000EV.pdf' },
  { id: 'irish', year: 2022, file: 'LC001GLP000IV.pdf' },
  { id: 'economics', year: 2024, file: 'LC034ALP000EV.pdf' },
];

/** A start-and-end time as the covers print it: "9:30 TO 12:30", "9.30 – 12.20", "2:00 - 4:30". */
const TIME_RANGE = /(\d{1,2})[:.](\d{2})\s*(?:TO|to|–|—|-)\s*(\d{1,2})[:.](\d{2})/;
const DAY_NAME = /\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Dé Luain|Dé Máirt|Dé Céadaoin|Déardaoin|Dé hAoine|Dé Sathairn)\b/i;
const MARKS_LINE = /^(?:Total Marks:\s*\d{2,3}|\(?\d{2,3}\s+(?:marks|marc)\)?)$/i;
/** Lines on a cover that are not instructions: the return notice and the examination-number box. */
const BOILERPLATE = [
  /^Do not hand this up\.?$/i,
  /^This document will not be returned to the$/i,
  /^State Examinations Commission\.?$/i,
  /^Examination Number$/i, /^Scrúduimhir$/i,
  /^Date of Birth$/i, /^Lá agus Mí do Bhreithe$/i,
  /^Centre Stamp$/i, /^Stampa an Ionaid$/i,
  /^For example, /i, /is entered as/i, /^Scríobh 3 Feabhra/i, /^mar shampla$/i,
];
const INSTRUCTIONS_HEADING = /^(Instructions|Treoracha)$/;
const INSTRUCTIONS_END = /make and model of your calculator/i;
/** A line that opens a new item however the line above it ends. */
const MARKER = /^(•|\([a-z]\)|N\.B\.)/;
/** A line that is complete without a full stop: a tariff row ("Section A: 100 marks", "Cuid I An Chluastuiscint 60 marc"). */
const COMPLETE = /\d+\s+(marks|marc|questions)$/i;
/** Two printed lines closer than this (points) are lines of one paragraph. */
const PARAGRAPH_GAP = 20;
/** The running footer sits below this. */
const FOOTER_Y = 70;

/** The text lines of a page, top to bottom, with their baselines: items grouped by y, ordered by x, a space where the print leaves one. */
const pageLines = async (page) => {
  const tc = await page.getTextContent();
  const items = tc.items
    .filter(i => typeof i.str === 'string' && i.str.trim())
    .map(i => ({ str: i.str, x: i.transform[4], y: i.transform[5], w: i.width }))
    .sort((a, b) => b.y - a.y || a.x - b.x);
  const lines = [];
  for (const it of items) {
    const last = lines[lines.length - 1];
    if (last && Math.abs(last.y - it.y) < 3) last.items.push(it); else lines.push({ y: it.y, items: [it] });
  }
  return lines.map(l => {
    const sorted = l.items.sort((a, b) => a.x - b.x);
    let text = '';
    let end = null;
    for (const it of sorted) {
      if (end !== null && it.x - end > 1.2 && !/\s$/.test(text) && !/^\s/.test(it.str)) text += ' ';
      text += it.str;
      end = it.x + it.w;
    }
    return { y: l.y, text: text.replace(/\s+/g, ' ').trim() };
  }).filter(l => l.text);
};

/** Rejoin lines the printer wrapped: a lower-case start, a comma before it, or an unfinished line above, within a paragraph's leading. */
const joinWrapped = (lines) => {
  const items = [];
  let prevY = null;
  for (const l of lines) {
    const prev = items[items.length - 1];
    const gap = prevY === null ? Infinity : prevY - l.y;
    const continues = prev !== undefined && gap <= PARAGRAPH_GAP && !MARKER.test(l.text) && (
      /^[a-záéíóú]/.test(l.text) || /[,;]$/.test(prev) || (/[A-Za-záéíóúÁÉÍÓÚ)]$/.test(prev) && !COMPLETE.test(prev))
    );
    if (continues) items[items.length - 1] = `${prev} ${l.text}`; else items.push(l.text);
    prevY = l.y;
  }
  return items;
};

/** Minutes between the two clock times of a sitting line; afternoon hours are printed on the twelve-hour clock. */
const minutesOf = (sitting) => {
  const m = TIME_RANGE.exec(sitting);
  if (!m) throw new Error(`no time range in "${sitting}"`);
  let start = Number(m[1]) * 60 + Number(m[2]);
  let end = Number(m[3]) * 60 + Number(m[4]);
  if (Number(m[1]) < 8) start += 12 * 60;
  if (Number(m[3]) < 8 || end <= start) end += 12 * 60;
  const minutes = end - start;
  if (minutes < 60 || minutes > 240) throw new Error(`implausible sitting of ${minutes} minutes in "${sitting}"`);
  return minutes;
};

const lift = async (paper) => {
  const file = path.join(CORPUS, String(paper.year), paper.file);
  const doc = await getDocument({ url: file, useSystemFonts: true, disableFontFace: true, verbosity: 0 }).promise;
  const cover = await pageLines(await doc.getPage(1));
  const timeAt = cover.findIndex(l => TIME_RANGE.test(l.text));
  if (timeAt < 0) throw new Error(`${paper.id}: no sitting time on the cover`);
  // A cover that puts the day on one line and the time on the next (Construction Studies).
  const splitDay = !DAY_NAME.test(cover[timeAt].text) && timeAt > 0 && DAY_NAME.test(cover[timeAt - 1].text);
  const sitting = splitDay ? `${cover[timeAt - 1].text} ${cover[timeAt].text}` : cover[timeAt].text;
  const marksLine = cover.find(l => MARKS_LINE.test(l.text));
  const marks = marksLine ? marksLine.text : null;
  const coverBody = cover.slice(timeAt + 1).filter(l => l !== marksLine && !BOILERPLATE.some(re => re.test(l.text)));
  let instructions = joinWrapped(coverBody);
  let instructionsPage = 1;
  if (!instructions.length) {
    for (let n = 2; n <= Math.min(3, doc.numPages) && !instructions.length; n++) {
      const lines = await pageLines(await doc.getPage(n));
      const at = lines.findIndex(l => INSTRUCTIONS_HEADING.test(l.text));
      if (at < 0) continue;
      const block = [];
      for (const l of lines.slice(at + 1)) {
        if (l.y < FOOTER_Y || INSTRUCTIONS_END.test(l.text)) break;
        block.push(l);
      }
      instructions = joinWrapped(block);
      instructionsPage = n;
    }
  }
  if (!instructions.length) throw new Error(`${paper.id}: no instructions found on the cover or the two pages after it`);
  await doc.cleanup();
  return { id: paper.id, year: paper.year, file: paper.file, sitting, minutes: minutesOf(sitting), marks, instructions, instructionsPage, coverLines: cover.map(l => l.text) };
};

const covers = [];
for (const p of PAPERS) covers.push(await lift(p));

if (PRINT) {
  for (const c of covers) {
    console.log(`\n== ${c.id}  ${c.year}/${c.file}`);
    console.log(`   sitting: ${c.sitting}  → ${c.minutes} min`);
    console.log(`   marks:   ${c.marks}`);
    console.log(`   instructions (page ${c.instructionsPage}):`);
    for (const i of c.instructions) console.log(`     - ${i}`);
  }
}

const q = (s) => JSON.stringify(s);
const ts = [
  '/**',
  ' * @license',
  ' * SPDX-License-Identifier: Apache-2.0',
  ' *',
  ' * GENERATED by scripts/landing/hall-cover.mjs — do not edit by hand.',
  ' *',
  ' * What each hall paper\'s cover prints, lifted off the SEC PDF in the Paper',
  ' * Trail corpus: the sitting line as printed, its length in minutes (end time',
  ' * minus start time), the marks line as printed, and the paper\'s own',
  ' * instructions — the cover\'s where it has them, otherwise the printed',
  ' * "Instructions" / "Treoracha" block on the page given. Nothing here is typed.',
  ' */',
  '',
  'export interface HallCover {',
  '  /** The StackPaper id in ../fx-c/papers.ts. */',
  '  id: string;',
  '  year: number;',
  '  /** The SEC fileid the text was lifted from. */',
  '  file: string;',
  '  /** The day-and-time line as the cover prints it. */',
  '  sitting: string;',
  '  /** The sitting\'s length: end time minus start time, from that line. */',
  '  minutes: number;',
  '  /** The marks line as printed, where the cover prints one. */',
  '  marks: string | null;',
  '  /** The paper\'s printed instructions, one item per printed paragraph or bullet. */',
  '  instructions: string[];',
  '  /** The page the instructions were printed on: 1 is the cover. */',
  '  instructionsPage: number;',
  '}',
  '',
  'export const HALL_COVERS: Record<string, HallCover> = {',
  ...covers.map(c => [
    `  ${q(c.id)}: {`,
    `    id: ${q(c.id)},`,
    `    year: ${c.year},`,
    `    file: ${q(c.file)},`,
    `    sitting: ${q(c.sitting)},`,
    `    minutes: ${c.minutes},`,
    `    marks: ${c.marks === null ? 'null' : q(c.marks)},`,
    `    instructions: [`,
    ...c.instructions.map(i => `      ${q(i)},`),
    `    ],`,
    `    instructionsPage: ${c.instructionsPage},`,
    `  },`,
  ].join('\n')),
  '};',
  '',
].join('\n');
fs.writeFileSync(OUT_TS, ts);
fs.mkdirSync(path.dirname(OUT_JSON), { recursive: true });
fs.writeFileSync(OUT_JSON, JSON.stringify({ built: new Date().toISOString().slice(0, 10), corpus: 'paper-trail-corpus/exampapers', papers: covers }, null, 2) + '\n');
console.log(`wrote ${path.relative(ROOT, OUT_TS)} and ${path.relative(ROOT, OUT_JSON)}: ${covers.length} covers`);
