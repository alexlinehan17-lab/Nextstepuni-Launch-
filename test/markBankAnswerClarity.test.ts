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
import { FRENCH_LISTENING_CARDS } from '../components/MarkBank/cards/french/listening';
import { FRENCH_READING_CARDS } from '../components/MarkBank/cards/french/reading';
import { FRENCH_CLOZE_CARDS } from '../components/MarkBank/cards/french/cloze';
import irish from '../components/MarkBank/cards/irish/authored.json';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as IRISH_ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
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
