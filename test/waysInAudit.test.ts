/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Ways In audit — what the planner makes of every card in the bank.
 *
 * Ways In shows a student the SHAPE of an answer before they attempt it: how
 * many pieces it needs, and what each piece is. It never shows the answer. So
 * the measure of a plan is not whether it is safe -- that is guaranteed by
 * construction -- but whether a student reading it learns anything about THIS
 * question they could not have guessed without it.
 *
 * Two rows reading "Response 1" and "Response 2" pass every existing test and
 * teach nothing. "Impact 1" and "Impact 2", against a paper printing "Outline
 * two positive impacts of globalisation", is the same frame doing its job.
 * This is how we tell those apart across the whole bank.
 */
import { writeFileSync } from 'node:fs';
import { describe, it } from 'vitest';
import { buildQuestionModel, COUNTED_UNIT_NOUNS } from '../components/WaysIn/questionModel';
import { CARDS as AGRICULTURAL_SCIENCE_HIGHER } from '../components/MarkBank/cards/agricultural-science/higher';
import { CARDS as AGRICULTURAL_SCIENCE_ORDINARY } from '../components/MarkBank/cards/agricultural-science/ordinary';
import { CARDS as ANCIENT_GREEK_HIGHER } from '../components/MarkBank/cards/ancient-greek/higher';
import { CARDS as ANCIENT_GREEK_ORDINARY } from '../components/MarkBank/cards/ancient-greek/ordinary';
import { CARDS as APPLIED_MATHS_HIGHER } from '../components/MarkBank/cards/applied-maths/higher';
import { CARDS as APPLIED_MATHS_ORDINARY } from '../components/MarkBank/cards/applied-maths/ordinary';
import { CARDS as ARABIC_HIGHER } from '../components/MarkBank/cards/arabic/higher';
import { CARDS as ARABIC_ORDINARY } from '../components/MarkBank/cards/arabic/ordinary';
import { CARDS as ART_HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as ART_ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import { CARDS as BIOLOGY_HIGHER } from '../components/MarkBank/cards/biology/higher';
import { CARDS as BIOLOGY_ORDINARY } from '../components/MarkBank/cards/biology/ordinary';
import { CARDS as BULGARIAN_HIGHER } from '../components/MarkBank/cards/bulgarian/higher';
import { CARDS as BUSINESS_HIGHER } from '../components/MarkBank/cards/business/higher';
import { CARDS as BUSINESS_ORDINARY } from '../components/MarkBank/cards/business/ordinary';
import { CARDS as CHEMISTRY_HIGHER } from '../components/MarkBank/cards/chemistry/higher';
import { CARDS as CHEMISTRY_ORDINARY } from '../components/MarkBank/cards/chemistry/ordinary';
import { CARDS as CLASSICAL_STUDIES_HIGHER } from '../components/MarkBank/cards/classical-studies/higher';
import { CARDS as CLASSICAL_STUDIES_ORDINARY } from '../components/MarkBank/cards/classical-studies/ordinary';
import { CARDS as COMPUTER_SCIENCE_HIGHER } from '../components/MarkBank/cards/computer-science/higher';
import { CARDS as COMPUTER_SCIENCE_ORDINARY } from '../components/MarkBank/cards/computer-science/ordinary';
import { CARDS as CONSTRUCTION_STUDIES_HIGHER } from '../components/MarkBank/cards/construction-studies/higher';
import { CARDS as CONSTRUCTION_STUDIES_ORDINARY } from '../components/MarkBank/cards/construction-studies/ordinary';
import { CARDS as CROATIAN_HIGHER } from '../components/MarkBank/cards/croatian/higher';
import { CARDS as CZECH_HIGHER } from '../components/MarkBank/cards/czech/higher';
import { CARDS as DANISH_HIGHER } from '../components/MarkBank/cards/danish/higher';
import { CARDS as DCG_HIGHER } from '../components/MarkBank/cards/dcg/higher';
import { CARDS as DCG_ORDINARY } from '../components/MarkBank/cards/dcg/ordinary';
import { CARDS as DUTCH_HIGHER } from '../components/MarkBank/cards/dutch/higher';
import { CARDS as ECONOMICS_HIGHER } from '../components/MarkBank/cards/economics/higher';
import { CARDS as ECONOMICS_ORDINARY } from '../components/MarkBank/cards/economics/ordinary';
import { CARDS as ENGINEERING_HIGHER } from '../components/MarkBank/cards/engineering/higher';
import { CARDS as ENGINEERING_ORDINARY } from '../components/MarkBank/cards/engineering/ordinary';
import { CARDS as ENGLISH_HIGHER } from '../components/MarkBank/cards/english/higher';
import { CARDS as ENGLISH_ORDINARY } from '../components/MarkBank/cards/english/ordinary';
import { CARDS as ESTONIAN_HIGHER } from '../components/MarkBank/cards/estonian/higher';
import { CARDS as FINNISH_HIGHER } from '../components/MarkBank/cards/finnish/higher';
import { CARDS as FRENCH_HIGHER } from '../components/MarkBank/cards/french/higher';
import { CARDS as FRENCH_ORDINARY } from '../components/MarkBank/cards/french/ordinary';
import { CARDS as GEOGRAPHY_HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as GEOGRAPHY_ORDINARY } from '../components/MarkBank/cards/geography/ordinary';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '../components/MarkBank/cards/german/ordinary';
import { CARDS as HISTORY_HIGHER } from '../components/MarkBank/cards/history/higher';
import { CARDS as HISTORY_ORDINARY } from '../components/MarkBank/cards/history/ordinary';
import { CARDS as HOME_ECONOMICS_HIGHER } from '../components/MarkBank/cards/home-economics/higher';
import { CARDS as HOME_ECONOMICS_ORDINARY } from '../components/MarkBank/cards/home-economics/ordinary';
import { CARDS as HUNGARIAN_HIGHER } from '../components/MarkBank/cards/hungarian/higher';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as IRISH_ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { CARDS as ITALIAN_HIGHER } from '../components/MarkBank/cards/italian/higher';
import { CARDS as ITALIAN_ORDINARY } from '../components/MarkBank/cards/italian/ordinary';
import { CARDS as JAPANESE_HIGHER } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as JAPANESE_ORDINARY } from '../components/MarkBank/cards/japanese/ordinary';
import { CARDS as LATIN_HIGHER } from '../components/MarkBank/cards/latin/higher';
import { CARDS as LATIN_ORDINARY } from '../components/MarkBank/cards/latin/ordinary';
import { CARDS as LATVIAN_HIGHER } from '../components/MarkBank/cards/latvian/higher';
import { CARDS as LCVP_COMMON } from '../components/MarkBank/cards/lcvp/common';
import { CARDS as LITHUANIAN_HIGHER } from '../components/MarkBank/cards/lithuanian/higher';
import { CARDS as LITHUANIAN_ORDINARY } from '../components/MarkBank/cards/lithuanian/ordinary';
import { CARDS as MALTESE_HIGHER } from '../components/MarkBank/cards/maltese/higher';
import { CARDS as MANDARIN_CHINESE_HIGHER } from '../components/MarkBank/cards/mandarin-chinese/higher';
import { CARDS as MANDARIN_CHINESE_ORDINARY } from '../components/MarkBank/cards/mandarin-chinese/ordinary';
import { CARDS as MATHS_HIGHER } from '../components/MarkBank/cards/maths/higher';
import { CARDS as MATHS_ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import { CARDS as MODERN_GREEK_HIGHER } from '../components/MarkBank/cards/modern-greek/higher';
import { CARDS as PHYSICAL_EDUCATION_HIGHER } from '../components/MarkBank/cards/physical-education/higher';
import { CARDS as PHYSICAL_EDUCATION_ORDINARY } from '../components/MarkBank/cards/physical-education/ordinary';
import { CARDS as PHYSICS_HIGHER } from '../components/MarkBank/cards/physics/higher';
import { CARDS as PHYSICS_ORDINARY } from '../components/MarkBank/cards/physics/ordinary';
import { CARDS as POLISH_HIGHER } from '../components/MarkBank/cards/polish/higher';
import { CARDS as POLISH_ORDINARY } from '../components/MarkBank/cards/polish/ordinary';
import { CARDS as PORTUGUESE_HIGHER } from '../components/MarkBank/cards/portuguese/higher';
import { CARDS as PORTUGUESE_ORDINARY } from '../components/MarkBank/cards/portuguese/ordinary';
import { CARDS as RELIGIOUS_EDUCATION_HIGHER } from '../components/MarkBank/cards/religious-education/higher';
import { CARDS as RELIGIOUS_EDUCATION_ORDINARY } from '../components/MarkBank/cards/religious-education/ordinary';
import { CARDS as ROMANIAN_HIGHER } from '../components/MarkBank/cards/romanian/higher';
import { CARDS as RUSSIAN_HIGHER } from '../components/MarkBank/cards/russian/higher';
import { CARDS as RUSSIAN_ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import { CARDS as SLOVAKIAN_HIGHER } from '../components/MarkBank/cards/slovakian/higher';
import { CARDS as SLOVENIAN_HIGHER } from '../components/MarkBank/cards/slovenian/higher';
import { CARDS as SPANISH_HIGHER } from '../components/MarkBank/cards/spanish/higher';
import { CARDS as SPANISH_ORDINARY } from '../components/MarkBank/cards/spanish/ordinary';
import { CARDS as SWEDISH_HIGHER } from '../components/MarkBank/cards/swedish/higher';
import { CARDS as TECHNOLOGY_HIGHER } from '../components/MarkBank/cards/technology/higher';
import { CARDS as TECHNOLOGY_ORDINARY } from '../components/MarkBank/cards/technology/ordinary';
import { CARDS as UKRAINIAN_HIGHER } from '../components/MarkBank/cards/ukrainian/higher';

type Deck = [string, string, readonly any[]];
const DECKS: Deck[] = [
['agricultural-science', 'higher', AGRICULTURAL_SCIENCE_HIGHER],
  ['agricultural-science', 'ordinary', AGRICULTURAL_SCIENCE_ORDINARY],
  ['ancient-greek', 'higher', ANCIENT_GREEK_HIGHER],
  ['ancient-greek', 'ordinary', ANCIENT_GREEK_ORDINARY],
  ['applied-maths', 'higher', APPLIED_MATHS_HIGHER],
  ['applied-maths', 'ordinary', APPLIED_MATHS_ORDINARY],
  ['arabic', 'higher', ARABIC_HIGHER],
  ['arabic', 'ordinary', ARABIC_ORDINARY],
  ['art', 'higher', ART_HIGHER],
  ['art', 'ordinary', ART_ORDINARY],
  ['biology', 'higher', BIOLOGY_HIGHER],
  ['biology', 'ordinary', BIOLOGY_ORDINARY],
  ['bulgarian', 'higher', BULGARIAN_HIGHER],
  ['business', 'higher', BUSINESS_HIGHER],
  ['business', 'ordinary', BUSINESS_ORDINARY],
  ['chemistry', 'higher', CHEMISTRY_HIGHER],
  ['chemistry', 'ordinary', CHEMISTRY_ORDINARY],
  ['classical-studies', 'higher', CLASSICAL_STUDIES_HIGHER],
  ['classical-studies', 'ordinary', CLASSICAL_STUDIES_ORDINARY],
  ['computer-science', 'higher', COMPUTER_SCIENCE_HIGHER],
  ['computer-science', 'ordinary', COMPUTER_SCIENCE_ORDINARY],
  ['construction-studies', 'higher', CONSTRUCTION_STUDIES_HIGHER],
  ['construction-studies', 'ordinary', CONSTRUCTION_STUDIES_ORDINARY],
  ['croatian', 'higher', CROATIAN_HIGHER],
  ['czech', 'higher', CZECH_HIGHER],
  ['danish', 'higher', DANISH_HIGHER],
  ['dcg', 'higher', DCG_HIGHER],
  ['dcg', 'ordinary', DCG_ORDINARY],
  ['dutch', 'higher', DUTCH_HIGHER],
  ['economics', 'higher', ECONOMICS_HIGHER],
  ['economics', 'ordinary', ECONOMICS_ORDINARY],
  ['engineering', 'higher', ENGINEERING_HIGHER],
  ['engineering', 'ordinary', ENGINEERING_ORDINARY],
  ['english', 'higher', ENGLISH_HIGHER],
  ['english', 'ordinary', ENGLISH_ORDINARY],
  ['estonian', 'higher', ESTONIAN_HIGHER],
  ['finnish', 'higher', FINNISH_HIGHER],
  ['french', 'higher', FRENCH_HIGHER],
  ['french', 'ordinary', FRENCH_ORDINARY],
  ['geography', 'higher', GEOGRAPHY_HIGHER],
  ['geography', 'ordinary', GEOGRAPHY_ORDINARY],
  ['german', 'higher', GERMAN_HIGHER],
  ['german', 'ordinary', GERMAN_ORDINARY],
  ['history', 'higher', HISTORY_HIGHER],
  ['history', 'ordinary', HISTORY_ORDINARY],
  ['home-economics', 'higher', HOME_ECONOMICS_HIGHER],
  ['home-economics', 'ordinary', HOME_ECONOMICS_ORDINARY],
  ['hungarian', 'higher', HUNGARIAN_HIGHER],
  ['irish', 'higher', IRISH_HIGHER],
  ['irish', 'ordinary', IRISH_ORDINARY],
  ['italian', 'higher', ITALIAN_HIGHER],
  ['italian', 'ordinary', ITALIAN_ORDINARY],
  ['japanese', 'higher', JAPANESE_HIGHER],
  ['japanese', 'ordinary', JAPANESE_ORDINARY],
  ['latin', 'higher', LATIN_HIGHER],
  ['latin', 'ordinary', LATIN_ORDINARY],
  ['latvian', 'higher', LATVIAN_HIGHER],
  ['lcvp', 'common', LCVP_COMMON],
  ['lithuanian', 'higher', LITHUANIAN_HIGHER],
  ['lithuanian', 'ordinary', LITHUANIAN_ORDINARY],
  ['maltese', 'higher', MALTESE_HIGHER],
  ['mandarin-chinese', 'higher', MANDARIN_CHINESE_HIGHER],
  ['mandarin-chinese', 'ordinary', MANDARIN_CHINESE_ORDINARY],
  ['maths', 'higher', MATHS_HIGHER],
  ['maths', 'ordinary', MATHS_ORDINARY],
  ['modern-greek', 'higher', MODERN_GREEK_HIGHER],
  ['physical-education', 'higher', PHYSICAL_EDUCATION_HIGHER],
  ['physical-education', 'ordinary', PHYSICAL_EDUCATION_ORDINARY],
  ['physics', 'higher', PHYSICS_HIGHER],
  ['physics', 'ordinary', PHYSICS_ORDINARY],
  ['polish', 'higher', POLISH_HIGHER],
  ['polish', 'ordinary', POLISH_ORDINARY],
  ['portuguese', 'higher', PORTUGUESE_HIGHER],
  ['portuguese', 'ordinary', PORTUGUESE_ORDINARY],
  ['religious-education', 'higher', RELIGIOUS_EDUCATION_HIGHER],
  ['religious-education', 'ordinary', RELIGIOUS_EDUCATION_ORDINARY],
  ['romanian', 'higher', ROMANIAN_HIGHER],
  ['russian', 'higher', RUSSIAN_HIGHER],
  ['russian', 'ordinary', RUSSIAN_ORDINARY],
  ['slovakian', 'higher', SLOVAKIAN_HIGHER],
  ['slovenian', 'higher', SLOVENIAN_HIGHER],
  ['spanish', 'higher', SPANISH_HIGHER],
  ['spanish', 'ordinary', SPANISH_ORDINARY],
  ['swedish', 'higher', SWEDISH_HIGHER],
  ['technology', 'higher', TECHNOLOGY_HIGHER],
  ['technology', 'ordinary', TECHNOLOGY_ORDINARY],
  ['ukrainian', 'higher', UKRAINIAN_HIGHER]
];

// The labels the planner falls back on when it has learned nothing about the
// question. A plan made only of these is one a student could have written
// without reading the paper at all.
const GENERIC = new Set([
  'Response', 'Direct response', 'Main reason or claim', 'Relevant information',
  'Link to the question', 'Point', 'Step',
]);

const strip = (label: string) => label.replace(/\s+\d+$/, '').trim();

// A count the PAPER prints, read the way the bank reads every other number:
// off the page, in words or digits, in front of the thing being counted.
const WORD_NUMBER: Record<string, number> = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6,
  seven: 7, eight: 8, nine: 9, ten: 10,
};
// The number has to be COUNTING something, not naming it. "calf 3", "cow 1 or
// 2" and "lactation 3 and 4" all put a digit beside a noun and count nothing,
// which is the same trap the planner's own allowlist exists to avoid — so the
// number must come FIRST, its noun must be plural, and the word in front of it
// must not be the thing being identified.
const IDENTIFIED = new Set([
  'calf', 'cow', 'sample', 'question', 'part', 'figure', 'table', 'page',
  'diagram', 'graph', 'year', 'lactation', 'site', 'plot', 'tube', 'stage',
  'day', 'week', 'month', 'section', 'line', 'row', 'column', 'point',
  'text', 'source', 'extract', 'passage', 'image', 'film', 'chapter',
]);
const COUNT_PHRASE = new RegExp(
  String.raw`(^|[^a-z])(one|two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+`
  + String.raw`((?:[a-z-]+\s+){0,2})([a-z]{3,}s)\b`, 'gi');

function printedCounts(text: string): { n: number; noun: string }[] {
  const out: { n: number; noun: string }[] = [];
  const words = (text || '').toLowerCase().split(/[^a-z0-9]+/);
  for (const m of (text || '').matchAll(COUNT_PHRASE)) {
    const raw = m[2].toLowerCase();
    const n = WORD_NUMBER[raw] ?? Number(raw);
    if (!Number.isFinite(n) || n < 1 || n > 12) continue;
    const at = words.indexOf(raw);
    if (at > 0 && IDENTIFIED.has(words[at - 1])) continue;
    // "the seven animals", "these two samples" — a definite article in front
    // means the number is naming what is already on the page, not asking for
    // that many answers. The planner refuses these and is right to; the
    // auditor has to refuse them too or it reports the planner's correct
    // behaviour as a defect.
    if (at > 0 && ['the', 'these', 'those', 'both', 'all'].includes(words[at - 1])) continue;
    const noun = m[4].toLowerCase();
    // The planner's own unit list decides, so the auditor cannot report a
    // "missed count" the planner is right to refuse. Without this it called
    // "every 3 - 5 years", "carry out the test three times" and "the seven
    // animals" missed counts, which is the very trap the allowlist exists for.
    if (COUNTED_UNIT_NOUNS.has(noun)) continue;
    out.push({ n, noun });
  }
  return out;
}

export interface Defect {
  subject: string; level: string; id: string; ref: string;
  kind: string; detail: string; question: string;
}

// The counted-answer checks read ENGLISH. A modern-language paper sets its
// questions in its own language, where a word ending in "s" is not a plural and
// a number in front of it counts nothing an English pattern can see —
// Lithuanian "dalis" is the singular for "part", and it alone accounted for 142
// reported misses. Those subjects need their own reading and get no claim here.
const ENGLISH_MEDIUM = new Set([
  'agricultural-science', 'applied-maths', 'art', 'biology', 'business',
  'chemistry', 'classical-studies', 'computer-science', 'construction-studies',
  'dcg', 'economics', 'engineering', 'english', 'geography', 'history',
  'home-economics', 'lcvp', 'maths', 'physical-education', 'physics',
  'politics-and-society', 'religious-education', 'technology',
]);

export function auditCard(subject: string, level: string, card: any): Defect[] {
  const model = buildQuestionModel({
    id: card.id, origin: 'mark-bank', subjectLabel: subject,
    questionRef: card.questionRef, questionText: card.questionText,
    stem: card.stem, textConfidence: 'verified', sourceLabel: 'SEC',
    answerShape: { totalMarks: card.totalMarks },
  } as any);
  const q: string = card.questionText || '';
  const out: Defect[] = [];
  const base = (kind: string, detail: string): Defect => ({
    subject, level, id: card.id, ref: card.questionRef,
    question: q.slice(0, 160), kind, detail,
  });

  const labels = model.planPrompts.map((p) => strip(p.label));
  const allGeneric = labels.length > 0 && labels.every((l) => GENERIC.has(l));
  // A count inside ONE sub-part says nothing about the whole question's shape.
  // Geography sets "(i) Name each of the landforms labelled A, B, C and D.
  // (ii) Name two specific processes..." and the plan rightly has a row per
  // numbered part; comparing the "two" from part (ii) against that reported 95
  // correct plans as defects. Where the question prints its own sub-parts, the
  // instructions are the shape and this check has nothing to say.
  const hasSubParts = (q.match(/\((?:i{1,3}|iv|v|vi{0,3})\)/gi) ?? []).length > 1;
  const counts = ENGLISH_MEDIUM.has(subject) && !hasSubParts ? printedCounts(q) : [];
  const named = counts.find((c) => c.n > 1);

  if (named && allGeneric) {
    out.push(base('generic-label-where-paper-names-it',
      `paper says "${named.n} ${named.noun}", plan says "${labels[0]}"`));
  }
  if (named && model.planShape.count !== named.n) {
    out.push(base('count-missed',
      `paper prints ${named.n} ${named.noun}, plan has ${model.planShape.count} row(s)`));
  }
  // NOT a defect: a question with one job, planned as one row. "Name one
  // water-soluble vitamin" needs one box and a frame that says so is right.
  // Counting those as failures was this auditor's own mistake and it put
  // 8,917 correct plans in the report — the tool has to be honest about what
  // it is measuring or it sends whoever reads it after the wrong 56%.
  const oneJob = model.planKind === 'direct' && labels.length === 1;
  if (!named && allGeneric && model.planShape.basis === 'flexible' && !oneJob) {
    out.push(base('fixed-scaffold-regardless-of-question',
      `${model.planKind} / ${labels.length} generic row(s), same on every such card`));
  }
  // Only where the items are actually THERE. "Identify each of the following
  // breeds of animals." prints its items as pictures, and the card titled
  // "Q18(a) Soil quality" covers one item of a list set out elsewhere — in
  // both the planner is right to keep one row, and calling that a flattened
  // list reports the planner's correct behaviour as a fault.
  // "Choose ONE of the following: • Castletown House" is a choice already made
  // — the card covers the one option — and "the following data ... Trial 1: 62,
  // Trial 2: 59" is data, not a set of jobs. One row is right for both, so
  // neither is a flattened list.
  const choiceOfOne = /\b(?:choose|select|answer)\s+(?:any\s+)?one\b/i.test(q);
  const dataList = /following\s+data\b/i.test(q);
  const colon = (choiceOfOne || dataList) ? -1 : q.search(/\bfollowing\b[^:]{0,80}:/i);
  const afterColon = colon >= 0 ? q.slice(q.indexOf(':', colon) + 1).trim() : '';
  const looksLikeItems = afterColon.length > 0 && /[;,]/.test(afterColon);
  if (looksLikeItems && model.planShape.count <= 1) {
    out.push(base('list-flattened',
      `question prints its items and the plan has ${model.planShape.count} row(s)`));
  }
  return out;
}

describe('Ways In: what the planner makes of the whole bank', () => {
  it('reports every plan that teaches a student nothing about its question', () => {
    const lines: string[] = [];
    const say = (t: string) => { lines.push(t); };
    const defects: Defect[] = [];
    let cards = 0;
    for (const [subject, level, deck] of DECKS) {
      for (const card of deck) {
        cards += 1;
        defects.push(...auditCard(subject, level, card));
      }
    }
    const byKind = new Map<string, number>();
    for (const d of defects) byKind.set(d.kind, (byKind.get(d.kind) ?? 0) + 1);
    const touched = new Set(defects.map((d) => d.id)).size;

    say(`\ncards audited: ${cards}`);
    say(`cards with at least one defect: ${touched} (${(100 * touched / cards).toFixed(1)}%)\n`);
    for (const [kind, n] of [...byKind].sort((a, b) => b[1] - a[1])) {
      say(`  ${String(n).padStart(6)}  ${kind}`);
    }
    const bySubject = new Map<string, number>();
    for (const d of defects) bySubject.set(d.subject, (bySubject.get(d.subject) ?? 0) + 1);
    say('\nworst subjects:');
    for (const [s, n] of [...bySubject].sort((a, b) => b[1] - a[1]).slice(0, 12)) {
      say(`  ${String(n).padStart(6)}  ${s}`);
    }
    say('\nexamples:');
    for (const kind of byKind.keys()) {
      const e = defects.find((d) => d.kind === kind)!;
      say(`  [${kind}] ${e.ref}`);
      say(`      Q: ${e.question.slice(0, 110)}`);
      say(`      ${e.detail}`);
    }
    writeFileSync('tmp/waysin-audit.txt', lines.join('\n') + '\n');
    writeFileSync('tmp/waysin-audit.json', JSON.stringify(defects, null, 1));
    console.log(lines.join('\n'));
  }, 600_000);
});
