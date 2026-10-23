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
import frenchListening from '../components/MarkBank/cards/french/listening.json';
import frenchReading from '../components/MarkBank/cards/french/reading.json';
import frenchCloze from '../components/MarkBank/cards/french/cloze.json';
import irish from '../components/MarkBank/cards/irish/authored.json';
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

  it('French: priced answers still sit in answerGuide prose (to convert)', () => {
    const pick = (card: Guided) => [card.rubric?.answerGuide ?? []];
    expect(pricedProseLines(frenchListening, pick)).toBeLessThanOrEqual(BASELINE.frenchListening);
    expect(pricedProseLines(frenchReading, pick)).toBeLessThanOrEqual(BASELINE.frenchReading);
    // Cloze prints the gap's answer as "3. organisé" and prices the set once.
    const clozeAnswers = cardsOf(frenchCloze).filter(card => (card.rubric?.answerGuide ?? []).some(line => /^\d+\.\s+\S/.test(line))).length;
    expect(clozeAnswers).toBeLessThanOrEqual(BASELINE.frenchClozeCards);
  });

  it('Irish: exact criteria still weld their answers into one bullet (to convert)', () => {
    const exact = cardsOf(irish).reduce((count, card) =>
      count + (card.criteria ?? []).filter(criterion => criterion.guidanceKind === 'exact').length, 0);
    expect(exact).toBeLessThanOrEqual(BASELINE.irishExactCriteria);
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

/** Measured 2026-10-23 on the decks as shipped. Only ever lower these. */
const BASELINE = {
  frenchListening: 1778,
  frenchReading: 2742,
  frenchClozeCards: 170,
  irishExactCriteria: 225,
  politicsBulletCards: 215,
  physicalEducationLines: 763,
  artTableCards: 1548,
};

if (process.env.CLARITY_PRINT) {
  const pick = (card: Guided) => [card.rubric?.answerGuide ?? []];
  console.log(JSON.stringify({
    frenchListening: pricedProseLines(frenchListening, pick),
    frenchReading: pricedProseLines(frenchReading, pick),
    frenchCloze: pricedProseLines(frenchCloze, pick),
    physicalEducationLines: cardsOf(physicalEducation).reduce((count, card) =>
      count + (card.rubric?.criteria ?? []).flatMap(criterion => criterion.guidance ?? []).filter(line => /:\s*\d+(?:\s*[–-]\s*\d+)?\s*[;.]|\b\d+\s*(?:×|x)\s*\d+\s*marks?|\b\d+\s*\+\s*\d+\s*marks?|\b\d+\s*marks?\b/i.test(line)).length, 0),
  }));
}
