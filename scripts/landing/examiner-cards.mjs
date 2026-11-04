/**
 * Landing page — "Answer like an examiner" data.
 *
 *   node scripts/landing/examiner-cards.mjs
 *
 * Writes components/landing/fx-d/examinerData.ts from the Mark Bank card
 * files (components/MarkBank/cards/<subject>/<level>.ts). Nothing here is
 * typed: every question, every marking point, every mark and every line of a
 * possible response is read from a card whose content was itself transcribed
 * from the SEC paper and marking scheme and gated at build time. This script
 * only SELECTS cards, adds accept alternatives the scheme itself allows, and
 * cuts prose responses at the scheme's own headings and sentence ends —
 * and it refuses to write anything that is not a substring of its source row.
 *
 * Subjects for "Mark my answer" were chosen by survey (scripts run 2026-09-08):
 * cards whose rows are all point-style with short verbatim lines — Physics
 * (385 such cards at Higher), Biology (169), Chemistry (133), Agricultural
 * Science (134) and Business (35 at Ordinary). Home Economics and Economics
 * are anyN-heavy; Geography has no question cards.
 */

import { buildSync } from 'esbuild';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT = path.join(ROOT, 'components/landing/fx-d/examinerData.ts');
/** esbuild's bundles of the card files, loaded and thrown away. */
const TMP = path.join(os.tmpdir(), 'landing-examiner');

const LABEL = {
  biology: 'Biology',
  chemistry: 'Chemistry',
  physics: 'Physics',
  'agricultural-science': 'Agricultural Science',
  business: 'Business',
  economics: 'Economics',
};

/* ── "Mark my answer": four cards per subject ──────────────────────────────
   Every card: kind 'question', rows all kind 'point' with numeric marks that
   sum to the printed tariff, no authored content. */
const MARK = [
  ['biology', ['bio-2025-hl-q1-a', 'bio-2025-hl-q3-a', 'bio-2025-hl-q4-c', 'bio-2024-hl-q14-c-ii']],
  ['chemistry', ['chem-2021-hl-q11-c-iii', 'chem-2021-hl-q4-a', 'chem-2021-hl-q11-c-ii', 'chem-2021-hl-q11-d-b-ii']],
  ['physics', ['phys-2022-hl-q7-i', 'phys-2021-hl-q7-i', 'phys-2022-hl-q6-k', 'phys-2022-hl-q7-v']],
  ['agricultural-science', ['agsci-2021-hl-q7a', 'agsci-2021-hl-q8a', 'agsci-2021-hl-q9a', 'agsci-2021-hl-q10a']],
  ['business', ['bus-2025-ol-s1-q1', 'bus-2021-ol-s2-q5di', 'bus-2024-ol-s2-q2aii', 'bus-2024-ol-s2-q4d']],
];

/* ── Accept alternatives ────────────────────────────────────────────────────
   The marker (components/landing/marking/marker.ts) earns a point when most
   of the scheme line's content words appear. Where the line is a formula, a
   number with its unit or a one-word answer, the words alone are the wrong
   test, so these points get explicit alternatives: each inner list is a set
   of tokens that must all be present. RULE: only what the scheme itself
   prints, or the same thing written differently. Never wider than the scheme.
   Keyed by card id, then row id. */
const ACCEPT = {
  // Printed with subscripts, flattened by extraction; n for x and y is the same general formula.
  'bio-2025-hl-q1-a': { 'r-formula': [['Cx(H2O)y'], ['Cn(H2O)n']] },
  // The scheme's own bracketed alternatives: "Nucleic acid (or DNA or RNA)".
  'bio-2024-hl-q14-c-ii': { __byVerbatim: { 'Nucleic acid (or DNA or RNA)': [['nucleic acid'], ['DNA'], ['RNA']] } },
  // "zero" and the numeral are the same answer.
  'phys-2022-hl-q7-v': { __byVerbatim: { zero: [['zero'], ['0']] } },
  // The scheme prints "Safety/Security" — its solidus lists alternatives. "Self Actualisation" hyphenated is the same word.
  'bus-2021-ol-s2-q5di': { __byVerbatim: { '2: Safety/Security': [['safety'], ['security']], '5: Self Actualisation': [['self actualisation'], ['self-actualisation'], ['self actualization'], ['self-actualization']] } },
  // "Primary" for "Primary Sector" is the sector named; nothing else scores.
  'bus-2024-ol-s2-q2aii': { __byVerbatim: { 'Primary Sector': [['primary']], 'Tertiary Sector': [['tertiary']] } },
  // The scheme prints the initials in brackets: "(CCPC)".
  'bus-2024-ol-s2-q4d': { __byVerbatim: { 'Competition and Consumer Protection Commission (CCPC).': [['competition', 'consumer', 'protection', 'commission'], ['CCPC']] } },
};

/* ── Possible responses with marks per point ───────────────────────────────
   Business and Economics schemes print a prose "possible response" under
   each point with the point's tariff beside it. `labelSep` is the scheme's
   own separator between the point's name and its response; `splitBefore`
   adds a line break the scheme prints (the example on its own line). */
