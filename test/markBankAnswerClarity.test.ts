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
import { CARDS as POLITICS_HIGHER } from '../components/MarkBank/cards/politics-and-society/higher';
import { CARDS as POLITICS_ORDINARY } from '../components/MarkBank/cards/politics-and-society/ordinary';
import { REVIEWED_CARDS as PE_CARDS } from '../components/MarkBank/cards/physical-education/factory';
import { CARDS as ART_HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as CONSTRUCTION_HIGHER } from '../components/MarkBank/cards/construction-studies/higher';
import { CARDS as CONSTRUCTION_ORDINARY } from '../components/MarkBank/cards/construction-studies/ordinary';
import { CARDS as HISTORY_HIGHER } from '../components/MarkBank/cards/history/higher';
import { CARDS as HISTORY_ORDINARY } from '../components/MarkBank/cards/history/ordinary';
import { CARDS as ART_ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import { isPointCard, isRubricCard, rowPartsReconcile, type ArtRubric, type GeographyAllocation, type SecRubricCard } from '../types/markBank';
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

  it('Politics: every card’s scheme is ladders and rows, or a visible list; what is still a list is pinned by id', () => {
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
    const cards = [...POLITICS_HIGHER, ...POLITICS_ORDINARY].filter(card => card.rubric.system === 'politics');
    const structured = cards.filter(card => card.rubric.system === 'politics' && card.rubric.allocation);
    for (const card of structured) {
      if (card.rubric.system !== 'politics') continue;
      const { allocation, criteria, schemeGuidance } = card.rubric;
      const corpus = normalise([...(schemeGuidance ?? []), ...criteria.flatMap(criterion => [criterion.label, ...(criterion.bands ?? []).flatMap(band => [band.label, band.guidance])])].join(' '));
      let total = 0;
      for (const part of allocation!.parts) {
        expect(part.bands || part.rows, `${card.id}: part without bands or rows`).toBeTruthy();
        if (part.caption) expect(corpus.includes(normalise(part.caption)), `${card.id}: caption "${part.caption.slice(0, 40)}" is not lifted`).toBe(true);
        for (const band of part.bands ?? []) {
          expect(corpus.includes(normalise(band.label)), `${card.id}: band "${band.label}" is not lifted`).toBe(true);
          if (band.descriptor) expect(corpus.includes(normalise(band.descriptor)), `${card.id}: descriptor is not lifted`).toBe(true);
          for (const mark of band.marks) expect(mark, card.id).toBeLessThanOrEqual(part.max);
        }
        if (part.bands) expect(Math.max(...part.bands.flatMap(band => band.marks)), `${card.id}: ladder top`).toBe(part.max);
        for (const row of part.rows ?? []) {
          expect(row.text.length, `${card.id}: empty row`).toBeGreaterThan(0);
          expect(corpus.includes(normalise(row.text)), `${card.id}: row "${row.text.slice(0, 40)}" is not lifted`).toBe(true);
          expect(row.marks, card.id).toBeLessThanOrEqual(part.max);
        }
        if (part.ladder) expect(part.ladder.at(-1), card.id).toBe(part.max);
        total += part.max;
      }
      expect(total, `${card.id}: parts add to ${total}`).toBe(card.totalMarks);
      for (const line of [...allocation!.examples, ...allocation!.directions]) {
        expect(corpus.includes(normalise(line)), `${card.id}: "${line.slice(0, 40)}" is not lifted`).toBe(true);
      }
    }
    expect(cards).toHaveLength(623);
    // 580 before the residue shapes were read: a name the scheme prints bare over a one- or two-mark criterion,
    // a sibling card's ladder on a split question's shared block, tariff rows beside a ladder, a range the text
    // layer broke over two lines, a band whose descriptor follows its marks.
    expect(structured).toHaveLength(615);
    // What is still a list, pinned by id: a two-line answer with "1 mark + 1 mark" inside it, a one-word answer under a
    // sibling's "2 marks + 2 marks", three "One fact" items over a two-mark ladder on a four-mark response, an essay whose
    // second criterion's bands the block does not carry, a sibling card's answer row, a bare "Name" the question also
    // says, and two tariffs the block does not print.
    expect(cards.filter(card => card.rubric.system === 'politics' && !card.rubric.allocation).map(card => card.id).sort()).toEqual([
      'politics-2018-hl-q1-c', 'politics-2018-ol-q1-b-i', 'politics-2018-ol-q1-k-example', 'politics-2018-ol-q1-o-i',
      'politics-2019-ol-q1-f', 'politics-2019-ol-q3-c', 'politics-2021-hl-q2-g', 'politics-2021-ol-q1-q-iii',
    ]);
    // No card hides its answers in a closed box any more: the bullets are a
    // visible list on every card, structured or not.
    expect(cardsOf(politics).filter(card => /^\s*•\s*\S/m.test((card.rubric?.schemeGuidance ?? []).join('\n'))).length).toBeGreaterThan(0);
  });

  it('PE: every criterion’s guidance is bands and rows that reach exactly its permitted marks; the rest is pinned', () => {
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
    const criteria = PE_CARDS.flatMap(card => card.rubric.criteria.map(criterion => ({ card, criterion })));
    const structured = criteria.filter(({ criterion }) => criterion.allocation);
    for (const { card, criterion } of structured) {
      const allocation = criterion.allocation!;
      const corpus = normalise(criterion.guidance.join(' ') + ' ' + criterion.label);
      for (const band of allocation.bands ?? []) {
        expect(corpus.includes(normalise(band.label)), `${card.id}/${criterion.label}: band "${band.label}" is not lifted`).toBe(true);
        for (const mark of band.marks) expect(criterion.permittedMarks, `${card.id}/${criterion.label}: band mark ${mark}`).toContain(mark);
      }
      for (const row of allocation.rows ?? []) {
        expect(row.text.length, `${card.id}/${criterion.label}: empty row`).toBeGreaterThan(0);
        expect(corpus.includes(normalise(row.text)), `${card.id}/${criterion.label}: row "${row.text.slice(0, 40)}" is not lifted`).toBe(true);
        expect(row.marks, card.id).toBeLessThanOrEqual(criterion.maxMarks);
      }
      if (allocation.caption) expect(corpus.includes(normalise(allocation.caption)), `${card.id}/${criterion.label}: caption is not lifted`).toBe(true);
      for (const note of allocation.notes) expect(corpus.includes(normalise(note)), `${card.id}/${criterion.label}: note is not lifted`).toBe(true);
      // What the bands and rows can reach is exactly the permitted marks.
      let sums = new Set<number>([0]);
      for (const row of allocation.rows ?? []) {
        const next = new Set(sums);
        for (const sum of sums) for (const value of row.steps ?? [row.marks]) next.add(sum + value);
        sums = next;
      }
      if (allocation.bands?.length) {
        const next = new Set(sums);
        for (const sum of sums) for (const mark of allocation.bands.flatMap(band => band.marks)) next.add(sum + mark);
        sums = next;
      }
      expect([...sums].sort((a, b) => a - b), `${card.id}/${criterion.label}: reachable marks`).toEqual([...criterion.permittedMarks].sort((a, b) => a - b));
    }
    expect(criteria).toHaveLength(1269);
    expect(structured).toHaveLength(1230);
    // Guidance whose marks the parser cannot reach exactly: counted items at
    // two possible values ("1 mark, or 2 marks where …, up to 6"), and prose
    // over several permitted marks. Rewrite the guidance in a readable shape
    // and take the criterion off this list.
    expect(criteria.filter(({ criterion }) => !criterion.allocation).map(({ card, criterion }) => `${card.id}/${criterion.id}`).sort()).toEqual([
      'pe-2020-hl-q11aiii/c1', 'pe-2020-hl-q13a/c1', 'pe-2020-hl-q15ai/c1', 'pe-2020-hl-q15ai/c2', 'pe-2020-hl-q15ai/c3', 'pe-2021-hl-q13b/c2',
      'pe-2021-hl-q13c/c1', 'pe-2021-hl-q15bii/c1', 'pe-2021-ol-q6/c1', 'pe-2022-hl-q3/c1', 'pe-2022-hl-q3/c2', 'pe-2023-hl-q13d/c1',
      'pe-2023-hl-q14aii/c1', 'pe-2023-hl-q15bi/c1', 'pe-2023-hl-q16a/c1', 'pe-2023-hl-q17aii/c1', 'pe-2023-hl-q18b/c1', 'pe-2023-hl-q18di/c1',
      'pe-2023-hl-q1a/c1', 'pe-2023-hl-q4a/c1', 'pe-2023-hl-q8/c1', 'pe-2023-ol-q15b/c1', 'pe-2023-ol-q16c/c1', 'pe-2023-ol-q16c/c2',
      'pe-2024-hl-q11b/c1', 'pe-2024-hl-q12a/c1', 'pe-2024-hl-q13aii/c1', 'pe-2024-hl-q16ai/c1', 'pe-2024-hl-q5b/c1', 'pe-2024-hl-q9b/c1',
      'pe-2025-hl-q15b/c1', 'pe-2025-hl-q16ai/c1', 'pe-2025-hl-q16bii/c1', 'pe-2025-hl-q16c/c1', 'pe-2025-hl-q17a/c1', 'pe-2025-hl-q17c/c1',
      'pe-2025-hl-q18aii/c1', 'pe-2025-hl-q9b/c1', 'pe-2026-hl-q12/c1',
    ]);
    // "Accurate description: 4; some accuracy: 2." and "3 × 2 marks. Load: javelin…" still as prose, in those criteria only.
    const PE_PRICED = /:\s*\d+(?:\s*[–-]\s*\d+)?\s*[;.]|\b\d+\s*(?:×|x)\s*\d+\s*marks?|\b\d+\s*\+\s*\d+\s*marks?|\b\d+\s*marks?\b/i;
    const lines = criteria.filter(({ criterion }) => !criterion.allocation).flatMap(({ criterion }) => criterion.guidance).filter(line => PE_PRICED.test(line)).length;
    expect(lines).toBeLessThanOrEqual(BASELINE.physicalEducationLines);
  });

  it('Art: every 2010–2022 component is rows the student places marks on, cut from the printed table', () => {
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
    const cards = [...ART_HIGHER, ...ART_ORDINARY].filter((card): card is SecRubricCard & { rubric: ArtRubric } => card.rubric.system === 'art');
    const criteria = cards.flatMap(card => card.rubric.criteria.map(criterion => ({ card, criterion })));
    const legacy = criteria.filter(({ criterion }) => criterion.rowMarks?.length);
    expect(legacy).toHaveLength(2574);
    // 2023+ descriptor criteria keep their bands; only a printed table becomes rows.
    for (const { card, criterion } of criteria.filter(({ criterion }) => !criterion.rowMarks?.length)) {
      expect(criterion.allocation, card.id).toBeUndefined();
      expect(criterion.bands?.length, card.id).toBe(3);
    }
    expect(legacy.filter(({ criterion }) => !criterion.allocation).map(({ card, criterion }) => `${card.id}/${criterion.id}`)).toEqual([]);
    let rows = 0;
    let cut = 0;
    const kept: string[] = [];
    for (const { card, criterion } of legacy) {
      const allocation = criterion.allocation!;
      const where = `${card.id}/${criterion.id}`;
      // The rows are the printed rows at the printed marks, and add up to the component.
      expect(allocation.rows.map(row => row.marks), where).toEqual(criterion.rowMarks);
      expect(allocation.rows.reduce((sum, row) => sum + row.marks, 0), where).toBe(criterion.maxMarks);
      allocation.rows.forEach((row, index) => {
        rows += 1;
        const note = criterion.rowNotes?.[index] ?? '';
        const corpus = normalise(`${criterion.guidance[index]} ${note}`);
        expect(normalise(row.text), `${where}/${row.id}: row text`).toBe(normalise(criterion.guidance[index]));
        if (row.parts) {
          cut += 1;
          expect(row.parts.length, `${where}/${row.id}: a split has at least two parts`).toBeGreaterThan(1);
          expect(row.parts.reduce((sum, part) => sum + part.marks, 0), `${where}/${row.id}: parts add up`).toBe(row.marks);
          for (const part of row.parts) {
            expect(part.marks, `${where}/${row.id}/${part.id}`).toBeGreaterThan(0);
            expect(corpus.includes(normalise(part.text)), `${where}/${row.id}/${part.id}: "${part.text}" is not lifted`).toBe(true);
          }
        } else if (row.note) {
          kept.push(`${where}/${row.id}`);
        }
        // A note is the cell's own words, one rule per sentence.
        for (const piece of row.note?.split('. ') ?? []) expect(corpus.includes(normalise(piece)), `${where}/${row.id}: note "${piece}" is not lifted`).toBe(true);
      });
    }
    expect([rows, cut]).toEqual([2616, 414]);
    // Notes cells the parser leaves as a note under a whole row: a rule on the
    // row ("Max 3 for partially correct name"), a cap ("3 points for 30 marks
    // and 2 detailed points for 26 marks maximum"), a count without a noun
    // ("3 x 5", "5/5/5"), one price for the whole row ("5 for named work"),
    // or a cell that prices alternatives ("2 for Lunula, 3 for …, 2 for Gorget only").
    expect(kept.sort()).toEqual([
      'art-2014-hl-q1-task1/b/r1', 'art-2014-hl-q2-task1/a/r1', 'art-2014-hl-q4-c/c/r1', 'art-2014-ol-q10-a/a/r1', 'art-2014-ol-q11-a/a/r1',
      'art-2014-ol-q13-a/a/r1', 'art-2014-ol-q17-a/a/r1', 'art-2014-ol-q17-b/b/r1', 'art-2014-ol-q18-a/a/r1', 'art-2014-ol-q19-a/a/r1',
      'art-2014-ol-q21-a/a/r1', 'art-2014-ol-q4-c/c/r1', 'art-2014-ol-q9-a/a/r1', 'art-2015-hl-q16-task1/b/r1', 'art-2016-hl-q1-task2/d/r1',
      'art-2016-hl-q16-task2/c/r1', 'art-2017-hl-q16-task2/c/r1', 'art-2019-hl-q1-task2/c/r1', 'art-2019-hl-q8-task1/b/r1', 'art-2019-ol-q16-b/b/r1',
      'art-2019-ol-q17-a/a/r1', 'art-2019-ol-q18-a/a/r1', 'art-2020-hl-q16-task2/c/r1', 'art-2021-hl-q2-task1/a/r1', 'art-2021-hl-q2-task2/d/r1',
      'art-2021-ol-q16-b/b/r1', 'art-2021-ol-q4-a-castletown-house/a/r1', 'art-2021-ol-q7-a-james-arthur-oconnor/a/r1',
      'art-2022-hl-q15-c-die-brucke/c/r1', 'art-2022-hl-q15-c-die-brucke/c/r2', 'art-2022-hl-q15-c-impressionism/c/r1', 'art-2022-hl-q15-c-impressionism/c/r2',
      'art-2022-hl-q15-c-international-gothic/c/r1', 'art-2022-hl-q15-c-international-gothic/c/r2', 'art-2022-hl-q15-c-surrealism/c/r1', 'art-2022-hl-q15-c-surrealism/c/r2',
      'art-2022-hl-q4-task1/b/r1', 'art-2022-ol-q10-b/b/r1', 'art-2022-ol-q11-b/b/r1', 'art-2022-ol-q12-b/b/r1', 'art-2022-ol-q13-a/a/r1',
      'art-2022-ol-q16-a/a/r1', 'art-2022-ol-q3-c/c/r1', 'art-2022-ol-q4-a/a/r1', 'art-2022-ol-q5-c/c/r1', 'art-2022-ol-q6-c/c/r1',
      'art-2022-ol-q7-a-daniel-maclise/a/r1', 'art-2022-ol-q9-b/b/r1',
    ]);
  });
  it('History: a price the scheme prints inside an answer line is a row, never a second answer behind one claim', () => {
    const cards = [...HISTORY_HIGHER, ...HISTORY_ORDINARY].filter(isPointCard);
    const rows = cards.flatMap(card => card.rows.map(row => ({ card, row })));
    // "Sods (3M) and saplings (3M)" was one six-mark row; hist_rows.py cuts it at the printed prices.
    const inline = /\(\s*\d+\s*[Mm](?:\s*\+\s*\d+\s*[Mm])?\s*\)/g;
    expect(rows.filter(({ row }) => row.kind === 'point' && (row.verbatim.match(inline) ?? []).length >= 2).map(({ card }) => card.id)).toEqual([]);
    // "… 5M + 5M Max =" left on a row by the tariff reader: the printed split is the row's note now.
    expect(rows.filter(({ row }) => /\d+\s*M\s*\+\s*\d+\s*M\s*Max\s*=\s*$/i.test(row.verbatim)).map(({ card }) => card.id)).toEqual([]);
    expect(rows.filter(({ row }) => /\bMax = \d+M$/.test(row.contextNote ?? '')).length).toBe(7);
    // The shapes the pass reads, pinned so a regenerated deck shows any change.
    const fixed = cards.filter(card => card.tariffModel.kind === 'fixed');
    expect(fixed.filter(card => card.rows.length === 2 && card.rows.every(row => row.kind === 'point' && row.marks === card.totalMarks / 2)).length).toBe(59);
    expect(rows.filter(({ row }) => row.kind === 'anyN' && row.group).map(({ row }) => row.group!.options)).toEqual([['Liverpool', 'Manchester', 'Birmingham', 'Leeds']]);
    expect(rows.filter(({ row }) => row.kind === 'criterion').map(({ row }) => [row.verbatim, row.marks, row.permittedMarks])).toEqual([['Clonmel prison', 6, [0, 3, 6]]]);
    expect(rows.filter(({ row }) => !row.verbatim.trim()).map(({ card }) => card.id)).toEqual([]);
  });

  it('Construction: a criterion row priced in named components carries them as parts the student places separately', () => {
    const cards = [...CONSTRUCTION_HIGHER, ...CONSTRUCTION_ORDINARY].filter(isPointCard);
    const rows = cards.flatMap(card => card.rows.map(row => ({ card, row })));
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
    // "Design feature 1 (2 for point, 4 for discussion)" offered one strip for six marks (construction_rows.py).
    const priced = /\b(\d+)\s*(?:marks?\s*)?for\s+[a-z]+\s*,\s*(\d+)\s*(?:marks?\s*)?for\s+[a-z]+|\(\s*[a-z]+\s+\d+\s*marks?\s*,\s*[a-z]+\s+\d+\s*marks?\s*\)|^Scale\s*[-–:]?\s*\d+\s*marks?.*Drafting/i;
    const unsplit = rows.filter(({ row }) => row.kind === 'criterion' && priced.test(row.verbatim) && !row.parts);
    // 2010 HL Q3(a) prices three details at note 4 + sketch 4 each, 24 in all: no two-part split adds up to the row.
    expect(unsplit.map(({ card, row }) => `${card.id}/${row.id}: ${row.verbatim}`)).toEqual([
      'cons-2010-hl-q3-a/internal: Internal Insulation System (note 4 marks, sketch 4 marks)',
      'cons-2010-hl-q3-a/external: External Insulation System (note 4 marks, sketch 4 marks)',
      'cons-2010-hl-q3-complete/a-internal: Internal Insulation System (note 4 marks, sketch 4 marks)',
      'cons-2010-hl-q3-complete/a-external: External Insulation System (note 4 marks, sketch 4 marks)',
    ]);
    const withParts = rows.filter(({ row }) => row.parts);
    // 1,145 rows: 664 priced in the row's own text, 481 priced in its note ("Notes 6 and sketches 6. Such as: …").
    expect(withParts).toHaveLength(1145);
    for (const { card, row } of withParts) {
      expect(rowPartsReconcile(row), `${card.id}/${row.id}`).toBe(true);
      // Every part is a word the row or its note prints, and the row's own text, marks and steps are untouched.
      for (const part of row.parts!) expect(normalise(`${row.verbatim} ${row.contextNote ?? ''}`).includes(normalise(part.verbatim)), `${card.id}/${row.id}/${part.id}`).toBe(true);
      expect(row.permittedMarks![0]).toBe(0);
      expect(row.permittedMarks!.at(-1)).toBe(row.marks);
    }
    // Complete-question cards mirror their tasks' parts under their own row ids.
    for (const card of cards.filter(item => item.taskGroups?.length)) {
      for (const group of card.taskGroups!) {
        const source = cards.find(item => item.id === group.sourceCardId)!;
        const twin = group.rowIds.map(id => card.rows.find(row => row.id === id)!);
        expect(twin.map(row => row.parts ?? null), `${card.id} ← ${source.id}`).toEqual(source.rows.map(row => row.parts ?? null));
      }
    }
  });

});

/** Measured 2026-10-23 on the decks as shipped. Only ever lower these.
 *  French (2026-10-24): listening and cloze are fully structured; the reading
 *  number is the priced lines left in the 50 opinion cards above. */
const BASELINE = {
  frenchReading: 1,
  irishExactCriteria: 89,
  physicalEducationLines: 15,
};

if (process.env.CLARITY_PRINT) {
  const pick = (card: Guided) => [card.rubric?.answerGuide ?? []];
  console.log(JSON.stringify({
    frenchReading: pricedProseLines(FRENCH_READING_CARDS.filter(card => !card.rubric.allocation), pick),
    physicalEducationLines: PE_CARDS.flatMap(card => card.rubric.criteria).filter(criterion => !criterion.allocation)
      .flatMap(criterion => criterion.guidance).filter(line => /:\s*\d+(?:\s*[–-]\s*\d+)?\s*[;.]|\b\d+\s*(?:×|x)\s*\d+\s*marks?|\b\d+\s*\+\s*\d+\s*marks?|\b\d+\s*marks?\b/i.test(line)).length,
  }));
}
