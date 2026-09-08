/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Today's Question — build the pool of short, point-style questions the
 * landing page serves one of per day.
 *
 * Reads the authored Mark Bank card files (components/MarkBank/cards/<subject>/
 * <level>.ts — every question and marking point in them is transcribed from
 * the SEC paper and marking scheme and gated on build), keeps the cards a
 * visitor can answer in a few words, and writes public/assets/landing/today/
 * pool.json. Nothing here is typed: the question text, the scheme's points,
 * their marks, the scheme's own printed alternatives and the figure path all
 * come off the card. The pool order is a seeded shuffle so consecutive days
 * change subject; the page picks pool[(day - epoch) mod length].
 *
 * Usage: node scripts/landing/today-pool.mjs [--stats]
 */

import fs from 'node:fs';
import path from 'node:path';
import esbuild from 'esbuild';
import { prng } from './lib.mjs';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const CARDS = path.join(ROOT, 'components', 'MarkBank', 'cards');
const OUT = path.join(ROOT, 'public', 'assets', 'landing', 'today', 'pool.json');
const STATS = process.argv.includes('--stats');
const WHY = (process.argv.find(a => a.startsWith('--why=')) || '').slice(6);

/** No subject takes more than this many places, so the year is not all Biology. */
const PER_SUBJECT = 60;

/** Subjects with point-style cards and the name the attribution line prints. */
const SUBJECTS = {
  'biology': 'Biology',
  'chemistry': 'Chemistry',
  'physics': 'Physics',
  'economics': 'Economics',
  'business': 'Business',
  'agricultural-science': 'Agricultural Science',
  'home-economics': 'Home Economics',
  'engineering': 'Engineering',
};
const LEVELS = { higher: 'Higher Level', ordinary: 'Ordinary Level' };

/** Bundle one card module (TypeScript, type-only imports) and import it. */
const loadCards = async (file) => {
  const r = await esbuild.build({ entryPoints: [file], bundle: true, format: 'esm', platform: 'node', write: false, logLevel: 'silent' });
  const mod = await import(`data:text/javascript;base64,${Buffer.from(r.outputFiles[0].text).toString('base64')}`);
  return mod.CARDS || [];
};

const words = (s) => s.trim().split(/\s+/).filter(Boolean);
/** The scheme's bracketed text is an elaboration; the words outside are the answer. */
const outsideBrackets = (s) => s.replace(/\([^)]*\)/g, ' ').replace(/\s+/g, ' ').trim();

/** A question that points at something the visitor cannot see. */
const NEEDS_CONTEXT = /\b(above|below|following|shown|diagram|table|graph|figure|extract|passage|chart|image|photograph|map|this experiment|the experiment|the investigation|the data|the results|the circuit|the apparatus|the reaction above|in the box|labelled|label)\b/i;
/** Question text the pool should not carry: multi-part prompts and instructions. */
const NOT_A_QUESTION = /\b(answer any|answer all|in each case|each of the following|the following questions|tick|underline|underlined|italic|in bold|highlighted|circle|draw|sketch|plot|calculate|show that|construct|complete the|fill in|match|modify|for each|true or false|he|she|they|his|her|their|you named|you have named|your answer)\b/i;
/** A question opens like a question: a question mark, or one of the paper's command words. */
const ASKS = /^(Name|State|Give|Write|Define|Identify|Explain|Outline|Suggest|What|Which|Why|How|Where|When|List|Describe|Distinguish|Mention|Say|Indicate|In what|To which|To what|From what|By what|Of what|Under what|At what|Is |Are |Do |Does |Can )/;
const COUNT_WORDS = { two: 2, three: 3, four: 4, five: 5 };

