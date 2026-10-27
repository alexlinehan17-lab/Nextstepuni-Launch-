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
import { CARDS as ITALIAN_HIGHER } from '../components/MarkBank/cards/italian/higher';
import { CARDS as ITALIAN_ORDINARY } from '../components/MarkBank/cards/italian/ordinary';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { CARDS as BUSINESS_HIGHER } from '../components/MarkBank/cards/business/higher';
import { CARDS as BUSINESS_ORDINARY } from '../components/MarkBank/cards/business/ordinary';
import { businessExpectedLayout } from '../components/MarkBank/businessRubric';
import { isPointCard, isRubricCard, rowPartsReconcile, type ArtRubric, type BusinessRubric, type GeographyAllocation, type IrishAllocation, type SecRubricCard } from '../types/markBank';
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
    // Reading 876 → 920 once an opinion list ("Any two of:" over bullets the scheme prices only in its
    // general rule) became a ladder of the total shared equally, where the ledger permits that step.
    expect(structured).toEqual({ listening: 715, reading: 920, cloze: 170 });

    // What is still a list, by shape. Fix a shape and lower its number here.
    const fallback = FRENCH_READING_CARDS.filter(card => !card.rubric.allocation);
    const shape = (card: typeof fallback[number]) => {
      // 2012 and 2015 Higher Q6: the ledger permits even marks only, so two points at 5 is not a step it allows.
      if (card.level === 'higher' && /\bQ6\b/.test(card.questionRef) && card.rubric.criteria[0].permittedMarks.every(mark => mark % 2 === 0)) {
        return /\(Two points/.test(card.questionText) || /^Any two of/m.test((card.rubric.answerGuide ?? []).join('\n'))
          ? 'HL Q6 opinion: the ledger permits even marks only, so the equal split is not a step'
          : 'HL Q6 two-part description: no printed count to share the total by';
      }
      return 'other';
    };
    const byShape: Record<string, string[]> = {};
    for (const card of fallback) (byShape[shape(card)] ??= []).push(card.id);
    expect(Object.fromEntries(Object.entries(byShape).map(([key, ids]) => [key, ids.length]))).toEqual({
      'HL Q6 opinion: the ledger permits even marks only, so the equal split is not a step': 3,
      'HL Q6 two-part description: no printed count to share the total by': 1,
      other: 1,
    });
    expect(byShape['HL Q6 two-part description: no printed count to share the total by']).toEqual(['fr-2012-hl-reading-a2-q6']);
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
    // Every row, prompt, sample and direction is a slice of the scheme's guidance or the
    // paper's question; a row that carries the answer the scheme printed for it
    // ("Ainm an fhile: Caitlín Maude") is two slices.
    const checkAllocation = (card: { id: string; questionText: string }, criterion: { guidance: string[]; maxMarks: number; allocation?: IrishAllocation }) => {
      const allocation = criterion.allocation!;
      const corpus = normalise(criterion.guidance.join(' ') + ' ' + card.questionText);
      const lifted = (text: string) => corpus.includes(normalise(text)) || text.split(': ').every(piece => corpus.includes(normalise(piece)));
      let total = 0;
      for (const part of allocation.parts) {
        if (part.prompt) expect(lifted(part.prompt), `${card.id}: prompt "${part.prompt.slice(0, 40)}" is not lifted`).toBe(true);
        expect(part.rows.length, `${card.id}: sub-question without rows`).toBeGreaterThan(0);
        for (const row of part.rows) {
          expect(row.text.length, `${card.id}: empty row`).toBeGreaterThan(0);
          expect(lifted(row.text), `${card.id}: row "${row.text.slice(0, 40)}" is not lifted`).toBe(true);
          expect(row.marks, card.id).toBeLessThanOrEqual(part.tariff);
          if (row.steps) {
            expect(row.steps[0], `${card.id}: steps start at 0`).toBe(0);
            expect(row.steps.at(-1), `${card.id}: steps end at the row's marks`).toBe(row.marks);
          }
        }
        for (const sample of part.samples ?? []) expect(lifted(sample), `${card.id}: sample "${sample.slice(0, 40)}" is not lifted`).toBe(true);
        // A ladder prices how many are right; tariff rows add up to the sub-question; an answer list
        // (listening and reading) prices each alternative, so its best row is what counts.
        if (part.ladder) expect(part.ladder.at(-1), card.id).toBe(part.tariff);
        else if (part.rows.some(row => row.steps) || part.rows.reduce((sum, row) => sum + row.marks, 0) === part.tariff) expect(part.rows.reduce((sum, row) => sum + row.marks, 0), `${card.id}: rows of a sub-question add to its tariff`).toBe(part.tariff);
        else expect(Math.max(...part.rows.map(row => row.marks)), card.id).toBeGreaterThan(0);
        total += part.tariff;
      }
      expect(total, `${card.id}: parts add to ${total}`).toBe(criterion.maxMarks);
      for (const note of allocation.directions) {
        expect(lifted(note), `${card.id}: direction "${note.slice(0, 40)}" is not lifted`).toBe(true);
      }
    };
    for (const card of structured) {
      if (card.rubric.system !== 'irish') continue;
      checkAllocation(card, card.rubric.criteria[0]);
    }
    expect(exact).toHaveLength(180);
    // 136 before irish_excerpts.py re-cut the reading excerpts across their pages and
    // tariffs.ts read the last question's composite tariff.
    expect(structured).toHaveLength(173);

    // What is still prose, pinned by id: four reading excerpts whose answers the
    // scheme prices in a shape answers.ts does not read yet (unpriced bullets under
    // a ladder, a section total inside the excerpt) and three listening extracts
    // whose tariff lines the text layer broke. Fix one and take it off this list.
    const fallback = exact.filter(card => card.rubric.system === 'irish' && !card.rubric.criteria[0].allocation);
    expect(fallback.map(card => card.id).sort()).toEqual([
      'irish-2021-ol-p2-reading-a-q2', 'irish-2021-ol-p2-reading-b-q5', 'irish-2022-hl-p1-listening-a-f1', 'irish-2022-hl-p2-reading-b-q1',
      'irish-2022-hl-p2-reading-b-q5', 'irish-2023-ol-p1-listening-b-c2', 'irish-2024-ol-p1-listening-b-c1',
    ]);

    // Literature: the Eolas criterion prices what the student must do ("Príomhthéama = 2 mharc",
    // "Dhá phointe eolais = 4 mharc + 4 mharc", "Tréith 1 = 13 mharc" under a band table) and
    // tariffs.ts cuts that into rows and steps; the sample points stay a list under each part.
    const literature = [...IRISH_HIGHER, ...IRISH_ORDINARY].filter(card => card.rubric.system === 'irish' && /Prose|Poetry|Literature/.test(card.questionRef));
    expect(literature).toHaveLength(130);
    const eolas = literature.map(card => ({ card, criterion: card.rubric.system === 'irish' ? card.rubric.criteria.find(criterion => criterion.guidanceKind === 'indicative')! : undefined! }));
    expect(eolas.filter(({ criterion }) => criterion.guidance.some(line => /\d+\s*m?h?arc/.test(line)))).toHaveLength(130);
    const literatureStructured = eolas.filter(({ criterion }) => criterion.allocation);
    for (const { card, criterion } of literatureStructured) checkAllocation(card, criterion);
    expect(literatureStructured).toHaveLength(127);
    // An option whose tariff summary the parser does not read yet, pinned by id.
    expect(eolas.filter(({ criterion }) => !criterion.allocation).map(({ card }) => card.id).sort()).toEqual([
      'irish-2022-hl-p2-poetry-3b-a', 'irish-2023-ol-p2-prose-2b-c', 'irish-2025-ol-p2-poetry-3a-a',
    ]);
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
    // 1230 before the residue shapes were read: "one mark per …" counted rows and rows per listed name, labels priced
    // without a colon, an extra "+1" as a step, ordinal responses as one counted row, and a ladder outranking a
    // printed breakdown that is not the criterion.
    expect(structured).toHaveLength(1269);
    expect(criteria.filter(({ criterion }) => !criterion.allocation).map(({ card, criterion }) => `${card.id}/${criterion.id}`)).toEqual([]);
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
    // 1,284 rows: 664 priced in the row's own text, 620 priced in its note ("Notes 6 and sketches 6. Such as: …",
    // "Location 3 and reason 2", "The distribution board drawn (4) and annotated (1)", "Correct tabulation 2, wood 3, …").
    // Every part is the scheme's own words (construction_paper.validate); a note that paraphrases the scheme's table
    // keeps only the words it prints, and a row whose head word the scheme does not print stays unsplit.
    expect(withParts).toHaveLength(1284);
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

  it('Construction: a drawing row priced "Any N of the above details (M marks each)" is a group of the scheme\'s own detail lines', () => {
    const cards = [...CONSTRUCTION_HIGHER, ...CONSTRUCTION_ORDINARY].filter(isPointCard);
    const rows = cards.flatMap(card => card.rows.map(row => ({ card, row })));
    const tariff = /^Any (\d+)\s*(?:of the above details|x|×)/i;
    // Ordinary Level draws to a priced table ("19 mm external render 5 … Any 7 of the above details (5 marks each)")
    // and Higher Level prices the same way under PERFORMANCE CRITERIA, the part's own tariff line heading its labels.
    // construction_choices.py reads each table's lines into the row's group: claim N at M each, the row's own marks,
    // the printed tariff kept as the row's note. A line the table prints twice is a detail drawn twice ("Stop valve 5"
    // on two valves, "70 x 20 mm architrave 4" each side of a door) and stays twice. 53 tasks and their twins.
    const groups = rows.filter(({ row }) => row.kind === 'anyN' && row.group && tariff.test(row.contextNote ?? ''));
    expect(groups).toHaveLength(105);
    for (const { card, row } of groups) {
      const n = Number(tariff.exec(row.contextNote!)![1]);
      expect(row.group!.claimMax, `${card.id}/${row.id}`).toBe(n);
      expect(row.group!.claimMax * row.group!.perOption, `${card.id}/${row.id}`).toBe(row.marks);
      expect(row.group!.options.length, `${card.id}/${row.id}`).toBeGreaterThanOrEqual(n);
      expect(row.group!.options.every(option => option.trim().length > 0), `${card.id}/${row.id}`).toBe(true);
      expect(/^(?:DETAILS|Details)(?:\s*[-–]\s*typical sizes)?$|^PERFORMANCE CRITERIA$/.test(row.verbatim), `${card.id}/${row.id}: ${row.verbatim}`).toBe(true);
    }
    // 2019 HL Q1(a) prices "Any 12 × 4marks" over 25 bulleted details in three menus (scheme p. 32): one pool of
    // twelve, past the 17 options a question may show, so the row keeps its strip and its note names the menus.
    const unlifted = rows.filter(({ row }) => row.kind === 'criterion' && tariff.test(row.verbatim.trim()));
    expect(unlifted.map(({ card, row }) => `${card.id}/${row.id}: ${row.verbatim}`)).toEqual([
      'cons-2019-hl-q1-a/details: Any 12 × 4marks',
      'cons-2019-hl-q1-complete/a-details: Any 12 × 4marks',
    ]);
    // Complete-question cards mirror their tasks' groups under their own row ids.
    for (const card of cards.filter(item => item.taskGroups?.length)) {
      for (const group of card.taskGroups!) {
        const source = cards.find(item => item.id === group.sourceCardId)!;
        const twin = group.rowIds.map(id => card.rows.find(row => row.id === id)!);
        expect(twin.map(row => row.group ?? null), `${card.id} ← ${source.id}`).toEqual(source.rows.map(row => row.group ?? null));
      }
    }
  });

  it('Italian: a price the scheme prints inside an answer is a row, and a shorter answer it prices is a printed step', () => {
    const cards = [...ITALIAN_HIGHER, ...ITALIAN_ORDINARY].filter(isPointCard);
    const rows = cards.flatMap(card => card.rows.map(row => ({ card, row })));
    // "Erano stati compagni (1m) di scuola (4m)", "By summer [2] 2022 [1]" were one row each; it_rows.py cuts them at the printed prices.
    const inline = /\(\s*\d+\s*m?\s*\)|\[\s*\d+\s*\]/g;
    expect(rows.filter(({ row }) => row.kind !== 'anyN' && (row.verbatim.match(inline) ?? []).length >= 2).map(({ card }) => card.id)).toEqual([]);
    const pieces = rows.filter(({ row }) => /^r-\d+-\d+$/.test(row.id));
    expect([pieces.length, new Set(pieces.map(({ card }) => card.id)).size]).toEqual([88, 35]);
    for (const { card, row } of pieces) {
      expect(row.kind, `${card.id}/${row.id}`).toBe('point');
      expect(/[\p{L}\p{N}]/u.test(row.verbatim), `${card.id}/${row.id}: "${row.verbatim}"`).toBe(true);
      expect(row.marks, `${card.id}/${row.id}`).toBeGreaterThan(0);
    }
    // The pieces of one row add up to the card: a fixed tariff still reconciles.
    for (const card of cards.filter(item => item.rows.some(row => /^r-\d+-\d+$/.test(row.id)))) {
      expect(card.rows.reduce((sum, row) => sum + (row.marks ?? 0), 0), card.id).toBe(card.totalMarks);
    }
    // The 2025 HL B2B 2(a) answer the SEC wrapped onto a second line, whose tail the reader had filed as a lesser answer.
    expect(cards.find(card => card.id === 'it-2025-hl-b2b-2-a')!.rows.map(row => [row.verbatim, row.marks])).toEqual([
      ['Il fatto che stesse per attaccare uno del partito di Rosello', 3], ['voleva coinvolgere Rosello stesso', 2],
    ]);
    // A shorter answer the scheme prices under the full one ("Nata nel 2020 2m") was a sentence in the
    // row's note; the row now carries that mark as a step, and the note still names the answer.
    const lesser = 'The scheme also pays part marks for a shorter answer: ';
    const stepped = rows.filter(({ row }) => row.kind === 'criterion');
    expect(stepped).toHaveLength(44);
    for (const { card, row } of stepped) {
      const where = `${card.id}/${row.id}`;
      expect(row.permittedMarks![0], where).toBe(0);
      expect(row.permittedMarks!.at(-1), where).toBe(row.marks);
      const priced = [...(row.contextNote ?? '').split(lesser)[1].matchAll(/”\s*(\d+)\s*marks?/g)].map(match => Number(match[1])).filter(value => value < row.marks!);
      expect([...new Set(row.permittedMarks!.slice(1, -1))].sort((a, b) => a - b), where).toEqual([...new Set(priced)].sort((a, b) => a - b));
    }
    // What is still a note: a shorter form of a cut answer (which piece?) and shorter forms of any-N
    // options (the group has no per-option steps). Model one of those and lower its number here.
    const noted = rows.filter(({ row }) => row.kind !== 'criterion' && (row.contextNote ?? '').includes(lesser));
    expect(noted.filter(({ row }) => row.kind === 'point').every(({ row }) => /^r-\d+-\d+$/.test(row.id))).toBe(true);
    expect([noted.filter(({ row }) => row.kind === 'point').length, noted.filter(({ row }) => row.kind === 'anyN').length]).toEqual([16, 93]);
  });

  it('Business: the responses the scheme prints for a part are rows on the card, each lifted from the cited scheme page', () => {
    const cards = [...BUSINESS_HIGHER, ...BUSINESS_ORDINARY].filter((card): card is SecRubricCard & { rubric: BusinessRubric } => isRubricCard(card) && card.rubric.system === 'business');
    expect(cards).toHaveLength(1988);
    const normalise = (value: string) => value.normalize('NFKC').toLowerCase().replace(/[^a-z0-9]+/g, '');
    const schemes = new Map<string, string>();
    // The scheme markdown as bus_expected.py reads it: no page heads, running footers, "(20 marks)" cells or marks column.
    const FOOT = /^\s*(?:Page \d+ of \d+|Bus\.? ?\d{4} ?\((?:OL|HL)\) ?\d+|LC Business \d{4} \((?:OL|HL)\)|Leaving Certificate\b.*|\d{1,2}\s*marks?|⟨\d+⟩|\d{1,2})\s*$/;
    const INLINE_FOOT = /\s*(?:LC Business \d{4} \((?:OL|HL)\)|Bus\.? ?\d{4} ?\((?:OL|HL)\) ?\d+|Page \d+ of \d+|Leaving Certificate(?: \d{4})?\s*[–-]\s*(?:Higher|Ordinary) Level(?: \d{4})?)\s*(?:⟨\d{1,2}⟩)?\s*/g;
    const schemeText = (year: number, level: string) => {
      const key = `${year}-${level === 'higher' ? 'hl' : 'ol'}`;
      if (!schemes.has(key)) {
        const lines = readFileSync(resolve(__dirname, '..', 'examiner-reports', 'business', 'schemes', `${key}.md`), 'utf8')
          .replace(/\u00a0/g, ' ').split('\n')
          .filter(line => !/^## Page \d+\s*$/.test(line))
          .map(line => line.replace(INLINE_FOOT, ' ').replace(/\s*⟨[^⟩]*⟩/g, '').replace(/\s*\(\s*\d{1,3}\s*marks?\s*\)/g, '').trim())
          .filter(line => line && !FOOT.test(line));
        schemes.set(key, normalise(lines.join(' ')));
      }
      return schemes.get(key)!;
    };
    const lifted = cards.filter(card => card.rubric.expected);
    expect(lifted).toHaveLength(1767);
    for (const card of lifted) {
      const corpus = schemeText(card.year, card.level);
      const expected = card.rubric.expected!;
      expect(expected.page, card.id).toBeGreaterThan(0);
      expect(expected.items.length, card.id).toBeGreaterThan(0);
      for (const item of expected.items) {
        expect(item.text.trim().length, `${card.id}/${item.id}`).toBeGreaterThan(0);
        for (const piece of [item.text, ...(item.detail ?? [])]) {
          expect(corpus.includes(normalise(piece)), `${card.id}/${item.id}: "${piece.slice(0, 50)}" is not lifted from the ${card.year} scheme`).toBe(true);
        }
      }
    }
    // A row sits under the response it names, or in one pool the responses draw from.
    const layouts = lifted.map(card => businessExpectedLayout(card.rubric)!.kind);
    expect([layouts.filter(kind => kind === 'per-response').length, layouts.filter(kind => kind === 'pool').length]).toEqual([221, 1546]);
    // What bus_expected.py could not lift, by reason, each with the pages it looked at. Fix a shape and lower its number here.
    const review = JSON.parse(readFileSync(resolve(__dirname, '..', 'scripts', 'markbank', 'authored', 'business-expected-review.json'), 'utf8')) as Array<{ id: string; reason: string; schemePages: number[] }>;
    const reasons: Record<string, number> = {};
    for (const entry of review) reasons[entry.reason] = (reasons[entry.reason] ?? 0) + 1;
    expect(reasons).toEqual({
      'an item is not one slice of the page text: a table or diagram the text layer reordered': 5,
      'part marker': 24,
      'roman marker': 22,
      's1 marker': 6,
      's1 part marker': 6,
      'table layout lost in the text layer': 59,
      'text layer glyph damage on the cited page': 27,
      'the scheme prints the marker and the question but no response under it on the cited page': 30,
      'tiny block': 1,
      'unbounded block over 3000 characters: a whole question, not this part': 14,
      'workings table flattened by the text layer': 24,
    });
    const ids = new Set(cards.map(card => card.id));
    for (const entry of review) {
      expect(ids.has(entry.id), entry.id).toBe(true);
      expect(entry.schemePages.length, entry.id).toBeGreaterThan(0);
    }
    const reviewed = new Set(review.map(entry => entry.id));
    // Every card either carries its rows or is on the review list; the three route-pool expansions share their template's data.
    expect(cards.filter(card => !card.rubric.expected && !reviewed.has(card.id)).length).toBe(3);
  });

});

/** Measured 2026-10-23 on the decks as shipped. Only ever lower these.
 *  French (2026-10-24): listening and cloze are fully structured; the reading
 *  number is the priced lines left in the 50 opinion cards above. */
const BASELINE = {
  frenchReading: 1,
  irishExactCriteria: 52,
  physicalEducationLines: 0,
};

if (process.env.CLARITY_PRINT) {
  const pick = (card: Guided) => [card.rubric?.answerGuide ?? []];
  console.log(JSON.stringify({
    frenchReading: pricedProseLines(FRENCH_READING_CARDS.filter(card => !card.rubric.allocation), pick),
    physicalEducationLines: PE_CARDS.flatMap(card => card.rubric.criteria).filter(criterion => !criterion.allocation)
      .flatMap(criterion => criterion.guidance).filter(line => /:\s*\d+(?:\s*[–-]\s*\d+)?\s*[;.]|\b\d+\s*(?:×|x)\s*\d+\s*marks?|\b\d+\s*\+\s*\d+\s*marks?|\b\d+\s*marks?\b/i.test(line)).length,
  }));
}
