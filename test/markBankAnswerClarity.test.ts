/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Answer clarity: a scheme answer the student can score must be a claimable
 * row showing the answer and its marks, never prose a student has to read to
 * find it. Alex, 2026-10-23, on Geography cards whose whole scheme sat as grey
 * text over one 0–30 slider: "the marking scheme answers should always be
 * clear to students! Not buried in blocks of text, set that as a rule when
 * making mark bank cards."
 *
 * Two kinds of defect, counted per subject:
 *  - a rubric criterion whose guidance prose carries a priced answer
 *    ("(i) … 6.1 ⟨3m⟩", "• German — 5 Marks", "Oifigeach = 2 mharc") instead
 *    of a row the student can claim;
 *  - a point row that is only a tariff ("Phase named") or that welds several
 *    answers into one string the student cannot claim one at a time.
 *
 * The numbers below are the state of each deck when the rule was set. Each
 * subject's conversion PR brings its number down and pins the new one; a
 * number may never go up. Geography is converted: its rows are structured by
 * cards/geography/allocation.ts, and the cards it cannot structure are pinned
 * by shape so a fix to one shape is visible.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as GEOGRAPHY_HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as GEOGRAPHY_ORDINARY } from '../components/MarkBank/cards/geography/ordinary';
import { FRENCH_LISTENING_CARDS } from '../components/MarkBank/cards/french/listening';
import { FRENCH_READING_CARDS } from '../components/MarkBank/cards/french/reading';
import { FRENCH_CLOZE_CARDS } from '../components/MarkBank/cards/french/cloze';
import irish from '../components/MarkBank/cards/irish/authored.json';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as IRISH_ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import politics from '../components/MarkBank/cards/politics-and-society/authored.json';
import physicalEducation from '../components/MarkBank/cards/physical-education/reviewed.json';
import art from '../components/MarkBank/cards/art/authored.json';
import { isRubricCard } from '../types/markBank';

type Guided = { rubric?: { answerGuide?: string[]; schemeGuidance?: string[]; criteria?: Array<{ guidance?: string[]; permittedMarks?: number[]; guidanceKind?: string; rowMarks?: number[] }> }; criteria?: Array<{ guidance?: string[]; guidanceKind?: string; rowMarks?: number[] }> };

const cardsOf = (deck: unknown): Guided[] => Array.isArray(deck) ? deck as Guided[] : (deck as { cards: Guided[] }).cards;

/** A line that prints an answer with its price, in any of the schemes' notations. */
const PRICED_ANSWER = /(?:⟨\s*\d+\s*m(?:\s*\+\s*\d+\s*m)*\s*⟩|[—–-]\s*\d+\s*Marks?\s*$|=\s*\d+\s*mharc|\b\d+\s*m\s*$|\b\d+\s*marks?\s*$)/i;

const pricedProseLines = (deck: unknown, pick: (card: Guided) => string[][]): number =>
  cardsOf(deck).reduce((count, card) =>
    count + pick(card).flat().filter(line => PRICED_ANSWER.test(line) && !/\bSRP/i.test(line) && !/^Total\b/i.test(line)).length, 0);