const shortRow = (r) => {
  if (!r || typeof r.verbatim !== 'string' || typeof r.marks !== 'number' || r.marks <= 0 || r.marks > 6) return false;
  const main = outsideBrackets(r.verbatim);
  // An open list of one term ("Deflation.") is a term, not a list; a longer open list is a slice of the scheme.
  if (r.openList && (words(main).length > 2 || r.accepts?.length)) return false;
  if (!main || words(main).length > 4 || main.length > 48) return false;
  if (/[:;]/.test(main)) return false;
  if (/^(or|and|etc)\b/i.test(main) || /\b(or|etc)\.?$/i.test(main)) return false;   // a fragment of a longer line
  if (/^(true|false|yes|no)$/i.test(main)) return false;                            // a true/false item, not an answer
  if (r.kind !== 'alt' && /\bor\b|\//i.test(main)) return false;                    // alternatives printed on a point row
  if (r.kind === 'point' || r.kind === 'gate') return true;
  if (r.kind === 'alt') return Array.isArray(r.accepts) && r.accepts.every(a => typeof a === 'string' && words(a).length <= 3 && a.length <= 32);
  return false;
};

const pointFor = (r) => {
  const p = { id: r.id, verbatim: r.verbatim, marks: r.marks };
  if (r.kind === 'alt' && r.accepts?.length) {
    // The scheme's own alternatives, each one enough on its own: the line's
    // words outside the brackets, then every printed "or" alternative.
    p.accept = [[outsideBrackets(r.verbatim)], ...r.accepts.map(a => [outsideBrackets(a)])];
  }
  return p;
};

const why = (c) => {
  if (c.source !== 'sec' || c.kind !== 'question') return 'not a question card';
  if (!c.questionText || typeof c.questionText !== 'string') return 'no question text';
  const q = c.questionText.trim();
  if (q.length < 18 || q.length > 150) return 'length';
  if (!/[?.]$/.test(q)) return 'no terminal punctuation';
  if (NOT_A_QUESTION.test(q)) return 'not a question';
  if (c.figure?.solution) return 'solution figure';
  if (!c.figure && NEEDS_CONTEXT.test(q)) return 'needs context';
  // "Name tube A" / "What is X?" — a lettered thing the visitor cannot see.
  if (!c.figure && /(^|[^A-Za-z])[A-HX-Z]([^A-Za-z]|$)/.test(q.replace(/\b(I|A)\b(?=\s+[a-z])/g, ''))) return 'lettered reference';
  if (!c.figure && /\b(this|these|it|its|the student|the candidate|the sample|the solution|the mixture|the crystal)\b/i.test(q)) return 'pronoun/context';
  if (c.figure && !(c.figure.src && c.figure.alt && c.figure.attribution)) return 'figure incomplete';
  if (c.figure && !fs.existsSync(path.join(ROOT, 'public', c.figure.src))) return 'figure file missing';
  if (!(q.endsWith('?') || ASKS.test(q))) return 'row count';
  if (!Array.isArray(c.rows) || c.rows.length < 1 || c.rows.length > 3) return 'row not short';
  if (!c.rows.every(shortRow)) return 'not a question';
  // "Identify three …" with one row: the card carries a slice of the scheme, not the answer.
  const asked = Math.max(0, ...Object.entries(COUNT_WORDS).filter(([w]) => new RegExp(`\\b${w}\\b`, 'i').test(q)).map(([, n]) => n));
  if (asked > c.rows.length) return 'count asked > rows';
  // A point whose words are already in the question is a heading, not an answer.
  const qWords = new Set(words(q.toLowerCase().replace(/[^a-z0-9\s-]/g, ' ')));
  if (c.rows.some(r => { const w = words(outsideBrackets(r.verbatim).toLowerCase().replace(/[^a-z0-9\s-]/g, ' ')); return w.length && w.every(x => qWords.has(x)); })) return 'point already in question';
  // Two rows sharing an accepted alternative would both score for one word.
  const seenAlt = new Set();
  for (const r of c.rows) for (const a of (r.kind === 'alt' ? [outsideBrackets(r.verbatim), ...(r.accepts || [])] : [])) { const k = a.toLowerCase(); if (seenAlt.has(k)) return 'shared alternative'; seenAlt.add(k); }
  if (c.tariffModel?.kind !== 'fixed') return 'tariff not fixed';
  const sum = c.rows.reduce((n, r) => n + r.marks, 0);
  if (sum !== c.totalMarks) return 'marks do not sum';
  if (!c.year || !LEVELS[c.level] || !c.questionRef || !c.schemeCitation) return 'missing metadata';
  return null;
};
const qualifies = (c) => why(c) === null;


const entryFor = (c, subjectId) => {
  const subject = SUBJECTS[subjectId];
  const level = LEVELS[c.level];
  const e = {
    id: c.id,
    subject,
    year: c.year,
    level,
    ref: c.questionRef,
    question: c.questionText.trim(),
    points: c.rows.map(pointFor),
    attribution: `SEC Leaving Certificate ${subject} ${c.year} ${level} — © State Examinations Commission`,
  };
  if (c.figure) e.figure = { src: c.figure.src, alt: c.figure.alt, attribution: c.figure.attribution };
  return e;
};

const main = async () => {
  const pool = [];
  const stats = [];
  for (const subjectId of Object.keys(SUBJECTS)) {
    for (const level of Object.keys(LEVELS)) {
      const file = path.join(CARDS, subjectId, `${level}.ts`);
      if (!fs.existsSync(file)) continue;
      const cards = await loadCards(file);
      if (WHY === subjectId) {
        const hist = {};
        for (const c of cards) { const r = why(c) || 'KEPT'; hist[r] = (hist[r] || 0) + 1; if (r !== 'KEPT' && c.questionText && c.questionText.length < 150 && (c.rows || []).every(x => typeof x.verbatim === 'string' && x.verbatim.length <= 40) && (c.rows || []).length <= 3) console.log(`  ${level} ${r}: ${c.questionRef} ${c.questionText} => ${(c.rows || []).map(x => x.kind + ' ' + x.marks + 'm ' + JSON.stringify(x.verbatim)).join(' | ')} total ${c.totalMarks} tariff ${c.tariffModel?.kind}`); }
        console.log(level, JSON.stringify(hist));
      }
      const kept = cards.filter(qualifies);
      stats.push({ subject: subjectId, level, cards: cards.length, kept: kept.length, figures: kept.filter(c => c.figure).length });
      for (const c of kept) pool.push(entryFor(c, subjectId));
    }
  }
  // One entry per paper part, then at most PER_SUBJECT per subject, taken
  // evenly across the years so a subject's places are not all one paper.
  const seen = new Set();
  const dedup = pool.filter(e => { const k = `${e.subject}|${e.year}|${e.level}|${e.ref}`; if (seen.has(k)) return false; seen.add(k); return true; });
  const unique = [];
  for (const subject of new Set(dedup.map(e => e.subject))) {
    const mine = dedup.filter(e => e.subject === subject);
    const byPaper = new Map();
    for (const e of mine) { const k = `${e.year}|${e.level}`; if (!byPaper.has(k)) byPaper.set(k, []); byPaper.get(k).push(e); }
    const lanes = Array.from(byPaper.values());
    for (let round = 0; unique.filter(e => e.subject === subject).length < PER_SUBJECT; round++) {
      let took = false;
      for (const lane of lanes) { if (lane[round]) { unique.push(lane[round]); took = true; if (unique.filter(e => e.subject === subject).length >= PER_SUBJECT) break; } }
      if (!took) break;
    }
  }
  // Seeded shuffle: the same input always writes the same order, so #N is stable.
  const rand = prng(20260901);
  for (let i = unique.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [unique[i], unique[j]] = [unique[j], unique[i]]; }
  if (STATS) {
    for (const s of stats) console.log(`${s.subject.padEnd(22)} ${s.level.padEnd(9)} cards ${String(s.cards).padStart(4)}  kept ${String(s.kept).padStart(4)}  with figure ${s.figures}`);
    const bySubject = {}; for (const e of unique) bySubject[e.subject] = (bySubject[e.subject] || 0) + 1;
    console.log('pool', unique.length, bySubject);
    console.log('bytes', JSON.stringify(unique).length);
    return;
  }
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify({ built: new Date().toISOString().slice(0, 10), count: unique.length, entries: unique }));
  console.log(`wrote ${unique.length} entries to ${path.relative(ROOT, OUT)} (${fs.statSync(OUT).size} bytes)`);
};

main().catch(e => { console.error(e); process.exit(1); });
