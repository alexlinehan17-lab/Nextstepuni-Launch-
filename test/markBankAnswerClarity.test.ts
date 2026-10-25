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
 * by shape so a fix to one shape is visible. Since the 2010–2026 review every
 * Geography card carries one criterion per published allocation line; each is
 * cut into rows on its own (tryParseGeographyCriterionAllocation).
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
import { isRubricCard, type GeographyAllocation } from '../types/markBank';
import { geographyAchievable, geographyAllocationMax } from '../components/MarkBank/cards/geography/allocation';

type Guided = { rubric?: { answerGuide?: string[]; schemeGuidance?: string[]; criteria?: Array<{ guidance?: string[]; permittedMarks?: number[]; guidanceKind?: string; rowMarks?: number[] }> }; criteria?: Array<{ guidance?: string[]; guidanceKind?: string; rowMarks?: number[] }> };

const cardsOf = (deck: unknown): Guided[] => Array.isArray(deck) ? deck as Guided[] : (deck as { cards: Guided[] }).cards;

/** A line that prints an answer with its price, in any of the schemes' notations. */
const PRICED_ANSWER = /(?:⟨\s*\d+\s*m(?:\s*\+\s*\d+\s*m)*\s*⟩|[—–-]\s*\d+\s*Marks?\s*$|=\s*\d+\s*mharc|\b\d+\s*m\s*$|\b\d+\s*marks?\s*$)/i;

const pricedProseLines = (deck: unknown, pick: (card: Guided) => string[][]): number =>
  cardsOf(deck).reduce((count, card) =>
    count + pick(card).flat().filter(line => PRICED_ANSWER.test(line) && !/\bSRP/i.test(line) && !/^Total\b/i.test(line)).length, 0);