describe('answer clarity: priced answers are rows, not prose', () => {
  it('Geography: every structured card reconciles and lifts its words from the scheme or the paper', () => {
    const cards = [...GEOGRAPHY_HIGHER, ...GEOGRAPHY_ORDINARY].filter(isRubricCard);
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
    const structured = cards.filter(card => card.rubric.system === 'geography' && card.rubric.criteria[0].allocation);
    for (const card of structured) {
      if (card.rubric.system !== 'geography') continue;
      const criterion = card.rubric.criteria[0];
      const allocation = criterion.allocation!;
      const corpus = normalise([...criterion.guidance, card.questionText].join(' '));
      let total = 0;
      for (const group of allocation.groups) {
        const times = group.repeat?.count ?? 1;
        for (const row of group.rows) {
          expect(row.text.length, `${card.id}: empty row`).toBeGreaterThan(0);
          expect(corpus.includes(normalise(row.text)), `${card.id}: row "${row.text}" is not lifted`).toBe(true);
          expect(row.marks, card.id).toBeGreaterThan(0);
          for (const step of row.steps ?? []) expect(step, card.id).toBeLessThanOrEqual(row.marks);
          total += row.marks * times;
        }
        for (const srp of group.srp) {
          expect(corpus.includes(normalise(srp.label)), `${card.id}: SRP label "${srp.label}" is not lifted`).toBe(true);
          if (srp.min === undefined) total += srp.count * srp.marks * times;
        }
        if (group.prompt) expect(corpus.includes(normalise(group.prompt)), `${card.id}: prompt is not lifted`).toBe(true);
      }
      if (allocation.srpPool) total += allocation.srpPool.count * allocation.srpPool.marks;
      expect(total, `${card.id}: rows add to ${total}`).toBe(card.totalMarks);
      for (const note of allocation.directions) {
        expect(corpus.includes(normalise(note)), `${card.id}: direction "${note.slice(0, 40)}" is not lifted`).toBe(true);
      }
    }
    expect(structured).toHaveLength(639);

    // What is still prose, by shape. Fix a shape and lower its number here.
    const fallback = cards.filter(card => card.rubric.system === 'geography' && !card.rubric.criteria[0].allocation);
    const shape = (card: typeof fallback[number]) => {
      if (card.rubric.system !== 'geography') return 'other';
      const lines = card.rubric.criteria[0].guidance;
      if (card.level === 'higher' && /Q(?:1[3-9]|2[0-4])\b/.test(card.questionRef)) return 'HL 80-mark option: aspects + Overall Coherence';
      if (lines.some(line => /Vertical axis/.test(line))) return 'HL graph-drawing table';
      return 'other';
    };
    const byShape: Record<string, string[]> = {};
    for (const card of fallback) (byShape[shape(card)] ??= []).push(card.id);
    expect(Object.fromEntries(Object.entries(byShape).map(([key, ids]) => [key, ids.length]))).toEqual({
      'HL 80-mark option: aspects + Overall Coherence': 95,
      'HL graph-drawing table': 12,
      other: 8,
    });
    // Part One tables whose two columns were read across into one line by the
    // scheme reader (geography_cards.py part_one_scheme). A row-by-row read of
    // the PDF table is the fix; until then they stay prose.
    expect(byShape.other.sort()).toEqual([
      'geography-2021-ol-p1-q2',
      'geography-2021-ol-p1-q3',
      'geography-2022-ol-p1-q2',
      'geography-2022-ol-p1-q3',
      'geography-2023-ol-p1-q2',
      'geography-2025-hl-p1-q10',
      'geography-2025-hl-p1-q4',
      'geography-2025-hl-p1-q6',
    ]);
  });

  it('French: every structured card reconciles and lifts its words from the scheme; the rest is pinned by shape', () => {
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9àâäéèêëîïôöùûüç’'-]+/g, '');
    const decks = { listening: FRENCH_LISTENING_CARDS, reading: FRENCH_READING_CARDS, cloze: FRENCH_CLOZE_CARDS };
    const structured: Record<string, number> = {};
    for (const [name, deck] of Object.entries(decks)) {
      structured[name] = 0;
      for (const card of deck) {
        const allocation = card.rubric.allocation;
        if (!allocation) continue;
        structured[name] += 1;
        const corpus = (card.rubric.answerGuide ?? []).map(normalise);
        expect(allocation.rows.length, `${card.id}: no rows`).toBeGreaterThan(0);
        for (const row of allocation.rows) {
          expect(row.text.length, `${card.id}: empty row`).toBeGreaterThan(0);
          expect(corpus.some(line => line.includes(normalise(row.text))), `${card.id}: row "${row.text}" is not lifted`).toBe(true);
          if (row.part) expect(corpus.some(line => line.includes(normalise(row.part!))), `${card.id}: part "${row.part}" is not lifted`).toBe(true);
          for (const step of row.steps ?? []) expect(step, card.id).toBeLessThanOrEqual(row.marks);
        }
        for (const note of allocation.directions) {
          expect(corpus.some(line => line.includes(normalise(note))), `${card.id}: direction "${note.slice(0, 40)}" is not lifted`).toBe(true);
        }
        const max = Math.max(0, ...allocation.rows.filter(row => row.marks > 0).map(row => row.marks));
        if (allocation.ladder) expect(allocation.ladder.at(-1), card.id).toBe(card.totalMarks);
        else if (allocation.scoring === 'higher-segment-both') expect(max * 2, card.id).toBe(card.totalMarks);
        else expect(max * allocation.count, card.id).toBe(card.totalMarks);
      }
    }
    expect(structured).toEqual({ listening: 715, reading: 876, cloze: 170 });

    // What is still a list, by shape. Fix a shape and lower its number here.
    const fallback = FRENCH_READING_CARDS.filter(card => !card.rubric.allocation);
    const shape = (card: typeof fallback[number]) => {
      if (card.level === 'higher' && /\bQ6\b/.test(card.questionRef)) return 'HL Q6 opinion: points priced in the general scheme, not on the card';
      if (card.level === 'ordinary' && /\bQ8\b/.test(card.questionRef)) return 'OL Q8 points: priced in the general scheme, not on the card';
      return 'other';
    };
    const byShape: Record<string, string[]> = {};
    for (const card of fallback) (byShape[shape(card)] ??= []).push(card.id);
    expect(Object.fromEntries(Object.entries(byShape).map(([key, ids]) => [key, ids.length]))).toEqual({
      'HL Q6 opinion: points priced in the general scheme, not on the card': 34,
      'OL Q8 points: priced in the general scheme, not on the card': 14,
      other: 1,
    });
    // A 2013 line whose bracketed note ends in its own price ("… 4 marks (Minus 1 mark …, e.g. je demande = 3 marks)").
    expect(byShape.other).toEqual(['fr-2013-ol-reading-a4-q3']);
    const pick = (card: Guided) => [card.rubric?.answerGuide ?? []];
    expect(pricedProseLines(FRENCH_LISTENING_CARDS.filter(card => !card.rubric.allocation), pick)).toBe(0);
    expect(pricedProseLines(fallback, pick)).toBeLessThanOrEqual(BASELINE.frenchReading);
    expect(FRENCH_CLOZE_CARDS.filter(card => !card.rubric.allocation)).toHaveLength(0);
  });

  it('Irish: listening and reading answers are rows; what is still welded prose is pinned by shape', () => {
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9áéíóú’'-]+/g, '');
    const exact = [...IRISH_HIGHER, ...IRISH_ORDINARY].filter(card =>
      card.rubric.system === 'irish' && /Cluastuiscint|Léamhthuiscint/.test(card.questionRef));
    const structured = exact.filter(card => card.rubric.system === 'irish' && card.rubric.criteria[0].allocation);
    for (const card of structured) {
      if (card.rubric.system !== 'irish') continue;
      const criterion = card.rubric.criteria[0];
      const allocation = criterion.allocation!;
      const corpus = normalise(criterion.guidance.join(' ') + ' ' + card.questionText);
      let total = 0;
      for (const part of allocation.parts) {
        if (part.prompt) expect(corpus.includes(normalise(part.prompt)), `${card.id}: prompt "${part.prompt.slice(0, 40)}" is not lifted`).toBe(true);
        expect(part.rows.length, `${card.id}: sub-question without rows`).toBeGreaterThan(0);
        for (const row of part.rows) {
          expect(row.text.length, `${card.id}: empty row`).toBeGreaterThan(0);
          expect(corpus.includes(normalise(row.text)), `${card.id}: row "${row.text.slice(0, 40)}" is not lifted`).toBe(true);
          expect(row.marks, card.id).toBeLessThanOrEqual(part.tariff);
        }
        if (part.ladder) expect(part.ladder.at(-1), card.id).toBe(part.tariff);
        else expect(Math.max(...part.rows.map(row => row.marks)), card.id).toBeGreaterThan(0);
        total += part.tariff;
      }
      expect(total, `${card.id}: parts add to ${total}`).toBe(criterion.maxMarks);
      for (const note of allocation.directions) {
        expect(corpus.includes(normalise(note)), `${card.id}: direction "${note.slice(0, 40)}" is not lifted`).toBe(true);
      }
    }
    expect(exact).toHaveLength(180);
    expect(structured).toHaveLength(136);

    // What is still prose, by shape. A reading excerpt irish_cards.py cut
    // short or started mid-question cannot reconcile; fix the excerpt and
    // lower its number here.
    const fallback = exact.filter(card => card.rubric.system === 'irish' && !card.rubric.criteria[0].allocation);
    const shape = (card: typeof fallback[number]) => {
      if (/Ceist 6\b/.test(card.questionRef)) return 'HL Q6 grammar + literary composite tariff';
      if (/Léamhthuiscint/.test(card.questionRef)) return 'reading excerpt cut short or started mid-question';
      return 'listening excerpt cut short';
    };
    const byShape: Record<string, number> = {};
    for (const card of fallback) byShape[shape(card)] = (byShape[shape(card)] ?? 0) + 1;
    expect(byShape).toEqual({
      'reading excerpt cut short or started mid-question': 31,
      'HL Q6 grammar + literary composite tariff': 10,
      'listening excerpt cut short': 3,
    });
    // Every other exact criterion (the 45 Ordinary composition "Tasc" 0/2
    // tariffs) is already a button; the welded ones above are the residue.
    const welded = cardsOf(irish).reduce((count, card) =>
      count + (card.criteria ?? []).filter(criterion => criterion.guidanceKind === 'exact').length, 0)
      - structured.length;
    expect(welded).toBeLessThanOrEqual(BASELINE.irishExactCriteria);
  });

  it('Politics: bullet answers still sit in a closed details box (to convert)', () => {
    const bulleted = cardsOf(politics).filter(card =>
      /^\s*•\s*\S/m.test((card.rubric?.schemeGuidance ?? []).join('\n'))).length;
    expect(bulleted).toBeLessThanOrEqual(BASELINE.politicsBulletCards);
  });

  it('PE: priced answers and quality ladders still sit in criterion prose (to convert)', () => {
    // "Accurate description: 4; some accuracy: 2." and "3 × 2 marks. Load: javelin…"
    const PE_PRICED = /:\s*\d+(?:\s*[–-]\s*\d+)?\s*[;.]|\b\d+\s*(?:×|x)\s*\d+\s*marks?|\b\d+\s*\+\s*\d+\s*marks?|\b\d+\s*marks?\b/i;
    const lines = cardsOf(physicalEducation).reduce((count, card) =>
      count + (card.rubric?.criteria ?? []).flatMap(criterion => criterion.guidance ?? []).filter(line => PE_PRICED.test(line)).length, 0);
    expect(lines).toBeLessThanOrEqual(BASELINE.physicalEducationLines);
  });

  it('Art: scheme tables still render their marks column as text (to convert)', () => {
    const tables = cardsOf(art).filter(card => (card.criteria ?? []).some(criterion => criterion.rowMarks?.length)).length;
    expect(tables).toBeLessThanOrEqual(BASELINE.artTableCards);
  });
});

/** Measured 2026-10-23 on the decks as shipped. Only ever lower these.
 *  French (2026-10-24): listening and cloze are fully structured; the reading
 *  number is the priced lines left in the 50 opinion cards above. */
const BASELINE = {
  frenchReading: 1,
  irishExactCriteria: 89,
  politicsBulletCards: 215,
  physicalEducationLines: 763,
  artTableCards: 1548,
};

if (process.env.CLARITY_PRINT) {
  const pick = (card: Guided) => [card.rubric?.answerGuide ?? []];
  console.log(JSON.stringify({
    frenchReading: pricedProseLines(FRENCH_READING_CARDS.filter(card => !card.rubric.allocation), pick),
    physicalEducationLines: cardsOf(physicalEducation).reduce((count, card) =>
      count + (card.rubric?.criteria ?? []).flatMap(criterion => criterion.guidance ?? []).filter(line => /:\s*\d+(?:\s*[–-]\s*\d+)?\s*[;.]|\b\d+\s*(?:×|x)\s*\d+\s*marks?|\b\d+\s*\+\s*\d+\s*marks?|\b\d+\s*marks?\b/i.test(line)).length, 0),
  }));
}