const WANTS = [
  { id: 'bus-2021-hl-s3-q8b', labelSep: ': ' },                    // Idea Generation / Product Screening / Concept Development / Feasibility Study — 4@5(2+3)
  { id: 'bus-2024-hl-s1-q6', labelSep: ': ' },                     // Embargo / Quota — 2@5(3+2)
  { id: 'econ-2022-hl-q13-a-ii', labelSep: ' are ', keepSep: true, splitBefore: [' e.g.,'] }, // Direct taxes / Indirect taxes — (6 + 2) + (6 + 2)
];
// Strengths / Weaknesses / Opportunities / Threats — 4@5(2+3). One line per point (`joinLines`): a chip lands on the whole response that earns it.
const PLACE = { id: 'bus-2025-hl-s3-q5b', labelSep: ': ', joinLines: true };

/* ── Load the card files ────────────────────────────────────────────────── */
mkdirSync(TMP, { recursive: true });
const loaded = new Map();
const load = async (subject, level) => {
  const key = `${subject}-${level}`;
  if (loaded.has(key)) return loaded.get(key);
  const entry = path.join(ROOT, 'components/MarkBank/cards', subject, `${level}.ts`);
  const r = buildSync({ entryPoints: [entry], bundle: true, format: 'esm', platform: 'node', write: false, absWorkingDir: ROOT, logLevel: 'silent' });
  const file = path.join(TMP, `${key}.mjs`);
  writeFileSync(file, r.outputFiles[0].text);
  const cards = (await import(pathToFileURL(file).href)).CARDS ?? [];
  loaded.set(key, cards);
  return cards;
};
const find = async (id) => {
  for (const subject of Object.keys(LABEL)) for (const level of ['higher', 'ordinary']) {
    const c = (await load(subject, level)).find(x => x.id === id);
    if (c) return c;
  }
  throw new Error(`card not found: ${id}`);
};

const levelName = (c) => (c.level === 'higher' ? 'Higher' : 'Ordinary');
const attribution = (c) => `SEC Leaving Certificate ${LABEL[c.subjectId]} ${c.year} ${levelName(c)} Level — © State Examinations Commission`;

const pngSize = (src) => {
  const buf = readFileSync(path.join(ROOT, 'public', src));
  if (buf.readUInt32BE(12) !== 0x49484452) throw new Error(`not a PNG: ${src}`);
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
};

const gateCard = (c, ids) => {
  if (c.kind !== 'question') throw new Error(`${c.id}: not a question card`);
  if (c.authored) throw new Error(`${c.id}: authored content is not scheme content`);
  for (const r of c.rows) {
    if (r.kind !== 'point') throw new Error(`${c.id}: row ${r.id} is ${r.kind}, not point`);
    if (typeof r.marks !== 'number') throw new Error(`${c.id}: row ${r.id} has no marks`);
  }
  const sum = c.rows.reduce((n, r) => n + r.marks, 0);
  if (sum !== c.totalMarks) throw new Error(`${c.id}: rows sum to ${sum}, paper says ${c.totalMarks}`);
  if (ids && ids.length !== 4) throw new Error(`${c.subjectId}: need four cards, got ${ids.length}`);
};

const acceptFor = (c, r) => {
  const table = ACCEPT[c.id];
  if (!table) return undefined;
  const byV = table.__byVerbatim?.[r.verbatim];
  const byId = table[r.id];
  return byV ?? byId;
};

/* ── Build "Mark my answer" ─────────────────────────────────────────────── */
const markSubjects = [];
for (const [subject, ids] of MARK) {
  const questions = [];
  for (const id of ids) {
    const c = await find(id);
    gateCard(c, ids);
    if (c.subjectId !== subject) throw new Error(`${id} is not ${subject}`);
    const used = new Set();
    const points = c.rows.map(r => {
      const accept = acceptFor(c, r);
      if (accept) used.add(r.verbatim);
      return { id: r.id, verbatim: r.verbatim, marks: r.marks, ...(accept ? { accept } : {}) };
    });
    const table = ACCEPT[c.id];
    if (table) {
      for (const k of Object.keys(table)) if (k !== '__byVerbatim' && !c.rows.some(r => r.id === k)) throw new Error(`${c.id}: no row ${k} (rows: ${c.rows.map(r => r.id).join(', ')})`);
      for (const k of Object.keys(table.__byVerbatim ?? {})) if (!used.has(k)) throw new Error(`${c.id}: no row printed as "${k}"`);
    }
    questions.push({
      id: c.id, subject: LABEL[subject], ref: c.questionRef, year: c.year, level: levelName(c),
      ...(c.stem ? { stem: c.stem } : {}),
      question: c.questionText,
      ...(c.figure ? { figure: { src: c.figure.src, alt: c.figure.alt, ...pngSize(c.figure.src) } } : {}),
      points, total: c.totalMarks, attribution: attribution(c),
    });
  }
  markSubjects.push({ id: subject, label: LABEL[subject], questions });
}