describe('answer clarity: priced answers are rows, not prose', () => {
  it('Geography: every structured criterion reconciles and lifts its words from the scheme or the paper', () => {
    const cards = [...GEOGRAPHY_HIGHER, ...GEOGRAPHY_ORDINARY].filter(isRubricCard);
    expect(cards).toHaveLength(4153);
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
    let criteria = 0;
    let structuredCriteria = 0;
    const structured: string[] = [];
    const fallback: typeof cards = [];
    for (const card of cards) {
      if (card.rubric.system !== 'geography') throw new Error(`${card.id}: wrong rubric`);
      // Every reviewed criterion's lines and the paper's own question: a row,
      // label, heading, option or direction must be a slice of one of them.
      const corpus = normalise([...card.rubric.criteria.flatMap(criterion => criterion.guidance), card.questionText].join(' '));
      const lifted = (text: string, what: string) =>
        expect(corpus.includes(normalise(text)), `${card.id}: ${what} "${text.slice(0, 50)}" is not lifted`).toBe(true);
      const walk = (allocation: GeographyAllocation) => {
        for (const group of allocation.groups) {
          // Headings join the printed lines they come from like cells.
          for (const piece of group.prompt?.split(' · ') ?? []) lifted(piece, 'heading');
          if (group.repeat?.unit) lifted(group.repeat.unit, 'unit');
          for (const row of group.rows) {
            expect(row.text.length, `${card.id}: empty row`).toBeGreaterThan(0);
            // One printed slice, or (an answer the scheme runs on under its
            // price) consecutive printed pieces divided like cells.
            if (!corpus.includes(normalise(row.text))) for (const piece of row.text.split(' · ')) lifted(piece, 'row');
            expect(row.marks, card.id).toBeGreaterThan(0);
            for (const step of row.steps ?? []) expect(step, card.id).toBeLessThanOrEqual(row.marks);
          }
          for (const srp of group.srp) if (srp.label) lifted(srp.label, 'SRP label');
        }
        for (const note of allocation.directions) lifted(note, 'direction');
        if (allocation.choice) {
          if (allocation.choice.prompt) lifted(allocation.choice.prompt, 'choice heading');
          for (const option of allocation.choice.options) {
            lifted(option.label, 'option');
            if (option.note) lifted(option.note, 'band descriptor');
            if (option.allocation) walk(option.allocation);
          }
        }
      };
      let all = true;
      for (const criterion of card.rubric.criteria) {
        criteria += 1;
        const allocation = criterion.allocation;
        if (!allocation) { all = false; continue; }
        structuredCriteria += 1;
        walk(allocation);
        // The rows reach the printed maximum and claim only marks the ledger permits.
        expect(geographyAllocationMax(allocation), `${card.id} ${criterion.id}`).toBe(criterion.maxMarks);
        const permitted = new Set(criterion.permittedMarks);
        expect([...geographyAchievable(allocation)].filter(mark => !permitted.has(mark)), `${card.id} ${criterion.id}`).toEqual([]);
      }
      if (all) structured.push(card.id); else fallback.push(card);
      // No examiner direction carries a priced answer of its own.
      for (const note of card.rubric.directions ?? []) {
        // ("Mount Everest · D · 0 marks" is the example the paper gives: no marks.)
        expect(/·\s*[1-9]\d*\s*(?:m|marks?)\s*$/i.test(note) && !/\bSRP|\bmax/i.test(note), `${card.id}: priced direction "${note}"`).toBe(false);
      }
    }
    expect([criteria, structuredCriteria]).toEqual([7689, 7598]);
    expect(structured).toHaveLength(4108);

    // What is still prose, by shape. Fix a shape and lower its number here.
    const shape = (card: typeof fallback[number]) => {
      if (card.rubric.system !== 'geography') return 'other';
      const lines = card.rubric.criteria.flatMap(criterion => criterion.guidance);
      // 2010–2013 HL options: the scheme prints one two-route table (3 aspects
      // at 27 + 27 + 26, or 4 at 20) whose rows the review splits into two
      // criteria, identifying + coherence (32) and discussion (48). The
      // discussion line ("8 x SRPs · OR · 6 x SRPs") prints no aspect count of
      // its own, and coherence is "7/6 marks graded" across three aspects.
      if (card.level === 'higher' && card.year <= 2013 && lines.some(line => /^(?:Discussion|Examination): · 8 x SRPs · OR · 6 x SRPs$/.test(line))) {
        return 'HL 80-mark option 2010-2013: one route table split over two criteria';
      }
      // 2016 OL Q12C prints all three patterns' prices on one line each
      // ("Named · 4m + 3m + 3m", "Located · 4m + 4m + 4m").
      if (lines.some(line => /^Named · 4m \+ 3m \+ 3m$/.test(line))) return 'three units priced on one line';
      return 'other';
    };
    const byShape: Record<string, string[]> = {};
    for (const card of fallback) (byShape[shape(card)] ??= []).push(card.id);
    expect(Object.fromEntries(Object.entries(byShape).map(([key, ids]) => [key, ids.length]))).toEqual({
      'HL 80-mark option 2010-2013: one route table split over two criteria': 44,
      'three units priced on one line': 1,
    });
    expect(byShape['three units priced on one line']).toEqual(['geography-2016-ol-p2-q12c']);
    // Options that ask for a fixed number of aspects (2011 Q16/Q17, 2012 Q18,
    // 2013 Q18 and Q24) are carded one criterion per aspect and do structure.
    const options = (year: number, numbers: Array<number | string>) => numbers.map(n => `geography-${year}-hl-p2-q${n}`);
    expect(byShape['HL 80-mark option 2010-2013: one route table split over two criteria'].sort()).toEqual([
      ...options(2010, [13, 14, 15, 16, 17, 18, 19, '20-language', '20-religion', 21, 22, 23, 24]),
      ...options(2011, [13, 14, 15, 18, 19, 20, 21, 22, 23, 24]),
      ...options(2012, [13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24]),
      ...options(2013, [13, 14, 15, 16, 17, 19, 20, 21, 22, 23]),
    ].sort());
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
