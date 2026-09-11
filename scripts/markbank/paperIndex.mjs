/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — read Paper Trail's harvested paper index.
 *
 * The SEC file id of the paper a card came from is RESOLVED from this index,
 * never typed by an author. The first Biology build defaulted the field to a
 * literal instead, and that literal turned out to be the id of the marking
 * SCHEME — so 1,104 cards would have deep-linked a student straight to the
 * answers. One implementation lives here so the build script and the test that
 * polices it cannot drift apart.
 */

import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

/** Paper Trail's index, keyed by subject id. */
export const paperIndex = (() => {
  const text = readFileSync(resolve(ROOT, 'paperTrailData.ts'), 'utf8');
  const start = text.indexOf('{', text.indexOf('export const PAPER_TRAIL_INDEX'));
  if (start < 0) throw new Error('PAPER_TRAIL_INDEX not found in paperTrailData.ts');

  // The literal is JSON apart from TypeScript's trailing commas, and its strings
  // hold prose that could contain a brace — so scan with string awareness rather
  // than counting braces blind, and drop trailing commas as we go.
  let depth = 0, inString = false, escaped = false;
  const kept = [];
  let pendingComma = -1;
  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      kept.push(ch);
      continue;
    }
    if (ch === '"') { inString = true; pendingComma = -1; }
    else if (ch === '{' || ch === '[') { depth++; pendingComma = -1; }
    else if (ch === '}' || ch === ']') {
      if (pendingComma >= 0) { kept[pendingComma] = ''; pendingComma = -1; }
      depth--;
    } else if (ch === ',') pendingComma = kept.length;
    else if (!/\s/.test(ch)) pendingComma = -1;
    kept.push(ch);
    if (depth === 0) return JSON.parse(kept.join(''));
  }
  throw new Error('PAPER_TRAIL_INDEX is not closed in paperTrailData.ts');
})();

/**
 * Where the Mark Bank's subject id is not the corpus's key for the same subject.
 *
 * Paper Trail files Home Economics under the syllabus's full name, and the deck
 * calls it what the app calls it. Nothing warned about the mismatch — the lookup
 * simply found nothing, resolvePaperFileid returned its honest null, and all 569
 * Home Economics cards shipped with no link to the paper they came from.
 */
const CORPUS_KEY = {
  'home-economics': 'home-economics-s-and-s',
  'maths': 'mathematics',
  // The corpus files LCVP's written paper under the module it examines.
  'lcvp': 'link-modules',
  // The corpus spells the subject out; the deck uses the SEC's own short name,
  // which is what students call it. Without this every Applied Maths card
  // shipped with no link to the paper it came from — the Home Economics
  // failure above, repeated.
  'applied-maths': 'applied-mathematics',
  // The corpus spells the subject out; the deck uses the abbreviation the SEC
  // prints on the paper and students use. Without this every DCG card would
  // ship with no link to the booklet it came from -- the Home Economics
  // failure above, repeated.
  dcg: 'design-and-communication-graphics',
};

/**
 * The corpus key for a card, where a SUBJECT is examined as two papers a
 * candidate chooses between.
 *
 * History is sat in one of two FIELDS OF STUDY, Later Modern and Early Modern.
 * The SEC prints them as separate papers under separate subject codes — 004
 * and 096 — and Paper Trail indexes them as two subjects, while Mark Bank
 * ships one deck whose citations name the field. Resolving an Early Modern
 * card against 'history' hands it the Later Modern paper: a real document, the
 * wrong one, and the student is deep-linked to questions they never sat.
 *
 * Exported so the build and the deck test resolve identically; they had
 * separate ideas of the corpus key once already (CORPUS_KEY below exists
 * because 569 Home Economics cards shipped with no paper link at all).
 */
export const corpusSubjectFor = (subjectId, questionRef) =>
  (subjectId === 'history' && /\bEarly Modern\b/.test(String(questionRef ?? ''))
    ? 'history-early-modern'
    : subjectId);

/** The sitting of one subject, year and level in its authored paper language. */
export const paperEntry = (subjectId, year, level) =>
  (paperIndex[CORPUS_KEY[subjectId] ?? subjectId] ?? [])
    .find(e => e.year === year && e.level === level
      && e.lang === (subjectId === 'irish' ? 'iv' : 'ev'));

