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
import { CARDS as ACCOUNTING_HIGHER } from '../components/MarkBank/cards/accounting/higher';
import { CARDS as ACCOUNTING_ORDINARY } from '../components/MarkBank/cards/accounting/ordinary';
import type { AccountingRubric } from '../types/markBank';
import accountingResidue from '../scripts/markbank/authored/accounting-rows-residue.json';
import { REVIEWED_CARDS as APPLIED_MATHS_REVIEWED } from '../components/MarkBank/cards/applied-maths/reviewed';
import type { AppliedMathematicsRubric } from '../types/markBank';
import appliedMathsResidue from '../scripts/markbank/authored/applied-maths-steps-residue.json';
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
import { CARDS as TECHNOLOGY_HIGHER } from '../components/MarkBank/cards/technology/higher';
import { CARDS as TECHNOLOGY_ORDINARY } from '../components/MarkBank/cards/technology/ordinary';
import technologyExclusions from '../scripts/markbank/authoring/exclusions/technology.json';
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
            // A row priced unalike per point carries one price per point, none above its own.
            if (row.unitMarks) {
              expect(row.unitMarks, card.id).toHaveLength(group.repeat?.count ?? 0);
              for (const marks of row.unitMarks) expect(marks, card.id).toBeLessThanOrEqual(row.marks);
            }
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
    // Every criterion structures since the last 45 cards did (2026-10-28):
    // the 2010–2013 Higher 80-mark options (a points table split over two
    // criteria) and 2016 Ordinary Q12C (one line pricing three patterns).
    expect([criteria, structuredCriteria]).toEqual([7689, 7689]);
    expect(structured).toHaveLength(4153);
    expect(fallback.map(card => card.id)).toEqual([]);

    // 2010–2013 Higher options print one table for 80 marks: "Number of
    // aspects: 3 (27 + 27 + 26) · (4 @ 20 marks each)" over identifying,
    // discussion and coherence, which the review splits over two criteria.
    // Both criteria share one pick (the discussion follows the first), and
    // point by point they award what the heading prints: 27, 27, 26 or 20 x 4.
    const options = (year: number, numbers: Array<number | string>) => numbers.map(n => `geography-${year}-hl-p2-q${n}`);
    const pointTables: string[] = [];
    for (const card of cards) {
      if (card.rubric.system !== 'geography') continue;
      const followers = card.rubric.criteria.filter(criterion => criterion.allocation?.choice?.follows);
      if (!followers.length) continue;
      pointTables.push(card.id);
      const owner = card.rubric.criteria.find(criterion => criterion.id === followers[0].allocation!.choice!.follows)!;
      const table = [owner, ...followers];
      const labels = (criterion: typeof owner) => criterion.allocation!.choice!.options.map(option => option.label);
      for (const criterion of followers) expect(labels(criterion), card.id).toEqual(labels(owner));
      const perPoint = owner.allocation!.choice!.options.map((_, column) => {
        const sums: number[] = [];
        for (const criterion of table) {
          const group = criterion.allocation!.choice!.options[column].allocation!.groups[0];
          for (let unit = 0; unit < group.repeat!.count; unit += 1) {
            sums[unit] = (sums[unit] ?? 0)
              + group.rows.reduce((sum, row) => sum + (row.unitMarks?.[unit] ?? row.marks), 0)
              + group.srp.reduce((sum, srp) => sum + srp.count * srp.marks, 0);
          }
        }
        return sums;
      });
      expect(perPoint, card.id).toEqual([[27, 27, 26], [20, 20, 20, 20]]);
    }
    // Options that ask for a fixed number of aspects (2011 Q16/Q17, 2012 Q18,
    // 2013 Q18 and Q24) are carded one criterion per aspect and need no table.
    expect(pointTables.sort()).toEqual([
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
    // 580 before the residue shapes were read (2026-10-27 #291), 615 after them; the last eight (a two-line answer with
    // "1 mark + 1 mark" inside it, a one-word answer under a sibling's "2 marks + 2 marks", three "One fact" items
    // priced 2 + 1 + 1 in the scheme's margin, an essay whose second criterion's label heads its ladder, a sibling
    // card's answer row, a bare "Name", and two sub-tariffs the block had lost) are read since the same day: every
    // card is ladders and rows. cards/politics-and-society/corrections.ts restores the two margin prices the block
    // lost, from the scheme PDF, and test/politicsAnswers.test.tsx pins each shape.
    expect(structured).toHaveLength(623);
    expect(cards.filter(card => card.rubric.system === 'politics' && !card.rubric.allocation).map(card => card.id)).toEqual([]);
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
    expect(rows.filter(({ row }) => /\bMax = \d+M$/.test(row.contextNote ?? '')).length).toBe(24);
    // The shapes the pass reads, pinned so a regenerated deck shows any change.
    const fixed = cards.filter(card => card.tariffModel.kind === 'fixed');
    expect(fixed.filter(card => card.rows.length === 2 && card.rows.every(row => row.kind === 'point' && row.marks === card.totalMarks / 2)).length).toBe(189);
    // "X/Y/Z (any two for 3m + 3m)" is an any-two group over the scheme's own alternatives too.
    expect(rows.filter(({ row }) => row.kind === 'anyN' && row.group).map(({ row }) => row.group!.options).sort()).toEqual([
      ['A new life', 'Better wages', 'Better work standards'],
      ['Chapel bell', 'convent chimes', 'organ'],
      ['Church renewal', 'Christian unity', 'Opening to the contemporary world'],
      ['Civil rights', 'Assassination', 'Vietnam'],
      ['Closure of rail link to Donegal', 'Closure of rail link to Dublin', 'Downgrading of rail link to Belfast'],
      ['Consecrating churches', 'Ordaining priests', 'Confirming children', 'Deciding marriage cases'],
      ['Dental services', 'spectacles', 'drugs'],
      ['Distinguished', 'Of illustrious or noble families', 'Renowned for great deeds or achievements', 'Valour or prowess'],
      ['Efficient', 'Hard-working', 'Intelligent', 'Shrewd'],
      ['England', 'France', 'Flanders'],
      ['Hawks', 'nets', 'guns', 'setting dogs', 'greyhounds'],
      ['He was tall', 'dark', 'scowling', 'wolf-like'],
      ['Her father’s death', 'Talk of radiation sickness', 'Sense of impending doom', 'Concern about missile strikes'],
      ['Intelligent and shrewd', 'Efficient and hard-working', 'Engaging and friendly'],
      ['Liverpool', 'Manchester', 'Birmingham', 'Leeds'],
      ['Members sat on the steps', 'They sat on the arms of benches', 'They sat on each other‟s knees'],
      ['Mercilessness', 'ruthlessness and calculation', 'hot- and cold-bloodiness 1'],
      ['Moluccas', 'Java', 'Malaya', 'India', 'Ceylon', 'Taiwan'],
      ['Nantes', 'Bordeaux', 'Lisbon', 'Cadiz'],
      ['On railways', 'as news vendors', 'bootblacks', 'lamplighters', 'barbers'],
      ['Pheasant', 'partridge', 'grouse', 'hares'],
      ['Pleasant situation', 'Gorgeous buildings', 'Population', 'Obedience and loyalty'],
      ['Preach', 'Lead men astray', 'Incite rebellion'],
      ['Ranks and titles', 'Civil laws', 'New social regulations', 'New customs and rules'],
      ['Salt fish', 'hides', 'cattle', 'hobby-horses'],
      ['Stoking the fire', 'Fetching water', 'Bringing in stacks of bread'],
      ['Tapestries', 'Mirrors', 'Candle holders', 'Upholstered furniture'],
      ['There was no roof', 'door', 'windscreen'],
      ['They dressed badly', 'wore shaggy jackets', 'kept their hands in their pockets', 'did not speak clearly.'],
      ['To watch over everyone', 'To warn in a friendly was those who are misbehaving', 'To report to ministers if necessary'],
      ['Training', 'Maintenance allowance', 'Bonus pay'],
    ]);
    // A row that is the scheme pricing an answer it does not print says so.
    // ("ONE valid export (e.g. wool, butter, etc.)" prints its examples, so it is an answer.)
    const tariffWording = rows.filter(({ row }) => row.kind !== 'anyN'
      && /^(?:ONE|TWO|THREE|One valid|Two valid|Any valid|Any (?:ONE|TWO|THREE))\b/.test(row.verbatim)
      && !/\be\.g\./.test(row.verbatim));
    expect(tariffWording.length).toBeGreaterThan(80);
    expect(tariffWording.filter(({ row }) => !(row.contextNote ?? '').includes('The scheme prints no answer here')).map(({ card }) => card.id)).toEqual([]);
    // A six-mark answer with a printed partial ("Green ribbons (ribbons = 3m)") is a stepped row: the partial is its note.
    // So is a row that prints a count and the price of each ("Any TWO ... @ 3M each"): 0, 3 or 6.
    expect(rows.filter(({ row }) => row.kind === 'criterion').map(({ row }) => [row.verbatim, row.marks, row.permittedMarks, row.contextNote]).sort()).toEqual([
      // Each a printed partial or alternative as a step on its row ("Green ribbons (ribbons = 3m)",
      // "Swastika 8M" / "Germanic cross = 4M"), a price for an answer the scheme does not print
      // ("One opinion = 5M"), or the bank's unprinted row where the scheme prints no answer at all.
      ['A or B – which is the more objective historical source?', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['A or B – which is the more valuable source about bardic schools and poets?', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['A or B – which offers more valuable depiction of life in Gaelic Ireland?', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Advantage is that with a visual source we can see for ourselves – we can look upon the scene as it actually was on the day. With the written source we have to rely on the writer that his description is fair and accurate.', 10, [0, 5, 10], undefined],
      ['An attempt to bring guns into Northern Ireland (through Dublin Airport)', 6, [0, 3, 6], '„To bring in guns‟ only = 3M'],
      ['Any TWO countries invaded by Napoleon 3M + 3M', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Any TWO features from second paragraph of text @ 3M each', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Any TWO of Beethoven’s compositions 3 + 3', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Any TWO valid aims from the war @ 3M each', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Any TWO valid aims of the Geraldine League (3M x 2)', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Any two valid countries of destination (3M + 3M)', 6, [0, 3, 6], undefined],
      ['As a colonist: Spenser considers the bardic poets a threat to the security of the colony because they encourage young men to admire the disobedient and rebellious He is very judgemental about the bards and their poems which gives the impression that, as a colonist, he is culturally superior', 5, [0, 1, 2, 3, 4, 5], undefined],
      ['BBC (1) were very much in favour of the strike (2) did not monitor NI broadcasts (3) did not know what was going on (4) were effectively running a rebel radio station', 10, [0, 5, 10], undefined],
      ['Battleship/ Warship', 6, [0, 3, 6], 'Ship = 3M'],
      ['By launching the Dreadnought', 6, [0, 3, 6], '‘Quickly’ ALONE = 3M'],
      ['Clonmel prison', 6, [0, 3, 6], 'Clonmel only (3m), prison only (3m)'],
      ['Compare role of poet as set out in Document A with role of poet as set out in Document B', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Compare the evidence in both documents', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Cusack was its founder/ One of its first Secretaries', 6, [0, 3, 6], 'Supporter ONLY = 3M'],
      ['Do the documents agree about Irish attitudes to divorce? Yes or no, with supporting points from each document.', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Do the documents agree about Irish attitudes to marriage? Yes or no, with supporting points from each document.', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Document A describes the 1967 march as “a great folk festival” characterised by “good humour”, a colourful musical social and traditional occasion which set out to offend no-one\nDocument B describes the 1969 march as one fraught with tension, with Catholic Bogsiders feeling “sick of Protestants and police cordons and riot tenders and drumbeating”, oppressed by the marchers’ triumphalism and the security apparatus of the state Catholics were not part of the traditional spectacle but stayed at home “irritated, ill-humoured and apprehensive” The intervening events in Northern Ireland 1967-1969 had clearly increased sectarian tensions and the entrenchment of the two communities in Derry', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], undefined],
      ['Document A does not support the claim: Faulkner went by helicopter because he couldn’t travel by road to Stormont He could see evidence of paramilitary activity on the ground from his helicopter There were even barricades at Dundonald House in Stormont itself That barricade reappeared only an hour after it had been removed', 5, [0, 1, 2, 3, 4, 5], undefined],
      ['Document A is a primary source because it is from a memoir/autobiography where the writer is remembering herself as a little girl witnessing the events from eighty years earlier.', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], undefined],
      ['Document B They enjoy a great reputation among the people Their verses are taken up with general applause They glorify wrongdoers and so apparently earn respect', 5, [0, 1, 2, 3, 4, 5], undefined],
      ['Document B does not support the claim: Rees writes that British authority in Northern Ireland was in question Rees himself had been warned of an assassination attempt His poor working conditions were a direct result of security problems He admits that effective administration was in the hands of the strikers, not of the government', 5, [0, 1, 2, 3, 4, 5], undefined],
      ['Evidence that Spenser was curious about bardic poetry\nHe had many of the poems translated so that he could understand them', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], undefined],
      ['Explanation', 5, undefined, 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Famine, Civil War, Political instability', 5, [0, 3, 5], 'Threats: two = 5M; one = 3M; “wolf and tiger” alone = 0'],
      ['Green ribbons', 6, [0, 3, 6], 'ribbons = 3m'],
      ['Hans Place', 8, [0, 4, 8], 'London ONLY = 4M'],
      ['Healy scored the first goal ever in an All-Ireland Championship', 6, [0, 3, 6], '‘first goal’ ONLY = 3M'],
      ['In document A Whitaker tells us that he and his colleagues did not receive extra payment for their work. He says that here was “no hope of any reward”.', 10, [0, 5, 10], undefined],
      ['It is an original document from the period called the Pacification of Ghent (8 Nov 1576) signed four days after the sack of Antwerp. It was actually drafted by the prelates, nobles, towns and states of the Netherlands.', 5, [0, 1, 2, 3, 4, 5], 'Mark quality of explanation on its merits. — Explanation be marked on a sliding scale out of 5: Excellent = 5 mks Very good = 4 mks Good = 3 mks Fair = 2 mks Weak = 0-1 mks — Max = 10M'],
      ['Less than half', 6, [0, 3, 6], 'Half ONLY = 3M'],
      ['Massive German air raids', 6, [0, 3, 6], 'air raids alone = 3m'],
      ['On the one hand Collins was “exuberant” as seen in the “horseplay” of throwing food and cushions. On the other hand he was religious as seen in his attendance at daily Mass.', 10, [0, 5, 10], undefined],
      ['One opinion', 5, undefined, 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Opinions of him differed from pure white to deepest black/ from hero to villain', 6, [0, 3, 6], '„Opinions of him differed‟ only = 3M'],
      ['Oriental rugs', 8, [0, 4, 8], 'Rugs ONLY = 4M'],
      ['Primary or secondary?', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Private/ family houses', 6, [0, 3, 6], '„Houses‟ only = 3M'],
      ['Reasons given for selecting phrase', 8, [0, 4, 8], 'Examples: If it is true that masked and armed men blocked roads, it is objective; If it is true that workers were threatened at workplaces such as H & W, it is objective; If it is not true that such things happened, it is biased. — Mark quality of explanation on its merits. — Max = 10M'],
      ['Residents and foreign-owned businesses in the town', 5, [0, 3, 5], 'TWO groups = 5m, ONE group = 3m'],
      ['Spenser’s preoccupations as a poet and as a colonist\nAs a poet: Spenser appreciates wit and invention, but more so the poet’s skill in the ornaments of poetry He believes that the purpose of poetry is to adorn and beautify virtue as opposed to the praise of vice', 5, [0, 1, 2, 3, 4, 5], undefined],
      ['Swastika', 8, [0, 4, 8], 'Germanic cross = 4M'],
      ['TWO New World commodities (@ 3M each) which were landed at Seville', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['TWO countries which were rivals to Dutch trade @ 3M each', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['TWO valid aims of the Apprentice Boys of Derry 3M x 2', 6, [0, 3, 6], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['The Nazi-Soviet Non-aggression Pact', 6, [0, 3, 6], 'Marriage/agreement between Hitler and Stalin (3M only) — Marriage/wedding only = 0M'],
      ['The Tu-104 was one of the first jet passenger planes in the world', 6, [0, 3, 6], 'Plane ONLY = 3M'],
      ['The original six members had access to Irish, British and Danish fisheries', 6, [0, 3, 6], 'access to Irish fisheries alone = 3m'],
      ['The scheme prints no answer for this part.', 10, undefined, 'The scheme prints one Criticism answer, under (a), and it is about the King’s proclamation (document B), which part (b) asks about. It prints nothing for this part.'],
      ['Third class', 8, [0, 4, 8], 'Train ONLY = 4M'],
      ['Two reasons for Yes or No', 8, [0, 4, 8], 'Sermon advised “restraint towards people of different religious persuasions” — Above quote only = 2M — Seems to be reasonable advice to behave respectfully to others, to not give offence which could lead to trouble At the same time the Apprentice Boys are asked to keep “firmness in defence of their Protestant heritage”, to assert themselves and keep the faith — Mark quality of explanation on its merits. — Max = 10M'],
      ['Von Eckstadt Vienna 1848', 6, [0, 3, 6], 'Any TWO @ 3M each'],
      ['We can see men, women and children – presumably families', 6, [0, 3, 6], 'Children ONLY = 3M'],
      ['Which is more sympathetic to bardic poets, A or B?', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['While it is not clear from either document who was ultimately responsible for the crisis, it could be argued that the crisis was exacerbated by the Congolese cutting the rope (Document A) and by the behaviour of the Belgian paratroopers (Document B).', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], undefined],
      ['Yes or No? Candidate makes choice and gives at least two reasons for choice', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Yes or No? One reason only required', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Yes or No?', 10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'The scheme prints no answer here: any correct one earns the marks.'],
      ['Yes, the documents agree that the bardic poet was an influential figure\nDocument A As a master of history and poetry he would be influential Influential because of his wealth and affluence He had gained victory over the Devil and the world', 5, [0, 1, 2, 3, 4, 5], undefined],
    ]);
    expect(rows.filter(({ row }) => !row.verbatim.trim()).map(({ card }) => card.id)).toEqual([]);
    // 2020 OL Q3(a) prices each component and answers the one that needs an answer:
    // "Document A is a primary source = 5M" / "Reason = 5M" / the reason / "5M + 5M 10M".
    const answeredSplit = cards.find(card => card.id === 'hist-2020-ol-lm-s1-q3a')!;
    expect([answeredSplit.tariffModel.kind, answeredSplit.totalMarks]).toEqual(['fixed', 10]);
    expect(answeredSplit.rows.map(row => [row.verbatim.split('. ')[0], row.marks, row.contextNote])).toEqual([
      ['Document A is a primary source', 5, undefined],
      ['It is the recollection/words of a North Vietnamese soldier who fought against the US in Vietnam', 5, 'Reason = 5M'],
    ]);
    // Priced statements, the older Ordinary comparison part (2016 OL Q2): each statement at its printed
    // marks, and document points the closing split prices, one term to a document.
    const statements = cards.find(card => card.id === 'hist-2016-ol-lm-s1-q2a')!;
    expect(statements.rows.map(row => [row.verbatim.split(' ').slice(0, 4).join(' '), row.marks])).toEqual([
      ['Yes. Ellen Wilkinson took', 2], ['Document A is from', 4], ['Document B states that', 4],
    ]);
    expect(statements.rows[0].contextNote).toBe('Must be clearly stated');
    const splitPriced = cards.find(card => card.id === 'hist-2016-ol-lm-s1-q2b')!;
    expect(splitPriced.rows.map(row => [row.verbatim.split(' ').slice(0, 3).join(' '), row.marks])).toEqual([
      ['Document B', 2], ['Document A describes', 4], ['Document B gives', 4],
    ]);
    // Closed by the part's marks printed bare: "... searchlights = 3M" / "... against the sky = 2M 5M" (2016 HL Q1(d)).
    const bareTotal = cards.find(card => card.id === 'hist-2016-hl-lm-s1-q1d')!;
    expect(bareTotal.rows.map(row => [row.verbatim, row.marks])).toEqual([
      ['Huge burning urns; flood-lighting by hundreds of powerful searchlights', 3],
      ['The mystical quality of the ritual was exaggerated; lights played eerily against the sky', 2],
    ]);
    // Priced items OR the answer after the solidus: "The spirit, content and enterprise (2M x 3)/
    // A free Constitution" (2013 OL Q6 A4, (6)) is two routes; claiming one side locks the other.
    const routed = cards.find(card => card.id === 'hist-2013-ol-em-s2t6a-q4')!;
    expect(routed.rows.map(row => [row.verbatim, row.marks, row.route])).toEqual([
      ['The spirit', 2, 'priced-items'], ['content', 2, 'priced-items'], ['enterprise', 2, 'priced-items'],
      ['A free Constitution', 6, 'alternative'],
    ]);
    expect(rows.filter(({ row }) => row.route).map(({ card }) => card.id)).toEqual(Array(4).fill('hist-2013-ol-em-s2t6a-q4'));
    // A verdict printed unstopped over its first reason ("Document A or B or both" / "Document A states ...")
    // keeps its own line in the row, so the two never read as one sentence; so does one document's point run
    // unstopped into the next ("... in document A Document B states ...", hist_all.document_lines).
    expect(rows.filter(({ row }) => row.verbatim.includes('\n')).map(({ card }) => card.id).sort()).toEqual([
      'hist-2010-hl-lm-s1-q2b',
      'hist-2011-hl-em-s1-q2a',
      'hist-2011-hl-em-s1-q2b',
      'hist-2011-hl-em-s1-q3b',
      'hist-2011-hl-lm-s1-q2a',
      'hist-2011-hl-lm-s1-q3a',
      'hist-2011-ol-em-s1-q3b',
      'hist-2012-hl-em-s1-q2b',
      'hist-2012-hl-em-s1-q3a',
      'hist-2012-hl-lm-s1-q2a',
      'hist-2012-hl-lm-s1-q2a',
      'hist-2012-ol-em-s1-q2a',
      'hist-2012-ol-em-s1-q2b',
      'hist-2012-ol-lm-s1-q3a',
      'hist-2013-hl-lm-s1-q2a',
      'hist-2013-hl-lm-s1-q2b',
      'hist-2013-ol-em-s1-q2a',
      'hist-2013-ol-em-s1-q2b',
      'hist-2014-ol-em-s1-q2b',
      'hist-2015-hl-em-s1-q2b',
      'hist-2015-ol-em-s1-q2b',
      'hist-2016-hl-lm-s1-q2a',
      'hist-2016-hl-lm-s1-q3b',
      'hist-2016-ol-em-s1-q2a',
      'hist-2023-ol-deferred-lm-s1-q2b',
    ]);
    // Where the closing prices the verdict, it is a row at its price: "Doc A and a valid reason 5M + 5M Max = 10M",
    // "2M + 4M + 4M Max = 10M" (2025 OL).
    expect(cards.find(card => card.id === 'hist-2025-ol-lm-s1-q3a')!.rows.map(row => row.marks)).toEqual([5, 5]);
    expect(cards.find(card => card.id === 'hist-2025-ol-em-s1-q2b')!.rows.map(row => row.marks)).toEqual([2, 4, 4]);
    // Bare-figure prices with the phrase running on: "In a slap-dash (3) meaningless (3) way" (2013 OL
    // Topic 6 A1): the rows are the priced spans, never a joined row the scheme does not print whole.
    expect(cards.find(card => card.id === 'hist-2013-ol-lm-s2t6a-q1')!.rows.map(row => [row.verbatim, row.marks])).toEqual([
      ['In a slap-dash', 3], ['meaningless', 3],
    ]);
  });

  it('Accounting: every task carries the scheme’s priced lines as rows that add up to it, or is listed in the residue with its reason', () => {
    const cards = [...ACCOUNTING_HIGHER, ...ACCOUNTING_ORDINARY].filter((card): card is SecRubricCard & { rubric: AccountingRubric } => card.kind === 'rubric' && card.rubric.system === 'accounting');
    expect(cards).toHaveLength(1365);
    const structured = cards.filter(card => card.rubric.rows?.length);
    for (const card of structured) {
      const rows = card.rubric.rows!;
      expect(new Set(rows.map(row => row.id)).size, `${card.id}: row ids`).toBe(rows.length);
      for (const row of rows) {
        expect(row.text.trim().length, `${card.id}/${row.id}: empty row`).toBeGreaterThan(0);
        expect(/[A-Za-z0-9]/.test(row.text), `${card.id}/${row.id}: "${row.text}" names nothing`).toBe(true);
        expect(row.marks, `${card.id}/${row.id}: marks`).toBeGreaterThan(0);
        expect(Number.isInteger(row.page) && row.page > 0, `${card.id}/${row.id}: page`).toBe(true);
      }
      // The rows are the task: they add up to its total exactly.
      expect(rows.reduce((sum, row) => sum + row.marks, 0), `${card.id}: rows add up`).toBe(card.totalMarks);
    }
    // 1,267 of 1,365 tasks (2026-10-28, exclusions wave): the rest keep the crop and the half-mark stepper, each with its reason in the residue file.
    // A floor, not an exact count, so a later lift never needs a re-pin; the residue is pinned by id against the file.
    expect(structured.length).toBeGreaterThanOrEqual(1267);
    const residue = cards.filter(card => !card.rubric.rows?.length).map(card => card.id).sort();
    expect(residue).toEqual(accountingResidue.tasks.map(task => task.id).sort());
    for (const task of accountingResidue.tasks) expect(task.reason.length, task.id).toBeGreaterThan(0);
    // A part the scheme prices only through its section total is one flagged block row; pinned so it cannot grow unnoticed.
    expect(structured.filter(card => card.rubric.rows!.some(row => row.inferred)).map(card => card.id).sort()).toEqual(["acc-2010-hl-q9(c)", "acc-2010-ol-q5(a)(i)", "acc-2010-ol-q5(b)(iv)", "acc-2011-hl-q2(c)", "acc-2011-hl-q4(b)", "acc-2011-hl-q5(c)", "acc-2011-ol-q4(c)", "acc-2011-ol-q5(d)", "acc-2011-ol-q8(a)(i)", "acc-2011-ol-q8(b)", "acc-2012-hl-q4(d)", "acc-2012-hl-q4(e)", "acc-2012-hl-q5(b)", "acc-2012-ol-q4(d)", "acc-2012-ol-q5(c)", "acc-2012-ol-q5(d)", "acc-2013-hl-q7(c)", "acc-2013-ol-q5(c)", "acc-2013-ol-q5(d)", "acc-2014-hl-q6(e)", "acc-2014-hl-q7(e)", "acc-2014-ol-q6(e)", "acc-2014-ol-q9(c)", "acc-2015-hl-q4(d)", "acc-2015-hl-q4(e)", "acc-2015-ol-q5(a)", "acc-2015-ol-q5(d)", "acc-2015-ol-q9(f)", "acc-2016-hl-q3(c)", "acc-2016-hl-q5(c)", "acc-2016-hl-q6(e)", "acc-2016-hl-q7(b)", "acc-2016-ol-q5(d)", "acc-2017-hl-q2(b)", "acc-2017-hl-q3(b)", "acc-2017-hl-q5(c)", "acc-2017-hl-q6(e)", "acc-2017-hl-q9(e)", "acc-2017-ol-q5(d)", "acc-2017-ol-q7(e)", "acc-2017-ol-q9(f)", "acc-2018-hl-q2(d)", "acc-2018-hl-q3(b)", "acc-2018-hl-q4(c)", "acc-2018-hl-q5(c)", "acc-2018-hl-q6(b)", "acc-2018-hl-q7(e)", "acc-2018-hl-q8(b)(iv)", "acc-2018-hl-q9(c)", "acc-2018-ol-q5(c)", "acc-2018-ol-q5(d)", "acc-2018-ol-q8(g)", "acc-2018-ol-q9(c)", "acc-2019-hl-q3(b)", "acc-2019-hl-q5(c)", "acc-2019-hl-q6(d)", "acc-2019-hl-q8(e)", "acc-2019-hl-q9(e)", "acc-2019-ol-q9(f)", "acc-2020-hl-q2(b)", "acc-2020-hl-q4(e)", "acc-2020-hl-q6(e)", "acc-2021-hl-q5(c)", "acc-2021-hl-q7(b)", "acc-2022-hl-q3(c)", "acc-2022-ol-q5(a)(ii)", "acc-2023-hl-q5(c)", "acc-2023-hl-q7(e)", "acc-2023-ol-q5(a)(ii)", "acc-2023-ol-q5(b)(iii)", "acc-2024-hl-q4(d)", "acc-2024-hl-q5(c)", "acc-2024-hl-q7(e)", "acc-2024-hl-q9(e)", "acc-2024-ol-q5(a)(i)", "acc-2024-ol-q5(a)(iv)", "acc-2024-ol-q5(c)", "acc-2024-ol-q6(b)", "acc-2024-ol-q8(g)", "acc-2026-hl-q4(c)", "acc-2026-hl-q8(b)(ii)"]);
  });

  it('Applied Maths: every published step shows the lines it prices as a crop of the scheme page, or the card is in the residue with its reason', () => {
    const cards = APPLIED_MATHS_REVIEWED.filter((card): card is SecRubricCard & { rubric: AppliedMathematicsRubric } => card.kind === 'rubric' && card.rubric.system === 'applied-mathematics');
    expect(cards).toHaveLength(1486);
    const residue = new Set(appliedMathsResidue.cards.map(card => card.id));
    let cut = 0, scaleOnly = 0;
    for (const card of cards) {
      const steps = card.rubric.allocations.filter(item => item.label.startsWith('Published step'));
      if (!steps.length) { scaleOnly += 1; continue; }
      if (residue.has(card.id)) {
        expect(steps.some(item => item.region), `${card.id}: in the residue yet cut`).toBe(false);
        continue;
      }
      cut += 1;
      const pages = card.rubric.solution.pages;
      const regions = card.rubric.solution.regions ?? [];
      let last: { p: number; top: number; bottom: number } | null = null;
      for (const item of steps) {
        expect(item.region, `${card.id}/${item.id}: no region`).toBeDefined();
        const { p, r } = item.region!;
        const index = pages.indexOf(p);
        expect(index, `${card.id}/${item.id}: page ${p} is not a solution page`).toBeGreaterThanOrEqual(0);
        const whole = regions[index] as [number, number, number, number] | undefined;
        // Inside the solution's own region, at least a line tall, and in reading order.
        if (whole) {
          expect(r[0] >= whole[0] - 1e-6 && r[2] <= whole[2] + 1e-6 && r[1] >= whole[1] - 1e-6 && r[3] <= whole[3] + 1e-6, `${card.id}/${item.id}: outside the solution`).toBe(true);
        }
        expect(r[3] - r[1], `${card.id}/${item.id}: thinner than a line`).toBeGreaterThanOrEqual(0.012);
        // In reading order; two steps the scheme prices on one line ("5, 5"), or beside one figure, share that band exactly.
        const shared = last !== null && last.p === p && r[1] === last.top && r[3] === last.bottom;
        if (last && last.p === p && !shared) expect(r[1], `${card.id}/${item.id}: out of order`).toBeGreaterThanOrEqual(last.bottom - 0.01);
        last = { p, top: r[1], bottom: r[3] };
      }
    }
    // 1,434 cut and 52 priced by a scale over the whole solution (2026-10-28, exclusions wave): every card with published steps is cut.
    // A floor, not an exact count, so a later lift never needs a re-pin; the residue is pinned by id (none).
    expect(cut).toBeGreaterThanOrEqual(1434);
    expect(scaleOnly).toBe(52);
    expect([...residue].sort()).toEqual([]);
    for (const card of appliedMathsResidue.cards) expect(card.reason.length, card.id).toBeGreaterThan(0);
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
    // on two valves, "70 x 20 mm architrave 4" each side of a door) and stays twice. 54 tasks and their twins
    // (2026-10-28: a floor, not an exact count, so a later lift never needs a re-pin).
    const groups = rows.filter(({ row }) => row.kind === 'anyN' && row.group && tariff.test(row.contextNote ?? ''));
    expect(groups.length).toBeGreaterThanOrEqual(107);
    for (const { card, row } of groups) {
      const n = Number(tariff.exec(row.contextNote!)![1]);
      expect(row.group!.claimMax, `${card.id}/${row.id}`).toBe(n);
      expect(row.group!.claimMax * row.group!.perOption, `${card.id}/${row.id}`).toBe(row.marks);
      expect(row.group!.options.length, `${card.id}/${row.id}`).toBeGreaterThanOrEqual(n);
      expect(row.group!.options.every(option => option.trim().length > 0), `${card.id}/${row.id}`).toBe(true);
      expect(/^(?:DETAILS|Details)(?:\s*[-–]\s*typical sizes)?$|^PERFORMANCE CRITERIA$/.test(row.verbatim), `${card.id}/${row.id}: ${row.verbatim}`).toBe(true);
    }
    // Every such row is lifted: 2019 HL Q1(a) prices "Any 12 × 4marks" over 25 bulleted details in three menus
    // (scheme p. 32) as one pool, and the menu ceiling (MAX_LONG_OPTION_ROWS, 25) follows that largest verified SEC menu.
    const unlifted = rows.filter(({ row }) => row.kind === 'criterion' && tariff.test(row.verbatim.trim()));
    expect(unlifted.map(({ card, row }) => `${card.id}/${row.id}: ${row.verbatim}`)).toEqual([]);
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

  it('Technology: a drawn answer is the ask as its one row behind the scheme\'s own print; every printed 2026 Higher ask is a card', () => {
    const cards = [...TECHNOLOGY_HIGHER, ...TECHNOLOGY_ORDINARY].filter(isPointCard);
    const normalise = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, '');
    // 716 shipped before the lane opened; 2026 Higher and the in-window parts that were
    // refused for a missing picture or a drawn answer are added, never removed (tech_all.py,
    // tech_crops.py). A floor, not a count: later sittings add to it.
    expect(cards.length).toBeGreaterThanOrEqual(815);
    for (const card of cards) {
      expect(card.rows.length, `${card.id}: no rows`).toBeGreaterThan(0);
      const askRows = card.rows.filter(row => row.ask);
      if (!askRows.length) continue;
      // Where the scheme answers with a drawing (a flowchart, a truth table, a cam, a
      // comparator circuit, a comparison table), the card's one row is the ask itself,
      // priced at the part's tariff, and the reveal shows the scheme's print as a solution
      // figure (chem_figures.py's rule). Nothing is typed: the row is the question's own
      // words and the figure is the examiner's drawing.
      expect(card.rows, `${card.id}: an ask row stands alone`).toHaveLength(1);
      expect(askRows[0].marks, `${card.id}: the ask row carries the tariff`).toBe(card.totalMarks);
      expect(normalise(card.questionText).includes(normalise(askRows[0].verbatim)), `${card.id}: the ask row is the question`).toBe(true);
      expect('figure' in card && card.figure?.solution, `${card.id}: an ask row needs the scheme's print`).toBe(true);
    }
    // 2026 Higher, carded part by part on 2026-10-28: 83 printed asks, 83 cards, nothing
    // excluded (every-printed-ask-gets-a-card). reconcile.py measures the same thing against
    // the census; this pins it where the deck is.
    const hl2026 = cards.filter(card => card.year === 2026 && card.level === 'higher');
    expect(hl2026.length).toBeGreaterThanOrEqual(83);
    expect(technologyExclusions.filter(entry => entry.ref.startsWith('2026 '))).toEqual([]);
  });

  it('Business: the responses the scheme prints for a part are rows on the card, each lifted from the cited scheme page', () => {
    const cards = [...BUSINESS_HIGHER, ...BUSINESS_ORDINARY].filter((card): card is SecRubricCard & { rubric: BusinessRubric } => isRubricCard(card) && card.rubric.system === 'business');
    expect(cards).toHaveLength(1988);
    const normalise = (value: string) => value.normalize('NFKC').toLowerCase().replace(/[^a-z0-9]+/g, '');
    const schemes = new Map<string, { text: string; cells: Set<string> }>();
    // The scheme markdown as bus_expected.py reads it: no page heads, running footers, "(20 marks)" cells or marks column.
    const FOOT = /^\s*(?:Page \d+ of \d+|Bus\.? ?\d{4} ?\((?:OL|HL)\) ?\d+|LC Business \d{4} \((?:OL|HL)\)|Leaving Certificate\b.*|\d{1,2}\s*marks?|⟨\d+⟩|\d{1,2})\s*$/;
    const INLINE_FOOT = /\s*(?:LC Business \d{4} \((?:OL|HL)\)|Bus\.? ?\d{4} ?\((?:OL|HL)\) ?\d+|Page \d+ of \d+|Leaving Certificate(?: \d{4})?\s*[–-]\s*(?:Higher|Ordinary) Level(?: \d{4})?)\s*(?:⟨\d{1,2}⟩)?\s*/g;
    const schemeText = (year: number, level: string) => {
      const key = `${year}-${level === 'higher' ? 'hl' : 'ol'}`;
      if (!schemes.has(key)) {
        const raw = readFileSync(resolve(__dirname, '..', 'examiner-reports', 'business', 'schemes', `${key}.md`), 'utf8').replace(/\u00a0/g, ' ');
        const lines = raw.split('\n')
          .filter(line => !/^## Page \d+\s*$/.test(line))
          .map(line => line.replace(INLINE_FOOT, ' ').replace(/\s*⟨[^⟩]*⟩/g, '').replace(/\s*\(\s*\d{1,3}\s*marks?\s*\)/g, '').trim())
          .filter(line => line && !FOOT.test(line));
        // A ⟨…⟩ cell is the marks column as the extractor read it; a word in one is still a word the page prints
        // (2018 HL p. 56 holds the deductions subtotal "(18257.09)" in one), so a geometry row may use it.
        const cells = new Set([...raw.matchAll(/⟨([^⟩]*)⟩/g)].flatMap(m => m[1].split(/\s+/)).map(normalise).filter(Boolean));
        schemes.set(key, { text: normalise(lines.join(' ')), cells });
      }
      return schemes.get(key)!;
    };
    const lifted = cards.filter(card => card.rubric.expected);
    // 1,766 from the text layer (stage A), 15 from a hand-checked slice, 198 from the page's geometry (stage B: tables, ticks, rings, True/False columns).
    // The six cards without rows are the recorded exclusions in business-expected-slices.json: two image answers, a drawn organisation chart, three drawn charts.
    expect(lifted).toHaveLength(1979);
    expect(lifted.filter(card => card.rubric.expected!.lifted === 'geometry')).toHaveLength(198);
    expect(lifted.filter(card => card.rubric.expected!.lifted === 'slice')).toHaveLength(15);
    for (const card of lifted) {
      const { text: corpus, cells } = schemeText(card.year, card.level);
      const expected = card.rubric.expected!;
      expect(expected.page, card.id).toBeGreaterThan(0);
      expect(expected.items.length, card.id).toBeGreaterThan(0);
      for (const item of expected.items) {
        expect(item.text.trim().length, `${card.id}/${item.id}`).toBeGreaterThan(0);
        for (const piece of [item.text, ...(item.detail ?? [])]) {
          if (expected.lifted === 'geometry' || expected.lifted === 'slice') {
            // A row rebuilt from word positions (or cut from a hand-checked slice of them): the text layer may hold its words in another order, but it holds every one.
            for (const word of piece.split(/\s+|\s—\s/)) {
              const token = normalise(word);
              // A column label the layout hyphenated over two header lines ("Take-" / "over") is two words of the page, as bus_expected.py's gate reads it.
              const hyphenated = (t: string) => Array.from({ length: Math.max(0, t.length - 5) }, (_, k) => k + 3).some(i => corpus.includes(t.slice(0, i)) && corpus.includes(t.slice(i)));
              if (token) expect(corpus.includes(token) || cells.has(token) || hyphenated(token), `${card.id}/${item.id}: "${word}" is not a word the ${card.year} scheme prints`).toBe(true);
            }
          } else {
            expect(corpus.includes(normalise(piece)), `${card.id}/${item.id}: "${piece.slice(0, 50)}" is not lifted from the ${card.year} scheme`).toBe(true);
          }
        }
      }
    }
    // A row sits under the response it names, or in one pool the responses draw from.
    const layouts = lifted.map(card => businessExpectedLayout(card.rubric)!.kind);
    expect([layouts.filter(kind => kind === 'per-response').length, layouts.filter(kind => kind === 'pool').length]).toEqual([258, 1721]);
    // What bus_expected.py could not lift — the text-layer reason, then the slice's — each with the pages it looked at.
    // Every entry is a recorded exclusion whose slice reason carries the page evidence; a new shape here needs its own evidence.
    const review = JSON.parse(readFileSync(resolve(__dirname, '..', 'scripts', 'markbank', 'authored', 'business-expected-review.json'), 'utf8')) as Array<{ id: string; reason: string; schemePages: number[] }>;
    const reasons: Record<string, number> = {};
    for (const entry of review) reasons[entry.reason] = (reasons[entry.reason] ?? 0) + 1;
    expect(reasons).toEqual({
      "part marker; slice: excluded: The response is a drawn bar chart; the text layer prints only its title, axis values and month labels, no priced rows.": 1,
      "text layer glyph damage on the cited page; slice: excluded: The response is a drawn break-even chart; the text layer prints only its title, the axis values and the curve labels (TR, TC, FC, break-even point, margin of safety), and the curves are 73 drawn line segments.": 1,
      "the scheme prints the marker and the question but no response under it on the cited page; slice: excluded: The completed matrix structure is an image; the text layer holds only \"Managing / Director\" and the marks cells.": 1,
      "the scheme prints the marker and the question but no response under it on the cited page; slice: excluded: The matching grid (1–5 over D E A C F) is an image; the region holds one image and thirteen drawn rules and no text.": 1,
      "the scheme prints the marker and the question but no response under it on the cited page; slice: excluded: The response is an organisation chart embedded as an image; the text layer holds only the marker and the marks cell \"3,3,2,2\" between y 0.144 and 0.463.": 1,
      "workings table flattened by the text layer; slice: excluded: The response is a drawn bar chart; the text layer prints only its title, the axis values and the series label, and the bars are 61 drawn line segments.": 1,
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