/* ── Build the possible responses ──────────────────────────────────────── */
const SENTENCE = /(?<=[.?!])\s+(?=[A-Z(])/;
const tariffOf = (c, marks) => {
  const notation = c.tariffModel?.notation ?? '';
  const m = notation.match(/\(([\d\s+]+)\)/);
  return m ? `${marks} (${m[1].replace(/\s+/g, '').split('+').join(' + ')})` : String(marks);
};
const buildResponse = async (cfg) => {
  const c = await find(cfg.id);
  gateCard(c);
  const points = [];
  const lines = [];
  c.rows.forEach((r, i) => {
    const at = r.verbatim.indexOf(cfg.labelSep);
    if (at <= 0) throw new Error(`${c.id}: row ${r.id} has no "${cfg.labelSep}" heading`);
    const label = r.verbatim.slice(0, at);
    let rest = r.verbatim.slice(cfg.keepSep ? 0 : at + cfg.labelSep.length).trim();
    for (const s of cfg.splitBefore ?? []) rest = rest.split(s).join(`\n${s.trim()}`);
    const pieces = cfg.joinLines ? [rest] : rest.split('\n').flatMap(p => p.split(SENTENCE)).map(s => s.trim()).filter(Boolean);
    for (const piece of pieces) if (!r.verbatim.includes(piece)) throw new Error(`${c.id}: "${piece}" is not in the scheme row`);
    if (!r.verbatim.startsWith(label)) throw new Error(`${c.id}: label "${label}" is not the row's own heading`);
    const pid = `p${i + 1}`;
    points.push({ id: pid, label, marks: r.marks, tariff: tariffOf(c, r.marks) });
    pieces.forEach((text, j) => lines.push({ id: `${pid}-l${j + 1}`, text, pointId: pid }));
  });
  return {
    id: c.id, subject: LABEL[c.subjectId], ref: c.questionRef, year: c.year, level: levelName(c),
    ...(c.stem ? { stem: c.stem } : {}),
    question: c.questionText, notation: c.tariffModel?.notation ?? '',
    points, lines, total: c.totalMarks, attribution: attribution(c),
  };
};
const wants = [];
for (const cfg of WANTS) wants.push(await buildResponse(cfg));
const place = await buildResponse(PLACE);
if (WANTS.some(w => w.id === PLACE.id)) throw new Error('"Mark one yourself" must be a different question from "What the examiner wants"');

/* ── Write ─────────────────────────────────────────────────────────────── */
const j = (v) => JSON.stringify(v, null, 2);
const out = `/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * GENERATED by scripts/landing/examiner-cards.mjs — do not edit by hand.
 *
 * Every question is verbatim from the SEC paper and every point, mark and
 * line of a possible response verbatim from the SEC marking scheme, read from
 * the gated Mark Bank card files. Accept alternatives are the scheme's own or
 * the same thing written differently, and are listed with their reasons in
 * the script. Attribute as printed on each item.
 */

import type { MarkPoint } from '../marking/marker';

export interface ExamFigure { src: string; alt: string; width: number; height: number }

export interface MarkQuestion {
  id: string;
  subject: string;
  ref: string;
  year: number;
  level: 'Higher' | 'Ordinary';
  stem?: string;
  question: string;
  figure?: ExamFigure;
  points: MarkPoint[];
  total: number;
  attribution: string;
}

export interface MarkSubject { id: string; label: string; questions: MarkQuestion[] }

/** A scheme point named in a possible response, with the tariff the scheme prints beside it. */
export interface ResponsePoint { id: string; label: string; marks: number; tariff: string }
/** One line of the scheme's possible response and the point it earns. */
export interface ResponseLine { id: string; text: string; pointId: string }

export interface ResponseQuestion {
  id: string;
  subject: string;
  ref: string;
  year: number;
  level: 'Higher' | 'Ordinary';
  stem?: string;
  question: string;
  /** The tariff notation as the scheme prints it, e.g. "4 x 5m (2+3)". */
  notation: string;
  points: ResponsePoint[];
  lines: ResponseLine[];
  total: number;
  attribution: string;
}

/** "Mark my answer": five subjects, four questions each. */
export const MARK_SUBJECTS: MarkSubject[] = ${j(markSubjects)};

/** "What the examiner wants": full-marks answers, line by line, each line mapped to its point. */
export const WANTS: ResponseQuestion[] = ${j(wants)};

/** "Mark one yourself": a different question, its points to be placed on its own response lines. */
export const PLACE: ResponseQuestion = ${j(place)};
`;
writeFileSync(OUT, out);
console.log(`wrote ${path.relative(ROOT, OUT)}: ${markSubjects.length} subjects × 4 questions, ${wants.length} wants, 1 place`);
for (const s of markSubjects) for (const q of s.questions) console.log(`  ${q.id.padEnd(26)} ${String(q.total).padStart(2)}m  ${q.points.length} pt${q.figure ? '  fig' : ''}${q.points.some(p => p.accept) ? '  accept' : ''}`);
for (const w of [...wants, place]) console.log(`  ${w.id.padEnd(26)} ${String(w.total).padStart(2)}m  ${w.points.length} pt  ${w.lines.length} lines  ${w.notation}`);