/**
 * The sections a paper's label covers: "Section A&B" -> {A, B}, "Section 2 & 3"
 * -> {2, 3}.
 *
 * Business numbers its sections instead of lettering them, and it splits across
 * two documents — Section 1 in one, the ABQ and long questions in the other. Read
 * only the letters and every Business card resolves to null, deep-linking a
 * student to nothing. Anchored on the word "Section" so that "Paper Two" and
 * "Practical Test Day 1" cannot be mistaken for section numbers.
 */
const labelCovers = (label) => {
  const text = String(label);
  const covered = new Set();
  if (/\bsection\b/i.test(text)) {
    for (const token of text.match(/\b[ABC1-9]\b/g) ?? []) covered.add(token);
  }
  // English and several language subjects name their documents "Paper One"
  // and "Paper Two" rather than "Section 1" and "Section 2". Mark Bank uses
  // those same numeric section ids, so treating the labels as unknowable left
  // every English card with a null paper link even though Paper Trail had the
  // exact document. Keep this anchored on the word Paper so a stray number in a
  // practical-test label cannot become a false section match.
  const paper = text.match(/\bpaper\s+(one|two|[1-9])\b/i)?.[1]?.toLowerCase();
  if (paper) covered.add(paper === 'one' ? '1' : paper === 'two' ? '2' : paper);
  // Geography names its two written documents "Part 1" and "Part 2".  They
  // are separate PDFs (042 and 043), so leaving Part unrecognised makes every
  // Geography card resolve to null even though Paper Trail holds both exact
  // documents.  Keep this anchored just as tightly as Paper/Section above.
  const part = text.match(/\bpart\s+(one|two|[1-9])\b/i)?.[1]?.toLowerCase();
  if (part) covered.add(part === 'one' ? '1' : part === 'two' ? '2' : part);
  return covered;
};

const stripPdf = (f) => (f ? String(f).replace(/\.pdf$/, '') : null);

/**
 * A companion document that carries READING MATTER only, and no questions.
 *
 * Spanish prints its Section B article on a two-page LOOSE SHEET with its own
 * SEC file id (LC012ALP015EV), and Paper Trail indexes it as a paper labelled
 * "Section B". It is not a question document: every Section B question is
 * printed in the Exam Paper, and the sheet holds the article alone. Left
 * unnamed here, labelCovers() reads "Section B" as a section match, so every
 * Spanish Section B card would deep-link to the article WITHOUT its questions
 * while Sections A and C resolved to null — a real document, the wrong one,
 * which is the failure this whole module exists to prevent.
 *
 * The sheet is still bound where it belongs: those cards set
 * sourceMaterial.sourceFileid, resolved by resolveCompanionFileid below.
 */
const TEXT_ONLY_COMPANION = {
  // "Section B" is the only such label the index carries for Spanish, across
  // all seventeen years of it. Named exactly, not as a pattern over A-C: a
  // companion labelled "Section A" would be a different document with a
  // different relationship to the questions, and guessing at one that does not
  // exist is how the wrong booklet gets bound.
  spanish: /^Section B$/i,
};

/**
 * The file id of a NAMED companion document — an illustration booklet, a loose
 * text sheet — or null.
 *
 * Null rather than a guess, and null unless the label names exactly ONE
 * document in that sitting: a card whose source cannot be resolved is dropped
 * by the build rather than pointed at whichever paper happened to be first.
 */
/**
 * The COMPONENT token inside an SEC file id: LC008ALP004BV.pdf is component
 * 004. '000' is the question paper itself; anything else is a companion
 * booklet — Paper X, an illustration sheet, a listening test.
 *
 * The id is the SEC's own structured name for the document. The label beside
 * it in the index is harvested prose, and it is sometimes simply wrong:
 * Classical Studies 2024 Ordinary indexes its Paper X as "Exam Paper", beside
 * the real exam paper, because the SEC published that file with a four-digit
 * typo in its name (LC008GLP0004BV.pdf). With two documents both labelled
 * "Exam Paper" the label logic below can identify neither, so every 2024
 * Ordinary card lost the illustration booklet its question is about — and
 * thirteen correct cards were dropped for it.
 *
 * Used only where the LABELS cannot decide, and only when the components do:
 * exactly one document with component '000' and every other with something
 * else. That is evidence from the id, not a guess about the label.
 */
const componentOf = (f) => {
  const m = /^LC\d{3}[ACG]LP(\d{3,4})[EIB]V/i.exec(String(f ?? ''));
  if (!m) return null;
  const token = m[1];
  return token.length === 4 && token.startsWith('0') ? token.slice(1) : token;
};

/**
 * The one document in this sitting whose id says it IS (or is not) the
 * question paper — but ONLY where the labels have already failed completely.
 *
 * "Failed completely" means every document in the sitting carries the SAME
 * label, so no label distinguishes anything. Anything weaker and this would
 * answer a question the labels have already answered differently: asked for
 * Art's "Section B", which Art does not publish, a looser rule handed back the
 * illustration booklet — a real document, the wrong one, which is the failure
 * resolveCompanionFileid returns null to prevent.
 */
const byComponent = (papers, want) => {
  if (papers.length !== 2) return null;
  const labels = new Set(papers.map(p => String(p.label).trim().toLowerCase()));
  if (labels.size !== 1) return null;
  const components = papers.map(p => componentOf(p.doc?.f));
  if (components.some(c => c === null)) return null;
  const hits = papers.filter((_, i) => (components[i] === '000') === want);
  return hits.length === 1 ? hits[0] : null;
};

export function resolveCompanionFileid(subjectId, year, level, label) {
  const entry = paperEntry(subjectId, year, level);
  const want = String(label ?? '').trim().toLowerCase();
  if (!want || !entry?.papers?.length) return null;
  const hits = entry.papers.filter(p => String(p.label).trim().toLowerCase() === want);
  if (hits.length === 1) return stripPdf(hits[0].doc?.f);
  // The labels could not name one document. Where the file ids can — one
  // question paper and one companion — the companion is the one the id says
  // is not the question paper.
  const companion = byComponent(entry.papers, false);
  if (companion && byComponent(entry.papers, true)) {
    return stripPdf(companion.doc?.f);
  }
  return null;
}

/**
 * The file id of the QUESTION PAPER holding a card's section, or null.
 *
 * Null rather than a guess: a wrong id sends a student to the wrong document,
 * and for the section-split subjects the nearest wrong answer is the scheme.
 */
export function resolvePaperFileid(subjectId, year, level, section) {
  const entry = paperEntry(subjectId, year, level);
  if (!entry?.papers?.length) return null;
  // One paper for the year means there is nothing to choose between.
  if (entry.papers.length === 1) return stripPdf(entry.papers[0].doc?.f);
  // Art's separate illustration booklet is indexed as a second "paper" even
  // though every written section lives in the document explicitly labelled
  // Exam Paper. Treating both documents as section candidates made every Art
  // card resolve to null. This is safe only when that label is unique and all
  // siblings identify themselves as picture/illustration companions.
  // The same shape covers the modern languages, whose second document is the
  // Listening Comprehension Test: French indexes "Exam Paper" beside "Aural
  // Paper", neither of which names a section, so every French card resolved to
  // null and every reading card lost the passage it quotes. A listening card
  // would need the aural document, and no listening card exists — the ask
  // cannot be answered from print, and the deck excludes it.
  const namedExamPapers = entry.papers.filter(p => /^Exam Paper$/i.test(p.label));
  const companions = entry.papers.filter(p => !/^Exam Paper$/i.test(p.label));
  const textOnly = TEXT_ONLY_COMPANION[subjectId];
  if (namedExamPapers.length === 1 && companions.length > 0
      && companions.every(p => /picture|illustration|aural|listening/i.test(p.label)
        || (textOnly && textOnly.test(p.label)))) {
    return stripPdf(namedExamPapers[0].doc?.f);
  }
  const direct = entry.papers.find(p => labelCovers(p.label).has(section));
  if (direct) return stripPdf(direct.doc?.f);
  // The 2022 Irish OL Paper 1 is labelled only "Exam Paper" in the SEC index,
  // beside an explicitly labelled Paper Two.  The sole unnumbered sibling is
  // therefore Paper 1; this evidence-based fallback stays null for ambiguous
  // multi-document entries.
  const unnumbered = entry.papers.filter(p => labelCovers(p.label).size === 0);
  if (section === '1' && unnumbered.length === 1
      && entry.papers.some(p => labelCovers(p.label).has('2'))) {
    return stripPdf(unnumbered[0].doc?.f);
  }
  // No label named a section and none identified a companion. The file ids
  // still can, where exactly one of the two documents is component '000'.
  const paper = byComponent(entry.papers, true);
  if (paper && byComponent(entry.papers, false)) return stripPdf(paper.doc?.f);
  return null;
}
